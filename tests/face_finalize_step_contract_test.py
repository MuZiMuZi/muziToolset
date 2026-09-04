# coding=utf-8
u"""
Face Finalize Step Contract Test
================================

纯 Python / AST 静态契约，不启动 Autodesk Maya。

验证：
    1. Step 04 正式 FaceFinalizer 文件存在并可被 AST 解析；
    2. FaceFinalizer 保持 Workflow 四阶段生命周期；
    3. Finalize 只做最终验收、Controller Set、Visibility 和 Step 状态；
    4. 成功后必须标记 Step 04 完成，并保持 Current Face Step = 04；
    5. Finalize 不允许重新创建 Joint / Controller / Matrix / Deformer；
    6. 正式 UI 允许通过 Lifecycle Controller 继续继承 finalize_controller。
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

FACE_FINALIZER_PATH = os.path.join(
    PACKAGE_DIR,
    "systems",
    "face",
    "finalize",
    "finalizer.py"
)

FACE_UI_INIT_PATH = os.path.join(
    PACKAGE_DIR,
    "systems",
    "face",
    "ui",
    "__init__.py"
)

FACE_UI_CONTROLLER_PATH = os.path.join(
    PACKAGE_DIR,
    "systems",
    "face",
    "ui",
    "face_rig_controller.py"
)

LIFECYCLE_CONTROLLER_PATH = os.path.join(
    PACKAGE_DIR,
    "systems",
    "face",
    "ui",
    "lifecycle_controller.py"
)

REQUIRED_METHODS = [
    "__init__",
    "collect_inputs",
    "prepare_data",
    "process_data",
    "finalize_step",
    "run_step",
]


def main():
    u"""执行 Face Workflow Step 04 静态架构契约。"""
    # -------------------------------------------------------------------------
    # Step 01：确认正式 Step 04 文件存在并可以被 AST 解析
    # -------------------------------------------------------------------------
    if not os.path.isfile(FACE_FINALIZER_PATH):
        raise AssertionError(
            u"缺少 systems/face/finalize/finalizer.py。"
        )

    with open(FACE_FINALIZER_PATH, "r", encoding="utf-8") as file_object:
        source = file_object.read()

    module_tree = ast.parse(
        source,
        filename=FACE_FINALIZER_PATH
    )

    # -------------------------------------------------------------------------
    # Step 02：找到 FaceFinalizer，并确认 Workflow 生命周期方法完整
    # -------------------------------------------------------------------------
    face_finalizer_class = None

    for node in module_tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        if node.name != "FaceFinalizer":
            continue

        face_finalizer_class = node
        break

    if face_finalizer_class is None:
        raise AssertionError(
            u"finalizer.py 缺少 FaceFinalizer。"
        )

    method_names = []

    for node in face_finalizer_class.body:
        if not isinstance(node, ast.FunctionDef):
            continue

        method_names.append(
            node.name
        )

    for required_method in REQUIRED_METHODS:
        if required_method in method_names:
            continue

        raise AssertionError(
            u"FaceFinalizer 缺少方法：{}".format(
                required_method
            )
        )

    # -------------------------------------------------------------------------
    # Step 03：确认 Step 04 正式职责和 Workflow 状态契约
    # -------------------------------------------------------------------------
    required_text_list = [
        "self.step_value = 4",
        "self.controller_nodes = self.collect_face_controllers()",
        "self.controller_set = self.ensure_controller_set()",
        "self.visibility_state = self.apply_final_visibility()",
        "scene_utils.ensure_object_set(",
        "self.set_step_completed(\n            completed=True",
        "self.set_current_step_value(\n            4",
        "def finalize_face():",
        "finalizer.run_step()",
    ]

    for required_text in required_text_list:
        if required_text in source:
            continue

        raise AssertionError(
            u"FaceFinalizer 缺少正式契约：{}".format(
                required_text
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：禁止 Finalize 越界重新构建绑定结构
    # -------------------------------------------------------------------------
    retired_text_list = [
        ".create_jnt(",
        ".create_ctrl(",
        ".create_connect(",
        ".create_deform(",
        "FaceRig()",
        "FaceBuild()",
        "build_face_step(",
        "cmds.joint(",
        "cmds.skinCluster(",
        "cmds.blendShape(",
    ]

    for retired_text in retired_text_list:
        if retired_text not in source:
            continue

        raise AssertionError(
            u"FaceFinalizer 越过 Step 04 边界：{}".format(
                retired_text
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：确认最终 UI 通过 Lifecycle Controller 继续继承 Finalize
    # -------------------------------------------------------------------------
    if not os.path.isfile(FACE_UI_INIT_PATH):
        raise AssertionError(
            u"缺少 systems/face/ui/__init__.py。"
        )

    with open(FACE_UI_INIT_PATH, "r", encoding="utf-8") as file_object:
        ui_source = file_object.read()

    if "from . import face_rig_controller" not in ui_source:
        raise AssertionError(
            u"Face UI 尚未路由到最终 face_rig_controller。"
        )

    if "return face_rig_controller.main()" not in ui_source:
        raise AssertionError(
            u"Face UI show() 没有返回最终 Face Rig Controller。"
        )

    if not os.path.isfile(FACE_UI_CONTROLLER_PATH):
        raise AssertionError(
            u"缺少 systems/face/ui/face_rig_controller.py。"
        )

    with open(FACE_UI_CONTROLLER_PATH, "r", encoding="utf-8") as file_object:
        controller_source = file_object.read()

    if "from . import lifecycle_controller" not in controller_source:
        raise AssertionError(
            u"最终 Face Rig Controller 尚未路由到 lifecycle_controller。"
        )

    if "class FaceRigWizard(lifecycle_controller.FaceRigWizard):" not in controller_source:
        raise AssertionError(
            u"最终 Face Rig Wizard 没有继承 Workflow Lifecycle Controller。"
        )

    if not os.path.isfile(LIFECYCLE_CONTROLLER_PATH):
        raise AssertionError(
            u"缺少 systems/face/ui/lifecycle_controller.py。"
        )

    with open(LIFECYCLE_CONTROLLER_PATH, "r", encoding="utf-8") as file_object:
        lifecycle_source = file_object.read()

    if "from . import finalize_controller" not in lifecycle_source:
        raise AssertionError(
            u"Workflow Lifecycle Controller 尚未继承 finalize_controller。"
        )

    if "class FaceRigWizard(finalize_controller.FaceRigWizard):" not in lifecycle_source:
        raise AssertionError(
            u"Workflow Lifecycle Wizard 没有继承 Step 04 Finalize Controller。"
        )

    # -------------------------------------------------------------------------
    # Step 06：完成静态契约
    # -------------------------------------------------------------------------
    print(
        u"Face Finalize Step Contract: PASS"
    )


if __name__ == "__main__":
    main()
