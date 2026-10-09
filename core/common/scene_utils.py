# coding=utf-8
"""scene_utils：供工具 UI 调用的 Maya 操作。"""

from __future__ import print_function
import os
from functools import partial
from functools import wraps
import maya.cmds as cmds
from ..common import file_utils

anim_curve_types = [
    "animCurveTA",
    "animCurveTL",
    "animCurveTT",
    "animCurveTU",
]

constraint_types = [
    "parentConstraint",
    "pointConstraint",
    "orientConstraint",
    "scaleConstraint",
    "aimConstraint",
    "poleVectorConstraint",
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

default_cameras = [
    "persp",
    "top",
    "front",
    "side",
]

def open_undo_chunk(chunk_name=None):
    u"""
    打开一个 Maya Undo Chunk。

    Args:
        chunk_name (str | None):
            可选 Undo Chunk 名称；None 时使用 Maya 默认命名。

    Returns:
        bool:
        Undo Chunk 成功打开后返回 True。
    """
    kwargs = {
        "openChunk": True,
    }

    if chunk_name:
        kwargs["chunkName"] = chunk_name

    cmds.undoInfo(
        **kwargs
    )
    return True

def close_undo_chunk():
    u"""
    关闭当前 Maya Undo Chunk。

    Returns:
        bool:
        Undo Chunk 成功关闭后返回 True。
    """
    cmds.undoInfo(
        closeChunk=True
    )
    return True

def undo_chunk(function):
    u"""
    把一次完整函数执行包装成一个 Maya Undo Chunk。

    Args:
        function (callable):
            需要在单个 Maya Undo Chunk 中执行的函数。

    Returns:
        callable:
        保留原函数元数据的 Undo Wrapper。
    """

    @wraps(function)
    def wrapped(*args, **kwargs):
        open_undo_chunk(
            function.__name__
        )

        try:
            return function(
                *args,
                **kwargs
            )
        finally:
            close_undo_chunk()

    return wrapped

def validate_node(node, label=None):
    u"""
    检查输入是否为真实存在的 Maya Node。

    Plug / Component 不属于 Node，因此例如 ``pCube1.translateX`` 和
    ``pCube1.vtx[0]`` 都会被拒绝。

    Args:
        node (str):
            需要验证的 Maya Node 名称或唯一 DAG Path。
        label (str | None):
            可选错误提示标签；None 时使用“ Maya 节点”。

    Returns:
        bool:
        节点存在且输入不是 Plug / Component 时返回 True。

    Raises:
        RuntimeError:
        名称为空、输入为 Plug / Component，或 Maya Node 不存在时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    display_label = label or u"Maya 节点"

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if node is None:
        raise RuntimeError(
            u"{}名称不能为空。".format(
                display_label
            )
        )

    node = str(node).strip()

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not node:
        raise RuntimeError(
            u"{}名称不能为空。".format(
                display_label
            )
        )

    if "." in node:
        raise RuntimeError(
            u"{}必须是 Maya Node，不能是 Plug / Component：{}".format(
                display_label,
                node
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not cmds.objExists(node):
        raise RuntimeError(
            u"{}不存在：{}".format(
                display_label,
                node
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True

def ensure_nodes_available(node_names, label=u"待创建节点"):
    u"""
    确保一组准备创建的 Maya 节点名称当前都没有被 Scene 占用。

    Args:
        node_names (str | list[str] | None):
            准备创建的一个或多个 Maya Node 名称；None 时直接视为可用。
        label (str):
            节点被占用时用于错误信息的业务标签。

    Returns:
        bool:
        所有有效名称都未被当前 Scene 占用时返回 True。

    Raises:
        RuntimeError:
        任意名称已经对应现有 Maya Node 时抛出，并列出全部冲突名称。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if node_names is None:
        return True

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if isinstance(node_names, str):
        node_names = [
            node_names
        ]

    existing_nodes = []

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node_name in node_names:
        if not node_name:
            continue

        if cmds.objExists(node_name):
            existing_nodes.append(
                node_name
            )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if existing_nodes:
        raise RuntimeError(
            u"{}已存在：{}".format(
                label,
                ", ".join(existing_nodes)
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True

def get_long_name(node):
    u"""
    返回唯一 Maya DAG Long Path；非 DAG 节点返回 Maya 查询得到的节点名。

    Args:
        node (str):
            需要解析的 Maya Node 名称或唯一 DAG Path。

    Returns:
        str:
        DAG 节点的唯一 Long Path，或非 DAG 节点的 Maya 节点名。

    Raises:
        RuntimeError:
        节点不存在，或输入短名称对应多个 DAG 节点时抛出。
    """
    validate_node(
        node
    )

    matches = cmds.ls(
        node,
        long=True
    )

    if matches is None:
        matches = []

    if not matches:
        return str(node)

    if len(matches) > 1:
        raise RuntimeError(
            u"节点名称不唯一，请使用完整路径：{}".format(
                node
            )
        )

    return matches[0]

def create_node(
        node_type,
        name,
        parent=None
):
    u"""
    创建一个 Maya Node，可选在创建时指定 DAG Parent。

    本函数不负责 Match / Snap。已经存在节点的 Reparent 统一交给
    ``hierarchy_utils.parent()``。

    Args:
        node_type (str):
            Maya Node Type，例如 ``transform``、``network`` 或 ``multMatrix``。
        name (str):
            新节点名称；当前场景中不能已经存在同名节点。
        parent (str | None):
            仅在创建 DAG Node 时使用的可选 Parent；None 表示不指定 Parent。

    Returns:
        str:
        Maya 创建后返回的节点名称。

    Raises:
        ValueError:
        ``node_type`` 或 ``name`` 为空时抛出。
        RuntimeError:
        同名节点已经存在，或指定 Parent 不存在时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not node_type:
        raise ValueError(
            u"node_type 不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not name:
        raise ValueError(
            u"节点名称不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    ensure_nodes_available(
        name,
        label=u"节点"
    )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if parent is not None:
        validate_node(
            parent,
            u"Parent"
        )

        return cmds.createNode(
            node_type,
            name=name,
            parent=parent
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return cmds.createNode(
        node_type,
        name=name
    )

def get_nodes_by_type(
        node_type,
        long=True
):
    u"""
    返回当前 Maya Scene 中指定 Node Type 的全部节点。

    Args:
        node_type (str):
            需要查询的 Maya Node Type，例如 ``jnt`` 或 ``transform``。
        long (bool):
            是否让 Maya 对 DAG Node 返回 Long Path。

    Returns:
        list[str]:
        指定类型的 Maya Node 列表；没有匹配节点时返回空列表。

    Raises:
        ValueError:
        ``node_type`` 为空时抛出。
    """
    if not node_type:
        raise ValueError(
            u"node_type 不能为空。"
        )

    nodes = cmds.ls(
        type=node_type,
        long=long
    )

    if nodes is None:
        nodes = []

    return nodes

def get_selected_nodes(
        node_type=None,
        long=True,
        flatten=True
):
    u"""
    返回当前 Maya Selection，可选按 Maya Node Type 过滤。

    未指定 ``node_type`` 时保留 Maya 当前 Selection Item，因此 Component
    Selection 也可能出现在结果中；指定 ``node_type`` 后 Component 会被忽略。

    Args:
        node_type (str | None):
            可选 Maya Node Type；None 时不过滤当前 Selection Item。
        long (bool):
            是否让 Maya 尽量返回 DAG Long Path。
        flatten (bool):
            是否展开 Maya Component Selection。

    Returns:
        list[str]:
        当前 Selection；没有选择或过滤后没有匹配项时返回空列表。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    selected_nodes = cmds.ls(
        selection=True,
        long=long,
        flatten=flatten
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if selected_nodes is None:
        selected_nodes = []

    if node_type is None:
        return selected_nodes

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    filtered_nodes = []

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for selected_node in selected_nodes:
        if "." in selected_node:
            continue

        try:
            selected_type = cmds.nodeType(
                selected_node
            )
        except Exception:
            continue

        if selected_type != node_type:
            continue

        filtered_nodes.append(
            selected_node
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return filtered_nodes

def is_default_camera(node):
    u"""
    判断节点是否为 Maya 默认相机 Transform。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    short_name = str(node).rsplit("|", 1)[-1]
    return short_name in default_cameras

def is_referenced(node):
    u"""
    判断节点是否来自 Reference。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object | bool:
        条件成立时返回 True，否则返回 False。
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
        当前 API 完成处理后返回的结果。
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
        当前 API 完成处理后返回的结果。
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
        当前 API 完成处理后返回的结果。
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

def has_incoming_animation(node):
    u"""
    判断 Transform 是否存在 AnimCurve 输入。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool:
        条件成立时返回 True，否则返回 False。
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
        条件成立时返回 True，否则返回 False。
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
        条件成立时返回 True，否则返回 False。
    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    history = cmds.listHistory(
        node,
        pruneDagObjects=True
    ) or []

    # -------------------------------------------------------------------------
    # Step 02：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 03：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
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
        当前操作成功或目标状态满足要求时返回 True，否则返回 False。
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
        当前 API 完成处理后返回的结果。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：建立候选节点列表。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if nodes is None:
        candidates = all_transform_nodes()
    else:
        candidates = existing_nodes(nodes)
        parent_candidates = _collect_parent_candidates(candidates)

        for parent in parent_candidates:
            if parent not in candidates:
                candidates.append(parent)

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    deleted_count = 0
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    changed = True

    # -------------------------------------------------------------------------
    # 步骤 2：循环检查直到本轮没有删除任何节点。
    #
    # 为什么需要循环：
    # Child 空组删除后，Parent 可能才刚刚变成空组，需要下一轮继续处理。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
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

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return deleted_count

def delete_history(nodes):
    u"""
    删除安全范围内的 Construction History。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        tuple: ``(processed_count, skipped_count)``。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    nodes = existing_nodes(nodes)
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    deleted_count = 0
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    skipped_count = 0

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return deleted_count, skipped_count

def freeze_transformations(nodes):
    u"""
    Freeze 安全范围内的 Transform。

    有 Animation、Constraint 或 Rig Deformer 的节点一律跳过。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        tuple:
        按当前 API 约定组织的结果元组。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    nodes = existing_nodes(nodes)
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    frozen_count = 0
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    skipped_count = 0

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return frozen_count, skipped_count

def unlock_and_show_attributes(nodes):
    u"""
    解锁并显示标准 Translate / Rotate / Scale / Visibility 通道。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    nodes = existing_nodes(nodes)
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
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
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    changed_count = 0

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return changed_count

def center_pivot(nodes):
    u"""
    把可编辑、带 Shape 的 Transform Pivot 居中。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
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

def delete_unknown_nodes(nodes=None):
    u"""
    删除非 Reference Unknown 节点。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    deleted_count = 0

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 04：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return deleted_count

@undo_chunk
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
        当前 API 完成处理后返回的结果。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
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
    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
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
    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if unlock_enabled:
        result["attributes"] = unlock_and_show_attributes(nodes)

    if center_pivot_enabled:
        result["pivot"] = center_pivot(nodes)

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if delete_unknown_enabled:
        unknown_scope = nodes

        if not selected_only:
            unknown_scope = None

        result["unknown"] = delete_unknown_nodes(
            unknown_scope
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result
