# coding=utf-8
u"""Face Rig UI。"""

from __future__ import print_function

from .workflow_controller import FaceRigWindow


window_instance = None


def show():
    u"""打开唯一 Face Rig Window。"""
    global window_instance

    if window_instance is not None:
        try:
            window_instance.close()
            window_instance.deleteLater()
        except Exception:
            pass

    window_instance = FaceRigWindow()
    window_instance.show()
    window_instance.raise_()
    window_instance.activateWindow()
    return window_instance


__all__ = [
    "FaceRigWindow",
    "show",
]
