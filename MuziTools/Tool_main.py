# coding=utf-8
u"""
Legacy Main Entry
=================

旧版 ``Tool_main.py`` 曾经直接导入多个 ``*_Tool_main.py`` 并把它们塞进
QTabWidget。那些旧实现已经由 ``MuziTools/tools/<category>/`` 中的新工具取代。

本文件只保留一个轻量入口，统一打开当前 ``rigging_toolbox``。
"""

from .rigging_toolbox import Rigging_Toolbox
from .rigging_toolbox import main


# 兼容极少量仍可能直接实例化旧类名的脚本。
Tool_main_Window = Rigging_Toolbox


__all__ = [
    "Rigging_Toolbox",
    "Tool_main_Window",
    "main",
]
