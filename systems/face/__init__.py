# coding=utf-8
u"""
Muzi Face Rig System
====================

Face Rig 的正式系统包。

公共入口只暴露稳定 Face API；完整业务单元使用 Module 术语，
底层曲线 / 眼睑 / Zip Lip 算法继续由 build 包提供。
"""

from __future__ import print_function

from .build import attach_joints_to_curves
from .build import build_eye_bag_joints
from .build import build_eyelid_joints
from .build import build_radial_curve_joints
from .build import build_zip_lip
from .face_base import FaceBase
from .guide import FaceGuide
from .modules import TeethModule
from .modules import build_teeth
from .setup import FaceSetup


def show():
    u"""打开正式 Face Rig Workflow UI。"""
    from . import ui

    return ui.show()


__all__ = [
    "FaceBase",
    "FaceGuide",
    "FaceSetup",
    "TeethModule",
    "attach_joints_to_curves",
    "build_radial_curve_joints",
    "build_eyelid_joints",
    "build_eye_bag_joints",
    "build_zip_lip",
    "build_teeth",
    "show",
]
