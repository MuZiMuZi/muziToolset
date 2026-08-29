# coding=utf-8
u"""
Scene Clean Utils
=================

Maya 场景安全清理底层模块。

安全原则：
    1. 不修改引用节点；
    2. 不删除默认相机；
    3. Delete History 跳过常见 Rig Deformer；
    4. Freeze 跳过动画、约束和 Rig Deformer；
    5. 删除空组采用递归方式；
    6. 本模块不包含 UI 和确认弹窗。
"""

from __future__ import print_function

import maya.cmds as cmds


default_cameras = [
    "persp",
    "top",
    "front",
    "side",
]

rig_history_types = [
    "skinCluster",
    "blendShape",
    "cluster",
    "wire",
    "ffd",
    "lattice",
    "nonLinear",
    "deltaMush",
    "tension",
    "wrap",
    "proximityWrap",
]

constraint_types = [
    "parentConstraint",
    "pointConstraint",
    "orientConstraint",
    "scaleConstraint",
    "aimConstraint",
    "poleVectorConstraint",
]

anim_curve_types = [
    "animCurveTA",
    "animCurveTL",
    "animCurveTT",
    "animCurveTU",
]


def get_short_name(node):
    """返回 DAG 节点短名称。"""
    return node.split("|")[-1]


def is_default_camera(node):
    """判断是否为 Maya 默认相机 Transform。"""
    return get_short_name(node) in default_cameras


def is_referenced(node):
    """判断节点是否来自 Reference。"""
    try:
        return cmds.referenceQuery(
            node,
            isNodeReferenced=True
        )
    except Exception:
        return False


def existing_nodes(nodes):
    """过滤不存在的节点，并转换成长名称。"""
    result = []

    if not nodes:
        return result

    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        matches = cmds.ls(
            node,
            long=True
        )

        if matches is None:
            matches = []

        resolved = node

        if matches:
            resolved = matches[0]

        if resolved not in result:
            result.append(resolved)

    return result


def all_transform_nodes():
    """返回全场景 Transform。"""
    nodes = cmds.ls(
        type="transform",
        long=True
    )

    if nodes is None:
        nodes = []

    return nodes


def sort_child_first(nodes):
    """按 DAG 深度从深到浅排序，不使用 lambda。"""
    result = []

    for node in nodes:
        if node not in result:
            result.append(node)

    item_count = len(result)
    outer_index = 0

    while outer_index < item_count:
        inner_index = 0

        while inner_index < item_count - 1:
            current_depth = result[inner_index].count("|")
            next_depth = result[inner_index + 1].count("|")

            if current_depth < next_depth:
                temporary_node = result[inner_index]
                result[inner_index] = result[inner_index + 1]
                result[inner_index + 1] = temporary_node

            inner_index += 1

        outer_index += 1

    return result


def has_incoming_animation(node):
    """判断 Transform 是否有 AnimCurve 输入。"""
    for anim_type in anim_curve_types:
        connections = cmds.listConnections(
            node,
            source=True,
            destination=False,
            type=anim_type
        )

        if connections:
            return True

    return False


def has_constraint(node):
    """判断节点是否存在 Constraint 输入。"""
    connections = cmds.listConnections(
        node,
        source=True,
        destination=False
    )

    if connections is None:
        connections = []

    for connection in connections:
        try:
            node_type = cmds.nodeType(connection)
        except Exception:
            continue

        if node_type in constraint_types:
            return True

    return False


def has_rig_history(node):
    """判断历史中是否存在需要保护的 Rig Deformer。"""
    history = cmds.listHistory(
        node,
        pruneDagObjects=True
    )

    if history is None:
        history = []

    for history_node in history:
        try:
            node_type = cmds.nodeType(history_node)
        except Exception:
            continue

        if node_type in rig_history_types:
            return True

    return False


def can_modify_transform(node):
    """判断节点是否适合执行场景清理。"""
    if not cmds.objExists(node):
        return False

    if is_default_camera(node):
        return False

    if is_referenced(node):
        return False

    if cmds.nodeType(node) != "transform":
        return False

    return True


def delete_empty_groups(nodes=None):
    """递归删除空 Transform Group。"""
    if nodes is None:
        candidates = all_transform_nodes()
    else:
        candidates = existing_nodes(nodes)
        parent_candidates = []

        for node in candidates:
            current = node

            while current:
                parents = cmds.listRelatives(
                    current,
                    parent=True,
                    fullPath=True
                )

                if parents is None:
                    parents = []

                if not parents:
                    break

                current = parents[0]

                if current not in parent_candidates:
                    parent_candidates.append(current)

        for parent in parent_candidates:
            if parent not in candidates:
                candidates.append(parent)

    deleted_count = 0
    changed = True

    while changed:
        changed = False
        current_candidates = []

        for node in candidates:
            if cmds.objExists(node):
                current_candidates.append(node)

        current_candidates = sort_child_first(current_candidates)

        for node in current_candidates:
            if not can_modify_transform(node):
                continue

            shapes = cmds.listRelatives(
                node,
                shapes=True,
                fullPath=True
            )

            if shapes is None:
                shapes = []

            children = cmds.listRelatives(
                node,
                children=True,
                fullPath=True
            )

            if children is None:
                children = []

            if shapes or children:
                continue

            try:
                cmds.delete(node)
                deleted_count += 1
                changed = True
            except Exception as error:
                cmds.warning(
                    u"无法删除空组 {}：{}".format(
                        node,
                        error
                    )
                )

    return deleted_count


