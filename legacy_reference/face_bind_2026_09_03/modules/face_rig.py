# coding=utf-8
u"""
Face Rig Orchestrator
=====================

FaceRig 只负责组织正式 Face Module 的构建顺序，不包含任何具体部位绑定算法。

依赖顺序：
    EyeModule
        -> EyelidModule

    JawModule
        -> LipModule
            -> MouthModule

其它模块彼此独立，但仍使用固定顺序保证场景结果稳定、便于测试和 Rebuild。
"""

from __future__ import print_function

from .brow import BrowModule
from .cheek import CheekModule
from .ear import EarModule
from .eye import EyeModule
from .eyelid import EyelidModule
from .jaw import JawModule
from .lip import LipModule
from .mouth import MouthModule
from .nose import NoseModule
from .teeth import TeethModule
from .tongue import TongueModule


class FaceRig(object):
    u"""按确定性依赖顺序构建全部正式 Face Module。"""

    module_classes = [
        BrowModule,
        EyeModule,
        EyelidModule,
        NoseModule,
        CheekModule,
        EarModule,
        JawModule,
        TeethModule,
        TongueModule,
        LipModule,
        MouthModule,
    ]

    def __init__(self):
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

        """

        self.module_list = []
        self.module_dict = {}

    def create_build(self):
        u"""
        依次实例化并构建全部 Face Module。

        Returns:
            dict:
            Key 为模块 part，Value 为对应模块 create_build() 的公开结果字典。
        """
        self.module_list = []
        self.module_dict = {}

        for module_class in self.module_classes:
            face_module = module_class()
            face_module_dict = face_module.create_build()

            self.module_list.append(
                face_module
            )
            self.module_dict[face_module.part] = face_module_dict

        return self.module_dict


def build_face():
    u"""

        构建完整 Face Rig，并返回全部模块结果。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    face_rig = FaceRig()
    face_rig_dict = face_rig.create_build()
    return face_rig_dict


__all__ = [
    "FaceRig",
    "build_face",
]
