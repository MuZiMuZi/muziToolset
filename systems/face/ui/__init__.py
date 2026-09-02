# coding=utf-8
u"""Face Rig UI Package。"""

from __future__ import print_function


def show():
    u"""
    创建并返回带 Config 恢复、Workflow Visibility 和 Step 03 Build 的正式 Face Rig Wizard。

    Returns:
        object:
            方法执行后的结果数据。
    """
    from . import build_controller

    return build_controller.main()


__all__ = [
    "show",
]
