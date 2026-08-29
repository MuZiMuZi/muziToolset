# coding=utf-8
u"""
Hierarchy Utils - Compatibility Shim
====================================

正式实现已经迁移到 ``core.hierarchy_utils``。
本文件仅用于兼容旧 CamelCase 模块路径，不再维护 DAG 层级业务逻辑。

新代码请使用：

    from muziToolset.core import hierarchy_utils

    group = hierarchy_utils.Hierarchy.add_extra_group(
        "ctrl_md_root_001",
        "zero_md_root_001"
    )

等正式调用全部迁移到 snake_case 后，本文件可以删除。
"""

from __future__ import print_function

from .hierarchy_utils import Hierarchy


__all__ = [
    "Hierarchy",
]
