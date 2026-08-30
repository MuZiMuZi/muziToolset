# coding=utf-8
u"""
Architecture Cleanup Phase 2 Runner
===================================

给一次性 Phase 2 Migration 提供窄范围修正版和第二层 Core Single Source 清理。

原则：
    - Generic Node / DAG / Transform 能力只保留一个正式 Core 实现；
    - 领域模块直接调用对应 Core，不再保留同名薄包装；
    - Snap 对 Component 的特殊语义保留，但使用明确的 Item API 名称；
    - 不修改 Face / Controller / Skin 等业务算法。
"""

from __future__ import print_function

import architecture_cleanup_phase2 as migration


def update_scene_utils():
    u"""稳定迁移 scene_utils.validate_node(node, label=None)。"""
    path = "core/scene_utils.py"
    source_text = migration.read_text(path)

    source_text = migration.replace_required(
        source_text,
        "def validate_node(node):\n",
        "def validate_node(node, label=None):\n",
        "scene_utils.validate_node signature"
    )

    # Args 章节由后续 Docstring Normalizer 根据真实函数签名补齐。
    source_text = migration.replace_required(
        source_text,
        "    # 步骤 1：空名称没有任何查询意义，直接报错。\n"
        "    if not node:\n"
        "        raise RuntimeError(u\"节点名称不能为空。\")\n\n"
        "    # 步骤 2：使用 objExists 检查 DAG / DG 节点。\n"
        "    if not cmds.objExists(node):\n"
        "        raise RuntimeError(\n"
        "            u\"Maya 节点不存在：{}\".format(node)\n"
        "        )\n",
        "    display_label = label or u\"Maya 节点\"\n\n"
        "    # 步骤 1：空名称没有任何查询意义，直接报错。\n"
        "    if not node:\n"
        "        raise RuntimeError(\n"
        "            u\"{}名称不能为空。\".format(\n"
        "                display_label\n"
        "            )\n"
        "        )\n\n"
        "    # 步骤 2：使用 objExists 检查 DAG / DG 节点。\n"
        "    if not cmds.objExists(node):\n"
        "        raise RuntimeError(\n"
        "            u\"{}不存在：{}\".format(\n"
        "                display_label,\n"
        "                node\n"
        "            )\n"
        "        )\n",
        "scene_utils.validate_node body"
    )

    migration.write_text(
        path,
        source_text
    )


def ensure_core_import(source_text, module_name):
    u"""确保 Core 模块内存在相对模块 Import。"""
    import_text = "from . import {}\n".format(
        module_name
    )

    if import_text in source_text:
        return source_text

    anchor = "import maya.cmds as cmds\n"

    if anchor not in source_text:
        raise RuntimeError(
            u"无法为 Core 文件加入 Import：{}".format(
                module_name
            )
        )

    return source_text.replace(
        anchor,
        anchor + "\n" + import_text,
        1
    )


def add_sanitized_short_name_api():
    u"""把 Namespace 安全短名正式收进 rename_utils。"""
    path = "core/rename_utils.py"
    source_text = migration.read_text(path)

    if "def get_sanitized_short_name(" in source_text:
        return

    marker = "\ndef get_selected_objects(show_warning=True):\n"

    api_text = (
        "\ndef get_sanitized_short_name(node, namespace_separator=\"_\"):\n"
        "    u\"\"\"\n"
        "    返回适合作为新 Maya 节点名或文件 Stem 使用的 Short Name。\n\n"
        "    先复用 get_short_name() 去掉 DAG Path，再把 Namespace 冒号替换为指定分隔符。\n\n"
        "    Args:\n"
        "        node (str | None):\n"
        "            Maya 节点名称或 Long DAG Path。\n"
        "        namespace_separator (str):\n"
        "            Namespace 冒号替换字符，默认使用下划线。\n\n"
        "    Returns:\n"
        "        str:\n"
        "            不含 DAG Path，且 Namespace 已安全转换的名称。\n"
        "    \"\"\"\n"
        "    short_name = get_short_name(\n"
        "        node\n"
        "    )\n\n"
        "    return short_name.replace(\n"
        "        \":\",\n"
        "        namespace_separator\n"
        "    )\n"
    )

    source_text = migration.replace_required(
        source_text,
        marker,
        api_text + marker,
        "rename_utils sanitized short name API"
    )

    migration.write_text(path, source_text)


