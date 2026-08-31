# coding=utf-8
u"""
Hierarchy Utils
===============

Maya DAG 层级通用底层工具。

模块职责
--------
- DAG 深度；
- Direct Parent / Child 查询；
- Descendant 查询；
- Parent / Unparent；
- 通用 Transform Group 创建；
- 在对象上方插入 Extra Group。

模块边界
--------
本模块只处理 DAG 层级关系，不读取 Selection，也不创建任何 Face / Body /
Controller 项目结构。具体 Rig Hierarchy 由对应 systems 模块组合这些 API 创建。

设计原则
--------
1. 无状态 Utils 使用模块函数，不使用只有 staticmethod 的包装类；
2. 每个外部 Maya Node 参数在函数入口校验；
3. Parent / Child API 不依赖当前 Selection；
4. Transform 数值读写复用 transform_utils。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import scene_utils
from . import transform_utils


# =============================================================================
# Query
# =============================================================================

def get_dag_depth(node):
    u"""返回唯一 DAG Long Path 的层级深度；Root 为 1。"""
    long_name = scene_utils.get_long_name(
        node
    )

    if not long_name:
        return 0

    return long_name.count(
        "|"
    )


def get_parent(node, full_path=True):
    u"""返回 DAG 节点的直接 Parent；没有 Parent 时返回 None。"""
    scene_utils.validate_node(
        node
    )

    parents = cmds.listRelatives(
        node,
        parent=True,
        fullPath=full_path
    ) or []

    if not parents:
        return None

    return parents[0]


def get_children(
        node,
        node_type=None,
        full_path=True
):
    u"""返回 DAG 节点的直接 Child，可选按 Maya Node Type 过滤。"""
    scene_utils.validate_node(
        node
    )

    kwargs = {
        "children": True,
        "fullPath": full_path,
    }

    if node_type:
        kwargs["type"] = node_type

    return cmds.listRelatives(
        node,
        **kwargs
    ) or []


def get_descendants(
        node,
        node_type=None,
        include_root=False,
        full_path=True
):
    u"""返回 DAG 节点的全部后代，并整理成由浅到深的顺序。"""
    scene_utils.validate_node(
        node
    )

    kwargs = {
        "allDescendents": True,
        "fullPath": full_path,
    }

    if node_type:
        kwargs["type"] = node_type

    descendants = cmds.listRelatives(
        node,
        **kwargs
    ) or []

    descendants.reverse()

    result = []

    if include_root:
        result.append(
            node
        )

    for descendant in descendants:
        result.append(
            descendant
        )

    return result


# =============================================================================
# Parent
# =============================================================================

def parent(
        child_node,
        parent_node=None
):
    u"""
    设置 DAG Parent，并保持 Child 当前世界姿态。

    ``parent_node=None`` 表示 Parent 到 World。
    """
    scene_utils.validate_node(
        child_node,
        label=u"子节点"
    )

    if parent_node is None:
        current_parent = get_parent(
            child_node,
            full_path=True
        )

        if current_parent is None:
            return child_node

        result = cmds.parent(
            child_node,
            world=True,
            absolute=True
        )

        if result:
            return result[0]

        return child_node

    scene_utils.validate_node(
        parent_node,
        label=u"父节点"
    )

    current_parent = get_parent(
        child_node,
        full_path=True
    )
    parent_matches = cmds.ls(
        parent_node,
        long=True
    ) or []

    parent_long_name = parent_node

    if parent_matches:
        parent_long_name = parent_matches[0]

    if current_parent == parent_long_name:
        return child_node

    result = cmds.parent(
        child_node,
        parent_node,
        absolute=True
    )

    if result:
        return result[0]

    return child_node


# =============================================================================
# Group
# =============================================================================

def create_group(
        name,
        parent=None
):
    u"""创建或复用一个 Transform Group。"""
    if name is None:
        raise RuntimeError(
            u"Group 名称不能为空。"
        )

    name = str(name).strip()

    if not name:
        raise RuntimeError(
            u"Group 名称不能为空。"
        )

    if cmds.objExists(name):
        node_type = cmds.nodeType(
            name
        )

        if node_type != "transform":
            raise RuntimeError(
                u"Group 名称已被非 Transform 节点占用：{} | type={}".format(
                    name,
                    node_type
                )
            )

        return name

    if parent is not None:
        transform_utils.validate_transform(
            parent
        )

    return cmds.createNode(
        "transform",
        name=name,
        parent=parent
    )


def add_extra_group(
        node,
        group_name,
        world_orient=False
):
    u"""在对象上方插入 Extra Group，并保持对象当前世界姿态。"""
    transform_utils.validate_transform(
        node
    )

    if group_name is None:
        raise RuntimeError(
            u"Group 名称不能为空。"
        )

    group_name = str(group_name).strip()

    if not group_name:
        raise RuntimeError(
            u"Group 名称不能为空。"
        )

    if cmds.objExists(group_name):
        raise RuntimeError(
            u"Group 名称已经存在：{}".format(
                group_name
            )
        )

    translation = transform_utils.get_world_translation(
        node
    )
    rotation = transform_utils.get_world_rotation(
        node
    )
    scale = cmds.xform(
        node,
        query=True,
        relative=True,
        scale=True
    )
    original_parent = get_parent(
        node,
        full_path=True
    )

    if world_orient:
        rotation = [0.0, 0.0, 0.0]

    object_group = cmds.createNode(
        "transform",
        name=group_name
    )

    if original_parent:
        object_group = parent(
            object_group,
            original_parent
        )

    transform_utils.set_world_translation(
        object_group,
        translation
    )
    transform_utils.set_world_rotation(
        object_group,
        rotation
    )
    cmds.xform(
        object_group,
        relative=True,
        scale=scale
    )

    parent(
        node,
        object_group
    )

    return object_group


# =============================================================================
# Transitional Compatibility
# =============================================================================

def _legacy_create_grp(grp, parent=None):
    return create_group(
        grp,
        parent=parent
    )


def _legacy_get_child_object(node, type="joint"):
    return get_descendants(
        node,
        node_type=type,
        include_root=True,
        full_path=True
    )


class _HierarchyCompatibility(object):
    u"""旧 ``Hierarchy.xxx`` 调用的过渡入口；新代码不要使用。"""

    get_dag_depth = staticmethod(get_dag_depth)
    get_parent = staticmethod(get_parent)
    get_children = staticmethod(get_children)
    get_descendants = staticmethod(get_descendants)
    parent = staticmethod(parent)
    create_group = staticmethod(create_group)
    create_grp = staticmethod(_legacy_create_grp)
    add_extra_group = staticmethod(add_extra_group)
    get_child_object = staticmethod(_legacy_get_child_object)


Hierarchy = _HierarchyCompatibility()


__all__ = [
    "get_dag_depth",
    "get_parent",
    "get_children",
    "get_descendants",
    "parent",
    "create_group",
    "add_extra_group",
]
