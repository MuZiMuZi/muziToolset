# coding=utf-8
u"""
Controller Builder
==================

大型绑定工具集的统一 Controller 创建 API。

所有 Body / Face / Rig 专项系统都应该通过本模块创建控制器，
而不是在各自工具里重复实现 Shape、颜色、Zero Group 和 FK 层级逻辑。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import control_shape_utils


axis_rotation = {
    "X+": (90.0, 0.0, 0.0),
    "X-": (-90.0, 0.0, 0.0),
    "Y+": (0.0, 90.0, 0.0),
    "Y-": (0.0, -90.0, 0.0),
    "Z+": (0.0, 0.0, 90.0),
    "Z-": (0.0, 0.0, -90.0),
}


def get_short_name(node):
    u"""
    返回 DAG 节点短名称。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """
    return node.split("|")[-1].replace(":", "_")


def get_control_name_from_target(target):
    u"""
    根据目标节点生成标准 ctrl_ 名称。

    Args:
        target (str):
            接收结果或被处理的目标 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """
    short_name = get_short_name(target)

    if short_name.startswith("jnt_"):
        return short_name.replace("jnt_", "ctrl_", 1)

    if short_name.startswith("bpjnt_"):
        return short_name.replace("bpjnt_", "ctrl_", 1)

    if short_name.startswith("ctrl_"):
        return short_name

    return "ctrl_{}".format(short_name)


def get_side_color(name):
    u"""
    根据标准左右命名返回 Maya Index Color。

    Args:
        name (str):
            创建或查询时使用的节点名称。

    Returns:
        int:
            方法执行后的结果数据。
    """
    lower_name = name.lower()

    left_tokens = [
        "_lf_",
        "_l_",
        "ctrl_lf_",
        "ctrl_l_",
    ]
    right_tokens = [
        "_rt_",
        "_r_",
        "ctrl_rt_",
        "ctrl_r_",
    ]

    for token in left_tokens:
        if token in lower_name or lower_name.startswith(token):
            return 6

    for token in right_tokens:
        if token in lower_name or lower_name.startswith(token):
            return 13

    return 17


def _safe_control_name(name):
    """整理控制器名称，并确保带 ctrl_ 前缀。"""
    clean_name = name.replace("|", "_")
    clean_name = clean_name.replace(":", "_")
    clean_name = clean_name.strip()

    if not clean_name:
        clean_name = "ctrl_new_001"

    if not clean_name.startswith("ctrl_"):
        clean_name = "ctrl_" + clean_name

    return clean_name


def _next_available_name(name):
    """返回场景中未被占用的 Maya 节点名称。"""
    if not cmds.objExists(name):
        return name

    index = 1

    while True:
        candidate = "{}_{:03d}".format(
            name,
            index
        )

        if not cmds.objExists(candidate):
            return candidate

        index += 1


def _replace_control_prefix(name, prefix):
    """把 ctrl_ 前缀替换成指定层级前缀。"""
    if name.startswith("ctrl_"):
        return name.replace(
            "ctrl_",
            prefix + "_",
            1
        )

    return "{}_{}".format(
        prefix,
        name
    )


def _add_to_control_set(control, set_name="ctrl_set"):
    """确保控制器加入动画控制器 Set。"""
    if not cmds.objExists(set_name):
        cmds.sets(
            name=set_name,
            empty=True
        )

    cmds.sets(
        control,
        add=set_name
    )


def _apply_shape_transform(transform, radius, axis, rotate_x=0.0):
    """应用控制器 Shape 大小和朝向。"""
    control_shape_utils.scale_shape(
        transform,
        float(radius)
    )

    rotation_value = axis_rotation.get(
        axis,
        (0.0, 0.0, 0.0)
    )

    final_rotate_x = rotation_value[0] + float(rotate_x)

    control_shape_utils.rotate_shape(
        transform,
        rotate_x=final_rotate_x,
        rotate_y=rotation_value[1],
        rotate_z=rotation_value[2]
    )


def create_controller(
        name,
        shape="circle",
        radius=1.0,
        axis="Y+",
        target=None,
        parent=None,
        color=17,
        rotate_x=0.0,
        create_sub_control=True,
        create_extra_groups=True,
        add_to_set=True,
        control_set="ctrl_set"
):
    u"""
    创建标准绑定控制器。

    标准层级::
        zero
          driven
            space
              connect
                offset
                  ctrl
                    ctrlSub
                    output

    Args:
        name (str):
            创建或查询时使用的节点名称。
        shape (str):
            `shape` 对应的名称、标记或字符串参数。
        radius (float):
            创建节点或控制器使用的半径值。
        axis (str):
            操作使用的轴向标记。
        target (str):
            接收结果或被处理的目标 Maya 节点名称。
        parent (str):
            父级 Maya 节点名称。
        color (int):
            `color` 对应的整数参数。
        rotate_x (float):
            `rotate_x` 对应的数值参数。
        create_sub_control (bool):
            是否启用 `create_sub_control` 对应的处理。
        create_extra_groups (bool):
            是否启用 `create_extra_groups` 对应的处理。
        add_to_set (bool):
            是否启用 `add_to_set` 对应的处理。
        control_set (str):
            `control_set` 对应的名称、标记或字符串参数。

    Returns:
        dict: 控制器、层级和输出节点信息。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    control_name = _safe_control_name(name)
    control_name = _next_available_name(control_name)

    shape_data = control_shape_utils.load_shape_data(shape)

    control = cmds.createNode(
        "transform",
        name=control_name
    )

    control_shape_utils.apply_shape_data(
        control,
        shape_data
    )
    _apply_shape_transform(
        control,
        radius=radius,
        axis=axis,
        rotate_x=rotate_x
    )
    control_shape_utils.set_shape_color(
        control,
        color
    )

    groups = {}
    top_group = control

    if create_extra_groups:
        group_order = [
            "offset",
            "connect",
            "space",
            "driven",
            "zero",
        ]

        current_child = control

        for group_type in group_order:
            group_name = _replace_control_prefix(
                control_name,
                group_type
            )
            group_name = _next_available_name(group_name)

            group = cmds.createNode(
                "transform",
                name=group_name
            )

            cmds.parent(
                current_child,
                group
            )

            groups[group_type] = group
            current_child = group

        top_group = groups["zero"]

    sub_control = None

    if create_sub_control:
        sub_name = control_name + "Sub"
        sub_name = _next_available_name(sub_name)

        sub_control = cmds.createNode(
            "transform",
            name=sub_name
        )

        control_shape_utils.apply_shape_data(
            sub_control,
            shape_data
        )
        _apply_shape_transform(
            sub_control,
            radius=float(radius) * 0.7,
            axis=axis,
            rotate_x=rotate_x
        )

        sub_color = min(
            int(color) + 1,
            31
        )
        control_shape_utils.set_shape_color(
            sub_control,
            sub_color
        )

        cmds.parent(
            sub_control,
            control
        )

        if not cmds.attributeQuery(
                "subCtrlVis",
                node=control,
                exists=True
        ):
            cmds.addAttr(
                control,
                longName="subCtrlVis",
                attributeType="bool",
                defaultValue=0
            )
            cmds.setAttr(
                control + ".subCtrlVis",
                channelBox=True
            )

        cmds.connectAttr(
            control + ".subCtrlVis",
            sub_control + ".visibility",
            force=True
        )

    output_name = _replace_control_prefix(
        control_name,
        "output"
    )
    output_name = _next_available_name(output_name)

    output = cmds.createNode(
        "transform",
        name=output_name,
        parent=control
    )

    output_driver = control

    if sub_control is not None:
        output_driver = sub_control

    connection_attrs = [
        "translate",
        "rotate",
        "scale",
        "rotateOrder",
    ]

    for attr in connection_attrs:
        cmds.connectAttr(
            "{}.{}".format(
                output_driver,
                attr
            ),
            "{}.{}".format(
                output,
                attr
            ),
            force=True
        )

    if target is not None:
        if not cmds.objExists(target):
            raise RuntimeError(
                u"吸附目标不存在：{}".format(target)
            )

        cmds.matchTransform(
            top_group,
            target,
            position=True,
            rotation=True
        )

    if parent is not None:
        if not cmds.objExists(parent):
            raise RuntimeError(
                u"父节点不存在：{}".format(parent)
            )

        cmds.parent(
            top_group,
            parent
        )

    if add_to_set:
        _add_to_control_set(
            control,
            set_name=control_set
        )

    result = {
        "control": control,
        "sub_control": sub_control,
        "output": output,
        "top_group": top_group,
        "groups": groups,
    }

    return result


