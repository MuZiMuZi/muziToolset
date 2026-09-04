# coding=utf-8
u"""
Core Import Style Test
======================

静态检查正式代码是否重新引入已经退休的 CamelCase Core 模块。

正式模块：
    attr_utils
    hierarchy_utils
    jnt_utils
    name_utils

已退休模块：
    attrUtils
    hierarchyUtils
    jntUtils
    nameUtils

检查内容
--------
1. ``core/`` 下不允许重新出现对应的 CamelCase Python 文件；
2. ``app / ui / core / tools / systems / tests`` 不允许重新 Import 这些旧模块名。

本测试使用 Python AST，只检查源码结构，不会因为普通注释或文档文字提到历史名称而误报。
它不 Import Maya，也不会修改场景，因此可以同时在 Maya 和 GitHub Actions 中运行。
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
    """返回需要执行正式 Import Gate 的源码目录。"""
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


def get_retired_module_names():
    """
    返回已经退休的 CamelCase Core 模块名。

    名称使用字符串拼接，避免未来额外增加的普通文本扫描规则把本测试自己的配置误判成 Import。
    """
    return [
        "attr" + "Utils",
        "hierarchy" + "Utils",
        "joint" + "Utils",
        "name" + "Utils",
    ]


def get_retired_file_paths():
    """返回四个已经删除、禁止重新出现的历史 Core 文件路径。"""
    package_root = get_package_root()
    core_directory = os.path.join(
        package_root,
        "core"
    )
    file_paths = []

    for module_name in get_retired_module_names():
        file_paths.append(
            os.path.abspath(
                os.path.join(
                    core_directory,
                    module_name + ".py"
                )
            )
        )

    return file_paths


# =============================================================================
# File Discovery
# =============================================================================

def iter_python_files():
    """遍历正式代码目录中的全部 Python 文件。"""
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

                yield os.path.join(
                    directory,
                    file_name
                )


# =============================================================================
# AST Import Check
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


def contains_retired_name(imported_name, retired_names):
    """判断 Import 名称是否包含已经退休的 Core 模块名。"""
    name_parts = imported_name.split(".")

    for name_part in name_parts:
        if name_part in retired_names:
            return True

    return False


def scan_file(file_path):
    """扫描单个 Python 文件并返回历史 Core Import 问题。"""
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

    retired_names = get_retired_module_names()
    issues = []

    for node in ast.walk(syntax_tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        imported_names = get_imported_names(node)

        for imported_name in imported_names:
            if not contains_retired_name(
                    imported_name,
                    retired_names
            ):
                continue

            issues.append({
                "issue_type": "retired_import",
                "file": file_path,
                "line": getattr(node, "lineno", None),
                "import_name": imported_name,
            })

    return issues


# =============================================================================
# Retired File Check
# =============================================================================

def scan_retired_files():
    """
    检查已经删除的 CamelCase Core 文件是否被重新加入仓库。

    为什么单独检查文件存在：
        即使某个重新加入的兼容文件内部只 Import snake_case 实现，单纯 AST Import 扫描也未必能发现问题。
        因此这里把“历史文件重新出现”本身就视为架构回退。
    """
    issues = []

    for file_path in get_retired_file_paths():
        if not os.path.isfile(file_path):
            continue

        issues.append({
            "issue_type": "retired_file",
            "file": file_path,
            "line": None,
            "import_name": None,
        })

    return issues


def scan_repository():
    """扫描退休文件和全部正式 Python Import。"""
    issues = []
    file_count = 0

    # -------------------------------------------------------------------------
    # 步骤 1：退休 CamelCase 文件本身不允许重新出现。
    # -------------------------------------------------------------------------
    retired_file_issues = scan_retired_files()

    for issue in retired_file_issues:
        issues.append(issue)

    # -------------------------------------------------------------------------
    # 步骤 2：扫描正式源码中的 Import 语义。
    # -------------------------------------------------------------------------
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
    """运行 snake_case Core 架构 Gate。"""
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

            if issue["issue_type"] == "retired_file":
                print(
                    u"[FAIL] {} | 已退休的 CamelCase Core 文件重新出现".format(
                        relative_path
                    )
                )
                continue

            print(
                u"[FAIL] {}:{} | {}".format(
                    relative_path,
                    issue["line"],
                    issue["import_name"]
                )
            )
    else:
        print(
            u"[PASS] {} 个正式 Python 文件全部使用当前 Core 模块命名。".format(
                result["file_count"]
            )
        )
        print(
            u"[PASS] 已退休 CamelCase Core 文件保持删除状态。"
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
    "get_retired_module_names",
    "get_retired_file_paths",
    "iter_python_files",
    "scan_file",
    "scan_retired_files",
    "scan_repository",
    "run",
]


# =============================================================================
# Command Line Entry
# =============================================================================
#
# 该入口专门给 GitHub Actions / 普通 Python 环境使用。
# 测试只读取源码并解析 AST，不会 Import Maya，因此可以安全作为 CI Gate。
# =============================================================================
if __name__ == "__main__":
    test_result = run()

    if test_result["passed"]:
        raise SystemExit(0)

    raise SystemExit(1)
