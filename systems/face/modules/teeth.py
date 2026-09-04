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
    Bind jnt
        ↓ Rigid Skin
    Teeth Model

边界：
    - Teeth 只处理 Upper / Lower Teeth；
    - Gum 属于 Mouth / Jaw Deformation，不在本 Module 中刚性绑定；
    - Naming 统一继承 FaceBase -> RigBase；
    - Controller 统一使用 systems.ctrl_base；
    - jnt / Matrix / Skin / Scene State 统一复用 Core；
    - 只在 Build / Rebuild 时检查已有 Scene Node，不重复验证内部 Rig Name。
"""

from __future__ import print_function

import maya.cmds as cmds

from core import hierarchy_utils
from ....core import jnt_utils
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
        self.upper_teeth_jnt_name = None
        self.lower_teeth_jnt_name = None
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
        self.upper_teeth_jnt = None
        self.lower_teeth_jnt = None

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


        return True

    def _prepare_names(self):

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
        
        #创建
        self.teeth_ctrl_grp_name = self.create_name(
            type = "grp" ,
            part = "teeth" ,
            function = "ctrl",
            index = 1
        )
        self.teeth_jnt_grp_name =  self.create_name(
            type = "grp" ,
            part = "teeth" ,
            function = "jnt",
            index = 1
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
        根据 Teeth Guide 创建 Upper / Lower Bind jnt。

        Returns:
            list[str]:
            Upper / Lower Teeth jnt。
        """
        #准备关节的名称
        self.upper_teeth_jnt_name = self.create_name (
            type = "jnt" ,
            part = "upper_teeth" ,
            function = "bind"
        )
        self.lower_teeth_jnt_name = self.create_name (
            type = "jnt" ,
            part = "lower_teeth" ,
            function = "bind"
        )
        
        
        
        jnt_radius = self.controller_radius * 0.25

        # -------------------------------------------------------------------------
        # Step 01：Upper Teeth jnt
        # -------------------------------------------------------------------------
        self.upper_teeth_jnt = jnt_utils.jnt.create_at_object(
            obj=self.upper_teeth_guide,
            name=self.upper_teeth_jnt_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=jnt_radius
        )

        # -------------------------------------------------------------------------
        # Step 02：Lower Teeth jnt
        # -------------------------------------------------------------------------
        self.lower_teeth_jnt = jnt_utils.jnt.create_at_object(
            obj=self.lower_teeth_guide,
            name=self.lower_teeth_jnt_name,
            parent=self.face_jnt_grp,
            match_rotation=True,
            radius=jnt_radius
        )

        self.module_dict["upper_jnt"] = self.upper_teeth_jnt
        self.module_dict["lower_jnt"] = self.lower_teeth_jnt
        
        self.teeth_jnt_list = [self.upper_teeth_jnt, self.lower_teeth_jnt ]

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
        #准备控制器的名称
        self.upper_teeth_ctrl_name = self.create_name (
            type = "ctrl" ,
            part = "upper_teeth" ,
            function = "bind"
        )
        self.lower_teeth_ctrl_name = self.create_name (
            type = "ctrl" ,
            part = "lower_teeth" ,
            function = "bind"
        )
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

        self.teeth_top_group_list = [self.upper_teeth_top_group , self.lower_teeth_top_group]


    # =========================================================================
    # 05. Create Connect
    # =========================================================================

    def create_connect(self):
        u"""
        创建 Controller Output -> Teeth jnt 的 Matrix 驱动关系。

        Returns:
            list[str]:
            Upper / Lower Matrix 节点。
        """
        # -------------------------------------------------------------------------
        # Step 01：Upper Teeth Matrix
        # -------------------------------------------------------------------------
        self.upper_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.upper_teeth_output,
            driven=self.upper_teeth_jnt,
            maintain_offset=False,
            name=self.upper_teeth_matrix_name
        )

        # -------------------------------------------------------------------------
        # Step 02：Lower Teeth Matrix
        # -------------------------------------------------------------------------
        self.lower_teeth_matrix_node = matrix_utils.create_parent_matrix_constraint(
            driver=self.lower_teeth_output,
            driven=self.lower_teeth_jnt,
            maintain_offset=False,
            name=self.lower_teeth_matrix_name
        )

        self.module_dict["upper_matrix"] = self.upper_teeth_matrix_node
        self.module_dict["lower_matrix"] = self.lower_teeth_matrix_node


    # =========================================================================
    # 06. Create Deform
    # =========================================================================

    def create_deform(self):
        pass

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
            self.upper_teeth_jnt,
            self.lower_teeth_jnt,
            self.upper_teeth_ctrl,
            self.lower_teeth_ctrl,
            self.upper_teeth_matrix_node,
            self.lower_teeth_matrix_node,
        ]

        # -------------------------------------------------------------------------
        # Step 01：验证必须存在的 jnt / Controller / Matrix
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

        #整理层级结构，创建模块的对应的控制器组和关节组
        self.teeth_ctrl_grp = cmds.createNode('transform',name=self.teeth_ctrl_grp_name,parent=self.face_ctrl_grp)
        self.teeth_jnt_grp = cmds.createNode('transform',name=self.teeth_jnt_grp_name,parent=self.face_jnt_grp)
        
        #将对应的控制器和关节都放到对应的组下
        for jnt in self.teeth_jnt_list:
            hierarchy_utils.parent (child_node = jnt , parent_node = self.teeth_jnt_grp)
        for top_grp in self. teeth_top_group_list:
            hierarchy_utils.parent (child_node = top_grp , parent_node = self. teeth_top_group_list)
        self.module_dict["upper_top_group"] = self.upper_teeth_top_group
        self.module_dict["lower_top_group"] = self.lower_teeth_top_group
        self.module_dict["built"] = True

    # =========================================================================
    # Naming / Scene State
    # =========================================================================






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
