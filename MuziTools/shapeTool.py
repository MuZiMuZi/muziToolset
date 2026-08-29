# coding=utf-8
u"""Legacy compatibility wrapper for the BlendShape invert-shape tool."""

from .tools.blendShape.invert_shape_tool import InvertShapeTool
from .tools.blendShape.invert_shape_tool import invert_shapes
from .tools.blendShape.invert_shape_tool import main


shape_Tool = InvertShapeTool


__all__ = [
    "InvertShapeTool",
    "shape_Tool",
    "invert_shapes",
    "main",
]
