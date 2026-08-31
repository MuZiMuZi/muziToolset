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

本类只负责上下牙床自己的输入、数据准备和三个具体构建阶段。
"""

from __future__ import print_function

from ....core import name_utils
from .. import config
from .. import face_base
from ..guide import FaceGuide


class TeethComponent(face_base.FaceBase):
    u"""Step 03 中的 Teeth Rig Component。"""

    def __init__(self):
        u"""初始化 Teeth Component。"""
        super(TeethComponent, self).__init__()

        self.face_guide = FaceGuide()

        self.upper_teeth_guide_name = None
        self.lower_teeth_guide_name = None
        self.upper_teeth_guide = None
        self.lower_teeth_guide = None

        self.upper_teeth_jnt_name = None
        self.lower_teeth_jnt_name = None
        self.upper_teeth_ctrl_name = None
        self.lower_teeth_ctrl_name = None

        self.controller_global_scale = 1.0
        self.controller_color = 17
        self.controller_size = 1.0

    def collect_inputs(self):
        u"""收集并检查 Teeth Component 所需输入。"""

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
        u"""准备 Teeth Joint / Controller 名称、层级和旧结果清理数据。"""

        # 准备上牙床绑定 Joint 名称。
        self.upper_teeth_jnt_name = name_utils.Name.create_name(
            node_type="jnt",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )

        # 准备下牙床绑定 Joint 名称。
        self.lower_teeth_jnt_name = name_utils.Name.create_name(
            node_type="jnt",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        # 准备上牙床 Controller 名称。
        self.upper_teeth_ctrl_name = name_utils.Name.create_name(
            node_type="ctrl",
            side="md",
            part="upper_teeth",
            function="bind",
            index=1
        )

        # 准备下牙床 Controller 名称。
        self.lower_teeth_ctrl_name = name_utils.Name.create_name(
            node_type="ctrl",
            side="md",
            part="lower_teeth",
            function="bind",
            index=1
        )

        return True

    def create_joint(self):
        u"""根据 Teeth Guide 创建上下牙床绑定 Joint。"""
        pass

    def create_controller(self):
        u"""创建上下牙床对应的标准 Controller Hierarchy。"""
        pass

    def create_connection(self):
        u"""建立 Teeth Controller、Joint 和模型之间的驱动关系。"""
        pass

    def finalize_step(self):
        u"""检查 Teeth Component 最终结果并整理显示 / Metadata。"""
        return True


__all__ = [
    "TeethComponent",
]
