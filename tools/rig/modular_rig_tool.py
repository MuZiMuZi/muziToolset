# coding=utf-8
u"""
Modular Rig Tool
================

MuziTools 模块化绑定系统主入口。

Tool 层只负责显示窗口，不实现 Module Build 算法。
"""

from __future__ import print_function

from ...systems import rig as rig_system
from ...ui import window_utils


TOOL_MODE = "ui"


def main():
    u"""

        显示并返回 Modular Rig 主窗口。

        Returns:
            object:
                当前工具入口创建并显示的窗口或执行结果。

    """
    return window_utils.show_window(
        "tools.rig.modular_rig_tool",
        rig_system.create_ui
    )


if __name__ == "__main__":
    main()
