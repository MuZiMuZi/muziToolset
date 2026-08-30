# coding=utf-8
u"""
Generated API Reference Refiner
===============================

对 AST Generator 生成的 API Reference 做第二阶段阅读体验整理。

当前负责：
    1. 所有模块“概览”只保留简短用途说明；
    2. 概览固定分成“用途”和“模块定位”两段；
    3. 不把完整 Module Docstring 正文直接铺在页面顶部；
    4. 保持详细 API、参数表、返回值、异常和示例不变。

使用顺序：
    python scripts/generate_mkdocs_reference.py
    python scripts/refine_generated_reference.py
"""

from __future__ import print_function

import ast
import importlib.util
import os
import re


MAX_SUMMARY_LENGTH = 140


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


def load_reference_generator(project_root):
    u"""静态加载 API Reference Generator。"""
    generator_path = os.path.join(
        project_root,
        "scripts",
        "generate_mkdocs_reference.py"
    )

    spec = importlib.util.spec_from_file_location(
        "muzi_reference_refiner_generator",
        generator_path
    )

    if spec is None:
        raise RuntimeError(
            u"无法创建 API Reference Generator Import Spec。"
        )

    if spec.loader is None:
        raise RuntimeError(
            u"无法读取 API Reference Generator Loader。"
        )

    module = importlib.util.module_from_spec(
        spec
    )
    spec.loader.exec_module(
        module
    )
    return module


# =============================================================================
# Summary
# =============================================================================

def is_underline_heading(line):
    u"""判断一行是否是 ReStructuredText 风格标题下划线。"""
    stripped_line = line.strip()

    if not stripped_line:
        return False

    characters = set(stripped_line)

    if characters == set("="):
        return True

    if characters == set("-"):
        return True

    return False


def get_docstring_paragraphs(docstring):
    u"""把 Module Docstring 整理成可用于摘要选择的自然段。"""
    if not docstring:
        return []

    raw_lines = docstring.expandtabs(4).strip().splitlines()
    clean_lines = []
    line_index = 0

    while line_index < len(raw_lines):
        line = raw_lines[line_index]
        stripped_line = line.strip()

        next_line = ""

        if line_index + 1 < len(raw_lines):
            next_line = raw_lines[line_index + 1]

        # 跳过：
        #   Animation Utils
        #   ===============
        if stripped_line and is_underline_heading(next_line):
            line_index += 2
            continue

        if is_underline_heading(line):
            line_index += 1
            continue

        clean_lines.append(
            line.rstrip()
        )
        line_index += 1

    paragraphs = []
    current_lines = []

    for line in clean_lines:
        stripped_line = line.strip()

        if not stripped_line:
            if current_lines:
                paragraphs.append(
                    " ".join(current_lines).strip()
                )
                current_lines = []
            continue

        current_lines.append(
            stripped_line
        )

    if current_lines:
        paragraphs.append(
            " ".join(current_lines).strip()
        )

    return paragraphs


def looks_like_section_title(paragraph):
    u"""判断自然段是否更像模块章节标题，而不是用途摘要。"""
    section_titles = [
        "模块职责",
        "当前公开方法",
        "公开类",
        "主要公开方法",
        "兼容辅助方法",
        "数据流",
        "本模块不负责",
        "设计原则",
        "正式模块路径",
        "兼容",
        "说明",
        "功能",
        "使用场景",
        "职责",
        "边界",
    ]

    normalized = paragraph.strip().rstrip(":：")

    if normalized in section_titles:
        return True

    if len(normalized) <= 18:
        for title in section_titles:
            if title in normalized:
                return True

    return False


def trim_summary(summary):
    u"""把摘要控制在两句话和合理字符长度内。"""
    summary = " ".join(
        summary.split()
    ).strip()

    if not summary:
        return summary

    sentence_parts = re.split(
        r"(?<=[。！？.!?])\s*",
        summary
    )

    selected_sentences = []

    for sentence in sentence_parts:
        sentence = sentence.strip()

        if not sentence:
            continue

        selected_sentences.append(
            sentence
        )

        if len(selected_sentences) >= 2:
            break

    if selected_sentences:
        summary = " ".join(
            selected_sentences
        )

    if len(summary) > MAX_SUMMARY_LENGTH:
        summary = summary[:MAX_SUMMARY_LENGTH - 3].rstrip()
        summary += "..."

    return summary


