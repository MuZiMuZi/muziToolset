# coding=utf-8
u"""
Muzi Face Rig System
====================

Face Rig 的正式系统包。
"""

from __future__ import print_function

from .face_base import FaceBase
from .face_guide import FaceGuide
from .face_setup import FaceSetup


def show():
    """打开 Face Rig Wizard。"""
    from . import wizard

    return wizard.main()


__all__ = [
    "FaceBase",
    "FaceGuide",
    "FaceSetup",
    "show",
]
