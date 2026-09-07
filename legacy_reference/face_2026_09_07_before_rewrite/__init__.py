# coding=utf-8
u"""
Muzi Face Rig System
====================

Face Rig 的正式系统包。

公共结构：
    - FaceSetup / FaceGuide / FaceBuild / FaceFinalizer：四步 Face Workflow；
    - FaceModuleBase：所有正式 Face Rig Module 的统一生命周期；
    - FaceRig：按依赖顺序组装完整 Face Rig；
    - Brow / Cheek / Ear / Eye / Eyelid / Jaw / Lip / Mouth / Nose / Teeth / Tongue：独立绑定模块；
    - build 包：Step 03 Workflow 与 Curve Attachment / Eyelid / Zip Lip 等可复用底层算法；
    - finalize 包：Step 04 最终验收、Controller Set 和显示管理。
"""

from __future__ import print_function

# Controller Appearance 的正式默认值必须在 Face Build / Module 被导入前应用，
# 这样 UI、FaceBuild 和单独 Module Build 始终读取同一份运行时配置。
from .controller_defaults import apply_controller_defaults

apply_controller_defaults()

from .build import attach_jnts_to_curves
from .build import build_eye_bag_jnts
from .build import build_eyelid_jnts
from .build import build_radial_curve_jnts
from .build import build_zip_lip
from .build.face_build import FaceBuild
from .build.face_build import build_face_step
from .face_base import FaceBase
from .finalize import FaceFinalizer
from .finalize import finalize_face
from .guide import FaceGuide
from .modules import BrowModule
from .modules import CheekModule
from .modules import EarModule
from .modules import EyeModule
from .modules import EyelidModule
from .modules import FaceModuleBase
from .modules import FaceRig
from .modules import JawModule
from .modules import LipModule
from .modules import MouthModule
from .modules import NoseModule
from .modules import TeethModule
from .modules import TongueModule
from .modules import build_brow
from .modules import build_cheek
from .modules import build_ear
from .modules import build_eye
from .modules import build_eyelid
from .modules import build_face
from .modules import build_jaw
from .modules import build_lip
from .modules import build_mouth
from .modules import build_nose
from .modules import build_teeth
from .modules import build_tongue
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
    "FaceBuild",
    "FaceFinalizer",
    "FaceRig",
    "BrowModule",
    "CheekModule",
    "EarModule",
    "EyeModule",
    "EyelidModule",
    "JawModule",
    "LipModule",
    "MouthModule",
    "NoseModule",
    "TeethModule",
    "TongueModule",
    "attach_jnts_to_curves",
    "build_radial_curve_jnts",
    "build_eyelid_jnts",
    "build_eye_bag_jnts",
    "build_zip_lip",
    "build_face_step",
    "finalize_face",
    "build_face",
    "build_brow",
    "build_cheek",
    "build_ear",
    "build_eye",
    "build_eyelid",
    "build_jaw",
    "build_lip",
    "build_mouth",
    "build_nose",
    "build_teeth",
    "build_tongue",
    "show",
]
