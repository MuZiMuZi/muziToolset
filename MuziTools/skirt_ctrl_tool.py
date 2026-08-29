# coding=utf-8
u"""Legacy compatibility wrapper for :mod:`MuziTools.tools.rig.skirt_ctrl_tool`."""

from .tools.rig.skirt_ctrl_tool import SkirtControlTool
from .tools.rig.skirt_ctrl_tool import main


Skirt_ctrl_tool = SkirtControlTool


__all__ = [
    "SkirtControlTool",
    "Skirt_ctrl_tool",
    "main",
]
