# coding=utf-8
u"""
Upper Layer Core Reuse Gate
===========================

静态检查 ``systems/``、``tools/`` 与 ``ui/`` 是否绕开已经有明确 Core 归属的通用能力。

目标
----
项目完成一次去重并不够。如果以后新的 System / Tool / UI 又重新写：

    validate_node()
    validate_transform()
    get_short_name()
    _ensure_group()
    get_parent()
    get_long_name()
    get_world_position()
    get_world_translation()
    get_world_rotation()

代码会再次产生多套规则。

本测试把这些高确定性的重复实现直接变成 CI Failure。
它只使用 Python AST，不 Import Maya，因此可以在 GitHub Actions 普通 Python 环境运行。

Compatibility Policy
--------------------
正式上层代码不保留 Generic Core Helper Allowlist。历史入口完成迁移后直接删除。
"""

from __future__ import print_function

import ast
import os


# =============================================================================
# Configuration
# =============================================================================

def get_package_root():
    u"""返回 muziToolset 根目录。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    return os.path.dirname(
        tests_directory
    )


def get_scan_root_names():
    u"""返回必须复用 Core 的正式上层源码目录。"""
    return [
        "systems",
        "tools",
        "ui",
    ]


def get_forbidden_helper_names():
    u"""
    返回 System / Tool / UI 不应重新实现的通用 Helper 名称。

    这些能力已经有唯一正式 Core：
        Node Exists      -> core.scene_utils
        Transform Check  -> core.transform_utils
        Short Name       -> core.rename_utils
        Group Hierarchy  -> core.hierarchy_utils
        World Position   -> core.transform_utils
    """
    return {
        "validate_node",
        "_validate_node",
        "validate_transform",
        "get_short_name",
        "_short_name",
        "get_long_name",
        "_get_long_name",
        "get_parent",
        "_get_parent",
        "get_world_position",
        "_world_position",
        "get_world_translation",
        "_get_world_translation",
        "get_world_rotation",
        "_get_world_rotation",
        "get_dag_depth",
        "_ensure_group",
    }



# =============================================================================
# File Discovery
# =============================================================================

def iter_upper_layer_python_files():
    u"""遍历 systems / tools / ui 下全部正式 Python 文件。"""
    package_root = get_package_root()
    root_names = get_scan_root_names()

    for root_name in root_names:
        source_root = os.path.join(
            package_root,
            root_name
        )

        if not os.path.isdir(source_root):
            continue

        for directory, directory_names, file_names in os.walk(
                source_root
        ):
            filtered_directory_names = []

            for directory_name in directory_names:
                if directory_name == "__pycache__":
                    continue

                filtered_directory_names.append(
                    directory_name
                )

            directory_names[:] = filtered_directory_names

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                yield os.path.join(
                    directory,
                    file_name
                )


def get_relative_path(file_path):
    u"""返回相对于项目根目录的统一 POSIX 风格路径。"""
    relative_path = os.path.relpath(
        file_path,
        get_package_root()
    )

    return relative_path.replace(
        os.sep,
        "/"
    )


# =============================================================================
# AST Scan
# =============================================================================

def scan_file(file_path):
    u"""扫描单个 System / Tool / UI 文件中的重复通用 Helper 定义。"""
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
    forbidden_names = get_forbidden_helper_names()
    issues = []

    for node in ast.walk(syntax_tree):
        if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            function_name = node.name

            if function_name in forbidden_names:
                issues.append({
                    "file": relative_path,
                    "line": getattr(
                        node,
                        "lineno",
                        None
                    ),
                    "name": function_name,
                    "kind": "helper",
                })

        if not isinstance(node, ast.Call):
            continue

        call_function = node.func

        if not isinstance(call_function, ast.Attribute):
            continue

        if not isinstance(call_function.value, ast.Name):
            continue

        if call_function.value.id != "cmds":
            continue

        command_name = call_function.attr

        if command_name == "undoInfo":
            issues.append({
                "file": relative_path,
                "line": getattr(node, "lineno", None),
                "name": "cmds.undoInfo",
                "kind": "core_bypass",
            })
            continue

        constraint_commands = {
            "parentConstraint",
            "pointConstraint",
            "orientConstraint",
            "scaleConstraint",
            "aimConstraint",
            "poleVectorConstraint",
        }

        if command_name not in constraint_commands:
            continue

        is_query = False

        for keyword in node.keywords:
            if keyword.arg not in ["query", "q"]:
                continue

            if isinstance(keyword.value, ast.Constant):
                is_query = bool(keyword.value.value)

        if is_query:
            continue

        issues.append({
            "file": relative_path,
            "line": getattr(node, "lineno", None),
            "name": "cmds.{}".format(command_name),
            "kind": "core_bypass",
        })

    return issues


def scan_repository():
    u"""扫描全部正式 System / Tool / UI 文件。"""
    issues = []
    file_count = 0

    for file_path in iter_upper_layer_python_files():
        file_count += 1

        file_issues = scan_file(
            file_path
        )

        for issue in file_issues:
            issues.append(
                issue
            )

    return {
        "file_count": file_count,
        "issues": issues,
    }


# =============================================================================
# Runner
# =============================================================================

def run():
    u"""运行 Systems / Tools -> Core Reuse 架构门禁。"""
    print("=" * 78)
    print("Muzi Toolset - Upper Layer Core Reuse Gate")
    print("=" * 78)

    result = scan_repository()
    issues = result["issues"]

    if issues:
        for issue in issues:
            print(
                u"[FAIL] {}:{} | 上层代码绕开 Core: {}".format(
                    issue["file"],
                    issue["line"],
                    issue["name"]
                )
            )

        print(
            u"请优先复用 core.scene_utils / transform_utils / rename_utils / hierarchy_utils。"
        )
        return False

    print(
        u"[PASS] {} 个 System / Tool / UI Python 文件没有新增重复 Core Helper。".format(
            result["file_count"]
        )
    )
    return True


if __name__ == "__main__":
    success = run()

    if not success:
        raise SystemExit(1)
