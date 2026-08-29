# coding=utf-8
u"""Legacy compatibility wrapper for :mod:`MuziTools.tools.basic.constraint_tool`."""

from .tools.basic.constraint_tool import ConstraintTool
from .tools.basic.constraint_tool import main


Constraint_Tool = ConstraintTool


__all__ = [
    "ConstraintTool",
    "Constraint_Tool",
    "main",
]
