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
            需要批量处理的 Target 节点；在 Constraint / BlendShape / Controller API 中保持输入顺序。
        shape (str):
            Controller、Curve 或 Geometry 的 Shape 节点 / Shape 名称。
        radius (float):
            创建节点或控制器使用的半径值。
        axis (str):
            操作使用的轴向标记。
        constrain (bool):
            创建 Controller 后是否建立 Controller / Output 到 Target 的约束关系。

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
