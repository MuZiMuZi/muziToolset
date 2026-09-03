# coding=utf-8
u"""
Face Rig Step 04 - Finalize
===========================

最终验收、Controller Set 和显示管理统一由 FaceFinalizer 负责。
文件 Export / Publish 暂不属于当前 Step 04 第一版。
"""

from __future__ import print_function

from .finalizer import FaceFinalizer
from .finalizer import finalize_face


__all__ = [
    "FaceFinalizer",
    "finalize_face",
]
