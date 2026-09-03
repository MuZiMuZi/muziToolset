# coding=utf-8
u"""Locator 可视世界位置修复的非 Maya 静态契约检查。"""

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
    u"""确认源文件包含本修复不能移除的契约文本。"""
    source_text = read_source(
        relative_path
    )

    for required_text in required_texts:
        if required_text not in source_text:
            raise RuntimeError(
                u"{} 缺少 Locator Alignment 契约：{}".format(
                    relative_path,
                    required_text
                )
            )

    return True


def run():
    u"""验证 Locator Shape、Joint、Face 计算和 Maya 回归覆盖。"""
    require_text(
        "resources/face/face_guide.ma",
        [
            'setAttr ".lp" -type "double3"',
        ]
    )
    require_text(
        "core/snap_utils.py",
        [
            'type="locator"',
            '".worldPosition[0]"',
        ]
    )
    require_text(
        "core/joint_utils.py",
        [
            "snap_utils.get_item_world_position(",
        ]
    )

    guide_position_consumers = [
        "systems/face/guide/face_guide.py",
        "systems/face/modules/eye.py",
        "systems/face/modules/mouth.py",
    ]

    for relative_path in guide_position_consumers:
        require_text(
            relative_path,
            [
                "snap_utils.get_item_world_position(",
            ]
        )

    require_text(
        "tests/ctrl_base_smoke_test.py",
        [
            "test_locator_visual_position",
            'guide_shape + ".localPosition"',
            "joint_utils.Joint.create_at_object(",
        ]
    )
    require_text(
        "tests/face_build_step_maya2023_smoke_test.py",
        [
            "validate_guide_ctrl_alignment",
            '"ctrl_lf_eye_main_001"',
            '"ctrl_md_nose_center_bind_001"',
            '"ctrl_rt_ear_fk_003"',
            '"ctrl_md_jaw_bind_001"',
            '"ctrl_rt_cheekbone_bind_002"',
        ]
    )

    print(
        "[PASS] Locator Shape worldPosition 与 Face Guide/Ctrl Runtime 契约完整。"
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
