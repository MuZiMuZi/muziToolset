# coding=utf-8
u"""Face Rig UI Package。"""

from __future__ import print_function


def show():
    u"""创建并返回带 Config 恢复和 Workflow Visibility 的正式 Face Rig Wizard。"""
    from . import workflow_controller

    return workflow_controller.main()


__all__ = [
    "show",
]
