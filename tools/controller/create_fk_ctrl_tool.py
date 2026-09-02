# coding=utf-8
u"""
FK Control Creator
==================

根据 Maya 当前选择顺序创建 FK Controller Chain。

实际控制器创建统一使用 systems.ctrl_base；
Rig Name 统一使用 systems.rig_base.RigBase；
外部 Maya Name Token 和 Selection 查询统一复用 Core。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import rename_utils
from ...core import scene_utils
from ...systems import ctrl_base
from ...systems.rig_base import RigBase


TOOL_MODE = "action"


def get_fk_ctrl_name(target, fallback_index):
    u"""根据 Target 名称生成标准 FK Ctrl Name。"""
    short_name = rename_utils.get_short_name(
        target
    )

    try:
        target_name = RigBase(
            name=short_name
        )
        return target_name.create_name(
            type="ctrl"
        )
    except (IndexError, ValueError):
        pass

    rig_name = RigBase(
        type="ctrl",
        side="md",
        part=rename_utils.get_name_token(
            short_name,
            fallback="fk"
        ),
        function="fk",
        index=fallback_index
    )

    return rig_name.name


def create_fk_controls(
        targets,
        shape="circle",
        radius=1.0,
        axis="Y+",
        constrain=True
):
    u"""使用 CtrlBase 创建标准 FK Controller Chain。"""
    if not targets:
        return []

    ctrl_name_list = []
    target_index = 0

    while target_index < len(targets):
        ctrl_name = get_fk_ctrl_name(
            targets[target_index],
            target_index + 1
        )
        ctrl_name_list.append(
            ctrl_name
        )
        target_index += 1

    return ctrl_base.create_fk_ctrl(
        target_list=targets,
        ctrl_name_list=ctrl_name_list,
        shape=shape,
        radius=radius,
        axis=axis,
        constrain=constrain,
        add_to_set=True
    )


def main():
    u"""按当前 Maya 选择顺序创建 FK Controller Chain。"""
    selections = scene_utils.get_selected_nodes(
        long=True,
        flatten=True
    )

    if not selections:
        cmds.warning(
            u"请选择多个物体或 Joint 后再创建 FK 控制器。"
        )
        return []

    return create_fk_controls(
        targets=selections,
        shape="circle",
        radius=1.0,
        axis="Y+",
        constrain=True
    )


__all__ = [
    "create_fk_controls",
    "get_fk_ctrl_name",
    "main",
]
