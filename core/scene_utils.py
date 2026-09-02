# coding=utf-8
u"""
Scene Utils
===========

Maya Scene 领域的通用底层工具。

模块职责
--------
本模块只处理 Maya Scene 本身的基础能力：

    - Undo Chunk；
    - Maya Node 存在性、唯一 DAG Long Path 和节点创建；
    - 一组待创建节点的 Scene Availability 检查；
    - 按 Maya Node Type 查询场景节点；
    - 当前 Selection 查询；
    - Object Set 创建与维护；
    - Maya Native Event Callback；
    - 当前 Scene 路径与修改状态；
    - Maya Scene Open / Import / Reference。

模块边界
--------
    Maya Scene / Node / Selection / Scene IO -> scene_utils
    硬盘 Path / Directory / JSON             -> file_utils
    Transform 空间数据                        -> transform_utils
    DAG Parent / Child                        -> hierarchy_utils
    Snap / Match                              -> snap_utils
    FBX / Alembic / USD 等导出                -> export_utils

设计原则
--------
1. Core 不弹确认窗口，交互确认由 Tool / App 负责；
2. 创建函数先完成输入验证，再修改 Maya Scene；
3. validate_node() 只接受 Maya Node，不接受 Plug / Component；
4. ensure_nodes_available() 只检查已有 Scene State，不判断 Rig Naming 格式；
5. get_nodes_by_type() / get_selected_nodes() 只负责 Scene Query，不附带 Tool Workflow；
6. 特定文件格式的导出逻辑不继续堆进 Scene Core；
7. Scene Core 不保留 Selection Workflow 或文件格式导出的历史兼容入口。
"""

from __future__ import print_function

import os
from functools import partial
from functools import wraps

import maya.api.OpenMaya as om
import maya.cmds as cmds

from . import file_utils


# =============================================================================
# Undo
# =============================================================================

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


# =============================================================================
# Node
# =============================================================================

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
            需要查询的 Maya Node Type，例如 ``joint`` 或 ``transform``。
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


# =============================================================================
# Selection
# =============================================================================

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


# =============================================================================
# Object Set
# =============================================================================

