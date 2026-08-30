# coding=utf-8
u"""
Transform Utils
===============

Maya Transform / Joint 的通用空间变换底层工具。

模块职责
--------
这个模块只处理“Transform 数据本身”，例如位置、移动、距离和矩阵。
它不负责创建 Constraint，也不负责更高层的 Snap / Space Switch Workflow。

当前公开方法
------------
    validate_transform(node)
        检查节点是否存在，并确认它是 Transform 或 Joint。

    get_world_translation(node)
        获取节点的世界空间位置 [x, y, z]。

    set_world_translation(node, translation)
        设置节点世界空间位置。

    move_relative(node, offset, object_space=False)
        按世界空间或物体空间做相对移动。

    distance_between(node_a, node_b)
        计算两个 Transform / Joint 世界位置之间的欧氏距离。

    get_world_matrix(node)
        获取节点 4x4 World Matrix，并以 16 个数值的普通 list 返回。

    set_world_matrix(node, matrix_values)
        使用 16 个数值设置节点完整 World Matrix。

本模块不负责
------------
- parentConstraint / pointConstraint 等 Maya Constraint；
- multMatrix / blendMatrix / offsetParentMatrix 网络；
- Selection 驱动的 Snap Tool；
- Controller / Rig System 层级创建；
- UI。

模块边界
--------
    Transform 数值读写         -> transform_utils
    Matrix DG 网络 / OPM       -> matrix_utils
    Maya Constraint Node       -> constraint_utils
    “把 A 对齐到 B”的工作流   -> snap_utils

设计原则
--------
1. 接收明确节点参数，不依赖当前 Maya Selection；
2. 每次场景修改前先校验节点类型；
3. 返回普通 Python 数据，方便 Tool / System / Test 复用；
4. 保留完整 for / if 流程，不把 Maya 操作压缩成难调试的表达式；
5. 统一使用正确拼写 ``distance_between``，不再保留早期 ``distence_between``。
"""

from __future__ import print_function

import math

import maya.cmds as cmds


# =============================================================================
# Validate - Transform / Joint 输入校验
# =============================================================================

def validate_transform(node):
    u"""
    检查节点是否存在，并且是 Maya Transform / Joint。

    Args:
        node (str):
            需要检查的 Maya 节点。

    Returns:
        bool: 节点有效时返回 True。

    Raises:
        RuntimeError:
        节点为空、不存在，或者类型不是 transform / joint。
    """
    # 步骤 1：先检查参数本身是否有效。
    if not node:
        raise RuntimeError(u"节点名称不能为空。")

    # 步骤 2：确认 Maya Scene 中确实存在这个节点。
    if not cmds.objExists(node):
        raise RuntimeError(
            u"Maya 节点不存在：{}".format(node)
        )

    # 步骤 3：确认节点类型。
    # Joint 继承 Transform 行为，但 Maya nodeType 返回的是 joint，
    # 因此这里显式允许 transform 和 joint 两种类型。
    node_type = cmds.nodeType(node)

    if node_type != "transform" and node_type != "joint":
        raise RuntimeError(
            u"节点不是 Transform / Joint：{} | type={}".format(
                node,
                node_type
            )
        )

    return True


# =============================================================================
# Translation - 世界位置读取 / 设置
# =============================================================================

def get_world_translation(node):
    u"""
    返回节点 World Translation。

    Args:
        node (str):
            Transform / Joint。

    Returns:
        list: [x, y, z]。
    """
    # 步骤 1：确认输入节点可以作为 Transform 使用。
    validate_transform(node)

    # 步骤 2：使用 xform 的 worldSpace 查询实际世界位置。
    translation = cmds.xform(
        node,
        query=True,
        worldSpace=True,
        translation=True
    )

    # 步骤 3：直接返回 Maya 的普通数值列表。
    return translation


