# coding=utf-8
u"""
Face Rig Build Utilities
========================

本包只保留可复用的底层 Face Build Algorithm。
Jaw / Teeth / Eye / Brow 等完整业务单元统一放在 systems.face.modules。
"""

from __future__ import print_function

from .curve_attachment import attach_jnts_to_curves
from .eyelid import build_eye_bag_jnts
from .eyelid import build_eyelid_jnts
from .eyelid import build_radial_curve_jnts
from .lip import build_zip_lip


__all__ = [
    "attach_jnts_to_curves",
    "build_radial_curve_jnts",
    "build_eyelid_jnts",
    "build_eye_bag_jnts",
    "build_zip_lip",
]
