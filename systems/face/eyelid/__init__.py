# coding=utf-8
u"""
Face Eyelid System
==================

眼皮 / 眼袋 Curve 驱动绑定系统。

职责：
    - 基于眼皮 Curve 创建放射状 Joint；
    - 创建 Curve Attachment；
    - 以眼球中心为 Pivot 建立 Aim 驱动；
    - 眼皮和眼袋共用同一套底层构建逻辑。

本包属于完整 Face Rig System，不允许被 core 反向依赖。
"""

from __future__ import print_function


__all__ = []
