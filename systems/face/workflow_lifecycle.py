# coding=utf-8
u"""
Face Workflow Lifecycle
=======================

统一处理 Face Rig Workflow 的回退清理和用户数据持久化。

核心原则：
    1. 向后回退时删除目标 Step 之后创建的场景生成物；
    2. Guide 位置和 Controller Appearance 属于用户数据，不能随场景生成物一起丢失；
    3. Step 03 / 04 使用 Scene Manifest 记录本次真正新建的 Maya Node；
    4. 新版场景优先按 UUID Manifest 精确删除，旧场景没有 Manifest 时使用 Face Group 兼容清理；
    5. Guide Snapshot 使用去掉 Namespace 的标准名称保存，重新导入模板后可以恢复。

本模块只负责 Workflow 生命周期，不负责创建 Guide、Rig 或 Finalize。
"""

from __future__ import print_function

import json

import maya.cmds as cmds

from . import config


GUIDE_SNAPSHOT_ATTR = "face_guide_snapshot_json"

STEP_MANIFEST_ATTR_NAMES = {
    3: "face_step_03_scene_manifest_json",
    4: "face_step_04_scene_manifest_json",
}

STEP03_FALLBACK_GROUP_ATTR_NAMES = [
    "face_ctrl_grp",
    "face_jnt_grp",
    "face_rig_nodes_grp",
    "face_pos_driver_grp",
]


# =============================================================================
# Common Helpers
# =============================================================================


def get_canonical_node_name(node):
    u"""
    返回去掉 DAG Path 和 Maya Namespace 后的标准节点名称。

    Args:
        node (str | None):
            Maya 节点名称或 Long Path。

    Returns:
        str:
            不包含 DAG Path 和 Namespace 的节点名称。
    """
    if not node:
        return ""

    short_name = str(node).rsplit(
        "|",
        1
    )[-1]

    return short_name.rsplit(
        ":",
        1
    )[-1]


def _read_json_config(
        face_context,
        attr_name
):
    u"""
    从 Face Config 读取一个 JSON String Attribute。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。
        attr_name (str):
            保存 JSON 文本的 Config Attribute 名称。

    Returns:
        dict | None:
            成功解析时返回字典；没有数据或数据无效时返回 None。
    """
    if not face_context.config_node_exists():
        return None

    try:
        value = face_context.get_config_value(
            attr_name
        )
    except Exception:
        return None

    if not value:
        return None

    try:
        result = json.loads(
            value
        )
    except Exception:
        return None

    if not isinstance(result, dict):
        return None

    return result


def _write_json_config(
        face_context,
        attr_name,
        value
):
    u"""
    把字典保存为 Face Config 的隐藏 JSON String Attribute。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。
        attr_name (str):
            保存 JSON 文本的 Config Attribute 名称。
        value (dict):
            需要持久化的数据。

    Returns:
        bool:
            保存完成时返回 True。
    """
    value_text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True
    )

    face_context.set_config_values(
        attrs_dict={
            attr_name: value_text,
        },
        attr_types={
            attr_name: "string",
        },
        lock=True,
        hide=True
    )
    return True


def _clear_json_config(
        face_context,
        attr_name
):
    u"""
    清空一个 Workflow JSON Config Attribute，但保留 Attribute Schema。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。
        attr_name (str):
            需要清空的 Config Attribute 名称。

    Returns:
        bool:
            清空完成时返回 True。
    """
    if not face_context.config_node_exists():
        return False

    face_context.set_config_values(
        attrs_dict={
            attr_name: "",
        },
        attr_types={
            attr_name: "string",
        },
        lock=True,
        hide=True
    )
    return True


# =============================================================================
# Scene Manifest
# =============================================================================


def capture_scene_state():
    u"""
    记录当前 Maya Scene 全部节点的 UUID、名称和 Node Type。

    Returns:
        dict:
            以 UUID 为 Key 的 Scene Snapshot。
    """
    state = {
        "nodes": {},
    }

    scene_nodes = cmds.ls(
        long=True
    )

    if scene_nodes is None:
        scene_nodes = []

    for node in scene_nodes:
        uuid_values = cmds.ls(
            node,
            uuid=True
        )

        if uuid_values is None:
            uuid_values = []

        if not uuid_values:
            continue

        node_uuid = uuid_values[0]

        try:
            node_type = cmds.nodeType(
                node
            )
        except Exception:
            node_type = None

        state["nodes"][node_uuid] = {
            "uuid": node_uuid,
            "name": node,
            "type": node_type,
        }

    return state


