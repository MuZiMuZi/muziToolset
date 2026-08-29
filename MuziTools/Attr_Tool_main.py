# coding=utf-8
u"""Legacy compatibility wrapper for :mod:`MuziTools.tools.basic.attr_tool`."""

from .tools.basic.attr_tool import AttrTool
from .tools.basic.attr_tool import main


# 兼容旧代码：Attr_Tool()
Attr_Tool = AttrTool


__all__ = [
    "AttrTool",
    "Attr_Tool",
    "main",
]