def set_world_translation(node, translation):
    u"""
    设置节点 World Translation。

    Args:
        node (str):
            Transform / Joint。
        translation (list/tuple):
            [x, y, z]。

    Returns:
        str: 被修改的节点名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：校验 Maya 节点。
    validate_transform(node)

    # 步骤 2：校验位置数据长度。
    if translation is None or len(translation) != 3:
        raise ValueError(
            u"translation 必须是包含 3 个数值的列表或元组。"
        )

    # 步骤 3：按世界空间写入位置。
    cmds.xform(
        node,
        worldSpace=True,
        translation=translation
    )

    return node


def move_relative(node, offset, object_space=False):
    u"""
    相对移动一个 Transform / Joint。

    Args:
        node (str):
            Transform / Joint。
        offset (list/tuple):
            [x, y, z] 相对偏移量。
        object_space (bool):
            False：按世界空间方向移动； True：按节点自身 Object Space 轴向移动。

    Returns:
        str: 被移动的节点名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：校验节点。
    validate_transform(node)

    # 步骤 2：校验 Offset 数据。
    if offset is None or len(offset) != 3:
        raise ValueError(
            u"offset 必须是包含 3 个数值的列表或元组。"
        )

    # 步骤 3：根据 object_space 准备 cmds.move 参数。
    #
    # Object Space 模式下同时打开 worldSpaceDistance，
    # 表示方向使用物体局部轴，但数值距离仍按世界单位解释。
    kwargs = {
        "relative": True,
    }

    if object_space:
        kwargs["objectSpace"] = True
        kwargs["worldSpaceDistance"] = True
    else:
        kwargs["worldSpace"] = True

    # 步骤 4：执行相对移动。
    cmds.move(
        offset[0],
        offset[1],
        offset[2],
        node,
        **kwargs
    )

    return node


# =============================================================================
# Distance - 世界空间距离
# =============================================================================

def distance_between(node_a, node_b):
    u"""
    返回两个 Transform / Joint 世界位置之间的欧氏距离。

    Args:
        node_a (str):
            第一个节点。
        node_b (str):
            第二个节点。

    Returns:
        float: 世界空间距离。
    """
    # 步骤 1：统一通过 get_world_translation 获取两个节点位置。
    position_a = get_world_translation(node_a)
    position_b = get_world_translation(node_b)

    # 步骤 2：计算三个轴向的差值。
    delta_x = position_b[0] - position_a[0]
    delta_y = position_b[1] - position_a[1]
    delta_z = position_b[2] - position_a[2]

    # 步骤 3：使用欧氏距离公式。
    distance_squared = (
        delta_x * delta_x
        + delta_y * delta_y
        + delta_z * delta_z
    )

    return math.sqrt(distance_squared)


# =============================================================================
# Matrix - 完整 World Matrix 读取 / 设置
# =============================================================================

def get_world_matrix(node):
    u"""
    返回节点完整 World Matrix。

    Args:
        node (str):
            Transform / Joint。

    Returns:
        list: 16 个数值组成的 4x4 Matrix。

    Notes:
        这里返回普通 list，而不是 MMatrix。
                                            需要矩阵计算时由 matrix_utils 转成 Maya API Matrix，
                                            这样 transform_utils 保持简单的数据读写职责。
    """
    # 步骤 1：校验节点。
    validate_transform(node)

    # 步骤 2：查询完整世界矩阵。
    matrix_values = cmds.xform(
        node,
        query=True,
        worldSpace=True,
        matrix=True
    )

    return matrix_values


def set_world_matrix(node, matrix_values):
    u"""
    设置节点完整 World Matrix。

    Args:
        node (str):
            Transform / Joint。
        matrix_values (list/tuple):
            16 个矩阵数值。

    Returns:
        str: 被修改的节点名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：校验节点。
    validate_transform(node)

    # 步骤 2：Maya 4x4 Matrix 必须正好包含 16 个数值。
    if matrix_values is None or len(matrix_values) != 16:
        raise ValueError(
            u"matrix_values 必须包含 16 个矩阵数值。"
        )

    # 步骤 3：按 World Space 写入完整矩阵。
    cmds.xform(
        node,
        worldSpace=True,
        matrix=matrix_values
    )

    return node


__all__ = [
    "validate_transform",
    "get_world_translation",
    "set_world_translation",
    "move_relative",
    "distance_between",
    "get_world_matrix",
    "set_world_matrix",
]
