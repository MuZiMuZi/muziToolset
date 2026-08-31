# coding=utf-8
u"""
Muzi Rig Systems
================

systems/ 负责把 PyMEL Node 操作和 Core 算法组合成完整 Rig Component。

当前正式保留：

    component_base.py
        通用 Component 生命周期。

    face/
        当前唯一继续开发和迁移的业务系统。

Body、Controller 等旧实现已经进入 legacy_reference，
后续会基于新的 PyMEL-first 架构重新实现。
"""

from __future__ import print_function

from .component_base import ComponentBase
from .component_base import RigComponentBase

__all__ = [
    "ComponentBase",
    "RigComponentBase",
]
