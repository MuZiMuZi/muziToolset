# coding=utf-8
u"""Maya 2023 Smoke Runner 的非 Maya 静态契约检查。"""

from __future__ import print_function

import ast
import os


REQUIRED_FUNCTIONS = {
    "require_maya_2023",
    "test_core_contract",
    "test_controller_contract",
    "test_face_step_contract",
    "run",
}


def get_smoke_path():
    u"""返回 Maya 2023 Runtime Smoke Runner 路径。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.join(
        tests_directory,
        "maya2023_smoke_test.py"
    )


def run():
    u"""检查 Maya 2023 Smoke Runner 的当前架构契约。"""
    smoke_path = get_smoke_path()

    if not os.path.isfile(smoke_path):
        print("[FAIL] maya2023_smoke_test.py 不存在。")
        return False

    with open(
            smoke_path,
            "r",
            encoding="utf-8"
    ) as source_file:
        source_text = source_file.read()

    syntax_tree = ast.parse(
        source_text,
        filename=smoke_path
    )

    function_names = set()

    for node in syntax_tree.body:
        if isinstance(node, ast.FunctionDef):
            function_names.add(
                node.name
            )

    missing_functions = []

    for function_name in REQUIRED_FUNCTIONS:
        if function_name not in function_names:
            missing_functions.append(
                function_name
            )

    if missing_functions:
        print(
            "[FAIL] Maya 2023 Smoke Runner 缺少入口：{}".format(
                ", ".join(
                    sorted(missing_functions)
                )
            )
        )
        return False

    required_texts = [
        "import maya.cmds as cmds",
        "face_build_smoke_test",
        "ctrl_base.create_ctrl",
        "face_setup.run_step()",
        "FaceGuide",
        "build_guide",
        "create_name",
    ]

    for required_text in required_texts:
        if required_text not in source_text:
            print(
                "[FAIL] Maya 2023 Smoke Runner 缺少契约文本：{}".format(
                    required_text
                )
            )
            return False

    retired_texts = [
        "face_component_smoke_test",
        "systems import controller",
        "Hierarchy.parent",
        "Hierarchy.get_parent",
    ]

    for retired_text in retired_texts:
        if retired_text in source_text:
            print(
                "[FAIL] Maya 2023 Smoke Runner 仍包含退休入口：{}".format(
                    retired_text
                )
            )
            return False

    print(
        "[PASS] Maya 2023 Smoke Runner 当前架构静态契约完整。"
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
