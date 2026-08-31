# coding=utf-8
u"""
这个类用来制作牙床component的绑定

"""
from systems.face import face_base
from ....core import name_utils

class  TeethComponent(face_base.FaceBase):
    def __init__(self):
        #继承face_base.FaceBase类，获得整体face绑定的命名结构
        face_base.FaceBase.__init__(self)


    def collect_inputs (self) :
        u"""收集并检查 Teeth Component 所需输入。"""

        # =========================================================================
        # 步骤 1：检查 Step 01 Setup 数据
        # =========================================================================

        self.validate_setup_config (
            require_mouth_jnt_number = False
        )

        # =========================================================================
        # 步骤 2：准备 Guide 名称
        # =========================================================================

        upper_teeth_guide_name = name_utils.Name.create_name (
            node_type = "loc" ,
            side = "md" ,
            part = "upper_teeth" ,
            function = "guide" ,
            index = 1
        )

        lower_teeth_guide_name = name_utils.Name.create_name (
            node_type = "loc" ,
            side = "md" ,
            part = "lower_teeth" ,
            function = "guide" ,
            index = 1
        )

        # =========================================================================
        # 步骤 3：获取并检查 Guide
        # =========================================================================

        self.upper_teeth_guide = self.get_guide_node (
            upper_teeth_guide_name ,
            required = True
        )

        self.lower_teeth_guide = self.get_guide_node (
            lower_teeth_guide_name ,
            required = True
        )

        # =========================================================================
        # 步骤 4：读取 Controller Settings
        # =========================================================================

        controller_settings = self.load_controller_settings ()

        self.controller_global_scale = controller_settings.get (
            "face_ctrl_global_scale"
        )

        self.controller_color = controller_settings.get (
            "face_ctrl_color_md"
        )

        return True


    def prepare_data(self):
        # 准备本次执行需要的层级、名称、中间数据以及旧结果清理。
        super(TeethComponent, self).process_data()


    def process_data(self):
        # 执行当前 Step 真正的核心场景或数据处理。
        super(TeethComponent, self).self.process_data()


    def finalize_step(self):
        # 检查最终结果、保存配置并完成当前 Step 状态。
        super(TeethComponent, self).finalize_step()