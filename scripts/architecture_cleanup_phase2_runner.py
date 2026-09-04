# coding=utf-8
u"""
Architecture Cleanup Phase 2 Runner
===================================

给一次性 Phase 2 Migration 提供修正版和后续 Core / Upper Layer 单源化清理。

原则：
    - Generic Node / DAG / Transform 能力只保留一个正式 Core 实现；
    - 领域模块直接调用对应 Core，不再保留同名薄包装；
    - Snap 对 Component 的特殊语义保留，但使用明确的 Item API 名称；
    - Tool / System / UI 的 Undo 生命周期统一经过 scene_utils；
    - Maya Constraint 创建统一经过 constraint_utils；
    - 不修改 Face / Controller / Skin 等业务算法。
"""

from __future__ import print_function

import ast
import os

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


def ensure_upper_core_import(source_text, relative_path, module_name):
    u"""根据包深度为 System / Tool / UI 加入 Core Import。"""
    directory = os.path.dirname(relative_path)
    directory_parts = []

    if directory:
        directory_parts = directory.split("/")

    dot_count = len(directory_parts) + 1
    import_text = "from {}core import {}\n".format(
        "." * dot_count,
        module_name
    )

    if import_text in source_text:
        return source_text

    import_lines = source_text.splitlines(True)
    insert_index = None

    for index in range(len(import_lines)):
        line = import_lines[index]

        if line.startswith("from ") and " import " in line:
            insert_index = index + 1

    if insert_index is None:
        anchor = "import maya.cmds as cmds\n"

        if anchor not in source_text:
            raise RuntimeError(
                u"无法为上层文件加入 Core Import：{} | {}".format(
                    relative_path,
                    module_name
                )
            )

        return source_text.replace(
            anchor,
            anchor + "\n" + import_text,
            1
        )

    import_lines.insert(
        insert_index,
        import_text
    )

    return "".join(import_lines)


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
        "    # 步骤 3：Transform / Jnt 世界旋转统一交给 Transform Core。\n"
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
        "core/scene_utils.py",
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


def add_scene_undo_lifecycle_api():
    u"""增加显式 Undo Chunk 生命周期 API，并让 decorator 复用它。"""
    path = "core/scene_utils.py"
    source_text = migration.read_text(path)

    if "def open_undo_chunk(" not in source_text:
        marker = "\ndef undo_chunk(function):\n"
        api_text = (
            "\ndef open_undo_chunk(chunk_name=None):\n"
            "    u\"\"\"打开一个 Maya Undo Chunk。\"\"\"\n"
            "    kwargs = {\n"
            "        \"openChunk\": True,\n"
            "    }\n\n"
            "    if chunk_name:\n"
            "        kwargs[\"chunkName\"] = chunk_name\n\n"
            "    cmds.undoInfo(\n"
            "        **kwargs\n"
            "    )\n"
            "    return True\n\n\n"
            "def close_undo_chunk():\n"
            "    u\"\"\"关闭当前 Maya Undo Chunk。\"\"\"\n"
            "    cmds.undoInfo(\n"
            "        closeChunk=True\n"
            "    )\n"
            "    return True\n"
        )

        source_text = migration.replace_required(
            source_text,
            marker,
            api_text + marker,
            "scene undo lifecycle API"
        )

    source_text = source_text.replace(
        "        cmds.undoInfo(\n"
        "            openChunk=True,\n"
        "            chunkName=function.__name__\n"
        "        )\n",
        "        open_undo_chunk(\n"
        "            function.__name__\n"
        "        )\n"
    )
    source_text = source_text.replace(
        "            cmds.undoInfo(\n"
        "                closeChunk=True\n"
        "            )\n",
        "            close_undo_chunk()\n"
    )

    migration.write_text(
        path,
        source_text
    )


def is_cmds_call(node, command_name):
    u"""判断 AST Call 是否为 cmds.<command_name>()。"""
    if not isinstance(node, ast.Call):
        return False

    function = node.func

    if not isinstance(function, ast.Attribute):
        return False

    if function.attr != command_name:
        return False

    if not isinstance(function.value, ast.Name):
        return False

    return function.value.id == "cmds"


def get_constant_bool(node):
    u"""读取 AST 常量 Bool。"""
    if isinstance(node, ast.Constant):
        return bool(node.value)

    if hasattr(ast, "NameConstant"):
        if isinstance(node, ast.NameConstant):
            return bool(node.value)

    return False


