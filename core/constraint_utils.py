# coding=utf-8
u"""
Constraint Utils
================

Maya Constraint 领域的通用底层工具。

模块职责
--------
本模块统一负责 Maya 原生 Constraint Node 的创建和 Driven 侧查询。
上层 Tool / System 只需要明确告诉 Core：谁是 Driver、谁是 Driven、需要什么 Constraint。

设计边界
--------
- 节点存在性统一复用 scene_utils；
- Matrix / offsetParentMatrix 网络进入 matrix_utils；
- Controller Follow / Parent Space Workflow 进入 systems.controller；
- Selection、批量 Workflow 和删除决策由上层 Tool / System 负责；
- 本模块不读取 Selection，不包含 UI。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import scene_utils


_STANDARD_CONSTRAINT_COMMANDS = {
    "parentConstraint": cmds.parentConstraint,
    "pointConstraint": cmds.pointConstraint,
    "orientConstraint": cmds.orientConstraint,
    "scaleConstraint": cmds.scaleConstraint,
    "aimConstraint": cmds.aimConstraint,
}

_CONSTRAINT_TYPES = [
    "parentConstraint",
    "pointConstraint",
    "orientConstraint",
    "scaleConstraint",
    "aimConstraint",
    "poleVectorConstraint",
]


# =============================================================================
# Internal Helpers
# =============================================================================

def _normalize_nodes(nodes):
    u"""
    将单节点或节点列表整理成保持原顺序的去重列表。

    Args:
        nodes (str | list[str]):
            需要查询或处理的 Maya 节点名称或节点列表。

    Returns:
        list[str]:
            已验证、去重并保持原顺序的 Maya 节点列表。
    """
    result = []

    if nodes is None:
        return result

    if isinstance(nodes, str):
        nodes = [nodes]

    for node in nodes:
        if not node:
            continue

        scene_utils.validate_node(
            node
        )

        if node in result:
            continue

        result.append(
            node
        )

    return result


def _normalize_search_types(search_types):
    u"""
    整理需要查询的 Constraint 类型。

    Args:
        search_types (str | list[str] | None):
            单个 Constraint 类型、Constraint 类型列表或 None。

    Returns:
        list[str]:
            已去重并保持原顺序的 Constraint 类型列表。

    Raises:
        ValueError:
            输入了当前 Core 不支持的 Constraint 类型时抛出。
    """
    if search_types is None:
        search_types = _CONSTRAINT_TYPES

    if isinstance(search_types, str):
        search_types = [search_types]

    result = []

    for constraint_type in search_types:
        if constraint_type not in _CONSTRAINT_TYPES:
            raise ValueError(
                u"不支持的 Constraint 类型：{}".format(
                    constraint_type
                )
            )

        if constraint_type in result:
            continue

        result.append(
            constraint_type
        )

    return result


def _get_constraint_command(constraint_type):
    u"""
    根据标准 Constraint Type 返回对应的 maya.cmds 命令。

    Args:
        constraint_type (str):
            parentConstraint、pointConstraint、orientConstraint、scaleConstraint 或 aimConstraint。

    Returns:
        callable:
            对应的 maya.cmds Constraint 命令。

    Raises:
        ValueError:
            输入类型不是标准 Constraint 创建入口支持的类型时抛出。
    """
    if constraint_type not in _STANDARD_CONSTRAINT_COMMANDS:
        raise ValueError(
            u"不支持的标准 Constraint 类型：{}".format(
                constraint_type
            )
        )

    return _STANDARD_CONSTRAINT_COMMANDS[constraint_type]


# =============================================================================
# Create
# =============================================================================

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
            真正接收 Constraint 输出的 Driven Maya 节点。
        constraint_type (str):
            parentConstraint、pointConstraint、orientConstraint、scaleConstraint 或 aimConstraint。
        maintain_offset (bool):
            是否保持 Driver 与 Driven 当前偏移。
        kwargs (dict):
            继续传递给对应 maya.cmds Constraint 命令的关键字参数。

    Returns:
        list[str]:
            Maya 创建出的 Constraint 节点列表；没有结果时返回空列表。

    Raises:
        RuntimeError:
            Driver / Driven 输入无效时抛出。
        ValueError:
            Constraint 类型不受标准创建入口支持时抛出。
    """
    driver_objects = _normalize_nodes(
        driver_objects
    )

    if not driver_objects:
        raise RuntimeError(
            u"至少需要一个 Driver。"
        )

    scene_utils.validate_node(
        driven_object
    )

    command = _get_constraint_command(
        constraint_type
    )

    result = command(
        driver_objects,
        driven_object,
        maintainOffset=maintain_offset,
        **kwargs
    )

    if result is None:
        return []

    return result


def create_pole_vector_constraint(
        driver_object,
        ik_handle
):
    u"""
    创建 Pole Vector Constraint。

    Args:
        driver_object (str):
            Pole Vector Driver Maya 节点。
        ik_handle (str):
            接收 Pole Vector Constraint 的 Maya ikHandle 节点。

    Returns:
        list[str]:
            Maya 创建出的 Pole Vector Constraint 节点列表；没有结果时返回空列表。

    Raises:
        RuntimeError:
            Driver / IK Handle 输入无效，或第二个参数不是 ikHandle 时抛出。
    """
    scene_utils.validate_node(
        driver_object
    )

    scene_utils.validate_node(
        ik_handle
    )

    if cmds.nodeType(ik_handle) != "ikHandle":
        raise RuntimeError(
            u"Pole Vector Driven 必须是 ikHandle：{}".format(
                ik_handle
            )
        )

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
    获取真正驱动一个或多个对象的 Constraint 节点。

    查询只沿 Maya DG 的输入方向查找 Constraint，因此：
    - Driven 对象会返回实际向它输出结果的 Constraint；
    - 仅作为 Driver 的对象不会因为连接到 Constraint 而被返回；
    - 不把“所有有关联的 Constraint”混同为“对象身上的 Constraint”。

    Args:
        nodes (str | list[str]):
            需要查询 Driven Constraint 的 Maya 节点名称或节点列表。
        search_types (str | list[str] | None):
            需要查询的 Constraint 类型；None 表示查询全部正式支持类型。

    Returns:
        list[str]:
            真正向输入对象输出驱动结果的 Constraint 节点，保持查询顺序并去重。

    Raises:
        RuntimeError:
            查询目标节点无效时抛出。
        ValueError:
            search_types 包含不受支持的 Constraint 类型时抛出。
    """
    nodes = _normalize_nodes(
        nodes
    )

    search_types = _normalize_search_types(
        search_types
    )

    result = []

    for node in nodes:
        for constraint_type in search_types:
            constraint_nodes = cmds.listConnections(
                node,
                source=True,
                destination=False,
                type=constraint_type
            )

            if constraint_nodes is None:
                constraint_nodes = []

            for constraint_node in constraint_nodes:
                if constraint_node in result:
                    continue

                result.append(
                    constraint_node
                )

    return result


__all__ = [
    "create_constraint",
    "create_pole_vector_constraint",
    "get_constraints",
]
