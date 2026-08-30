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
    u"""
    调用统一 Controller System 创建 FK 控制器。

    Args:
        targets (str | list[str]):
            `targets` 对应的输入数据。
        shape (str):
            `shape` 对应的名称、标记或字符串参数。
        radius (float):
            创建节点或控制器使用的半径值。
        axis (str):
            操作使用的轴向标记。
        constrain (bool):
            是否启用 `constrain` 对应的处理。

    Returns:
        object:
            方法执行后的结果数据。
    """
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
    u"""
    按当前 Maya 选择顺序创建 FK 控制器链。

    Returns:
        object | list:
            方法执行后的结果数据。
    """
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
