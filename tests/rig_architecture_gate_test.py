# coding=utf-8
u"""
Current Rig Architecture Gate
=============================

阻止 MuziTools 当前 Rig 架构重新退回已经退休的中间版本。

当前正式基础结构：
    core/common/name_utils.py
        Rig Naming Contract。

    core/rigging/ctrl_utils.py
        Controller Primitive。

    core/rigging/jnt_utils.py
        Joint Primitive。

    systems/rig_module.py
        当前通用 Rig Module Lifecycle。

明确退休的正式架构入口：
    core/name_utils.py
    systems/rig_base.py
    systems/module_base.py
    systems/ctrl_base.py
    systems/component_base.py
    systems/controller/
    systems/face/build/teeth_component.py
    systems/face/build/teeth_builder.py

明确退休的正式 Runtime 类：
    RigBase
    ModuleBase
    RigModuleBase
    CtrlBase
    ComponentBase
    RigComponentBase
    TeethComponent

兼容说明：
    ``legacy_reference`` 与 ``core/bake`` 可以保留历史实现用于迁移参考；它们不属于
    当前正式架构，因此本 Gate 不扫描这些兼容区，也不会因为 Tool 显式引用
    ``legacy_reference`` 就把历史 API 重新认定为正式架构。

本测试使用 AST，只检查正式 Runtime 路径，不 Import Maya。
"""

from __future__ import print_function

import ast
import os


REQUIRED_PATHS = [
    "core/common/name_utils.py",
    "core/rigging/ctrl_utils.py",
    "core/rigging/jnt_utils.py",
    "systems/rig_module.py",
]

FORBIDDEN_PATHS = [
    "core/name_utils.py",
    "systems/rig_base.py",
    "systems/module_base.py",
    "systems/ctrl_base.py",
    "systems/component_base.py",
    "systems/controller",
    "systems/face/build/teeth_component.py",
    "systems/face/build/teeth_builder.py",
]

FORBIDDEN_CLASS_NAMES = {
    "RigBase",
    "ModuleBase",
    "RigModuleBase",
    "CtrlBase",
    "ComponentBase",
    "RigComponentBase",
    "TeethComponent",
}

FORBIDDEN_DIRECT_IMPORTS = {
    "systems.rig_base",
    "systems.module_base",
    "systems.ctrl_base",
    "systems.component_base",
    "systems.controller",
    "core.name_utils",
}

FORMAL_ROOTS = [
    "app",
    "ui",
    os.path.join("core", "common"),
    os.path.join("core", "rigging"),
    "systems",
    "tools",
]


# =============================================================================
# Path Helpers
# =============================================================================

