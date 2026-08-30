# coding=utf-8
u"""
Face Rig Step 03 - Build
========================

Step 03 的正式构建包。

公共入口只暴露稳定 Builder API；具体 Jaw / Lip / Eye / Eyelid / Brow 等
Component 可以继续在本包下独立扩展。
"""

from __future__ import print_function

from .curve_attachment import attach_joints_to_curves
from .eyelid import build_eye_bag_joints
from .eyelid import build_eyelid_joints
from .eyelid import build_radial_curve_joints
from .lip import build_zip_lip


__all__ = [
    "attach_joints_to_curves",
    "build_radial_curve_joints",
    "build_eyelid_joints",
    "build_eye_bag_joints",
    "build_zip_lip",
]
