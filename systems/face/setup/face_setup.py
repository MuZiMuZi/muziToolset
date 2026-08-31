# coding=utf-8
u"""
Step 01 - Face Setup
====================

PyMEL-first 的 Face Setup。
"""

from __future__ import print_function

import pymel.core as pm

from ....core import naming
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

        self.input_models = []
        self.work_model_names = {}

        self.head_tweak_model = None
        self.head_stretch_model = None
        self.head_deform_model = None

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

        self.input_models = [
            self.head_model,
            self.left_eye_model,
            self.right_eye_model,
            self.upper_teeth_model,
            self.lower_teeth_model,
            self.tongue_model,
            self.gum_model,
        ]

        self.validate_mouth_joint_count()
        return True

    def prepare_data(self):
        self.ensure_hierarchy()

        self.work_model_names = {
            "tweak": naming.create_name(
                "model",
                self.side,
                "head",
                "tweak"
            ),
            "stretch": naming.create_name(
                "model",
                self.side,
                "head",
                "stretch"
            ),
            "deform": naming.create_name(
                "model",
                self.side,
                "head",
                "deform"
            ),
        }

        self.delete_old_work_models()
        return True

    def process_data(self):
        self.parent_input_models()
        self.create_work_models()
        return True

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
            mouth_joint_count=self.mouth_joint_count
        )

        self.set_step_completed(True)
        self.invalidate_later_steps()
        self.set_current_step(2)
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

    def parent_input_models(self):
        for model in self.input_models:
            if model is None:
                continue

            if model.getParent() != self.model_group:
                model.setParent(self.model_group)

        return True

    def delete_old_work_models(self):
        for model_name in self.work_model_names.values():
            if not pm.objExists(model_name):
                continue

            pm.delete(
                pm.PyNode(model_name)
            )

        return True

    @staticmethod
    def _duplicate_model(
            source_model,
            name,
            parent
    ):
        duplicate = pm.duplicate(
            source_model,
            name=name,
            returnRootsOnly=True
        )[0]
        duplicate.setParent(parent)
        return duplicate

    def create_work_models(self):
        self.head_tweak_model = self._duplicate_model(
            self.head_model,
            self.work_model_names["tweak"],
            self.tweak_group
        )
        self.head_stretch_model = self._duplicate_model(
            self.head_model,
            self.work_model_names["stretch"],
            self.stretch_group
        )
        self.head_deform_model = self._duplicate_model(
            self.head_model,
            self.work_model_names["deform"],
            self.deform_group
        )
        return True

    def validate_results(self):
        result_models = [
            (u"Head Tweak Model", self.head_tweak_model),
            (u"Head Stretch Model", self.head_stretch_model),
            (u"Head Deform Model", self.head_deform_model),
        ]

        for label, model in result_models:
            self.validate_model(
                model,
                label
            )

        return True


__all__ = [
    "FaceSetup",
]
