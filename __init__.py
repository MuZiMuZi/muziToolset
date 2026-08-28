# coding=utf-8
u"""
muziToolset
===========

Maya Rigging Toolset 主包。
"""


def show():
    """
    打开 MuziTools 主工具箱。
    """
    from .MuziTools import show as show_tools

    return show_tools()