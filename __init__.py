# coding=utf-8
u"""
muziToolset
===========

仓库根包就是正式 Maya Rigging Toolset。

迁移阶段同时兼容：
    1. 新根架构：app / ui / core / tools / systems / resources
    2. 旧过渡架构：muzi_rigging

等根架构迁移完成后，会删除旧兼容分支。
"""

from __future__ import print_function


__version__ = "0.3.0"


def show():
    """打开 Muzi Rigging 主工具箱。"""
    try:
        from .app import toolbox
        return toolbox.main()
    except ImportError:
        from .muzi_rigging import show as show_rigging
        return show_rigging()


def initialize():
    """初始化并打开主工具箱。"""
    return show()
