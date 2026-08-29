# coding=utf-8
u"""Legacy compatibility wrapper for :mod:`MuziTools.tools.joint.joint_tool`."""

from .tools.joint.joint_tool import JointTool
from .tools.joint.joint_tool import main


Joint_Tool = JointTool


__all__ = [
    "JointTool",
    "Joint_Tool",
    "main",
]
