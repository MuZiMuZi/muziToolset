# coding=utf-8
u"""
Face Workflow Lifecycle Contract Test
=====================================

纯 Python 文本契约，不启动 Autodesk Maya。

验证当前正式 Wizard 的关键交互规则：
    1. Step 02 下一步自动 Build；
    2. Step 03 只显示 Controller Appearance；
    3. 顶部 Step Button 只允许向后；
    4. 回退时使用统一 Lifecycle Cleanup；
    5. Guide Snapshot 和 Scene Manifest 都持久化；
    6. 下一步按钮不接受 Enter / Return 默认激活；
    7. 正式 Controller 默认大小符合当前制作标准。
"""

from __future__ import print_function

import os


TESTS_DIR = os.path.dirname(
    os.path.abspath(__file__)
)
PACKAGE_DIR = os.path.dirname(
    TESTS_DIR
)


def read_source(relative_path):
    u"""
    读取 Package 内一个 UTF-8 源文件。

    Args:
        relative_path (str):
            相对 Package Root 的文件路径。

    Returns:
        str:
            文件完整文本。
    """
    file_path = os.path.join(
        PACKAGE_DIR,
        relative_path
    )

    with open(file_path, "r", encoding="utf-8") as file_object:
        return file_object.read()


def require_text(
        relative_path,
        required_texts
):
    u"""
    确认文件包含指定 Workflow 契约文本。

    Args:
        relative_path (str):
            相对 Package Root 的文件路径。
        required_texts (list[str]):
            必须存在的文本列表。

    Returns:
        bool:
            所有契约都存在时返回 True。
    """
    source = read_source(
        relative_path
    )

    for required_text in required_texts:
        if required_text in source:
            continue

        raise AssertionError(
            u"{} 缺少 Workflow Lifecycle 契约：{}".format(
                relative_path,
                required_text
            )
        )

    return True


def main():
    u"""执行 Face Workflow Lifecycle 静态契约。"""
    require_text(
        "systems/face/ui/face_rig_controller.py",
        [
            "from . import lifecycle_controller",
            "class FaceRigWizard(lifecycle_controller.FaceRigWizard):",
        ]
    )

    require_text(
        "systems/face/ui/lifecycle_controller.py",
        [
            "def clicked_next_button(self):",
            "if self.current_step_index == 1:",
            "if not self.finalize_step2():",
            "if not self.clicked_build_face():",
            "face_guide.set_current_step_value(\n                3",
            "if self.current_step_index == 2:",
            "face_context.set_current_step_value(\n                4",
            "def clicked_step_button(self):",
            "if step_index >= self.current_step_index:",
            "workflow_lifecycle.cleanup_to_step(",
            "self.next_button.setAutoDefault(\n            False",
            "self.next_button.setDefault(\n            False",
            "self.next_button.setFocusPolicy(\n            Qt.NoFocus",
            "u\"Controller Appearance\"",
            "self.build_face_button.setVisible(\n            False",
        ]
    )

    require_text(
        "systems/face/workflow_lifecycle.py",
        [
            'GUIDE_SNAPSHOT_ATTR = "face_guide_snapshot_json"',
            '3: "face_step_03_scene_manifest_json"',
            '4: "face_step_04_scene_manifest_json"',
            "def capture_scene_state():",
            "def create_scene_manifest(before_state):",
            "def save_guide_snapshot(face_guide):",
            "def restore_guide_snapshot(face_guide):",
            "def cleanup_to_step(",
            "face_guide.remove_guide_content()",
            "cleanup_legacy_step3_content(",
        ]
    )

    require_text(
        "systems/face/controller_defaults.py",
        [
            '"global_scale": 1.0',
            '"color_lf": 6',
            '"color_rt": 13',
            '"color_md": 17',
            '"brow": 1.1',
            '"eye": 1.0',
            '"eyelid": 1.3',
            '"nose": 0.5',
            '"cheek": 1.3',
            '"lip": 1.8',
            '"jaw": 1.0',
            '"teeth": 1.0',
            '"tongue": 1.0',
        ]
    )

    require_text(
        "systems/face/__init__.py",
        [
            "from .controller_defaults import apply_controller_defaults",
            "apply_controller_defaults()",
        ]
    )

    print(
        u"Face Workflow Lifecycle Contract: PASS"
    )


if __name__ == "__main__":
    main()
