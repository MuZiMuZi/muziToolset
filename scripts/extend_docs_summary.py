# coding=utf-8
u"""
Extend MkDocs Summary
=====================

扩展 API Generator 生成的 ``docs/SUMMARY.md``。

API Generator 负责动态生成源码树导航；本脚本只负责把人工维护的用户手册任务页
插入“用户手册”区域，避免为了增加一个手册页面去修改大型 AST Generator。

职责：
    1. 读取 docs/SUMMARY.md；
    2. 找到“常用工具工作流”入口；
    3. 插入基础工具 / Controller / Joint / Skin / BlendShape / Cleanup；
    4. 重复执行时不产生重复导航项。

说明：
    - 不修改 API Reference 源码树；
    - 不 import Maya；
    - 可以在 GitHub Actions Linux Runner 中运行。
"""

from __future__ import print_function

import os


manual_navigation_lines = [
    "    * [基础工具](manual/basic-tools.md)",
    "    * [Controller](manual/controller.md)",
    "    * [Joint](manual/joint.md)",
    "    * [Skin](manual/skin.md)",
    "    * [BlendShape](manual/blendshape.md)",
    "    * [场景清理与模型检查](manual/cleanup.md)",
]

anchor_line = "    * [常用工具工作流](manual/tools.md)"


def get_project_root():
    """返回仓库根目录。"""
    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    return os.path.dirname(
        script_directory
    )


def get_summary_path(project_root):
    """返回 docs/SUMMARY.md 绝对路径。"""
    return os.path.join(
        project_root,
        "docs",
        "SUMMARY.md"
    )


def read_summary(summary_path):
    """读取 SUMMARY.md。"""
    if not os.path.isfile(summary_path):
        raise RuntimeError(
            u"没有找到 docs/SUMMARY.md，请先执行 API Reference Generator。"
        )

    with open(
            summary_path,
            "r",
            encoding="utf-8"
    ) as file_object:
        return file_object.read()


def remove_existing_manual_lines(lines):
    """删除旧任务页导航，保证脚本可以重复执行。"""
    result = []

    for line in lines:
        if line in manual_navigation_lines:
            continue

        result.append(
            line
        )

    return result


def extend_summary_content(content):
    """返回插入任务页导航后的 SUMMARY 内容。"""
    lines = content.splitlines()
    lines = remove_existing_manual_lines(
        lines
    )

    result = []
    inserted = False

    for line in lines:
        result.append(
            line
        )

        if line != anchor_line:
            continue

        for navigation_line in manual_navigation_lines:
            result.append(
                navigation_line
            )

        inserted = True

    if not inserted:
        raise RuntimeError(
            u"SUMMARY.md 中没有找到用户手册导航锚点: {}".format(
                anchor_line
            )
        )

    result.append("")

    return "\n".join(
        result
    )


def write_summary(summary_path, content):
    """写回 SUMMARY.md。"""
    with open(
            summary_path,
            "w",
            encoding="utf-8",
            newline="\n"
    ) as file_object:
        file_object.write(
            content
        )


def main():
    """扩展 docs/SUMMARY.md 用户手册导航。"""
    project_root = get_project_root()
    summary_path = get_summary_path(
        project_root
    )

    content = read_summary(
        summary_path
    )

    content = extend_summary_content(
        content
    )

    write_summary(
        summary_path,
        content
    )

    print(
        u"MuziTools 用户手册导航扩展完成: {}".format(
            summary_path
        )
    )

    return True


if __name__ == "__main__":
    main()
