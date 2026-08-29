# coding=utf-8
u"""
muziToolset
===========

仓库级启动入口。

正式运行代码位于 ``muzi_rigging`` 主包。
历史参考代码位于 ``legacy_reference``，不会参与正常启动。
"""

from __future__ import print_function


def show():
    """打开 Muzi Rigging 主工具箱。"""
    from .muzi_rigging import show as show_rigging

    return show_rigging()


def initialize():
    """初始化并打开主工具箱。"""
    return show()
