# coding=utf-8
u"""
Runtime Generic Documentation Refiner
=====================================

只处理第一轮自动 Docstring 生成后仍然存在的“通用占位说明”。

本脚本与 ``refine_runtime_docstring_semantics.py`` 分工明确：
    - ``refine_runtime_docstring_semantics.py`` 负责 Args 参数的 Maya / Rigging 语义；
    - 本脚本负责 Summary 和 Returns 的通用占位文本。

安全原则：
    1. 只替换明确识别到的自动占位句；
    2. 人工写过的 Summary / Returns 一个字都不改；
    3. 不修改 Function Body、参数列表、Import 或任何 Maya 业务逻辑；
    4. 写入后必须通过 Runtime Docstring Gate 和 Python Compile。

使用：
    python scripts/refine_runtime_generic_docs.py --check
    python scripts/refine_runtime_generic_docs.py --write
"""

from __future__ import print_function

import argparse
import ast
import os
import re
import sys


SOURCE_ROOTS = [
    "app",
    "core",
    "systems",
    "tools",
    "ui",
]

ROOT_MODULE_FILES = [
    "__init__.py",
    "config.py",
]

GENERIC_RETURN_DESCRIPTION = u"方法执行后的结果数据。"
GENERIC_SUMMARY_PATTERN = re.compile(
    r"^执行 `([^`]+)` 对应的 Maya 工具操作。$"
)


# =============================================================================
# Project / File Discovery
# =============================================================================

def get_project_root():
    u"""
    返回 MuziTools 仓库根目录。

    Returns:
        str:
            当前脚本所在仓库的绝对根目录。
    """
    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )
    return os.path.dirname(
        script_directory
    )


def iter_runtime_source_files(project_root):
    u"""
    返回正式 Runtime Python 文件。

    Args:
        project_root (str):
            MuziTools 仓库绝对根目录。

    Returns:
        list[str]:
            按路径排序后的 Runtime Python 文件列表。
    """
    source_files = []

    # -------------------------------------------------------------------------
    # Step 01：遍历正式 Runtime 分层目录
    # -------------------------------------------------------------------------
    for root_name in SOURCE_ROOTS:
        source_root = os.path.join(
            project_root,
            root_name
        )

        if not os.path.isdir(source_root):
            continue

        for current_root, directory_names, file_names in os.walk(source_root):
            if "__pycache__" in directory_names:
                directory_names.remove(
                    "__pycache__"
                )

            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                if file_name.startswith("_") and file_name != "__init__.py":
                    continue

                source_files.append(
                    os.path.join(
                        current_root,
                        file_name
                    )
                )

    # -------------------------------------------------------------------------
    # Step 02：补充仓库根目录公开 Runtime Module
    # -------------------------------------------------------------------------
    for file_name in ROOT_MODULE_FILES:
        source_path = os.path.join(
            project_root,
            file_name
        )

        if os.path.isfile(source_path):
            source_files.append(
                source_path
            )

    source_files.sort()
    return source_files


# =============================================================================
# Callable Discovery
# =============================================================================

