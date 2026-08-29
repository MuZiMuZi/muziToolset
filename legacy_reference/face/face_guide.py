# coding=utf-8
#Step 02 - Face Guide
#步骤2，创建face的定位器位置
from imp import reload

from . import face_base

reload(face_base)


class FaceGuide(face_base.FaceBase):

    def __init__(self):

        # ------------------------------------------------------------
        # 初始化公共 Face 配置
        # ------------------------------------------------------------

        super().__init__()

        # ------------------------------------------------------------
        # 当前步骤
        # ------------------------------------------------------------

        self.step_value = 2

        # ------------------------------------------------------------
        # 读取 Step01 模型配置
        # ------------------------------------------------------------

        self.face_head_model = self.get_config_message(
            "face_head_model"
        )

        self.face_lf_eye_model = self.get_config_message(
            "face_lf_eye_model"
        )

        self.face_rt_eye_model = self.get_config_message(
            "face_rt_eye_model"
        )

        self.upper_teech_model = self.get_config_message(
            "upper_teech_model"
        )

        self.lower_teech_model = self.get_config_message(
            "lower_teech_model"
        )

        self.face_tongue_model = self.get_config_message(
            "face_tongue_model"
        )

        self.face_gum_model = self.get_config_message(
            "face_gum_model"
        )

        # ------------------------------------------------------------
        # 读取 Step01 数值配置
        # ------------------------------------------------------------

        self.mouth_jnt_number = self.get_config_value(
            "mouth_jnt_number"
        )



def maya_test_face_guide():
    guide = step2_face_guide.FaceGuide ()
    print (guide.face_head_model)
    print (guide.face_lf_eye_model)
    print (guide.mouth_jnt_number)
    print (guide.face_guide_grp)