# coding=utf-8
u"""
Constraint Utils
================

Maya Constraint 领域的通用底层工具。

模块职责
--------
这个模块统一负责 Maya 原生 Constraint Node 的创建、查询和删除。
上层 Tool / System 只需要明确告诉 Core：谁是 Driver、谁是 Driven、需要什么 Constraint。

当前公开方法
------------
基础校验：
    validate_node(node)
        检查 Maya 节点是否存在。

    normalize_nodes(nodes)
        将单节点 / 节点列表整理成保持原顺序的去重列表。

Constraint 创建：
    get_constraint_command(constraint_type)
        根据 Constraint Type 返回对应 maya.cmds 命令。

    create_constraint(driver_objects, driven_object,
                      constraint_type="parentConstraint",
                      maintain_offset=True, **kwargs)
        给一个 Driven 创建 Parent / Point / Orient / Scale / Aim Constraint。

    create_constraints(driver_objects, driven_objects,
                       constraint_type="parentConstraint",
                       maintain_offset=True, **kwargs)
        使用同一组 Driver 批量约束多个 Driven。

    create_pole_vector_constraint(driver_object, ik_handle)
        创建 Pole Vector Constraint。

Constraint 查询 / 删除：
    get_constraints(nodes, search_types=None)
        查询一个或多个对象关联的 Constraint 节点。

    delete_constraints(nodes, search_types=None)
        删除对象关联的 Constraint，并返回实际删除节点。

本模块不负责
------------
- offsetParentMatrix / multMatrix 约束网络；
- Controller Space Switch / Follow Blend 的完整业务；
- Selection 解释；
- UI；
- Constraint Weight 动画逻辑。

模块边界
--------
    Maya 原生 Constraint Node         -> constraint_utils
    Matrix / offsetParentMatrix 网络   -> matrix_utils
    Controller Follow / Parent Space   -> systems.controller

设计原则
--------
1. Core 接收明确参数，不从当前 Selection 猜 Driver / Driven；
2. 批量 API 复用单项 API，不复制 Constraint 创建逻辑；
3. 查询结果保持搜索顺序并去重；
4. 不静默吞掉输入错误，节点不存在时尽早报错；
5. poleVectorConstraint 因 Maya 命令签名不同，保留独立创建函数。
"""

from __future__ import print_function

import maya.cmds as cmds


# Maya 当前正式支持并允许查询的 Constraint 类型。
constraint_types = [
    "parentConstraint",
    "pointConstraint",
    "orientConstraint",
    "scaleConstraint",
    "aimConstraint",
    "poleVectorConstraint",
]


# =============================================================================
# Validate - 节点输入整理
# =============================================================================

