# coding=utf-8
u"""
Teeth Component
===============

用于构建上下牙床与 Gum 的 Face Rig Component。

继承关系：
    ComponentBase
        -> RigComponentBase
            -> FaceBase
                -> TeethComponent

标准构建顺序：
    1. create_joint()；
    2. create_controller()；
    3. create_connection()。

当前职责：
    - 根据 Teeth Guide 创建 Upper / Lower Teeth Bind Joint；
    - 创建 Upper / Lower Teeth Controller Hierarchy；
    - 使用 Matrix Network 建立 Controller -> Joint 驱动；
    - 对独立 Upper / Lower Teeth Model 创建单 Influence 刚性 SkinCluster；
    - 调用 gum_binding 完成 Gum Connected Shell 分类与双 Influence 刚性权重；
    - 保留 Lower Teeth Controller Top Group，供后续 Jaw Component 接管 Follow。

边界：
    - Teeth Component 负责 Rig 生命周期与节点关系；
    - Gum Mesh Shell 几何分析和 Gum 权重算法放在 gum_binding.py；
    - 不覆盖已有未知 SkinCluster；
    - 不使用 Maya 默认 Smooth Bind 结果作为最终牙床权重。
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
from . import gum_binding


class TeethComponent(face_base.FaceBase):
    u"""Step 03 中负责 Upper / Lower Teeth 与 Gum 的 Rig Component。"""

    def __init__(self):
        u"""初始化 Teeth Component。"""
        super(TeethComponent, self).__init__()

        self.face_guide = FaceGuide()

        # ---------------------------------------------------------------------
        # Guide
        # ---------------------------------------------------------------------
        self.upper_teeth_guide_name = None
        self.lower_teeth_guide_name = None
        self.upper_teeth_guide = None
        self.lower_teeth_guide = None

        # ---------------------------------------------------------------------
        # Build Name
        # ---------------------------------------------------------------------
        self.upper_teeth_jnt_name = None
        self.lower_teeth_jnt_name = None
        self.upper_teeth_ctrl_name = None
        self.lower_teeth_ctrl_name = None
        self.upper_teeth_matrix_name = None
        self.lower_teeth_matrix_name = None
        self.upper_teeth_skin_name = None
        self.lower_teeth_skin_name = None
        self.gum_skin_name = None

        # ---------------------------------------------------------------------
        # Controller Setting
        # ---------------------------------------------------------------------
        self.controller_global_scale = 1.0
        self.controller_color = 17
        self.controller_size = 1.0
        self.controller_radius = 1.0

        # ---------------------------------------------------------------------
        # Prepared Gum Data
        # ---------------------------------------------------------------------
        self.gum_shell_data = []

        # ---------------------------------------------------------------------
        # Build Result
        # ---------------------------------------------------------------------
        self.upper_teeth_joint = None
        self.lower_teeth_joint = None

        self.upper_teeth_controller = None
        self.lower_teeth_controller = None
        self.upper_teeth_control = None
        self.lower_teeth_control = None
        self.upper_teeth_top_group = None
        self.lower_teeth_top_group = None

        self.upper_teeth_matrix_node = None
        self.lower_teeth_matrix_node = None

        self.upper_teeth_skin_cluster = None
        self.lower_teeth_skin_cluster = None
        self.gum_skin_cluster = None

    # =========================================================================
    # Input / Prepare
    # =========================================================================

    def collect_inputs(self):
        u"""
        收集并检查 Teeth Component 所需输入。

        Returns:
            bool:
                Setup、Guide 和 Controller Settings 全部读取成功后返回 True。
        """
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )

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

        self.upper_teeth_guide = self.face_guide.get_guide_node(
            self.upper_teeth_guide_name,
            required=True
        )

        self.lower_teeth_guide = self.face_guide.get_guide_node(
            self.lower_teeth_guide_name,
            required=True
        )

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

    def prepare_data(self):
        u"""
        准备 Teeth 名称、层级、Gum Shell 数据和构建前安全检查。

        Returns:
            bool:
                所有构建数据准备完成后返回 True。
        """
        self.ensure_hierarchy()
        self._prepare_names()

        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(
                u"Teeth Controller Radius 必须大于 0。"
            )

        self._validate_model_inputs_unique()
        self._validate_build_nodes_available()

        self._validate_model_skin_state(
            self.upper_teech_model,
            label=u"Upper Teeth Model"
        )

        self._validate_model_skin_state(
            self.lower_teech_model,
            label=u"Lower Teeth Model"
        )

        self._validate_model_skin_state(
            self.face_gum_model,
            label=u"Gum Model"
        )

        # 在创建任何 Rig 节点前先验证 Gum 拓扑和 Shell 分类。
        # 如果 Gum 不符合自动绑定条件，本次构建会在干净状态直接停止。
        self.gum_shell_data = gum_binding.prepare_gum_shell_data(
            model=self.face_gum_model,
            upper_reference=self.upper_teeth_guide,
            lower_reference=self.lower_teeth_guide
        )

        return True

    def _prepare_names(self):
        u"""准备 Teeth / Gum 构建使用的确定性标准名称。"""
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

        self.gum_skin_name = name_utils.Name.create_name(
            node_type="skin",
            side="md",
            part="gum",
            function="bind",
            index=1
        )

        return True

    # =========================================================================
    # Build Validation
    # =========================================================================

    @staticmethod
    def _get_controller_hierarchy_names(control_name):
        u"""返回标准 Controller Builder 会创建的确定性节点名称。"""
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
        u"""确保 Upper Teeth、Lower Teeth 与 Gum 没有误指向同一个 Transform。"""
        model_inputs = [
            (u"Upper Teeth Model", self.upper_teech_model),
            (u"Lower Teeth Model", self.lower_teech_model),
            (u"Gum Model", self.face_gum_model),
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
                    u"{} 与 {} 指向同一个模型：{}。当前 Teeth Rig 需要独立输入。".format(
                        other_label,
                        label,
                        long_name
                    )
                )

            resolved_models[long_name] = label

        return True

    def _validate_build_nodes_available(self):
        u"""阻止旧 Teeth Rig 残留导致 Builder 静默生成带后缀的重复节点。"""
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

        if self.face_gum_model:
            expected_nodes.append(
                self.gum_skin_name
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
        u"""构建前拒绝覆盖模型上已经存在的未知 SkinCluster。"""
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
    # Joint
    # =========================================================================

    def create_joint(self):
        u"""
        根据 Teeth Guide 创建 Upper / Lower Teeth Bind Joint。

        Returns:
            list[str]:
                按 Upper、Lower 顺序返回创建完成的两个 Joint。
        """
        joint_radius = self.controller_radius * 0.25

        self.upper_teeth_joint = joint_utils.Joint.create_at_object(
            obj=self.upper_teeth_guide,
            name=self.upper_teeth_jnt_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=joint_radius
        )

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
    # Controller
    # =========================================================================

    def create_controller(self):
        u"""
        创建 Upper / Lower Teeth 标准 Controller Hierarchy。

        Returns:
            list[dict]:
                按 Upper、Lower 顺序返回 Controller Builder 的结果字典。
        """
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

        self.upper_teeth_control = self.upper_teeth_controller["control"]
        self.lower_teeth_control = self.lower_teeth_controller["control"]
        self.upper_teeth_top_group = self.upper_teeth_controller["top_group"]
        self.lower_teeth_top_group = self.lower_teeth_controller["top_group"]

        return [
            self.upper_teeth_controller,
            self.lower_teeth_controller,
        ]

    # =========================================================================
    # Connection
    # =========================================================================

    def create_connection(self):
        u"""
        建立 Teeth Controller、Joint、独立牙齿模型和 Gum 的驱动关系。

        Returns:
            bool:
                Matrix 驱动与全部可选 Skin 构建完成后返回 True。
        """
        # 两个 Teeth Controller 都关闭 Sub Control，因此可见 Control 的 worldMatrix
        # 就是最终动画矩阵。直接使用 Control 可避免依赖额外 Output 层级语义。
        self.upper_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.upper_teeth_control,
            driven=self.upper_teeth_joint,
            maintain_offset=False,
            name=self.upper_teeth_matrix_name
        )

        self.lower_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.lower_teeth_control,
            driven=self.lower_teeth_joint,
            maintain_offset=False,
            name=self.lower_teeth_matrix_name
        )

        self.upper_teeth_skin_cluster = self._create_rigid_skin_cluster(
            model=self.upper_teech_model,
            joint=self.upper_teeth_joint,
            skin_name=self.upper_teeth_skin_name
        )

        self.lower_teeth_skin_cluster = self._create_rigid_skin_cluster(
            model=self.lower_teech_model,
            joint=self.lower_teeth_joint,
            skin_name=self.lower_teeth_skin_name
        )

        self.gum_skin_cluster = gum_binding.create_gum_skin_cluster(
            model=self.face_gum_model,
            upper_joint=self.upper_teeth_joint,
            lower_joint=self.lower_teeth_joint,
            skin_name=self.gum_skin_name,
            shell_data=self.gum_shell_data
        )

        return True

    @staticmethod
    def _create_rigid_skin_cluster(
            model,
            joint,
            skin_name
    ):
        u"""使用单个 Joint 创建全权重为 1 的刚性 Teeth SkinCluster。"""
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
    # Finalize
    # =========================================================================

    def finalize_step(self):
        u"""
        检查 Teeth Component 最终节点与可选 SkinCluster。

        Returns:
            bool:
                所有必须结果都存在时返回 True。
        """
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

        self._validate_skin_result(
            model=self.upper_teech_model,
            skin_cluster=self.upper_teeth_skin_cluster,
            label=u"Upper Teeth"
        )

        self._validate_skin_result(
            model=self.lower_teech_model,
            skin_cluster=self.lower_teeth_skin_cluster,
            label=u"Lower Teeth"
        )

        self._validate_skin_result(
            model=self.face_gum_model,
            skin_cluster=self.gum_skin_cluster,
            label=u"Gum"
        )

        return True

    @staticmethod
    def _validate_skin_result(
            model,
            skin_cluster,
            label
    ):
        u"""检查可选模型对应的 SkinCluster 构建结果。"""
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
