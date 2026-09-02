# coding=utf-8
u"""
Ctrl Base
=========

MuziTools 所有绑定系统共用的 Controller 基础模块。

本模块当前集中维护四部分能力：

    1. Ctrl Creation
    2. Follow
    3. Space Switch
    4. Rebuild Cache

这里不包含 Jaw / Teeth / Arm / Leg 等具体 Component 的业务逻辑。

标准控制器层级：

    zero
      └── driven
          └── space
              └── connect
                  └── offset
                      └── ctrl
                          ├── sub ctrl（可选）
                          └── output

层级职责：

    zero
        保存控制器初始空间。

    driven
        接收 Follow 和系统自动驱动。

    space
        接收 Space Switch。

    connect
        预留 Component 内部连接。

    offset
        预留绑定师局部 Offset。

    ctrl
        动画师直接操作。

    output
        最终输出 Transform。
        Output 直接 Parent 到最终动画输入节点，不再重复连接 Transform Channel，
        避免旧写法中 Parent + Channel Connection 可能产生的双重变换。

Rebuild Cache：

    Component Rebuild 前，把 Ctrl 上的 User Defined Attribute 和外部连接
    写入临时 Maya network Node。

    新 Ctrl 创建完成以后，再恢复 Attribute / Value / Connection。
    Rebuild 成功后删除 Cache；中途失败则保留 Cache。
"""

from __future__ import print_function

import json

import maya.cmds as cmds

from ..core import connection_utils
from ..core import control_shape_utils
from ..core import constraint_utils
from ..core import hierarchy_utils
from ..core import rename_utils
from ..core import scene_utils


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

def _validate_ctrl_name(ctrl_name):
    u"""
    检查传入的 Controller Name 是否符合 Ctrl Base 的最基础要求。

    Ctrl Base 不负责自动补全、修正或推导控制器名称。
    Controller Name 必须由上层 Component 在 Naming 阶段准备完成。
    """
    if not isinstance(ctrl_name, str):
        raise TypeError(
            u"Ctrl Name 必须是字符串：{}".format(ctrl_name)
        )

    if not ctrl_name:
        raise ValueError(u"Ctrl Name 不能为空。")

    if ctrl_name != ctrl_name.strip():
        raise ValueError(
            u"Ctrl Name 不能包含首尾空格：{}".format(ctrl_name)
        )

    if "|" in ctrl_name:
        raise ValueError(
            u"Ctrl Name 必须是节点名称，不能传入 DAG Path：{}".format(
                ctrl_name
            )
        )

    if ":" in ctrl_name:
        raise ValueError(
            u"Ctrl Name 不应该包含 Namespace：{}".format(ctrl_name)
        )

    if not ctrl_name.startswith("ctrl_"):
        raise ValueError(
            u"Ctrl Name 必须使用 ctrl_ 前缀：{}".format(ctrl_name)
        )

    return True


# =============================================================================
# Ctrl Creation
# =============================================================================

def _validate_create_name_list(node_name_list):
    u"""创建前一次性检查所有确定性节点名称。"""
    exists_node_list = []

    for node_name in node_name_list:
        if not node_name:
            continue

        if cmds.objExists(node_name):
            exists_node_list.append(node_name)

    if exists_node_list:
        raise RuntimeError(
            u"Controller Build Node 已存在，请先执行 Component Rebuild Cleanup：{}".format(
                ", ".join(exists_node_list)
            )
        )

    return True


def _apply_shape_transform(ctrl_node, radius, axis, rotate_x=0.0):
    u"""设置 Controller Shape 的大小和轴向。"""
    control_shape_utils.scale_shape(ctrl_node, float(radius))

    rotation_value = axis_rotation[axis]
    control_shape_utils.rotate_shape(
        ctrl_node,
        rotate_x=rotation_value[0] + float(rotate_x),
        rotate_y=rotation_value[1],
        rotate_z=rotation_value[2]
    )


