# coding=utf-8
u"""
FK Control Creator
==================

根据 Maya 当前选择顺序创建 FK Controller Chain。

实际控制器创建统一使用 systems.ctrl_base；
Rig Name 统一使用 systems.rig_base.RigBase。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import rename_utils
from ...systems import ctrl_base
from ...systems.rig_base import RigBase


TOOL_MODE = "action"


def _clean_part(text):
    u"""把任意 Maya Short Name 整理成 RigBase part。"""
    text = str(text).strip().lower()
    text = text.replace("|", "_")
    text = text.replace(":", "_")
    text = text.replace(" ", "_")
    text = text.replace("-", "_")

    while "__" in text:
        text = text.replace("__", "_")

    text = text.strip("_")

    if not text:
        text = "fk"

    return text


def get_fk_ctrl_name(target, fallback_index):
    u"""根据 Target 生成标准 FK Ctrl Name。"""
    short_name = rename_utils.get_short_name(
        target
    )

    if RigBase.validate_name(short_name):
        fields = RigBase.parse_name(
            short_name
        )
        return RigBase.create_name(
            type="ctrl",
            side=fields["side"],
            part=fields["part"],
            function=fields["function"],
            index=fields["index"]
        )

    return RigBase.create_name(
        type="ctrl",
        side="md",
        part=_clean_part(short_name),
        function="fk",
        index=fallback_index
    )


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
    selections = cmds.ls(
        selection=True,
        long=True
    )

    if selections is None:
        selections = []

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
