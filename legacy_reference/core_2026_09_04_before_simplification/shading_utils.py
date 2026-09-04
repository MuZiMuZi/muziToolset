# coding=utf-8
u"""
Shading Utils
=============

Maya Shading Group 锁状态相关的通用底层工具。

职责：
    1. 查询 Maya Node 的 lock / lockUnpublished 状态；
    2. 查询包含指定 Node 的 Container 链；
    3. 临时解除 Node 与 Container 链的锁定；
    4. 操作完成后严格恢复调用前锁状态；
    5. 为 Maya 默认 initialShadingGroup 提供明确包装 API。

使用场景：
    Maya 的 loft 等建模命令在创建 Shape 时可能自动把新 Shape 加入
    initialShadingGroup。当默认 Shading Group 或其 Container 被锁定时，
    Maya 会因为无法写入 dagSetMembers 而让建模命令失败。

设计边界：
    - 本模块不创建材质；
    - 本模块不修改 Shader Assignment 业务关系；
    - 临时解锁后必须恢复原始状态；
    - 不依赖 Selection；
    - 不包含 UI。
"""

from __future__ import print_function

import maya.cmds as cmds


DEFAULT_SHADING_GROUP = ":initialShadingGroup"


def get_node_lock_state(node):
    u"""
    读取 Maya Node 的普通锁和 unpublished lock 状态。

    Args:
        node (str):
            需要查询的 Maya Node。

    Returns:
        dict:
            包含 node、locked、lock_unpublished 的状态字典。

    Raises:
        RuntimeError:
            Node 不存在时抛出。
    """
    if not node:
        raise RuntimeError(
            u"Shading Lock Node 不能为空。"
        )

    if not cmds.objExists(node):
        raise RuntimeError(
            u"Shading Lock Node 不存在：{}".format(
                node
            )
        )

    node_lock_state = cmds.lockNode(
        node,
        query=True,
        lock=True
    )
    unpublished_lock_state = cmds.lockNode(
        node,
        query=True,
        lockUnpublished=True
    )

    locked = False
    lock_unpublished = False

    if node_lock_state:
        locked = bool(
            node_lock_state[0]
        )

    if unpublished_lock_state:
        lock_unpublished = bool(
            unpublished_lock_state[0]
        )

    return {
        "node": node,
        "locked": locked,
        "lock_unpublished": lock_unpublished,
    }


def get_container_chain(node):
    u"""
    返回包含指定 Node 的 Container 链，顺序为最外层到最内层。

    Args:
        node (str):
            需要查询 Container 所属关系的 Maya Node。

    Returns:
        list[str]:
            Container 名称列表；没有 Container 时返回空列表。
    """
    if not node:
        return []

    if not cmds.objExists(node):
        return []

    container_chain = []
    visited_containers = []

    try:
        current_container = cmds.container(
            query=True,
            findContainer=node
        )
    except Exception:
        current_container = ""

    while current_container:
        if current_container in visited_containers:
            break

        visited_containers.append(
            current_container
        )
        container_chain.append(
            current_container
        )

        try:
            parent_container = cmds.container(
                current_container,
                query=True,
                parentContainer=True
            )
        except Exception:
            parent_container = ""

        current_container = parent_container or ""

    container_chain.reverse()
    return container_chain


def restore_node_lock_state(state):
    u"""
    恢复 unlock_node_with_containers() 保存的完整锁状态。

    恢复顺序：
        1. Node；
        2. Container 从最内层到最外层。

    Args:
        state (dict):
            unlock_node_with_containers() 返回的状态。

    Returns:
        bool:
            成功恢复或无需恢复时返回 True。
    """
    if not state:
        return True

    if not state.get(
            "exists",
            False
    ):
        return True

    node_state = state.get(
        "node_state"
    )

    if node_state:
        node = node_state.get(
            "node"
        )

        if node:
            if cmds.objExists(node):
                cmds.lockNode(
                    node,
                    lock=node_state.get(
                        "locked",
                        False
                    ),
                    lockUnpublished=node_state.get(
                        "lock_unpublished",
                        False
                    )
                )

    container_states = state.get(
        "container_states",
        []
    )
    container_index = len(container_states) - 1

    while container_index >= 0:
        container_state = container_states[container_index]
        container_node = container_state.get(
            "node"
        )

        if container_node:
            if cmds.objExists(container_node):
                cmds.lockNode(
                    container_node,
                    lock=container_state.get(
                        "locked",
                        False
                    ),
                    lockUnpublished=container_state.get(
                        "lock_unpublished",
                        False
                    )
                )

        container_index -= 1

    return True


def unlock_node_with_containers(node):
    u"""
    保存并临时解除指定 Node 与其 Container 链的锁状态。

    Container 必须从最外层到最内层依次解锁，最后再解锁目标 Node。
    若解锁过程中发生异常，会尝试恢复已经记录的原始状态后继续抛出。

    Args:
        node (str):
            需要临时解锁的 Maya Node。

    Returns:
        dict:
            可传给 restore_node_lock_state() 的完整原始状态。
    """
    state = {
        "exists": False,
        "node_state": None,
        "container_states": [],
    }

    if not node:
        return state

    if not cmds.objExists(node):
        return state

    state["exists"] = True

    container_chain = get_container_chain(
        node
    )

    for container_node in container_chain:
        container_state = get_node_lock_state(
            container_node
        )
        state["container_states"].append(
            container_state
        )

    state["node_state"] = get_node_lock_state(
        node
    )

    try:
        for container_state in state["container_states"]:
            cmds.lockNode(
                container_state["node"],
                lock=False,
                lockUnpublished=False
            )

        cmds.lockNode(
            node,
            lock=False,
            lockUnpublished=False
        )
    except Exception:
        try:
            restore_node_lock_state(
                state
            )
        except Exception:
            pass

        raise

    return state


def unlock_default_shading_group():
    u"""
    临时解除 Maya 默认 initialShadingGroup 与 Container 链的锁定。

    Returns:
        dict:
            后续用于恢复原状态的锁状态字典。
    """
    return unlock_node_with_containers(
        DEFAULT_SHADING_GROUP
    )


def restore_default_shading_group(state):
    u"""
    恢复 unlock_default_shading_group() 保存的默认 Shading Group 锁状态。

    Args:
        state (dict):
            unlock_default_shading_group() 返回的状态字典。

    Returns:
        bool:
            成功恢复或无需恢复时返回 True。
    """
    return restore_node_lock_state(
        state
    )


__all__ = [
    "DEFAULT_SHADING_GROUP",
    "get_node_lock_state",
    "get_container_chain",
    "unlock_node_with_containers",
    "restore_node_lock_state",
    "unlock_default_shading_group",
    "restore_default_shading_group",
]
