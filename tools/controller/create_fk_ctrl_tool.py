# coding=utf-8
u"""
FK Control Creator
==================

根据 Maya 当前选择顺序创建 FK 控制器链。

本工具只负责用户入口，实际 Controller 创建逻辑统一维护在：
    muzi_rigging.systems.controller
"""

from __future__ import print_function

import maya.cmds as cmds

from ...systems import controller as controller_system


def create_fk_controls(
        targets,
        shape="circle",
        radius=1.0,
        axis="Y+",
        constrain=True
):
    """调用统一 Controller System 创建 FK 控制器。"""
    return controller_system.create_fk_controls(
        targets=targets,
        shape=shape,
        radius=radius,
        axis=axis,
        constrain=constrain,
        create_extra_groups=True,
        add_to_set=True
    )


def main():
    """按当前 Maya 选择顺序创建 FK 控制器链。"""
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
    "main",
]