def _lock_ctrl_attr(ctrl_node, lock_attr_list):
    u"""锁定并隐藏指定 Controller Attribute。"""
    if not lock_attr_list:
        return True

    for attr_name in lock_attr_list:
        attr_plug = "{}.{}".format(ctrl_node, attr_name)

        if not cmds.objExists(attr_plug):
            continue

        cmds.setAttr(
            attr_plug,
            lock=True,
            keyable=False,
            channelBox=False
        )

    return True


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

    制作思路：
        1. Controller Name 由调用方提前准备，Ctrl Base 不再自动修正名称；
        2. zero / driven / space / connect / offset 固定创建；
        3. 调用方只传真正会变化的参数；
        4. 所有名称保持确定性，同名时直接报错；
        5. Output 是最终动画输入节点的 Identity Child；
        6. Component 可以直接把 top_grp Parent 到自己的 ctrl_grp。

    Returns:
        dict:
            ctrl_node
            sub_ctrl_node
            output_node
            top_grp
            grp_dict
            build_node_list
    """
    # -------------------------------------------------------------------------
    # Step 01：检查创建参数
    # -------------------------------------------------------------------------
    _validate_ctrl_name(name)

    if float(radius) <= 0.0:
        raise ValueError(u"Controller Radius 必须大于 0。")

    if axis not in axis_rotation:
        raise ValueError(u"不支持的 Controller Axis：{}".format(axis))

    color = int(color)

    if color < 0 or color > 31:
        raise ValueError(u"Maya Index Color 必须在 0 - 31 之间。")

    if target_node is not None:
        scene_utils.validate_node(target_node, u"Target Node")

    if parent_node is not None:
        scene_utils.validate_node(parent_node, u"Parent Node")

    # -------------------------------------------------------------------------
    # Step 02：准备固定名称
    # -------------------------------------------------------------------------
    ctrl_name = name

    zero_grp_name = ctrl_name.replace("ctrl_", "zero_", 1)
    driven_grp_name = ctrl_name.replace("ctrl_", "driven_", 1)
    space_grp_name = ctrl_name.replace("ctrl_", "space_", 1)
    connect_grp_name = ctrl_name.replace("ctrl_", "connect_", 1)
    offset_grp_name = ctrl_name.replace("ctrl_", "offset_", 1)
    output_name = ctrl_name.replace("ctrl_", "output_", 1)

    sub_ctrl_name = None

    if create_sub_ctrl:
        ctrl_name_base, ctrl_index = ctrl_name.rsplit("_", 1)
        sub_ctrl_name = "{}_sub_{}".format(ctrl_name_base, ctrl_index)

    create_name_list = [
        ctrl_name,
        zero_grp_name,
        driven_grp_name,
        space_grp_name,
        connect_grp_name,
        offset_grp_name,
        output_name,
    ]

    if sub_ctrl_name:
        create_name_list.append(sub_ctrl_name)

    _validate_create_name_list(create_name_list)

    # -------------------------------------------------------------------------
    # Step 03：创建固定 Controller Hierarchy
    # -------------------------------------------------------------------------
    zero_grp = cmds.createNode("transform", name=zero_grp_name)
    driven_grp = cmds.createNode(
        "transform",
        name=driven_grp_name,
        parent=zero_grp
    )
    space_grp = cmds.createNode(
        "transform",
        name=space_grp_name,
        parent=driven_grp
    )
    connect_grp = cmds.createNode(
        "transform",
        name=connect_grp_name,
        parent=space_grp
    )
    offset_grp = cmds.createNode(
        "transform",
        name=offset_grp_name,
        parent=connect_grp
    )

    # -------------------------------------------------------------------------
    # Step 04：创建主 Ctrl
    # -------------------------------------------------------------------------
    shape_data = control_shape_utils.load_shape_data(shape)

    ctrl_node = cmds.createNode(
        "transform",
        name=ctrl_name,
        parent=offset_grp
    )
    control_shape_utils.apply_shape_data(ctrl_node, shape_data)
    _apply_shape_transform(
        ctrl_node,
        radius=radius,
        axis=axis,
        rotate_x=rotate_x
    )
    control_shape_utils.set_shape_color(ctrl_node, color)

    # -------------------------------------------------------------------------
    # Step 05：创建可选 Sub Ctrl
    # -------------------------------------------------------------------------
    sub_ctrl_node = None
    output_parent_node = ctrl_node

    if create_sub_ctrl:
        sub_ctrl_node = cmds.createNode(
            "transform",
            name=sub_ctrl_name,
            parent=ctrl_node
        )
        control_shape_utils.apply_shape_data(sub_ctrl_node, shape_data)
        _apply_shape_transform(
            sub_ctrl_node,
            radius=float(radius) * 0.7,
            axis=axis,
            rotate_x=rotate_x
        )

        if sub_color is None:
            sub_color = min(color + 1, 31)

        control_shape_utils.set_shape_color(
            sub_ctrl_node,
            int(sub_color)
        )

        if not cmds.attributeQuery(
                "subCtrlVis",
                node=ctrl_node,
                exists=True
        ):
            cmds.addAttr(
                ctrl_node,
                longName="subCtrlVis",
                attributeType="bool",
                defaultValue=0
            )
            cmds.setAttr(
                ctrl_node + ".subCtrlVis",
                channelBox=True
            )

        connection_utils.connect_plugs(
            ctrl_node + ".subCtrlVis",
            sub_ctrl_node + ".visibility",
            force=True
        )
        output_parent_node = sub_ctrl_node

    # -------------------------------------------------------------------------
    # Step 06：创建最终 Output
    # -------------------------------------------------------------------------
    output_node = cmds.createNode(
        "transform",
        name=output_name,
        parent=output_parent_node
    )

    # -------------------------------------------------------------------------
    # Step 07：对齐 Target
    # -------------------------------------------------------------------------
    if target_node is not None:
        cmds.matchTransform(
            zero_grp,
            target_node,
            position=True,
            rotation=True
        )

    # -------------------------------------------------------------------------
    # Step 08：整理到 Component Ctrl Group
    # -------------------------------------------------------------------------
    if parent_node is not None:
        zero_grp = hierarchy_utils.parent(zero_grp, parent_node)

    # -------------------------------------------------------------------------
    # Step 09：锁定通道并加入 Animation Set
    # -------------------------------------------------------------------------
    _lock_ctrl_attr(ctrl_node, lock_attr_list)

    if sub_ctrl_node is not None:
        _lock_ctrl_attr(sub_ctrl_node, lock_attr_list)

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
        build_node_list.append(sub_ctrl_node)

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
    根据 Target List 和明确的 Ctrl Name List 创建标准 FK Controller Chain。

    Ctrl Base 不根据 Target 自动推导 Controller Name，也不根据左右侧自动推导颜色。
    名称和颜色属于上层 Component 的 Build Setting。
    """
    if not target_list:
        return []

    if not ctrl_name_list:
        raise ValueError(u"FK Ctrl Name List 不能为空。")

    if len(target_list) != len(ctrl_name_list):
        raise ValueError(
            u"FK Target List 和 Ctrl Name List 数量必须一致。"
        )

    ctrl_dict_list = []
    previous_ctrl_node = None
    target_index = 0

    while target_index < len(target_list):
        target_node = target_list[target_index]
        ctrl_name = ctrl_name_list[target_index]

        scene_utils.validate_node(target_node, u"FK Target")
        _validate_ctrl_name(ctrl_name)

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

        ctrl_dict_list.append(ctrl_dict)
        previous_ctrl_node = ctrl_node
        target_index += 1

    ctrl_list = []

    for ctrl_dict in ctrl_dict_list:
        ctrl_list.append(ctrl_dict["ctrl_node"])

    if ctrl_list:
        cmds.select(ctrl_list, replace=True)

    return ctrl_dict_list


