# coding=utf-8
u"""Muzi Rigging 应用启动入口。"""

from __future__ import print_function

from . import toolbox


def main():
    u"""
    打开 Muzi Rigging 主工具箱。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    return toolbox.main()


if __name__ == "__main__":
    main()
