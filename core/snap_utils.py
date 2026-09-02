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

average_vectors(vectors)
    计算一组三维向量的算术平均值。

snap_to_average(reference_items, target_item, include_rotation=True)
    把目标对象吸附到多个参考项的平均位置，并在条件允许时应用平均旋转。

典型使用场景
------------
1. 把 Joint 放到两个 Vertex 中间；
2. 把 Locator 放到多个 CV 的平均位置；
3. 把 Controller Zero Group 对齐到多个参考 Transform 的平均位置；
4. UI Tool 先解释用户当前选择，再把明确的 reference_items / target_item 交给本模块。

设计原则
--------
- Core 不读取“最后选择的是目标”这类 UI 语义；这部分由 tools/snap_tool.py 决定。
- Component 可以提供位置，但通常不能直接作为 Rotation 参考。
- DAG Parent 查询复用 hierarchy_utils，不在本模块重新包装 listRelatives。
- 本模块使用普通循环展开数据处理，方便后续在 Maya Script Editor 中逐步调试。
- 这里只提供简单欧拉角平均；复杂 Orientation Blend 应进入 Matrix / Rig System，而不是继续扩张 Snap Utils。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import hierarchy_utils
from . import transform_utils


# =============================================================================
# Component Query
# =============================================================================

def is_component(item):
    u"""判断 Maya 选择项是否为常见组件。"""
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
    u"""返回对象或组件的世界空间位置。"""
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
    u"""返回 Transform / Joint 世界旋转，组件返回 None。"""
    if is_component(item):
        return None

    if not cmds.objExists(item):
        return None

    try:
        node_type = cmds.nodeType(
            item
        )
    except Exception:
        return None

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

    try:
        rotation = transform_utils.get_world_rotation(
            item
        )
    except Exception:
        return None

    return [
        float(rotation[0]),
        float(rotation[1]),
        float(rotation[2]),
    ]


# =============================================================================
# Math
# =============================================================================

def average_vectors(vectors):
    u"""计算三维向量列表平均值。"""
    if not vectors:
        return None

    total_x = 0.0
    total_y = 0.0
    total_z = 0.0

    for vector in vectors:
        total_x += vector[0]
        total_y += vector[1]
        total_z += vector[2]

    count = float(
        len(vectors)
    )

    return [
        total_x / count,
        total_y / count,
        total_z / count,
    ]


# =============================================================================
# Snap
# =============================================================================

def snap_to_average(
        reference_items,
        target_item,
        include_rotation=True
):
    u"""把目标吸附到参考项平均位置和平均旋转。"""
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

    average_position = average_vectors(
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

    average_rotation = average_vectors(
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

    return result


__all__ = [
    "is_component",
    "get_item_world_position",
    "get_item_world_rotation",
    "average_vectors",
    "snap_to_average",
]