def ensure_object_set(
        set_name,
        objects=None,
        parent_set=None
):
    u"""
    创建或复用 Object Set，并可安全加入对象和父 Set。

    Args:
        set_name (str):
            需要创建或复用的 Maya Object Set 名称。
        objects (str | list[str] | None):
            可选需要加入 Set 的 Maya Node；None 时只确保 Set 本身存在。
        parent_set (str | None):
            可选父 Object Set；不存在时会自动创建。

    Returns:
        str:
        已确认存在并完成成员维护的 Object Set 名称。

    Raises:
        ValueError:
        ``set_name`` 为空时抛出。
        RuntimeError:
        Set 名称或 Parent Set 名称被非 Object Set 节点占用，或成员节点无效时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not set_name:
        raise ValueError(
            u"Set 名称不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if cmds.objExists(set_name):
        if cmds.nodeType(set_name) != "objectSet":
            raise RuntimeError(
                u"同名节点不是 Object Set：{}".format(
                    set_name
                )
            )
    else:
        set_name = cmds.sets(
            name=set_name,
            empty=True
        )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if objects is not None:
        if isinstance(objects, str):
            objects = [
                objects
            ]

        for scene_object in objects:
            if not scene_object:
                continue

            validate_node(
                scene_object
            )

            cmds.sets(
                scene_object,
                edit=True,
                addElement=set_name
            )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if parent_set:
        if cmds.objExists(parent_set):
            if cmds.nodeType(parent_set) != "objectSet":
                raise RuntimeError(
                    u"父 Set 名称被非 Object Set 节点占用：{}".format(
                        parent_set
                    )
                )
        else:
            parent_set = cmds.sets(
                name=parent_set,
                empty=True
            )

        cmds.sets(
            set_name,
            edit=True,
            addElement=parent_set
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return set_name


# =============================================================================
# Maya Native Callback
# =============================================================================

def create_native_event_callback(
        event_name,
        callback
):
    u"""
    创建 Maya ``MEventMessage`` Callback，并返回对应删除函数。

    Args:
        event_name (str):
            Maya Native Event 名称，例如 ``SelectionChanged``。
        callback (callable):
            Event 触发时由 Maya 调用的函数。

    Returns:
        callable:
        无参数删除函数；调用后移除本次创建的 Maya Callback。

    Raises:
        ValueError:
        ``event_name`` 为空时抛出。
        TypeError:
        ``callback`` 不是可调用对象时抛出。
    """
    if not event_name:
        raise ValueError(
            u"event_name 不能为空。"
        )

    if not callable(callback):
        raise TypeError(
            u"callback 必须是可调用对象。"
        )

    callback_id = om.MEventMessage.addEventCallback(
        event_name,
        callback
    )

    remove_callback = partial(
        om.MMessage.removeCallback,
        callback_id
    )

    return remove_callback


# =============================================================================
# Scene State
# =============================================================================

def get_current_scene_path():
    u"""
    返回当前 Maya Scene 的规范路径；未保存时返回空字符串。

    Returns:
        str:
        当前 Scene 的规范化文件路径；Untitled Scene 返回空字符串。
    """
    scene_path = cmds.file(
        query=True,
        sceneName=True
    )

    if not scene_path:
        return ""

    return file_utils.normalize_path(
        scene_path
    )


def is_scene_modified():
    u"""
    返回当前 Maya Scene 是否存在未保存修改。

    Returns:
        bool:
        当前 Scene 有未保存修改时返回 True，否则返回 False。
    """
    return bool(
        cmds.file(
            query=True,
            modified=True
        )
    )


def validate_scene_file(file_path):
    u"""
    检查 Maya Scene 输入文件是否存在，并返回规范化路径。

    Args:
        file_path (str):
            需要 Open / Import / Reference 的文件路径。

    Returns:
        str:
        经过 ``file_utils.normalize_path()`` 处理后的现有文件路径。

    Raises:
        ValueError:
        ``file_path`` 为空时抛出。
        RuntimeError:
        规范化后的文件路径不存在时抛出。
    """
    normalized_path = file_utils.normalize_path(
        file_path
    )

    if not normalized_path:
        raise ValueError(
            u"file_path 不能为空。"
        )

    if not os.path.isfile(normalized_path):
        raise RuntimeError(
            u"文件不存在：{}".format(
                normalized_path
            )
        )

    return normalized_path


# =============================================================================
# Scene IO
# =============================================================================

def open_scene(
        file_path,
        force=False,
        ignore_version=True
):
    u"""
    打开 Maya Scene；Core 不弹保存确认窗口。

    Args:
        file_path (str):
            需要打开的 Maya Scene 文件路径。
        force (bool):
            是否允许 Maya 强制打开文件；False 时若当前 Scene 有未保存修改会先拒绝操作。
        ignore_version (bool):
            是否让 Maya 忽略文件版本差异。

    Returns:
        str:
        成功打开后的规范化 Scene 文件路径。

    Raises:
        RuntimeError:
        文件不存在，或当前 Scene 有未保存修改且 ``force=False`` 时抛出。
    """
    normalized_path = validate_scene_file(
        file_path
    )

    if is_scene_modified() and not force:
        raise RuntimeError(
            u"当前场景存在未保存修改，请确认后使用 force=True 打开新场景。"
        )

    cmds.file(
        normalized_path,
        open=True,
        ignoreVersion=ignore_version,
        force=force
    )

    return normalized_path


def import_scene(
        file_path,
        ignore_version=True
):
    u"""
    将 Maya Scene 导入当前场景，并返回本次新创建节点。

    Args:
        file_path (str):
            需要 Import 的 Maya Scene 文件路径。
        ignore_version (bool):
            是否让 Maya 忽略文件版本差异。

    Returns:
        list[str]:
        本次 Import 新创建的 Maya Node；没有新节点时返回空列表。

    Raises:
        RuntimeError:
        输入文件不存在时抛出。
    """
    normalized_path = validate_scene_file(
        file_path
    )

    imported_nodes = cmds.file(
        normalized_path,
        i=True,
        ignoreVersion=ignore_version,
        returnNewNodes=True
    )

    if imported_nodes is None:
        imported_nodes = []

    return imported_nodes


def reference_scene(
        file_path,
        namespace=None,
        group_reference=False,
        group_name=None,
        ignore_version=True
):
    u"""
    在当前 Maya Scene 创建 Reference，并返回 Maya Reference Node。

    ``namespace`` 未指定时使用输入文件名 Stem。

    Args:
        file_path (str):
            需要 Reference 的 Maya Scene 文件路径。
        namespace (str | None):
            Reference Namespace；None 时使用文件名 Stem。
        group_reference (bool):
            是否让 Maya 为本次 Reference 创建 Reference Group。
        group_name (str | None):
            ``group_reference=True`` 时可选的 Reference Group 名称。
        ignore_version (bool):
            是否让 Maya 忽略文件版本差异。

    Returns:
        str:
        Maya 为本次 Reference 创建的 Reference Node 名称。

    Raises:
        RuntimeError:
        输入文件不存在时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    normalized_path = validate_scene_file(
        file_path
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if namespace is None:
        namespace = file_utils.get_file_stem(
            normalized_path
        )

    reference_kwargs = {
        "reference": True,
        "ignoreVersion": ignore_version,
        "namespace": namespace,
        "returnNewNodes": False,
    }

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if group_reference:
        reference_kwargs["groupReference"] = True

        if group_name:
            reference_kwargs["groupName"] = group_name

    reference_file = cmds.file(
        normalized_path,
        **reference_kwargs
    )

    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    reference_node = cmds.file(
        reference_file,
        query=True,
        referenceNode=True
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return reference_node


__all__ = [
    "open_undo_chunk",
    "close_undo_chunk",
    "undo_chunk",
    "validate_node",
    "ensure_nodes_available",
    "get_long_name",
    "create_node",
    "get_nodes_by_type",
    "get_selected_nodes",
    "ensure_object_set",
    "create_native_event_callback",
    "get_current_scene_path",
    "is_scene_modified",
    "validate_scene_file",
    "open_scene",
    "import_scene",
    "reference_scene",
]
