# coding=utf-8
u"""
Scene Utils
===========

Maya 场景级通用底层工具。

从旧 pipelineUtils 中拆出的职责：
    - 创建 Maya 节点并可选匹配 Transform；
    - 获取当前选择并按节点类型过滤；
    - 创建 / 更新 Object Set；
    - 创建 Maya Native Event Callback；
    - Maya Undo Chunk 装饰器。

不包含：
    Constraint / Curve / Surface / Skin / Controller 等具体业务。
"""

from __future__ import print_function

from functools import partial
from functools import wraps

import maya.cmds as cmds
import maya.api.OpenMaya as om


# =============================================================================
# Undo
# =============================================================================

def undo_chunk(function):
    """把一个函数执行过程包装成一个 Maya Undo Chunk。"""
    @wraps(function)
    def wrapped(*args, **kwargs):
        cmds.undoInfo(
            openChunk=True,
            chunkName=function.__name__
        )

        try:
            return function(
                *args,
                **kwargs
            )
        finally:
            cmds.undoInfo(
                closeChunk=True
            )

    return wrapped


# =============================================================================
# Node
# =============================================================================

def validate_node(node):
    """检查 Maya 节点是否存在。"""
    if not node:
        raise RuntimeError(u"节点名称不能为空。")

    if not cmds.objExists(node):
        raise RuntimeError(
            u"Maya 节点不存在：{}".format(node)
        )

    return True


def get_long_name(node):
    """返回唯一 Maya DAG 长路径；非 DAG 节点返回原名称。"""
    validate_node(node)

    matches = cmds.ls(
        node,
        long=True
    )

    if matches is None:
        matches = []

    if not matches:
        return node

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
        match_node=None,
        parent=None
):
    """
    创建 Maya 节点，可选择匹配另一个 Transform 并指定 Parent。

    与旧 Pipeline.create_node() 相比，不再使用额外 match bool；
    给定 match_node 就执行匹配，不给就不匹配。
    """
    if not node_type:
        raise ValueError(u"node_type 不能为空。")

    if not name:
        raise ValueError(u"节点名称不能为空。")

    if cmds.objExists(name):
        raise RuntimeError(
            u"节点已经存在：{}".format(name)
        )

    node = cmds.createNode(
        node_type,
        name=name
    )

    if match_node:
        validate_node(match_node)

        cmds.matchTransform(
            node,
            match_node,
            position=True,
            rotation=True,
            scale=False
        )

    if parent:
        validate_node(parent)

        parent_result = cmds.parent(
            node,
            parent
        )

        if parent_result:
            node = parent_result[0]

    return node


# =============================================================================
# Selection
# =============================================================================

def get_selected_nodes(
        node_type=None,
        long=True,
        flatten=True
):
    """返回当前 Maya 选择，可按节点类型过滤。"""
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


def require_selected_nodes(
        node_type=None,
        minimum_count=1
):
    """获取选择并检查最小数量，不满足时抛出明确错误。"""
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


# =============================================================================
# Object Set
# =============================================================================

def ensure_object_set(
        set_name,
        objects=None,
        parent_set=None
):
    """
    创建或复用 Object Set，并可加入对象和父 Set。

    Returns:
        str: Object Set 名称。
    """
    if not set_name:
        raise ValueError(u"Set 名称不能为空。")

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
            objects = [objects]

        for scene_object in objects:
            if not scene_object:
                continue

            validate_node(scene_object)

            cmds.sets(
                scene_object,
                edit=True,
                forceElement=set_name
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
            forceElement=parent_set
        )

    return set_name


# =============================================================================
# Maya Native Callback
# =============================================================================

def create_native_event_callback(
        event_name,
        callback
):
    """
    创建 Maya MEventMessage Callback。

    Returns:
        callable: 调用该函数即可删除 Callback。
    """
    if not event_name:
        raise ValueError(u"event_name 不能为空。")

    if not callable(callback):
        raise TypeError(u"callback 必须是可调用对象。")

    callback_id = om.MEventMessage.addEventCallback(
        event_name,
        callback
    )

    remove_callback = partial(
        om.MMessage.removeCallback,
        callback_id
    )

    return remove_callback


__all__ = [
    "undo_chunk",
    "validate_node",
    "get_long_name",
    "create_node",
    "get_selected_nodes",
    "require_selected_nodes",
    "ensure_object_set",
    "create_native_event_callback",
]
