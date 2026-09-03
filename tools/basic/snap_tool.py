# coding=utf-8
u"""
Quick Snap Tool
===============

选择规则：
    1. 前面的选择作为参考；
    2. 最后一个选择作为目标；
    3. 吸附到参考项平均位置；
    4. Transform / Joint 同时使用有效参考对象的平均旋转。

实际吸附算法维护在：
    muziToolset.core.snap_utils

当前 Selection 查询统一复用 core.scene_utils，Tool 只解释选择顺序的交互语义。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import scene_utils
from ...core import snap_utils


TOOL_MODE = "action"


def main():
    u"""
    按当前 Maya 选择执行一次快速吸附。

    Returns:
        bool:
        吸附成功返回 True；选择不足或吸附失败返回 False。
    """
    selected_items = scene_utils.get_selected_nodes(
        long=True,
        flatten=True
    )

    if len(selected_items) < 2:
        cmds.warning(
            u"至少选择两个对象或组件，最后一个作为被吸附目标。"
        )
        return False

    reference_items = selected_items[:-1]
    target_item = selected_items[-1]

    scene_utils.open_undo_chunk(
        "MuziQuickSnap"
    )

    try:
        snap_utils.snap_to_average(
            reference_items=reference_items,
            target_item=target_item,
            include_rotation=True
        )
    except Exception as error:
        cmds.warning(
            str(error)
        )
        return False
    finally:
        scene_utils.close_undo_chunk()

    return True


__all__ = [
    "main",
]
