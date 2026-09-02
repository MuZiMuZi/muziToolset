# coding=utf-8
u"""
Ctrl Base
=========

MuziTools 所有绑定系统共用的 Controller 基础模块。

本模块只维护：

    1. Ctrl Creation
    2. Controller Hierarchy Naming
    3. Follow
    4. Space Switch
    5. Rebuild Cache

Rig Naming 统一交给 systems.rig_base.RigBase。
Scene / Attr / Connection / Hierarchy / Snap 等通用能力统一复用 Core。
内部 Controller Name 默认来自统一 Naming API，不重复检查名称格式。
只有在 Build / Rebuild / Restore 面对 Maya 场景状态时检查节点、属性和连接是否存在。

标准控制器层级：

    zero
      └── driven
          └── space
              └── connect
                  └── offset
                      └── ctrl
                          ├── sub ctrl（可选）
                          └── output
"""

from __future__ import print_function

import json

import maya.cmds as cmds

from ..core import attr_utils
from ..core import connection_utils
from ..core import control_shape_utils
from ..core import constraint_utils
from ..core import hierarchy_utils
from ..core import rename_utils
from ..core import scene_utils
from ..core import snap_utils
from .rig_base import RigBase


# =============================================================================
# Constant
# =============================================================================

axis_rotation = {
    "X+": (90.0, 0.0, 0.0),
    "X-": (-90.0, 0.0, 0.0),
    "Y+": (0.0, 90.0, 0.0),
    "Y-": (0.0, -90.0, 0.0),
    "Z+": (0.0, 0.0, 90.0),
    "Z-": (0.0, 0.0, -90.0),
}


# =============================================================================
# Naming
# =============================================================================

def _get_rig_name(node_name):
    u"""把内部标准节点名称转换成 RigBase Name Object。"""
    short_name = rename_utils.get_short_name(
        node_name
    )
    return RigBase(
        name=short_name
    )


def _get_ctrl_part(ctrl_rig):
    u"""返回包含 Controller 原 function 的派生节点 part。"""
    return "{}_{}".format(
        ctrl_rig.part,
        ctrl_rig.function
    )


