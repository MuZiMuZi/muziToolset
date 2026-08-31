# coding=utf-8
u"""
Rig Control
===========

Muzi Toolset 标准 Controller Hierarchy。

这是项目自己的 Rig 结构规则，不是对 PyMEL 的通用包装。
"""

from __future__ import print_function

import pymel.core as pm

from . import name as name_rule


axis_normals = {
    "X+": (1.0, 0.0, 0.0),
    "X-": (-1.0, 0.0, 0.0),
    "Y+": (0.0, 1.0, 0.0),
    "Y-": (0.0, -1.0, 0.0),
    "Z+": (0.0, 0.0, 1.0),
    "Z-": (0.0, 0.0, -1.0),
}


def _resolve_node(node, label):
    if node is None:
        return None

    if isinstance(node, str):
        if not pm.objExists(node):
            raise RuntimeError(
                u"{} 不存在：{}".format(label, node)
            )
        node = pm.PyNode(node)

    return node


def _set_curve_color(control, color_index):
    for shape in control.getShapes(noIntermediate=True):
        shape.overrideEnabled.set(True)
        shape.overrideColor.set(
            int(color_index)
        )


def _create_circle(
        control_name,
        radius,
        axis
):
    normal = axis_normals.get(axis)

    if normal is None:
        raise ValueError(
            u"不支持的 Controller Axis：{}".format(axis)
        )

    return pm.circle(
        name=control_name,
        normal=normal,
        radius=float(radius),
        constructionHistory=False
    )[0]


def create_control(
        control_name,
        radius=1.0,
        axis="Y+",
        target=None,
        parent=None,
        color=17,
        create_sub_control=False,
        add_to_set=True,
        control_set=None
):
    u"""创建 Muzi 标准 Controller Hierarchy。"""
    target = _resolve_node(
        target,
        u"Control Target"
    )
    parent = _resolve_node(
        parent,
        u"Control Parent"
    )

    hierarchy_types = [
        "zero",
        "driven",
        "space",
        "connect",
        "offset",
    ]
    groups = {}
    previous_group = None

    for group_type in hierarchy_types:
        group_name = name_rule.replace_node_type(
            control_name,
            group_type
        )

        if pm.objExists(group_name):
            raise RuntimeError(
                u"Controller Group 已经存在：{}".format(group_name)
            )

        group = pm.createNode(
            "transform",
            name=group_name
        )

        if previous_group is not None:
            group.setParent(
                previous_group
            )

        groups[group_type] = group
        previous_group = group

    control = _create_circle(
        control_name,
        radius,
        axis
    )
    control.setParent(
        groups["offset"]
    )
    _set_curve_color(
        control,
        color
    )

    sub_control = None
    output_parent = control

    if create_sub_control:
        sub_name = "{}_sub".format(control_name)
        sub_control = _create_circle(
            sub_name,
            float(radius) * 0.7,
            axis
        )
        sub_control.setParent(
            control
        )
        _set_curve_color(
            sub_control,
            color
        )
        output_parent = sub_control

    output_name = name_rule.replace_node_type(
        control_name,
        "output"
    )
    output = pm.createNode(
        "transform",
        name=output_name,
        parent=output_parent
    )

    top_group = groups["zero"]

    if target is not None:
        top_group.setMatrix(
            target.getMatrix(worldSpace=True),
            worldSpace=True
        )

    if parent is not None:
        top_group.setParent(
            parent
        )

    if add_to_set:
        if control_set is None:
            control_set = "ctrl_set"

        if pm.objExists(control_set):
            control_set = pm.PyNode(control_set)
        else:
            control_set = pm.sets(
                name=control_set,
                empty=True
            )

        pm.sets(
            control,
            edit=True,
            forceElement=control_set
        )

    return {
        "control": control,
        "sub_control": sub_control,
        "output": output,
        "top_group": top_group,
        "groups": groups,
    }


__all__ = [
    "create_control",
]
