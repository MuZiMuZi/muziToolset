# coding=utf-8
u"""
Step 01 - Face Setup
====================

Face Rig 的 Source Model 注册和 Head Work Model 构建入口。

设计原则：
    - Source Model 只作为输入，不修改其原有 Parent；
    - Face 自己生成的 Work Model 才进入 Face Hierarchy；
    - Work Model 通过 FaceConfig Message Connection 持久化；
    - Setup 重建时先创建新结果，再替换旧结果。
"""

from __future__ import print_function

import pymel.core as pm

from ....core import name
from .. import config
from .. import face_base


class FaceSetup(face_base.FaceBase):
    u"""Face Rig Step 01。"""

    def __init__(
            self,
            head_model=None,
            left_eye_model=None,
            right_eye_model=None,
            upper_teeth_model=None,
            lower_teeth_model=None,
            tongue_model=None,
            gum_model=None,
            mouth_joint_count=32
    ):
        super(FaceSetup, self).__init__()

        self.step_value = 1

        self.head_model = head_model
        self.left_eye_model = left_eye_model
        self.right_eye_model = right_eye_model
        self.upper_teeth_model = upper_teeth_model
        self.lower_teeth_model = lower_teeth_model
        self.tongue_model = tongue_model
        self.gum_model = gum_model
        self.mouth_joint_count = mouth_joint_count

        self.source_models = {}
        self.work_model_names = {}
        self.result_models = {}

    def collect_inputs(self):
        self.head_model = self._resolve_model(
            self.head_model,
            u"Head Model",
            required=True
        )
        self.left_eye_model = self._resolve_model(
            self.left_eye_model,
            u"Left Eye Model"
        )
        self.right_eye_model = self._resolve_model(
            self.right_eye_model,
            u"Right Eye Model"
        )
        self.upper_teeth_model = self._resolve_model(
            self.upper_teeth_model,
            u"Upper Teeth Model"
        )
        self.lower_teeth_model = self._resolve_model(
            self.lower_teeth_model,
            u"Lower Teeth Model"
        )
        self.tongue_model = self._resolve_model(
            self.tongue_model,
            u"Tongue Model"
        )
        self.gum_model = self._resolve_model(
            self.gum_model,
            u"Gum Model"
        )

        self.source_models = {
            "head_model": self.head_model,
            "left_eye_model": self.left_eye_model,
            "right_eye_model": self.right_eye_model,
            "upper_teeth_model": self.upper_teeth_model,
            "lower_teeth_model": self.lower_teeth_model,
            "tongue_model": self.tongue_model,
            "gum_model": self.gum_model,
        }

        self.validate_mouth_joint_count()
        return True

    def prepare_data(self):
        self.ensure_hierarchy()
        self.config.ensure()

        self.work_model_names = {
            "tweak": name.create_name(
                "model",
                self.side,
                "head",
                "tweak"
            ),
            "stretch": name.create_name(
                "model",
                self.side,
                "head",
                "stretch"
            ),
            "deform": name.create_name(
                "model",
                self.side,
                "head",
                "deform"
            ),
        }

        self.result_models = {}
        return True

    def process_data(self):
        self.result_models = self.create_work_models()
        return self.result_models

    def finalize_step(self):
        self.validate_results()

        self.config.save_setup(
            head_model=self.head_model,
            left_eye_model=self.left_eye_model,
            right_eye_model=self.right_eye_model,
            upper_teeth_model=self.upper_teeth_model,
            lower_teeth_model=self.lower_teeth_model,
            tongue_model=self.tongue_model,
            gum_model=self.gum_model,
            head_tweak_model=self.head_tweak_model,
            head_stretch_model=self.head_stretch_model,
            head_deform_model=self.head_deform_model,
            mouth_joint_count=self.mouth_joint_count
        )

        self.set_step_completed(True)
        self.invalidate_later_steps()
        self.set_current_step(2)
        self.apply_step_visibility(2)
        return True

    def _resolve_model(
            self,
            model,
            label,
            required=False
    ):
        if model is None:
            if required:
                raise RuntimeError(
                    u"{} 不能为空。".format(label)
                )
            return None

        if isinstance(model, str):
            model_name = model.strip()

            if not model_name:
                if required:
                    raise RuntimeError(
                        u"{} 不能为空。".format(label)
                    )
                return None

            if not pm.objExists(model_name):
                raise RuntimeError(
                    u"{} 不存在：{}".format(label, model_name)
                )

            model = pm.PyNode(model_name)

        return self.validate_model(
            model,
            label
        )

    def validate_mouth_joint_count(self):
        if self.mouth_joint_count is None:
            raise RuntimeError(
                u"没有设置 Mouth Joint Count。"
            )

        if isinstance(self.mouth_joint_count, bool):
            raise TypeError(
                u"Mouth Joint Count 必须是整数。"
            )

        if not isinstance(self.mouth_joint_count, int):
            raise TypeError(
                u"Mouth Joint Count 必须是整数。"
            )

        if self.mouth_joint_count < 4:
            raise ValueError(
                u"Mouth Joint Count 不能小于 4。"
            )

        if self.mouth_joint_count % 4 != 0:
            raise ValueError(
                u"Mouth Joint Count 必须是 4 的倍数，当前值为：{}".format(
                    self.mouth_joint_count
                )
            )

        return True

    @staticmethod
    def _duplicate_model(
            source_model,
            model_name,
            parent
    ):
        duplicate = pm.duplicate(
            source_model,
            name=model_name,
            returnRootsOnly=True
        )[0]
        duplicate.setParent(parent)
        return duplicate

    def _get_previous_work_models(self):
        previous_models = []

        if self.config.exists():
            setup_data = self.config.load_setup()

            for attribute_name in config.setup_work_node_attributes:
                model = setup_data.get(attribute_name)

                if model is None:
                    continue

                if pm.objExists(model):
                    previous_models.append(model)

        for model_name in self.work_model_names.values():
            if not pm.objExists(model_name):
                continue

            model = pm.PyNode(model_name)

            if model not in previous_models:
                previous_models.append(model)

        return previous_models

    def delete_old_work_models(self):
        source_nodes = []

        for model in self.source_models.values():
            if model is not None:
                source_nodes.append(model)

        previous_models = self._get_previous_work_models()

        for model in previous_models:
            if model in source_nodes:
                continue

            if pm.objExists(model):
                pm.delete(model)

        return True

    def create_work_models(self):
        work_specs = [
            (
                "tweak",
                "head_tweak_model",
                self.tweak_group
            ),
            (
                "stretch",
                "head_stretch_model",
                self.stretch_group
            ),
            (
                "deform",
                "head_deform_model",
                self.deform_group
            ),
        ]

        pending_models = {}

        try:
            for role, property_name, parent_group in work_specs:
                temporary_name = name.create_unique_name(
                    "model",
                    self.side,
                    "head",
                    "{}_build".format(role)
                )
                duplicate = self._duplicate_model(
                    self.head_model,
                    temporary_name,
                    parent_group
                )
                pending_models[role] = duplicate

        except Exception:
            for model in pending_models.values():
                if pm.objExists(model):
                    pm.delete(model)
            raise

        self.delete_old_work_models()

        result = {}

        for role, property_name, parent_group in work_specs:
            model = pending_models[role]
            model.rename(
                self.work_model_names[role]
            )
            setattr(
                self,
                property_name,
                model
            )
            result[role] = model

        return result

    def validate_results(self):
        result_models = [
            (
                u"Head Tweak Model",
                self.head_tweak_model,
                self.work_model_names["tweak"],
                self.tweak_group
            ),
            (
                u"Head Stretch Model",
                self.head_stretch_model,
                self.work_model_names["stretch"],
                self.stretch_group
            ),
            (
                u"Head Deform Model",
                self.head_deform_model,
                self.work_model_names["deform"],
                self.deform_group
            ),
        ]

        for label, model, expected_name, expected_parent in result_models:
            model = self.validate_model(
                model,
                label
            )

            if model.nodeName() != expected_name:
                raise RuntimeError(
                    u"{} 名称不正确：{}".format(label, model)
                )

            if model.getParent() != expected_parent:
                raise RuntimeError(
                    u"{} Parent 不正确：{}".format(label, model.getParent())
                )

        return True


__all__ = [
    "FaceSetup",
]
