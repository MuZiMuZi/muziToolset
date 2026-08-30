# coding=utf-8
u"""
Face Guide Mirror
=================

Step 02 Guide 左右镜像和单步撤销模块。

设计目标：
    1. 支持 lf -> rt 和 rt -> lf；
    2. 镜像只复制当前状态，不建立永久左右连接；
    3. Mirror 本身作为一次 Maya Undo Chunk，可直接 Ctrl + Z；
    4. UI 同时保存上一次 Target Snapshot，可独立执行“撤销上次镜像”；
    5. md 中线 Guide 不参与左右镜像。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import connection_utils
from ....core import hierarchy_utils
from ....core import rename_utils
from ....core import scene_utils


valid_sides = [
    "lf",
    "rt",
]

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

zero_attributes = list(
    transform_attributes
)
zero_attributes.append(
    "rotateOrder"
)

locator_attributes = [
    "translateX",
    "translateY",
    "translateZ",
    "rotateX",
    "rotateY",
    "rotateZ",
    "scaleX",
    "scaleY",
    "scaleZ",
    "rotateOrder",
    "visibility",
]

locator_shape_attributes = [
    "localPositionX",
    "localPositionY",
    "localPositionZ",
    "localScaleX",
    "localScaleY",
    "localScaleZ",
]


# =============================================================================
# Validate / Name
# =============================================================================

def validate_mirror_sides(
        source_side,
        target_side
):
    u"""检查 Guide Mirror 的 Source / Target Side。"""
    if source_side not in valid_sides:
        raise ValueError(
            u"source_side 必须是 lf 或 rt。"
        )

    if target_side not in valid_sides:
        raise ValueError(
            u"target_side 必须是 lf 或 rt。"
        )

    if source_side == target_side:
        raise ValueError(
            u"Guide Mirror 的 Source / Target Side 不能相同。"
        )

    return True


def get_mirror_name(
        source_name,
        source_side,
        target_side
):
    u"""把标准五段式名称中的 Side Token 替换为目标 Side。"""
    source_token = "_{}_".format(
        source_side
    )
    target_token = "_{}_".format(
        target_side
    )

    if source_token not in source_name:
        raise ValueError(
            u"节点名称中没有 {}，无法镜像: {}".format(
                source_token,
                source_name
            )
        )

    return source_name.replace(
        source_token,
        target_token,
        1
    )


# =============================================================================
# Query
# =============================================================================

def get_side_zero_groups(
        face_guide,
        side
):
    u"""返回指定 Side 下全部 zero_* Guide Group，并按父级优先排序。"""
    if side not in valid_sides:
        raise ValueError(
            u"side 必须是 lf 或 rt。"
        )

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

    prefix = "zero_{}_".format(
        side
    )
    zero_groups = []

    for node in descendants:
        short_name = rename_utils.get_short_name(
            node
        )

        if not short_name.startswith(
                prefix
        ):
            continue

        zero_groups.append(
            node
        )

    zero_groups.sort(
        key=hierarchy_utils.Hierarchy.get_dag_depth
    )

    return zero_groups


def get_side_locator(
        zero_group,
        side
):
    u"""返回一个 Side Zero Group 下对应的 Locator Transform。"""
    children = cmds.listRelatives(
        zero_group,
        children=True,
        type="transform",
        fullPath=True
    )

    if children is None:
        children = []

    prefix = "loc_{}_".format(
        side
    )

    for child in children:
        short_name = rename_utils.get_short_name(
            child
        )

        if short_name.startswith(
                prefix
        ):
            return child

    return None


def get_target_parent(
        face_guide,
        source_parent,
        source_side,
        target_side
):
    u"""根据 Source Parent 解析 Target Side 对应 Parent。"""
    if not source_parent:
        return None

    source_parent_name = rename_utils.get_short_name(
        source_parent
    )
    source_token = "_{}_".format(
        source_side
    )

    if source_token not in source_parent_name:
        return source_parent

    target_parent_name = get_mirror_name(
        source_parent_name,
        source_side,
        target_side
    )

    target_parent = face_guide.get_guide_node(
        target_parent_name,
        required=False
    )

    if not target_parent:
        raise RuntimeError(
            u"找不到 Guide Mirror 对应 Parent: {} -> {}".format(
                source_parent_name,
                target_parent_name
            )
        )

    return target_parent


# =============================================================================
# Attribute
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


def disconnect_inputs(
        node,
        attributes
):
    u"""断开指定属性输入，保证镜像后 Target 可以独立编辑。"""
    for attribute in attributes:
        destination_plug = "{}.{}".format(
            node,
            attribute
        )

        if not cmds.objExists(
                destination_plug
        ):
            continue

        connection_utils.disconnect_input(
            destination_plug
        )

    return True


def copy_attribute(
        face_guide,
        source_node,
        target_node,
        attribute
):
    u"""复制一个普通 Attribute，并恢复 Target 原 Lock 状态。"""
    source_plug = "{}.{}".format(
        source_node,
        attribute
    )
    target_plug = "{}.{}".format(
        target_node,
        attribute
    )

    if not cmds.objExists(source_plug):
        return False

    if not cmds.objExists(target_plug):
        return False

    value = cmds.getAttr(
        source_plug
    )

    connection_utils.disconnect_input(
        target_plug
    )

    face_guide.set_attr_preserve_lock(
        target_node,
        attribute,
        value
    )

    return True


def restore_attributes(
        face_guide,
        node,
        values
):
    u"""恢复节点 Attribute，并确保恢复后仍可独立编辑。"""
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
# Snapshot / Undo
# =============================================================================

def capture_side_state(
        face_guide,
        side
):
    u"""记录指定 Target Side 在镜像前的 Zero / Locator 状态。"""
    if side not in valid_sides:
        raise ValueError(
            u"side 必须是 lf 或 rt。"
        )

    snapshot = {
        "side": side,
        "zero_names": [],
        "items": [],
    }

    zero_groups = get_side_zero_groups(
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

        locator = get_side_locator(
            zero_group,
            side
        )

        locator_name = None
        locator_values = {}
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
                locator_shape_values = capture_attributes(
                    locator_shapes[0],
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
                "locator_shape_values": locator_shape_values,
            }
        )

    return snapshot


def remove_new_target_nodes(
        face_guide,
        snapshot
):
    u"""删除 Mirror 过程中新增、但 Snapshot 中原本不存在的 Target Zero。"""
    side = snapshot.get(
        "side"
    )
    original_zero_names = snapshot.get(
        "zero_names",
        []
    )

    current_zero_groups = get_side_zero_groups(
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

        if cmds.objExists(zero_group):
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

    if side not in valid_sides:
        raise ValueError(
            u"Mirror Snapshot 缺少有效 Side。"
        )

    remove_new_target_nodes(
        face_guide,
        snapshot
    )

    restored_count = 0
    items = snapshot.get(
        "items",
        []
    )

    for item in items:
        zero_group = face_guide.get_guide_node(
            item.get("zero_name"),
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
        current_locator = get_side_locator(
            zero_group,
            side
        )

        if not locator_name:
            if current_locator:
                if cmds.objExists(current_locator):
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

    face_guide.set_step_completed(
        completed=False
    )
    face_guide.invalidate_later_steps()

    return {
        "side": side,
        "restored_count": restored_count,
    }


# =============================================================================
# Mirror Build
# =============================================================================

def create_or_update_target_zero(
        face_guide,
        source_zero,
        source_side,
        target_side
):
    u"""创建或更新一个 Target Side Zero Group。"""
    source_zero_name = rename_utils.get_short_name(
        source_zero
    )
    target_zero_name = get_mirror_name(
        source_zero_name,
        source_side,
        target_side
    )

    source_parent = hierarchy_utils.Hierarchy.get_parent(
        source_zero
    )
    target_parent = get_target_parent(
        face_guide,
        source_parent,
        source_side,
        target_side
    )

    target_zero = face_guide.get_node_under_parent(
        target_parent,
        target_zero_name
    )

    if target_zero is None:
        target_zero = face_guide.get_guide_node(
            target_zero_name,
            required=False
        )

    if target_zero is None:
        target_zero = scene_utils.create_node(
            "transform",
            target_zero_name
        )

    current_parent = hierarchy_utils.Hierarchy.get_parent(
        target_zero
    )

    if target_parent:
        if current_parent != target_parent:
            target_zero = hierarchy_utils.Hierarchy.parent(
                target_zero,
                target_parent
            )

    disconnect_inputs(
        target_zero,
        zero_attributes
    )

    is_mirror_root = True

    if source_parent:
        source_parent_name = rename_utils.get_short_name(
            source_parent
        )
        source_token = "_{}_".format(
            source_side
        )

        if source_token in source_parent_name:
            is_mirror_root = False

    if is_mirror_root:
        face_guide.set_attr_preserve_lock(
            target_zero,
            "translateX",
            -cmds.getAttr(source_zero + ".translateX")
        )

        direct_attributes = [
            "translateY",
            "translateZ",
            "rotateX",
            "rotateY",
            "rotateZ",
            "scaleY",
            "scaleZ",
            "rotateOrder",
        ]

        for attribute in direct_attributes:
            copy_attribute(
                face_guide,
                source_zero,
                target_zero,
                attribute
            )

        face_guide.set_attr_preserve_lock(
            target_zero,
            "scaleX",
            -cmds.getAttr(source_zero + ".scaleX")
        )
    else:
        for attribute in zero_attributes:
            copy_attribute(
                face_guide,
                source_zero,
                target_zero,
                attribute
            )

    return target_zero


def create_or_update_target_locator(
        face_guide,
        source_locator,
        target_zero,
        source_side,
        target_side
):
    u"""创建或更新一个 Target Side Locator，并复制 Source 当前状态。"""
    source_locator_name = rename_utils.get_short_name(
        source_locator
    )
    target_locator_name = get_mirror_name(
        source_locator_name,
        source_side,
        target_side
    )

    target_locator = face_guide.get_node_under_parent(
        target_zero,
        target_locator_name
    )

    if target_locator is None:
        target_locator = face_guide.get_guide_node(
            target_locator_name,
            required=False
        )

    if target_locator is None:
        target_locator = cmds.spaceLocator(
            name=target_locator_name
        )[0]

    current_parent = hierarchy_utils.Hierarchy.get_parent(
        target_locator
    )

    if current_parent != target_zero:
        target_locator = hierarchy_utils.Hierarchy.parent(
            target_locator,
            target_zero
        )

    for attribute in locator_attributes:
        copy_attribute(
            face_guide,
            source_locator,
            target_locator,
            attribute
        )

    source_shapes = face_guide.get_locator_shapes(
        source_locator
    )
    target_shapes = face_guide.get_locator_shapes(
        target_locator
    )

    if source_shapes and target_shapes:
        source_shape = source_shapes[0]
        target_shape = target_shapes[0]

        for attribute in locator_shape_attributes:
            copy_attribute(
                face_guide,
                source_shape,
                target_shape,
                attribute
            )

    return target_locator


def mirror_guide(
        face_guide,
        source_zero,
        source_side,
        target_side
):
    u"""镜像一个 Side Guide Zero + Locator。"""
    source_locator = get_side_locator(
        source_zero,
        source_side
    )

    if not source_locator:
        raise RuntimeError(
            u"没有在 {} 下找到 loc_{}_*。".format(
                source_zero,
                source_side
            )
        )

    target_zero = create_or_update_target_zero(
        face_guide,
        source_zero,
        source_side,
        target_side
    )
    target_locator = create_or_update_target_locator(
        face_guide,
        source_locator,
        target_zero,
        source_side,
        target_side
    )

    return {
        "source_zero": source_zero,
        "source_locator": source_locator,
        "target_zero": target_zero,
        "target_locator": target_locator,
    }


def apply_mirror(
        face_guide,
        source_side,
        target_side
):
    u"""执行实际镜像，不创建 Snapshot / Undo Chunk。"""
    validate_mirror_sides(
        source_side,
        target_side
    )
    face_guide.validate_setup()

    if not face_guide.guide_exists():
        raise RuntimeError(
            u"Face Guide 尚未加载。"
        )

    source_zero_groups = get_side_zero_groups(
        face_guide,
        source_side
    )

    if not source_zero_groups:
        raise RuntimeError(
            u"没有找到 zero_{}_* Guide。".format(
                source_side
            )
        )

    results = []

    for source_zero in source_zero_groups:
        result = mirror_guide(
            face_guide,
            source_zero,
            source_side,
            target_side
        )
        results.append(
            result
        )

    face_guide.set_step_completed(
        completed=False
    )
    face_guide.invalidate_later_steps()

    return {
        "source_side": source_side,
        "target_side": target_side,
        "count": len(results),
        "items": results,
    }


@scene_utils.undo_chunk
def mirror_guides(
        face_guide,
        source_side,
        target_side
):
    u"""保存 Target Snapshot，并把一次 Mirror 写入 Maya Undo Queue。"""
    snapshot = capture_side_state(
        face_guide,
        target_side
    )

    result = apply_mirror(
        face_guide,
        source_side,
        target_side
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
    "valid_sides",
    "transform_attributes",
    "locator_attributes",
    "locator_shape_attributes",
    "capture_side_state",
    "apply_mirror",
    "mirror_guides",
    "undo_mirror",
]
