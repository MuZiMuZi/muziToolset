# coding=utf-8
u"""Face Step 03 Controller Appearance 的非 Maya 静态契约检查。"""

from __future__ import print_function

import os


def get_package_root():
    u"""返回 muziToolset Package Root。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(
        tests_directory
    )


def read_source(relative_path):
    u"""读取 Package 内的 UTF-8 源文件。"""
    file_path = os.path.join(
        get_package_root(),
        relative_path
    )

    with open(
            file_path,
            "r",
            encoding="utf-8"
    ) as source_file:
        return source_file.read()


def require_text(relative_path, required_texts):
    u"""确认源文件包含本功能不能移除的契约文本。"""
    source_text = read_source(
        relative_path
    )

    for required_text in required_texts:
        if required_text not in source_text:
            raise RuntimeError(
                u"{} 缺少 Controller Appearance 契约：{}".format(
                    relative_path,
                    required_text
                )
            )

    return True


def run():
    u"""验证 Step 03 UI、Shape-only 更新、Config 单数据源和 Maya Runner 契约。"""
    require_text(
        "systems/face/ui/build_controller.py",
        [
            "Controller Appearance",
            "controller_appearance.apply_controller_settings(",
            "face_context.save_controller_settings(",
            "if step_value == 3:",
            "self.controller_size_widgets = {}",
            "self.controller_color_widgets = {}",
        ]
    )

    require_text(
        "systems/face/controller_appearance.py",
        [
            "def _resolve_face_ctrl_set():",
            'type="objectSet"',
            "def _get_canonical_short_name(node):",
            "CONTROLLER_MODULE_PART_ALIASES = {",
            '"cheekbone",',
            '"nasolabial",',
            "control_shape_utils.scale_shape(",
            "control_shape_utils.set_shape_color(",
            "scale_ratio = new_effective_size / old_effective_size",
        ]
    )

    require_text(
        "tests/face_controller_appearance_maya2023_smoke_test.py",
        [
            '"ctrl_rt_cheekbone_bind_002"',
            '"module": "cheek"',
            "_validate_controller_transform_invariants(",
            "_validate_joint_invariants(",
            "_validate_representative_appearance(",
            "validate_guide_ctrl_alignment()",
            '"transform_scale_invariant": [1.0, 1.0, 1.0]',
        ]
    )

    require_text(
        "__init__.py",
        [
            "def face_controller_appearance_maya2023_smoke_test():",
            '"face_controller_appearance_maya2023_smoke_test",',
        ]
    )

    appearance_source = read_source(
        "systems/face/controller_appearance.py"
    )

    forbidden_transform_edits = [
        "cmds.xform(",
        "cmds.move(",
        "cmds.rotate(",
        "cmds.scale(",
        "snap_to_average(",
        "set_world_matrix(",
    ]

    for forbidden_text in forbidden_transform_edits:
        if forbidden_text in appearance_source:
            raise RuntimeError(
                u"Controller Appearance 不允许修改 Transform / Guide 对齐：{}".format(
                    forbidden_text
                )
            )

    build_source = read_source(
        "systems/face/ui/build_controller.py"
    )

    controller_changed_start = build_source.find(
        "def controller_settings_changed("
    )
    state_section_start = build_source.find(
        "# Step 03 State / Navigation"
    )

    if controller_changed_start < 0 or state_section_start < 0:
        raise RuntimeError(
            u"没有找到 Step 03 Controller Settings 回调边界。"
        )

    controller_changed_source = build_source[
        controller_changed_start:state_section_start
    ]

    if "mark_step2_dirty(" in controller_changed_source:
        raise RuntimeError(
            u"Controller Appearance 调整不应把 Step 02 Guide 标记 Dirty。"
        )

    print(
        "[PASS] Face Step 03 Controller Appearance 静态契约完整。"
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
