# coding=utf-8
u"""
Teeth Component
===============

用于构建上下牙床的简单 Face Component。

当前先完成 Component 生命周期和输入数据收集，后续再在 process_data() 中加入：
    1. Upper / Lower Teeth Joint；
    2. 单控制器；
    3. Controller -> Joint 驱动；
    4. Teeth Model 绑定关系。
"""

from __future__ import print_function

from ....core import name_utils
from .. import config
from .. import face_base
from ..guide import FaceGuide


class TeethComponent(face_base.FaceBase):
    u"""Step 03 中的 Teeth Component。"""

    def __init__(self):
        u"""初始化 Teeth Component。"""
        super(TeethComponent, self).__init__()

        self.face_guide = FaceGuide()

        self.upper_teeth_guide = None
        self.lower_teeth_guide = None

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
        #准备上下牙床的绑定关节名称
        self.upper_teeth_jnt_name = name_utils.Name.create_name (
            node_type = "jnt" ,
            side = "md" ,
            part = "upper_teeth" ,
            function = "bind" ,
            index = 1
        )

        self.lower_teeth_jnt_name = name_utils.Name.create_name (
            node_type = "jnt" ,
            side = "md" ,
            part = "lower_teeth" ,
            function = "bind" ,
            index = 1
        )

        #准备上下牙床的控制器名称
        self.upper_teeth_ctrl_name = name_utils.Name.create_name (
            node_type = "ctrl" ,
            side = "md" ,
            part = "upper_teeth" ,
            function = "bind" ,
            index = 1
        )

        self.lower_teeth_ctrl_name = name_utils.Name.create_name (
            node_type = "ctrl" ,
            side = "md" ,
            part = "lower_teeth" ,
            function = "bind" ,
            index = 1
        )

    def process_data(self):
        u"""创建 Teeth Component 的 Joint、Controller 和驱动关系。"""
        #开始根据定位器的位置创建上下牙床的关节
        self.create_joint()

        #开始创建对应的控制器组
        self.create_controller()

        #控制器组与关节建立绑定联系
        self.create_connection()

    def create_joint(self):
        #根据定位器的位置创建上下牙床的关节
        pass

    def create_controller(self):
        # 开始创建对应的控制器组
        pass

    def create_connection(self):
        # 控制器组与关节建立绑定联系
        pass




    def finalize_step(self):
        u"""检查 Teeth Component 最终结果并整理显示 / Metadata。"""
        return True


__all__ = [
    "TeethComponent",
]
