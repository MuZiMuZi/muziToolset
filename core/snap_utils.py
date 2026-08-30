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

get_world_position(item)
    获取对象或组件的世界空间位置。

get_world_rotation(item)
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
- 本模块使用普通循环展开数据处理，方便后续在 Maya Script Editor 中逐步调试。
- 这里只提供简单欧拉角平均；复杂 Orientation Blend 应进入 Matrix / Rig System，而不是继续扩张 Snap Utils。
"""

from __future__ import print_function

import maya.cmds as cmds


# =============================================================================
# Component Query
# =============================================================================

def is_component(item):
    u"""
    判断 Maya 选择项是否为常见组件。

    Args:
        item (str):
            Maya 对象名或组件字符串。

    Returns:
        bool:
        True 表示 Vertex / Edge / Face / CV 等组件；否则返回 False。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：没有“.”时通常就是普通 DAG / DG 节点，不可能是组件字符串。
    # -------------------------------------------------------------------------
    if not item:
        return False

    if "." not in item:
        return False

    # -------------------------------------------------------------------------
    # 步骤 2：检查 Maya 常见组件 Token。
    #
    # 为什么不用 cmds.filterExpand：
    # 这个函数经常用于已经拿到字符串之后的轻量判断，不需要额外依赖当前 Selection。
    # -------------------------------------------------------------------------
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

def get_world_position(item):
    u"""
    返回对象或组件的世界空间位置。

    Maya 的 cmds.xform 同时可以查询 Transform 和大部分组件，因此这里统一使用 xform，
    避免在调用端分别判断 Vertex / CV / Transform。

    Args:
        item (object):
            `item` 对应的输入数据。

    Returns:
        list | None:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：尝试直接查询 World Translation。
    # -------------------------------------------------------------------------
    try:
        position = cmds.xform(
            item,
            query=True,
            worldSpace=True,
            translation=True
        )
    except Exception:
        position = None

    # -------------------------------------------------------------------------
    # 步骤 2：过滤 Maya 查询失败或返回数据不完整的情况。
    # -------------------------------------------------------------------------
    if not position:
        return None

    if len(position) < 3:
        return None

    # -------------------------------------------------------------------------
    # 步骤 3：统一返回普通 Python float，方便后续 JSON / 数学工具继续处理。
    # -------------------------------------------------------------------------
    return [
        float(position[0]),
        float(position[1]),
        float(position[2]),
    ]


def get_world_rotation(item):
    u"""
    返回 Transform / Joint 世界旋转，组件返回 None。

    如果传入的是 Shape，会先尝试找到它的 Transform Parent，再查询 Transform Rotation。

    Args:
        item (object):
            `item` 对应的输入数据。

    Returns:
        list | None:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：组件没有可直接当作 Transform Rotation 使用的稳定旋转值，因此直接跳过。
    # -------------------------------------------------------------------------
    if is_component(item):
        return None

    if not cmds.objExists(item):
        return None

    # -------------------------------------------------------------------------
    # 步骤 2：判断当前节点是不是可以直接查询 Rotation 的 Transform / Joint。
    # -------------------------------------------------------------------------
    try:
        node_type = cmds.nodeType(item)
    except Exception:
        return None

    if node_type not in [
        "transform",
        "joint",
    ]:
        # ---------------------------------------------------------------------
        # Shape 本身没有独立 Transform Rotation，所以回到它的父 Transform。
        # ---------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 3：查询世界欧拉角。
    # -------------------------------------------------------------------------
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


# =============================================================================
# Math
# =============================================================================

def average_vectors(vectors):
    u"""
    计算三维向量列表平均值。

    Args:
        vectors (list):
            [[x, y, z], [x, y, z], ...]

    Returns:
        list/None:
        [x, y, z]；没有有效输入时返回 None。
    """
    if not vectors:
        return None

    total_x = 0.0
    total_y = 0.0
    total_z = 0.0

    # -------------------------------------------------------------------------
    # 步骤 1：分别累计 XYZ，保留最直观的调试过程。
    # -------------------------------------------------------------------------
    for vector in vectors:
        total_x += vector[0]
        total_y += vector[1]
        total_z += vector[2]

    # -------------------------------------------------------------------------
    # 步骤 2：除以有效向量数量得到平均值。
    # -------------------------------------------------------------------------
    count = float(len(vectors))

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
    u"""
    把目标吸附到参考项平均位置和平均旋转。

    Args:
        reference_items (list):
            一个或多个参考 Transform / Joint / Component。
        target_item (str):
            需要移动的目标对象或组件。
        include_rotation (bool):
            True 时尝试计算参考 Transform 的平均世界旋转；False 时只处理位置。

    Returns:
        dict:
        {
        "position": [x, y, z],
        "rotation": [x, y, z] 或 None,
        }

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    if not reference_items:
        raise RuntimeError(u"参考对象不能为空。")

    if not target_item:
        raise RuntimeError(u"目标对象不能为空。")

    # -------------------------------------------------------------------------
    # 步骤 1：从所有参考项收集有效世界位置。
    #
    # Component 和 Transform 都可以进入这一阶段，因此 Joint 对齐到 Vertex 中点这类工作流
    # 不需要在上层再写第二套位置算法。
    # -------------------------------------------------------------------------
    positions = []

    for item in reference_items:
        position = get_world_position(item)

        if position is not None:
            positions.append(position)

    # -------------------------------------------------------------------------
    # 步骤 2：计算平均位置并应用到目标。
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 3：如果调用者只要求位置，到这里即可返回。
    # -------------------------------------------------------------------------
    if not include_rotation:
        return result

    # -------------------------------------------------------------------------
    # 步骤 4：目标本身如果是组件，不尝试写 Rotation。
    # -------------------------------------------------------------------------
    if is_component(target_item):
        return result

    # -------------------------------------------------------------------------
    # 步骤 5：只从能够提供 Transform Rotation 的参考项收集旋转。
    # -------------------------------------------------------------------------
    rotations = []

    for item in reference_items:
        rotation = get_world_rotation(item)

        if rotation is not None:
            rotations.append(rotation)

    average_rotation = average_vectors(rotations)

    if average_rotation is None:
        return result

    # -------------------------------------------------------------------------
    # 步骤 6：应用平均欧拉角。
    #
    # 注意：这是轻量 Snap 行为，不是严格的 Quaternion / Matrix Orientation Blend。
    # 对高端 Rig Orientation Blend 应使用 matrix_utils 或专门 Rig System。
    # -------------------------------------------------------------------------
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
