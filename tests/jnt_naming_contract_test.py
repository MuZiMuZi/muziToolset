# coding=utf-8
u"""
Jnt Naming Contract Test
========================

纯 Python 静态门禁，不需要 Autodesk Maya。

本 Gate 只约束**当前正式 Runtime**，不把 Compatibility / Migration Source 当成新架构。

当前扫描范围：
    app/
    ui/
    core/common/
    core/rigging/
    systems/
    tools/

明确不属于本 Gate：
    core/bake/
        历史 Compatibility Module，允许保留 jointUtils 等旧命名用于迁移参考。

    legacy_reference/
        已退休实现。

    scripts/
        迁移、审计、文档维护脚本可以提到旧名称。

    tests/
        测试配置本身可能需要描述被禁止的旧名称，不属于 Runtime Naming Contract。

规则：
    1. 当前 MuziTools 自有 Joint 命名统一使用 jnt / Jnt；
    2. Maya 官方 API 仍必须使用 cmds.joint / jointDisplayScale；
    3. Maya Joint Node Type 字符串仍必须是 ``"joint"``；
    4. 当前 Runtime 禁止重新使用 joint_utils / tools.joint 等退休项目入口。
"""

from __future__ import print_function

import os
import re


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SCAN_ROOTS = [
    os.path.join("app"),
    os.path.join("ui"),
    os.path.join("core", "common"),
    os.path.join("core", "rigging"),
    os.path.join("systems"),
    os.path.join("tools"),
]

FORBIDDEN_PROJECT_TEXT = [
    "joint_utils",
    "joint_chain_utils",
    "tools.joint",
    "tools/joint",
    "joint_tool",
    "joint_resamp_tool",
]

FORBIDDEN_MAYA_API_TEXT = [
    "cmds.jnt(",
    "cmds.jntDisplayScale(",
    "maya.cmds.jnt(",
    "maya.cmds.jntDisplayScale(",
    "orientjnt=",
    ".jntOrient",
]

MAYA_COMMANDS_WITH_NODE_TYPE = [
    "ls",
    "listRelatives",
    "listConnections",
    "createNode",
]


def iter_python_files():
    u"""遍历当前正式 Runtime 中的 Python 文件。"""
    for root_name in SCAN_ROOTS:
        root_path = os.path.join(
            REPO_ROOT,
            root_name
        )

        if not os.path.isdir(root_path):
            continue

        for current_root, dir_names, file_names in os.walk(root_path):
            dir_names[:] = [
                dir_name
                for dir_name in dir_names
                if dir_name != "__pycache__"
            ]

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                yield os.path.join(
                    current_root,
                    file_name
                )


def read_source(file_path):
    u"""读取 UTF-8 Python Source。"""
    with open(file_path, "r", encoding="utf-8") as file_object:
        return file_object.read()


def assert_paths_use_jnt():
    u"""当前正式 Runtime 路径中禁止重新使用 joint 作为项目命名。"""
    invalid_paths = []

    for root_name in SCAN_ROOTS:
        root_path = os.path.join(
            REPO_ROOT,
            root_name
        )

        if not os.path.exists(root_path):
            continue

        for current_root, dir_names, file_names in os.walk(root_path):
            relative_root = os.path.relpath(
                current_root,
                REPO_ROOT
            )

            path_parts = relative_root.replace("\\", "/").split("/")

            for path_part in path_parts:
                if "joint" in path_part.lower():
                    invalid_paths.append(relative_root)
                    break

            for file_name in file_names:
                if "joint" not in file_name.lower():
                    continue

                invalid_paths.append(
                    os.path.join(
                        relative_root,
                        file_name
                    )
                )

    if invalid_paths:
        raise AssertionError(
            u"当前正式 Runtime 路径仍包含 joint：{}".format(
                ", ".join(sorted(set(invalid_paths)))
            )
        )


def assert_project_imports_use_jnt():
    u"""当前 Runtime 禁止旧 Joint Project Import / Tool Entry。"""
    issues = []

    for file_path in iter_python_files():
        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_PROJECT_TEXT:
            if forbidden_text not in source:
                continue

            issues.append(
                u"{} -> {}".format(
                    os.path.relpath(file_path, REPO_ROOT),
                    forbidden_text
                )
            )

    if issues:
        raise AssertionError(
            u"当前正式 Runtime 仍存在旧 Joint Project 命名：{}".format(
                "; ".join(issues)
            )
        )


def assert_maya_api_is_not_renamed():
    u"""禁止把 Maya 官方 Joint API 错改为 jnt。"""
    issues = []

    for file_path in iter_python_files():
        source = read_source(file_path)

        for forbidden_text in FORBIDDEN_MAYA_API_TEXT:
            if forbidden_text not in source:
                continue

            issues.append(
                u"{} -> {}".format(
                    os.path.relpath(file_path, REPO_ROOT),
                    forbidden_text
                )
            )

        command_pattern = re.compile(
            r"cmds\.(?:ls|listRelatives|listConnections)\([^\)]*?type\s*=\s*['\"]jnt['\"]",
            re.DOTALL
        )
        if command_pattern.search(source):
            issues.append(
                u"{} -> Maya type='jnt'".format(
                    os.path.relpath(file_path, REPO_ROOT)
                )
            )

        create_node_pattern = re.compile(
            r"cmds\.createNode\(\s*['\"]jnt['\"]"
        )
        if create_node_pattern.search(source):
            issues.append(
                u"{} -> cmds.createNode('jnt')".format(
                    os.path.relpath(file_path, REPO_ROOT)
                )
            )

        node_type_pattern = re.compile(
            r"cmds\.nodeType\([^\)]*\)\s*(?:==|!=)\s*['\"]jnt['\"]"
        )
        if node_type_pattern.search(source):
            issues.append(
                u"{} -> cmds.nodeType(...) jnt".format(
                    os.path.relpath(file_path, REPO_ROOT)
                )
            )

    if issues:
        raise AssertionError(
            u"Maya Joint API 被错误改名：{}".format(
                "; ".join(issues)
            )
        )


def main():
    u"""执行当前正式 Runtime 的 Jnt Naming 静态契约。"""
    assert_paths_use_jnt()
    assert_project_imports_use_jnt()
    assert_maya_api_is_not_renamed()

    print(
        u"[PASS] Current Runtime Jnt Naming / Maya Joint API Contract 正常。"
    )
    print(
        u"[PASS] Compatibility / Migration Source 不参与当前 Naming Gate。"
    )


if __name__ == "__main__":
    main()
