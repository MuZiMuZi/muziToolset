# coding=utf-8
u"""
Joint Utils - Compatibility Shim
===============================

正式 Joint 实现已经迁移到 ``core.joint_utils``。
本文件只负责兼容旧 CamelCase Import，不再维护 Joint 创建、查询、显示、Curve Bridge 或 Chain 逻辑。

新代码请使用：

    from muziToolset.core import joint_utils

    joint = joint_utils.Joint.create(
        name="jnt_md_spine_bind_001",
        position=[0.0, 10.0, 0.0]
    )

兼容导出
--------
Joint
JointCurve
JointChain

等正式调用全部迁移到 snake_case 后，本文件可以删除。
"""

from __future__ import print_function

from .joint_utils import Joint
from .joint_utils import JointChain
from .joint_utils import JointCurve


__all__ = [
    "Joint",
    "JointCurve",
    "JointChain",
]
