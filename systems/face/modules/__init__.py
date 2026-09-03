# coding=utf-8
u"""
Face Rig 正式 Modules
=====================

所有独立 Face Rig Module 统一使用：
    load_setup()
    load_guide()
    create_jnt()
    create_ctrl()
    create_connect()
    create_deform()
    create_finalize()
    create_build()

旧 Face Module 生命周期不再作为正式 API 维护。
"""

from __future__ import print_function

from .brow import BrowModule
from .brow import build_brow
from .cheek import CheekModule
from .cheek import build_cheek
from .ear import EarModule
from .ear import build_ear
from .eye import EyeModule
from .eye import build_eye
from .eyelid import EyelidModule
from .eyelid import build_eyelid
from .face_module_base import FaceModuleBase
from .face_rig import FaceRig
from .face_rig import build_face
from .jaw import JawModule
from .jaw import build_jaw
from .lip import LipModule
from .lip import build_lip
from .mouth import MouthModule
from .mouth import build_mouth
from .nose import NoseModule
from .nose import build_nose
from .teeth import TeethModule
from .teeth import build_teeth
from .tongue import TongueModule
from .tongue import build_tongue


__all__ = [
    "FaceModuleBase",
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
]
