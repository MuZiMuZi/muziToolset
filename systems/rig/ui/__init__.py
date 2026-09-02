# coding=utf-8
u"""Modular Rig UI Package。"""

from __future__ import print_function


def create_window():
    u"""创建 Modular Rig Window。"""
    from .modular_rig_ui import ModularRigWindow

    return ModularRigWindow()


__all__ = [
    "create_window",
]