def create_scene_manifest(before_state):
    u"""
    根据 Build 前后的 Scene Snapshot 计算本次新增节点 Manifest。

    Args:
        before_state (dict):
            capture_scene_state() 返回的 Build 前 Scene Snapshot。

    Returns:
        dict:
            只包含本次新建 Maya Node 的 Manifest。
    """
    after_state = capture_scene_state()
    before_nodes = before_state.get(
        "nodes",
        {}
    )
    after_nodes = after_state.get(
        "nodes",
        {}
    )

    created_nodes = []

    for node_uuid in after_nodes:
        if node_uuid in before_nodes:
            continue

        node_data = after_nodes.get(
            node_uuid
        )

        if not isinstance(node_data, dict):
            continue

        created_nodes.append(
            dict(node_data)
        )

    created_nodes.sort(
        key=lambda item: item.get("name", "")
    )

    return {
        "nodes": created_nodes,
    }


def save_step_manifest(
        face_context,
        step_value,
        manifest
):
    u"""
    保存 Step 03 或 Step 04 的 Scene Manifest。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。
        step_value (int):
            需要保存 Manifest 的 Workflow Step。
        manifest (dict):
            create_scene_manifest() 返回的数据。

    Returns:
        bool:
            找到对应 Manifest Attribute 并成功保存时返回 True。
    """
    attr_name = STEP_MANIFEST_ATTR_NAMES.get(
        step_value
    )

    if not attr_name:
        return False

    return _write_json_config(
        face_context,
        attr_name,
        manifest
    )


def load_step_manifest(
        face_context,
        step_value
):
    u"""
    读取 Step 03 或 Step 04 的 Scene Manifest。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。
        step_value (int):
            需要读取 Manifest 的 Workflow Step。

    Returns:
        dict | None:
            存在有效 Manifest 时返回字典，否则返回 None。
    """
    attr_name = STEP_MANIFEST_ATTR_NAMES.get(
        step_value
    )

    if not attr_name:
        return None

    return _read_json_config(
        face_context,
        attr_name
    )


def clear_step_manifest(
        face_context,
        step_value
):
    u"""
    清空某个 Step 保存的 Scene Manifest。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。
        step_value (int):
            需要清空 Manifest 的 Workflow Step。

    Returns:
        bool:
            成功找到对应 Attribute 并完成清空时返回 True。
    """
    attr_name = STEP_MANIFEST_ATTR_NAMES.get(
        step_value
    )

    if not attr_name:
        return False

    return _clear_json_config(
        face_context,
        attr_name
    )


def _get_scene_uuid_node_map():
    u"""
    返回当前 Scene 的 UUID 到 Long Name 映射。

    Returns:
        dict:
            UUID 到当前 Maya Node Long Name 的映射。
    """
    result = {}
    scene_nodes = cmds.ls(
        long=True
    )

    if scene_nodes is None:
        scene_nodes = []

    for node in scene_nodes:
        uuid_values = cmds.ls(
            node,
            uuid=True
        )

        if uuid_values is None:
            uuid_values = []

        if not uuid_values:
            continue

        result[uuid_values[0]] = node

    return result


def _node_delete_sort_key(node):
    u"""
    返回删除节点时使用的 DAG 深度排序值。

    Args:
        node (str):
            Maya Node Long Name。

    Returns:
        int:
            DAG Path 越深，返回值越大。
    """
    return str(node).count(
        "|"
    )


def delete_step_manifest_nodes(
        face_context,
        step_value
):
    u"""
    按保存的 UUID Manifest 删除某个 Step 真正创建的 Maya Node。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。
        step_value (int):
            需要清理生成物的 Workflow Step。

    Returns:
        list[str] | None:
            有 Manifest 时返回实际尝试删除的节点列表；没有 Manifest 时返回 None。
    """
    manifest = load_step_manifest(
        face_context,
        step_value
    )

    if manifest is None:
        return None

    manifest_nodes = manifest.get(
        "nodes",
        []
    )

    if not isinstance(manifest_nodes, list):
        manifest_nodes = []

    uuid_node_map = _get_scene_uuid_node_map()
    delete_nodes = []

    for node_data in manifest_nodes:
        if not isinstance(node_data, dict):
            continue

        node_uuid = node_data.get(
            "uuid"
        )
        node = uuid_node_map.get(
            node_uuid
        )

        if not node:
            continue

        if node in delete_nodes:
            continue

        delete_nodes.append(
            node
        )

    delete_nodes.sort(
        key=_node_delete_sort_key,
        reverse=True
    )

    deleted_nodes = []

    for node in delete_nodes:
        if not cmds.objExists(node):
            continue

        try:
            cmds.delete(
                node
            )
            deleted_nodes.append(
                node
            )
        except Exception:
            continue

    clear_step_manifest(
        face_context,
        step_value
    )
    return deleted_nodes


