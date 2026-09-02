# coding=utf-8
u"""
Transform Utils
===============

Maya Transform / Joint 的通用空间数据底层工具。

模块职责
--------
- Transform / Joint 输入校验；
- World Translation 读取 / 写入；
- World Rotation 读取 / 写入；
- World Matrix 读取 / 写入；
- 相对移动。

模块边界
--------
    Transform 空间数据读写        -> transform_utils
    纯 Point / Vector 数学         -> math_utils
    Matrix 数学 / Matrix DG 网络   -> matrix_utils
    Maya Constraint Node           -> constraint_utils
    “把 A 对齐到 B”的工作流       -> snap_utils

设计原则
--------
1. 本模块是无状态 Utils，每次收到外部 node 参数时都进行有效性检查；
2. 接收明确节点参数，不依赖当前 Maya Selection；
3. 返回普通 Python 数据，方便 Tool / System / Test 复用；
4. World Space 查询统一从这里进入，避免上层重复 cmds.xform 参数组合。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import math_utils
from . import scene_utils


# =============================================================================
# Validate
# =============================================================================

def validate_transform(node):
    u"""
    检查节点存在，并确认它是 Maya Transform / Joint。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool:
            方法执行后的结果数据。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    scene_utils.validate_node(
        node
    )

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


def _validate_vector3(value, label):
    u"""检查 Translation / Rotation / Offset 是否包含 3 个数值。"""
    if value is None:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    try:
        value_count = len(
            value
        )
    except TypeError:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    if value_count != 3:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
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
    validate_transform(
        node
    )

    return cmds.xform(
        node,
        query=True,
        worldSpace=True,
        translation=True
    )


def set_world_translation(node, translation):
    u"""
    设置 Transform / Joint 的 World Translation。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。
        translation (object):
            当前方法执行 Maya / Rig 操作时使用的 `translation` 数据。

    Returns:
        object:
            方法执行后的结果数据。
    """
    validate_transform(
        node
    )
    _validate_vector3(
        translation,
        "translation"
    )

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
    validate_transform(
        node
    )

    return cmds.xform(
        node,
        query=True,
        worldSpace=True,
        rotation=True
    )


def set_world_rotation(node, rotation):
    u"""
    设置 Transform / Joint 的 World Rotation。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。
        rotation (list[float] | tuple[float, float, float]):
            Joint / Transform 使用的 XYZ Rotation。

    Returns:
        object:
            方法执行后的结果数据。
    """
    validate_transform(
        node
    )
    _validate_vector3(
        rotation,
        "rotation"
    )

    cmds.xform(
        node,
        worldSpace=True,
        rotation=rotation
    )

    return node


# =============================================================================
# Matrix
# =============================================================================

def get_world_matrix(node):
    u"""
    返回 Transform / Joint 的完整 4x4 World Matrix 普通 list。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """
    validate_transform(
        node
    )

    return cmds.xform(
        node,
        query=True,
        worldSpace=True,
        matrix=True
    )


def set_world_matrix(node, matrix_values):
    u"""
    设置 Transform / Joint 的完整 4x4 World Matrix。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。
        matrix_values (object):
            当前方法执行 Maya / Rig 操作时使用的 `matrix_values` 数据。

    Returns:
        object:
            方法执行后的结果数据。

    Raises:
        ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    validate_transform(
        node
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if matrix_values is None:
        raise ValueError(
            u"matrix_values 必须包含 16 个矩阵数值。"
        )

    try:
        value_count = len(
            matrix_values
        )
    except TypeError:
        raise ValueError(
            u"matrix_values 必须包含 16 个矩阵数值。"
        )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if value_count != 16:
        raise ValueError(
            u"matrix_values 必须包含 16 个矩阵数值。"
        )

    # -------------------------------------------------------------------------
    # Step 04：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    cmds.xform(
        node,
        worldSpace=True,
        matrix=matrix_values
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return node


# =============================================================================
# Move
# =============================================================================

def move_relative(
        node,
        offset,
        space="world",
        object_space=None
):
    u"""
    相对移动一个 Transform / Joint。

    Args:
        node (str):
            Transform / Joint。
        offset (list | tuple):
            [x, y, z] 相对偏移量。
        space (str):
            ``world`` 或 ``object``。
        object_space (bool | None):
            旧调用兼容参数；新代码请使用 space。

    Returns:
        object:
            方法执行后的结果数据。

    Raises:
        ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    validate_transform(
        node
    )
    _validate_vector3(
        offset,
        "offset"
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if object_space is not None:
        if object_space:
            space = "object"
        else:
            space = "world"

    if isinstance(space, bool):
        if space:
            space = "object"
        else:
            space = "world"

    space = str(space).strip().lower()

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if space not in ["world", "object"]:
        raise ValueError(
            u"space 只能是 'world' 或 'object'。"
        )

    kwargs = {
        "relative": True,
    }

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if space == "object":
        kwargs["objectSpace"] = True
        kwargs["worldSpaceDistance"] = True
    else:
        kwargs["worldSpace"] = True

    cmds.move(
        offset[0],
        offset[1],
        offset[2],
        node,
        **kwargs
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return node


# =============================================================================
# Legacy Compatibility
# =============================================================================

def distance_between(node_a, node_b):
    u"""
    旧 Transform 距离入口。

    新代码应读取 World Translation 后调用
    math_utils.distance_between_points()。

    Args:
        node_a (object):
            当前方法执行 Maya / Rig 操作时使用的 `node_a` 数据。
        node_b (object):
            当前方法执行 Maya / Rig 操作时使用的 `node_b` 数据。

    Returns:
        object:
            方法执行后的结果数据。
    """
    position_a = get_world_translation(
        node_a
    )
    position_b = get_world_translation(
        node_b
    )

    return math_utils.distance_between_points(
        position_a,
        position_b
    )


__all__ = [
    "validate_transform",
    "get_world_translation",
    "set_world_translation",
    "get_world_rotation",
    "set_world_rotation",
    "get_world_matrix",
    "set_world_matrix",
    "move_relative",
]
