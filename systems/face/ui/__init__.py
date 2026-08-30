# coding=utf-8
u"""Face Rig UI Package。"""

from __future__ import print_function


def show():
    u"""创建并返回 Face Rig Wizard。"""
    from . import face_rig_ui

    return face_rig_ui.main()


__all__ = [
    "show",
]