# =============================================================================
# Legacy Scene Fallback Cleanup
# =============================================================================


def _resolve_scene_node(
        node,
        node_type=None
):
    u"""
    按标准名称解析当前 Scene 中唯一节点，并兼容 Namespace。

    Args:
        node (str):
            Maya 节点名称、Long Path 或标准短名。
        node_type (str | None):
            可选的 Maya Node Type 限制。

    Returns:
        str | None:
            找到唯一节点时返回 Long Name，否则返回 None。
    """
    if not node:
        return None

    if cmds.objExists(node):
        if node_type is not None:
            if cmds.nodeType(node) != node_type:
                return None

        long_names = cmds.ls(
            node,
            long=True
        )

        if long_names:
            return long_names[0]

        return node

    canonical_name = get_canonical_node_name(
        node
    )
    search_kwargs = {
        "long": True,
    }

    if node_type is not None:
        search_kwargs["type"] = node_type

    candidates = cmds.ls(
        **search_kwargs
    )

    if candidates is None:
        candidates = []

    matches = []

    for candidate in candidates:
        if get_canonical_node_name(candidate) != canonical_name:
            continue

        matches.append(
            candidate
        )

    if len(matches) != 1:
        return None

    return matches[0]


def _delete_group_children(group_node):
    u"""
    删除一个 Face 基础 Group 下的全部子节点，但保留基础 Group 本身。

    Args:
        group_node (str):
            需要清空的 Face Group。

    Returns:
        list[str]:
            实际删除的直接子节点列表。
    """
    if not group_node:
        return []

    if not cmds.objExists(group_node):
        return []

    children = cmds.listRelatives(
        group_node,
        children=True,
        fullPath=True
    )

    if children is None:
        children = []

    deleted_nodes = []

    for child in children:
        if not cmds.objExists(child):
            continue

        cmds.delete(
            child
        )
        deleted_nodes.append(
            child
        )

    return deleted_nodes


def cleanup_legacy_step3_content(face_context):
    u"""
    兼容清理没有 Scene Manifest 的旧 Step 03 场景。

    只清空 Face Ctrl / Joint / Rig Nodes / Position Driver 基础 Group 的子节点，
    并删除 Face Controller Set。不会删除模型、Guide、Face Config 或基础 Group。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。

    Returns:
        list[str]:
            实际删除的场景节点列表。
    """
    deleted_nodes = []

    for group_attr_name in STEP03_FALLBACK_GROUP_ATTR_NAMES:
        configured_group = getattr(
            face_context,
            group_attr_name,
            None
        )
        group_node = _resolve_scene_node(
            configured_group,
            node_type="transform"
        )

        group_deleted_nodes = _delete_group_children(
            group_node
        )

        for deleted_node in group_deleted_nodes:
            deleted_nodes.append(
                deleted_node
            )

    controller_set = _resolve_scene_node(
        config.face_ctrl_set,
        node_type="objectSet"
    )

    if controller_set:
        if cmds.objExists(controller_set):
            cmds.delete(
                controller_set
            )
            deleted_nodes.append(
                controller_set
            )

    return deleted_nodes


# =============================================================================
# Persistent Guide Snapshot
# =============================================================================


def save_guide_snapshot(face_guide):
    u"""
    把当前 Guide Move Ctrl 和 Locator 世界矩阵持久化到 Face Config。

    Args:
        face_guide (FaceGuide):
            当前正式 FaceGuide 实例。

    Returns:
        dict | None:
            Guide 存在时返回保存后的标准化 Snapshot，否则返回 None。
    """
    if not face_guide.config_node_exists():
        return None

    if not face_guide.guide_exists():
        return None

    state = face_guide.capture_guide_state()
    normalized_state = {
        "move_ctrl_matrix": state.get(
            "move_ctrl_matrix"
        ),
        "locators": {},
    }

    locator_states = state.get(
        "locators",
        {}
    )

    for locator_name in locator_states:
        canonical_name = get_canonical_node_name(
            locator_name
        )

        if not canonical_name:
            continue

        normalized_state["locators"][canonical_name] = locator_states[locator_name]

    _write_json_config(
        face_guide,
        GUIDE_SNAPSHOT_ATTR,
        normalized_state
    )
    return normalized_state


