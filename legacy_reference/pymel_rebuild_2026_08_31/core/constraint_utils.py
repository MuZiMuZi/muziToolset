# coding=utf-8
u"""
Constraint Utils
================

Maya Constraint 领域的通用底层工具。

模块职责
--------
本模块统一负责 Maya 原生 Constraint Node 的创建、查询和删除。
上层 Tool / System 只需要明确告诉 Core：谁是 Driver、谁是 Driven、需要什么 Constraint。

设计边界
--------
- 节点存在性统一复用 scene_utils；
- Matrix / offsetParentMatrix 网络进入 matrix_utils；
- Controller Follow / Parent Space Workflow 进入 systems.controller；
- 本模块不读取 Selection，不包含 UI。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import scene_utils


constraint_types = [
    "parentConstraint",
    "pointConstraint",
    "orientConstraint",
    "scaleConstraint",
    "aimConstraint",
    "poleVectorConstraint",
]


# =============================================================================
# Validate / Normalize
# =============================================================================


def normalize_nodes(nodes):
    u"""
    将单节点或节点列表整理成保持原顺序的去重列表。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    result = []

    if nodes is None:
        return result

    if isinstance(nodes, str):
        nodes = [nodes]

    for node in nodes:
        if not node:
            continue

        # 使用 Scene Core 统一验证每个输入节点。
        scene_utils.validate_node(
            node
        )

        if node in result:
            continue

        result.append(
            node
        )

    return result


# =============================================================================
# Create
# =============================================================================

def get_constraint_command(constraint_type):
    u"""
    根据 Constraint Type 返回对应的 maya.cmds 命令。

    Args:
        constraint_type (str):
            Maya Constraint 类型，例如 parentConstraint、pointConstraint、orientConstraint、scaleConstraint 或 aimConstraint。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    command_map = {
        "parentConstraint": cmds.parentConstraint,
        "pointConstraint": cmds.pointConstraint,
        "orientConstraint": cmds.orientConstraint,
        "scaleConstraint": cmds.scaleConstraint,
        "aimConstraint": cmds.aimConstraint,
    }

    if constraint_type not in command_map:
        raise ValueError(
            u"不支持的标准 Constraint 类型：{}".format(
                constraint_type
            )
        )

    return command_map[constraint_type]


def create_constraint(
        driver_objects,
        driven_object,
        constraint_type="parentConstraint",
        maintain_offset=True,
        **kwargs
):
    u"""
    给一个 Driven 创建标准 Maya Constraint。

    Args:
        driver_objects (str | list[str]):
            一个或多个 Driver Maya 节点；输入顺序会保留。
        driven_object (str):
            接收 Constraint、Matrix 或属性驱动结果的 Driven 节点。
        constraint_type (str):
            Maya Constraint 类型，例如 parentConstraint、pointConstraint、orientConstraint、scaleConstraint 或 aimConstraint。
        maintain_offset (bool):
            是否在建立约束或矩阵关系时保持当前偏移。
        kwargs (dict):
            继续传递给底层 maya.cmds、Qt 或 Builder API 的关键字参数。

    Returns:
        object | list:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 整理并验证 Driver 输入。
    driver_objects = normalize_nodes(
        driver_objects
    )

    if not driver_objects:
        raise RuntimeError(
            u"至少需要一个 Driver。"
        )

    # 使用 Scene Core 验证 Driven。
    scene_utils.validate_node(
        driven_object
    )

    # 获取当前 Constraint Type 对应 Maya Command。
    command = get_constraint_command(
        constraint_type
    )

    # 创建真正的 Maya Constraint。
    result = command(
        driver_objects,
        driven_object,
        maintainOffset=maintain_offset,
        **kwargs
    )

    if result is None:
        return []

    return result