# =============================================================================
# Ctrl Attribute
# =============================================================================

def _ensure_float_attr(
        ctrl_node,
        attr_name,
        default_value,
        min_value=0.0,
        max_value=1.0
):
    u"""创建或复用一个 Keyable Float Attribute。"""
    scene_utils.validate_node(ctrl_node, u"Ctrl Node")

    if cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            exists=True
    ):
        return "{}.{}".format(ctrl_node, attr_name)

    cmds.addAttr(
        ctrl_node,
        longName=attr_name,
        attributeType="double",
        defaultValue=float(default_value),
        minValue=float(min_value),
        maxValue=float(max_value),
        keyable=True
    )

    return "{}.{}".format(ctrl_node, attr_name)


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

    Follow 只作用在 driven_grp：

        zero
          └── driven   <- Follow
              └── space
                  └── ...

    Follow = 1：完全跟随外部 Driver。
    Follow = 0：回到自己的 Zero Space。
    """
    # -------------------------------------------------------------------------
    # Step 01：取得标准 Ctrl / Group
    # -------------------------------------------------------------------------
    scene_utils.validate_node(driver_node, u"Follow Driver")

    ctrl_node = ctrl_dict["ctrl_node"]
    grp_dict = ctrl_dict["grp_dict"]
    zero_grp = grp_dict["zero"]
    driven_grp = grp_dict["driven"]

    scene_utils.validate_node(ctrl_node, u"Ctrl Node")
    scene_utils.validate_node(zero_grp, u"Zero Group")
    scene_utils.validate_node(driven_grp, u"Driven Group")

    # -------------------------------------------------------------------------
    # Step 02：创建 Follow Attribute
    # -------------------------------------------------------------------------
    weight = max(0.0, min(1.0, float(weight)))
    follow_plug = _ensure_float_attr(
        ctrl_node,
        attr_name,
        default_value=weight
    )

    # -------------------------------------------------------------------------
    # Step 03：创建 Constraint 和 Reverse
    # -------------------------------------------------------------------------
    ctrl_name = rename_utils.get_short_name(ctrl_node)
    ctrl_name_base, ctrl_index = ctrl_name.rsplit("_", 1)
    ctrl_name_base = ctrl_name_base.replace("ctrl_", "", 1)

    constraint_name = "cns_{}_{}_{}".format(ctrl_name_base, attr_name, ctrl_index)
    reverse_name = "reverse_{}_{}_{}".format(ctrl_name_base, attr_name, ctrl_index)

    _validate_create_name_list([
        constraint_name,
        reverse_name,
    ])

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
            u"Follow Parent Constraint 创建失败：{}".format(driven_grp)
        )

    constraint_node = constraint_node_list[0]
    weight_alias_list = cmds.parentConstraint(
        constraint_node,
        query=True,
        weightAliasList=True
    )

    if weight_alias_list is None:
        weight_alias_list = []

    if len(weight_alias_list) != 2:
        cmds.delete(constraint_node)
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

    reverse_node = scene_utils.create_node("reverse", reverse_name)
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

    space_target_dict Example：

        {
            "World": "ctrl_md_global_001",
            "Chest": "ctrl_md_chest_001",
            "Head": "ctrl_md_head_001",
        }

    Space Switch 只作用在 space_grp。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查 Target
    # -------------------------------------------------------------------------
    if not space_target_dict:
        raise ValueError(u"Space Target Dict 不能为空。")

    if len(space_target_dict) < 2:
        raise ValueError(u"Space Switch 至少需要两个 Space Target。")

    ctrl_node = ctrl_dict["ctrl_node"]
    space_grp = ctrl_dict["grp_dict"]["space"]

    scene_utils.validate_node(ctrl_node, u"Ctrl Node")
    scene_utils.validate_node(space_grp, u"Space Group")

    space_label_list = []
    space_target_list = []

    for space_label, target_node in space_target_dict.items():
        scene_utils.validate_node(target_node, u"Space Target")

        clean_label = str(space_label).replace(":", "_")
        space_label_list.append(clean_label)
        space_target_list.append(target_node)

    if default_index < 0:
        default_index = 0

    if default_index >= len(space_target_list):
        default_index = len(space_target_list) - 1

    # -------------------------------------------------------------------------
    # Step 02：创建 Enum Attribute
    # -------------------------------------------------------------------------
    if cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            exists=True
    ):
        raise RuntimeError(
            u"Ctrl 上已经存在 Space Attribute：{}.{}".format(
                ctrl_node,
                attr_name
            )
        )

    cmds.addAttr(
        ctrl_node,
        longName=attr_name,
        attributeType="enum",
        enumName=":".join(space_label_list),
        defaultValue=int(default_index),
        keyable=True
    )
    space_plug = "{}.{}".format(ctrl_node, attr_name)

    # -------------------------------------------------------------------------
    # Step 03：创建 Parent Constraint
    # -------------------------------------------------------------------------
    ctrl_name = rename_utils.get_short_name(ctrl_node)
    ctrl_name_base, ctrl_index = ctrl_name.rsplit("_", 1)
    ctrl_name_base = ctrl_name_base.replace("ctrl_", "", 1)
    constraint_name = "cns_{}_{}_{}".format(ctrl_name_base, attr_name, ctrl_index)

    _validate_create_name_list([constraint_name])

    constraint_node_list = constraint_utils.create_constraint(
        driver_objects=space_target_list,
        driven_object=space_grp,
        constraint_type="parentConstraint",
        maintain_offset=maintain_offset,
        name=constraint_name
    )

    if not constraint_node_list:
        raise RuntimeError(
            u"Space Parent Constraint 创建失败：{}".format(space_grp)
        )

    constraint_node = constraint_node_list[0]
    weight_alias_list = cmds.parentConstraint(
        constraint_node,
        query=True,
        weightAliasList=True
    )

    if weight_alias_list is None:
        weight_alias_list = []

    if len(weight_alias_list) != len(space_target_list):
        cmds.delete(constraint_node)
        raise RuntimeError(
            u"Space Constraint Target 数量异常：{}".format(
                constraint_node
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：使用 Condition 控制每个 Space Weight
    # -------------------------------------------------------------------------
    condition_node_list = []
    space_index = 0

    while space_index < len(space_target_list):
        condition_name = "condition_{}_{}_{}_{}".format(
            ctrl_name_base,
            attr_name,
            space_index + 1,
            ctrl_index
        )
        _validate_create_name_list([condition_name])

        condition_node = scene_utils.create_node(
            "condition",
            condition_name
        )

        cmds.setAttr(condition_node + ".operation", 0)
        cmds.setAttr(condition_node + ".secondTerm", space_index)
        cmds.setAttr(condition_node + ".colorIfTrueR", 1.0)
        cmds.setAttr(condition_node + ".colorIfFalseR", 0.0)

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

        condition_node_list.append(condition_node)
        space_index += 1

    build_node_list = [constraint_node]

    for condition_node in condition_node_list:
        build_node_list.append(condition_node)

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
    attr_plug = "{}.{}".format(ctrl_node, attr_name)
    attr_type = cmds.getAttr(attr_plug, type=True)

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
            attr_data["value"] = cmds.getAttr(attr_plug)
        except Exception:
            attr_data["value"] = None

    return attr_data


def _get_plug_node(plug_name):
    u"""从 Maya Plug 字符串中取得 Node Name。"""
    return plug_name.split(".", 1)[0]


def _is_owned_connection(connected_plug, owned_node_set):
    u"""判断连接另一端是否属于本次会删除的 Build Result。"""
    if not owned_node_set:
        return False

    connected_node = _get_plug_node(connected_plug)
    connected_short_name = rename_utils.get_short_name(connected_node)

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

    input_plug_list = cmds.listConnections(
        attr_plug,
        source=True,
        destination=False,
        plugs=True,
        skipConversionNodes=False
    )

    if input_plug_list is None:
        input_plug_list = []

    for input_plug in input_plug_list:
        if _is_owned_connection(input_plug, owned_node_set):
            continue

        attr_data["input_plug_list"].append(input_plug)

    output_plug_list = cmds.listConnections(
        attr_plug,
        source=False,
        destination=True,
        plugs=True,
        skipConversionNodes=False
    )

    if output_plug_list is None:
        output_plug_list = []

    for output_plug in output_plug_list:
        if _is_owned_connection(output_plug, owned_node_set):
            continue

        attr_data["output_plug_list"].append(output_plug)

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

    owned_node_list：
        当前 Component 自己创建、Rebuild 时会被删除的节点。
        与这些节点之间的内部连接不保存。
    """
    scene_utils.validate_node(ctrl_node, u"Ctrl Node")

    if cache_name is None:
        ctrl_name = rename_utils.get_short_name(ctrl_node)
        ctrl_name_base, ctrl_index = ctrl_name.rsplit("_", 1)
        ctrl_name_base = ctrl_name_base.replace("ctrl_", "", 1)
        cache_name = "network_{}_rebuild_cache_{}".format(ctrl_name_base, ctrl_index)

    if cmds.objExists(cache_name):
        raise RuntimeError(u"Rebuild Cache 已存在：{}".format(cache_name))

    owned_node_set = set()

    if owned_node_list:
        for owned_node in owned_node_list:
            if not owned_node:
                continue

            owned_node_set.add(owned_node)

            if cmds.objExists(owned_node):
                owned_node_set.add(
                    rename_utils.get_short_name(owned_node)
                )

    owned_node_set.add(ctrl_node)
    owned_node_set.add(rename_utils.get_short_name(ctrl_node))

    # -------------------------------------------------------------------------
    # Step 01：读取 User Defined Attribute
    # -------------------------------------------------------------------------
    user_attr_list = cmds.listAttr(
        ctrl_node,
        userDefined=True
    )

    if user_attr_list is None:
        user_attr_list = []

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
        attr_data_list.append(attr_data)

    # -------------------------------------------------------------------------
    # Step 02：写入临时 Network Node
    # -------------------------------------------------------------------------
    cache_node = cmds.createNode("network", name=cache_name)

    cmds.addAttr(
        cache_node,
        longName="sourceCtrlName",
        dataType="string"
    )
    cmds.addAttr(
        cache_node,
        longName="ctrlData",
        dataType="string"
    )

    cmds.setAttr(
        cache_node + ".sourceCtrlName",
        rename_utils.get_short_name(ctrl_node),
        type="string"
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

    cmds.setAttr(
        cache_node + ".ctrlData",
        cache_text,
        type="string"
    )

    return cache_node


# =============================================================================
# Rebuild Cache - Restore
# =============================================================================

def _create_cached_attr(ctrl_node, attr_data):
    u"""根据 Cache Data 重新创建一个自定义 Attribute。"""
    attr_name = attr_data["name"]

    if cmds.attributeQuery(
            attr_name,
            node=ctrl_node,
            exists=True
    ):
        return "{}.{}".format(ctrl_node, attr_name)

    attr_type = attr_data["type"]
    numeric_attr_type_list = [
        "double",
        "float",
        "long",
        "short",
        "byte",
        "bool",
    ]
    add_attr_kwargs = {
        "longName": attr_name,
    }

    if attr_type in numeric_attr_type_list:
        add_attr_kwargs["attributeType"] = attr_type

        if attr_data["default"] is not None:
            add_attr_kwargs["defaultValue"] = attr_data["default"]

        if attr_data["min"] is not None:
            add_attr_kwargs["minValue"] = attr_data["min"]

        if attr_data["max"] is not None:
            add_attr_kwargs["maxValue"] = attr_data["max"]

    elif attr_type == "enum":
        add_attr_kwargs["attributeType"] = "enum"
        enum_name = attr_data["enum_name"]

        if not enum_name:
            enum_name = "Item"

        add_attr_kwargs["enumName"] = enum_name

        if attr_data["default"] is not None:
            add_attr_kwargs["defaultValue"] = int(attr_data["default"])

    elif attr_type == "string":
        add_attr_kwargs["dataType"] = "string"

    elif attr_type == "message":
        add_attr_kwargs["attributeType"] = "message"

    else:
        cmds.warning(
            u"暂不自动恢复复合 / 特殊自定义属性：{}.{} ({})".format(
                ctrl_node,
                attr_name,
                attr_type
            )
        )
        return None

    cmds.addAttr(ctrl_node, **add_attr_kwargs)
    return "{}.{}".format(ctrl_node, attr_name)


def _restore_cached_attr_value(attr_plug, attr_data):
    u"""恢复 Attribute Value 和 Channel State。"""
    if attr_plug is None:
        return False

    attr_type = attr_data["type"]
    attr_value = attr_data["value"]

    if attr_type != "message" and attr_value is not None:
        try:
            if attr_type == "string":
                cmds.setAttr(attr_plug, attr_value, type="string")
            else:
                cmds.setAttr(attr_plug, attr_value)
        except Exception as error:
            cmds.warning(
                u"恢复 Attribute Value 失败：{} | {}".format(
                    attr_plug,
                    error
                )
            )

    try:
        cmds.setAttr(
            attr_plug,
            keyable=bool(attr_data["keyable"])
        )

        if not attr_data["keyable"]:
            cmds.setAttr(
                attr_plug,
                channelBox=bool(attr_data["channel_box"])
            )
    except Exception:
        pass

    return True


def _restore_cached_connections(ctrl_node, attr_data):
    u"""恢复一个自定义 Attribute 的外部 Input / Output Connection。"""
    attr_plug = "{}.{}".format(
        ctrl_node,
        attr_data["name"]
    )

    restored_connection_list = []
    skipped_connection_list = []

    # -------------------------------------------------------------------------
    # Input Connection
    # -------------------------------------------------------------------------
    for source_plug in attr_data["input_plug_list"]:
        connection_text = "{} -> {}".format(
            source_plug,
            attr_plug
        )

        if not cmds.objExists(source_plug):
            skipped_connection_list.append(connection_text)
            continue

        if cmds.isConnected(source_plug, attr_plug):
            continue

        current_input_list = cmds.listConnections(
            attr_plug,
            source=True,
            destination=False,
            plugs=True
        )

        if current_input_list:
            skipped_connection_list.append(connection_text)
            continue

        cmds.connectAttr(source_plug, attr_plug, force=False)
        restored_connection_list.append(connection_text)

    # -------------------------------------------------------------------------
    # Output Connection
    # -------------------------------------------------------------------------
    for destination_plug in attr_data["output_plug_list"]:
        connection_text = "{} -> {}".format(
            attr_plug,
            destination_plug
        )

        if not cmds.objExists(destination_plug):
            skipped_connection_list.append(connection_text)
            continue

        if cmds.isConnected(attr_plug, destination_plug):
            continue

        current_input_list = cmds.listConnections(
            destination_plug,
            source=True,
            destination=False,
            plugs=True
        )

        if current_input_list:
            skipped_connection_list.append(connection_text)
            continue

        cmds.connectAttr(attr_plug, destination_plug, force=False)
        restored_connection_list.append(connection_text)

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

    顺序：
        Attribute Definition
            ↓
        Attribute Value
            ↓
        External Connection
            ↓
        Lock State
            ↓
        Delete Cache
    """
    scene_utils.validate_node(cache_node, u"Rebuild Cache")
    scene_utils.validate_node(ctrl_node, u"New Ctrl Node")

    if not cmds.attributeQuery(
            "ctrlData",
            node=cache_node,
            exists=True
    ):
        raise RuntimeError(
            u"Rebuild Cache 缺少 ctrlData：{}".format(cache_node)
        )

    cache_text = cmds.getAttr(cache_node + ".ctrlData")

    if not cache_text:
        raise RuntimeError(
            u"Rebuild Cache 没有可恢复数据：{}".format(cache_node)
        )

    cache_data = json.loads(cache_text)
    attr_data_list = cache_data.get("attr_data_list", [])

    restored_attr_list = []
    restored_connection_list = []
    skipped_connection_list = []

    # -------------------------------------------------------------------------
    # Step 01：恢复 Attribute Definition / Value
    # -------------------------------------------------------------------------
    for attr_data in attr_data_list:
        attr_plug = _create_cached_attr(ctrl_node, attr_data)

        if attr_plug is None:
            continue

        _restore_cached_attr_value(attr_plug, attr_data)
        restored_attr_list.append(attr_plug)

    # -------------------------------------------------------------------------
    # Step 02：恢复 External Connection
    # -------------------------------------------------------------------------
    for attr_data in attr_data_list:
        attr_name = attr_data["name"]

        if not cmds.attributeQuery(
                attr_name,
                node=ctrl_node,
                exists=True
        ):
            continue

        connection_result = _restore_cached_connections(
            ctrl_node,
            attr_data
        )

        for connection_text in connection_result[
                "restored_connection_list"
        ]:
            restored_connection_list.append(connection_text)

        for connection_text in connection_result[
                "skipped_connection_list"
        ]:
            skipped_connection_list.append(connection_text)

    # -------------------------------------------------------------------------
    # Step 03：最后恢复 Lock State
    # -------------------------------------------------------------------------
    for attr_data in attr_data_list:
        attr_plug = "{}.{}".format(
            ctrl_node,
            attr_data["name"]
        )

        if not cmds.objExists(attr_plug):
            continue

        try:
            cmds.setAttr(
                attr_plug,
                lock=bool(attr_data["lock"])
            )
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Step 04：成功后删除 Cache
    # -------------------------------------------------------------------------
    if delete_cache:
        cmds.delete(cache_node)

    return {
        "ctrl_node": ctrl_node,
        "restored_attr_list": restored_attr_list,
        "restored_connection_list": restored_connection_list,
        "skipped_connection_list": skipped_connection_list,
    }


def delete_rebuild_cache(cache_node):
    u"""手动删除 Controller Rebuild Cache。"""
    if not cache_node:
        return False

    if not cmds.objExists(cache_node):
        return False

    cmds.delete(cache_node)
    return True


__all__ = [
    "axis_rotation",
    "create_ctrl",
    "create_fk_ctrl",
    "create_follow",
    "create_space_switch",
    "save_rebuild_cache",
    "restore_rebuild_cache",
    "delete_rebuild_cache",
]