def get_package_root():
    u"""返回 muziToolset 根目录。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(
        tests_directory
    )


def get_relative_path(file_path):
    u"""返回 POSIX 风格仓库相对路径。"""
    relative_path = os.path.relpath(
        file_path,
        get_package_root()
    )
    return relative_path.replace(
        os.sep,
        "/"
    )


def iter_python_files():
    u"""遍历当前正式 Runtime Python 文件。"""
    package_root = get_package_root()

    for root_name in FORMAL_ROOTS:
        root_path = os.path.join(
            package_root,
            root_name
        )

        if not os.path.isdir(root_path):
            continue

        for directory, directory_names, file_names in os.walk(root_path):
            filtered_directories = []

            for directory_name in directory_names:
                if directory_name == "__pycache__":
                    continue

                if directory_name == "legacy_reference":
                    continue

                filtered_directories.append(directory_name)

            directory_names[:] = filtered_directories

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                yield os.path.join(
                    directory,
                    file_name
                )


# =============================================================================
# Architecture Paths
# =============================================================================

def scan_required_paths():
    u"""确认当前架构的四个基础入口仍然存在。"""
    package_root = get_package_root()
    issues = []

    for relative_path in REQUIRED_PATHS:
        absolute_path = os.path.join(
            package_root,
            *relative_path.split("/")
        )

        if os.path.isfile(absolute_path):
            continue

        issues.append({
            "file": relative_path,
            "line": None,
            "detail": "当前正式架构入口缺失",
        })

    return issues


def scan_forbidden_paths():
    u"""检查已经退休的正式文件 / 目录是否重新出现。"""
    package_root = get_package_root()
    issues = []

    for relative_path in FORBIDDEN_PATHS:
        absolute_path = os.path.join(
            package_root,
            *relative_path.split("/")
        )

        if not os.path.exists(absolute_path):
            continue

        issues.append({
            "file": relative_path,
            "line": None,
            "detail": "退休正式架构路径重新出现",
        })

    return issues


# =============================================================================
# AST Import / Class Check
# =============================================================================

def get_import_names(node):
    u"""从 Import AST 节点提取完整模块和导入名称。"""
    names = []

    if isinstance(node, ast.Import):
        for alias in node.names:
            names.append(alias.name)
        return names

    if isinstance(node, ast.ImportFrom):
        module_name = node.module or ""

        if module_name:
            names.append(module_name)

        for alias in node.names:
            if module_name:
                names.append(
                    "{}.{}".format(
                        module_name,
                        alias.name
                    )
                )
            else:
                names.append(alias.name)

    return names


def import_is_forbidden(import_name):
    u"""判断 Import 是否重新依赖退休的正式架构入口。"""
    # 显式 Compatibility Import 允许保留，不能把它误判成正式架构回退。
    if "legacy_reference" in import_name:
        return False

    if ".bake" in import_name or import_name.startswith("core.bake"):
        return False

    normalized_name = import_name.lstrip(".")

    for forbidden_name in FORBIDDEN_DIRECT_IMPORTS:
        if normalized_name == forbidden_name:
            return True

        if normalized_name.endswith("." + forbidden_name):
            return True

        if normalized_name.startswith(forbidden_name + "."):
            return True

    return False


def scan_file(file_path):
    u"""扫描一个正式 Runtime 文件中的退休 Class / Import。"""
    with open(
            file_path,
            "r",
            encoding="utf-8"
    ) as source_file:
        source_text = source_file.read()

    syntax_tree = ast.parse(
        source_text,
        filename=file_path
    )
    relative_path = get_relative_path(file_path)
    issues = []

    for node in ast.walk(syntax_tree):
        if isinstance(node, ast.ClassDef):
            if node.name in FORBIDDEN_CLASS_NAMES:
                issues.append({
                    "file": relative_path,
                    "line": node.lineno,
                    "detail": "退休正式类名重新出现：{}".format(node.name),
                })
            continue

        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        for import_name in get_import_names(node):
            if not import_is_forbidden(import_name):
                continue

            issues.append({
                "file": relative_path,
                "line": node.lineno,
                "detail": "退休正式 Import 重新出现：{}".format(import_name),
            })

    return issues


# =============================================================================
# Runner
# =============================================================================

def run():
    u"""运行当前 RigModule / Core Primitive 架构门禁。"""
    print("=" * 78)
    print("Muzi Toolset - Current Rig Architecture Gate")
    print("=" * 78)

    issues = []

    for issue in scan_required_paths():
        issues.append(issue)

    for issue in scan_forbidden_paths():
        issues.append(issue)

    file_count = 0

    for file_path in iter_python_files():
        file_count += 1

        for issue in scan_file(file_path):
            issues.append(issue)

    if issues:
        for issue in issues:
            print(
                u"[FAIL] {}:{} | {}".format(
                    issue["file"],
                    issue["line"],
                    issue["detail"]
                )
            )

        return False

    print(
        u"[PASS] {} 个正式 Runtime 文件符合当前 RigModule / Core Primitive 架构。".format(
            file_count
        )
    )
    print(
        u"[PASS] core/bake 与 legacy_reference 保持 Compatibility 边界。"
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