def validate_node(node):
    u"""
    检查 Maya 节点是否存在。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool: 节点有效时返回 True。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：空名称直接报错。
    if not node:
        raise RuntimeError(u"节点名称不能为空。")

    # 步骤 2：确认 Scene 中真实存在节点。
    if not cmds.objExists(node):
        raise RuntimeError(
            u"Maya 节点不存在：{}".format(node)
        )

    return True


def normalize_nodes(nodes):
    u"""
    将单节点或节点列表整理成保持原顺序的去重列表。

    Args:
        nodes (str/list/None):
            输入节点。

    Returns:
        list: 校验通过并去重后的节点列表。
    """
    result = []

    # 步骤 1：None 统一转为空列表。
    if nodes is None:
        return result

    # 步骤 2：单个字符串转成 list，后续只维护一套循环。
    if isinstance(nodes, str):
        nodes = [nodes]

    # 步骤 3：逐节点校验并保持原顺序去重。
    for node in nodes:
        if not node:
            continue

        validate_node(node)

        if node in result:
            continue

        result.append(node)

    return result


# =============================================================================
# Create - Constraint 创建
# =============================================================================

def get_constraint_command(constraint_type):
    u"""
    根据 Constraint 类型返回对应的 ``maya.cmds`` 命令。

    poleVectorConstraint 不走这里，因为它的调用签名和标准 Constraint 不一致。

    Args:
        constraint_type (object):
            `constraint_type` 对应的输入数据。

    Returns:
        object:
            方法执行后的结果数据。

    Raises:
        ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：维护标准 Constraint Type -> Command 映射。
    command_map = {
        "parentConstraint": cmds.parentConstraint,
        "pointConstraint": cmds.pointConstraint,
        "orientConstraint": cmds.orientConstraint,
        "scaleConstraint": cmds.scaleConstraint,
        "aimConstraint": cmds.aimConstraint,
    }

    # 步骤 2：遇到未支持类型时明确报错。
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
        driver_objects (str/list):
            一个或多个 Driver。
        driven_object (str):
            Driven。
        constraint_type (str):
            parentConstraint / pointConstraint / orientConstraint / scaleConstraint / aimConstraint。
        maintain_offset (bool):
            是否保持创建前 Offset。
        kwargs (dict):
            继续传给 Maya Constraint 命令的其它参数。

    Returns:
        list: Maya 创建出来的 Constraint 节点列表。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：整理并验证 Driver。
    # -------------------------------------------------------------------------
    driver_objects = normalize_nodes(
        driver_objects
    )

    if not driver_objects:
        raise RuntimeError(u"至少需要一个 Driver。")

    # -------------------------------------------------------------------------
    # 步骤 2：验证 Driven。
    # -------------------------------------------------------------------------
    validate_node(driven_object)

    # -------------------------------------------------------------------------
    # 步骤 3：取得对应 Maya Constraint 命令。
    # -------------------------------------------------------------------------
    command = get_constraint_command(
        constraint_type
    )

    # -------------------------------------------------------------------------
    # 步骤 4：创建 Constraint。
    #
    # Maya 的 Constraint 命令支持一个 Driver List + 一个 Driven，
    # 所以这里直接保留多 Driver 能力，不需要上层自己循环 Driver。
    # -------------------------------------------------------------------------
    result = command(
        driver_objects,
        driven_object,
        maintainOffset=maintain_offset,
        **kwargs
    )

    # -------------------------------------------------------------------------
    # 步骤 5：统一返回 list。
    # -------------------------------------------------------------------------
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
        driver_objects (object):
            `driver_objects` 对应的输入数据。
        driven_objects (object):
            `driven_objects` 对应的输入数据。
        constraint_type (str):
            `constraint_type` 对应的名称、标记或字符串参数。
        maintain_offset (bool):
            是否在建立约束或矩阵关系时保持当前偏移。
        kwargs (dict):
            `kwargs` 对应的配置或映射字典。

    Returns:
        list: 所有创建出来的 Constraint 节点，保持创建顺序并去重。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：整理 Driver / Driven 输入。
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

    # 步骤 2：逐个 Driven 复用 create_constraint。
    for driven_object in driven_objects:
        result = create_constraint(
            driver_objects=driver_objects,
            driven_object=driven_object,
            constraint_type=constraint_type,
            maintain_offset=maintain_offset,
            **kwargs
        )

        # 步骤 3：收集并去重 Constraint 节点。
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
    u"""
    创建 Pole Vector Constraint。

    poleVectorConstraint 的第二个对象必须是 IK Handle，
    调用签名和标准 Parent / Point / Orient Constraint 不同，因此单独封装。

    Args:
        driver_object (object):
            `driver_object` 对应的输入数据。
        ik_handle (object):
            `ik_handle` 对应的输入数据。

    Returns:
        object | list:
            方法执行后的结果数据。
    """
    # 步骤 1：验证 Driver 和 IK Handle。
    validate_node(driver_object)
    validate_node(ik_handle)

    # 步骤 2：创建 Pole Vector Constraint。
    result = cmds.poleVectorConstraint(
        driver_object,
        ik_handle
    )

    # 步骤 3：统一返回 list。
    if result is None:
        return []

    return result


# =============================================================================
# Query - Constraint 查询
# =============================================================================

def get_constraints(
        nodes,
        search_types=None
):
    u"""
    获取一个或多个对象关联的 Constraint 节点。

    Args:
        nodes (str/list):
            要查询的 Maya 节点。
        search_types (list/None):
            None 时查询模块支持的全部 Constraint Type。

    Returns:
        list: 搜索顺序稳定、已去重的 Constraint 节点。
    """
    # 步骤 1：整理输入节点。
    nodes = normalize_nodes(nodes)

    # 步骤 2：准备要搜索的 Constraint Type。
    if search_types is None:
        search_types = constraint_types

    result = []

    # 步骤 3：逐节点、逐类型查询连接。
    for node in nodes:
        for constraint_type in search_types:
            connected_nodes = cmds.listConnections(
                node,
                type=constraint_type
            )

            if connected_nodes is None:
                connected_nodes = []

            # 步骤 4：保持搜索顺序去重。
            for connected_node in connected_nodes:
                if connected_node in result:
                    continue

                result.append(
                    connected_node
                )

    return result


# =============================================================================
# Delete - Constraint 删除
# =============================================================================

def delete_constraints(
        nodes,
        search_types=None
):
    u"""
    删除对象关联的 Constraint。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。
        search_types (object):
            `search_types` 对应的输入数据。

    Returns:
        list: 实际删除的 Constraint 节点名称。
    """
    # 步骤 1：先统一查询目标 Constraint。
    constraint_nodes = get_constraints(
        nodes=nodes,
        search_types=search_types
    )

    deleted_nodes = []

    # 步骤 2：逐节点确认仍存在，然后删除。
    for constraint_node in constraint_nodes:
        if not cmds.objExists(constraint_node):
            continue

        deleted_nodes.append(
            constraint_node
        )

        cmds.delete(
            constraint_node
        )

    # 步骤 3：返回实际删除记录。
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
