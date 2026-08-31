# coding=utf-8
u"""
Face Build
==========

Face Rig Step 03 的构建编排器。
"""

from __future__ import print_function

from ..face_base import FaceBase
from .teeth_component import TeethComponent


class FaceBuild(FaceBase):
    u"""Face Rig Step 03。"""

    def __init__(self, build_teeth=True):
        super(FaceBuild, self).__init__()
        self.step_value = 3
        self.build_teeth = bool(build_teeth)
        self.results = {}

    def collect_inputs(self):
        self.validate_setup_data(require_mouth_joint_count=True)
        if not self.is_step_completed(2):
            raise RuntimeError(u"Face Guide Step 尚未完成。")
        return True

    def prepare_data(self):
        self.ensure_hierarchy()
        self.results = {}
        return True

    def process_data(self):
        if self.build_teeth:
            if self.upper_teeth_model is not None and self.lower_teeth_model is not None:
                teeth_component = TeethComponent()
                teeth_component.run_step()
                self.results["teeth"] = teeth_component
        return self.results

    def finalize_step(self):
        self.set_step_completed(True)
        self.invalidate_later_steps()
        self.set_current_step(4)
        return True


__all__ = [
    "FaceBuild",
]
