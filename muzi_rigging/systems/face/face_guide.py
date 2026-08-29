# coding=utf-8
u"""
Step 02 - Face Guide
====================

负责读取 Step 01 保存的模型配置，并为后续 Face Guide 构建准备数据。
具体 Guide 创建逻辑会继续在本模块中扩展。
"""

from __future__ import print_function

from . import face_base


class FaceGuide(face_base.FaceBase):
    u"""Face Rig Step 02。"""

    def __init__(self):
        super(FaceGuide, self).__init__()

        self.step_value = 2

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

        self.mouth_jnt_number = self.get_config_value(
            "mouth_jnt_number"
        )

    def validate_setup(self):
        u"""检查 Step 01 是否已经提供基本数据。"""
        if not self.face_head_model:
            raise RuntimeError(
                u"没有读取到 Face Head Model，请先完成 Face Setup。"
            )

        if self.mouth_jnt_number is None:
            raise RuntimeError(
                u"没有读取到嘴唇关节数量，请先完成 Face Setup。"
            )

        return True
