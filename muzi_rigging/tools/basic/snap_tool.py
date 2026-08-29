# coding=utf-8
u"""
Quick Snap Tool
===============

选择规则：
    1. 前面的选择作为参考；
    2. 最后一个选择作为需要移动的目标；
    3. 目标位置吸附到所有参考项的世界空间平均位置；
    4. 当目标是 Transform / Joint 时，再使用可取得旋转的参考对象平均旋转。

支持 Transform、Joint 和组件位置查询，不依赖旧 ``core.snapUtils``。
"""

from __future__ import print_function

import maya.cmds as cmds


def _is_component(item):
    """粗略判断 Maya 选择项是否为组件。"""
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


def _world_position(item):
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


def _world_rotation(item):
    """返回 Transform / Joint 的世界旋转；组件返回 None。"""
    if _is_component(item):
        return None

    if not cmds.objExists(item):
        return None

    try:
        node_type = cmds.nodeType(item)
    except Exception:
        return None

    if node_type not in ("transform", "joint"):
        parents = cmds.listRelatives(
            item,
            parent=True,
            fullPath=True
        ) or []

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

    if not rotation or len(rotation) < 3:
        return None

    return [
        float(rotation[0]),
        float(rotation[1]),
        float(rotation[2]),
    ]


def _average_vectors(vectors):
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


def snap_to_average(reference_items, target_item, include_rotation=True):
    """
    将目标吸附到参考项平均位置。

    Args:
        reference_items(list[str]): 参考对象或组件。
        target_item(str): 被移动目标。
        include_rotation(bool): 目标为 Transform / Joint 时是否同时平均旋转。

    Returns:
        dict: 实际设置的位置和旋转。
    """
    if not reference_items:
        raise RuntimeError(u"参考对象不能为空。")

    if not target_item:
        raise RuntimeError(u"目标对象不能为空。")

    positions = []

    for item in reference_items:
        position = _world_position(item)
        if position is not None:
            positions.append(position)

    average_position = _average_vectors(positions)

    if average_position is None:
        raise RuntimeError(u"无法从选择中取得有效参考位置。")

    result = {
        "position": average_position,
        "rotation": None,
    }

    cmds.xform(
        target_item,
        worldSpace=True,
        translation=average_position
    )

    if not include_rotation:
        return result

    if _is_component(target_item):
        return result

    rotations = []

    for item in reference_items:
        rotation = _world_rotation(item)
        if rotation is not None:
            rotations.append(rotation)

    average_rotation = _average_vectors(rotations)

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


def main():
    """按当前 Maya 选择执行一次 Position + Rotation 快速吸附。"""
    selected_items = cmds.ls(
        selection=True,
        flatten=True,
        long=True
    ) or []

    if len(selected_items) < 2:
        cmds.warning(u"至少选择两个对象或组件，最后一个作为被吸附目标。")
        return False

    reference_items = selected_items[:-1]
    target_item = selected_items[-1]

    cmds.undoInfo(openChunk=True, chunkName="MuziQuickSnap")
    try:
        snap_to_average(
            reference_items=reference_items,
            target_item=target_item,
            include_rotation=True
        )
    except Exception as error:
        cmds.warning(str(error))
        return False
    finally:
        cmds.undoInfo(closeChunk=True)

    return True


if __name__ == "__main__":
    main()
