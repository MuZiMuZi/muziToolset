# coding=utf-8
u"""
Scene Clean Utils
=================

Maya 场景安全清理模块。

模块职责
--------
本模块负责“明确会修改场景”的通用清理操作，并通过一组保护规则避免误伤 Rig、动画和 Reference。

主要公开 API
------------
all_transform_nodes()
    返回全场景 Transform Long Path。

delete_empty_groups(nodes=None)
    递归删除空 Transform Group。

delete_history(nodes)
    删除安全范围内的 Construction History；存在 Rig Deformer 时跳过。

freeze_transformations(nodes)
    Freeze 安全范围内的 Transform；动画、Constraint、Rig Deformer、Reference 会跳过。

unlock_and_show_attributes(nodes)
    解锁并显示标准 TRS / Visibility 属性。

center_pivot(nodes)
    对可编辑、带 Shape 的 Transform 执行 Center Pivot。

delete_unknown_nodes(nodes=None)
    删除非 Reference Unknown 节点。

run_cleanup(...)
    按开关组合执行一次安全清理，并返回统计字典。

安全保护
--------
1. 不修改 Reference 节点；
2. 不删除 Maya 默认相机；
3. Delete History 遇到 Skin / BlendShape / Wrap 等 Rig Deformer 时跳过；
4. Freeze 遇到 Animation、Constraint 或 Rig Deformer 时跳过；
5. Delete Empty Group 采用 Child First + 递归循环，确保父组在子组删除后可以再次检查；
6. Core 不弹确认窗口，真正的“是否执行清理”由上层 Tool / App 决定。

和 model_check_utils.py 的区别
-----------------------------
model_check_utils.py
    负责发现问题，默认尽量只读。

scene_clean_utils.py
    负责执行明确的场景修改。

因此两个模块不合并，避免“检查一下模型”意外产生场景修改。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import scene_utils


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


# =============================================================================
# Common Query
# =============================================================================

def get_short_name(node):
    u"""
    返回 DAG Short Name。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return node.split("|")[-1]


def is_default_camera(node):
    u"""
    判断节点是否为 Maya 默认相机 Transform。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return get_short_name(node) in default_cameras


def is_referenced(node):
    u"""
    判断节点是否来自 Reference。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object | bool:
        方法执行后的结果数据。
    """
    try:
        return cmds.referenceQuery(
            node,
            isNodeReferenced=True
        )
    except Exception:
        return False


def existing_nodes(nodes):
    u"""
    过滤不存在的节点、转换为 Long Path 并去重。

    该步骤在真正修改场景前统一执行，避免调用过程中遇到已经被前一个清理动作删除的节点。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    result = []

    if not nodes:
        return result

    for node in nodes:
        if not node or not cmds.objExists(node):
            continue

        matches = cmds.ls(
            node,
            long=True
        ) or []
        resolved = matches[0] if matches else node

        if resolved not in result:
            result.append(resolved)

    return result


def all_transform_nodes():
    u"""
    返回全场景 Transform Long Path。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return cmds.ls(
        type="transform",
        long=True
    ) or []


def sort_child_first(nodes):
    u"""
    按 DAG 深度从深到浅排序。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    result = []

    for node in nodes:
        if node not in result:
            result.append(node)

    def get_depth(node):
        return node.count("|")

    result.sort(
        key=get_depth,
        reverse=True
    )

    return result


# =============================================================================
# Protection Query
# =============================================================================

def has_incoming_animation(node):
    u"""
    判断 Transform 是否存在 AnimCurve 输入。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool:
        方法执行后的结果数据。
    """
    for anim_type in anim_curve_types:
        connections = cmds.listConnections(
            node,
            source=True,
            destination=False,
            type=anim_type
        ) or []

        if connections:
            return True

    return False


def has_constraint(node):
    u"""
    判断节点是否存在常见 Constraint 输入。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool:
        方法执行后的结果数据。
    """
    connections = cmds.listConnections(
        node,
        source=True,
        destination=False
    ) or []

    for connection in connections:
        try:
            node_type = cmds.nodeType(connection)
        except Exception:
            continue

        if node_type in constraint_types:
            return True

    return False


def has_rig_history(node):
    u"""
    判断历史中是否存在需要保护的 Rig Deformer。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool:
        方法执行后的结果数据。
    """
    history = cmds.listHistory(
        node,
        pruneDagObjects=True
    ) or []

    for history_node in history:
        try:
            node_type = cmds.nodeType(history_node)
        except Exception:
            continue

        if node_type in rig_history_types:
            return True

        # 未列进白名单但属于 geometryFilter 的节点同样按 Deformer 保护。
        try:
            if cmds.objectType(
                    history_node,
                    isAType="geometryFilter"
            ):
                return True
        except Exception:
            pass

    return False


def can_modify_transform(node):
    u"""
    判断节点是否允许进入 Transform 类清理操作。

    默认相机、Reference、非 Transform 都返回 False。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool:
        方法执行后的结果数据。
    """
    if not cmds.objExists(node):
        return False

    if is_default_camera(node):
        return False

    if is_referenced(node):
        return False

    if cmds.nodeType(node) != "transform":
        return False

    return True


# =============================================================================
# Delete Empty Group
# =============================================================================

def _collect_parent_candidates(nodes):
    """把输入节点一直向上追溯到 Root，收集可能在清理后变空的 Parent。"""
    parent_candidates = []

    for node in nodes:
        current = node

        while current:
            parents = cmds.listRelatives(
                current,
                parent=True,
                fullPath=True
            ) or []

            if not parents:
                break

            current = parents[0]

            if current not in parent_candidates:
                parent_candidates.append(current)

    return parent_candidates


