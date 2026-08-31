# coding=utf-8
u"""Face Rig Step 04 Finalize。"""

from __future__ import print_function

from ..face_base import FaceBase


class FaceFinalize(FaceBase):
    u"""Face Rig Step 04。"""

    def __init__(self):
        super(FaceFinalize, self).__init__()
        self.step_value = 4

    def collect_inputs(self):
        self.validate_setup_data(require_mouth_joint_count=True)
        if not self.is_step_completed(3):
            raise RuntimeError(u"Face Build Step 尚未完成。")
        return True

    def prepare_data(self):
        self.ensure_hierarchy()
        return True

    def process_data(self):
        self.apply_step_visibility(4)
        return True

    def finalize_step(self):
        self.set_step_completed(True)
        self.set_current_step(4)
        return True


__all__ = [
    "FaceFinalize",
]
