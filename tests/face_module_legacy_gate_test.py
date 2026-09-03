# coding=utf-8
u"""
Face Module Legacy Gate Test
============================

纯 Python 静态门禁，不需要 Autodesk Maya。

目标：
    1. 当前开发分支只维护新的 systems.face.modules；
    2. 旧 legacy_reference/bind/subject/face_subject 不允许重新出现；
    3. 正式 Face Module 不允许重新 import legacy_reference；
    4. 每一个已经迁移的 Face 部位都必须存在独立 Module 文件。
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


def test_legacy_face_directory_removed():
    u"""确认旧 Face Bind 源码已经从当前开发分支移除。"""
    if os.path.exists(LEGACY_FACE_DIR):
        raise AssertionError(
            u"旧 Face Bind 目录仍然存在：{}".format(
                LEGACY_FACE_DIR
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
    u"""执行 Face Legacy 移除门禁。"""
    test_legacy_face_directory_removed()
    test_required_face_modules_exist()
    test_no_legacy_imports_in_face_modules()

    print(
        u"Face Module Legacy Gate: PASS"
    )


if __name__ == "__main__":
    main()
