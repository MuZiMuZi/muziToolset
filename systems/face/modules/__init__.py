# coding=utf-8
u"""
Face Rig Step 03 正式 Modules。

所有 Face Module 统一使用：
    load_setup()
    load_guide()
    create_jnt()
    create_ctrl()
    create_connect()
    create_deform()
    create_finalize()
    create_build()

旧 Face Module 生命周期不再作为正式 API 维护。
"""

from __future__ import print_function

from .face_module_base import FaceModuleBase
from .jaw import JawModule
from .jaw import build_jaw
from .teeth import TeethModule
from .teeth import build_teeth


__all__ = [
    "FaceModuleBase",
    "JawModule",
    "TeethModule",
    "build_jaw",
    "build_teeth",
]
