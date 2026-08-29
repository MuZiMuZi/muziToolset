# coding=utf-8
u"""Legacy compatibility wrapper for the face driven-key tool."""

from .tools.face.face_select_key_tool import FaceDrivenKeyTool
from .tools.face.face_select_key_tool import Select_key_tool
from .tools.face.face_select_key_tool import add_extra_group
from .tools.face.face_select_key_tool import create_driven_key_setup
from .tools.face.face_select_key_tool import main


__all__ = [
    "FaceDrivenKeyTool",
    "Select_key_tool",
    "add_extra_group",
    "create_driven_key_setup",
    "main",
]
