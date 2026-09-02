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

边界：
    - Teeth 只处理 Upper / Lower Teeth；
    - Gum 属于 Mouth / Jaw Deformation，不在本 Module 中刚性绑定；
    - Rig Name 直接继承 FaceBase -> RigBase；
    - Controller 创建统一使用 systems.ctrl_base；
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
        u"""初始化 Teeth Module 输入、设置和构建结果。"""
        super(TeethModule, self).__init__()

        self.face_guide = FaceGuide()

        self.upper_teeth_guide_name = None
        self.lower_teeth_guide_name = None
        self.upper_teeth_guide = None
        self.lower_teeth_guide = None

        self.upper_teeth_jnt_name = None
        self.lower_teeth_jnt_name = None
        self.upper_teeth_ctrl_name = None
        self.lower_teeth_ctrl_name = None
        self.upper_teeth_matrix_name = None
        self.lower_teeth_matrix_name = None
        self.upper_teeth_skin_name = None
        self.lower_teeth_skin_name = None

        self.controller_global_scale = 1.0
        self.controller_color = 17
        self.controller_size = 1.0
        self.controller_radius = 1.0

        self.upper_teeth_joint = None
        self.lower_teeth_joint = None

        self.upper_teeth_ctrl_dict = None
        self.lower_teeth_ctrl_dict = None
        self.upper_teeth_control = None
        self.lower_teeth_control = None
        self.upper_teeth_top_group = None
        self.lower_teeth_top_group = None

        self.upper_teeth_matrix_node = None
        self.lower_teeth_matrix_node = None
        self.upper_teeth_skin_cluster = None
        self.lower_teeth_skin_cluster = None

    # =========================================================================
    # Module Lifecycle
    # =========================================================================

    def collect_inputs(self):
        u"""读取 Setup、Guide 和 Controller Settings。"""
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )

        self.upper_teeth_guide_name = self.create_name(
            type="loc",
            side="md",
            part="upper_teeth",
            function="guide",
            index=1
        )
        self.lower_teeth_guide_name = self.create_name(
            type="loc",
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
        u"""准备确定性名称、层级并执行构建前安全检查。"""
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
        u"""检查 Teeth Module 的最终构建结果。"""
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

            if not cmds.objExists(node):
                raise RuntimeError(
                    u"Teeth Module 构建节点不存在：{}".format(
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
        return True

    # =========================================================================
    # Naming / Validation
    # =========================================================================

    def _prepare_names(self):
        u"""准备 Teeth Module 的全部标准名称。"""
        self.upper_teeth_jnt_name = self.create_name(
            type="jnt",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )
        self.lower_teeth_jnt_name = self.create_name(
            type="jnt",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        self.upper_teeth_ctrl_name = self.create_name(
            type="ctrl",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )
        self.lower_teeth_ctrl_name = self.create_name(
            type="ctrl",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        self.upper_teeth_matrix_name = self.create_name(
            type="mult",
            side="md",
            part="upper_teeth",
            function="parent",
            index=1
        )
        self.lower_teeth_matrix_name = self.create_name(
            type="mult",
            side="md",
            part="lower_teeth",
            function="parent",
            index=1
        )

        self.upper_teeth_skin_name = self.create_name(
            type="skin",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )
        self.lower_teeth_skin_name = self.create_name(
            type="skin",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )
        return True

    def _get_ctrl_hierarchy_names(self, ctrl_name):
        u"""返回 ctrl_base.create_ctrl() 会创建的确定性层级名称。"""
        prefix_list = [
            "ctrl",
            "zero",
            "driven",
            "space",
            "connect",
            "offset",
            "output",
        ]
        node_name_list = []

        for prefix in prefix_list:
            if prefix == "ctrl":
                node_name = ctrl_name
            else:
                node_name = ctrl_name.replace(
                    "ctrl_",
                    prefix + "_",
                    1
                )

            node_name_list.append(
                node_name
            )

        return node_name_list

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
        u"""构建前检查全部确定性节点名称是否可用。"""
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

        upper_ctrl_nodes = self._get_ctrl_hierarchy_names(
            self.upper_teeth_ctrl_name
        )
        lower_ctrl_nodes = self._get_ctrl_hierarchy_names(
            self.lower_teeth_ctrl_name
        )

        for node_name in upper_ctrl_nodes:
            expected_nodes.append(
                node_name
            )

        for node_name in lower_ctrl_nodes:
            expected_nodes.append(
                node_name
            )

        existing_nodes = []

        for node_name in expected_nodes:
            if cmds.objExists(node_name):
                existing_nodes.append(
                    node_name
                )

        if existing_nodes:
            raise RuntimeError(
                u"Teeth Module 已存在或存在同名残留节点，请先清理后再构建：{}".format(
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
            u"{} 已经存在 SkinCluster：{}。Teeth Module 不会覆盖已有权重。".format(
                label,
                skin_cluster
            )
        )

    # =========================================================================
    # RigModuleBase Build
    # =========================================================================

    def create_joint(self):
        u"""根据 Teeth Guide 创建 Upper / Lower Bind Joint。"""
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
        u"""使用 ctrl_base 创建 Upper / Lower Teeth Controller。"""
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
        u"""创建 Controller -> Joint -> Teeth Model 的驱动链。"""
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

        if not cmds.objExists(skin_cluster):
            raise RuntimeError(
                u"{} SkinCluster 不存在：{}".format(
                    label,
                    skin_cluster
                )
            )

        return True


def build_teeth():
    u"""执行 TeethModule 并返回后续 Module 需要的公开结果。"""
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
