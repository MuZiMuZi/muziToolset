# coding=utf-8
u"""
Face Rig Build Utilities
========================

本包只保留可复用的底层 Face Build Algorithm。
Jaw / Teeth / Eye / Brow 等完整业务单元统一放在 systems.face.modules。
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
