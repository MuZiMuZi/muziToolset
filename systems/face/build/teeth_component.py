# coding=utf-8
u"""
这个类用来制作牙床component的绑定

"""
from systems.face import face_base

class  TeethComponent(face_base.FaceBase):
    def __init__(self):
        #继承face_base.FaceBase类，获得整体face绑定的命名结构
        face_base.FaceBase.__init__(self)


    def collect_inputs (self) :
        # 步骤 1：确认前置 Setup 数据有效。
        self.validate_setup_config(require_mouth_jnt_number=False)

        # 步骤 2：获取牙床 Guide。
        self.teeth_guides = self.get_part_guides(part="teeth" )

        # 步骤 3：检查必须的 Guide 是否存在。
        ...

        # 步骤 4：读取 Controller Settings。
        ...


    def prepare_data(self):
        # 准备本次执行需要的层级、名称、中间数据以及旧结果清理。
        super(TeethComponent, self).process_data()


    def process_data(self):
        # 执行当前 Step 真正的核心场景或数据处理。
        super(TeethComponent, self).self.process_data()


    def finalize_step(self):
        # 检查最终结果、保存配置并完成当前 Step 状态。
        super(TeethComponent, self).finalize_step()