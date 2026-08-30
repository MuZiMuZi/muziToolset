# coding=utf-8
u"""
Controller Builder
==================

大型绑定工具集的统一 Controller 创建 API。

所有 Body / Face / Rig 专项系统都应该通过本模块创建控制器，
而不是在各自工具里重复实现 Shape、颜色、Zero Group 和 FK 层级逻辑。

重要边界：
    - DAG Short Name 统一复用 core.rename_utils；
    - Object Set 统一复用 core.scene_utils；
    - DAG Parent 统一复用 core.hierarchy_utils；
    - Controller Shape 统一复用 core.control_shape_utils；
    - 本模块只保留完整 Controller Workflow。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import control_shape_utils
from ...core import hierarchy_utils
from ...core import rename_utils
from ...core import scene_utils


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
    返回 Controller Workflow 使用的节点短名称。

    DAG Short Name 查询统一复用 rename_utils；Controller 名称不保留 Namespace，
    因此这里只额外把 ``:`` 转换成 ``_``。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """
    # 使用 Core 统一提取 DAG Short Name，避免本模块维护第二套 Long Path 解析。
    short_name = rename_utils.get_short_name(
        node
    )

    return short_name.replace(
        ":",
        "_"
    )


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
    # 先取得稳定的目标节点短名称，再根据来源类型替换 Controller 前缀。
    short_name = get_short_name(
        target
    )

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
    # 使用 Scene Core 创建或复用 Object Set，并把当前 Controller 加入其中。
    scene_utils.ensure_object_set(
        set_name,
        objects=control
    )


def _apply_shape_transform(transform, radius, axis, rotate_x=0.0):
    """应用控制器 Shape 大小和朝向。"""
    # 使用统一 Controller Shape API 设置控制器视觉大小。
    control_shape_utils.scale_shape(
        transform,
        float(radius)
    )

    rotation_value = axis_rotation.get(
        axis,
        (0.0, 0.0, 0.0)
    )

    final_rotate_x = rotation_value[0] + float(rotate_x)

    # 使用统一 Controller Shape API 设置轴向和额外 X 旋转。
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
            Controller、Curve 或 Geometry 的 Shape 节点 / Shape 名称。
        radius (float):
            创建节点或控制器使用的半径值。
        axis (str):
            操作使用的轴向标记。
        target (str):
            接收结果或被处理的目标 Maya 节点名称。
        parent (str):
            父级 Maya 节点名称。
        color (int):
            Viewport Override 使用的 Index Color 或 RGB Color。
        rotate_x (float):
            Controller Shape / Transform 绕 X 轴应用的旋转角度。
        create_sub_control (bool):
            当前 Rig 操作或驱动使用的动画 Controller Transform。
        create_extra_groups (bool):
            是否创建 Zero、Driven、Space、Connect、Offset 等标准 Controller Extra Groups。
        add_to_set (bool):
            是否把创建后的 Controller 加入指定 Controller Set。
        control_set (str):
            创建后的 Controller 需要加入的 Maya Set 名称。

    Returns:
        dict: 控制器、层级和输出节点信息。
    """
    # 整理输入名称并确保本次创建不会占用已经存在的节点名称。
    control_name = _safe_control_name(name)
    control_name = _next_available_name(control_name)

    # 从统一 Shape Library 读取需要创建的 Controller Shape 数据。
    shape_data = control_shape_utils.load_shape_data(
        shape
    )

    control = cmds.createNode(
        "transform",
        name=control_name
    )

    # 把 Shape Library 数据应用到新建 Controller Transform。
    control_shape_utils.apply_shape_data(
        control,
        shape_data
    )

    # 设置 Controller Shape 的半径和轴向，不修改 Transform 通道值。
    _apply_shape_transform(
        control,
        radius=radius,
        axis=axis,
        rotate_x=rotate_x
    )

    # 使用统一 Shape API 设置 Controller Viewport Color。
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

        # 从 Controller 向外逐层创建标准 Extra Group Hierarchy。
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

            # 使用统一 Hierarchy API 建立当前 Child 和新 Group 的父子关系。
            hierarchy_utils.Hierarchy.parent(
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

        # 给 Sub Controller 应用与主控制器相同的 Shape 数据。
        control_shape_utils.apply_shape_data(
            sub_control,
            shape_data
        )

        # Sub Controller 使用主控制器 70% 的 Shape 半径并保持相同轴向。
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

        # 使用相邻颜色区分主 Controller 和 Sub Controller。
        control_shape_utils.set_shape_color(
            sub_control,
            sub_color
        )

        # 把 Sub Controller 放在主 Controller 下形成二级动画控制关系。
        hierarchy_utils.Hierarchy.parent(
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

    # 根据主 Controller 名称生成 Output Transform 名称。
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

    # 把最终动画驱动节点的 Transform 通道转发到 Output Transform。
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
        # 使用 Scene Core 验证吸附目标，避免静默操作不存在的节点。
        scene_utils.validate_node(
            target
        )

        cmds.matchTransform(
            top_group,
            target,
            position=True,
            rotation=True
        )

    if parent is not None:
        # 使用 Scene Core 验证指定 Parent，再整理整个 Controller 顶层组。
        scene_utils.validate_node(
            parent
        )

        hierarchy_utils.Hierarchy.parent(
            top_group,
            parent
        )

    if add_to_set:
        # 把主 Controller 加入统一动画 Controller Set。
        _add_to_control_set(
            control,
            set_name=control_set
        )

    return {
        "control": control,
        "sub_control": sub_control,
        "output": output,
        "top_group": top_group,
        "groups": groups,
    }


@scene_utils.undo_chunk
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

    整个创建流程通过 scene_utils.undo_chunk 合并成一次 Maya Undo。

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
        create_extra_groups (bool):
            是否创建 Zero、Driven、Space、Connect、Offset 等标准 Controller Extra Groups。
        add_to_set (bool):
            是否把创建后的 Controller 加入指定 Controller Set。

    Returns:
        object | list:
            方法执行后的结果数据。
    """
    if not targets:
        return []

    controls = []
    previous_control = None

    # 按输入顺序逐个创建 Controller，输入顺序同时决定最终 FK Parent 顺序。
    for target in targets:
        try:
            # 使用 Scene Core 验证当前 FK Target 是否仍然存在。
            scene_utils.validate_node(
                target
            )
        except RuntimeError:
            cmds.warning(
                u"目标不存在，跳过：{}".format(target)
            )
            continue

        # 根据 Target 名称生成对应 Controller 名称。
        control_name = get_control_name_from_target(
            target
        )

        # 根据 Controller Side Token 决定默认 Viewport Color。
        color = get_side_color(
            control_name
        )

        # 使用统一 Controller Builder 创建当前 FK Controller 和标准层级。
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
            # 把当前 Controller 顶层组挂到上一个 Controller，形成 FK Chain。
            hierarchy_utils.Hierarchy.parent(
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
