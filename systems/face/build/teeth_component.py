# coding=utf-8
u"""
Teeth Component
===============

功能
----
本模块负责构建 Face Rig 中的 Upper Teeth / Lower Teeth 刚体绑定。

这里的 Teeth 指牙齿本身，不包含 Gum。
Gum 后续直接参与 Mouth / Jaw 的 Skin 权重，不在 Teeth Component 中创建额外绑定。

制作思路
--------
牙齿本身属于刚体结构，不需要像嘴唇、脸颊一样产生柔性变形。
因此整个 Teeth Rig 使用非常明确的四层关系：

    Guide
        ↓
    Controller
        ↓
    Bind Joint
        ↓
    Teeth Model

其中：

1. Guide
    只负责确定 Upper / Lower Teeth 的初始位置和方向。

2. Controller
    给动画师提供最终可操作的控制器。
    Upper / Lower Teeth 各自有一个独立 Controller。

3. Bind Joint
    Controller 不直接驱动模型，而是先驱动一个 Teeth Bind Joint。
    这样后续 Jaw、Mouth、Export Skeleton 都可以继续围绕 Joint 扩展。

4. Teeth Model
    Upper Teeth Model 只绑定 Upper Teeth Joint；
    Lower Teeth Model 只绑定 Lower Teeth Joint；
    每个牙齿模型都是单 Influence SkinCluster，因此权重始终为 1.0。

为什么使用 Matrix 驱动
----------------------
Controller -> Joint 使用 matrix_utils.create_parent_matrix_constraint()：

    ctrl.worldMatrix
        ↓
    multMatrix
        ↓
    joint.offsetParentMatrix

这样可以避免传统 parentConstraint 产生额外 Constraint Node，
同时保持 Teeth Rig 的驱动关系清晰、可查询、可程序化重建。

为什么 Gum 不在这里绑定
-----------------------
Gum 是口腔软组织的一部分，它应该同时受到 Mouth / Jaw 等变形骨骼影响。
如果在 Teeth Component 中给 Gum 单独创建 Teeth SkinCluster，会把它错误地变成牙齿刚体。

因此这里明确规定：

    Teeth Component
        -> 只处理 Upper / Lower Teeth

    Mouth / Jaw Deformation
        -> 后续处理 Gum Skin 权重

后续 Jaw 接入方式
----------------
当前 Lower Teeth Controller 的 top_group 会被保留下来。
Jaw Component 完成以后，只需要让 Jaw 驱动 Lower Teeth Controller 的上层 Follow Group，
就可以实现：

    Jaw
        ↓
    Lower Teeth Controller Hierarchy
        ↓
    Lower Teeth Joint
        ↓
    Lower Teeth Model

而不需要重新修改 Teeth Component 内部的 Controller -> Joint 逻辑。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import joint_utils
from ....core import matrix_utils
from ....core import name_utils
from ....core import scene_utils
from ....core import skin_utils
from ...controller import builder as controller_builder
from .. import config
from .. import face_base
from ..guide import FaceGuide


class TeethComponent(face_base.FaceBase):
    u"""构建 Upper / Lower Teeth 刚体 Rig。"""

    def __init__(self):
        u"""初始化 Teeth Component 的输入、命名和构建结果。"""
        super(TeethComponent, self).__init__()

        # =====================================================================
        # Guide
        # =====================================================================
        self.face_guide = FaceGuide()

        self.upper_teeth_guide_name = None
        self.lower_teeth_guide_name = None

        self.upper_teeth_guide = None
        self.lower_teeth_guide = None

        # =====================================================================
        # Build Name
        # =====================================================================
        self.upper_teeth_jnt_name = None
        self.lower_teeth_jnt_name = None

        self.upper_teeth_ctrl_name = None
        self.lower_teeth_ctrl_name = None

        self.upper_teeth_matrix_name = None
        self.lower_teeth_matrix_name = None

        self.upper_teeth_skin_name = None
        self.lower_teeth_skin_name = None

        # =====================================================================
        # Controller Setting
        # =====================================================================
        self.controller_global_scale = 1.0
        self.controller_color = 17
        self.controller_size = 1.0
        self.controller_radius = 1.0

        # =====================================================================
        # Build Result - Joint
        # =====================================================================
        self.upper_teeth_joint = None
        self.lower_teeth_joint = None

        # =====================================================================
        # Build Result - Controller
        # =====================================================================
        self.upper_teeth_controller = None
        self.lower_teeth_controller = None

        self.upper_teeth_control = None
        self.lower_teeth_control = None

        # 保留 top_group，后续 Jaw Component 会从这里接入 Follow。
        self.upper_teeth_top_group = None
        self.lower_teeth_top_group = None

        # =====================================================================
        # Build Result - Matrix
        # =====================================================================
        self.upper_teeth_matrix_node = None
        self.lower_teeth_matrix_node = None

        # =====================================================================
        # Build Result - Skin
        # =====================================================================
        self.upper_teeth_skin_cluster = None
        self.lower_teeth_skin_cluster = None

    # =========================================================================
    # Step 01 - Collect Inputs
    # =========================================================================

    def collect_inputs(self):
        u"""
        收集 Teeth Component 构建需要的 Setup、Guide 和 Controller Settings。

        制作思路：
            Teeth Build 不应该依赖当前 Selection。
            所有输入都来自 Step 01 保存的数据和 Step 02 的标准 Guide。

        Returns:
            bool:
                所有输入读取成功后返回 True。
        """

        # ---------------------------------------------------------------------
        # Step 01：读取 Step 01 Face Setup 数据
        # ---------------------------------------------------------------------
        # 这里会刷新：
        #     self.upper_teech_model
        #     self.lower_teech_model
        #
        # Teeth Model 允许为空。
        # 这样可以先构建 Rig，再晚一点接模型。
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )

        # ---------------------------------------------------------------------
        # Step 02：生成标准 Teeth Guide 名称
        # ---------------------------------------------------------------------
        # Guide 名称不直接写死，统一通过 name_utils 生成。
        # 这样命名规则修改时，Face System 不需要到处改字符串。
        self.upper_teeth_guide_name = name_utils.Name.create_name(
            node_type="loc",
            side="md",
            part="upper_teeth",
            function="guide",
            index=1
        )

        self.lower_teeth_guide_name = name_utils.Name.create_name(
            node_type="loc",
            side="md",
            part="lower_teeth",
            function="guide",
            index=1
        )

        # ---------------------------------------------------------------------
        # Step 03：获取 Upper / Lower Teeth Guide
        # ---------------------------------------------------------------------
        # Teeth Joint 和 Controller 都会从 Guide 获取初始位置和旋转。
        # 因此这两个 Guide 是 Teeth Component 的必须输入。
        self.upper_teeth_guide = self.face_guide.get_guide_node(
            self.upper_teeth_guide_name,
            required=True
        )

        self.lower_teeth_guide = self.face_guide.get_guide_node(
            self.lower_teeth_guide_name,
            required=True
        )

        # ---------------------------------------------------------------------
        # Step 04：读取 Controller Settings
        # ---------------------------------------------------------------------
        # Controller Settings 来自 Face Guide Config。
        # Teeth 不自己定义另一套颜色和尺寸规则。
        controller_settings = self.face_guide.load_controller_settings()

        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )

        self.controller_color = controller_settings.get(
            config.face_controller_color_attr_names["md"],
            17
        )

        self.controller_size = controller_settings.get(
            config.face_controller_size_attr_names["teeth"],
            1.0
        )

        return True

    # =========================================================================
    # Step 02 - Prepare Build Data
    # =========================================================================

    def prepare_data(self):
        u"""
        准备 Teeth Build 使用的层级、名称和安全检查数据。

        制作思路：
            所有可能失败的检查尽量放在真正创建 Maya 节点之前。
            这样出错时不会留下半套 Teeth Rig。

        Returns:
            bool:
                构建前准备完成后返回 True。
        """

        # ---------------------------------------------------------------------
        # Step 01：确保 Face Rig 标准层级存在
        # ---------------------------------------------------------------------
        # Teeth Joint 会进入 face_jnt_grp。
        # Teeth Controller 会进入 face_ctrl_grp。
        self.ensure_hierarchy()

        # ---------------------------------------------------------------------
        # Step 02：准备所有确定性节点名称
        # ---------------------------------------------------------------------
        self._prepare_names()

        # ---------------------------------------------------------------------
        # Step 03：计算 Teeth Controller 最终半径
        # ---------------------------------------------------------------------
        # 最终尺寸 = Face 全局控制器缩放 × Teeth 局部尺寸。
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(
                u"Teeth Controller Radius 必须大于 0。"
            )

        # ---------------------------------------------------------------------
        # Step 04：检查 Upper / Lower Teeth Model 是否误用了同一个模型
        # ---------------------------------------------------------------------
        self._validate_model_inputs_unique()

        # ---------------------------------------------------------------------
        # Step 05：检查场景中是否残留旧 Teeth Rig 节点
        # ---------------------------------------------------------------------
        # Controller Builder 如果遇到重名，Maya 可能自动生成 _001 / _002。
        # 对自动 Rig 来说这种静默重命名非常危险，因此这里提前阻止。
        self._validate_build_nodes_available()

        # ---------------------------------------------------------------------
        # Step 06：检查牙齿模型现有 SkinCluster
        # ---------------------------------------------------------------------
        # Teeth Component 不会删除或覆盖艺术家已有的未知 SkinCluster。
        self._validate_model_skin_state(
            self.upper_teech_model,
            label=u"Upper Teeth Model"
        )

        self._validate_model_skin_state(
            self.lower_teech_model,
            label=u"Lower Teeth Model"
        )

        return True

    def _prepare_names(self):
        u"""准备 Teeth Rig 所有确定性标准名称。"""

        # ---------------------------------------------------------------------
        # Step 01：Joint Name
        # ---------------------------------------------------------------------
        self.upper_teeth_jnt_name = name_utils.Name.create_name(
            node_type="jnt",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )

        self.lower_teeth_jnt_name = name_utils.Name.create_name(
            node_type="jnt",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        # ---------------------------------------------------------------------
        # Step 02：Controller Name
        # ---------------------------------------------------------------------
        self.upper_teeth_ctrl_name = name_utils.Name.create_name(
            node_type="ctrl",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )

        self.lower_teeth_ctrl_name = name_utils.Name.create_name(
            node_type="ctrl",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        # ---------------------------------------------------------------------
        # Step 03：Matrix Node Name
        # ---------------------------------------------------------------------
        self.upper_teeth_matrix_name = name_utils.Name.create_name(
            node_type="mult",
            side="md",
            part="upper_teeth",
            function="parent",
            index=1
        )

        self.lower_teeth_matrix_name = name_utils.Name.create_name(
            node_type="mult",
            side="md",
            part="lower_teeth",
            function="parent",
            index=1
        )

        # ---------------------------------------------------------------------
        # Step 04：SkinCluster Name
        # ---------------------------------------------------------------------
        self.upper_teeth_skin_name = name_utils.Name.create_name(
            node_type="skin",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )

        self.lower_teeth_skin_name = name_utils.Name.create_name(
            node_type="skin",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        return True

    # =========================================================================
    # Build Validation
    # =========================================================================

    @staticmethod
    def _get_controller_hierarchy_names(control_name):
        u"""
        返回 Controller Builder 会创建的完整标准层级名称。

        制作思路：
            Teeth Build 必须保证节点名称完全确定。
            因此构建前需要把 Controller Builder 会生成的所有节点都检查一遍。
        """
        prefixes = [
            "ctrl",
            "offset",
            "connect",
            "space",
            "driven",
            "zero",
            "output",
        ]
        node_names = []

        for prefix in prefixes:
            if prefix == "ctrl":
                node_name = control_name
            else:
                node_name = control_name.replace(
                    "ctrl_",
                    prefix + "_",
                    1
                )

            node_names.append(
                node_name
            )

        return node_names

    def _validate_model_inputs_unique(self):
        u"""检查 Upper / Lower Teeth 是否误指向同一个模型 Transform。"""
        model_inputs = [
            (u"Upper Teeth Model", self.upper_teech_model),
            (u"Lower Teeth Model", self.lower_teech_model),
        ]
        resolved_models = {}

        for label, model in model_inputs:
            if not model:
                continue

            long_name = scene_utils.get_long_name(
                model
            )

            if long_name in resolved_models:
                other_label = resolved_models[long_name]

                raise RuntimeError(
                    u"{} 与 {} 指向同一个模型：{}。Upper / Lower Teeth 必须是独立输入。".format(
                        other_label,
                        label,
                        long_name
                    )
                )

            resolved_models[long_name] = label

        return True

    def _validate_build_nodes_available(self):
        u"""检查 Teeth Rig 是否已经存在或存在同名残留节点。"""
        expected_nodes = [
            self.upper_teeth_jnt_name,
            self.lower_teeth_jnt_name,
            self.upper_teeth_matrix_name,
            self.lower_teeth_matrix_name,
        ]

        if self.upper_teech_model:
            expected_nodes.append(
                self.upper_teeth_skin_name
            )

        if self.lower_teech_model:
            expected_nodes.append(
                self.lower_teeth_skin_name
            )

        upper_control_nodes = self._get_controller_hierarchy_names(
            self.upper_teeth_ctrl_name
        )

        lower_control_nodes = self._get_controller_hierarchy_names(
            self.lower_teeth_ctrl_name
        )

        for node_name in upper_control_nodes:
            expected_nodes.append(
                node_name
            )

        for node_name in lower_control_nodes:
            expected_nodes.append(
                node_name
            )

        existing_nodes = []

        for node_name in expected_nodes:
            if not cmds.objExists(node_name):
                continue

            existing_nodes.append(
                node_name
            )

        if existing_nodes:
            raise RuntimeError(
                u"Teeth Rig 已存在或存在同名残留节点，请先清理后再构建：{}".format(
                    ", ".join(existing_nodes)
                )
            )

        return True

    @staticmethod
    def _validate_model_skin_state(model, label):
        u"""检查 Teeth Model 是否已经存在 SkinCluster。"""
        if not model:
            return True

        skin_cluster = skin_utils.find_skin_cluster(
            model
        )

        if not skin_cluster:
            return True

        raise RuntimeError(
            u"{} 已经存在 SkinCluster：{}。Teeth Component 不会自动覆盖已有权重。".format(
                label,
                skin_cluster
            )
        )

    # =========================================================================
    # Step 03 - Create Joint
    # =========================================================================

    def create_joint(self):
        u"""
        根据 Upper / Lower Teeth Guide 创建两个 Bind Joint。

        制作思路：
            Upper 和 Lower Teeth 是两个独立刚体，因此创建两个互不 Parent 的 Joint。
            两个 Joint 都统一放入 face_jnt_grp。

        Returns:
            list[str]:
                按 Upper、Lower 顺序返回创建完成的 Joint。
        """

        # ---------------------------------------------------------------------
        # Step 01：计算 Joint 显示半径
        # ---------------------------------------------------------------------
        # Joint Radius 只影响 Maya Viewport 显示，不参与绑定计算。
        joint_radius = self.controller_radius * 0.25

        # ---------------------------------------------------------------------
        # Step 02：创建 Upper Teeth Joint
        # ---------------------------------------------------------------------
        self.upper_teeth_joint = joint_utils.Joint.create_at_object(
            obj=self.upper_teeth_guide,
            name=self.upper_teeth_jnt_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=joint_radius
        )

        # ---------------------------------------------------------------------
        # Step 03：创建 Lower Teeth Joint
        # ---------------------------------------------------------------------
        self.lower_teeth_joint = joint_utils.Joint.create_at_object(
            obj=self.lower_teeth_guide,
            name=self.lower_teeth_jnt_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=joint_radius
        )

        return [
            self.upper_teeth_joint,
            self.lower_teeth_joint,
        ]

    # =========================================================================
    # Step 04 - Create Controller
    # =========================================================================

    def create_controller(self):
        u"""
        创建 Upper / Lower Teeth 的标准 Controller Hierarchy。

        制作思路：
            Controller 只负责动画输入。
            Controller 不直接 Skin 模型，而是通过 Matrix 驱动对应 Bind Joint。

            当前关闭 Sub Control，因为 Teeth 是简单刚体控制，不需要第二层局部控制。

        Returns:
            list[dict]:
                按 Upper、Lower 顺序返回 Controller Builder 结果。
        """

        # ---------------------------------------------------------------------
        # Step 01：创建 Upper Teeth Controller
        # ---------------------------------------------------------------------
        self.upper_teeth_controller = controller_builder.create_controller(
            name=self.upper_teeth_ctrl_name,
            shape="circle",
            radius=self.controller_radius,
            axis="Z+",
            target=self.upper_teeth_guide,
            parent=self.face_ctrl_grp,
            color=self.controller_color,
            create_sub_control=False,
            create_extra_groups=True,
            add_to_set=True,
            control_set=config.face_ctrl_set
        )

        # ---------------------------------------------------------------------
        # Step 02：创建 Lower Teeth Controller
        # ---------------------------------------------------------------------
        self.lower_teeth_controller = controller_builder.create_controller(
            name=self.lower_teeth_ctrl_name,
            shape="circle",
            radius=self.controller_radius,
            axis="Z+",
            target=self.lower_teeth_guide,
            parent=self.face_ctrl_grp,
            color=self.controller_color,
            create_sub_control=False,
            create_extra_groups=True,
            add_to_set=True,
            control_set=config.face_ctrl_set
        )

        # ---------------------------------------------------------------------
        # Step 03：保存后续连接需要的关键节点
        # ---------------------------------------------------------------------
        self.upper_teeth_control = self.upper_teeth_controller["control"]
        self.lower_teeth_control = self.lower_teeth_controller["control"]

        self.upper_teeth_top_group = self.upper_teeth_controller["top_group"]
        self.lower_teeth_top_group = self.lower_teeth_controller["top_group"]

        return [
            self.upper_teeth_controller,
            self.lower_teeth_controller,
        ]

    # =========================================================================
    # Step 05 - Create Connection
    # =========================================================================

    def create_connection(self):
        u"""
        建立 Controller -> Joint -> Teeth Model 的完整驱动链。

        制作思路：

            Upper：
                Upper Control
                    ↓ Matrix
                Upper Teeth Joint
                    ↓ Skin 1.0
                Upper Teeth Model

            Lower：
                Lower Control
                    ↓ Matrix
                Lower Teeth Joint
                    ↓ Skin 1.0
                Lower Teeth Model

        Returns:
            bool:
                Matrix 和可选 Teeth Skin 全部创建完成后返回 True。
        """

        # ---------------------------------------------------------------------
        # Step 01：Upper Controller -> Upper Joint
        # ---------------------------------------------------------------------
        # 两个 Teeth Controller 都关闭了 Sub Control。
        # 因此可见 Control 的 worldMatrix 就是最终动画矩阵。
        self.upper_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.upper_teeth_control,
            driven=self.upper_teeth_joint,
            maintain_offset=False,
            name=self.upper_teeth_matrix_name
        )

        # ---------------------------------------------------------------------
        # Step 02：Lower Controller -> Lower Joint
        # ---------------------------------------------------------------------
        self.lower_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.lower_teeth_control,
            driven=self.lower_teeth_joint,
            maintain_offset=False,
            name=self.lower_teeth_matrix_name
        )

        # ---------------------------------------------------------------------
        # Step 03：Upper Joint -> Upper Teeth Model
        # ---------------------------------------------------------------------
        # Teeth 是刚体，所以只有一个 Influence，所有 Vertex 权重都是 1.0。
        self.upper_teeth_skin_cluster = self._create_rigid_skin_cluster(
            model=self.upper_teech_model,
            joint=self.upper_teeth_joint,
            skin_name=self.upper_teeth_skin_name
        )

        # ---------------------------------------------------------------------
        # Step 04：Lower Joint -> Lower Teeth Model
        # ---------------------------------------------------------------------
        self.lower_teeth_skin_cluster = self._create_rigid_skin_cluster(
            model=self.lower_teech_model,
            joint=self.lower_teeth_joint,
            skin_name=self.lower_teeth_skin_name
        )

        return True

    @staticmethod
    def _create_rigid_skin_cluster(
            model,
            joint,
            skin_name
    ):
        u"""
        使用一个 Joint 创建 Teeth 刚性 SkinCluster。

        制作思路：
            Teeth 不需要 Smooth Weight。
            一个模型只允许一个 Influence，因此所有 Vertex 始终完整跟随对应 Teeth Joint。
        """
        if not model:
            return None

        existing_skin_cluster = skin_utils.find_skin_cluster(
            model
        )

        if existing_skin_cluster:
            raise RuntimeError(
                u"模型已经存在 SkinCluster：{}".format(
                    existing_skin_cluster
                )
            )

        skin_result = cmds.skinCluster(
            joint,
            model,
            name=skin_name,
            toSelectedBones=True,
            bindMethod=0,
            skinMethod=0,
            normalizeWeights=1,
            maximumInfluences=1,
            obeyMaxInfluences=True
        )

        if not skin_result:
            raise RuntimeError(
                u"创建 Teeth SkinCluster 失败：{}".format(
                    model
                )
            )

        return skin_result[0]

    # =========================================================================
    # Step 06 - Finalize
    # =========================================================================

    def finalize_step(self):
        u"""
        检查 Teeth Component 的最终构建结果。

        制作思路：
            Build 方法没有报错不代表结果一定完整。
            Finalize 再检查一次关键 Rig Node 和可选 SkinCluster，
            可以尽早发现 Maya 命令静默失败或场景状态异常。

        Returns:
            bool:
                所有必须结果有效时返回 True。
        """

        # ---------------------------------------------------------------------
        # Step 01：检查必须存在的 Rig Node
        # ---------------------------------------------------------------------
        required_nodes = [
            self.upper_teeth_joint,
            self.lower_teeth_joint,
            self.upper_teeth_control,
            self.lower_teeth_control,
            self.upper_teeth_matrix_node,
            self.lower_teeth_matrix_node,
        ]

        for node in required_nodes:
            if not node:
                raise RuntimeError(
                    u"Teeth Component 构建结果不完整。"
                )

            if not cmds.objExists(node):
                raise RuntimeError(
                    u"Teeth Component 构建节点不存在：{}".format(
                        node
                    )
                )

        # ---------------------------------------------------------------------
        # Step 02：检查 Upper Teeth Skin
        # ---------------------------------------------------------------------
        self._validate_skin_result(
            model=self.upper_teech_model,
            skin_cluster=self.upper_teeth_skin_cluster,
            label=u"Upper Teeth"
        )

        # ---------------------------------------------------------------------
        # Step 03：检查 Lower Teeth Skin
        # ---------------------------------------------------------------------
        self._validate_skin_result(
            model=self.lower_teech_model,
            skin_cluster=self.lower_teeth_skin_cluster,
            label=u"Lower Teeth"
        )

        return True

    @staticmethod
    def _validate_skin_result(
            model,
            skin_cluster,
            label
    ):
        u"""检查一个可选 Teeth Model 的 SkinCluster 构建结果。"""
        if not model:
            return True

        if not skin_cluster:
            raise RuntimeError(
                u"{} Model 没有完成 Skin 绑定。".format(
                    label
                )
            )

        if not cmds.objExists(skin_cluster):
            raise RuntimeError(
                u"{} SkinCluster 不存在：{}".format(
                    label,
                    skin_cluster
                )
            )

        return True


__all__ = [
    "TeethComponent",
]
