# coding=utf-8
u"""
Core Import Style Test
======================

静态检查正式代码是否仍然依赖旧 CamelCase Core Compatibility Shim。

正式模块：
    attr_utils
    hierarchy_utils
    joint_utils
    name_utils

兼容入口：
    attrUtils
    hierarchyUtils
    jointUtils
    nameUtils

本测试使用 Python AST，只检查 Import 语义，不会因为文档或注释里提到旧文件名而误报。
它不 Import Maya，也不会修改场景。
"""

from __future__ import print_function

import ast
import os


# =============================================================================
# Configuration
# =============================================================================

def get_package_root():
    """返回 muziToolset 根目录。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(tests_directory)


def get_formal_roots():
    """返回需要执行正式 Import Gate 的目录。"""
    package_root = get_package_root()
    root_names = [
        "app",
        "ui",
        "core",
        "tools",
        "systems",
        "tests",
    ]
    roots = []

    for root_name in root_names:
        roots.append(
            os.path.join(
                package_root,
                root_name
            )
        )

    return roots


def get_forbidden_module_names():
    """
    返回旧 CamelCase Compatibility Shim 名称。

    字符串使用分段组合，避免本测试源码本身被未来的普通文本扫描器误判为旧 Import。
    """
    return [
        "attr" + "Utils",
        "hierarchy" + "Utils",
        "joint" + "Utils",
        "name" + "Utils",
    ]


def get_compatibility_file_paths():
    """返回允许存在的四个兼容转发文件。"""
    package_root = get_package_root()
    core_directory = os.path.join(
        package_root,
        "core"
    )
    file_paths = []

    for module_name in get_forbidden_module_names():
        file_paths.append(
            os.path.normcase(
                os.path.abspath(
                    os.path.join(
                        core_directory,
                        module_name + ".py"
                    )
                )
            )
        )

    return file_paths


# =============================================================================
# File Discovery
# =============================================================================

def iter_python_files():
    """遍历正式代码目录中的 Python 文件。"""
    compatibility_paths = get_compatibility_file_paths()

    for formal_root in get_formal_roots():
        if not os.path.isdir(formal_root):
            continue

        for directory, directory_names, file_names in os.walk(formal_root):
            filtered_directory_names = []

            for directory_name in directory_names:
                if directory_name == "__pycache__":
                    continue

                filtered_directory_names.append(directory_name)

            directory_names[:] = filtered_directory_names

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                file_path = os.path.join(
                    directory,
                    file_name
                )
                normalized_path = os.path.normcase(
                    os.path.abspath(file_path)
                )

                if normalized_path in compatibility_paths:
                    continue

                yield file_path


# =============================================================================
# AST Check
# =============================================================================

def get_imported_names(import_node):
    """从 ast.Import / ast.ImportFrom 中提取模块和 Alias 名称。"""
    imported_names = []

    if isinstance(import_node, ast.Import):
        for alias in import_node.names:
            imported_names.append(alias.name)

            if alias.asname:
                imported_names.append(alias.asname)

        return imported_names

    if isinstance(import_node, ast.ImportFrom):
        if import_node.module:
            imported_names.append(import_node.module)

        for alias in import_node.names:
            imported_names.append(alias.name)

            if alias.asname:
                imported_names.append(alias.asname)

    return imported_names


def contains_forbidden_name(imported_name, forbidden_names):
    """判断 Import 名称是否引用旧 Compatibility Shim。"""
    name_parts = imported_name.split(".")

    for name_part in name_parts:
        if name_part in forbidden_names:
            return True

    return False


def scan_file(file_path):
    """扫描单个 Python 文件并返回旧 Core Import 问题。"""
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

    forbidden_names = get_forbidden_module_names()
    issues = []

    for node in ast.walk(syntax_tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        imported_names = get_imported_names(node)

        for imported_name in imported_names:
            if not contains_forbidden_name(
                    imported_name,
                    forbidden_names
            ):
                continue

            issues.append({
                "file": file_path,
                "line": getattr(node, "lineno", None),
                "import_name": imported_name,
            })

    return issues


def scan_repository():
    """扫描全部正式 Python 文件。"""
    issues = []
    file_count = 0

    for file_path in iter_python_files():
        file_count += 1

        file_issues = scan_file(file_path)

        for issue in file_issues:
            issues.append(issue)

    return {
        "file_count": file_count,
        "issues": issues,
    }


# =============================================================================
# Runner
# =============================================================================

def run():
    """运行 CamelCase Core Compatibility Import Gate。"""
    print("=" * 78)
    print("Muzi Toolset - Core Import Style Test")
    print("=" * 78)

    result = scan_repository()
    issues = result["issues"]

    if issues:
        for issue in issues:
            relative_path = os.path.relpath(
                issue["file"],
                get_package_root()
            )

            print(
                u"[FAIL] {}:{} | {}".format(
                    relative_path,
                    issue["line"],
                    issue["import_name"]
                )
            )
    else:
        print(
            u"[PASS] {} 个正式 Python 文件未引用旧 CamelCase Core 入口。".format(
                result["file_count"]
            )
        )

    print("-" * 78)
    print(
        "Files: {} | Issues: {}".format(
            result["file_count"],
            len(issues)
        )
    )
    print("=" * 78)

    result["passed"] = not bool(issues)
    return result


__all__ = [
    "get_package_root",
    "get_formal_roots",
    "iter_python_files",
    "scan_file",
    "scan_repository",
    "run",
]
