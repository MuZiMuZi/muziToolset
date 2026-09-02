# coding=utf-8
u"""
Core Single Source Gate
=======================

检查 core/ 中高确定性的 Generic 能力只有一个正式实现位置。

本测试只扫描模块顶层 Function，不限制 Joint / Attr 等领域类自己的业务 Method。

目的：
    - 新增 Helper 前优先复用现有 Core；
    - 已经确定 Owner 的 Generic API 不允许在第二个 Core 模块重新实现；
    - 已退休的兼容入口不允许重新出现。
"""

from __future__ import print_function

import ast
import os


OWNER_BY_FUNCTION = {
    # Scene
    "undo_chunk": "core/scene_utils.py",
    "validate_node": "core/scene_utils.py",
    "ensure_nodes_available": "core/scene_utils.py",
    "get_long_name": "core/scene_utils.py",

    # Rename / external Maya name token
    "get_short_name": "core/rename_utils.py",
    "get_sanitized_short_name": "core/rename_utils.py",
    "get_name_token": "core/rename_utils.py",

    # Transform
    "validate_transform": "core/transform_utils.py",
    "get_world_translation": "core/transform_utils.py",
    "set_world_translation": "core/transform_utils.py",
    "get_world_rotation": "core/transform_utils.py",
    "set_world_rotation": "core/transform_utils.py",

    # Hierarchy
    "get_dag_depth": "core/hierarchy_utils.py",
    "get_parent": "core/hierarchy_utils.py",
    "get_children": "core/hierarchy_utils.py",
    "get_descendants": "core/hierarchy_utils.py",
    "parent": "core/hierarchy_utils.py",
    "ensure_group": "core/hierarchy_utils.py",
    "insert_parent_group": "core/hierarchy_utils.py",

    # Pure math
    "add_vector3": "core/math_utils.py",
    "subtract_vector3": "core/math_utils.py",
    "multiply_vector3": "core/math_utils.py",
    "length_vector3": "core/math_utils.py",
    "normalize_vector3": "core/math_utils.py",
    "dot_vector3": "core/math_utils.py",
    "distance_between_points": "core/math_utils.py",
    "lerp_point3": "core/math_utils.py",
    "average_point3": "core/math_utils.py",

    # Joint chain
    "validate_joint_list": "core/joint_chain_utils.py",
    "get_joint_path": "core/joint_chain_utils.py",
    "parent_joints_as_chain": "core/joint_chain_utils.py",
    "create_joints_at_items": "core/joint_chain_utils.py",
    "get_curve_joint_base_name": "core/joint_chain_utils.py",
    "create_joints_on_curve_cvs": "core/joint_chain_utils.py",

    # Export
    "ensure_fbx_plugin_loaded": "core/export_utils.py",
}


FORBIDDEN_TOP_LEVEL_COMPATIBILITY_FUNCTIONS = {
    "get_world_position",
    "maya_undo",
    "dag_depth",
    "require_selected_nodes",
    "export_selected_fbx",
    "average_vectors",
}


def get_package_root():
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(tests_directory)


def iter_core_python_files():
    core_root = os.path.join(
        get_package_root(),
        "core"
    )

    for file_name in os.listdir(core_root):
        if not file_name.endswith(".py"):
            continue

        yield os.path.join(
            core_root,
            file_name
        )


def get_relative_path(file_path):
    relative_path = os.path.relpath(
        file_path,
        get_package_root()
    )
    return relative_path.replace(os.sep, "/")


def scan_file(file_path):
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

    for node in syntax_tree.body:
        if not isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            continue

        function_name = node.name

        if function_name in OWNER_BY_FUNCTION:
            owner_path = OWNER_BY_FUNCTION[function_name]

            if relative_path != owner_path:
                issues.append({
                    "file": relative_path,
                    "line": node.lineno,
                    "name": function_name,
                    "owner": owner_path,
                })

        if function_name in FORBIDDEN_TOP_LEVEL_COMPATIBILITY_FUNCTIONS:
            issues.append({
                "file": relative_path,
                "line": node.lineno,
                "name": function_name,
                "owner": "领域 Core API",
            })

    return issues


def run():
    print("=" * 78)
    print("Muzi Toolset - Core Single Source Gate")
    print("=" * 78)

    issues = []
    file_count = 0

    for file_path in iter_core_python_files():
        file_count += 1
        file_issues = scan_file(file_path)

        for issue in file_issues:
            issues.append(issue)

    if issues:
        for issue in issues:
            print(
                u"[FAIL] {}:{} | {} 应统一归属 {}".format(
                    issue["file"],
                    issue["line"],
                    issue["name"],
                    issue["owner"]
                )
            )

        return False

    print(
        u"[PASS] {} 个 Core Python 文件符合 Single Source 规则。".format(
            file_count
        )
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
