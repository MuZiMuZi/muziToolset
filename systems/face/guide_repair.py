# coding=utf-8
u"""
Face Guide Repair
=================

Face Guide Template 修复 / 重新导入模块。

职责：
    1. 重新导入模板前记录当前仍然存在的 Guide Locator 世界矩阵；
    2. 记录 Face Move Controller 世界矩阵；
    3. 删除当前可能已经损坏的 Guide 内容；
    4. 重新导入干净的 resources/face/face_guide.ma；
    5. 按标准节点名称恢复原来仍然存在的 Locator 位置；
    6. 原场景中已经缺失的 Locator 使用模板默认位置。

设计原则：
    - 这是 Repair，不是 Reset；
    - 不尝试猜测已经被删除 Locator 的旧位置；
    - 匹配依据只使用标准 Rig Short Name；
    - World Matrix 查询 / 写入统一复用 core.transform_utils；
    - 整个 Repair 作为一次 Maya Undo Chunk 执行。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import rename_utils
from ...core import scene_utils
from ...core import transform_utils
from . import guide_template


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
# Query
# =============================================================================

def get_existing_guide_locators(face_guide):
    u"""返回当前 Face Guide 层级中仍然存在的全部 Locator Transform。"""
    if not cmds.objExists(
            face_guide.face_guide_grp
    ):
        return []

    descendants = cmds.listRelatives(
        face_guide.face_guide_grp,
        allDescendents=True,
        type="transform",
        fullPath=True
    )

    if descendants is None:
        descendants = []

    locators = []

    for node in descendants:
        locator_shapes = face_guide.get_locator_shapes(
            node
        )

        if not locator_shapes:
            continue

        locators.append(
            node
        )

    return locators


def capture_guide_state(face_guide):
    u"""
    记录当前仍然存在的 Guide Locator 和 Move Controller 世界矩阵。

    Returns:
        dict:
            move_ctrl_matrix、locators。
    """
    state = {
        "move_ctrl_matrix": None,
        "locators": {},
    }

    face_guide.refresh_guide_handles()

    if face_guide.guide_move_ctrl:
        if cmds.objExists(
                face_guide.guide_move_ctrl
        ):
            state["move_ctrl_matrix"] = transform_utils.get_world_matrix(
                face_guide.guide_move_ctrl
            )

    locators = get_existing_guide_locators(
        face_guide
    )

    for locator in locators:
        short_name = rename_utils.get_short_name(
            locator
        )

        state["locators"][short_name] = transform_utils.get_world_matrix(
            locator
        )

    return state


# =============================================================================
# Restore
# =============================================================================

def set_world_matrix_preserve_lock(
        node,
        matrix_values
):
    u"""临时解锁 Transform Channel，写入 World Matrix 后恢复原 Lock 状态。"""
    lock_states = {}

    for attribute in transform_attributes:
        plug = "{}.{}".format(
            node,
            attribute
        )

        if not cmds.objExists(
                plug
        ):
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

            if not cmds.objExists(
                    plug
            ):
                continue

            cmds.setAttr(
                plug,
                lock=lock_states[attribute]
            )

    return node


def restore_guide_state(
        face_guide,
        state
):
    u"""
    把重新导入后的同名 Locator 恢复到 Repair 前的世界矩阵。

    原场景缺失的 Locator 没有快照，因此保持模板默认位置。
    """
    if not isinstance(state, dict):
        raise TypeError(
            u"Guide Repair State 必须是 dict。"
        )

    restored_locators = []
    missing_locators = []

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
            missing_locators.append(
                short_name
            )
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
        "missing_count": len(missing_locators),
        "restored_locators": restored_locators,
        "missing_locators": missing_locators,
    }


# =============================================================================
# Repair
# =============================================================================

@scene_utils.undo_chunk
def reimport_template_preserve_guide(face_guide):
    u"""
    重新导入 Face Guide Template，并尽可能保留当前已有 Locator 位置。

    整个过程作为一次 Maya Undo Chunk，因此也可以直接 Ctrl + Z 回退。
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

    # 删除旧 Template 内容。FaceBase 主 Guide Container / Config 由现有系统负责维护。
    face_guide.remove_guide()

    # 导入一份完整、干净的 Template。
    build_result = guide_template.build_guide(
        face_guide
    )

    # 先恢复 Move Ctrl，再恢复各 Locator 的 World Matrix。
    restore_result = restore_guide_state(
        face_guide,
        state
    )

    # Repair 后必须重新提交 Step 02，后续旧 Build 同步失效。
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
        "missing_count": restore_result.get(
            "missing_count",
            0
        ),
        "build_result": build_result,
        "restore_result": restore_result,
    }


__all__ = [
    "transform_attributes",
    "get_existing_guide_locators",
    "capture_guide_state",
    "set_world_matrix_preserve_lock",
    "restore_guide_state",
    "reimport_template_preserve_guide",
]
