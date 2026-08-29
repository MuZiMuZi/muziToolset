# coding=utf-8
u"""
Constraint Utils
================

Maya Constraint 底层工具。

职责：
    1. 创建常用 Constraint；
    2. 批量为多个 Driven 创建 Constraint；
    3. 创建 Pole Vector Constraint；
    4. 查询对象关联的 Constraint；
    5. 删除对象关联的 Constraint。

说明：
    - 本模块只负责 Maya 场景操作，不创建 UI；
    - 不依赖 tools / app / ui / systems；
    - UI 层负责解释用户选择，本模块接收明确的 Driver / Driven 参数；
    - 从旧 pipelineUtils 中拆出的通用约束职责统一收口到这里。
"""

from __future__ import print_function

import maya.cmds as cmds


constraint_types = [
    "parentConstraint",
    "pointConstraint",
    "orientConstraint",
    "scaleConstraint",
    "aimConstraint",
    "poleVectorConstraint",
]


# =============================================================================
# Validate
# =============================================================================

def validate_node(node):
    """检查 Maya 节点是否存在。"""
    if not node:
        raise RuntimeError(u"节点名称不能为空。")

    if not cmds.objExists(node):
        raise RuntimeError(
            u"Maya 节点不存在：{}".format(node)
        )

    return True


def normalize_nodes(nodes):
    """把单个节点或节点列表整理成列表，并保持原顺序去重。"""
    result = []

    if nodes is None:
        return result

    if isinstance(nodes, str):
        nodes = [nodes]

    for node in nodes:
        if not node:
            continue

        validate_node(node)

        if node in result:
            continue

        result.append(node)

    return result


# =============================================================================
# Create
# =============================================================================

def get_constraint_command(constraint_type):
    """根据 Constraint 类型返回对应 maya.cmds 命令。"""
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
    """
    给一个 Driven 创建标准 Constraint。

    Args:
        driver_objects(str/list): 一个或多个 Driver。
        driven_object(str): Driven。
        constraint_type(str): parent / point / orient / scale / aim Constraint。
        maintain_offset(bool): 是否保持偏移。
        **kwargs: 继续传给 Maya Constraint 命令的参数。

    Returns:
        list: Maya 创建出来的 Constraint 节点列表。
    """
    driver_objects = normalize_nodes(
        driver_objects
    )

    if not driver_objects:
        raise RuntimeError(u"至少需要一个 Driver。")

    validate_node(driven_object)

    command = get_constraint_command(
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


def create_constraints(
        driver_objects,
        driven_objects,
        constraint_type="parentConstraint",
        maintain_offset=True,
        **kwargs
):
    """
    使用同一组 Driver 批量约束多个 Driven。

    Returns:
        list: 所有创建出来的 Constraint 节点。
    """
    driver_objects = normalize_nodes(
        driver_objects
    )
    driven_objects = normalize_nodes(
        driven_objects
    )

    if not driver_objects:
        raise RuntimeError(u"至少需要一个 Driver。")

    if not driven_objects:
        raise RuntimeError(u"至少需要一个 Driven。")

    created_constraints = []

    for driven_object in driven_objects:
        result = create_constraint(
            driver_objects=driver_objects,
            driven_object=driven_object,
            constraint_type=constraint_type,
            maintain_offset=maintain_offset,
            **kwargs
        )

        for constraint_node in result:
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
    """创建 Pole Vector Constraint。"""
    validate_node(driver_object)
    validate_node(ik_handle)

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
    """
    获取一个或多个对象关联的 Constraint 节点。

    结果保持搜索顺序并去重。
    """
    nodes = normalize_nodes(nodes)

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
    """删除对象关联的 Constraint，并返回实际删除的节点名称。"""
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
    "validate_node",
    "normalize_nodes",
    "get_constraint_command",
    "create_constraint",
    "create_constraints",
    "create_pole_vector_constraint",
    "get_constraints",
    "delete_constraints",
]
