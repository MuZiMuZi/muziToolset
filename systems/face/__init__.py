# coding=utf-8
u"""
Muzi Face Rig System
====================

Face Rig 的正式系统包。

公共入口只暴露稳定的 Face System API；
上层 Tool / UI 不需要依赖各 Step / Component 内部文件路径。
"""

from __future__ import print_function

from .build import attach_joints_to_curves
from .build import build_eye_bag_joints
from .build import build_eyelid_joints
from .build import build_radial_curve_joints
from .build import build_zip_lip
from .face_base import FaceBase
from .guide import FaceGuide
from .setup import FaceSetup


def show():
    u"""打开 Face Rig UI。"""
    from .ui import face_rig_ui

    return face_rig_ui.main()


__all__ = [
    "FaceBase",
    "FaceGuide",
    "FaceSetup",
    "attach_joints_to_curves",
    "build_radial_curve_joints",
    "build_eyelid_joints",
    "build_eye_bag_joints",
    "build_zip_lip",
    "show",
]
