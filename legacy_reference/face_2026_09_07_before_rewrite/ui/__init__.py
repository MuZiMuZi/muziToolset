# coding=utf-8
u"""Face Rig UI Package。"""

from __future__ import print_function


def show():
    u"""
    创建并返回带 Setup、Guide、Build 和 Finalize 的正式 Face Rig Wizard。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    from . import face_rig_controller

    return face_rig_controller.main()


__all__ = [
    "show",
]
