# coding=utf-8
from __future__ import print_function

import os


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SMOKE_PATH = os.path.join(ROOT, "tests", "face_modules_maya2023_smoke_test.py")


def main():
    with open(SMOKE_PATH, "r", encoding="utf-8") as file_object:
        source = file_object.read()

    start_marker = 'DEFAULT_SHADING_GROUP = ":initialShadingGroup"\n'
    end_marker = '\ndef create_fixture_models():'

    start_index = source.index(start_marker)
    end_index = source.index(end_marker, start_index)

    replacement = r'''DEFAULT_SHADING_GROUP = ":initialShadingGroup"


def _query_lock_state(node):
    u"""读取 Maya Node 的普通锁与未发布属性锁状态。"""
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

    return {
        "node": node,
        "locked": bool(node_lock_state[0]) if node_lock_state else False,
        "lock_unpublished": bool(unpublished_lock_state[0]) if unpublished_lock_state else False,
    }


def _get_container_chain(node):
    u"""返回包含指定 Node 的 Container 链，顺序为最外层到最内层。"""
    container_chain = []
    visited = set()

    try:
        current_container = cmds.container(
            query=True,
            findContainer=node
        )
    except Exception:
        current_container = ""

    while current_container:
        if current_container in visited:
            break

        visited.add(
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


def prepare_default_shading_group():
    u"""
    临时解除默认 Shading Group 及其 Container 链的 unpublished lock。

    Returns:
        dict:
            initialShadingGroup 与 Container 链的原始锁状态。
    """
    state = {
        "exists": False,
        "node_state": None,
        "container_states": [],
    }

    if not cmds.objExists(DEFAULT_SHADING_GROUP):
        return state

    state["exists"] = True

    # -------------------------------------------------------------------------
    # Step 01：先记录 Container 链状态；外层 Container 必须最先解除锁定
    # -------------------------------------------------------------------------
    container_chain = _get_container_chain(
        DEFAULT_SHADING_GROUP
    )

    for container_node in container_chain:
        container_state = _query_lock_state(
            container_node
        )
        state["container_states"].append(
            container_state
        )

    state["node_state"] = _query_lock_state(
        DEFAULT_SHADING_GROUP
    )

    # -------------------------------------------------------------------------
    # Step 02：从最外层到最内层解除 Container 的普通锁与 unpublished lock
    # -------------------------------------------------------------------------
    for container_state in state["container_states"]:
        cmds.lockNode(
            container_state["node"],
            lock=False,
            lockUnpublished=False
        )

    # -------------------------------------------------------------------------
    # Step 03：最后解除 initialShadingGroup 自身 unpublished lock
    # 不再直接 setAttr(..., lock=False)，避免 locked-container unpublished 错误。
    # -------------------------------------------------------------------------
    cmds.lockNode(
        DEFAULT_SHADING_GROUP,
        lock=False,
        lockUnpublished=False
    )

    return state


def restore_default_shading_group(state):
    u"""
    恢复 Runtime Smoke 运行前的默认 Shading Group 与 Container 锁状态。

    Args:
        state (dict):
            prepare_default_shading_group() 保存的原始状态。

    Returns:
        bool:
            成功恢复或无需恢复时返回 True。
    """
    if not state:
        return True

    if not state.get("exists"):
        return True

    if not cmds.objExists(DEFAULT_SHADING_GROUP):
        return True

    # -------------------------------------------------------------------------
    # Step 01：Container 仍保持解锁时，先恢复 initialShadingGroup 自身状态
    # -------------------------------------------------------------------------
    node_state = state.get("node_state")

    if node_state:
        cmds.lockNode(
            DEFAULT_SHADING_GROUP,
            lock=node_state.get("locked", False),
            lockUnpublished=node_state.get("lock_unpublished", False)
        )

    # -------------------------------------------------------------------------
    # Step 02：从最内层到最外层恢复 Container，避免父 Container 提前锁死子级
    # -------------------------------------------------------------------------
    container_states = state.get(
        "container_states",
        []
    )

    container_index = len(container_states) - 1

    while container_index >= 0:
        container_state = container_states[container_index]
        container_node = container_state["node"]

        if cmds.objExists(container_node):
            cmds.lockNode(
                container_node,
                lock=container_state.get("locked", False),
                lockUnpublished=container_state.get("lock_unpublished", False)
            )

        container_index -= 1

    return True
'''

    source = source[:start_index] + replacement + source[end_index:]

    with open(SMOKE_PATH, "w", encoding="utf-8", newline="\n") as file_object:
        file_object.write(source)


if __name__ == "__main__":
    main()
