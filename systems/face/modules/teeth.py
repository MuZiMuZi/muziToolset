# coding=utf-8
u"""
Teeth Module
============

Upper / Lower Teeth 刚体绑定模块。

统一 Face Module 生命周期：

    load_setup()
        ↓
    load_guide()
        ↓
    create_jnt()
        ↓
    create_ctrl()
        ↓
    create_connect()
        ↓
    create_deform()
        ↓
    create_finalize()
        ↓
    create_build()

Rig 关系：

    Guide
        ↓
    Controller
        ↓ Matrix
    Bind Joint
        ↓ Rigid Skin
    Teeth Model

边界：
    - Teeth 只处理 Upper / Lower Teeth；
    - Gum 属于 Mouth / Jaw Deformation，不在本 Module 中刚性绑定；
    - Naming 统一继承 FaceBase -> RigBase；
    - Controller 统一使用 systems.ctrl_base；
    - Joint / Matrix / Skin / Scene State 统一复用 Core；
    - 只在 Build / Rebuild 时检查已有 Scene Node，不重复验证内部 Rig Name。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import joint_utils
from ....core import matrix_utils
from ....core import scene_utils
from ....core import skin_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class TeethModule(FaceModuleBase):
    u"""构建 Upper / Lower Teeth 刚体 Rig。"""

    def __init__(self):
        u"""
        初始化 Teeth Module 输入、设置、名称和构建结果。
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

        # Guide
        self.upper_teeth_guide_name = None
        self.lower_teeth_guide_name = None
        self.upper_teeth_guide = None
        self.lower_teeth_guide = None

        # Naming
        self.upper_teeth_joint_name = None
        self.lower_teeth_joint_name = None
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.upper_teeth_ctrl_name = None
        self.lower_teeth_ctrl_name = None
        self.upper_teeth_matrix_name = None
        self.lower_teeth_matrix_name = None
        self.upper_teeth_skin_name = None
        self.lower_teeth_skin_name = None

        # Controller Settings
        self.controller_global_scale = 1.0
        self.controller_color = 17
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.controller_size = 1.0
        self.controller_radius = 1.0

        # Build Result
        self.upper_teeth_joint = None
        self.lower_teeth_joint = None

        self.upper_teeth_ctrl_dict = None
        self.lower_teeth_ctrl_dict = None
        self.upper_teeth_ctrl = None
        self.lower_teeth_ctrl = None
        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.upper_teeth_output = None
        self.lower_teeth_output = None
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
    # 01. Load Setup
    # =========================================================================

    def load_setup(self):
        u"""
        准备 Teeth 参数、确定性名称、公共层级和 Rebuild Scene State。

        Returns:
            bool:
            Setup 阶段完成后返回 True。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：确认 Face Setup 数据可用，并确保公共层级存在
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )
        self.ensure_hierarchy()

        # -------------------------------------------------------------------------
        # Step 02：读取统一 Controller Settings
        # -------------------------------------------------------------------------
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
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(
                u"Teeth Controller Radius 必须大于 0。"
            )

        # -------------------------------------------------------------------------
        # Step 03：准备全部标准名称
        # -------------------------------------------------------------------------
        self._prepare_names()

        # -------------------------------------------------------------------------
        # Step 04：只检查真实 Scene / Rebuild 状态
        # -------------------------------------------------------------------------
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

    # =========================================================================
    # 02. Load Guide
    # =========================================================================

    def load_guide(self):
        u"""
        读取 Upper / Lower Teeth Guide。

        Returns:
            list[str]:
            Upper Guide 与 Lower Guide。
        """
        # -------------------------------------------------------------------------
        # Step 01：生成当前模板中的标准 Guide 名称
        # -------------------------------------------------------------------------
        self.upper_teeth_guide_name = self.create_name(
            type="loc",
            part="upper_teeth",
            function="guide"
        )
        self.lower_teeth_guide_name = self.create_name(
            type="loc",
            part="lower_teeth",
            function="guide"
        )

        # -------------------------------------------------------------------------
        # Step 02：读取真实 Guide Node；缺失时阻止后续构建
        # -------------------------------------------------------------------------
        self.upper_teeth_guide = self.face_guide.get_guide_node(
            self.upper_teeth_guide_name,
            required=True
        )
        self.lower_teeth_guide = self.face_guide.get_guide_node(
            self.lower_teeth_guide_name,
            required=True
        )

        return [
            self.upper_teeth_guide,
            self.lower_teeth_guide,
        ]

    # =========================================================================
    # 03. Create Jnt
    # =========================================================================

    def create_jnt(self):
        u"""
        根据 Teeth Guide 创建 Upper / Lower Bind Joint。

        Returns:
            list[str]:
            Upper / Lower Teeth Joint。
        """
        joint_radius = self.controller_radius * 0.25

        # -------------------------------------------------------------------------
        # Step 01：Upper Teeth Joint
        # -------------------------------------------------------------------------
        self.upper_teeth_joint = joint_utils.Joint.create_at_object(
            obj=self.upper_teeth_guide,
            name=self.upper_teeth_joint_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=joint_radius
        )

        # -------------------------------------------------------------------------
        # Step 02：Lower Teeth Joint
        # -------------------------------------------------------------------------
        self.lower_teeth_joint = joint_utils.Joint.create_at_object(
            obj=self.lower_teeth_guide,
            name=self.lower_teeth_joint_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=joint_radius
        )

        self.module_dict["upper_joint"] = self.upper_teeth_joint
        self.module_dict["lower_joint"] = self.lower_teeth_joint

        return [
            self.upper_teeth_joint,
            self.lower_teeth_joint,
        ]

    # =========================================================================
    # 04. Create Ctrl
    # =========================================================================

    def create_ctrl(self):
        u"""
        使用 CtrlBase 创建 Upper / Lower Teeth Controller。

        Returns:
            list[dict]:
            Upper / Lower Controller Dict。
        """
        # -------------------------------------------------------------------------
        # Step 01：Upper Teeth Controller
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 02：Lower Teeth Controller
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 03：保存明确业务变量和统一 Module 输出
        # -------------------------------------------------------------------------
        self.upper_teeth_ctrl = self.upper_teeth_ctrl_dict["ctrl_node"]
        self.lower_teeth_ctrl = self.lower_teeth_ctrl_dict["ctrl_node"]
        self.upper_teeth_output = self.upper_teeth_ctrl_dict["output_node"]
        self.lower_teeth_output = self.lower_teeth_ctrl_dict["output_node"]
        self.upper_teeth_top_group = self.upper_teeth_ctrl_dict["top_grp"]
        self.lower_teeth_top_group = self.lower_teeth_ctrl_dict["top_grp"]

        self.module_dict["upper_ctrl_dict"] = self.upper_teeth_ctrl_dict
        self.module_dict["lower_ctrl_dict"] = self.lower_teeth_ctrl_dict
        self.module_dict["upper_ctrl"] = self.upper_teeth_ctrl
        self.module_dict["lower_ctrl"] = self.lower_teeth_ctrl
        self.module_dict["upper_output"] = self.upper_teeth_output
        self.module_dict["lower_output"] = self.lower_teeth_output

        return [
            self.upper_teeth_ctrl_dict,
            self.lower_teeth_ctrl_dict,
        ]

    # =========================================================================
    # 05. Create Connect
    # =========================================================================

    def create_connect(self):
        u"""
        创建 Controller Output -> Teeth Joint 的 Matrix 驱动关系。

        Returns:
            list[str]:
            Upper / Lower Matrix 节点。
        """
        # -------------------------------------------------------------------------
        # Step 01：Upper Teeth Matrix
        # -------------------------------------------------------------------------
        self.upper_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.upper_teeth_output,
            driven=self.upper_teeth_joint,
            maintain_offset=False,
            name=self.upper_teeth_matrix_name
        )

        # -------------------------------------------------------------------------
        # Step 02：Lower Teeth Matrix
        # -------------------------------------------------------------------------
        self.lower_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.lower_teeth_output,
            driven=self.lower_teeth_joint,
            maintain_offset=False,
            name=self.lower_teeth_matrix_name
        )

        self.module_dict["upper_matrix"] = self.upper_teeth_matrix_node
        self.module_dict["lower_matrix"] = self.lower_teeth_matrix_node

        return [
            self.upper_teeth_matrix_node,
            self.lower_teeth_matrix_node,
        ]

    # =========================================================================
    # 06. Create Deform
    # =========================================================================

    def create_deform(self):
        u"""
        使用单 Joint SkinCluster 把 Upper / Lower Teeth 刚性绑定到对应 Joint。

        Returns:
            list[str | None]:
            Upper / Lower Teeth SkinCluster；没有对应模型时为 None。
        """
        # -------------------------------------------------------------------------
        # Step 01：Upper Teeth Rigid Skin
        # -------------------------------------------------------------------------
        self.upper_teeth_skin_cluster = self._create_rigid_skin_cluster(
            model=self.upper_teech_model,
            joint=self.upper_teeth_joint,
            skin_name=self.upper_teeth_skin_name
        )

        # -------------------------------------------------------------------------
        # Step 02：Lower Teeth Rigid Skin
        # -------------------------------------------------------------------------
        self.lower_teeth_skin_cluster = self._create_rigid_skin_cluster(
            model=self.lower_teech_model,
            joint=self.lower_teeth_joint,
            skin_name=self.lower_teeth_skin_name
        )

        self.module_dict["upper_skin"] = self.upper_teeth_skin_cluster
        self.module_dict["lower_skin"] = self.lower_teeth_skin_cluster

        return [
            self.upper_teeth_skin_cluster,
            self.lower_teeth_skin_cluster,
        ]

    # =========================================================================
    # 07. Create Finalize
    # =========================================================================

    def create_finalize(self):
        u"""
        验证 Teeth Module 最终 Scene State，并完成模块输出。

        Returns:
            bool:
            构建结果完整时返回 True。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        required_nodes = [
            self.upper_teeth_joint,
            self.lower_teeth_joint,
            self.upper_teeth_ctrl,
            self.lower_teeth_ctrl,
            self.upper_teeth_matrix_node,
            self.lower_teeth_matrix_node,
        ]

        # -------------------------------------------------------------------------
        # Step 01：验证必须存在的 Joint / Controller / Matrix
        # -------------------------------------------------------------------------
        for node in required_nodes:
            if not node:
                raise RuntimeError(
                    u"Teeth Module 构建结果不完整。"
                )

            scene_utils.validate_node(
                node,
                label=u"Teeth Module Build Node"
            )

        # -------------------------------------------------------------------------
        # Step 02：可选模型只有在传入时才要求 SkinCluster 构建完成
        # -------------------------------------------------------------------------
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

        self.module_dict["upper_top_group"] = self.upper_teeth_top_group
        self.module_dict["lower_top_group"] = self.lower_teeth_top_group
        self.module_dict["built"] = True
        return True

    # =========================================================================
    # Naming / Scene State
    # =========================================================================

    def _prepare_names(self):
        u"""根据 Teeth Module Identity 准备全部标准名称。"""
        # -------------------------------------------------------------------------
        # Step 01：Joint Names
        # -------------------------------------------------------------------------
        self.upper_teeth_joint_name = self.create_name(
            type="jnt",
            part="upper_teeth",
            function="bind"
        )
        self.lower_teeth_joint_name = self.create_name(
            type="jnt",
            part="lower_teeth",
            function="bind"
        )

        # -------------------------------------------------------------------------
        # Step 02：Controller Names
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
        # Step 03：Matrix / Skin Names
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
        u"""构建前检查上一次 Teeth Build 的确定性节点是否已经存在。"""
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        expected_nodes = [
            self.upper_teeth_joint_name,
            self.lower_teeth_joint_name,
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
        teeth_ctrl_name_list = [
            self.upper_teeth_ctrl_name,
            self.lower_teeth_ctrl_name,
        ]

        for teeth_ctrl_name in teeth_ctrl_name_list:
            teeth_ctrl_hierarchy_names = ctrl_base.get_ctrl_hierarchy_names(
                teeth_ctrl_name
            )

            for hierarchy_key in teeth_ctrl_hierarchy_names:
                hierarchy_name = teeth_ctrl_hierarchy_names[hierarchy_key]

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

    @staticmethod
    def _create_rigid_skin_cluster(
            model,
            joint,
            skin_name
    ):
        u"""
        使用一个 Joint 创建 Teeth 刚性 SkinCluster。

        Args:
            model (str | None):
                需要绑定的 Teeth Model。
            joint (str):
                唯一影响 Teeth Model 的 Bind Joint。
            skin_name (str):
                标准 SkinCluster 名称。

        Returns:
            str | None:
                SkinCluster；没有模型输入时返回 None。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not model:
            return None

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        existing_skin_cluster = skin_utils.find_skin_cluster(
            model
        )

        if existing_skin_cluster:
            raise RuntimeError(
                u"模型已经存在 SkinCluster：{}".format(
                    existing_skin_cluster
                )
            )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not skin_result:
            raise RuntimeError(
                u"创建 Teeth SkinCluster 失败：{}".format(
                    model
                )
            )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
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
    构建 Teeth Module，并返回统一模块结果字典。

    Returns:
        dict:
        TeethModule.create_build() 的完整公开结果。
    """
    teeth_module = TeethModule()
    teeth_module_dict = teeth_module.create_build()
    return teeth_module_dict


__all__ = [
    "TeethModule",
    "build_teeth",
]
