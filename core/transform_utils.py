# coding=utf-8
u"""
Transform Utils
===============

Maya Transform 通用底层工具。

从旧 pipelineUtils 中拆出的职责：
    - 获取 / 设置世界位置；
    - 相对移动 Transform；
    - 计算两个节点之间的世界距离；
    - 获取 / 设置完整 World Matrix。

说明：
    - 不负责 Constraint；
    - 不负责 Snap 工作流；
    - 不创建 UI；
    - 统一使用正确拼写 distance_between，淘汰旧 distence_between。
"""

from __future__ import print_function

import math

import maya.cmds as cmds


# =============================================================================
# Validate
# =============================================================================

def validate_transform(node):
    """检查节点是否存在，并且是 DAG Transform / Joint。"""
    if not node:
        raise RuntimeError(u"节点名称不能为空。")

    if not cmds.objExists(node):
        raise RuntimeError(
            u"Maya 节点不存在：{}".format(node)
        )

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
# Translation
# =============================================================================

def get_world_translation(node):
    """返回节点 World Translation [x, y, z]。"""
    validate_transform(node)

    translation = cmds.xform(
        node,
        query=True,
        worldSpace=True,
        translation=True
    )

    return translation


def set_world_translation(node, translation):
    """设置节点 World Translation。"""
    validate_transform(node)

    if translation is None or len(translation) != 3:
        raise ValueError(
            u"translation 必须是包含 3 个数值的列表或元组。"
        )

    cmds.xform(
        node,
        worldSpace=True,
        translation=translation
    )

    return node


def move_relative(node, offset, object_space=False):
    """
    相对移动节点。

    Args:
        node(str): Transform / Joint。
        offset(list/tuple): [x, y, z]。
        object_space(bool): True 时按 Object Space 移动，否则按 World Space。
    """
    validate_transform(node)

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
    """返回两个 Transform / Joint 世界位置之间的欧氏距离。"""
    position_a = get_world_translation(node_a)
    position_b = get_world_translation(node_b)

    delta_x = position_b[0] - position_a[0]
    delta_y = position_b[1] - position_a[1]
    delta_z = position_b[2] - position_a[2]

    distance_squared = (
        delta_x * delta_x
        + delta_y * delta_y
        + delta_z * delta_z
    )

    return math.sqrt(distance_squared)


# =============================================================================
# Matrix
# =============================================================================

def get_world_matrix(node):
    """返回节点 16 个数值组成的 World Matrix。"""
    validate_transform(node)

    matrix_values = cmds.xform(
        node,
        query=True,
        worldSpace=True,
        matrix=True
    )

    return matrix_values


def set_world_matrix(node, matrix_values):
    """设置节点完整 World Matrix。"""
    validate_transform(node)

    if matrix_values is None or len(matrix_values) != 16:
        raise ValueError(
            u"matrix_values 必须包含 16 个矩阵数值。"
        )

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
