# coding=utf-8
u"""
README / Navigation Consistency Test
====================================

确保仓库 README 的文档入口与 MkDocs 用户手册导航保持一致。

本测试在 API Generator 与 extend_docs_summary.py 之后执行。
"""

from __future__ import print_function

import os


MANUAL_PAGES = [
    ("MuziTools 用户手册", "docs/manual/index.md", "manual/index.md"),
    ("常用工具工作流", "docs/manual/tools.md", "manual/tools.md"),
    ("基础工具", "docs/manual/basic-tools.md", "manual/basic-tools.md"),
    ("Controller", "docs/manual/controller.md", "manual/controller.md"),
    (__MUZI_MAYA_JNT_PROTECTED_00000__, "docs/manual/jnt.md", "manual/jnt.md"),
    ("Skin", "docs/manual/skin.md", "manual/skin.md"),
    ("BlendShape", "docs/manual/blendshape.md", "manual/blendshape.md"),
    ("场景清理与模型检查", "docs/manual/cleanup.md", "manual/cleanup.md"),
    ("完整绑定工作流", "docs/manual/rigging.md", "manual/rigging.md"),
    ("Face Guide", "docs/manual/face-guide.md", "manual/face-guide.md"),
]

TOP_LEVEL_DOCS = [
    "docs/getting-started/installation.md",
    "docs/getting-started/maya-usage.md",
    "docs/architecture/index.md",
    "docs/reference/index.md",
    "docs/development/documentation.md",
    "docs/migration/pipeline.md",
]


# =============================================================================
# Helper
# =============================================================================

def get_project_root():
    u"""返回仓库根目录。"""
    tests_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(
        tests_directory
    )


def read_text(file_path):
    u"""读取 UTF-8 文本文件。"""
    with open(
            file_path,
            "r",
            encoding="utf-8"
    ) as file_object:
        return file_object.read()


# =============================================================================
# Test
# =============================================================================

def run_test():
    u"""检查 README 和 SUMMARY 的文档入口是否一致。"""
    project_root = get_project_root()

    readme_path = os.path.join(
        project_root,
        "README.md"
    )
    summary_path = os.path.join(
        project_root,
        "docs",
        "SUMMARY.md"
    )

    if not os.path.isfile(summary_path):
        raise AssertionError(
            u"没有找到 docs/SUMMARY.md，请先生成网站导航。"
        )

    readme_text = read_text(
        readme_path
    )
    summary_text = read_text(
        summary_path
    )

    errors = []

    for label, readme_link, summary_link in MANUAL_PAGES:
        if readme_link not in readme_text:
            errors.append(
                u"README 缺少 {}: {}".format(
                    label,
                    readme_link
                )
            )

        if summary_link not in summary_text:
            errors.append(
                u"SUMMARY 缺少 {}: {}".format(
                    label,
                    summary_link
                )
            )

    for readme_link in TOP_LEVEL_DOCS:
        if readme_link in readme_text:
            continue

        errors.append(
            u"README 缺少顶层文档入口: {}".format(
                readme_link
            )
        )

    required_readme_sections = [
        "# 快速开始",
        "# 文档导航",
        "## 1. 用户手册",
        "## 2. 架构",
        "## 3. API Reference",
        "## 4. 开发指南",
        "## 5. 迁移记录",
    ]

    previous_index = -1

    for section in required_readme_sections:
        section_index = readme_text.find(
            section
        )

        if section_index < 0:
            errors.append(
                u"README 缺少章节: {}".format(section)
            )
            continue

        if section_index <= previous_index:
            errors.append(
                u"README 章节顺序异常: {}".format(section)
            )

        previous_index = section_index

    if errors:
        print(u"README / Navigation errors:")

        for error in errors:
            print(
                u"  - {}".format(error)
            )

        raise AssertionError(
            u"README 与网站导航不一致。"
        )

    print(u"README / MkDocs navigation: PASS")
    return True


if __name__ == "__main__":
    run_test()
