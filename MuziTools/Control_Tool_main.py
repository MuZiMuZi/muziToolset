# coding=utf-8
u"""Legacy compatibility wrapper for the controller Shape tool."""

from .tools.ctrl.control_shape_tool import ControlShapeTool
from .tools.ctrl.control_shape_tool import main


# 兼容旧工具和旧 Shelf 中的类名。
ControlsWidget = ControlShapeTool


__all__ = [
    "ControlShapeTool",
    "ControlsWidget",
    "main",
]