def get_ctrl_hierarchy_names(
        name,
        create_sub_ctrl=False
):
    u"""

        根据标准 Controller Name 返回 CtrlBase 会创建的确定性层级名称。

        其它 Module 如果需要在 Build 前检查 Controller 层级残留，应调用本方法，
        不要再次手写 ctrl_ -> zero_ / driven_ / space_ 等字符串替换。

        Args:
            name (str):
                创建或查询时使用的节点名称。
            create_sub_ctrl (bool):
                当前 Rig 操作或驱动使用的动画 Controller Transform。

        Returns:
            object:
                当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    ctrl_rig = _get_rig_name(
        name
    )

    names = {
        "zero": ctrl_rig.create_name(type="zero"),
        "driven": ctrl_rig.create_name(type="driven"),
        "space": ctrl_rig.create_name(type="space"),
        "connect": ctrl_rig.create_name(type="connect"),
        "offset": ctrl_rig.create_name(type="offset"),
        "ctrl": ctrl_rig.name,
        "output": ctrl_rig.create_name(type="output"),
        "sub_ctrl": None,
    }

    if create_sub_ctrl:
        names["sub_ctrl"] = ctrl_rig.create_name(
            type="ctrl",
            part=_get_ctrl_part(ctrl_rig),
            function="sub"
        )

    return names


# =============================================================================
# Ctrl Creation
# =============================================================================

def _apply_shape_transform(ctrl_node, radius, axis, rotate_x=0.0):
    u"""设置 Controller Shape 的大小和轴向。"""
    control_shape_utils.scale_shape(
        ctrl_node,
        float(radius)
    )

    rotation_value = axis_rotation[axis]
    control_shape_utils.rotate_shape(
        ctrl_node,
        rotate_x=rotation_value[0] + float(rotate_x),
        rotate_y=rotation_value[1],
        rotate_z=rotation_value[2]
    )


def create_ctrl(
        name,
        shape="circle",
        radius=1.0,
        color=17,
        axis="Y+",
        target_node=None,
        parent_node=None,
        rotate_x=0.0,
        create_sub_ctrl=False,
        sub_color=None,
        lock_attr_list=None,
        add_to_set=True,
        ctrl_set="ctrl_set"
):
    u"""

        创建 MuziTools 标准 Controller。

        Args:
            name (str):
                创建或查询时使用的节点名称。
            shape (str):
                Controller、Curve 或 Geometry 的 Shape 节点 / Shape 名称。
            radius (float):
                创建节点或控制器使用的半径值。
            color (int):
                Viewport Override 使用的 Index Color 或 RGB Color。
            axis (str):
                操作使用的轴向标记。
            target_node (str):
                接收数据、匹配结果或操作结果的 Target Maya 节点。
            parent_node (str):
                Child 最终需要挂接到的 Parent DAG 节点名称。
            rotate_x (float):
                Controller Shape / Transform 绕 X 轴应用的旋转角度。
            create_sub_ctrl (bool):
                当前 Rig 操作或驱动使用的动画 Controller Transform。
            sub_color (object):
                当前方法执行 Maya / Rig 操作时使用的 `sub_color` 数据。
            lock_attr_list (list):
                当前方法需要保持顺序批量处理的数据列表。
            add_to_set (bool):
                是否把创建后的 Controller 加入指定 Controller Set。
            ctrl_set (str):
                当前 Maya / Rig 操作使用的 `ctrl_set` 名称或标记。

        Returns:
            dict:
                包含本次构建、查询或处理结果的结构化字典。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # -------------------------------------------------------------------------
    # Step 01：检查创建参数与 Scene 输入
    # -------------------------------------------------------------------------
    if float(radius) <= 0.0:
        raise ValueError(
            u"Controller Radius 必须大于 0。"
        )

    if axis not in axis_rotation:
        raise ValueError(
            u"不支持的 Controller Axis：{}".format(axis)
        )

    color = int(color)

    if color < 0 or color > 31:
        raise ValueError(
            u"Maya Index Color 必须在 0 - 31 之间。"
        )

    if target_node is not None:
        scene_utils.validate_node(
            target_node,
            u"Target Node"
        )

    if parent_node is not None:
        scene_utils.validate_node(
            parent_node,
            u"Parent Node"
        )

    # -------------------------------------------------------------------------
    # Step 02：由 CtrlBase 自己的 Naming API 准备固定层级名称
    # -------------------------------------------------------------------------
    hierarchy_names = get_ctrl_hierarchy_names(
        name,
        create_sub_ctrl=create_sub_ctrl
    )

    ctrl_name = hierarchy_names["ctrl"]
    zero_grp_name = hierarchy_names["zero"]
    driven_grp_name = hierarchy_names["driven"]
    space_grp_name = hierarchy_names["space"]
    connect_grp_name = hierarchy_names["connect"]
    offset_grp_name = hierarchy_names["offset"]
    output_name = hierarchy_names["output"]
    sub_ctrl_name = hierarchy_names["sub_ctrl"]

    create_name_list = [
        zero_grp_name,
        driven_grp_name,
        space_grp_name,
        connect_grp_name,
        offset_grp_name,
        ctrl_name,
        output_name,
    ]

    if sub_ctrl_name is not None:
        create_name_list.append(
            sub_ctrl_name
        )

    scene_utils.ensure_nodes_available(
        create_name_list,
        label=u"Controller Build Node"
    )

    # -------------------------------------------------------------------------
    # Step 03：创建固定 Controller Hierarchy
    # -------------------------------------------------------------------------
    zero_grp = scene_utils.create_node(
        "transform",
        zero_grp_name
    )
    driven_grp = scene_utils.create_node(
        "transform",
        driven_grp_name,
        parent=zero_grp
    )
    space_grp = scene_utils.create_node(
        "transform",
        space_grp_name,
        parent=driven_grp
    )
    connect_grp = scene_utils.create_node(
        "transform",
        connect_grp_name,
        parent=space_grp
    )
    offset_grp = scene_utils.create_node(
        "transform",
        offset_grp_name,
        parent=connect_grp
    )

    # -------------------------------------------------------------------------
    # Step 04：创建主 Ctrl
    # -------------------------------------------------------------------------
    shape_data = control_shape_utils.load_shape_data(
        shape
    )

    ctrl_node = scene_utils.create_node(
        "transform",
        ctrl_name,
        parent=offset_grp
    )
    control_shape_utils.apply_shape_data(
        ctrl_node,
        shape_data
    )
    _apply_shape_transform(
        ctrl_node,
        radius=radius,
        axis=axis,
        rotate_x=rotate_x
    )
    control_shape_utils.set_shape_color(
        ctrl_node,
        color
    )

    # -------------------------------------------------------------------------
    # Step 05：创建可选 Sub Ctrl
    # -------------------------------------------------------------------------
    sub_ctrl_node = None
    output_parent_node = ctrl_node

    if create_sub_ctrl:
        sub_ctrl_node = scene_utils.create_node(
            "transform",
            sub_ctrl_name,
            parent=ctrl_node
        )
        control_shape_utils.apply_shape_data(
            sub_ctrl_node,
            shape_data
        )
        _apply_shape_transform(
            sub_ctrl_node,
            radius=float(radius) * 0.7,
            axis=axis,
            rotate_x=rotate_x
        )

        if sub_color is None:
            sub_color = min(
                color + 1,
                31
            )

        control_shape_utils.set_shape_color(
            sub_ctrl_node,
            int(sub_color)
        )

        ctrl_attr = attr_utils.Attr(
            ctrl_node
        )
        sub_ctrl_vis_plug = ctrl_attr.add_attr(
            "subCtrlVis",
            attr_type="bool",
            lock=False,
            hide=True,
            default_value=0,
            keyable=False,
            channel_box=True
        )

        connection_utils.connect_plugs(
            sub_ctrl_vis_plug,
            sub_ctrl_node + ".visibility",
            force=True
        )
        output_parent_node = sub_ctrl_node

    # -------------------------------------------------------------------------
    # Step 06：创建最终 Output
    # -------------------------------------------------------------------------
    output_node = scene_utils.create_node(
        "transform",
        output_name,
        parent=output_parent_node
    )

    # -------------------------------------------------------------------------
    # Step 07：对齐 Target
    # -------------------------------------------------------------------------
    if target_node is not None:
        snap_utils.snap_to_average(
            [target_node],
            zero_grp,
            include_rotation=True
        )

    # -------------------------------------------------------------------------
    # Step 08：整理到 Module Ctrl Group
    # -------------------------------------------------------------------------
    if parent_node is not None:
        zero_grp = hierarchy_utils.parent(
            zero_grp,
            parent_node
        )

    # -------------------------------------------------------------------------
    # Step 09：锁定通道并加入 Animation Set
    # -------------------------------------------------------------------------
    if lock_attr_list:
        ctrl_attr = attr_utils.Attr(
            ctrl_node
        )
        ctrl_attr.set_attrs_state(
            lock_attr_list,
            lock=True,
            keyable=False,
            channel_box=False
        )

        if sub_ctrl_node is not None:
            sub_ctrl_attr = attr_utils.Attr(
                sub_ctrl_node
            )
            sub_ctrl_attr.set_attrs_state(
                lock_attr_list,
                lock=True,
                keyable=False,
                channel_box=False
            )

    if add_to_set:
        scene_utils.ensure_object_set(
            ctrl_set,
            objects=ctrl_node
        )

    grp_dict = {
        "zero": zero_grp,
        "driven": driven_grp,
        "space": space_grp,
        "connect": connect_grp,
        "offset": offset_grp,
    }

    build_node_list = [
        zero_grp,
        driven_grp,
        space_grp,
        connect_grp,
        offset_grp,
        ctrl_node,
        output_node,
    ]

    if sub_ctrl_node is not None:
        build_node_list.append(
            sub_ctrl_node
        )

    return {
        "ctrl_node": ctrl_node,
        "sub_ctrl_node": sub_ctrl_node,
        "output_node": output_node,
        "top_grp": zero_grp,
        "grp_dict": grp_dict,
        "build_node_list": build_node_list,
    }


