# coding=utf-8
u"""
Face Module Legacy Gate Test
============================

纯 Python 静态门禁，不需要 Autodesk Maya。

目标：
    1. 当前开发分支只维护新的 systems.face.modules；
    2. 2026-08-29 的旧 Bind / Face Subject 允许保存在 legacy_reference 作为历史参考；
    3. 正式 Face Module 不允许重新 import legacy_reference；
    4. 每一个已经迁移的 Face 部位都必须存在独立 Module 文件；
    5. 旧 Face Bind 关键文件必须继续保留，避免参考快照被误删。
"""

from __future__ import print_function

import os


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FACE_MODULE_DIR = os.path.join(
    REPO_ROOT,
    "systems",
    "face",
    "modules"
)

LEGACY_FACE_DIR = os.path.join(
    REPO_ROOT,
    "legacy_reference",
    "bind",
    "subject",
    "face_subject"
)

REQUIRED_MODULE_FILES = [
    "face_module_base.py",
    "face_rig.py",
    "brow.py",
    "cheek.py",
    "ear.py",
    "eye.py",
    "eyelid.py",
    "jaw.py",
    "lip.py",
    "mouth.py",
    "nose.py",
    "teeth.py",
    "tongue.py",
]

LEGACY_REFERENCE_FILES = [
    "brow.py",
    "cheek.py",
    "ear.py",
    "eye.py",
    "eyeLid.py",
    "face_rig.py",
    "jaw.py",
    "mouth.py",
    "mouthLip.py",
    "nose.py",
    "tongue.py",
]


def test_legacy_face_reference_exists():
    u"""确认 2026-08-29 旧 Face Bind 参考快照仍然完整保留。"""
    if not os.path.isdir(LEGACY_FACE_DIR):
        raise AssertionError(
            u"缺少旧 Face Bind 参考目录：{}".format(
                LEGACY_FACE_DIR
            )
        )

    missing_files = []

    for file_name in LEGACY_REFERENCE_FILES:
        file_path = os.path.join(
            LEGACY_FACE_DIR,
            file_name
        )

        if os.path.isfile(file_path):
            continue

        missing_files.append(
            file_name
        )

    if missing_files:
        raise AssertionError(
            u"旧 Face Bind 参考文件缺失：{}".format(
                ", ".join(missing_files)
            )
        )


def test_required_face_modules_exist():
    u"""确认所有已迁移 Face 部位仍有独立正式 Module 文件。"""
    missing_files = []

    for file_name in REQUIRED_MODULE_FILES:
        file_path = os.path.join(
            FACE_MODULE_DIR,
            file_name
        )

        if os.path.isfile(file_path):
            continue

        missing_files.append(
            file_name
        )

    if missing_files:
        raise AssertionError(
            u"正式 Face Module 文件缺失：{}".format(
                ", ".join(missing_files)
            )
        )


def test_no_legacy_imports_in_face_modules():
    u"""确认正式 Face Module 不再依赖 legacy_reference。"""
    invalid_files = []

    for file_name in REQUIRED_MODULE_FILES:
        file_path = os.path.join(
            FACE_MODULE_DIR,
            file_name
        )

        with open(file_path, "r", encoding="utf-8") as file_object:
            source = file_object.read()

        if "legacy_reference" not in source:
            continue

        # 模块说明允许提到旧算法来源，但真正 import / from 不允许。
        source_lines = source.splitlines()

        for source_line in source_lines:
            stripped_line = source_line.strip()

            if not stripped_line.startswith(("import ", "from ")):
                continue

            if "legacy_reference" not in stripped_line:
                continue

            invalid_files.append(
                file_name
            )
            break

    if invalid_files:
        raise AssertionError(
            u"正式 Face Module 仍导入 Legacy 代码：{}".format(
                ", ".join(invalid_files)
            )
        )


def main():
    u"""执行 Face Legacy 参考与正式 Runtime 隔离门禁。"""
    test_legacy_face_reference_exists()
    test_required_face_modules_exist()
    test_no_legacy_imports_in_face_modules()

    print(
        u"Face Module Legacy Reference Gate: PASS"
    )


if __name__ == "__main__":
    main()