def build_concise_summary(module_info):
    u"""从 Module Docstring 中选择最适合页面顶部的简短用途说明。"""
    source_path = module_info[
        "source_path"
    ]

    with open(
            source_path,
            "r",
            encoding="utf-8"
    ) as file_object:
        source_text = file_object.read()

    module_tree = ast.parse(
        source_text,
        filename=source_path
    )
    module_docstring = ast.get_docstring(
        module_tree
    ) or ""

    paragraphs = get_docstring_paragraphs(
        module_docstring
    )

    for paragraph in paragraphs:
        if looks_like_section_title(paragraph):
            continue

        # 跳过只包含 import path / code 标记的短段。
        if paragraph.startswith("``"):
            continue

        summary = trim_summary(
            paragraph
        )

        if summary:
            return summary

    return u"提供 `{}` 模块对应的 Maya 工具能力。".format(
        module_info["module_name"]
    )


def build_module_position(module_info):
    u"""根据源码目录生成一行清晰的模块定位说明。"""
    root_name = module_info[
        "root_name"
    ]

    position_map = {
        "core": u"Core 底层公共能力；不负责 UI 和完整 Rig Workflow。",
        "systems": u"System 业务构建层；负责可重复构建的完整 Rig 组件或流程。",
        "tools": u"Tool 用户操作层；负责 UI、Selection 和调用底层能力。",
        "ui": u"UI 公共层；负责可复用界面组件，不承载 Rig 算法。",
        "app": u"应用入口层；负责主工具箱、窗口生命周期和工具调度。",
        "package": u"MuziTools 包级入口或全局配置模块。",
    }

    return position_map.get(
        root_name,
        u"MuziTools 正式运行时模块。"
    )


# =============================================================================
# Markdown
# =============================================================================

def replace_overview(markdown_text, summary, position):
    u"""替换生成页面中的“概览”区域。"""
    start_marker = "## 概览"
    end_marker = "## 常用任务"

    start_index = markdown_text.find(
        start_marker
    )
    end_index = markdown_text.find(
        end_marker
    )

    if start_index < 0:
        return markdown_text

    if end_index < 0:
        return markdown_text

    if end_index <= start_index:
        return markdown_text

    overview_lines = [
        "## 概览",
        "",
        "**用途**",
        "",
        summary,
        "",
        "**模块定位**",
        "",
        position,
        "",
    ]

    overview_text = "\n".join(
        overview_lines
    )

    return (
        markdown_text[:start_index]
        + overview_text
        + markdown_text[end_index:]
    )


def refine_reference_docs(project_root=None):
    u"""统一整理全部自动生成 API 页面的概览。"""
    if project_root is None:
        project_root = get_project_root()

    generator = load_reference_generator(
        project_root
    )
    docs_root = os.path.join(
        project_root,
        "docs"
    )
    source_files = generator.iter_source_files(
        project_root
    )

    changed_count = 0

    for source_path in source_files:
        module_info = generator.collect_module_info(
            project_root,
            source_path
        )
        output_relative_path = generator.get_output_relative_path(
            module_info
        )
        output_path = os.path.join(
            docs_root,
            output_relative_path
        )

        if not os.path.isfile(output_path):
            continue

        with open(
                output_path,
                "r",
                encoding="utf-8"
        ) as file_object:
            markdown_text = file_object.read()

        summary = build_concise_summary(
            module_info
        )
        position = build_module_position(
            module_info
        )
        refined_text = replace_overview(
            markdown_text,
            summary,
            position
        )

        if refined_text == markdown_text:
            continue

        with open(
                output_path,
                "w",
                encoding="utf-8",
                newline="\n"
        ) as file_object:
            file_object.write(
                refined_text
            )

        changed_count += 1

    print(
        u"Refined API overview pages: {}".format(
            changed_count
        )
    )
    return changed_count


if __name__ == "__main__":
    refine_reference_docs()