@scene_utils.undo_chunk
def create_fk_ctrl(
        target_list,
        ctrl_name_list,
        shape="circle",
        radius=1.0,
        color=17,
        axis="Y+",
        parent_node=None,
        constrain=True,
        add_to_set=True,
        ctrl_set="ctrl_set"
):
    u"""

        根据 Target List 和明确的 Ctrl Name List 创建 FK Controller Chain。

        Args:
            target_list (list):
                当前方法需要保持顺序批量处理的数据列表。
            ctrl_name_list (list):
                当前方法需要保持顺序批量处理的数据列表。
            shape (str):
                Controller、Curve 或 Geometry 的 Shape 节点 / Shape 名称。
            radius (float):
                创建节点或控制器使用的半径值。
            color (int):
                Viewport Override 使用的 Index Color 或 RGB Color。
            axis (str):
                操作使用的轴向标记。
            parent_node (str):
                Child 最终需要挂接到的 Parent DAG 节点名称。
            constrain (bool):
                创建 Controller 后是否建立 Controller / Output 到 Target 的约束关系。
            add_to_set (bool):
                是否把创建后的 Controller 加入指定 Controller Set。
            ctrl_set (str):
                当前 Maya / Rig 操作使用的 `ctrl_set` 名称或标记。

        Returns:
            object | list:
                按当前 API 约定顺序返回的结果列表。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not target_list:
        return []

    if not ctrl_name_list:
        raise ValueError(
            u"FK Ctrl Name List 不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if len(target_list) != len(ctrl_name_list):
        raise ValueError(
            u"FK Target List 和 Ctrl Name List 数量必须一致。"
        )

    ctrl_dict_list = []
    previous_ctrl_node = None
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    target_index = 0

    while target_index < len(target_list):
        target_node = target_list[target_index]
        ctrl_name = ctrl_name_list[target_index]

        scene_utils.validate_node(
            target_node,
            u"FK Target"
        )

        current_parent_node = parent_node

        if previous_ctrl_node is not None:
            current_parent_node = previous_ctrl_node

        ctrl_dict = create_ctrl(
            name=ctrl_name,
            shape=shape,
            radius=radius,
            color=color,
            axis=axis,
            target_node=target_node,
            parent_node=current_parent_node,
            create_sub_ctrl=False,
            add_to_set=add_to_set,
            ctrl_set=ctrl_set
        )

        ctrl_node = ctrl_dict["ctrl_node"]

        if constrain:
            constraint_utils.create_constraint(
                driver_objects=ctrl_node,
                driven_object=target_node,
                constraint_type="parentConstraint",
                maintain_offset=False
            )

        ctrl_dict_list.append(
            ctrl_dict
        )
        previous_ctrl_node = ctrl_node
        target_index += 1

    ctrl_list = []

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for ctrl_dict in ctrl_dict_list:
        ctrl_list.append(
            ctrl_dict["ctrl_node"]
        )

    if ctrl_list:
        cmds.select(
            ctrl_list,
            replace=True
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return ctrl_dict_list


# =============================================================================
# Follow
# =============================================================================

def create_follow(
        driver_node,
        ctrl_dict,
        weight=1.0,
        attr_name="follow",
        maintain_offset=True
):
    u"""

        给标准 Controller 创建 0 - 1 Follow。

        Args:
            driver_node (object):
                当前方法执行 Maya / Rig 操作时使用的 `driver_node` 数据。
            ctrl_dict (dict):
                当前方法使用的结构化配置 / 映射数据。
            weight (float):
                当前计算、混合或变形使用的权重值。
            attr_name (str):
                `attr_name` 对应的 Maya 节点或资源名称。
            maintain_offset (bool):
                是否在建立约束或矩阵关系时保持当前偏移。

        Returns:
            dict:
                包含本次构建、查询或处理结果的结构化字典。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    scene_utils.validate_node(
        driver_node,
        u"Follow Driver"
    )

    ctrl_node = ctrl_dict["ctrl_node"]
    grp_dict = ctrl_dict["grp_dict"]
    zero_grp = grp_dict["zero"]
    driven_grp = grp_dict["driven"]

    scene_utils.validate_node(
        ctrl_node,
        u"Ctrl Node"
    )
    scene_utils.validate_node(
        zero_grp,
        u"Zero Group"
    )
    # -------------------------------------------------------------------------
    # Step 02：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    scene_utils.validate_node(
        driven_grp,
        u"Driven Group"
    )

    weight = max(
        0.0,
        min(1.0, float(weight))
    )
    ctrl_attr = attr_utils.Attr(
        ctrl_node
    )
    follow_plug = ctrl_attr.add_attr(
        attr_name,
        attr_type="double",
        lock=False,
        hide=False,
        default_value=weight,
        min_value=0.0,
        max_value=1.0,
        keyable=True,
        channel_box=True
    )

    ctrl_rig = _get_rig_name(
        ctrl_node
    )
    related_part = _get_ctrl_part(
        ctrl_rig
    )
    constraint_name = ctrl_rig.create_name(
        type="cns",
        part=related_part,
        function=attr_name
    )
    # -------------------------------------------------------------------------
    # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    reverse_name = ctrl_rig.create_name(
        type="reverse",
        part=related_part,
        function=attr_name
    )

    scene_utils.ensure_nodes_available(
        [constraint_name, reverse_name],
        label=u"Follow Build Node"
    )

    constraint_node_list = constraint_utils.create_constraint(
        driver_objects=[
            driver_node,
            zero_grp,
        ],
        driven_object=driven_grp,
        constraint_type="parentConstraint",
        maintain_offset=maintain_offset,
        name=constraint_name
    )

    if not constraint_node_list:
        raise RuntimeError(
            u"Follow Parent Constraint 创建失败：{}".format(
                driven_grp
            )
        )

    constraint_node = constraint_node_list[0]
    weight_alias_list = cmds.parentConstraint(
        constraint_node,
        query=True,
        weightAliasList=True
    )

    if weight_alias_list is None:
        weight_alias_list = []

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if len(weight_alias_list) != 2:
        cmds.delete(
            constraint_node
        )
        raise RuntimeError(
            u"Follow Constraint Target 数量异常：{}".format(
                constraint_node
            )
        )

    driver_weight_plug = "{}.{}".format(
        constraint_node,
        weight_alias_list[0]
    )
    zero_weight_plug = "{}.{}".format(
        constraint_node,
        weight_alias_list[1]
    )

    connection_utils.connect_plugs(
        follow_plug,
        driver_weight_plug,
        force=True
    )

    reverse_node = scene_utils.create_node(
        "reverse",
        reverse_name
    )
    connection_utils.connect_plugs(
        follow_plug,
        reverse_node + ".inputX",
        force=True
    )
    connection_utils.connect_plugs(
        reverse_node + ".outputX",
        zero_weight_plug,
        force=True
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return {
        "driver_node": driver_node,
        "ctrl_node": ctrl_node,
        "zero_grp": zero_grp,
        "driven_grp": driven_grp,
        "constraint_node": constraint_node,
        "reverse_node": reverse_node,
        "follow_plug": follow_plug,
        "build_node_list": [
            constraint_node,
            reverse_node,
        ],
    }


# =============================================================================
# Space Switch
# =============================================================================

def create_space_switch(
        ctrl_dict,
        space_target_dict,
        attr_name="space",
        default_index=0,
        maintain_offset=True
):
    u"""

        给标准 Controller 创建 Enum Space Switch。

        Args:
            ctrl_dict (dict):
                当前方法使用的结构化配置 / 映射数据。
            space_target_dict (dict):
                当前方法使用的结构化配置 / 映射数据。
            attr_name (str):
                `attr_name` 对应的 Maya 节点或资源名称。
            default_index (int):
                对应 Maya Array Attribute、Target、Guide 或构建元素的逻辑索引。
            maintain_offset (bool):
                是否在建立约束或矩阵关系时保持当前偏移。

        Returns:
            dict:
                包含本次构建、查询或处理结果的结构化字典。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not space_target_dict:
        raise ValueError(
            u"Space Target Dict 不能为空。"
        )

    if len(space_target_dict) < 2:
        raise ValueError(
            u"Space Switch 至少需要两个 Space Target。"
        )

    ctrl_node = ctrl_dict["ctrl_node"]
    space_grp = ctrl_dict["grp_dict"]["space"]

    scene_utils.validate_node(
        ctrl_node,
        u"Ctrl Node"
    )
    scene_utils.validate_node(
        space_grp,
        u"Space Group"
    )

    space_label_list = []
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    space_target_list = []

    for space_label, target_node in space_target_dict.items():
        scene_utils.validate_node(
            target_node,
            u"Space Target"
        )

        clean_label = str(space_label).replace(
            ":",
            "_"
        )
        space_label_list.append(
            clean_label
        )
        space_target_list.append(
            target_node
        )

    if default_index < 0:
        default_index = 0

    if default_index >= len(space_target_list):
        default_index = len(space_target_list) - 1

    ctrl_attr = attr_utils.Attr(
        ctrl_node
    )

    if ctrl_attr.attr_exists(
            attr_name
    ):
        raise RuntimeError(
            u"Ctrl 上已经存在 Space Attribute：{}.{}".format(
                ctrl_node,
                attr_name
            )
        )

    space_plug = ctrl_attr.add_attr(
        attr_name,
        attr_type="enum",
        lock=False,
        hide=False,
        default_value=int(default_index),
        enum_name=":".join(space_label_list),
        keyable=True,
        channel_box=True
    )

    ctrl_rig = _get_rig_name(
        ctrl_node
    )
    # -------------------------------------------------------------------------
    # Step 03：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    related_part = _get_ctrl_part(
        ctrl_rig
    )
    constraint_name = ctrl_rig.create_name(
        type="cns",
        part=related_part,
        function=attr_name
    )

    scene_utils.ensure_nodes_available(
        constraint_name,
        label=u"Space Constraint"
    )

    constraint_node_list = constraint_utils.create_constraint(
        driver_objects=space_target_list,
        driven_object=space_grp,
        constraint_type="parentConstraint",
        maintain_offset=maintain_offset,
        name=constraint_name
    )

    if not constraint_node_list:
        raise RuntimeError(
            u"Space Parent Constraint 创建失败：{}".format(
                space_grp
            )
        )

    constraint_node = constraint_node_list[0]
    weight_alias_list = cmds.parentConstraint(
        constraint_node,
        query=True,
        weightAliasList=True
    )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if weight_alias_list is None:
        weight_alias_list = []

    if len(weight_alias_list) != len(space_target_list):
        cmds.delete(
            constraint_node
        )
        raise RuntimeError(
            u"Space Constraint Target 数量异常：{}".format(
                constraint_node
            )
        )

    condition_node_list = []
    space_index = 0

    while space_index < len(space_target_list):
        condition_part = "{}_{}".format(
            related_part,
            attr_name
        )
        condition_name = ctrl_rig.create_name(
            type="condition",
            part=condition_part,
            function=str(space_index + 1)
        )

        scene_utils.ensure_nodes_available(
            condition_name,
            label=u"Space Condition"
        )

        condition_node = scene_utils.create_node(
            "condition",
            condition_name
        )

        cmds.setAttr(
            condition_node + ".operation",
            0
        )
        cmds.setAttr(
            condition_node + ".secondTerm",
            space_index
        )
        cmds.setAttr(
            condition_node + ".colorIfTrueR",
            1.0
        )
        cmds.setAttr(
            condition_node + ".colorIfFalseR",
            0.0
        )

        connection_utils.connect_plugs(
            space_plug,
            condition_node + ".firstTerm",
            force=True
        )

        weight_plug = "{}.{}".format(
            constraint_node,
            weight_alias_list[space_index]
        )
        connection_utils.connect_plugs(
            condition_node + ".outColorR",
            weight_plug,
            force=True
        )

        condition_node_list.append(
            condition_node
        )
        space_index += 1

    build_node_list = [
        constraint_node
    ]

    for condition_node in condition_node_list:
        build_node_list.append(
            condition_node
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return {
        "ctrl_node": ctrl_node,
        "space_grp": space_grp,
        "space_plug": space_plug,
        "constraint_node": constraint_node,
        "condition_node_list": condition_node_list,
        "space_label_list": space_label_list,
        "space_target_list": space_target_list,
        "build_node_list": build_node_list,
    }


# =============================================================================
# Rebuild Cache - Query
# =============================================================================

def _get_attr_definition(ctrl_node, attr_name):
    u"""读取一个 User Defined Attribute 的定义和值。"""
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    attr_plug = "{}.{}".format(
        ctrl_node,
        attr_name
    )
    attr_type = cmds.getAttr(
        attr_plug,
        type=True
    )

    # -------------------------------------------------------------------------
    # Step 02：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    attr_data = {
        "name": attr_name,
        "type": attr_type,
        "value": None,
        "keyable": cmds.getAttr(attr_plug, keyable=True),
        "channel_box": cmds.getAttr(attr_plug, channelBox=True),
        "lock": cmds.getAttr(attr_plug, lock=True),
        "min": None,
        "max": None,
        "default": None,
        "enum_name": None,
        "input_plug_list": [],
        "output_plug_list": [],
    }

    if cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            minExists=True
    ):
        min_value_list = cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            minimum=True
        )

        if min_value_list:
            attr_data["min"] = min_value_list[0]

    if cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            maxExists=True
    ):
        max_value_list = cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            maximum=True
        )

        if max_value_list:
            attr_data["max"] = max_value_list[0]

    # -------------------------------------------------------------------------
    # Step 03：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        default_value_list = cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            listDefault=True
        )
    except Exception:
        default_value_list = None

    if default_value_list:
        attr_data["default"] = default_value_list[0]

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if attr_type == "enum":
        enum_name_list = cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            listEnum=True
        )

        if enum_name_list:
            attr_data["enum_name"] = enum_name_list[0]

    if attr_type != "message":
        try:
            attr_data["value"] = cmds.getAttr(
                attr_plug
            )
        except Exception:
            attr_data["value"] = None

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return attr_data


def _get_plug_node(plug_name):
    u"""从 Maya Plug 字符串中取得 Node Name。"""
    return plug_name.split(
        ".",
        1
    )[0]


def _is_owned_connection(connected_plug, owned_node_set):
    u"""判断连接另一端是否属于本次会删除的 Build Result。"""
    if not owned_node_set:
        return False

    connected_node = _get_plug_node(
        connected_plug
    )
    connected_short_name = rename_utils.get_short_name(
        connected_node
    )

    if connected_node in owned_node_set:
        return True

    if connected_short_name in owned_node_set:
        return True

    return False


def _get_external_connection_data(
        ctrl_node,
        attr_data,
        owned_node_set
):
    u"""读取一个自定义 Attribute 的外部输入 / 输出连接。"""
    attr_plug = "{}.{}".format(
        ctrl_node,
        attr_data["name"]
    )

    input_plug_list = connection_utils.get_input_connections(
        attr_plug
    )

    for input_plug in input_plug_list:
        if _is_owned_connection(
                input_plug,
                owned_node_set
        ):
            continue

        attr_data["input_plug_list"].append(
            input_plug
        )

    output_plug_list = connection_utils.get_output_connections(
        attr_plug
    )

    for output_plug in output_plug_list:
        if _is_owned_connection(
                output_plug,
                owned_node_set
        ):
            continue

        attr_data["output_plug_list"].append(
            output_plug
        )

    return attr_data


# =============================================================================
# Rebuild Cache - Save
# =============================================================================

def save_rebuild_cache(
        ctrl_node,
        cache_name=None,
        owned_node_list=None
):
    u"""

        把 Ctrl 自定义属性和外部连接保存到 Maya Network Node。

        Args:
            ctrl_node (object):
                当前方法执行 Maya / Rig 操作时使用的 `ctrl_node` 数据。
            cache_name (str):
                `cache_name` 对应的 Maya 节点或资源名称。
            owned_node_list (list):
                当前方法需要保持顺序批量处理的数据列表。

        Returns:
            object:
                当前 API 完成处理后返回的结果。

    """
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    scene_utils.validate_node(
        ctrl_node,
        u"Ctrl Node"
    )

    if cache_name is None:
        ctrl_rig = _get_rig_name(
            ctrl_node
        )
        cache_part = "{}_{}_rebuild".format(
            ctrl_rig.part,
            ctrl_rig.function
        )
        cache_name = ctrl_rig.create_name(
            type="network",
            part=cache_part,
            function="cache"
        )

    scene_utils.ensure_nodes_available(
        cache_name,
        label=u"Rebuild Cache"
    )

    owned_node_set = set()

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if owned_node_list:
        for owned_node in owned_node_list:
            if not owned_node:
                continue

            owned_node_set.add(
                owned_node
            )

            if cmds.objExists(owned_node):
                owned_node_set.add(
                    rename_utils.get_short_name(
                        owned_node
                    )
                )

    owned_node_set.add(
        ctrl_node
    )
    owned_node_set.add(
        rename_utils.get_short_name(ctrl_node)
    )

    user_attr_list = cmds.listAttr(
        ctrl_node,
        userDefined=True
    )

    if user_attr_list is None:
        user_attr_list = []

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    attr_data_list = []

    for attr_name in user_attr_list:
        attr_data = _get_attr_definition(
            ctrl_node,
            attr_name
        )
        attr_data = _get_external_connection_data(
            ctrl_node,
            attr_data,
            owned_node_set
        )
        attr_data_list.append(
            attr_data
        )

    cache_node = scene_utils.create_node(
        "network",
        cache_name
    )

    cache_attr = attr_utils.Attr(
        cache_node
    )
    # -------------------------------------------------------------------------
    # Step 04：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    cache_attr.set_value(
        "sourceCtrlName",
        rename_utils.get_short_name(ctrl_node),
        attr_type="string",
        lock=False,
        keyable=False,
        channel_box=False
    )

    cache_data = {
        "ctrl_name": rename_utils.get_short_name(ctrl_node),
        "attr_data_list": attr_data_list,
    }
    cache_text = json.dumps(
        cache_data,
        ensure_ascii=False,
        indent=2
    )
    cache_attr.set_value(
        "ctrlData",
        cache_text,
        attr_type="string",
        lock=False,
        keyable=False,
        channel_box=False
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return cache_node


# =============================================================================
# Rebuild Cache - Restore
# =============================================================================

def _create_cached_attr(ctrl_node, attr_data):
    u"""根据 Cache Data 重新创建一个自定义 Attribute。"""
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    attr_name = attr_data["name"]
    attr_type = attr_data["type"]
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    supported_types = [
        "double",
        "float",
        "long",
        "short",
        "byte",
        "bool",
        "enum",
        "string",
        "message",
    ]

    if attr_type not in supported_types:
        cmds.warning(
            u"暂不自动恢复复合 / 特殊自定义属性：{}.{} ({})".format(
                ctrl_node,
                attr_name,
                attr_type
            )
        )
        return None

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    enum_name = attr_data["enum_name"]

    if attr_type == "enum" and not enum_name:
        enum_name = "Item"

    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    ctrl_attr = attr_utils.Attr(
        ctrl_node
    )
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return ctrl_attr.add_attr(
        attr_name,
        attr_type=attr_type,
        lock=False,
        hide=True,
        default_value=attr_data["default"],
        min_value=attr_data["min"],
        max_value=attr_data["max"],
        enum_name=enum_name,
        keyable=False,
        channel_box=False
    )


def _restore_cached_attr_value(ctrl_node, attr_data):
    u"""恢复 Attribute Value 和 Channel State。"""
    attr_name = attr_data["name"]
    attr_type = attr_data["type"]
    attr_value = attr_data["value"]
    ctrl_attr = attr_utils.Attr(
        ctrl_node
    )

    if attr_type != "message" and attr_value is not None:
        try:
            ctrl_attr.set_value(
                attr_name,
                attr_value,
                attr_type=attr_type
            )
        except Exception as error:
            cmds.warning(
                u"恢复 Attribute Value 失败：{}.{} | {}".format(
                    ctrl_node,
                    attr_name,
                    error
                )
            )

    ctrl_attr.set_attr_state(
        attr_name,
        keyable=bool(attr_data["keyable"]),
        channel_box=bool(attr_data["channel_box"])
    )
    return True


def _restore_cached_connections(ctrl_node, attr_data):
    u"""恢复一个自定义 Attribute 的外部 Input / Output Connection。"""
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    attr_plug = "{}.{}".format(
        ctrl_node,
        attr_data["name"]
    )

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    restored_connection_list = []
    skipped_connection_list = []

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for source_plug in attr_data["input_plug_list"]:
        connection_text = "{} -> {}".format(
            source_plug,
            attr_plug
        )

        if not cmds.objExists(source_plug):
            skipped_connection_list.append(
                connection_text
            )
            continue

        if connection_utils.connect_plugs(
                source_plug,
                attr_plug,
                force=False
        ):
            restored_connection_list.append(
                connection_text
            )
        else:
            skipped_connection_list.append(
                connection_text
            )

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for destination_plug in attr_data["output_plug_list"]:
        connection_text = "{} -> {}".format(
            attr_plug,
            destination_plug
        )

        if not cmds.objExists(destination_plug):
            skipped_connection_list.append(
                connection_text
            )
            continue

        if connection_utils.connect_plugs(
                attr_plug,
                destination_plug,
                force=False
        ):
            restored_connection_list.append(
                connection_text
            )
        else:
            skipped_connection_list.append(
                connection_text
            )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return {
        "restored_connection_list": restored_connection_list,
        "skipped_connection_list": skipped_connection_list,
    }


def restore_rebuild_cache(
        cache_node,
        ctrl_node,
        delete_cache=True
):
    u"""

        把 Rebuild Cache 恢复到新 Ctrl。

        Args:
            cache_node (object):
                当前方法执行 Maya / Rig 操作时使用的 `cache_node` 数据。
            ctrl_node (object):
                当前方法执行 Maya / Rig 操作时使用的 `ctrl_node` 数据。
            delete_cache (bool):
                当前清理 / 重建流程是否执行 `delete_cache` 对应的删除步骤。

        Returns:
            dict:
                包含本次构建、查询或处理结果的结构化字典。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    scene_utils.validate_node(
        cache_node,
        u"Rebuild Cache"
    )
    scene_utils.validate_node(
        ctrl_node,
        u"New Ctrl Node"
    )

    cache_attr = attr_utils.Attr(
        cache_node
    )

    if not cache_attr.attr_exists(
            "ctrlData"
    ):
        raise RuntimeError(
            u"Rebuild Cache 缺少 ctrlData：{}".format(
                cache_node
            )
        )

    # -------------------------------------------------------------------------
    # Step 02：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    cache_text = cache_attr.get_value(
        "ctrlData"
    )

    if not cache_text:
        raise RuntimeError(
            u"Rebuild Cache 没有可恢复数据：{}".format(
                cache_node
            )
        )

    cache_data = json.loads(
        cache_text
    )
    attr_data_list = cache_data.get(
        "attr_data_list",
        []
    )

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    restored_attr_list = []
    restored_connection_list = []
    skipped_connection_list = []

    for attr_data in attr_data_list:
        attr_plug = _create_cached_attr(
            ctrl_node,
            attr_data
        )

        if attr_plug is None:
            continue

        _restore_cached_attr_value(
            ctrl_node,
            attr_data
        )
        restored_attr_list.append(
            attr_plug
        )

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for attr_data in attr_data_list:
        ctrl_attr = attr_utils.Attr(
            ctrl_node
        )

        if not ctrl_attr.attr_exists(
                attr_data["name"]
        ):
            continue

        connection_result = _restore_cached_connections(
            ctrl_node,
            attr_data
        )

        for connection_text in connection_result[
                "restored_connection_list"
        ]:
            restored_connection_list.append(
                connection_text
            )

        for connection_text in connection_result[
                "skipped_connection_list"
        ]:
            skipped_connection_list.append(
                connection_text
            )

    ctrl_attr = attr_utils.Attr(
        ctrl_node
    )

    for attr_data in attr_data_list:
        attr_name = attr_data["name"]

        if not ctrl_attr.attr_exists(
                attr_name
        ):
            continue

        ctrl_attr.set_attr_state(
            attr_name,
            lock=bool(attr_data["lock"])
        )

    if delete_cache:
        cmds.delete(
            cache_node
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return {
        "ctrl_node": ctrl_node,
        "restored_attr_list": restored_attr_list,
        "restored_connection_list": restored_connection_list,
        "skipped_connection_list": skipped_connection_list,
    }


def delete_rebuild_cache(cache_node):
    u"""

        手动删除 Controller Rebuild Cache。

        Args:
            cache_node (object):
                当前方法执行 Maya / Rig 操作时使用的 `cache_node` 数据。

        Returns:
            bool:
                当前操作成功或目标状态满足要求时返回 True，否则返回 False。

    """
    if not cache_node:
        return False

    if not cmds.objExists(cache_node):
        return False

    cmds.delete(
        cache_node
    )
    return True


__all__ = [
    "axis_rotation",
    "get_ctrl_hierarchy_names",
    "create_ctrl",
    "create_fk_ctrl",
    "create_follow",
    "create_space_switch",
    "save_rebuild_cache",
    "restore_rebuild_cache",
    "delete_rebuild_cache",
]
