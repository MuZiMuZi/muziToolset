# coding=utf-8
u"""
Locator Visual Position Contract Test
====================================

验证当前正式 Runtime 仍然正确处理 Maya Locator 的**可见世界位置**。

为什么需要这个契约：
    Locator Transform 的 translate 并不一定等于用户在 Viewport 中看到的定位点。
    Locator Shape 可以通过 ``localPosition`` 产生局部偏移，因此 Guide → Joint / Ctrl
    对齐必须读取 Shape 的 ``worldPosition[0]``，不能只复制 Transform 原点。

当前正式数据路径：

    resources/face/face_guide.ma
        Locator Shape.localPosition
            ↓
    core/common/transform_utils.py
        Transform.match_transform()
        Locator Shape.worldPosition[0]
            ↓
    core/rigging/jnt_utils.py
        Jnt.set_match_transform()
            ↓
    systems/rig_module.py
        create_joint() / create_ctrl()
            ↓
    systems/face/* / systems/components/*

本测试只检查当前 Runtime Contract，不再引用已经退休的 ``core/snap_utils.py``、
``systems/face/modules/*`` 或旧 Face Build Step 测试。
"""

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
    u"""读取 Package 内 UTF-8 文本。"""
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
    u"""确认当前实现包含不能被回退的 Locator Position 契约文本。"""
    source_text = read_source(
        relative_path
    )

    for required_text in required_texts:
        if required_text in source_text:
            continue

        raise RuntimeError(
            u"{} 缺少 Locator Visual Position 契约：{}".format(
                relative_path,
                required_text
            )
        )

    return True


def run():
    u"""验证 Guide Resource → Transform → Jnt / RigModule 的当前定位链。"""
    # Face Guide 资源允许 Locator Shape 使用 localPosition 保存可视定位偏移。
    require_text(
        "resources/face/face_guide.ma",
        [
            'setAttr ".lp" -type "double3"',
        ]
    )

    # 当前 Transform Core 必须识别 Locator，并读取 Shape.worldPosition。
    require_text(
        "core/common/transform_utils.py",
        [
            'type="locator"',
            '".worldPosition[0]"',
            "cmds.xform(str(self.object), worldSpace=True, translation=world_position)",
        ]
    )

    # Jnt Primitive 必须继续通过 Transform.match_transform 读取 Guide 位置。
    require_text(
        "core/rigging/jnt_utils.py",
        [
            "transform_utils.Transform(self.jnt)",
            "jnt_object.match_transform(target",
        ]
    )

    # RigModule 的 Joint / Controller 创建入口必须继续把 Guide 传给 Core Primitive。
    require_text(
        "systems/rig_module.py",
        [
            "jnt_object.set_match_transform(guide)",
            "match_transform_target=guide",
        ]
    )

    # 当前 Face Eye Module 仍必须明确从语义 Guide 创建 Ball Joint 与 Iris / Aim Ctrl。
    require_text(
        "systems/face/eye_module.py",
        [
            'guide=self.guide_map["ball"]',
            'guide=self.guide_map["iris"]',
            'guide=self.guide_map["aim"]',
        ]
    )

    print(
        "[PASS] Current Locator Shape worldPosition -> Transform/Jnt/RigModule contract 完整。"
    )
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
