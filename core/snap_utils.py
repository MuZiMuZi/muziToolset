# coding=utf-8
u"""
Snap Utils
==========

Maya 对象 / 组件快速吸附底层模块。
"""

from __future__ import print_function

import maya.cmds as cmds


def is_component(item):
    """判断 Maya 选择项是否为常见组件。"""
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


def get_world_position(item):
    """返回对象或组件的世界空间位置。"""
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


def get_world_rotation(item):
    """返回 Transform / Joint 世界旋转，组件返回 None。"""
    if is_component(item):
        return None

    if not cmds.objExists(item):
        return None

    try:
        node_type = cmds.nodeType(item)
    except Exception:
        return None

    if node_type not in [
        "transform",
        "joint",
    ]:
        parents = cmds.listRelatives(
            item,
            parent=True,
            fullPath=True
        )

        if parents is None:
            parents = []

        if not parents:
            return None

        item = parents[0]

    try:
        rotation = cmds.xform(
            item,
            query=True,
            worldSpace=True,
            rotation=True
        )
    except Exception:
        rotation = None

    if not rotation:
        return None

    if len(rotation) < 3:
        return None

    return [
        float(rotation[0]),
        float(rotation[1]),
        float(rotation[2]),
    ]


def average_vectors(vectors):
    """计算三维向量列表平均值。"""
    if not vectors:
        return None

    total_x = 0.0
    total_y = 0.0
    total_z = 0.0

    for vector in vectors:
        total_x += vector[0]
        total_y += vector[1]
        total_z += vector[2]

    count = float(len(vectors))

    return [
        total_x / count,
        total_y / count,
        total_z / count,
    ]


def snap_to_average(
        reference_items,
        target_item,
        include_rotation=True
):
    """把目标吸附到参考项平均位置和平均旋转。"""
    if not reference_items:
        raise RuntimeError(u"参考对象不能为空。")

    if not target_item:
        raise RuntimeError(u"目标对象不能为空。")

    positions = []

    for item in reference_items:
        position = get_world_position(item)

        if position is not None:
            positions.append(position)

    average_position = average_vectors(positions)

    if average_position is None:
        raise RuntimeError(u"无法从选择中取得有效参考位置。")

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
        rotation = get_world_rotation(item)

        if rotation is not None:
            rotations.append(rotation)

    average_rotation = average_vectors(rotations)

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
    "get_world_position",
    "get_world_rotation",
    "average_vectors",
    "snap_to_average",
]
