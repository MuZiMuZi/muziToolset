# coding=utf-8
u"""
Attribute Utils - Compatibility Shim
====================================

兼容说明
--------
正式实现已经迁移到 ``core.attr_utils``。
本文件只保留旧 ``from muziToolset.core import attrUtils`` 调用的兼容入口，
不再维护任何 Attribute 业务逻辑。

新代码请使用：

    from muziToolset.core import attr_utils

    attr = attr_utils.Attr("ctrl_md_root_001")

保留这个薄壳的原因，是避免尚未迁移的旧 Tool / System 在本轮重构中突然失效。
等所有正式调用都切换到 snake_case 后，本文件可以安全删除。
"""

from __future__ import print_function

from .attr_utils import Attr


__all__ = [
    "Attr",
]
