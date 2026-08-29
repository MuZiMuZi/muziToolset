# coding=utf-8
u"""
Step 01 - Face Setup
====================

负责：
    1. 指定头部模型；
    2. 指定左右眼模型；
    3. 指定上下牙模型；
    4. 指定舌头模型；
    5. 指定牙龈模型；
    6. 设置嘴唇关节数量；
    7. 更新 Face Rig 工作模型；
    8. 更新 Config Network Node。

设计：
    Config Node 只创建一次。
    Step 01 可以重复执行。
    用户修改 Step 01 后，会把最新配置写回同一个 Config Node。
    后续 Step 统一从 Config Node 获取最新数据。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import hierarchyUtils
from ...core import mesh_utils
from ...core import nameUtils
from . import face_base


class FaceSetup(face_base.FaceBase):
    u"""Face Rig Step 01。"""

    def __init__(
        self,
        face_head_model=None,
        face_lf_eye_model=None,
        face_rt_eye_model=None,
        upper_teech_model=None,
        lower_teech_model=None,
        face_tongue_model=None,
        face_gum_model=None,
        mouth_jnt_number=32
    ):
        super(FaceSetup, self).__init__()

        self.face_head_model = face_head_model
        self.face_lf_eye_model = face_lf_eye_model
        self.face_rt_eye_model = face_rt_eye_model
        self.upper_teech_model = upper_teech_model
        self.lower_teech_model = lower_teech_model
        self.face_tongue_model = face_tongue_model
        self.face_gum_model = face_gum_model

        self.face_model_list = [
            self.face_head_model,
            self.face_lf_eye_model,
            self.face_rt_eye_model,
            self.upper_teech_model,
            self.lower_teech_model,
            self.face_tongue_model,
            self.face_gum_model,
        ]

        self.mouth_jnt_number = mouth_jnt_number

        self.face_head_tweak_model = None
        self.face_head_stretch_model = None
        self.face_head_deform_model = None

    # =========================================================================
    # Check
    # =========================================================================

    def check_model_exists(self):
        u"""检查 Step 01 指定的模型是否存在。"""
        if self.face_head_model is None or self.face_head_model == "":
            raise RuntimeError(
                u"Face Setup 必须指定头部模型。"
            )

        for face_model in self.face_model_list:
            if face_model is None:
                continue

            if face_model == "":
                continue

            if not cmds.objExists(face_model):
                raise RuntimeError(
                    u"给定名称的模型不存在于当前 Maya 场景中: {}".format(
                        face_model
                    )
                )

        return True

    def check_mouth_jnt_number(self):
        u"""检查嘴唇关节数量。"""
        if self.mouth_jnt_number is None:
            raise RuntimeError(
                u"没有设置嘴唇关节数量。"
            )

        if not isinstance(self.mouth_jnt_number, int):
            raise TypeError(
                u"嘴唇关节数量必须是整数。"
            )

        if self.mouth_jnt_number < 4:
            raise ValueError(
                u"嘴唇关节数量不能小于 4。"
            )

        if self.mouth_jnt_number % 4 != 0:
            raise ValueError(
                u"嘴唇关节数量必须是 4 的倍数，当前值为: {}".format(
                    self.mouth_jnt_number
                )
            )

        return True

    # =========================================================================
    # Model
    # =========================================================================

    def parent_input_models(self):
        u"""把 Step 01 指定的模型整理到 Face Model Group。"""
        for face_model in self.face_model_list:
            if face_model is None:
                continue

            if face_model == "":
                continue

            hierarchyUtils.Hierarchy.parent(
                face_model,
                self.face_model_grp
            )

        return True

    def get_work_model_names(self):
        u"""生成 Step 01 三个头部工作模型名称。"""
        face_head_tweak_name = nameUtils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="tweak",
            index=1
        )

        face_head_stretch_name = nameUtils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="stretch",
            index=1
        )

        face_head_deform_name = nameUtils.Name.create_name(
            node_type="model",
            side=self.face_side,
            part="head",
            function="deform",
            index=1
        )

        work_model_name_dict = {
            "tweak": face_head_tweak_name,
            "stretch": face_head_stretch_name,
            "deform": face_head_deform_name,
        }

        return work_model_name_dict

    def delete_old_work_models(self, work_model_name_dict):
        u"""删除 Step 01 之前生成的旧工作模型。"""
        for key in work_model_name_dict:
            model = work_model_name_dict.get(key)

            if not model:
                continue

            if not cmds.objExists(model):
                continue

            cmds.delete(model)

        return True

    def create_work_models(self, work_model_name_dict):
        u"""根据最新 Head Model 创建三个独立工作模型。"""
        face_head_tweak_name = work_model_name_dict.get("tweak")
        face_head_stretch_name = work_model_name_dict.get("stretch")
        face_head_deform_name = work_model_name_dict.get("deform")

        self.face_head_tweak_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_tweak_name,
            parent=self.face_tweak_grp
        )

        self.face_head_stretch_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_stretch_name,
            parent=self.face_stretch_grp
        )

        self.face_head_deform_model = mesh_utils.duplicate_model(
            source_model=self.face_head_model,
            new_name=face_head_deform_name,
            parent=self.face_deform_grp
        )

        return True

    def update_work_models(self):
        u"""根据最新输入更新 Step 01 工作模型。"""
        self.parent_input_models()

        work_model_name_dict = self.get_work_model_names()

        self.delete_old_work_models(
            work_model_name_dict
        )

        self.create_work_models(
            work_model_name_dict
        )

        return True

    # =========================================================================
    # Config
    # =========================================================================

    def save_config(self):
        u"""把 Step 01 最新设置更新到 Config Node。"""
        self.ensure_config_node()
        config_attr = self.get_config_attr()

        model_config_dict = {
            "face_head_model": self.face_head_model,
            "face_lf_eye_model": self.face_lf_eye_model,
            "face_rt_eye_model": self.face_rt_eye_model,
            "upper_teech_model": self.upper_teech_model,
            "lower_teech_model": self.lower_teech_model,
            "face_tongue_model": self.face_tongue_model,
            "face_gum_model": self.face_gum_model,
        }

        config_attr.connect_messages(
            attrs_dict=model_config_dict,
            force=True,
            clear_empty=True
        )

        value_config_dict = {
            "mouth_jnt_number": self.mouth_jnt_number,
        }

        value_type_dict = {
            "mouth_jnt_number": "long",
        }

        config_attr.set_attr_values(
            attrs_dict=value_config_dict,
            attr_types=value_type_dict,
            lock=False,
            hide=False
        )

        return True

    # =========================================================================
    # Build
    # =========================================================================

    def build(self):
        u"""执行可以重复运行的 Face Rig Step 01。"""
        self.check_model_exists()
        self.check_mouth_jnt_number()
        self.ensure_hierarchy()
        self.update_work_models()
        self.save_config()
        return True
