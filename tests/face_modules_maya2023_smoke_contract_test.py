# coding=utf-8
u"""
Face Modules Maya 2023 Smoke Contract Test
==========================================

纯 Python / AST 静态契约，不启动 Autodesk Maya。

验证：
    1. 新 Face Module Runtime Smoke Runner 存在；
    2. Runner 使用正式 FaceSetup / FaceGuide Fixture；
    3. 所有正式 Face 部位都在 MODULE_CASES 中；
    4. Eyelid 明确依赖 Eye；
    5. Mouth 明确依赖 Jaw + Lip；
    6. 正式构建入口只使用 create_build()；
    7. Runner 不重新依赖 Legacy Face Bind。
"""

from __future__ import print_function

import ast
import os


TESTS_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SMOKE_PATH = os.path.join(
    TESTS_DIR,
    "face_modules_maya2023_smoke_test.py"
)

REQUIRED_FUNCTIONS = {
    "prepare_default_shading_group",
    "restore_default_shading_group",
    "create_fixture_models",
    "create_face_fixture",
    "create_dependency_skip_result",
    "run_module_case",
    "print_case_result",
    "run",
}

REQUIRED_MODULE_LABELS = [
    "BrowModule",
    "EyeModule",
    "EyelidModule",
    "NoseModule",
    "CheekModule",
    "EarModule",
    "JawModule",
    "TeethModule",
    "TongueModule",
    "LipModule",
    "MouthModule",
]


def get_module_cases(module_tree):
    u"""从 AST 读取 MODULE_CASES 的字面量数据。"""
    for node in module_tree.body:
        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if not isinstance(target, ast.Name):
                continue

            if target.id != "MODULE_CASES":
                continue

            return node.value

    raise AssertionError(
        u"Smoke Runner 缺少 MODULE_CASES。"
    )


def get_case_literals(module_cases_node):
    u"""读取 MODULE_CASES 中可静态确认的 key / label / dependencies。"""
    if not isinstance(module_cases_node, ast.List):
        raise AssertionError(
            u"MODULE_CASES 必须使用显式 List。"
        )

    case_list = []

    for element_node in module_cases_node.elts:
        if not isinstance(element_node, ast.Dict):
            raise AssertionError(
                u"MODULE_CASES 每一项必须是显式 Dict。"
            )

        case_data = {}
        pair_index = 0

        while pair_index < len(element_node.keys):
            key_node = element_node.keys[pair_index]
            value_node = element_node.values[pair_index]

            if isinstance(key_node, ast.Constant):
                key_name = key_node.value
            else:
                pair_index += 1
                continue

            if key_name in ["key", "label"]:
                if isinstance(value_node, ast.Constant):
                    case_data[key_name] = value_node.value

            if key_name == "dependencies":
                dependencies = []

                if isinstance(value_node, ast.List):
                    for dependency_node in value_node.elts:
                        if not isinstance(dependency_node, ast.Constant):
                            continue

                        dependencies.append(
                            dependency_node.value
                        )

                case_data[key_name] = dependencies

            pair_index += 1

        case_list.append(
            case_data
        )

    return case_list


def main():
    u"""执行新 Face Modules Maya 2023 Smoke Runner 静态契约。"""
    # -------------------------------------------------------------------------
    # Step 01：确认 Runner 文件存在并能被 Python AST 正常解析
    # -------------------------------------------------------------------------
    if not os.path.isfile(SMOKE_PATH):
        raise AssertionError(
            u"缺少 face_modules_maya2023_smoke_test.py。"
        )

    with open(SMOKE_PATH, "r", encoding="utf-8") as file_object:
        source = file_object.read()

    module_tree = ast.parse(
        source,
        filename=SMOKE_PATH
    )

    # -------------------------------------------------------------------------
    # Step 02：检查必须存在的正式 Runner 函数
    # -------------------------------------------------------------------------
    function_names = set()

    for node in module_tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue

        function_names.add(
            node.name
        )

    missing_functions = REQUIRED_FUNCTIONS.difference(
        function_names
    )

    if missing_functions:
        raise AssertionError(
            u"Face Module Smoke Runner 缺少函数：{}".format(
                ", ".join(sorted(missing_functions))
            )
        )

    # -------------------------------------------------------------------------
    # Step 03：检查全部正式 Face Module 都进入逐模块 Runtime Case
    # -------------------------------------------------------------------------
    case_list = get_case_literals(
        get_module_cases(module_tree)
    )
    case_label_list = []
    case_by_key = {}

    for case_data in case_list:
        case_label_list.append(
            case_data.get("label")
        )
        case_by_key[case_data.get("key")] = case_data

    if case_label_list != REQUIRED_MODULE_LABELS:
        raise AssertionError(
            u"Face Module Runtime 顺序错误：{}".format(
                case_label_list
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：检查跨模块显式依赖，避免依赖关系重新藏进业务代码
    # -------------------------------------------------------------------------
    if case_by_key["eyelid"].get("dependencies") != ["eye"]:
        raise AssertionError(
            u"EyelidModule 必须显式依赖 EyeModule。"
        )

    if case_by_key["mouth"].get("dependencies") != ["jaw", "lip"]:
        raise AssertionError(
            u"MouthModule 必须显式依赖 JawModule + LipModule。"
        )

    # -------------------------------------------------------------------------
    # Step 05：检查 Runner 使用当前正式 Fixture / Lifecycle，而不是旧 Bind API
    # -------------------------------------------------------------------------
    required_text_list = [
        "face_system.FaceSetup",
        "face_system.FaceGuide",
        "face_setup.run_step()",
        "face_guide.build_guide()",
        "face_guide.run_step()",
        "face_module.create_build()",
        "mouth_jnt_number=32",
        "DEFAULT_SHADING_GROUP = \":initialShadingGroup\"",
        "prepare_default_shading_group()",
        "restore_default_shading_group(",
    ]

    for required_text in required_text_list:
        if required_text in source:
            continue

        raise AssertionError(
            u"Face Module Smoke Runner 缺少契约：{}".format(
                required_text
            )
        )

    retired_text_list = [
        "legacy_reference",
        ".build_rig(",
        ".build_setup(",
        ".create_bpjnt(",
        ".create_joint(",
        ".add_constraint(",
    ]

    for retired_text in retired_text_list:
        if retired_text not in source:
            continue

        raise AssertionError(
            u"Face Module Smoke Runner 重新使用退休入口：{}".format(
                retired_text
            )
        )

    print(
        u"Face Modules Maya 2023 Smoke Contract: PASS"
    )


if __name__ == "__main__":
    main()
