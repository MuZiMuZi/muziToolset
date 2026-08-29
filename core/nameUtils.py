# coding=utf-8
u"""
Name Utils - Compatibility Shim
==============================

正式命名实现已经迁移到 ``core.name_utils``。
本文件仅兼容旧 CamelCase Import，不再维护名称生成、解析、镜像、唯一序号或重名修复逻辑。

新代码请使用：

    from muziToolset.core import name_utils

    name = name_utils.Name.create_name(
        node_type="jnt",
        side="lf",
        part="arm",
        function="bind",
        index=1
    )

兼容导出
--------
Name
maya_undo
dag_depth

等正式调用全部迁移到 snake_case 后，本文件可以删除。
"""

from __future__ import print_function

from .name_utils import Name
from .name_utils import dag_depth
from .name_utils import maya_undo


__all__ = [
    "Name",
    "maya_undo",
    "dag_depth",
]
