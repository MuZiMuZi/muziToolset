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
- Transform / Joint Parent 与 Unparent；
- 确保通用 Transform Group 存在于指定层级；
- 在 Transform / Joint 上方插入 Parent Group。

模块边界
--------
本模块只处理 DAG 层级关系，不读取 Selection，也不创建任何 Face / Body /
Controller 项目结构。具体 Rig Hierarchy 由对应 systems 模块组合这些 API 创建。

设计原则
--------
1. 无状态 Utils 使用模块函数，不使用只有 staticmethod 的包装类；
2. Query 接口接受通用 DAG Node，Parent 写操作只接受 Transform / Joint；
3. 所有 DAG 查询先解析唯一 Long Path，不对重名节点做猜测；
4. Parent / Child API 不依赖当前 Selection；
5. Transform 数值读写复用 transform_utils；
6. Ensure 语义必须同时保证“节点存在”和“Parent 正确”。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import scene_utils
from . import transform_utils


# =============================================================================
# Internal
# =============================================================================

def _get_dag_long_name(
        node,
        label=None
):
    u"""验证输入为唯一 DAG Node，并返回 Long Path。"""
    display_label = label or u"DAG 节点"

    scene_utils.validate_node(
        node,
        label=display_label
    )

    long_name = scene_utils.get_long_name(
        node
    )

    is_dag_node = cmds.objectType(
        long_name,
        isAType="dagNode"
    )

    if not is_dag_node:
        raise RuntimeError(
            u"{}必须是 DAG Node：{}".format(
                display_label,
                node
            )
        )

    return long_name


def _get_path_depth(path):
    u"""返回已经解析好的 DAG Long Path 深度。"""
    return path.count(
        "|"
    )


def _get_transform_long_name(
        node,
        label
):
    u"""验证 Transform / Joint，并返回唯一 Long Path。"""
    long_name = scene_utils.get_long_name(
        node
    )

    transform_utils.validate_transform(
        long_name
    )

    return long_name


# =============================================================================
# Query
# =============================================================================

def get_dag_depth(node):
    u"""
    返回唯一 DAG Long Path 的层级深度；World 下节点为 1。

    Args:
        node (str):
            需要查询 DAG 层级深度的 Maya 节点名称或唯一 DAG Path。

    Returns:
        int:
        节点 Long Path 的 DAG 深度；直接位于 World 下的节点返回 1。
    """
    long_name = _get_dag_long_name(
        node
    )

    return _get_path_depth(
        long_name
    )


