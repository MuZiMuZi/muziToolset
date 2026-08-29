# coding=utf-8
u"""Legacy compatibility wrapper for :mod:`MuziTools.tools.rig.rig_tool`."""

from .tools.rig.rig_tool import RigTool
from .tools.rig.rig_tool import create_ik_rig
from .tools.rig.rig_tool import main


Rig_Tool = RigTool


__all__ = [
    "RigTool",
    "Rig_Tool",
    "create_ik_rig",
    "main",
]
