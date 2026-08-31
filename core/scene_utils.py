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
4. get_selected_nodes() 只负责查询 Selection，不规定工具必须选择多少对象；
5. 特定文件格式的导出逻辑不继续堆进 Scene Core。
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
    u"""打开一个 Maya Undo Chunk。"""
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
    u"""关闭当前 Maya Undo Chunk。"""
    cmds.undoInfo(
        closeChunk=True
    )
    return True


def undo_chunk(function):
    u"""把一次完整工具执行包装成一个 Maya Undo Chunk。"""

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

    Plug / Component 不属于 Node，因此例如：
        pCube1.translateX
        pCube1.vtx[0]
    都会被拒绝。
    """
    display_label = label or u"Maya 节点"

    if node is None:
        raise RuntimeError(
            u"{}名称不能为空。".format(
                display_label
            )
        )

    node = str(node).strip()

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

    if not cmds.objExists(node):
        raise RuntimeError(
            u"{}不存在：{}".format(
                display_label,
                node
            )
        )

    return True


def get_long_name(node):
    u"""
    返回唯一 Maya DAG Long Path；非 DAG 节点返回 Maya 查询得到的节点名。

    短名称对应多个 DAG 节点时拒绝猜测。
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
    hierarchy_utils.parent()。
    """
    if not node_type:
        raise ValueError(
            u"node_type 不能为空。"
        )

    if not name:
        raise ValueError(
            u"节点名称不能为空。"
        )

    if cmds.objExists(name):
        raise RuntimeError(
            u"节点已经存在：{}".format(
                name
            )
        )

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

    return cmds.createNode(
        node_type,
        name=name
    )


# =============================================================================
# Selection
# =============================================================================

def get_selected_nodes(
        node_type=None,
        long=True,
        flatten=True
):
    u"""返回当前 Maya Selection，可选按 Maya Node Type 过滤。"""
    selected_nodes = cmds.ls(
        selection=True,
        long=long,
        flatten=flatten
    )

    if selected_nodes is None:
        selected_nodes = []

    if node_type is None:
        return selected_nodes

    filtered_nodes = []

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

    return filtered_nodes


# =============================================================================
# Object Set
# =============================================================================

def ensure_object_set(
        set_name,
        objects=None,
        parent_set=None
):
    u"""创建或复用 Object Set，并可安全加入对象和父 Set。"""
    if not set_name:
        raise ValueError(
            u"Set 名称不能为空。"
        )

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

    return set_name


# =============================================================================
# Maya Native Callback
# =============================================================================

def create_native_event_callback(
        event_name,
        callback
):
    u"""创建 Maya MEventMessage Callback，并返回对应的删除函数。"""
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
    u"""返回当前 Maya Scene 的规范路径；未保存时返回空字符串。"""
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
    u"""返回当前 Maya Scene 是否存在未保存修改。"""
    return bool(
        cmds.file(
            query=True,
            modified=True
        )
    )


def validate_scene_file(file_path):
    u"""检查 Maya Scene 文件是否存在，并返回规范化路径。"""
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
    u"""打开 Maya Scene；Core 不弹保存确认窗口。"""
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
    u"""将 Maya Scene 导入当前场景，并返回本次新创建节点。"""
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

    namespace 未指定时使用文件名 Stem。
    """
    normalized_path = validate_scene_file(
        file_path
    )

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

    if group_reference:
        reference_kwargs["groupReference"] = True

        if group_name:
            reference_kwargs["groupName"] = group_name

    reference_file = cmds.file(
        normalized_path,
        **reference_kwargs
    )

    reference_node = cmds.file(
        reference_file,
        query=True,
        referenceNode=True
    )

    return reference_node


# =============================================================================
# Legacy Compatibility
# =============================================================================

def require_selected_nodes(
        node_type=None,
        minimum_count=1
):
    u"""
    旧 Selection Workflow 兼容入口。

    新代码应直接使用 get_selected_nodes()，并在 Tool 层判断数量。
    本函数不属于正式 Scene Core API。
    """
    selected_nodes = get_selected_nodes(
        node_type=node_type,
        long=True,
        flatten=True
    )

    if len(selected_nodes) < minimum_count:
        if node_type:
            raise RuntimeError(
                u"请至少选择 {} 个 {} 节点。".format(
                    minimum_count,
                    node_type
                )
            )

        raise RuntimeError(
            u"请至少选择 {} 个 Maya 节点。".format(
                minimum_count
            )
        )

    return selected_nodes


def ensure_fbx_plugin_loaded():
    u"""
    旧 FBX 兼容入口。

    新代码请使用 core.export_utils.ensure_fbx_plugin_loaded()。
    """
    from . import export_utils

    return export_utils.ensure_fbx_plugin_loaded()


def export_selected_fbx(file_path):
    u"""
    旧 FBX Selection 兼容入口。

    新代码请使用 export_utils.export_fbx(objects, file_path)。
    """
    from . import export_utils

    selected_nodes = get_selected_nodes(
        long=True,
        flatten=False
    )

    if not selected_nodes:
        raise RuntimeError(
            u"导出 FBX 前请先选择对象。"
        )

    return export_utils.export_fbx(
        selected_nodes,
        file_path
    )


__all__ = [
    "open_undo_chunk",
    "close_undo_chunk",
    "undo_chunk",
    "validate_node",
    "get_long_name",
    "create_node",
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
