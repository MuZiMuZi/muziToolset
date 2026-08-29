# coding=utf-8
u"""
Animation IO Utils
==================

Maya 动画关键帧 JSON 导入导出底层工具。

从旧 fileUtils.export_animation_json / import_animation_json 重构而来。

职责：
    1. 查询节点上真实存在关键帧的属性；
    2. 把 Key Time / Value 保存成结构化 JSON；
    3. 从 JSON 恢复关键帧；
    4. 支持节点名称映射，方便 Namespace / 角色实例之间迁移动画。

说明：
    - 本模块只保存基础 Key Time / Value；
    - 不负责 PySide 文件选择窗口；
    - 不硬编码测试动画路径；
    - JSON 文件读写统一复用 core.file_utils。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import file_utils


format_name = "muzi_animation"
format_version = 1


# =============================================================================
# Query
# =============================================================================

def normalize_nodes(nodes):
    """把单个节点或节点列表统一成有效节点列表。"""
    if nodes is None:
        return []

    if isinstance(nodes, str):
        nodes = [nodes]

    valid_nodes = []

    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        valid_nodes.append(node)

    return valid_nodes


def get_keyed_plugs(node):
    """返回节点上当前存在关键帧的可动画 Plug。"""
    if not cmds.objExists(node):
        return []

    animatable_plugs = cmds.listAnimatable(node)

    if animatable_plugs is None:
        animatable_plugs = []

    keyed_plugs = []

    for plug in animatable_plugs:
        key_count = cmds.keyframe(
            plug,
            query=True,
            keyframeCount=True
        )

        if not key_count:
            continue

        if plug not in keyed_plugs:
            keyed_plugs.append(plug)

    return keyed_plugs


def get_attribute_name(plug):
    """从完整 Plug 名称中取得 Attribute 名。"""
    if "." not in plug:
        return ""

    return plug.split(".", 1)[1]


def get_key_data(plug):
    """返回一个 Plug 的基础 Key Time / Value 数据。"""
    times = cmds.keyframe(
        plug,
        query=True,
        timeChange=True
    )

    values = cmds.keyframe(
        plug,
        query=True,
        valueChange=True
    )

    if times is None:
        times = []

    if values is None:
        values = []

    key_count = min(
        len(times),
        len(values)
    )

    keys = []
    key_index = 0

    while key_index < key_count:
        key_info = {
            "time": float(times[key_index]),
            "value": float(values[key_index]),
        }

        keys.append(key_info)
        key_index += 1

    return keys


def collect_animation(nodes):
    """把节点列表转换成可直接 JSON 序列化的动画数据。"""
    valid_nodes = normalize_nodes(nodes)

    animation_nodes = []

    for node in valid_nodes:
        keyed_plugs = get_keyed_plugs(node)
        attributes = []

        for plug in keyed_plugs:
            attribute_name = get_attribute_name(plug)

            if not attribute_name:
                continue

            keys = get_key_data(plug)

            if not keys:
                continue

            attribute_info = {
                "name": attribute_name,
                "keys": keys,
            }

            attributes.append(attribute_info)

        if not attributes:
            continue

        node_info = {
            "name": node,
            "attributes": attributes,
        }

        animation_nodes.append(node_info)

    data = {
        "format": format_name,
        "version": format_version,
        "nodes": animation_nodes,
    }

    return data


# =============================================================================
# Export
# =============================================================================

def export_animation(
        nodes,
        file_path
):
    """把给定节点动画导出成 JSON。"""
    valid_nodes = normalize_nodes(nodes)

    if not valid_nodes:
        raise RuntimeError(u"没有可导出的 Maya 节点。")

    data = collect_animation(valid_nodes)

    if not data["nodes"]:
        raise RuntimeError(u"给定节点上没有可导出的关键帧。")

    return file_utils.write_json(
        file_path=file_path,
        data=data,
        indent=4,
        ensure_ascii=False,
        sort_keys=False
    )


def export_selected_animation(file_path):
    """导出当前选择节点的动画。"""
    selected_nodes = cmds.ls(
        selection=True,
        long=True
    )

    if selected_nodes is None:
        selected_nodes = []

    return export_animation(
        nodes=selected_nodes,
        file_path=file_path
    )


# =============================================================================
# Import
# =============================================================================

def validate_animation_data(data):
    """检查 Muzi Animation JSON 基础结构。"""
    if not isinstance(data, dict):
        raise RuntimeError(u"动画 JSON 根数据必须是字典。")

    if data.get("format") != format_name:
        raise RuntimeError(
            u"不是 Muzi Animation JSON：{}".format(
                data.get("format")
            )
        )

    version = data.get("version")

    if version != format_version:
        raise RuntimeError(
            u"不支持的动画 JSON 版本：{}".format(version)
        )

    nodes = data.get("nodes")

    if not isinstance(nodes, list):
        raise RuntimeError(u"动画 JSON 缺少有效 nodes 列表。")

    return True


def resolve_target_node(source_node, node_map=None):
    """根据可选 node_map 解析导入目标节点。"""
    if node_map is None:
        return source_node

    if source_node in node_map:
        return node_map[source_node]

    return source_node


def apply_attribute_keys(
        target_node,
        attribute_info,
        clear_existing=False
):
    """把一个属性的 Key 数据写入目标节点。"""
    attribute_name = attribute_info.get("name")
    keys = attribute_info.get("keys")

    if not attribute_name:
        return 0

    if not isinstance(keys, list):
        return 0

    plug = "{}.{}".format(
        target_node,
        attribute_name
    )

    if not cmds.objExists(plug):
        return 0

    if clear_existing:
        try:
            cmds.cutKey(
                plug,
                clear=True
            )
        except RuntimeError:
            pass

    created_count = 0

    for key_info in keys:
        if not isinstance(key_info, dict):
            continue

        if "time" not in key_info:
            continue

        if "value" not in key_info:
            continue

        key_time = float(
            key_info["time"]
        )

        key_value = float(
            key_info["value"]
        )

        try:
            cmds.setKeyframe(
                target_node,
                attribute=attribute_name,
                time=key_time,
                value=key_value
            )
            created_count += 1
        except RuntimeError:
            continue

    return created_count


def import_animation(
        file_path,
        node_map=None,
        clear_existing=False,
        strict=False
):
    """
    从 Muzi Animation JSON 导入关键帧。

    Args:
        file_path(str): JSON 文件路径。
        node_map(dict/None):
            可选节点映射，例如：

                {
                    "ctrl_lf_arm_001": "characterA:ctrl_lf_arm_001"
                }

        clear_existing(bool):
            True 时导入某个属性前清除该属性已有 Key。

        strict(bool):
            True 时遇到缺失节点直接报错；False 时记录并跳过。

    Returns:
        dict: created_keys / imported_nodes / missing_nodes。
    """
    data = file_utils.read_json(file_path)
    validate_animation_data(data)

    created_keys = 0
    imported_nodes = []
    missing_nodes = []

    animation_nodes = data.get("nodes")

    for node_info in animation_nodes:
        if not isinstance(node_info, dict):
            continue

        source_node = node_info.get("name")

        if not source_node:
            continue

        target_node = resolve_target_node(
            source_node=source_node,
            node_map=node_map
        )

        if not cmds.objExists(target_node):
            missing_nodes.append(target_node)

            if strict:
                raise RuntimeError(
                    u"导入动画时找不到目标节点：{}".format(
                        target_node
                    )
                )

            continue

        attributes = node_info.get("attributes")

        if not isinstance(attributes, list):
            continue

        node_created_keys = 0

        for attribute_info in attributes:
            node_created_keys += apply_attribute_keys(
                target_node=target_node,
                attribute_info=attribute_info,
                clear_existing=clear_existing
            )

        if node_created_keys > 0:
            created_keys += node_created_keys
            imported_nodes.append(target_node)

    return {
        "created_keys": created_keys,
        "imported_nodes": imported_nodes,
        "missing_nodes": missing_nodes,
    }


__all__ = [
    "format_name",
    "format_version",
    "normalize_nodes",
    "get_keyed_plugs",
    "get_attribute_name",
    "get_key_data",
    "collect_animation",
    "export_animation",
    "export_selected_animation",
    "validate_animation_data",
    "resolve_target_node",
    "apply_attribute_keys",
    "import_animation",
]
