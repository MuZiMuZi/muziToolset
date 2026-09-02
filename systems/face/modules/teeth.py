# coding=utf-8
u"""
Teeth Module
============

Face Rig Step 03 的 Upper / Lower Teeth 刚体绑定 Module。

Rig 关系：

    Guide
        ↓
    Ctrl
        ↓ Matrix
    Bind Joint
        ↓ Rigid Skin
    Teeth Model

Module Identity：

    side  = md
    part  = teeth
    index = 001

边界：
    - Teeth 只处理 Upper / Lower Teeth；
    - Gum 属于 Mouth / Jaw Deformation，不在本 Module 中刚性绑定；
    - Rig Naming 继承 FaceBase -> RigBase；
    - Controller 创建与层级名称统一使用 systems.ctrl_base；
    - Scene Node Availability 统一使用 core.scene_utils；
    - Module 生命周期统一使用 systems.module_base.RigModuleBase。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import joint_utils
from ....core import matrix_utils
from ....core import scene_utils
from ....core import skin_utils
from ... import ctrl_base
from .. import config
from ..face_base import FaceBase
from ..guide import FaceGuide


class TeethModule(FaceBase):
    u"""构建 Upper / Lower Teeth 刚体 Rig。"""

    def __init__(self):
        u"""
        初始化 Teeth Module Identity、输入、设置和构建结果。
        """
        # -------------------------------------------------------------------------
        # Step 01：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        super(TeethModule, self).__init__(
            side="md",
            part="teeth",
            index=1
        )

        self.face_guide = FaceGuide()

        self.upper_teeth_guide_name = None
        self.lower_teeth_guide_name = None
        self.upper_teeth_guide = None
        self.lower_teeth_guide = None

        self.upper_teeth_jnt_name = None
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.lower_teeth_jnt_name = None
        self.upper_teeth_ctrl_name = None
        self.lower_teeth_ctrl_name = None
        self.upper_teeth_matrix_name = None
        self.lower_teeth_matrix_name = None
        self.upper_teeth_skin_name = None
        self.lower_teeth_skin_name = None

        self.controller_global_scale = 1.0
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.controller_color = 17
        self.controller_size = 1.0
        self.controller_radius = 1.0

        self.upper_teeth_joint = None
        self.lower_teeth_joint = None

        self.upper_teeth_ctrl_dict = None
        self.lower_teeth_ctrl_dict = None
        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.upper_teeth_control = None
        self.lower_teeth_control = None
        self.upper_teeth_top_group = None
        self.lower_teeth_top_group = None

        self.upper_teeth_matrix_node = None
        self.lower_teeth_matrix_node = None
        self.upper_teeth_skin_cluster = None
        # -------------------------------------------------------------------------
        # Step 05：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.lower_teeth_skin_cluster = None

    # =========================================================================
    # Module Lifecycle
    # =========================================================================

    def collect_inputs(self):
        u"""

                读取 Setup、Guide 和 Controller Settings。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )

        self.upper_teeth_guide_name = self.create_name(
            type="loc",
            part="upper_teeth",
            function="guide"
        )
        # -------------------------------------------------------------------------
        # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.lower_teeth_guide_name = self.create_name(
            type="loc",
            part="lower_teeth",
            function="guide"
        )

        self.upper_teeth_guide = self.face_guide.get_guide_node(
            self.upper_teeth_guide_name,
            required=True
        )
        self.lower_teeth_guide = self.face_guide.get_guide_node(
            self.lower_teeth_guide_name,
            required=True
        )

        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        controller_settings = self.face_guide.load_controller_settings()

        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )
        # -------------------------------------------------------------------------
        # Step 04：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.controller_color = controller_settings.get(
            config.face_controller_color_attr_names["md"],
            17
        )
        self.controller_size = controller_settings.get(
            config.face_controller_size_attr_names["teeth"],
            1.0
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def prepare_data(self):
        u"""

                准备确定性名称、层级并执行构建前安全检查。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    ValueError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

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
        return True

    def finalize_step(self):
        u"""

                检查 Teeth Module 的最终构建结果。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

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
                    u"Teeth Module 构建结果不完整。"
                )

            scene_utils.validate_node(
                node,
                label=u"Teeth Module Build Node"
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
        return True

    # =========================================================================
    # Naming / Scene State
    # =========================================================================

    def _prepare_names(self):
        u"""根据 TeethModule Identity 准备全部标准名称。"""
        # -------------------------------------------------------------------------
        # Step 01：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.upper_teeth_jnt_name = self.create_name(
            type="jnt",
            part="upper_teeth",
            function="bind"
        )
        self.lower_teeth_jnt_name = self.create_name(
            type="jnt",
            part="lower_teeth",
            function="bind"
        )

        # -------------------------------------------------------------------------
        # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.upper_teeth_ctrl_name = self.create_name(
            type="ctrl",
            part="upper_teeth",
            function="bind"
        )
        self.lower_teeth_ctrl_name = self.create_name(
            type="ctrl",
            part="lower_teeth",
            function="bind"
        )

        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.upper_teeth_matrix_name = self.create_name(
            type="mult",
            part="upper_teeth",
            function="parent"
        )
        self.lower_teeth_matrix_name = self.create_name(
            type="mult",
            part="lower_teeth",
            function="parent"
        )

        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.upper_teeth_skin_name = self.create_name(
            type="skin",
            part="upper_teeth",
            function="bind"
        )
        self.lower_teeth_skin_name = self.create_name(
            type="skin",
            part="lower_teeth",
            function="bind"
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def _validate_model_inputs_unique(self):
        u"""检查 Upper / Lower Teeth 是否误用了同一个模型。"""
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
        u"""构建前检查上一次 Build 的确定性节点是否已经存在。"""
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        expected_nodes = [
            self.upper_teeth_jnt_name,
            self.lower_teeth_jnt_name,
            self.upper_teeth_matrix_name,
            self.lower_teeth_matrix_name,
        ]

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if self.upper_teech_model:
            expected_nodes.append(
                self.upper_teeth_skin_name
            )

        if self.lower_teech_model:
            expected_nodes.append(
                self.lower_teeth_skin_name
            )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        ctrl_names = [
            self.upper_teeth_ctrl_name,
            self.lower_teeth_ctrl_name,
        ]

        for ctrl_name in ctrl_names:
            hierarchy_names = ctrl_base.get_ctrl_hierarchy_names(
                ctrl_name
            )

            for hierarchy_key in hierarchy_names:
                hierarchy_name = hierarchy_names[hierarchy_key]

                if hierarchy_name is None:
                    continue

                expected_nodes.append(
                    hierarchy_name
                )

        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        scene_utils.ensure_nodes_available(
            expected_nodes,
            label=u"Teeth Module Build Node"
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
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
            u"{} 已经存在 SkinCluster：{}。Teeth Module 不会覆盖已有权重。".format(
                label,
                skin_cluster
            )
        )

    # =========================================================================
    # RigModuleBase Build
    # =========================================================================

    def create_joint(self):
        u"""

                根据 Teeth Guide 创建 Upper / Lower Bind Joint。

                Returns:
                    list:
                        按当前 API 约定顺序返回的结果列表。

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

    def create_controller(self):
        u"""

                使用 ctrl_base 创建 Upper / Lower Teeth Controller。

                Returns:
                    list:
                        按当前 API 约定顺序返回的结果列表。

        """
        self.upper_teeth_ctrl_dict = ctrl_base.create_ctrl(
            name=self.upper_teeth_ctrl_name,
            shape="circle",
            radius=self.controller_radius,
            color=self.controller_color,
            axis="Z+",
            target_node=self.upper_teeth_guide,
            parent_node=self.face_ctrl_grp,
            create_sub_ctrl=False,
            add_to_set=True,
            ctrl_set=config.face_ctrl_set
        )
        self.lower_teeth_ctrl_dict = ctrl_base.create_ctrl(
            name=self.lower_teeth_ctrl_name,
            shape="circle",
            radius=self.controller_radius,
            color=self.controller_color,
            axis="Z+",
            target_node=self.lower_teeth_guide,
            parent_node=self.face_ctrl_grp,
            create_sub_ctrl=False,
            add_to_set=True,
            ctrl_set=config.face_ctrl_set
        )

        self.upper_teeth_control = self.upper_teeth_ctrl_dict["ctrl_node"]
        self.lower_teeth_control = self.lower_teeth_ctrl_dict["ctrl_node"]
        self.upper_teeth_top_group = self.upper_teeth_ctrl_dict["top_grp"]
        self.lower_teeth_top_group = self.lower_teeth_ctrl_dict["top_grp"]

        return [
            self.upper_teeth_ctrl_dict,
            self.lower_teeth_ctrl_dict,
        ]

    def create_connection(self):
        u"""

                创建 Controller -> Joint -> Teeth Model 的驱动链。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
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
        return True

    @staticmethod
    def _create_rigid_skin_cluster(
            model,
            joint,
            skin_name
    ):
        u"""使用一个 Joint 创建 Teeth 刚性 SkinCluster。"""
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

        scene_utils.validate_node(
            skin_cluster,
            label=u"{} SkinCluster".format(label)
        )
        return True


def build_teeth():
    u"""

        执行 TeethModule 并返回后续 Module 需要的公开结果。

        Returns:
            dict:
                包含本次构建、查询或处理结果的结构化字典。

    """
    module = TeethModule()
    module.run_step()

    return {
        "module": module,
        "upper_joint": module.upper_teeth_joint,
        "lower_joint": module.lower_teeth_joint,
        "upper_control": module.upper_teeth_control,
        "lower_control": module.lower_teeth_control,
        "upper_top_group": module.upper_teeth_top_group,
        "lower_top_group": module.lower_teeth_top_group,
        "upper_matrix": module.upper_teeth_matrix_node,
        "lower_matrix": module.lower_teeth_matrix_node,
        "upper_skin": module.upper_teeth_skin_cluster,
        "lower_skin": module.lower_teeth_skin_cluster,
    }


__all__ = [
    "TeethModule",
    "build_teeth",
]