def cleanup_short_name_wrapper(relative_path, sanitized=False):
    u"""删除 Core 领域模块自己的 get_short_name() 薄包装。"""
    source_text = migration.read_text(relative_path)

    source_text = migration.remove_definition(
        source_text,
        "get_short_name"
    )
    source_text = ensure_core_import(
        source_text,
        "rename_utils"
    )

    replacement = "rename_utils.get_short_name("

    if sanitized:
        replacement = "rename_utils.get_sanitized_short_name("

    source_text = source_text.replace(
        "get_short_name(",
        replacement
    )

    source_text = source_text.replace(
        "    \"get_short_name\",\n",
        ""
    )

    migration.write_text(
        relative_path,
        source_text
    )


def cleanup_validate_node_wrapper(relative_path):
    u"""删除 Core 领域模块自己的 validate_node() 薄包装。"""
    source_text = migration.read_text(relative_path)

    source_text = migration.remove_definition(
        source_text,
        "validate_node"
    )
    source_text = ensure_core_import(
        source_text,
        "scene_utils"
    )

    source_text = source_text.replace(
        "validate_node(",
        "scene_utils.validate_node("
    )
    source_text = source_text.replace(
        "    \"validate_node\",\n",
        ""
    )

    migration.write_text(
        relative_path,
        source_text
    )


def cleanup_snap_item_queries():
    u"""把 Snap 的 Component-aware 查询改成明确 Item API。"""
    path = "core/snap_utils.py"
    source_text = migration.read_text(path)

    source_text = ensure_core_import(
        source_text,
        "transform_utils"
    )

    source_text = migration.replace_required(
        source_text,
        "def get_world_position(item):\n",
        "def get_item_world_position(item):\n",
        "snap item world position"
    )
    source_text = migration.replace_required(
        source_text,
        "def get_world_rotation(item):\n",
        "def get_item_world_rotation(item):\n",
        "snap item world rotation"
    )

    source_text = source_text.replace(
        "get_world_position(",
        "get_item_world_position("
    )
    source_text = source_text.replace(
        "get_world_rotation(",
        "get_item_world_rotation("
    )

    # Transform / Joint Rotation 不再重复 xform；Component / Shape 的 Snap 语义继续留在本模块。
    old_rotation_query = (
        "    # -------------------------------------------------------------------------\n"
        "    # 步骤 3：查询世界欧拉角。\n"
        "    # -------------------------------------------------------------------------\n"
        "    try:\n"
        "        rotation = cmds.xform(\n"
        "            item,\n"
        "            query=True,\n"
        "            worldSpace=True,\n"
        "            rotation=True\n"
        "        )\n"
        "    except Exception:\n"
        "        rotation = None\n\n"
        "    if not rotation:\n"
        "        return None\n\n"
        "    if len(rotation) < 3:\n"
        "        return None\n\n"
        "    return [\n"
        "        float(rotation[0]),\n"
        "        float(rotation[1]),\n"
        "        float(rotation[2]),\n"
        "    ]\n"
    )

    new_rotation_query = (
        "    # -------------------------------------------------------------------------\n"
        "    # 步骤 3：Transform / Joint 世界旋转统一交给 Transform Core。\n"
        "    # -------------------------------------------------------------------------\n"
        "    try:\n"
        "        rotation = transform_utils.get_world_rotation(\n"
        "            item\n"
        "        )\n"
        "    except Exception:\n"
        "        return None\n\n"
        "    return [\n"
        "        float(rotation[0]),\n"
        "        float(rotation[1]),\n"
        "        float(rotation[2]),\n"
        "    ]\n"
    )

    source_text = migration.replace_required(
        source_text,
        old_rotation_query,
        new_rotation_query,
        "snap transform rotation delegation"
    )

    migration.write_text(
        path,
        source_text
    )


def cleanup_second_layer_core_duplicates():
    u"""清理第一轮 Core Single Source Gate 暴露出的历史包装层。"""
    add_sanitized_short_name_api()

    cleanup_short_name_wrapper(
        "core/skin_utils.py",
        sanitized=True
    )
    cleanup_short_name_wrapper(
        "core/scene_clean_utils.py",
        sanitized=False
    )
    cleanup_short_name_wrapper(
        "core/model_check_utils.py",
        sanitized=False
    )
    cleanup_short_name_wrapper(
        "core/blendshape_utils.py",
        sanitized=True
    )

    cleanup_validate_node_wrapper(
        "core/mesh_utils.py"
    )
    cleanup_validate_node_wrapper(
        "core/surface_utils.py"
    )
    cleanup_validate_node_wrapper(
        "core/curve_utils.py"
    )

    cleanup_snap_item_queries()


def run():
    u"""运行 Phase 2 迁移，并继续完成 Core 第二层单源化。"""
    migration.update_scene_utils = update_scene_utils
    migration.run()
    cleanup_second_layer_core_duplicates()


if __name__ == "__main__":
    run()