def collect_public_callables(module_tree):
    u"""
    收集公开顶层 Function 和 Class Method。

    Args:
        module_tree (ast.Module):
            当前 Python 文件的 AST Module。

    Returns:
        list[ast.FunctionDef | ast.AsyncFunctionDef]:
            按源码顺序返回的公开 Callable。
    """
    callables = []

    # -------------------------------------------------------------------------
    # Step 01：收集模块顶层公开 Function
    # -------------------------------------------------------------------------
    for node in module_tree.body:
        if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            if node.name == "__init__" or not node.name.startswith("_"):
                callables.append(
                    node
                )
            continue

        if not isinstance(node, ast.ClassDef):
            continue

        if node.name.startswith("_"):
            continue

        # ---------------------------------------------------------------------
        # Step 02：收集公开 Class Method，包括 __init__
        # ---------------------------------------------------------------------
        for child_node in node.body:
            if not isinstance(
                    child_node,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                continue

            if child_node.name != "__init__" and child_node.name.startswith("_"):
                continue

            callables.append(
                child_node
            )

    return callables


def get_docstring_statement(function_node):
    u"""
    返回 Callable 当前 Docstring AST Statement。

    Args:
        function_node (ast.FunctionDef | ast.AsyncFunctionDef):
            当前公开 Callable。

    Returns:
        ast.Expr | None:
            Docstring Expr；没有 Docstring 时返回 None。
    """
    if not function_node.body:
        return None

    first_statement = function_node.body[0]

    if not isinstance(first_statement, ast.Expr):
        return None

    value_node = first_statement.value

    if isinstance(value_node, ast.Constant):
        if isinstance(value_node.value, str):
            return first_statement

    return None


# =============================================================================
# Summary Semantics
# =============================================================================

def infer_summary(function_name):
    u"""
    根据高频 API 命名生成比自动占位句更明确的中文 Summary。

    Args:
        function_name (str):
            当前公开 Function / Method 名称。

    Returns:
        str:
            推断得到的中文功能摘要。
    """
    # -------------------------------------------------------------------------
    # Step 01：先处理 UI / Runtime 中高频且语义固定的方法名称
    # -------------------------------------------------------------------------
    exact_rules = {
        "__init__": u"初始化当前对象，并准备运行时需要的状态和成员。",
        "main": u"执行当前模块的公开入口，并显示或运行对应工具。",
        "run": u"执行当前模块定义的主要工作流。",
        "create_widgets": u"创建当前工具窗口需要的 Qt 控件。",
        "create_layouts": u"创建并组织当前工具窗口的 Qt Layout。",
        "create_connections": u"连接当前工具窗口的 Qt Signal / Slot。",
        "refresh_ui": u"根据当前数据状态刷新工具界面。",
        "refresh": u"重新读取当前状态并刷新缓存或界面结果。",
        "show": u"显示并返回当前工具或窗口。",
    }

    if function_name in exact_rules:
        return exact_rules[function_name]

    # -------------------------------------------------------------------------
    # Step 02：按常见 API Verb 推断动作类型
    # -------------------------------------------------------------------------
    prefix_rules = [
        ("get_", u"查询并返回当前 {}。"),
        ("find_", u"查找并返回当前 {}。"),
        ("list_", u"列出并返回当前 {}。"),
        ("collect_", u"收集并返回当前 {}。"),
        ("create_", u"创建当前 {}。"),
        ("build_", u"构建当前 {}。"),
        ("set_", u"设置当前 {}。"),
        ("apply_", u"应用当前 {}。"),
        ("update_", u"更新当前 {}。"),
        ("reset_", u"重置当前 {}。"),
        ("delete_", u"删除当前 {}。"),
        ("remove_", u"移除当前 {}。"),
        ("clear_", u"清理当前 {}。"),
        ("load_", u"加载当前 {}。"),
        ("save_", u"保存当前 {}。"),
        ("export_", u"导出当前 {}。"),
        ("import_", u"导入当前 {}。"),
        ("validate_", u"验证当前 {} 是否满足要求。"),
        ("is_", u"判断当前 {} 状态。"),
        ("has_", u"判断当前是否存在 {}。"),
        ("open_", u"打开当前 {}。"),
        ("close_", u"关闭当前 {}。"),
        ("select_", u"选择当前 {}。"),
        ("mirror_", u"镜像当前 {}。"),
    ]

    for prefix, template in prefix_rules:
        if not function_name.startswith(prefix):
            continue

        subject = function_name[len(prefix):]
        subject = subject.replace(
            "_",
            " "
        )

        return template.format(
            subject
        )

    # -------------------------------------------------------------------------
    # Step 03：没有稳定 Verb 语义时使用中性的 API 流程说明
    # -------------------------------------------------------------------------
    return u"执行当前 API 的主要处理流程。"


# =============================================================================
# Return Semantics
# =============================================================================

def infer_return_description(function_name, return_type):
    u"""
    根据函数名称和 Returns 类型生成中文结果说明。

    Args:
        function_name (str):
            当前公开 Function / Method 名称。
        return_type (str):
            Docstring ``Returns`` 中已经存在的类型文本。

    Returns:
        str:
            用于替换自动 ``方法执行后的结果数据。`` 的中文说明。
    """
    lower_type = return_type.lower()

    # -------------------------------------------------------------------------
    # Step 01：优先根据明确返回类型生成稳定说明
    # -------------------------------------------------------------------------
    if "bool" in lower_type:
        if function_name.startswith("is_") or function_name.startswith("has_"):
            return u"条件成立时返回 True，否则返回 False。"

        return u"当前操作成功或目标状态满足要求时返回 True，否则返回 False。"

    if "dict" in lower_type:
        return u"包含本次构建、查询或处理结果的结构化字典。"

    if "list" in lower_type:
        return u"按当前 API 约定顺序返回的结果列表。"

    if "tuple" in lower_type:
        return u"按当前 API 约定组织的结果元组。"

    if "float" in lower_type:
        return u"当前数学、权重或空间计算得到的浮点结果。"

    if "int" in lower_type:
        if function_name.startswith("get_"):
            return u"当前查询得到的整数值。"

        return u"本次操作得到的整数结果或成功处理数量。"

    if "qtwidgets" in lower_type or "qwidget" in lower_type or "qdialog" in lower_type:
        return u"创建、显示或处理后的 Qt Widget / Dialog 对象。"

    if "str" in lower_type:
        if "path" in function_name:
            return u"规范化、查询或生成后的路径字符串。"

        if "name" in function_name:
            return u"当前查询、生成或处理后的名称字符串。"

        return u"当前 API 查询或处理后得到的字符串结果。"

    # -------------------------------------------------------------------------
    # Step 02：类型过于宽泛时再根据函数动作推断结果语义
    # -------------------------------------------------------------------------
    if function_name.startswith("create_") or function_name.startswith("build_"):
        return u"创建或构建完成后的 Maya / Rig 对象或 Build Result。"

    if function_name.startswith("get_") or function_name.startswith("find_"):
        return u"当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。"

    if function_name.startswith("set_") or function_name.startswith("apply_"):
        return u"完成设置或应用后的目标对象 / 状态结果。"

    if function_name in ["main", "show"]:
        return u"当前工具入口创建并显示的窗口或执行结果。"

    return u"当前 API 完成处理后返回的结果。"


# =============================================================================
# Docstring Rewrite
# =============================================================================

def refine_docstring(function_node):
    u"""
    只替换一个 Callable Docstring 中的自动 Summary / Returns 占位句。

    Args:
        function_node (ast.FunctionDef | ast.AsyncFunctionDef):
            当前公开 Callable。

    Returns:
        tuple[str, bool]:
            新 Docstring 文本和是否发生变化。
    """
    docstring = ast.get_docstring(
        function_node,
        clean=False
    )

    if not docstring:
        return "", False

    lines = docstring.expandtabs(4).splitlines()
    changed = False

    # -------------------------------------------------------------------------
    # Step 01：只在第一条有效 Summary 是自动占位句时替换 Summary
    # -------------------------------------------------------------------------
    first_content_index = None
    line_index = 0

    while line_index < len(lines):
        if lines[line_index].strip():
            first_content_index = line_index
            break

        line_index += 1

    if first_content_index is not None:
        summary_text = lines[first_content_index].strip()
        summary_match = GENERIC_SUMMARY_PATTERN.match(
            summary_text
        )

        if summary_match:
            indent = lines[first_content_index][
                :len(lines[first_content_index]) - len(lines[first_content_index].lstrip())
            ]
            lines[first_content_index] = indent + infer_summary(
                function_node.name
            )
            changed = True

    # -------------------------------------------------------------------------
    # Step 02：找到 Returns Section，并取得其中第一条返回类型
    # -------------------------------------------------------------------------
    returns_index = None
    return_type = "object"
    line_index = 0

    while line_index < len(lines):
        if lines[line_index].strip() == "Returns:":
            returns_index = line_index
            break

        line_index += 1

    if returns_index is not None:
        type_index = returns_index + 1

        while type_index < len(lines):
            stripped_line = lines[type_index].strip()

            if not stripped_line:
                type_index += 1
                continue

            if stripped_line.endswith(":"):
                return_type = stripped_line[:-1].strip()
            break

        # ---------------------------------------------------------------------
        # Step 03：仅替换 Returns 内精确匹配的自动通用结果说明
        # ---------------------------------------------------------------------
        description_index = type_index + 1

        while description_index < len(lines):
            stripped_description = lines[description_index].strip()

            if not stripped_description:
                description_index += 1
                continue

            if stripped_description == GENERIC_RETURN_DESCRIPTION:
                indent = lines[description_index][
                    :len(lines[description_index]) - len(lines[description_index].lstrip())
                ]
                lines[description_index] = indent + infer_return_description(
                    function_node.name,
                    return_type
                )
                changed = True
            break

    return "\n".join(lines), changed


def build_docstring_source(docstring, indent):
    u"""
    把 Docstring 文本转换成保持当前函数缩进的源码行。

    Args:
        docstring (str):
            已经精修完成的 Docstring 内容。
        indent (str):
            Function Body 使用的源码缩进。

    Returns:
        list[str]:
            可直接替换原 Docstring Expr 的源码行。
    """
    lines = [
        indent + 'u"""'
    ]

    for doc_line in docstring.splitlines():
        if doc_line:
            lines.append(
                indent + doc_line
            )
        else:
            lines.append("")

    lines.append(
        indent + '"""'
    )
    return lines


def refine_source_text(source_text, source_path):
    u"""
    精修一个 Runtime Python 文件的通用 Summary / Returns 占位说明。

    Args:
        source_text (str):
            当前 Runtime Python 完整源码。
        source_path (str):
            当前源码路径，仅用于 AST 错误上下文。

    Returns:
        tuple[str, int]:
            精修后的完整源码和发生变化的 Callable 数量。
    """
    module_tree = ast.parse(
        source_text,
        filename=source_path
    )
    source_lines = source_text.splitlines()
    had_final_newline = source_text.endswith("\n")
    replacement_records = []
    changed_count = 0

    # -------------------------------------------------------------------------
    # Step 01：逐个分析公开 Callable，只记录确实存在自动占位句的 Docstring
    # -------------------------------------------------------------------------
    public_callables = collect_public_callables(
        module_tree
    )

    for function_node in public_callables:
        docstring_statement = get_docstring_statement(
            function_node
        )

        if docstring_statement is None:
            continue

        refined_docstring, changed = refine_docstring(
            function_node
        )

        if not changed:
            continue

        indent = " " * docstring_statement.col_offset
        replacement_records.append({
            "start_index": docstring_statement.lineno - 1,
            "end_index": docstring_statement.end_lineno,
            "lines": build_docstring_source(
                refined_docstring,
                indent
            ),
        })
        changed_count += 1

    # -------------------------------------------------------------------------
    # Step 02：从文件底部向上替换，避免前面的 AST 行号发生偏移
    # -------------------------------------------------------------------------
    replacement_records.sort(
        key=lambda record: record["start_index"],
        reverse=True
    )

    for record in replacement_records:
        source_lines[
            record["start_index"]:record["end_index"]
        ] = record["lines"]

    refined_text = "\n".join(
        source_lines
    )

    if had_final_newline:
        refined_text += "\n"

    return refined_text, changed_count


# =============================================================================
# Repository Runner
# =============================================================================

def process_repository(write=False):
    u"""
    检查或写入全部 Runtime 的通用 Summary / Returns 占位说明。

    Args:
        write (bool):
            True 时写回源码；False 时只统计待精修项。

    Returns:
        dict:
            Runtime 文件数量、待精修 Callable 数量和变化文件列表。
    """
    project_root = get_project_root()
    source_files = iter_runtime_source_files(
        project_root
    )
    changed_files = []
    callable_count = 0

    # -------------------------------------------------------------------------
    # Step 01：逐文件生成只包含 Docstring 变化的新源码
    # -------------------------------------------------------------------------
    for source_path in source_files:
        with open(
                source_path,
                "r",
                encoding="utf-8"
        ) as source_file:
            source_text = source_file.read()

        new_source_text, changed_count = refine_source_text(
            source_text,
            source_path
        )
        callable_count += changed_count

        if new_source_text == source_text:
            continue

        relative_path = os.path.relpath(
            source_path,
            project_root
        ).replace(
            os.sep,
            "/"
        )
        changed_files.append(
            relative_path
        )

        # ---------------------------------------------------------------------
        # Step 02：Write 模式才真正覆盖 Runtime 文件
        # ---------------------------------------------------------------------
        if write:
            with open(
                    source_path,
                    "w",
                    encoding="utf-8",
                    newline="\n"
            ) as source_file:
                source_file.write(
                    new_source_text
                )

    return {
        "file_count": len(source_files),
        "callable_count": callable_count,
        "changed_files": changed_files,
    }


def main():
    u"""
    命令行入口。

    Returns:
        bool:
            Check / Write 操作满足要求时返回 True。
    """
    parser = argparse.ArgumentParser(
        description="Refine generic Runtime Summary and Returns descriptions."
    )
    mode_group = parser.add_mutually_exclusive_group(
        required=True
    )
    mode_group.add_argument(
        "--check",
        action="store_true",
        help="Report generic Summary / Returns placeholders without writing."
    )
    mode_group.add_argument(
        "--write",
        action="store_true",
        help="Replace only generic Summary / Returns placeholders."
    )
    arguments = parser.parse_args()

    # -------------------------------------------------------------------------
    # Step 01：执行全仓通用文档精修
    # -------------------------------------------------------------------------
    result = process_repository(
        write=arguments.write
    )

    print("=" * 78)
    print("Runtime Generic Documentation Refiner")
    print("=" * 78)
    print(
        "Runtime files:       {}".format(
            result["file_count"]
        )
    )
    print(
        "Callables pending:   {}".format(
            result["callable_count"]
        )
    )
    print(
        "Changed files:       {}".format(
            len(result["changed_files"])
        )
    )

    # -------------------------------------------------------------------------
    # Step 02：Check 模式发现自动占位句时返回失败码，供 CI 长期阻止回退
    # -------------------------------------------------------------------------
    if arguments.check:
        if result["callable_count"] > 0:
            print("Status:              NEEDS REFINEMENT")
            return False

    print("Status:              PASS")
    return True


if __name__ == "__main__":
    success = main()

    if not success:
        sys.exit(1)