def create_fk_controls(
        targets,
        shape="circle",
        radius=1.0,
        axis="Y+",
        constrain=True,
        create_extra_groups=True,
        add_to_set=True
):
    u"""
    根据 targets 顺序创建标准 FK Controller Chain。

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
        create_extra_groups (bool):
            是否启用 `create_extra_groups` 对应的处理。
        add_to_set (bool):
            是否启用 `add_to_set` 对应的处理。

    Returns:
        object | list:
            方法执行后的结果数据。
    """
    if not targets:
        return []

    controls = []
    previous_control = None

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziCreateFkControls"
    )

    try:
        for target in targets:
            if not cmds.objExists(target):
                cmds.warning(
                    u"目标不存在，跳过：{}".format(target)
                )
                continue

            control_name = get_control_name_from_target(target)
            color = get_side_color(control_name)

            result = create_controller(
                name=control_name,
                shape=shape,
                radius=radius,
                axis=axis,
                target=target,
                color=color,
                create_sub_control=False,
                create_extra_groups=create_extra_groups,
                add_to_set=add_to_set
            )

            control = result["control"]
            top_group = result["top_group"]

            if previous_control is not None:
                cmds.parent(
                    top_group,
                    previous_control
                )

            if constrain:
                cmds.parentConstraint(
                    control,
                    target,
                    maintainOffset=False
                )

            controls.append(control)
            previous_control = control

    finally:
        cmds.undoInfo(closeChunk=True)

    if controls:
        cmds.select(
            controls,
            replace=True
        )

    return controls


__all__ = [
    "axis_rotation",
    "get_short_name",
    "get_control_name_from_target",
    "get_side_color",
    "create_controller",
    "create_fk_controls",
]