def delete_history(nodes):
    """删除安全范围内的 Construction History。"""
    nodes = existing_nodes(nodes)
    deleted_count = 0
    skipped_count = 0

    for node in nodes:
        if not can_modify_transform(node):
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        )

        if shapes is None:
            shapes = []

        if not shapes:
            continue

        if has_rig_history(node):
            skipped_count += 1
            continue

        try:
            cmds.delete(
                node,
                constructionHistory=True
            )
            deleted_count += 1
        except Exception as error:
            cmds.warning(
                u"无法删除历史 {}：{}".format(
                    node,
                    error
                )
            )

    return deleted_count, skipped_count


def freeze_transformations(nodes):
    """冻结安全范围内的 Transform。"""
    nodes = existing_nodes(nodes)
    frozen_count = 0
    skipped_count = 0

    for node in nodes:
        if not can_modify_transform(node):
            skipped_count += 1
            continue

        if has_incoming_animation(node):
            skipped_count += 1
            continue

        if has_constraint(node):
            skipped_count += 1
            continue

        if has_rig_history(node):
            skipped_count += 1
            continue

        try:
            cmds.makeIdentity(
                node,
                apply=True,
                translate=True,
                rotate=True,
                scale=True,
                normal=False,
                preserveNormals=True
            )
            frozen_count += 1
        except Exception as error:
            cmds.warning(
                u"无法冻结变换 {}：{}".format(
                    node,
                    error
                )
            )

    return frozen_count, skipped_count


def unlock_and_show_attributes(nodes):
    """解锁并显示标准 Transform 属性。"""
    nodes = existing_nodes(nodes)
    attrs = [
        "tx",
        "ty",
        "tz",
        "rx",
        "ry",
        "rz",
        "sx",
        "sy",
        "sz",
        "v",
    ]
    changed_count = 0

    for node in nodes:
        if is_referenced(node):
            continue

        for attr in attrs:
            if not cmds.attributeQuery(
                    attr,
                    node=node,
                    exists=True
            ):
                continue

            plug = "{}.{}".format(
                node,
                attr
            )

            try:
                cmds.setAttr(
                    plug,
                    lock=False
                )
                cmds.setAttr(
                    plug,
                    keyable=True
                )
                changed_count += 1
            except Exception:
                pass

    return changed_count


def center_pivot(nodes):
    """把可编辑几何 Transform 的 Pivot 居中。"""
    nodes = existing_nodes(nodes)
    centered_count = 0

    for node in nodes:
        if not can_modify_transform(node):
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        )

        if shapes is None:
            shapes = []

        if not shapes:
            continue

        try:
            cmds.xform(
                node,
                centerPivots=True
            )
            centered_count += 1
        except Exception:
            pass

    return centered_count


def delete_unknown_nodes(nodes=None):
    """删除 Unknown 节点。"""
    if nodes is None:
        unknown_nodes = cmds.ls(
            type="unknown",
            long=True
        )

        if unknown_nodes is None:
            unknown_nodes = []
    else:
        unknown_nodes = []

        for node in existing_nodes(nodes):
            if cmds.nodeType(node) == "unknown":
                unknown_nodes.append(node)

    deleted_count = 0

    for node in unknown_nodes:
        if is_referenced(node):
            continue

        try:
            cmds.delete(node)
            deleted_count += 1
        except Exception as error:
            cmds.warning(
                u"无法删除 Unknown 节点 {}：{}".format(
                    node,
                    error
                )
            )

    return deleted_count


def run_cleanup(
        nodes,
        selected_only=True,
        delete_empty=True,
        delete_history_enabled=False,
        freeze_enabled=False,
        unlock_enabled=False,
        center_pivot_enabled=False,
        delete_unknown_enabled=True
):
    """按配置执行一次安全清理并返回结果字典。"""
    result = {}

    if delete_empty:
        empty_scope = nodes

        if not selected_only:
            empty_scope = None

        result["empty_groups"] = delete_empty_groups(empty_scope)

    if delete_history_enabled:
        deleted_count, skipped_count = delete_history(nodes)
        result["history"] = {
            "processed": deleted_count,
            "skipped": skipped_count,
        }

    if freeze_enabled:
        frozen_count, skipped_count = freeze_transformations(nodes)
        result["freeze"] = {
            "processed": frozen_count,
            "skipped": skipped_count,
        }

    if unlock_enabled:
        result["attributes"] = unlock_and_show_attributes(nodes)

    if center_pivot_enabled:
        result["pivot"] = center_pivot(nodes)

    if delete_unknown_enabled:
        unknown_scope = nodes

        if not selected_only:
            unknown_scope = None

        result["unknown"] = delete_unknown_nodes(unknown_scope)

    return result


__all__ = [
    "all_transform_nodes",
    "delete_empty_groups",
    "delete_history",
    "freeze_transformations",
    "unlock_and_show_attributes",
    "center_pivot",
    "delete_unknown_nodes",
    "run_cleanup",
]
