# coding=utf-8
u"""
Teeth Component
===============

用于构建上下牙床的 Face Rig Component。

继承关系：
    ComponentBase
        -> RigComponentBase
            -> FaceBase
                -> TeethComponent

Teeth Component 使用 RigComponentBase 提供的标准 process_data()：
    1. create_joint()；
    2. create_controller()；
    3. create_connection()。

当前职责：
    - 根据 Teeth Guide 创建上下牙床绑定 Joint；
    - 创建上下牙床标准 Controller Hierarchy；
    - 使用 Matrix Network 建立 Controller Output -> Joint 驱动；
    - 对独立 Upper / Lower Teeth Model 创建单 Influence 刚性 SkinCluster；
    - 保留 Lower Teeth Controller Top Group，供后续 Jaw Component 接管 Follow。

重要边界：
    - 单独的 Gum Model 可能同时包含上下牙龈，不能直接当作一个刚体处理；
    - Gum 的双 Influence 分区属于下一层明确权重 Workflow，不使用 Maya 默认 Smooth Bind 猜权重；
    - 本 Component 不修改已有的未知 SkinCluster，避免破坏艺术家已有权重。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import joint_utils
from ....core import matrix_utils
from ....core import name_utils
from ....core import skin_utils
from ...controller import builder as controller_builder
from .. import config
from .. import face_base
from ..guide import FaceGuide


class TeethComponent(face_base.FaceBase):
    u"""Step 03 中的 Teeth Rig Component。"""

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

        # ---------------------------------------------------------------------
        # Controller Setting
        # ---------------------------------------------------------------------
        self.controller_global_scale = 1.0
        self.controller_color = 17
        self.controller_size = 1.0
        self.controller_radius = 1.0

        # ---------------------------------------------------------------------
        # Build Result
        # ---------------------------------------------------------------------
        self.upper_teeth_joint = None
        self.lower_teeth_joint = None

        self.upper_teeth_controller = None
        self.lower_teeth_controller = None

        self.upper_teeth_control = None
        self.lower_teeth_control = None
        self.upper_teeth_output = None
        self.lower_teeth_output = None
        self.upper_teeth_top_group = None
        self.lower_teeth_top_group = None

        self.upper_teeth_matrix_node = None
        self.lower_teeth_matrix_node = None

        self.upper_teeth_skin_cluster = None
        self.lower_teeth_skin_cluster = None

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

        # =========================================================================
        # 步骤 1：检查 Step 01 Setup 数据
        # =========================================================================

        self.validate_setup_config(
            require_mouth_jnt_number=False
        )

        # =========================================================================
        # 步骤 2：动态生成必须的 Teeth Guide 名称
        # =========================================================================

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

        # =========================================================================
        # 步骤 3：获取并检查 Guide
        # =========================================================================

        self.upper_teeth_guide = self.face_guide.get_guide_node(
            self.upper_teeth_guide_name,
            required=True
        )

        self.lower_teeth_guide = self.face_guide.get_guide_node(
            self.lower_teeth_guide_name,
            required=True
        )

        # =========================================================================
        # 步骤 4：读取 Controller Settings
        # =========================================================================

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
        准备 Teeth Joint / Controller 名称、层级和构建前检查数据。

        Returns:
            bool:
                命名、层级与构建前安全检查全部完成后返回 True。
        """

        # 确保 Face 的正式层级存在。
        self.ensure_hierarchy()

        # ---------------------------------------------------------------------
        # Joint Name
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
        # Controller Name
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
        # Rig Node Name
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

        # ---------------------------------------------------------------------
        # Controller Radius
        # ---------------------------------------------------------------------
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(
                u"Teeth Controller Radius 必须大于 0。"
            )

        # ---------------------------------------------------------------------
        # Build 前安全检查
        # ---------------------------------------------------------------------
        self._validate_build_nodes_available()
        self._validate_model_skin_state(
            self.upper_teech_model,
            label=u"Upper Teeth Model"
        )
        self._validate_model_skin_state(
            self.lower_teech_model,
            label=u"Lower Teeth Model"
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
                if control_name.startswith("ctrl_"):
                    node_name = control_name.replace(
                        "ctrl_",
                        prefix + "_",
                        1
                    )
                else:
                    node_name = "{}_{}".format(
                        prefix,
                        control_name
                    )

            node_names.append(
                node_name
            )

        return node_names

    def _validate_build_nodes_available(self):
        u"""阻止旧 Teeth Rig 残留导致 Builder 静默生成带后缀的重复节点。"""
        expected_nodes = [
            self.upper_teeth_jnt_name,
            self.lower_teeth_jnt_name,
            self.upper_teeth_matrix_name,
            self.lower_teeth_matrix_name,
            self.upper_teeth_skin_name,
            self.lower_teeth_skin_name,
        ]

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
            if not node_name:
                continue

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
        根据 Teeth Guide 创建上下牙床绑定 Joint。

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
        创建上下牙床对应的标准 Controller Hierarchy。

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

        self.upper_teeth_output = self.upper_teeth_controller["output"]
        self.lower_teeth_output = self.lower_teeth_controller["output"]

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
        建立 Teeth Controller、Joint 和独立牙齿模型之间的驱动关系。

        Returns:
            bool:
                上下牙床 Matrix 驱动及可选模型刚性 Skin 全部完成后返回 True。
        """

        # ---------------------------------------------------------------------
        # Controller Output -> Joint
        # ---------------------------------------------------------------------
        self.upper_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.upper_teeth_output,
            driven=self.upper_teeth_joint,
            maintain_offset=False,
            name=self.upper_teeth_matrix_name
        )

        self.lower_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.lower_teeth_output,
            driven=self.lower_teeth_joint,
            maintain_offset=False,
            name=self.lower_teeth_matrix_name
        )

        # ---------------------------------------------------------------------
        # Joint -> Teeth Model
        # ---------------------------------------------------------------------
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

        return True

    @staticmethod
    def _create_rigid_skin_cluster(
            model,
            joint,
            skin_name
    ):
        u"""使用单个 Joint 创建全权重为 1 的刚性 SkinCluster。"""
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
        检查 Teeth Component 最终结果并整理显示 / Metadata。

        Returns:
            bool:
                必须节点及可选牙齿模型 Skin 结果全部有效时返回 True。
        """
        required_nodes = [
            self.upper_teeth_joint,
            self.lower_teeth_joint,
            self.upper_teeth_control,
            self.lower_teeth_control,
            self.upper_teeth_output,
            self.lower_teeth_output,
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

        if self.upper_teech_model:
            if not self.upper_teeth_skin_cluster:
                raise RuntimeError(
                    u"Upper Teeth Model 没有完成刚性 Skin 绑定。"
                )

        if self.lower_teech_model:
            if not self.lower_teeth_skin_cluster:
                raise RuntimeError(
                    u"Lower Teeth Model 没有完成刚性 Skin 绑定。"
                )

        return True


__all__ = [
    "TeethComponent",
]
