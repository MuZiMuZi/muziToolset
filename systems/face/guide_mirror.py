# coding=utf-8
u"""
Face Guide Mirror
=================

Face Guide 左右定位器镜像模块。

设计目标：
    1. 支持 lf -> rt 和 rt -> lf 两个方向；
    2. 镜像操作只复制当前 Guide 状态，不建立永久 Transform 连接；
    3. 镜像完成后左右 Guide 仍然可以独立编辑；
    4. md 中线 Guide 不参与左右镜像；
    5. 复用 FaceGuide 的查询能力和 Core 的 DAG / Connection 能力。

重要边界：
    - 本模块只处理 Guide Mirror，不负责 Step Finalize；
    - Guide Template 的初始层级仍然由 resources/face/face_guide.ma 提供；
    - Maya Plug 输入断开统一复用 core.connection_utils；
    - DAG Parent 操作统一复用 core.hierarchy_utils；
    - 新建通用 Transform 统一复用 core.scene_utils。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import connection_utils
from ...core import hierarchy_utils
from ...core import rename_utils
from ...core import scene_utils


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
    u"""把标准 Rig 名称中的 Side Token 替换成目标 Side。"""
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

def disconnect_inputs(
        node,
        attributes
):
    u"""断开目标节点指定属性的全部输入，保证镜像后可以独立编辑。"""
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
    u"""复制一个普通 Maya Attribute，并保留 Target 原 Lock 状态。"""
    source_plug = "{}.{}".format(
        source_node,
        attribute
    )
    target_plug = "{}.{}".format(
        target_node,
        attribute
    )

    if not cmds.objExists(
            source_plug
    ):
        return False

    if not cmds.objExists(
            target_plug
    ):
        return False

    connection_utils.disconnect_input(
        target_plug
    )

    value = cmds.getAttr(
        source_plug
    )

    face_guide.set_attr_preserve_lock(
        target_node,
        attribute,
        value
    )

    return True


# =============================================================================
# Mirror
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
        transform_attributes
    )

    copy_attribute(
        face_guide,
        source_zero,
        target_zero,
        "rotateOrder"
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
        translate_x = cmds.getAttr(
            source_zero + ".translateX"
        )
        translate_y = cmds.getAttr(
            source_zero + ".translateY"
        )
        translate_z = cmds.getAttr(
            source_zero + ".translateZ"
        )

        rotate_x = cmds.getAttr(
            source_zero + ".rotateX"
        )
        rotate_y = cmds.getAttr(
            source_zero + ".rotateY"
        )
        rotate_z = cmds.getAttr(
            source_zero + ".rotateZ"
        )

        scale_x = cmds.getAttr(
            source_zero + ".scaleX"
        )
        scale_y = cmds.getAttr(
            source_zero + ".scaleY"
        )
        scale_z = cmds.getAttr(
            source_zero + ".scaleZ"
        )

        face_guide.set_attr_preserve_lock(
            target_zero,
            "translateX",
            -translate_x
        )
        face_guide.set_attr_preserve_lock(
            target_zero,
            "translateY",
            translate_y
        )
        face_guide.set_attr_preserve_lock(
            target_zero,
            "translateZ",
            translate_z
        )

        face_guide.set_attr_preserve_lock(
            target_zero,
            "rotateX",
            rotate_x
        )
        face_guide.set_attr_preserve_lock(
            target_zero,
            "rotateY",
            rotate_y
        )
        face_guide.set_attr_preserve_lock(
            target_zero,
            "rotateZ",
            rotate_z
        )

        face_guide.set_attr_preserve_lock(
            target_zero,
            "scaleX",
            -scale_x
        )
        face_guide.set_attr_preserve_lock(
            target_zero,
            "scaleY",
            scale_y
        )
        face_guide.set_attr_preserve_lock(
            target_zero,
            "scaleZ",
            scale_z
        )
    else:
        for attribute in transform_attributes:
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
    u"""创建或更新一个 Target Side Locator，并复制当前 Source 状态。"""
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

    disconnect_inputs(
        target_locator,
        locator_attributes
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


def mirror_guides(
        face_guide,
        source_side,
        target_side
):
    u"""
    批量把 Source Side Guide 镜像到 Target Side。

    Mirror 只执行一次数据复制，不保留 Source -> Target 的永久 DG 连接。
    """
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

    # 新镜像工作流允许左右独立编辑，不再要求 LF -> RT 永久连接。
    face_guide.check_symmetry = False

    # Guide 发生变化后，当前 Step 和后续 Build 结果都需要重新提交。
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


__all__ = [
    "valid_sides",
    "transform_attributes",
    "locator_attributes",
    "locator_shape_attributes",
    "validate_mirror_sides",
    "get_mirror_name",
    "get_side_zero_groups",
    "get_side_locator",
    "mirror_guide",
    "mirror_guides",
]
