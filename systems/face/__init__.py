# coding=utf-8
u"""PyMEL-first Face Rig System。"""

from __future__ import print_function

from .face_base import FaceBase
from .face_config import FaceConfig


def show():
    from .ui import show as show_face_ui
    return show_face_ui()


__all__ = [
    "FaceBase",
    "FaceConfig",
    "show",
]
