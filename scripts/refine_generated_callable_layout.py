# coding=utf-8
u"""
Generated Callable Layout Refiner
=================================

让每个自动生成的 Function / Method API 在 Signature 之前先明确显示“作用”。

目标页面结构：

    ### `method()`

    **作用**

    一到两句中文功能摘要。

    **适用场景**

    ...

    **Signature**

    ...

这样绑定师扫 API 页面时，可以先理解“这个方法是干什么的”，再决定是否继续看参数。
"""

from __future__ import print_function

import argparse
import os
import re
import sys


GENERATED_MARKER = "<!-- AUTO-GENERATED: scripts/generate_mkdocs_reference.py -->"
CALLABLE_HEADING_PATTERN = re.compile(
    r"^(#{3,6})\s+`[^`]+\(\)`\s*$"
)


# =============================================================================
# Project
# =============================================================================

def get_project_root():
    u"""返回 MuziTools 仓库根目录。"""
    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(
        script_directory
    )


def iter_generated_reference_files(project_root):
    u"""扫描自动生成的 Runtime API Reference Markdown。"""
    reference_root = os.path.join(
        project_root,
        "docs",
        "reference"
    )
    markdown_files = []

    if not os.path.isdir(reference_root):
        return markdown_files

    for current_root, folder_names, file_names in os.walk(reference_root):
        for file_name in file_names:
            if not file_name.endswith(".md"):
                continue

            file_path = os.path.join(
                current_root,
                file_name
            )

            with open(
                    file_path,
                    "r",
                    encoding="utf-8"
            ) as file_object:
                prefix = file_object.read(256)

            if GENERATED_MARKER not in prefix:
                continue

            markdown_files.append(
                file_path
            )

    markdown_files.sort()
    return markdown_files


# =============================================================================
# Layout
# =============================================================================

def refine_markdown_text(markdown_text):
    u"""在每个 Function / Method 功能摘要前插入“作用”标签。"""
    lines = markdown_text.splitlines()
    result_lines = []
    changed = False
    line_index = 0

    while line_index < len(lines):
        line = lines[line_index]
        result_lines.append(
            line
        )

        if not CALLABLE_HEADING_PATTERN.match(line):
            line_index += 1
            continue

        next_index = line_index + 1

        # 保留 Heading 后已有的空行。
        while next_index < len(lines):
            if lines[next_index].strip():
                break

            result_lines.append(
                lines[next_index]
            )
            next_index += 1

        if next_index >= len(lines):
            line_index = next_index
            continue

        # 已处理过的页面保持幂等。
        if lines[next_index].strip() == "**作用**":
            line_index = next_index
            continue

        result_lines.append(
            "**作用**"
        )
        result_lines.append("")
        changed = True
        line_index = next_index

    refined_text = "\n".join(
        result_lines
    )

    if markdown_text.endswith("\n"):
        refined_text += "\n"

    return refined_text, changed


def validate_markdown_text(markdown_text, relative_path):
    u"""检查所有 Function / Method Heading 后都存在“作用”区域。"""
    errors = []
    lines = markdown_text.splitlines()

    for line_index, line in enumerate(lines):
        if not CALLABLE_HEADING_PATTERN.match(line):
            continue

        next_index = line_index + 1

        while next_index < len(lines):
            if lines[next_index].strip():
                break

            next_index += 1

        if next_index >= len(lines):
            errors.append(
                u"{}:{} 方法标题后缺少作用说明。".format(
                    relative_path,
                    line_index + 1
                )
            )
            continue

        if lines[next_index].strip() != "**作用**":
            errors.append(
                u"{}:{} 方法标题后没有固定的“作用”区域。".format(
                    relative_path,
                    line_index + 1
                )
            )

    return errors


def run(write=False):
    u"""整理或检查全部生成 API 页面。"""
    project_root = get_project_root()
    markdown_files = iter_generated_reference_files(
        project_root
    )
    changed_files = []
    errors = []

    for file_path in markdown_files:
        with open(
                file_path,
                "r",
                encoding="utf-8"
        ) as file_object:
            markdown_text = file_object.read()

        if write:
            refined_text, changed = refine_markdown_text(
                markdown_text
            )

            if changed:
                with open(
                        file_path,
                        "w",
                        encoding="utf-8",
                        newline="\n"
                ) as file_object:
                    file_object.write(
                        refined_text
                    )

                markdown_text = refined_text
                changed_files.append(
                    file_path
                )

        relative_path = os.path.relpath(
            file_path,
            project_root
        )
        file_errors = validate_markdown_text(
            markdown_text,
            relative_path
        )

        for error in file_errors:
            errors.append(
                error
            )

    print("=" * 78)
    print("Generated Callable Layout")
    print("=" * 78)
    print("Reference files: {}".format(len(markdown_files)))
    print("Changed files:   {}".format(len(changed_files)))
    print("Layout errors:   {}".format(len(errors)))

    if errors:
        for error in errors:
            print(
                "  - " + error
            )

        print("=" * 78)
        return False

    print("Status:          PASS")
    print("=" * 78)
    return True


def main():
    u"""命令行入口。"""
    parser = argparse.ArgumentParser(
        description="Highlight Function / Method purpose in generated API Reference."
    )
    mode_group = parser.add_mutually_exclusive_group(
        required=True
    )
    mode_group.add_argument(
        "--check",
        action="store_true",
        help="Validate that every callable has a purpose section."
    )
    mode_group.add_argument(
        "--write",
        action="store_true",
        help="Insert purpose labels into generated API pages."
    )

    arguments = parser.parse_args()
    success = run(
        write=arguments.write
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