def create_constraints(
        driver_objects,
        driven_objects,
        constraint_type="parentConstraint",
        maintain_offset=True,
        **kwargs
):
    u"""
    使用同一组 Driver 批量约束多个 Driven。

    Args:
        driver_objects (str | list[str]):
            一个或多个 Driver Maya 节点；输入顺序会保留。
        driven_objects (str | list[str]):
            需要批量接收驱动结果的 Driven 节点或节点列表。
        constraint_type (str):
            Maya Constraint 类型，例如 parentConstraint、pointConstraint、orientConstraint、scaleConstraint 或 aimConstraint。
        maintain_offset (bool):
            是否在建立约束或矩阵关系时保持当前偏移。
        kwargs (dict):
            继续传递给底层 maya.cmds、Qt 或 Builder API 的关键字参数。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 整理 Driver 输入。
    driver_objects = normalize_nodes(
        driver_objects
    )

    # 整理 Driven 输入。
    driven_objects = normalize_nodes(
        driven_objects
    )

    if not driver_objects:
        raise RuntimeError(
            u"至少需要一个 Driver。"
        )

    if not driven_objects:
        raise RuntimeError(
            u"至少需要一个 Driven。"
        )

    created_constraints = []

    for driven_object in driven_objects:
        # 复用单项 Constraint API，避免批量入口维护第二套创建逻辑。
        constraint_nodes = create_constraint(
            driver_objects=driver_objects,
            driven_object=driven_object,
            constraint_type=constraint_type,
            maintain_offset=maintain_offset,
            **kwargs
        )

        for constraint_node in constraint_nodes:
            if constraint_node in created_constraints:
                continue

            created_constraints.append(
                constraint_node
            )

    return created_constraints


def create_pole_vector_constraint(
        driver_object,
        ik_handle
):
    u"""
    创建 Pole Vector Constraint。

    Args:
        driver_object (str):
            作为 Constraint、Matrix 或属性关系 Driver 的 Maya 节点。
        ik_handle (str):
            接收 Pole Vector Constraint 或 IK 操作的 Maya ikHandle 节点。

    Returns:
        object | list:
        方法执行后的结果数据。
    """
    # 使用 Scene Core 验证 Driver。
    scene_utils.validate_node(
        driver_object
    )

    # 使用 Scene Core 验证 IK Handle。
    scene_utils.validate_node(
        ik_handle
    )

    # Pole Vector 调用签名不同，因此保留独立创建入口。
    result = cmds.poleVectorConstraint(
        driver_object,
        ik_handle
    )

    if result is None:
        return []

    return result


# =============================================================================
# Query
# =============================================================================

def get_constraints(
        nodes,
        search_types=None
):
    u"""
    获取一个或多个对象关联的 Constraint 节点。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。
        search_types (str | list[str] | None):
            需要查询的 Maya 节点类型；None 表示使用方法默认的类型集合。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 整理并验证查询目标。
    nodes = normalize_nodes(
        nodes
    )

    if search_types is None:
        search_types = constraint_types

    result = []

    for node in nodes:
        for constraint_type in search_types:
            connected_nodes = cmds.listConnections(
                node,
                type=constraint_type
            )

            if connected_nodes is None:
                connected_nodes = []

            for connected_node in connected_nodes:
                if connected_node in result:
                    continue

                result.append(
                    connected_node
                )

    return result


# =============================================================================
# Delete
# =============================================================================

def delete_constraints(
        nodes,
        search_types=None
):
    u"""
    删除对象关联的 Constraint，并返回实际删除节点。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。
        search_types (str | list[str] | None):
            需要查询的 Maya 节点类型；None 表示使用方法默认的类型集合。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 统一查询目标 Constraint。
    constraint_nodes = get_constraints(
        nodes=nodes,
        search_types=search_types
    )

    deleted_nodes = []

    for constraint_node in constraint_nodes:
        if not cmds.objExists(constraint_node):
            continue

        deleted_nodes.append(
            constraint_node
        )

        cmds.delete(
            constraint_node
        )

    return deleted_nodes


__all__ = [
    "constraint_types",
    "normalize_nodes",
    "get_constraint_command",
    "create_constraint",
    "create_constraints",
    "create_pole_vector_constraint",
    "get_constraints",
    "delete_constraints",
]
