# coding=utf-8
u"""
临时迁移脚本：把 Scene Clean 与 Export 能力统一收口到 core.scene_utils。

迁移完成并通过静态测试后删除本脚本。
"""

from __future__ import print_function

from pathlib import Path
import re


ROOT = Path(".")
SCENE_PATH = ROOT / "core" / "scene_utils.py"
CLEAN_PATH = ROOT / "core" / "scene_utils.py"
EXPORT_PATH = ROOT / "core" / "scene_utils.py"

TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".yml",
    ".yaml",
    ".txt",
}

SKIP_PARTS = {
    ".git",
    "legacy_reference",
    "site",
    "__pycache__",
}


SCENE_DOCSTRING = '''# coding=utf-8
u"""
Scene Utils
===========

Maya Scene 领域的统一底层工具。

模块职责
--------
本模块统一负责 Maya Scene 级别的查询、创建、修改、清理和文件 IO：

    - Undo Chunk；
    - Maya Node 存在性、唯一 DAG Long Path 和节点创建；
    - Scene Availability、Node Type 和 Selection 查询；
    - Object Set 创建与维护；
    - Maya Native Event Callback；
    - 当前 Scene 路径与修改状态；
    - Maya Scene Open / Import / Reference；
    - FBX 等场景导出；
    - 安全范围内的 Scene Cleanup。

模块边界
--------
    Maya Scene / Node / Selection / Scene IO / Export / Cleanup -> scene_utils
    硬盘 Path / Directory / JSON                                -> file_utils
    Transform 空间数据                                           -> transform_utils
    DAG Parent / Child                                           -> hierarchy_utils
    Snap / Match                                                 -> snap_utils
    模型问题检查 / 诊断                                           -> model_check_utils

设计原则
--------
1. Core 不弹确认窗口，交互确认由 Tool / App 负责；
2. 创建函数先处理必要输入，再修改 Maya Scene；
3. validate_node() 只接受 Maya Node，不接受 Plug / Component；
4. ensure_nodes_available() 只检查已有 Scene State，不判断 Rig Naming 格式；
5. 内部 Rig Naming 默认可信，Scene Core 不负责重复验证命名规范；
6. Cleanup 只保护 Scene State：Reference、Animation、Constraint、Rig Deformer 等；
7. Export 接收明确对象列表，不依赖用户当前 Selection，并在结束后恢复 Selection；
8. model_check_utils 保持只读检查职责，不与会修改场景的 Scene API 合并。
"""
'''


COMBINED_EXPORTS = [
    # Undo
    "open_undo_chunk",
    "close_undo_chunk",
    "undo_chunk",
    # Node / Selection / Set / Callback
    "validate_node",
    "ensure_nodes_available",
    "get_long_name",
    "create_node",
    "get_nodes_by_type",
    "get_selected_nodes",
    "ensure_object_set",
    "create_native_event_callback",
    # Scene State / IO
    "get_current_scene_path",
    "is_scene_modified",
    "validate_scene_file",
    "open_scene",
    "import_scene",
    "reference_scene",
    # Export
    "ensure_fbx_plugin_loaded",
    "export_fbx",
    # Cleanup Query
    "is_default_camera",
    "is_referenced",
    "existing_nodes",
    "all_transform_nodes",
    "sort_child_first",
    "has_incoming_animation",
    "has_constraint",
    "has_rig_history",
    "can_modify_transform",
    # Cleanup Action
    "delete_empty_groups",
    "delete_history",
    "freeze_transformations",
    "unlock_and_show_attributes",
    "center_pivot",
    "delete_unknown_nodes",
    "run_cleanup",
]


def _read(path):
    return path.read_text(
        encoding="utf-8"
    )


def _write(path, content):
    path.write_text(
        content,
        encoding="utf-8"
    )


def _strip_module_docstring(source):
    marker = 'u"""'
    start_index = source.find(marker)

    if start_index < 0:
        raise RuntimeError(
            u"scene_utils.py 没有找到模块 Docstring。"
        )

    end_index = source.find(
        '"""',
        start_index + len(marker)
    )

    if end_index < 0:
        raise RuntimeError(
            u"scene_utils.py 模块 Docstring 没有正确闭合。"
        )

    end_index += 3
    return source[end_index:].lstrip("\n")


def _strip_all(source):
    marker = "\n\n__all__ = ["
    index = source.rfind(marker)

    if index < 0:
        raise RuntimeError(
            u"模块没有找到 __all__ 导出列表。"
        )

    return source[:index].rstrip()


def _extract(source, start_marker):
    body = _strip_all(source)
    start_index = body.find(start_marker)

    if start_index < 0:
        raise RuntimeError(
            u"没有找到迁移起点：{}".format(
                start_marker
            )
        )

    return body[start_index:].strip()


def _build_all():
    lines = [
        "__all__ = ["
    ]

    for name in COMBINED_EXPORTS:
        lines.append(
            '    "{}",'.format(name)
        )

    lines.append(
        "]"
    )
    return "\n".join(lines)


