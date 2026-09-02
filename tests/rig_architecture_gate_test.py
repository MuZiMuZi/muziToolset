# coding=utf-8
u"""
Rig Architecture Migration Gate
===============================

阻止已经完成的 Rig 架构迁移再次回退。

禁止重新出现：
    core/name_utils.py
    systems/component_base.py
    systems/controller/
    systems/face/build/teeth_component.py
    systems/face/build/teeth_builder.py

禁止正式源码重新 Import：
    name_utils
    component_base
    systems.controller

禁止类名：
    ComponentBase
    RigComponentBase
    TeethComponent

RigBase Contract：
    - RigBase 是实例化 Rig Object Base；
    - create_name / mirror_name / create_unique_name 等必须通过实例调用；
    - parse_name / validate_name / normalize_* 可以继续作为 Class Method 使用；
    - 不允许恢复旧 Name Object Constructor：RigBase(name=...)。
"""

from __future__ import print_function

import ast
import os


FORBIDDEN_PATHS = [
    "core/name_utils.py",
    "systems/component_base.py",
    "systems/controller",
    "systems/face/build/teeth_component.py",
    "systems/face/build/teeth_builder.py",
]

FORBIDDEN_CLASS_NAMES = {
    "ComponentBase",
    "RigComponentBase",
    "TeethComponent",
}

FORBIDDEN_IMPORT_TOKENS = {
    "name_utils",
    "component_base",
}

RIG_BASE_INSTANCE_METHODS = {
    "create_name",
    "mirror_name",
    "get_next_index",
    "create_unique_name",
    "get_opposite_side",
    "flip_side",
    "is_left",
    "is_right",
    "is_center",
    "resolve_identity",
    "set_identity",
}


# =============================================================================
# Path
# =============================================================================

def get_package_root():
    u"""返回 muziToolset 根目录。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(
        tests_directory
    )


def iter_python_files():
    u"""遍历正式源码和测试文件。"""
    package_root = get_package_root()
    root_names = [
        "app",
        "core",
        "systems",
        "tools",
        "ui",
        "tests",
    ]

    for root_name in root_names:
        root_path = os.path.join(
            package_root,
            root_name
        )

        if not os.path.isdir(root_path):
            continue

        for directory, directory_names, file_names in os.walk(
                root_path
        ):
            filtered_directories = []

            for directory_name in directory_names:
                if directory_name == "__pycache__":
                    continue

                filtered_directories.append(
                    directory_name
                )

            directory_names[:] = filtered_directories

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                yield os.path.join(
                    directory,
                    file_name
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


# =============================================================================
# Import
# =============================================================================

def get_import_names(node):
    u"""从 Import AST 节点提取完整模块和导入名称。"""
    names = []

    if isinstance(node, ast.Import):
        for alias in node.names:
            names.append(
                alias.name
            )
        return names

    if isinstance(node, ast.ImportFrom):
        module_name = node.module or ""

        if module_name:
            names.append(
                module_name
            )

        for alias in node.names:
            if module_name:
                names.append(
                    "{}.{}".format(
                        module_name,
                        alias.name
                    )
                )
            else:
                names.append(
                    alias.name
                )

    return names


def import_is_forbidden(import_name):
    u"""检查 Import 是否指向退休架构。"""
    name_parts = import_name.split(".")

    for token in FORBIDDEN_IMPORT_TOKENS:
        if token in name_parts:
            return True

    if "systems.controller" in import_name:
        return True

    return False


# =============================================================================
# RigBase AST Contract
# =============================================================================

def get_keyword_names(call_node):
    u"""返回一个 AST Call 的 Keyword 名称。"""
    keyword_names = []

    for keyword in call_node.keywords:
        if keyword.arg is None:
            continue

        keyword_names.append(
            keyword.arg
        )

    return keyword_names


def is_rig_base_class_method_call(call_node):
    u"""判断是否为 RigBase.some_method(...) 形式。"""
    function_node = call_node.func

    if not isinstance(function_node, ast.Attribute):
        return False

    value_node = function_node.value

    if not isinstance(value_node, ast.Name):
        return False

    if value_node.id != "RigBase":
        return False

    return True


def check_rig_base_call(call_node, relative_path):
    u"""检查 RigBase 是否被重新当成 Name Utility / Name Object。"""
    issues = []

    if isinstance(call_node.func, ast.Name):
        if call_node.func.id == "RigBase":
            keyword_names = get_keyword_names(
                call_node
            )

            if "name" in keyword_names:
                issues.append({
                    "file": relative_path,
                    "line": call_node.lineno,
                    "detail": "RigBase 不允许恢复 name= Name Object Constructor",
                })

        return issues

    if not is_rig_base_class_method_call(call_node):
        return issues

    method_name = call_node.func.attr

    if method_name not in RIG_BASE_INSTANCE_METHODS:
        return issues

    issues.append({
        "file": relative_path,
        "line": call_node.lineno,
        "detail": "RigBase.{}() 必须通过 RigBase 实例调用".format(
            method_name
        ),
    })
    return issues


# =============================================================================
# Scan
# =============================================================================

def scan_file(file_path):
    u"""扫描一个 Python 文件中的退休 Import / Class / RigBase 调用。"""
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
    relative_path = get_relative_path(
        file_path
    )
    issues = []

    for node in ast.walk(syntax_tree):
        if isinstance(node, ast.ClassDef):
            if node.name in FORBIDDEN_CLASS_NAMES:
                issues.append({
                    "file": relative_path,
                    "line": node.lineno,
                    "detail": "退休类名 {}".format(node.name),
                })
            continue

        if isinstance(node, ast.Call):
            rig_base_issues = check_rig_base_call(
                node,
                relative_path
            )

            for issue in rig_base_issues:
                issues.append(
                    issue
                )

            continue

        if not isinstance(
                node,
                (ast.Import, ast.ImportFrom)
        ):
            continue

        import_names = get_import_names(
            node
        )

        for import_name in import_names:
            if import_is_forbidden(
                    import_name
            ):
                issues.append({
                    "file": relative_path,
                    "line": node.lineno,
                    "detail": "退休 Import {}".format(import_name),
                })

    return issues


def scan_forbidden_paths():
    u"""检查已经退休的文件 / 目录是否重新出现。"""
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
            "detail": "退休路径重新出现",
        })

    return issues


# =============================================================================
# Runner
# =============================================================================

def run():
    u"""运行 Rig Architecture Migration Gate。"""
    print("=" * 78)
    print("Muzi Toolset - Rig Architecture Migration Gate")
    print("=" * 78)

    issues = scan_forbidden_paths()
    file_count = 0

    for file_path in iter_python_files():
        relative_path = get_relative_path(
            file_path
        )

        if relative_path == "tests/rig_architecture_gate_test.py":
            continue

        file_count += 1
        file_issues = scan_file(
            file_path
        )

        for issue in file_issues:
            issues.append(
                issue
            )

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
        u"[PASS] {} 个 Python 文件符合 RigBase Identity / ModuleBase / CtrlBase 架构。".format(
            file_count
        )
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