def replace_upper_undo_calls(relative_path):
    u"""把一个上层文件里的 cmds.undoInfo 转发到 Scene Core。"""
    source_text = migration.read_text(relative_path)
    syntax_tree = ast.parse(
        source_text,
        filename=relative_path
    )
    replacements = []

    for node in ast.walk(syntax_tree):
        if not is_cmds_call(node, "undoInfo"):
            continue

        open_chunk = False
        close_chunk = False
        chunk_name_source = None

        for keyword in node.keywords:
            if keyword.arg == "openChunk":
                open_chunk = get_constant_bool(keyword.value)
            elif keyword.arg == "closeChunk":
                close_chunk = get_constant_bool(keyword.value)
            elif keyword.arg == "chunkName":
                chunk_name_source = ast.get_source_segment(
                    source_text,
                    keyword.value
                )

        if open_chunk:
            replacement = "scene_utils.open_undo_chunk()"

            if chunk_name_source:
                replacement = "scene_utils.open_undo_chunk({})".format(
                    chunk_name_source
                )
        elif close_chunk:
            replacement = "scene_utils.close_undo_chunk()"
        else:
            raise RuntimeError(
                u"上层出现未识别的 cmds.undoInfo 用法：{}:{}".format(
                    relative_path,
                    node.lineno
                )
            )

        source_segment = ast.get_source_segment(
            source_text,
            node
        )

        if not source_segment:
            raise RuntimeError(
                u"无法取得 Undo Call Source：{}:{}".format(
                    relative_path,
                    node.lineno
                )
            )

        replacements.append(
            (source_segment, replacement)
        )

    if not replacements:
        return False

    for source_segment, replacement in replacements:
        if source_segment not in source_text:
            raise RuntimeError(
                u"Undo Call 已发生结构变化：{}".format(
                    relative_path
                )
            )

        source_text = source_text.replace(
            source_segment,
            replacement,
            1
        )

    source_text = ensure_upper_core_import(
        source_text,
        relative_path,
        "scene_utils"
    )

    migration.write_text(
        relative_path,
        source_text
    )
    return True


def iter_upper_python_files():
    u"""遍历 systems / tools / ui 正式 Python 文件。"""
    root_names = [
        "systems",
        "tools",
        "ui",
    ]

    for root_name in root_names:
        root_path = migration.get_path(root_name)

        for directory, directory_names, file_names in os.walk(root_path):
            filtered_names = []

            for directory_name in directory_names:
                if directory_name == "__pycache__":
                    continue

                filtered_names.append(directory_name)

            directory_names[:] = filtered_names

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                file_path = os.path.join(
                    directory,
                    file_name
                )
                relative_path = os.path.relpath(
                    file_path,
                    migration.REPOSITORY_ROOT
                ).replace(os.sep, "/")

                yield relative_path


def migrate_upper_undo_calls():
    u"""批量迁移上层 Undo Call。"""
    changed_files = []

    for relative_path in iter_upper_python_files():
        changed = replace_upper_undo_calls(
            relative_path
        )

        if changed:
            changed_files.append(
                relative_path
            )

    print(
        u"[PASS] Upper Undo Migration: {} files".format(
            len(changed_files)
        )
    )


def cleanup_zip_lip_parent_wrapper():
    u"""删除 Zip Lip 的 get_parent Compatibility Wrapper。"""
    path = "systems/face/lip/zip_builder.py"
    source_text = migration.read_text(path)

    source_text = migration.remove_definition(
        source_text,
        "get_parent"
    )
    source_text = source_text.replace(
        "get_parent(",
        "hierarchy_utils.Hierarchy.get_parent("
    )
    source_text = source_text.replace(
        "    \"get_parent\",\n",
        ""
    )

    migration.write_text(
        path,
        source_text
    )


def cleanup_jnt_tool_constraint():
    u"""把 Jnt Tool 的批量 Parent Constraint 统一交给 Constraint Core。"""
    path = "tools/jnt/jnt_tool.py"
    source_text = migration.read_text(path)

    source_text = ensure_upper_core_import(
        source_text,
        path,
        "constraint_utils"
    )

    source_text = migration.replace_required(
        source_text,
        "                cmds.parentConstraint(\n"
        "                    driver,\n"
        "                    driven,\n"
        "                    maintainOffset=True\n"
        "                )\n",
        "                constraint_utils.create_constraint(\n"
        "                    driver_objects=driver,\n"
        "                    driven_object=driven,\n"
        "                    constraint_type=\"parentConstraint\",\n"
        "                    maintain_offset=True\n"
        "                )\n",
        "jnt tool parent constraint"
    )

    migration.write_text(
        path,
        source_text
    )


def cleanup_upper_layer_core_bypass():
    u"""清理 Upper Layer Gate 暴露的 Undo / Parent / Constraint 绕过。"""
    add_scene_undo_lifecycle_api()
    cleanup_zip_lip_parent_wrapper()
    cleanup_jnt_tool_constraint()
    migrate_upper_undo_calls()


def run():
    u"""运行 Phase 2 全部架构迁移。"""
    migration.update_scene_utils = update_scene_utils
    migration.run()
    cleanup_second_layer_core_duplicates()
    cleanup_upper_layer_core_bypass()


if __name__ == "__main__":
    run()