def get_parent(
        node,
        full_path=True
):
    u"""
    返回 DAG 节点的直接 Parent；没有 Parent 时返回 None。

    Args:
        node (str):
            需要查询直接 Parent 的 Maya DAG 节点名称或唯一 DAG Path。
        full_path (bool):
            True 时返回 Parent Long Path；False 时返回 Maya Short Name。

    Returns:
        str | None:
        直接 Parent 名称；节点位于 World 下时返回 None。
    """
    long_name = _get_dag_long_name(
        node
    )

    parents = cmds.listRelatives(
        long_name,
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
    u"""
    返回 DAG 节点的直接 Child，可选按 Maya Node Type 过滤。

    Args:
        node (str):
            需要查询直接 Child 的 Maya DAG 节点名称或唯一 DAG Path。
        node_type (str | None):
            可选 Maya Node Type，例如 ``joint`` 或 ``transform``；None 表示不过滤类型。
        full_path (bool):
            True 时返回 Child Long Path；False 时返回 Maya Short Name。

    Returns:
        list[str]:
        按 Maya DAG 查询结果顺序返回的直接 Child 列表；没有 Child 时返回空列表。
    """
    long_name = _get_dag_long_name(
        node
    )

    kwargs = {
        "children": True,
        "fullPath": full_path,
    }

    if node_type:
        kwargs["type"] = node_type

    return cmds.listRelatives(
        long_name,
        **kwargs
    ) or []


def get_descendants(
        node,
        node_type=None,
        include_root=False,
        full_path=True
):
    u"""
    返回 DAG 节点的全部后代，并明确保证由浅到深排序。

    ``include_root=True`` 时，Root 同样遵守 ``node_type`` 过滤规则。
    ``full_path=True`` 时，Root 和 Descendant 全部返回 Long Path。

    Args:
        node (str):
            作为 Descendant 查询起点的 Maya DAG Root 节点名称或唯一 DAG Path。
        node_type (str | None):
            可选 Maya Node Type；提供后只返回该类型的 Root / Descendant。
        include_root (bool):
            是否把查询起点本身加入结果；Root 仍会遵守 ``node_type`` 过滤。
        full_path (bool):
            True 时统一返回 Long Path；False 时返回 Maya Short Name。

    Returns:
        list[str]:
        由浅到深排列的 Descendant 列表；启用 ``include_root`` 时 Root 位于最前面。
    """
    root_long_name = _get_dag_long_name(
        node
    )

    kwargs = {
        "allDescendents": True,
        "fullPath": True,
    }

    if node_type:
        kwargs["type"] = node_type

    descendants = cmds.listRelatives(
        root_long_name,
        **kwargs
    ) or []

    descendants.sort(
        key=_get_path_depth
    )

    result = []

    if include_root:
        include_current_root = True

        if node_type:
            root_type = cmds.nodeType(
                root_long_name
            )
            include_current_root = root_type == node_type

        if include_current_root:
            if full_path:
                result.append(
                    root_long_name
                )
            else:
                result.append(
                    root_long_name.split("|")[-1]
                )

    for descendant in descendants:
        if full_path:
            result.append(
                descendant
            )
        else:
            result.append(
                descendant.split("|")[-1]
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
    设置 Transform / Joint Parent，并保持 Child 当前世界姿态。

    ``parent_node=None`` 表示 Parent 到 World。
    所有成功路径统一返回 Child 最新的唯一 Long Path。

    Args:
        child_node (str):
            需要重新挂接 Parent 的 Transform 或 Joint 节点名称。
        parent_node (str | None):
            Child 最终需要挂接到的 Transform / Joint；None 表示挂到 World。

    Returns:
        str:
        Parent 操作完成后 Child 最新的唯一 DAG Long Path。

    Raises:
        RuntimeError:
        Child / Parent 无效、不是 Transform / Joint，或尝试 Parent 到自身时抛出。
    """
    child_long_name = _get_transform_long_name(
        child_node,
        label=u"子节点"
    )

    current_parent = get_parent(
        child_long_name,
        full_path=True
    )

    if parent_node is None:
        if current_parent is None:
            return child_long_name

        result = cmds.parent(
            child_long_name,
            world=True,
            absolute=True
        )

        if not result:
            return scene_utils.get_long_name(
                child_long_name
            )

        return scene_utils.get_long_name(
            result[0]
        )

    parent_long_name = _get_transform_long_name(
        parent_node,
        label=u"父节点"
    )

    if child_long_name == parent_long_name:
        raise RuntimeError(
            u"节点不能 Parent 到自身：{}".format(
                child_long_name
            )
        )

    if current_parent == parent_long_name:
        return child_long_name

    result = cmds.parent(
        child_long_name,
        parent_long_name,
        absolute=True
    )

    if not result:
        return scene_utils.get_long_name(
            child_long_name
        )

    return scene_utils.get_long_name(
        result[0]
    )


# =============================================================================
# Group
# =============================================================================

def ensure_group(
        name,
        parent_node=None
):
    u"""
    确保一个 Transform Group 存在，并处于指定 Parent 下。

    ``parent_node=None`` 表示该 Group 应位于 World。
    已存在但 Parent 错误时会通过 ``parent()`` 修正层级，同时保持世界姿态。

    Args:
        name (str):
            需要创建或复用的 Transform Group 名称；必须能唯一解析现有同名 DAG 节点。
        parent_node (str | None):
            Group 应处于的 Transform / Joint Parent；None 表示 Group 必须位于 World 下。

    Returns:
        str:
        已确认存在且 Parent 正确的 Group 唯一 DAG Long Path。

    Raises:
        RuntimeError:
        Group 名称为空、现有名称被非 Transform 节点占用，或 Parent 无效时抛出。
    """
    if name is None:
        raise RuntimeError(
            u"Group 名称不能为空。"
        )

    name = str(name).strip()

    if not name:
        raise RuntimeError(
            u"Group 名称不能为空。"
        )

    parent_long_name = None

    if parent_node is not None:
        parent_long_name = _get_transform_long_name(
            parent_node,
            label=u"Group Parent"
        )

    if cmds.objExists(name):
        group_long_name = scene_utils.get_long_name(
            name
        )
        node_type = cmds.nodeType(
            group_long_name
        )

        if node_type != "transform":
            raise RuntimeError(
                u"Group 名称已被非 Transform 节点占用：{} | type={}".format(
                    name,
                    node_type
                )
            )

        current_parent = get_parent(
            group_long_name,
            full_path=True
        )

        if parent_long_name is None:
            if current_parent is None:
                return group_long_name

            return parent(
                group_long_name,
                None
            )

        if current_parent == parent_long_name:
            return group_long_name

        return parent(
            group_long_name,
            parent_long_name
        )

    group = scene_utils.create_node(
        "transform",
        name,
        parent=parent_long_name
    )

    return scene_utils.get_long_name(
        group
    )


def insert_parent_group(
        node,
        group_name,
        match_rotation=True
):
    u"""
    在 Transform / Joint 与原 Parent 之间插入一个新 Group。

    新 Group 匹配对象世界位置；``match_rotation=True`` 时同时匹配对象世界旋转，
    否则 Group 使用 World Orientation。函数不复制 Child Local Scale。
    Child 通过 ``parent(..., absolute=True)`` 保持当前世界姿态。

    Args:
        node (str):
            需要插入 Parent Group 的 Transform 或 Joint 节点名称。
        group_name (str):
            新建 Parent Group 的名称；该名称在当前场景中必须尚未被占用。
        match_rotation (bool):
            True 时新 Group 匹配 Child 世界旋转；False 时新 Group 保持 World Orientation。

    Returns:
        str:
        新建 Parent Group 的唯一 DAG Long Path。

    Raises:
        RuntimeError:
        输入节点无效、Group 名称为空，或 Group 名称已经被占用时抛出。
    """
    node_long_name = _get_transform_long_name(
        node,
        label=u"插组对象"
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
        node_long_name
    )
    rotation = [0.0, 0.0, 0.0]

    if match_rotation:
        rotation = transform_utils.get_world_rotation(
            node_long_name
        )

    original_parent = get_parent(
        node_long_name,
        full_path=True
    )

    object_group = scene_utils.create_node(
        "transform",
        group_name
    )

    if original_parent is not None:
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

    parent(
        node_long_name,
        object_group
    )

    return scene_utils.get_long_name(
        object_group
    )


__all__ = [
    "get_dag_depth",
    "get_parent",
    "get_children",
    "get_descendants",
    "parent",
    "ensure_group",
    "insert_parent_group",
]
