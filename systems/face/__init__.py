# coding=utf-8
u"""
Muzi Face Rig System
====================

Face Rig 的正式系统包。

公共入口只暴露稳定的 Face System API；
上层 Tool / Wizard 不需要依赖各组件内部 builder 文件路径。
"""

from __future__ import print_function

from .curve_attachment import attach_joints_to_curves
from .eyelid import build_eye_bag_joints
from .eyelid import build_eyelid_joints
from .eyelid import build_radial_curve_joints
from .face_base import FaceBase
from .face_guide import FaceGuide
from .face_setup import FaceSetup
from .lip import build_zip_lip


def show():
    u"""
    打开 Face Rig Wizard。

    Returns:
        object:
            方法执行后的结果数据。
    """
    from . import wizard

    return wizard.main()


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
