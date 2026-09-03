# coding=utf-8
u"""
MuziTools Rig System
====================

模块化绑定系统的正式 System Package。

当前阶段先提供 Modular Rig 主界面。
后续 RigBase / ModuleBase / Template / Build / Rebuild 会逐步收敛到本 Package。
"""

from __future__ import print_function


def create_ui():
    u"""
    创建并返回 Modular Rig 主界面。

    Returns:
        object:
        创建或构建完成后的 Maya / Rig 对象或 Build Result。
    """
    from . import ui

    return ui.create_window()


__all__ = [
    "create_ui",
]
