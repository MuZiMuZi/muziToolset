# coding=utf-8
u"""一次性修复 Face Modules Runtime Smoke 的默认 Shading Group 隔离。"""

from __future__ import print_function

import os


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


RUNNER_PATH = os.path.join(
    REPO_ROOT,
    "tests",
    "face_modules_maya2023_smoke_test.py"
)

CONTRACT_PATH = os.path.join(
    REPO_ROOT,
    "tests",
    "face_modules_maya2023_smoke_contract_test.py"
)


SHADING_HELPERS = r'''

DEFAULT_SHADING_GROUP = ":initialShadingGroup"


def prepare_default_shading_group():
    u"""
    临时解除默认 Shading Group 的写入锁，避免 Smoke 创建几何体时受用户场景状态影响。

    Returns:
        dict:
            默认 Shading Group 原始 Node Lock 与 dagSetMembers Lock 状态。
    """
    # -------------------------------------------------------------------------
    # Step 01：记录当前默认 Shading Group 的原始状态
    # -------------------------------------------------------------------------
    state = {
        "exists": False,
        "node_locked": False,
        "dag_set_members_locked": False,
    }

    if not cmds.objExists(DEFAULT_SHADING_GROUP):
        return state

    state["exists"] = True

    node_lock_state = cmds.lockNode(
        DEFAULT_SHADING_GROUP,
        query=True,
        lock=True
    )

    if node_lock_state:
        state["node_locked"] = bool(
            node_lock_state[0]
        )

    dag_members_plug = DEFAULT_SHADING_GROUP + ".dagSetMembers"

    try:
        state["dag_set_members_locked"] = bool(
            cmds.getAttr(
                dag_members_plug,
                lock=True
            )
        )
    except Exception:
        state["dag_set_members_locked"] = False

    # -------------------------------------------------------------------------
    # Step 02：只在测试期间解除阻止 Geometry / Surface 加入材质集的锁
    # -------------------------------------------------------------------------
    if state["node_locked"]:
        cmds.lockNode(
            DEFAULT_SHADING_GROUP,
            lock=False
        )

    if state["dag_set_members_locked"]:
        cmds.setAttr(
            dag_members_plug,
            lock=False
        )

    return state


def restore_default_shading_group(state):
    u"""
    恢复 Runtime Smoke 运行前的默认 Shading Group 锁定状态。

    Args:
        state (dict):
            prepare_default_shading_group() 保存的原始状态。

    Returns:
        bool:
            成功恢复或无需恢复时返回 True。
    """
    # -------------------------------------------------------------------------
    # Step 01：确认测试前确实存在默认 Shading Group
    # -------------------------------------------------------------------------
    if not state:
        return True

    if not state.get("exists"):
        return True

    if not cmds.objExists(DEFAULT_SHADING_GROUP):
        return True

    dag_members_plug = DEFAULT_SHADING_GROUP + ".dagSetMembers"

    # -------------------------------------------------------------------------
    # Step 02：先恢复 Attribute Lock，再恢复 Node Lock
    # -------------------------------------------------------------------------
    if state.get("dag_set_members_locked"):
        cmds.setAttr(
            dag_members_plug,
            lock=True
        )

    if state.get("node_locked"):
        cmds.lockNode(
            DEFAULT_SHADING_GROUP,
            lock=True
        )

    return True
'''


def read_text(path):
    with open(path, "r", encoding="utf-8") as file_object:
        return file_object.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as file_object:
        file_object.write(text)


def patch_runner():
    source = read_text(RUNNER_PATH)

    if "def prepare_default_shading_group():" not in source:
        anchor = "\n\ndef create_fixture_models():"

        if anchor not in source:
            raise RuntimeError("Runner helper insertion anchor not found.")

        source = source.replace(
            anchor,
            SHADING_HELPERS + anchor,
            1
        )

    old_setup = """    maya_version = require_maya_2023()\n    namespace = create_namespace()\n    fixture_dict = None\n"""
    new_setup = """    maya_version = require_maya_2023()\n    namespace = create_namespace()\n    shading_group_state = prepare_default_shading_group()\n    fixture_dict = None\n"""

    if "shading_group_state = prepare_default_shading_group()" not in source:
        if old_setup not in source:
            raise RuntimeError("Runner setup anchor not found.")

        source = source.replace(
            old_setup,
            new_setup,
            1
        )

    old_cleanup = """        remove_namespace(\n            namespace\n        )\n"""
    new_cleanup = """        remove_namespace(\n            namespace\n        )\n        restore_default_shading_group(\n            shading_group_state\n        )\n"""

    if "restore_default_shading_group(\n            shading_group_state" not in source:
        if old_cleanup not in source:
            raise RuntimeError("Runner cleanup anchor not found.")

        source = source.replace(
            old_cleanup,
            new_cleanup,
            1
        )

    write_text(
        RUNNER_PATH,
        source
    )


def patch_contract():
    source = read_text(CONTRACT_PATH)

    old_functions = """REQUIRED_FUNCTIONS = {\n    \"create_fixture_models\",\n"""
    new_functions = """REQUIRED_FUNCTIONS = {\n    \"prepare_default_shading_group\",\n    \"restore_default_shading_group\",\n    \"create_fixture_models\",\n"""

    if '"prepare_default_shading_group"' not in source:
        if old_functions not in source:
            raise RuntimeError("Contract function anchor not found.")

        source = source.replace(
            old_functions,
            new_functions,
            1
        )

    old_required = """        \"mouth_jnt_number=32\",\n"""
    new_required = """        \"mouth_jnt_number=32\",\n        \"DEFAULT_SHADING_GROUP = \\\":initialShadingGroup\\\"\",\n        \"prepare_default_shading_group()\",\n        \"restore_default_shading_group(\",\n"""

    if 'DEFAULT_SHADING_GROUP = \\":initialShadingGroup\\"' not in source:
        if old_required not in source:
            raise RuntimeError("Contract required-text anchor not found.")

        source = source.replace(
            old_required,
            new_required,
            1
        )

    write_text(
        CONTRACT_PATH,
        source
    )


def main():
    patch_runner()
    patch_contract()
    print("Face smoke default Shading Group isolation patch: DONE")


if __name__ == "__main__":
    main()