def merge_scene_modules():
    u"""把两个 Scene 旁支模块合并到 scene_utils.py。"""
    if not CLEAN_PATH.exists() and not EXPORT_PATH.exists():
        print("Scene domain modules already merged.")
        return False

    if not CLEAN_PATH.exists() or not EXPORT_PATH.exists():
        raise RuntimeError(
            u"Scene Domain 当前处于半迁移状态，请先检查旧模块。"
        )

    scene_source = _read(
        SCENE_PATH
    )
    clean_source = _read(
        CLEAN_PATH
    )
    export_source = _read(
        EXPORT_PATH
    )

    scene_body = _strip_all(
        _strip_module_docstring(scene_source)
    )

    # Step 01：补齐统一 Scene 模块需要的底层依赖。
    if "import maya.mel as mel" not in scene_body:
        scene_body = scene_body.replace(
            "import maya.cmds as cmds\n",
            "import maya.cmds as cmds\nimport maya.mel as mel\n",
            1
        )

    if "from . import rename_utils" not in scene_body:
        scene_body = scene_body.replace(
            "from . import file_utils\n",
            "from . import file_utils\nfrom . import rename_utils\n",
            1
        )

    # Step 02：提取 Export API，并改成同模块直接调用 Scene API。
    export_body = _extract(
        export_source,
        "def ensure_fbx_plugin_loaded():"
    )
    export_body = export_body.replace(
        "scene_utils.validate_node(",
        "validate_node("
    )
    export_body = export_body.replace(
        "scene_utils.get_selected_nodes(",
        "get_selected_nodes("
    )

    # Step 03：提取 Cleanup API，并把 Undo Decorator 改成本模块直接调用。
    clean_body = _extract(
        clean_source,
        "default_cameras = ["
    )
    clean_body = clean_body.replace(
        "@scene_utils.undo_chunk",
        "@undo_chunk"
    )

    merged_source = "\n\n".join([
        SCENE_DOCSTRING.rstrip(),
        scene_body.rstrip(),
        "# =============================================================================\n# Export\n# =============================================================================\n\n" + export_body,
        "# =============================================================================\n# Scene Cleanup\n# =============================================================================\n\n" + clean_body,
        _build_all(),
    ])
    merged_source += "\n"

    _write(
        SCENE_PATH,
        merged_source
    )

    CLEAN_PATH.unlink()
    EXPORT_PATH.unlink()

    print("Merged scene_utils.py and scene_utils.py into scene_utils.py.")
    return True


def _skip_path(path):
    for part in path.parts:
        if part in SKIP_PARTS:
            return True

    return False


def _deduplicate_scene_imports(text):
    lines = text.splitlines()
    result = []
    scene_import_lines = set()

    for line in lines:
        stripped = line.strip()

        if (
                stripped.startswith("from ")
                and " import scene_utils" in stripped
        ):
            if stripped in scene_import_lines:
                continue

            scene_import_lines.add(
                stripped
            )

        result.append(
            line
        )

    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(result) + suffix


def migrate_references():
    u"""把仓库内旧 Scene Clean / Export 模块引用统一迁移到 scene_utils。"""
    changed_files = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if _skip_path(path):
            continue

        if path == Path(__file__):
            continue

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            source = _read(
                path
            )
        except UnicodeDecodeError:
            continue

        updated = source.replace(
            "scene_utils",
            "scene_utils"
        )
        updated = updated.replace(
            "scene_utils",
            "scene_utils"
        )

        # 两个旧模块同时被同一个文件 Import 时，全局替换可能产生重复 Import。
        updated = _deduplicate_scene_imports(
            updated
        )

        # 处理同一条 from-import 中替换后出现的重复名字。
        updated = re.sub(
            r"\bscene_utils\s*,\s*scene_utils\b",
            "scene_utils",
            updated
        )

        if updated == source:
            continue

        _write(
            path,
            updated
        )
        changed_files.append(
            str(path)
        )

    print(
        "Migrated scene domain references in {} files.".format(
            len(changed_files)
        )
    )
    return changed_files


def validate_no_legacy_references():
    u"""确认正式源码、测试和文档不再引用退休 Scene 模块。"""
    errors = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if _skip_path(path):
            continue

        if path == Path(__file__):
            continue

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            source = _read(
                path
            )
        except UnicodeDecodeError:
            continue

        if "scene_utils" in source or "scene_utils" in source:
            errors.append(
                str(path)
            )

    if errors:
        raise RuntimeError(
            u"仍然存在退休 Scene 模块引用：{}".format(
                ", ".join(errors)
            )
        )

    print("Legacy scene domain references: 0")
    return True


def run():
    u"""执行 Scene Domain 合并与全仓引用迁移。"""
    merge_scene_modules()
    migrate_references()
    validate_no_legacy_references()
    return True


if __name__ == "__main__":
    run()
