# coding=utf-8
u"""
一次性 Face Module 迁移收尾脚本。

职责：
    1. 清理 Jaw / Teeth 中残留的旧生命周期文案；
    2. 把 Face Legacy Gate 接入长期 Static Contract；
    3. 删除当前开发分支中的旧 Face Bind 实现；
    4. 不触碰 pymel-archive 历史分支。

本脚本只用于本次迁移，成功后由 Workflow 自删除。
"""

from __future__ import print_function

import os
import shutil


REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


OLD_LIFECYCLE_BLOCK = u"""    setup
        ↓
    guide
        ↓
    joint
        ↓
    control
        ↓
    connect
        ↓
    deform
        ↓
    finalize"""

NEW_LIFECYCLE_BLOCK = u"""    load_setup()
        ↓
    load_guide()
        ↓
    create_jnt()
        ↓
    create_ctrl()
        ↓
    create_connect()
        ↓
    create_deform()
        ↓
    create_finalize()
        ↓
    create_build()"""

SECTION_REPLACEMENTS = [
    ("# 01. Setup", "# 01. Load Setup"),
    ("# 02. Guide", "# 02. Load Guide"),
    ("# 03. Joint", "# 03. Create Jnt"),
    ("# 04. Control", "# 04. Create Ctrl"),
    ("# 05. Connect", "# 05. Create Connect"),
    ("# 06. Deform", "# 06. Create Deform"),
    ("# 07. Finalize", "# 07. Create Finalize"),
]


def read_text(relative_path):
    u"""读取仓库内 UTF-8 文本。"""
    file_path = os.path.join(
        REPO_ROOT,
        relative_path
    )

    with open(file_path, "r", encoding="utf-8") as file_object:
        return file_object.read()


def write_text(relative_path, content):
    u"""覆盖写回仓库内 UTF-8 文本。"""
    file_path = os.path.join(
        REPO_ROOT,
        relative_path
    )

    with open(file_path, "w", encoding="utf-8", newline="\n") as file_object:
        file_object.write(content)


def normalize_module_lifecycle_text(relative_path):
    u"""把一个正式 Face Module 的旧生命周期文案改成最终 API。"""
    source = read_text(relative_path)
    updated_source = source.replace(
        OLD_LIFECYCLE_BLOCK,
        NEW_LIFECYCLE_BLOCK
    )

    for old_text, new_text in SECTION_REPLACEMENTS:
        updated_source = updated_source.replace(
            old_text,
            new_text
        )

    if updated_source != source:
        write_text(
            relative_path,
            updated_source
        )


def update_static_contract_workflow():
    u"""把 Legacy Removal Gate 接入长期 Static Contract。"""
    workflow_path = ".github/workflows/static_contract_tests.yml"
    source = read_text(workflow_path)

    test_line = "        run: python tests/face_module_legacy_gate_test.py"

    if test_line in source:
        return

    anchor = u"""      - name: Test Face module lifecycle contract
        run: python tests/face_module_lifecycle_contract_test.py
"""

    replacement = anchor + u"""
      - name: Test Face legacy removal gate
        run: python tests/face_module_legacy_gate_test.py
"""

    if anchor not in source:
        raise RuntimeError(
            u"Static Contract Workflow 中没有找到 Face Lifecycle 插入位置。"
        )

    source = source.replace(
        anchor,
        replacement,
        1
    )
    write_text(
        workflow_path,
        source
    )


def remove_legacy_face_modules():
    u"""删除已经迁移完成的旧 Face Bind 目录。"""
    legacy_face_path = os.path.join(
        REPO_ROOT,
        "legacy_reference",
        "bind",
        "subject",
        "face_subject"
    )

    if not os.path.isdir(legacy_face_path):
        return

    shutil.rmtree(
        legacy_face_path
    )


def main():
    u"""执行本次 Face Module 迁移的最终源码清理。"""
    module_files = [
        "systems/face/modules/jaw.py",
        "systems/face/modules/teeth.py",
    ]

    for module_file in module_files:
        normalize_module_lifecycle_text(
            module_file
        )

    update_static_contract_workflow()
    remove_legacy_face_modules()

    print(
        u"Face Module migration finalizer: DONE"
    )


if __name__ == "__main__":
    main()
