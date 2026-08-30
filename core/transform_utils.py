# coding=utf-8
u"""
Transform Utils
===============

Maya Transform / Joint 的通用空间变换底层工具。

模块职责
--------
这个模块只处理 Transform 数据本身，例如：

    - Transform / Joint 输入校验；
    - World Translation 读取 / 写入；
    - World Rotation 读取 / 写入；
    - 相对移动；
    - Transform 间距离；
    - World Matrix 读取 / 写入。

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
5. Transform / Joint 的 World Space 查询统一从这里进入，避免上层重复 cmds.xform。
"""

from __future__ import print_function

import math

import maya.cmds as cmds

from . import scene_utils


# =============================================================================
# Validate
# =============================================================================

def validate_transform(node):
    u"""
    检查节点是否存在，并确认它是 Maya Transform / Joint。

    Args:
        node (str):
            需要检查的 Maya 节点。

    Returns:
        bool:
        节点有效时返回 True。

    Raises:
        RuntimeError:
        节点为空、不存在，或者类型不是 transform / joint。
    """
    # 先使用 Scene 层统一检查节点存在性，避免 Core 内维护第二套 objExists 逻辑。
    scene_utils.validate_node(
        node
    )

    # Joint 继承 Transform 行为，但 Maya nodeType 返回 joint，
    # 因此这里显式允许 transform 和 joint 两种节点类型。
    node_type = cmds.nodeType(
        node
    )

    if node_type not in ["transform", "joint"]:
        raise RuntimeError(
            u"节点不是 Transform / Joint：{} | type={}".format(
                node,
                node_type
            )
        )

    return True


# =============================================================================
# Translation
# =============================================================================

def get_world_translation(node):
    u"""
    返回 Transform / Joint 的 World Translation。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 确保输入节点可以作为 Transform 使用。
    validate_transform(
        node
    )

    # 统一从这里读取 World Translation，上层不再重复 cmds.xform 查询。
    translation = cmds.xform(
        node,
        query=True,
        worldSpace=True,
        translation=True
    )

    return translation


def set_world_translation(node, translation):
    u"""
    设置 Transform / Joint 的 World Translation。

    Args:
        node (str):
            Transform / Joint。
        translation (list | tuple):
            [x, y, z]。

    Returns:
        str:
        被修改的节点名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 确保输入节点可以作为 Transform 使用。
    validate_transform(
        node
    )

    if translation is None or len(translation) != 3:
        raise ValueError(
            u"translation 必须是包含 3 个数值的列表或元组。"
        )

    # 写入 World Translation。
    cmds.xform(
        node,
        worldSpace=True,
        translation=translation
    )

    return node


# =============================================================================
# Rotation
# =============================================================================

def get_world_rotation(node):
    u"""
    返回 Transform / Joint 的 World Rotation。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 确保输入节点可以作为 Transform 使用。
    validate_transform(
        node
    )

    # 统一从这里读取 World Rotation，上层不再重复 cmds.xform 查询。
    rotation = cmds.xform(
        node,
        query=True,
        worldSpace=True,
        rotation=True
    )

    return rotation


def set_world_rotation(node, rotation):
    u"""
    设置 Transform / Joint 的 World Rotation。

    Args:
        node (str):
            Transform / Joint。
        rotation (list | tuple):
            [x, y, z]。

    Returns:
        str:
        被修改的节点名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 确保输入节点可以作为 Transform 使用。
    validate_transform(
        node
    )

    if rotation is None or len(rotation) != 3:
        raise ValueError(
            u"rotation 必须是包含 3 个数值的列表或元组。"
        )

    # 写入 World Rotation。
    cmds.xform(
        node,
        worldSpace=True,
        rotation=rotation
    )

    return node


# =============================================================================
# Move
# =============================================================================

def move_relative(node, offset, object_space=False):
    u"""
    相对移动一个 Transform / Joint。

    Args:
        node (str):
            Transform / Joint。
        offset (list | tuple):
            [x, y, z] 相对偏移量。
        object_space (bool):
            False 按世界空间方向移动；True 按 Object Space 轴向移动。

    Returns:
        str:
        被移动的节点名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 确保输入节点可以作为 Transform 使用。
    validate_transform(
        node
    )

    if offset is None or len(offset) != 3:
        raise ValueError(
            u"offset 必须是包含 3 个数值的列表或元组。"
        )

    kwargs = {
        "relative": True,
    }

    if object_space:
        kwargs["objectSpace"] = True
        kwargs["worldSpaceDistance"] = True
    else:
        kwargs["worldSpace"] = True

    # 根据指定空间执行相对位移。
    cmds.move(
        offset[0],
        offset[1],
        offset[2],
        node,
        **kwargs
    )

    return node


# =============================================================================
# Distance
# =============================================================================

def distance_between(node_a, node_b):
    u"""
    返回两个 Transform / Joint 世界位置之间的欧氏距离。

    Args:
        node_a (object):
            当前方法执行 Maya / Rig 操作时使用的 `node_a` 数据。
        node_b (object):
            当前方法执行 Maya / Rig 操作时使用的 `node_b` 数据。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 获取两个节点的统一 World Translation 数据。
    position_a = get_world_translation(
        node_a
    )
    position_b = get_world_translation(
        node_b
    )

    delta_x = position_b[0] - position_a[0]
    delta_y = position_b[1] - position_a[1]
    delta_z = position_b[2] - position_a[2]

    distance_squared = (
        delta_x * delta_x
        + delta_y * delta_y
        + delta_z * delta_z
    )

    return math.sqrt(
        distance_squared
    )


# =============================================================================
# Matrix
# =============================================================================

def get_world_matrix(node):
    u"""
    返回 Transform / Joint 的完整 4x4 World Matrix。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 确保输入节点可以作为 Transform 使用。
    validate_transform(
        node
    )

    # 读取完整 World Matrix，并保持普通 Python list 作为 Core API 输出。
    matrix_values = cmds.xform(
        node,
        query=True,
        worldSpace=True,
        matrix=True
    )

    return matrix_values


def set_world_matrix(node, matrix_values):
    u"""
    设置 Transform / Joint 的完整 World Matrix。

    Args:
        node (str):
            Transform / Joint。
        matrix_values (list | tuple):
            16 个矩阵数值。

    Returns:
        str:
        被修改的节点名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 确保输入节点可以作为 Transform 使用。
    validate_transform(
        node
    )

    if matrix_values is None or len(matrix_values) != 16:
        raise ValueError(
            u"matrix_values 必须包含 16 个矩阵数值。"
        )

    # 写入完整 World Matrix。
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
    "get_world_rotation",
    "set_world_rotation",
    "move_relative",
    "distance_between",
    "get_world_matrix",
    "set_world_matrix",
]
