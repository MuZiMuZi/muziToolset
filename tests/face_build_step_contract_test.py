# coding=utf-8
u"""
Face Build Step Contract Test
=============================

纯 Python / AST 静态契约，不启动 Autodesk Maya。

验证：
    1. Step 03 正式 FaceBuild 文件存在；
    2. FaceBuild 只通过 FaceRig Orchestrator 组装完整 Rig；
    3. Workflow Step 使用 run_step() 四阶段接口，不复制 Face Module 生命周期；
    4. 成功后必须标记 Step 03 完成并推进到 Step 04；
    5. Step 03 不直接导入 Brow / Eye / Lip 等具体 Module。
"""

from __future__ import print_function

import ast
import os


TESTS_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PACKAGE_DIR = os.path.dirname(
    TESTS_DIR
)

FACE_BUILD_PATH = os.path.join(
    PACKAGE_DIR,
    "systems",
    "face",
    "build",
    "face_build.py"
)

REQUIRED_METHODS = [
    "__init__",
    "collect_inputs",
    "prepare_data",
    "process_data",
    "finalize_step",
]


def main():
    u"""执行 Face Workflow Step 03 静态架构契约。"""
    # -------------------------------------------------------------------------
    # Step 01：确认正式 Step 03 文件存在并可以被 AST 解析
    # -------------------------------------------------------------------------
    if not os.path.isfile(FACE_BUILD_PATH):
        raise AssertionError(
            u"缺少 systems/face/build/face_build.py。"
        )

    with open(FACE_BUILD_PATH, "r", encoding="utf-8") as file_object:
        source = file_object.read()

    module_tree = ast.parse(
        source,
        filename=FACE_BUILD_PATH
    )

    # -------------------------------------------------------------------------
    # Step 02：找到 FaceBuild，并确认 Workflow 四阶段方法完整
    # -------------------------------------------------------------------------
    face_build_class = None

    for node in module_tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        if node.name != "FaceBuild":
            continue

        face_build_class = node
        break

    if face_build_class is None:
        raise AssertionError(
            u"face_build.py 缺少 FaceBuild。"
        )

    method_names = []

    for node in face_build_class.body:
        if not isinstance(node, ast.FunctionDef):
            continue

        method_names.append(
            node.name
        )

    for required_method in REQUIRED_METHODS:
        if required_method in method_names:
            continue

        raise AssertionError(
            u"FaceBuild 缺少方法：{}".format(
                required_method
            )
        )

    # -------------------------------------------------------------------------
    # Step 03：确认 Step 03 只通过 FaceRig Orchestrator 进入全部 Face Module
    # -------------------------------------------------------------------------
    required_text_list = [
        "self.step_value = 3",
        "self.face_rig = FaceRig()",
        "self.face_rig.create_build()",
        "self.set_step_completed(\n            completed=True",
        "self.set_current_step_value(\n            4",
        "def build_face_step():",
        "face_build.run_step()",
    ]

    for required_text in required_text_list:
        if required_text in source:
            continue

        raise AssertionError(
            u"FaceBuild 缺少正式契约：{}".format(
                required_text
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：禁止 Step 03 重新知道具体部位 Module，避免 Orchestrator 失去边界
    # -------------------------------------------------------------------------
    retired_text_list = [
        "BrowModule",
        "CheekModule",
        "EarModule",
        "EyeModule",
        "EyelidModule",
        "JawModule",
        "LipModule",
        "MouthModule",
        "NoseModule",
        "TeethModule",
        "TongueModule",
        ".create_jnt(",
        ".create_ctrl(",
        ".create_connect(",
        ".create_deform(",
    ]

    for retired_text in retired_text_list:
        if retired_text not in source:
            continue

        raise AssertionError(
            u"FaceBuild 越过 FaceRig 边界：{}".format(
                retired_text
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：完成静态契约
    # -------------------------------------------------------------------------
    print(
        u"Face Build Step Contract: PASS"
    )


if __name__ == "__main__":
    main()
