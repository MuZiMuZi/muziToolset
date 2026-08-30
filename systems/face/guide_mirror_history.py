# coding=utf-8
u"""
Face Guide Mirror History
=========================

Guide Mirror 的单步历史 / 撤销支持。

职责：
    1. 镜像前记录 Target Side 当前 Zero / Locator 状态；
    2. 执行现有 guide_mirror.mirror_guides()；
    3. 允许 UI 独立恢复“上一次镜像前”的 Target Side；
    4. Mirror / Restore 都作为一次 Maya Undo Chunk 执行。

为什么不只调用 cmds.undo()
-------------------------
用户镜像后可能继续拖动其它 Guide。此时直接 cmds.undo() 会先撤销最近一次拖动，
并不能保证回到“镜像前”。因此 UI 的“撤销上次镜像”使用显式 Snapshot 恢复；
同时 Mirror 本身仍然进入 Maya Undo Queue，Ctrl + Z 也可以正常使用。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import connection_utils
from ...core import hierarchy_utils
from ...core import rename_utils
from ...core import scene_utils
from . import guide_mirror


zero_attributes = list(
    guide_mirror.transform_attributes
)
zero_attributes.append(
    "rotateOrder"
)

locator_attributes = list(
    guide_mirror.locator_attributes
)

locator_shape_attributes = list(
    guide_mirror.locator_shape_attributes
)


# =============================================================================
# Attribute State
# =============================================================================

def capture_attributes(
        node,
        attributes
):
    u"""记录节点指定 Attribute 的当前值。"""
    values = {}

    if not node:
        return values

    if not cmds.objExists(node):
        return values

    for attribute in attributes:
        plug = "{}.{}".format(
            node,
            attribute
        )

        if not cmds.objExists(
                plug
        ):
            continue

        values[attribute] = cmds.getAttr(
            plug
        )

    return values


def restore_attributes(
        face_guide,
        node,
        values
):
    u"""恢复节点 Attribute，并保证恢复后仍可独立编辑。"""
    if not node:
        return False

    if not cmds.objExists(node):
        return False

    if not isinstance(values, dict):
        return False

    for attribute in values:
        plug = "{}.{}".format(
            node,
            attribute
        )

        if not cmds.objExists(
                plug
        ):
            continue

        connection_utils.disconnect_input(
            plug
        )

        face_guide.set_attr_preserve_lock(
            node,
            attribute,
            values[attribute]
        )

    return True


# =============================================================================
# Snapshot
# =============================================================================

def capture_side_state(
        face_guide,
        side
):
    u"""记录指定 Side 在镜像前的 Zero / Locator 状态。"""
    if side not in guide_mirror.valid_sides:
        raise ValueError(
            u"side 必须是 lf 或 rt。"
        )

    snapshot = {
        "side": side,
        "zero_names": [],
        "items": [],
    }

    zero_groups = guide_mirror.get_side_zero_groups(
        face_guide,
        side
    )

    for zero_group in zero_groups:
        zero_name = rename_utils.get_short_name(
            zero_group
        )

        snapshot["zero_names"].append(
            zero_name
        )

        locator = guide_mirror.get_side_locator(
            zero_group,
            side
        )

        locator_name = None
        locator_values = {}
        locator_shape_name = None
        locator_shape_values = {}

        if locator:
            locator_name = rename_utils.get_short_name(
                locator
            )
            locator_values = capture_attributes(
                locator,
                locator_attributes
            )

            locator_shapes = face_guide.get_locator_shapes(
                locator
            )

            if locator_shapes:
                locator_shape = locator_shapes[0]
                locator_shape_name = rename_utils.get_short_name(
                    locator_shape
                )
                locator_shape_values = capture_attributes(
                    locator_shape,
                    locator_shape_attributes
                )

        snapshot["items"].append(
            {
                "zero_name": zero_name,
                "zero_values": capture_attributes(
                    zero_group,
                    zero_attributes
                ),
                "locator_name": locator_name,
                "locator_values": locator_values,
                "locator_shape_name": locator_shape_name,
                "locator_shape_values": locator_shape_values,
            }
        )

    return snapshot


# =============================================================================
# Restore
# =============================================================================

def remove_new_target_nodes(
        face_guide,
        snapshot
):
    u"""删除镜像过程中新增、但 Snapshot 中原本不存在的 Target Zero。"""
    side = snapshot.get(
        "side"
    )
    original_zero_names = snapshot.get(
        "zero_names",
        []
    )

    current_zero_groups = guide_mirror.get_side_zero_groups(
        face_guide,
        side
    )

    current_zero_groups.sort(
        key=hierarchy_utils.Hierarchy.get_dag_depth,
        reverse=True
    )

    for zero_group in current_zero_groups:
        zero_name = rename_utils.get_short_name(
            zero_group
        )

        if zero_name in original_zero_names:
            continue

        if cmds.objExists(
                zero_group
        ):
            cmds.delete(
                zero_group
            )

    return True


def restore_snapshot(
        face_guide,
        snapshot
):
    u"""恢复 Target Side 到最近一次 Mirror 之前的状态。"""
    if not isinstance(snapshot, dict):
        raise TypeError(
            u"Mirror Snapshot 必须是 dict。"
        )

    side = snapshot.get(
        "side"
    )

    if side not in guide_mirror.valid_sides:
        raise ValueError(
            u"Mirror Snapshot 缺少有效 Side。"
        )

    remove_new_target_nodes(
        face_guide,
        snapshot
    )

    items = snapshot.get(
        "items",
        []
    )

    restored_count = 0

    for item in items:
        zero_name = item.get(
            "zero_name"
        )
        zero_group = face_guide.get_guide_node(
            zero_name,
            required=False
        )

        if not zero_group:
            continue

        restore_attributes(
            face_guide,
            zero_group,
            item.get(
                "zero_values",
                {}
            )
        )

        locator_name = item.get(
            "locator_name"
        )
        current_locator = guide_mirror.get_side_locator(
            zero_group,
            side
        )

        # Mirror 前这个 Zero 下没有 Locator，则删除镜像时新建的 Locator。
        if not locator_name:
            if current_locator:
                if cmds.objExists(
                        current_locator
                ):
                    cmds.delete(
                        current_locator
                    )
            restored_count += 1
            continue

        locator = face_guide.get_guide_node(
            locator_name,
            required=False
        )

        if not locator:
            continue

        restore_attributes(
            face_guide,
            locator,
            item.get(
                "locator_values",
                {}
            )
        )

        locator_shapes = face_guide.get_locator_shapes(
            locator
        )

        if locator_shapes:
            restore_attributes(
                face_guide,
                locator_shapes[0],
                item.get(
                    "locator_shape_values",
                    {}
                )
            )

        restored_count += 1

    face_guide.check_symmetry = False
    face_guide.set_step_completed(
        completed=False
    )
    face_guide.invalidate_later_steps()

    return {
        "side": side,
        "restored_count": restored_count,
    }


# =============================================================================
# Undoable Operations
# =============================================================================

@scene_utils.undo_chunk
def mirror_guides(
        face_guide,
        source_side,
        target_side
):
    u"""记录 Target Snapshot，并执行一次可进入 Maya Undo Queue 的 Guide Mirror。"""
    snapshot = capture_side_state(
        face_guide,
        target_side
    )

    result = guide_mirror.mirror_guides(
        face_guide,
        source_side=source_side,
        target_side=target_side
    )

    result["snapshot"] = snapshot

    return result


@scene_utils.undo_chunk
def undo_mirror(
        face_guide,
        snapshot
):
    u"""独立恢复 UI 记录的上一次 Mirror Snapshot。"""
    return restore_snapshot(
        face_guide,
        snapshot
    )


__all__ = [
    "zero_attributes",
    "locator_attributes",
    "locator_shape_attributes",
    "capture_attributes",
    "restore_attributes",
    "capture_side_state",
    "restore_snapshot",
    "mirror_guides",
    "undo_mirror",
]