def load_guide_snapshot(face_guide):
    u"""
    从 Face Config 读取上一次持久化的 Guide Snapshot。

    Args:
        face_guide (FaceGuide):
            当前正式 FaceGuide 实例。

    Returns:
        dict | None:
            存在有效 Snapshot 时返回字典，否则返回 None。
    """
    return _read_json_config(
        face_guide,
        GUIDE_SNAPSHOT_ATTR
    )


def restore_guide_snapshot(face_guide):
    u"""
    把持久化 Guide Snapshot 恢复到当前重新导入的 Guide Template。

    Args:
        face_guide (FaceGuide):
            当前正式 FaceGuide 实例。

    Returns:
        list[str]:
            成功恢复矩阵的 Locator 列表。
    """
    state = load_guide_snapshot(
        face_guide
    )

    if not state:
        return []

    if not face_guide.guide_exists():
        return []

    return face_guide.restore_guide_state(
        state
    )


# =============================================================================
# Workflow Rollback
# =============================================================================


def cleanup_to_step(
        face_context,
        target_step_value,
        face_guide=None
):
    u"""
    回退到指定 Step，并删除该 Step 之后创建的场景生成物。

    回退规则：
        Step 04 -> 03：删除 Step 04 新增节点，保留 Step 03 Rig；
        Step 03 -> 02：删除 Step 03 / 04 生成物，保留当前 Guide；
        Step 02 -> 01：先保存 Guide Snapshot，再删除 Guide 与 Step 03 / 04 生成物。

    Args:
        face_context (FaceBase):
            当前 Face Workflow Config 上下文。
        target_step_value (int):
            需要回退到的 Workflow Step，合法值为 1、2、3。
        face_guide (FaceGuide | None):
            可选 Guide 实例；回退到 Step 01 时用于保存和删除 Guide。

    Returns:
        dict:
            清理结果、目标 Step 和删除节点摘要。

    Raises:
        ValueError:
            target_step_value 不是 1、2、3 时抛出。
    """
    if target_step_value not in [1, 2, 3]:
        raise ValueError(
            u"Workflow 回退目标只能是 Step 01、02 或 03。"
        )

    result = {
        "target_step": target_step_value,
        "step4_deleted": [],
        "step3_deleted": [],
        "guide_snapshot_saved": False,
        "guide_removed": False,
        "used_step3_fallback": False,
    }

    if target_step_value <= 3:
        step4_deleted = delete_step_manifest_nodes(
            face_context,
            4
        )

        if step4_deleted is not None:
            result["step4_deleted"] = step4_deleted

    if target_step_value <= 2:
        step3_deleted = delete_step_manifest_nodes(
            face_context,
            3
        )

        if step3_deleted is None:
            step3_deleted = cleanup_legacy_step3_content(
                face_context
            )
            result["used_step3_fallback"] = True

        result["step3_deleted"] = step3_deleted

    if target_step_value <= 1:
        if face_guide is not None:
            if face_guide.guide_exists():
                snapshot = save_guide_snapshot(
                    face_guide
                )
                result["guide_snapshot_saved"] = bool(
                    snapshot
                )

                face_guide.remove_guide_content()
                result["guide_removed"] = True

    step_value = target_step_value + 1

    while step_value <= face_context.last_step_value:
        face_context.set_step_completed(
            step_value=step_value,
            completed=False
        )
        step_value += 1

    face_context.set_current_step_value(
        target_step_value
    )
    face_context.organize_config_attributes()
    return result


__all__ = [
    "GUIDE_SNAPSHOT_ATTR",
    "STEP_MANIFEST_ATTR_NAMES",
    "capture_scene_state",
    "create_scene_manifest",
    "save_step_manifest",
    "load_step_manifest",
    "clear_step_manifest",
    "delete_step_manifest_nodes",
    "cleanup_legacy_step3_content",
    "save_guide_snapshot",
    "load_guide_snapshot",
    "restore_guide_snapshot",
    "cleanup_to_step",
    "get_canonical_node_name",
]
