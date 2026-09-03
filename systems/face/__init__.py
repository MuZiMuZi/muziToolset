# coding=utf-8
u"""
Muzi Face Rig System
====================

Face Rig 的正式系统包。

公共入口：
    - FaceSetup / FaceGuide：工作流 Step；
    - FaceModuleBase：所有正式 Face Rig Module 的统一生命周期；
    - JawModule / TeethModule：当前已经迁移到新模块架构的绑定模块；
    - build 包：Curve / Eyelid / Zip Lip 等底层算法。
"""

from __future__ import print_function

from .build import attach_joints_to_curves
from .build import build_eye_bag_joints
from .build import build_eyelid_joints
from .build import build_radial_curve_joints
from .build import build_zip_lip
from .face_base import FaceBase
from .guide import FaceGuide
from .modules import FaceModuleBase
from .modules import JawModule
from .modules import TeethModule
from .modules import build_jaw
from .modules import build_teeth
from .setup import FaceSetup


def show():
    u"""
    打开正式 Face Rig Workflow UI。

    Returns:
        object:
            当前工具入口创建并显示的窗口或执行结果。
    """
    from . import ui

    return ui.show()


__all__ = [
    "FaceBase",
    "FaceModuleBase",
    "FaceGuide",
    "FaceSetup",
    "JawModule",
    "TeethModule",
    "attach_joints_to_curves",
    "build_radial_curve_joints",
    "build_eyelid_joints",
    "build_eye_bag_joints",
    "build_zip_lip",
    "build_jaw",
    "build_teeth",
    "show",
]