def delete_empty_groups(nodes=None):
    u"""
    递归删除空 Transform Group。

    ``nodes=None`` 时扫描全场景；给定 nodes 时还会自动把它们的 Parent 加入候选，
    因为删除 Child 后原本非空的 Parent 可能变成空组。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：建立候选节点列表。
    # -------------------------------------------------------------------------
    if nodes is None:
        candidates = all_transform_nodes()
    else:
        candidates = existing_nodes(nodes)
        parent_candidates = _collect_parent_candidates(candidates)

        for parent in parent_candidates:
            if parent not in candidates:
                candidates.append(parent)

    deleted_count = 0
    changed = True

    # -------------------------------------------------------------------------
    # 步骤 2：循环检查直到本轮没有删除任何节点。
    #
    # 为什么需要循环：
    # Child 空组删除后，Parent 可能才刚刚变成空组，需要下一轮继续处理。
    # -------------------------------------------------------------------------
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
            ) or []
            children = cmds.listRelatives(
                node,
                children=True,
                fullPath=True
            ) or []

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


# =============================================================================
# Delete History
# =============================================================================

def delete_history(nodes):
    u"""
    删除安全范围内的 Construction History。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        tuple: ``(processed_count, skipped_count)``。
    """
    nodes = existing_nodes(nodes)
    deleted_count = 0
    skipped_count = 0

    for node in nodes:
        if not can_modify_transform(node):
            skipped_count += 1
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        ) or []

        if not shapes:
            continue

        # Rig Deformer 比建模 History 更重要，发现后整个对象跳过 Delete History。
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


# =============================================================================
# Freeze Transform
# =============================================================================

def freeze_transformations(nodes):
    u"""
    Freeze 安全范围内的 Transform。

    有 Animation、Constraint 或 Rig Deformer 的节点一律跳过。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        tuple:
        方法执行后的结果数据。
    """
    nodes = existing_nodes(nodes)
    frozen_count = 0
    skipped_count = 0

    for node in nodes:
        # 步骤 1：基础保护。
        if not can_modify_transform(node):
            skipped_count += 1
            continue

        # 步骤 2：Animation / Constraint / Deformer 保护。
        if has_incoming_animation(node):
            skipped_count += 1
            continue

        if has_constraint(node):
            skipped_count += 1
            continue

        if has_rig_history(node):
            skipped_count += 1
            continue

        # 步骤 3：正式 Freeze，并保留 Normal。
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


# =============================================================================
# Attribute / Pivot
# =============================================================================

def unlock_and_show_attributes(nodes):
    u"""
    解锁并显示标准 Translate / Rotate / Scale / Visibility 通道。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
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
    u"""
    把可编辑、带 Shape 的 Transform Pivot 居中。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
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
        ) or []

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


# =============================================================================
# Unknown Node
# =============================================================================

def delete_unknown_nodes(nodes=None):
    u"""
    删除非 Reference Unknown 节点。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    if nodes is None:
        unknown_nodes = cmds.ls(
            type="unknown",
            long=True
        ) or []
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


# =============================================================================
# Cleanup Runner
# =============================================================================

@scene_utils.undo_chunk
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
    u"""
    按配置执行一次安全清理并返回统计字典。

    整个 Cleanup 被包装为一次 Maya Undo，方便用户完整回退一次清理操作。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。
        selected_only (bool):
            清理 / 检查范围是否限制为当前 Maya Selection。
        delete_empty (bool):
            场景清理时是否删除确认无 Child / Shape 的空 Transform。
        delete_history_enabled (bool):
            清理流程是否执行 Modeling History 删除。
        freeze_enabled (bool):
            清理流程是否执行 Freeze Transform。
        unlock_enabled (bool):
            清理流程是否解除可安全处理的 Locked Channel。
        center_pivot_enabled (bool):
            清理流程是否执行 Center Pivot。
        delete_unknown_enabled (bool):
            清理流程是否删除确认无用的 Unknown Node。

    Returns:
        object:
        方法执行后的结果数据。
    """
    result = {}

    # 步骤 1：空组与 Unknown 可以根据 selected_only 决定局部 / 全场景范围。
    if delete_empty:
        empty_scope = nodes

        if not selected_only:
            empty_scope = None

        result["empty_groups"] = delete_empty_groups(
            empty_scope
        )

    # 步骤 2：History / Freeze 始终针对明确传入节点，并返回 Processed / Skipped。
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

    # 步骤 3：其它安全清理。
    if unlock_enabled:
        result["attributes"] = unlock_and_show_attributes(nodes)

    if center_pivot_enabled:
        result["pivot"] = center_pivot(nodes)

    if delete_unknown_enabled:
        unknown_scope = nodes

        if not selected_only:
            unknown_scope = None

        result["unknown"] = delete_unknown_nodes(
            unknown_scope
        )

    return result


__all__ = [
    "get_short_name",
    "is_default_camera",
    "is_referenced",
    "existing_nodes",
    "all_transform_nodes",
    "sort_child_first",
    "has_incoming_animation",
    "has_constraint",
    "has_rig_history",
    "can_modify_transform",
    "delete_empty_groups",
    "delete_history",
    "freeze_transformations",
    "unlock_and_show_attributes",
    "center_pivot",
    "delete_unknown_nodes",
    "run_cleanup",
]
