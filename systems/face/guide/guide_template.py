# coding=utf-8
u"""
Face Guide Template
===================

Step 02 Face Guide Template 的导入、重置和修复模块。

职责：
    1. 导入 resources/face/face_guide.ma；
    2. 解决 Step 01 空 Guide Group 与模板 Root 同名冲突；
    3. 重新导入模板时保留当前仍存在 Locator 的世界位置；
    4. 被误删的 Locator 使用模板默认位置自动补回；
    5. Import / Reset / Reimport 均保持 Step 状态和 Config 一致。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import hierarchy_utils
from ....core import rename_utils
from ....core import scene_utils
from ....core import transform_utils
from . import guide_data
from . import guide_mirror


temporary_guide_container_name = "grp_md_face_guide_container_001"

transform_attributes = [
    "translateX",
    "translateY",
    "translateZ",
    "rotateX",
    "rotateY",
    "rotateZ",
    "scaleX",
    "scaleY",
    "scaleZ",
]


# =============================================================================
# Helper
# =============================================================================

def get_children(node):
    u"""返回一个 DAG 节点的全部直接 Child。"""
    if not node:
        return []

    if not cmds.objExists(node):
        return []

    children = cmds.listRelatives(
        node,
        children=True,
        fullPath=True
    )

    if children is None:
        children = []

    return children


def get_available_temporary_name():
    u"""返回场景中未被占用的临时 Guide Container 名称。"""
    if not cmds.objExists(
            temporary_guide_container_name
    ):
        return temporary_guide_container_name

    index = 2

    while True:
        candidate = "grp_md_face_guide_container_{:03d}".format(
            index
        )

        if not cmds.objExists(candidate):
            return candidate

        index += 1


def get_imported_template_root(imported_nodes):
    u"""从本次 Import 新节点中找到唯一 Face Guide Template Root。"""
    imported_transforms = cmds.ls(
        imported_nodes,
        type="transform",
        long=True
    )

    if imported_transforms is None:
        imported_transforms = []

    candidates = []

    for node in imported_transforms:
        parent = hierarchy_utils.Hierarchy.get_parent(
            node
        )

        if parent:
            continue

        short_name = rename_utils.get_short_name(
            node
        )

        if short_name != guide_data.guide_root_name:
            continue

        candidates.append(
            node
        )

    if len(candidates) != 1:
        raise RuntimeError(
            u"无法唯一识别 Face Guide Template Root，候选数量: {}".format(
                len(candidates)
            )
        )

    return candidates[0]


def set_world_matrix_preserve_lock(
        node,
        matrix_values
):
    u"""临时解锁 Transform Channel，写入 World Matrix 后恢复 Lock。"""
    lock_states = {}

    for attribute in transform_attributes:
        plug = "{}.{}".format(
            node,
            attribute
        )

        if not cmds.objExists(plug):
            continue

        lock_states[attribute] = bool(
            cmds.getAttr(
                plug,
                lock=True
            )
        )

        if lock_states[attribute]:
            cmds.setAttr(
                plug,
                lock=False
            )

    try:
        transform_utils.set_world_matrix(
            node,
            matrix_values
        )
    finally:
        for attribute in lock_states:
            plug = "{}.{}".format(
                node,
                attribute
            )

            if not cmds.objExists(plug):
                continue

            cmds.setAttr(
                plug,
                lock=lock_states[attribute]
            )

    return node


# =============================================================================
# State
# =============================================================================

def capture_guide_state(face_guide):
    u"""记录当前仍存在的 Move Ctrl 和 Guide Locator 世界矩阵。"""
    state = {
        "move_ctrl_matrix": None,
        "locators": {},
    }

    face_guide.refresh_guide_handles()

    if face_guide.guide_move_ctrl:
        if cmds.objExists(face_guide.guide_move_ctrl):
            state["move_ctrl_matrix"] = transform_utils.get_world_matrix(
                face_guide.guide_move_ctrl
            )

    locators = face_guide.get_guide_locators()

    for locator in locators:
        short_name = rename_utils.get_short_name(
            locator
        )
        state["locators"][short_name] = transform_utils.get_world_matrix(
            locator
        )

    return state


def restore_guide_state(
        face_guide,
        state
):
    u"""
    恢复重新导入前仍存在的 Locator 位置。

    原来已经被误删的 Locator 没有 Snapshot，因此保持新模板默认位置。
    """
    if not isinstance(state, dict):
        raise TypeError(
            u"Guide State 必须是 dict。"
        )

    restored_locators = []

    face_guide.refresh_guide_handles()

    move_ctrl_matrix = state.get(
        "move_ctrl_matrix"
    )

    if move_ctrl_matrix:
        if face_guide.guide_move_ctrl:
            set_world_matrix_preserve_lock(
                face_guide.guide_move_ctrl,
                move_ctrl_matrix
            )

    locator_states = state.get(
        "locators",
        {}
    )

    for short_name in locator_states:
        locator = face_guide.get_guide_node(
            short_name,
            required=False
        )

        if not locator:
            continue

        set_world_matrix_preserve_lock(
            locator,
            locator_states[short_name]
        )
        restored_locators.append(
            locator
        )

    return {
        "restored_count": len(restored_locators),
        "restored_locators": restored_locators,
    }


# =============================================================================
# Remove / Build
# =============================================================================

def clear_guide_config(face_guide):
    u"""清除 Config 中保存的 Guide Message 引用。"""
    if not face_guide.config_node_exists():
        return False

    face_guide.set_config_messages(
        attrs_dict={
            "face_guide_root": None,
            "face_guide_move_ctrl": None,
        },
        force=True,
        clear_empty=True
    )

    return True


def remove_template_content(face_guide):
    u"""删除正式 Face Guide Root 下的 Template 内容，但保留 Root Container。"""
    if not cmds.objExists(face_guide.face_guide_grp):
        face_guide.ensure_hierarchy()

    children = get_children(
        face_guide.face_guide_grp
    )

    for child in children:
        if not cmds.objExists(child):
            continue

        cmds.delete(
            child
        )

    clear_guide_config(
        face_guide
    )
    face_guide.refresh_guide_handles()

    if face_guide.config_node_exists():
        face_guide.set_step_completed(
            completed=False
        )
        face_guide.invalidate_later_steps()

    return True


def build_guide(face_guide):
    u"""导入或复用可编辑的 Face Guide Template。"""
    face_guide.validate_setup()
    face_guide.ensure_hierarchy()
    face_guide.ensure_config_node()

    if face_guide.guide_exists():
        return {
            "imported": False,
            "guide_root": face_guide.guide_root,
            "guide_move_ctrl": face_guide.guide_move_ctrl,
            "new_nodes": [],
        }

    guide_container = scene_utils.get_long_name(
        face_guide.face_guide_grp
    )
    container_children = get_children(
        guide_container
    )

    if container_children:
        raise RuntimeError(
            u"Face Guide Group 中存在未知内容，无法安全自动导入模板：{}".format(
                face_guide.face_guide_grp
            )
        )

    template_path = guide_data.validate_guide_template_file()
    temporary_name = get_available_temporary_name()
    temporary_container = rename_utils.rename_node(
        guide_container,
        temporary_name
    )

    imported_nodes = []
    template_root = None

    try:
        imported_nodes = scene_utils.import_scene(
            template_path,
            ignore_version=True
        )
        template_root = get_imported_template_root(
            imported_nodes
        )
        template_root = hierarchy_utils.Hierarchy.parent(
            template_root,
            face_guide.face_master_grp
        )

        if temporary_container:
            if cmds.objExists(temporary_container):
                cmds.delete(
                    temporary_container
                )

    except Exception:
        for imported_node in imported_nodes:
            if not cmds.objExists(imported_node):
                continue

            try:
                cmds.delete(
                    imported_node
                )
            except Exception:
                pass

        if temporary_container:
            if cmds.objExists(temporary_container):
                rename_utils.rename_node(
                    temporary_container,
                    face_guide.face_guide_grp
                )

        raise

    face_guide.refresh_guide_handles()

    if not face_guide.guide_exists():
        raise RuntimeError(
            u"Face Guide 模板导入完成，但没有找到 {}。".format(
                guide_data.guide_move_ctrl_name
            )
        )

    # 模板保留了旧版左右连接。导入后复制一次 LF 状态到 RT，并断开 Target 输入。
    guide_mirror.apply_mirror(
        face_guide,
        source_side="lf",
        target_side="rt"
    )

    face_guide.save_guide_config()
    face_guide.set_step_completed(
        completed=False
    )
    face_guide.invalidate_later_steps()

    return {
        "imported": True,
        "guide_root": face_guide.guide_root,
        "guide_move_ctrl": face_guide.guide_move_ctrl,
        "new_nodes": imported_nodes,
    }


@scene_utils.undo_chunk
def reset_template(face_guide):
    u"""删除当前调整并恢复一份干净 Guide Template。"""
    remove_template_content(
        face_guide
    )
    return build_guide(
        face_guide
    )


@scene_utils.undo_chunk
def reimport_template_preserve_guide(face_guide):
    u"""
    重新导入完整模板，并保留当前仍存在 Locator 的世界位置。

    用于绑定师误删 Locator 后修复当前 Guide。
    """
    face_guide.validate_setup()

    state = capture_guide_state(
        face_guide
    )
    saved_locator_count = len(
        state.get(
            "locators",
            {}
        )
    )

    remove_template_content(
        face_guide
    )
    build_result = build_guide(
        face_guide
    )
    restore_result = restore_guide_state(
        face_guide,
        state
    )

    face_guide.set_step_completed(
        completed=False
    )
    face_guide.invalidate_later_steps()
    face_guide.save_guide_config()

    return {
        "saved_locator_count": saved_locator_count,
        "restored_count": restore_result.get(
            "restored_count",
            0
        ),
        "template_locator_count": len(
            guide_data.get_template_locator_names()
        ),
        "build_result": build_result,
        "restore_result": restore_result,
    }


__all__ = [
    "build_guide",
    "reset_template",
    "reimport_template_preserve_guide",
    "capture_guide_state",
    "restore_guide_state",
]
