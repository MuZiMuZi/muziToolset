# coding=utf-8
u"""
Snap Utils
==========

Maya 对象 / 组件快速吸附底层模块。

模块职责
--------
本模块只负责“根据一个或多个参考项计算位置 / 旋转，并把结果应用到目标对象”这一类
通用 Snap 能力。它不负责读取 Maya UI 选择顺序，也不创建任何 PySide / cmds UI。

公开方法
--------
is_component(item)
    判断给定 Maya 选择项是否属于 Vertex / Edge / Face / CV 等常见组件。

get_item_world_position(item)
    获取对象或组件的世界空间位置。

get_item_world_rotation(item)
    获取 Transform / Joint 的世界旋转；组件没有稳定的 Transform Rotation，因此返回 None。

snap_to_average(reference_items, target_item, include_rotation=True)
    把目标对象吸附到多个参考项的平均位置，并在条件允许时应用平均旋转。

设计原则
--------
- Core 不读取“最后选择的是目标”这类 UI 语义；这部分由 tools/basic/snap_tool.py 决定。
- Component 可以提供位置，但通常不能直接作为 Rotation 参考。
- DAG Parent 查询复用 hierarchy_utils，不在本模块重新包装 listRelatives。
- Point / Vector 数学统一复用 math_utils，不在 Snap 模块维护第二套数学实现或兼容别名。
- 复杂 Orientation Blend 应进入 Matrix / Rig System，而不是继续扩张 Snap Utils。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import hierarchy_utils
from . import math_utils
from . import transform_utils


# =============================================================================
# Component Query
# =============================================================================

def is_component(item):
    u"""
    判断 Maya 选择项是否为常见组件。

    Args:
        item (str):
            Maya Node 或 Component 字符串。

    Returns:
        bool:
        输入是 Vertex、Edge、Face、CV 等常见组件时返回 True。
    """
    if not item:
        return False

    if "." not in item:
        return False

    component_tokens = [
        ".vtx[",
        ".e[",
        ".f[",
        ".cv[",
        ".ep[",
        ".pt[",
        ".map[",
    ]

    for token in component_tokens:
        if token in item:
            return True

    return False


# =============================================================================
# World Space Query
# =============================================================================

def get_item_world_position(item):
    u"""
    返回对象、Locator 可视点或组件的世界空间位置。

    Locator Transform 允许 Shape.localPosition 不为零；此时可视十字中心并不等于
    Transform 原点，所以优先读取 Locator Shape.worldPosition[0]。普通 Transform、
    Joint 和 Component 仍使用 ``cmds.xform(..., worldSpace=True)``。

    Args:
        item (str):
            需要查询的 Maya Transform、Joint 或 Component。

    Returns:
        list | None:
        有效时返回 [x, y, z]；无法查询位置时返回 None。
    """
    position = None

    # -------------------------------------------------------------------------
    # Step 01：Locator 的可视定位点来自 Shape.worldPosition
    # -------------------------------------------------------------------------
    if not is_component(item):
        locator_shapes = []

        try:
            node_type = cmds.nodeType(
                item
            )
        except Exception:
            node_type = None

        if node_type == "locator":
            locator_shapes = [
                item
            ]
        elif node_type in [
                "transform",
                "joint",
        ]:
            locator_shapes = cmds.listRelatives(
                item,
                shapes=True,
                noIntermediate=True,
                fullPath=True,
                type="locator"
            ) or []

        if locator_shapes:
            try:
                world_position = cmds.getAttr(
                    locator_shapes[0] + ".worldPosition[0]"
                )
            except Exception:
                world_position = None

            if world_position:
                position = world_position[0]

    # -------------------------------------------------------------------------
    # Step 02：普通 Transform / Joint / Component 继续读取世界平移
    # -------------------------------------------------------------------------
    if position is None:
        try:
            position = cmds.xform(
                item,
                query=True,
                worldSpace=True,
                translation=True
            )
        except Exception:
            position = None

    if not position:
        return None

    if len(position) < 3:
        return None

    return [
        float(position[0]),
        float(position[1]),
        float(position[2]),
    ]


def get_item_world_rotation(item):
    u"""
    返回 Transform / Joint 世界旋转，组件返回 None。

    Args:
        item (str):
            需要查询的 Maya Transform、Joint 或 Shape 名称。

    Returns:
        list | None:
        有效时返回 [rotateX, rotateY, rotateZ]；组件或无法查询时返回 None。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if is_component(item):
        return None

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not cmds.objExists(item):
        return None

    try:
        node_type = cmds.nodeType(
            item
        )
    except Exception:
        return None

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if node_type not in [
        "transform",
        "joint",
    ]:
        try:
            item = hierarchy_utils.get_parent(
                item,
                full_path=True
            )
        except RuntimeError:
            return None

        if not item:
            return None

    # -------------------------------------------------------------------------
    # Step 04：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        rotation = transform_utils.get_world_rotation(
            item
        )
    except Exception:
        return None

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return [
        float(rotation[0]),
        float(rotation[1]),
        float(rotation[2]),
    ]


# =============================================================================
# Snap
# =============================================================================

def snap_to_average(
        reference_items,
        target_item,
        include_rotation=True
):
    u"""
    把目标吸附到参考项平均位置和平均旋转。

    Args:
        reference_items (list[str]):
            一个或多个参考 Transform、Joint 或 Component。
        target_item (str):
            需要被移动的目标 Maya Item。
        include_rotation (bool):
            是否在位置之外尝试应用有效参考对象的平均世界旋转。

    Returns:
        dict:
        返回 position 和 rotation；没有有效平均旋转时 rotation 为 None。

    Raises:
        RuntimeError:
        没有参考项、目标为空或无法取得任何有效参考位置时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not reference_items:
        raise RuntimeError(
            u"参考对象不能为空。"
        )

    if not target_item:
        raise RuntimeError(
            u"目标对象不能为空。"
        )

    positions = []

    for item in reference_items:
        position = get_item_world_position(
            item
        )

        if position is not None:
            positions.append(
                position
            )

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    average_position = math_utils.average_point3(
        positions
    )

    if average_position is None:
        raise RuntimeError(
            u"无法从选择中取得有效参考位置。"
        )

    cmds.xform(
        target_item,
        worldSpace=True,
        translation=average_position
    )

    result = {
        "position": average_position,
        "rotation": None,
    }

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not include_rotation:
        return result

    if is_component(target_item):
        return result

    rotations = []

    for item in reference_items:
        rotation = get_item_world_rotation(
            item
        )

        if rotation is not None:
            rotations.append(
                rotation
            )

    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    average_rotation = math_utils.average_point3(
        rotations
    )

    if average_rotation is None:
        return result

    try:
        cmds.xform(
            target_item,
            worldSpace=True,
            rotation=average_rotation
        )
        result["rotation"] = average_rotation
    except Exception:
        pass

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result


__all__ = [
    "is_component",
    "get_item_world_position",
    "get_item_world_rotation",
    "snap_to_average",
]
