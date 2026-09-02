# coding=utf-8
u"""
Runtime Step Comment Annotator
==============================

为 MuziTools 中“流程较复杂但还没有步骤注释”的 Runtime 函数补充中文 Step 注释。

安全原则：
    1. 只插入 ``#`` 注释，不修改任何 Python 表达式、调用参数或控制流；
    2. 已经包含 ``Step 01`` 的函数完全跳过，保护人工精修结果；
    3. 只在 Function / Method 的顶层 Statement 前插入注释；
    4. 每个复杂函数最多生成 5 个主要步骤，避免注释比代码还密；
    5. 写入后必须通过 ``python -m compileall`` 才允许合并。

复杂函数阈值与 ``audit_runtime_step_comments.py`` 保持一致：
    - 源码跨度 >= 45 行；或
    - 控制流节点 >= 5；或
    - Call 节点 >= 15。

使用：
    python scripts/annotate_runtime_steps.py --check
    python scripts/annotate_runtime_steps.py --write
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

STEP_PATTERN = re.compile(
    r"#\s*-*\s*Step\s*0?1\b",
    re.IGNORECASE
)

CONTROL_FLOW_TYPES = (
    ast.If,
    ast.For,
    ast.While,
    ast.Try,
    ast.With,
)

MAX_STEPS = 5


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


def iter_runtime_python_files(project_root):
    u"""
    返回需要处理的 Runtime Python 文件。

    Args:
        project_root (str):
            MuziTools 仓库绝对根目录。

    Returns:
        list[str]:
            按路径排序后的 Runtime Python 文件列表。
    """
    source_files = []

    # -------------------------------------------------------------------------
    # Step 01：遍历项目正式 Runtime 分层目录
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

                source_files.append(
                    os.path.join(
                        current_root,
                        file_name
                    )
                )

    # -------------------------------------------------------------------------
    # Step 02：稳定排序，保证每次自动整理顺序一致
    # -------------------------------------------------------------------------
    source_files.sort()
    return source_files


# =============================================================================
# Callable Discovery / Metrics
# =============================================================================

def collect_callables(module_tree):
    u"""
    收集模块顶层 Function 和 Class Method。

    Args:
        module_tree (ast.Module):
            当前 Python 文件解析后的 AST Module。

    Returns:
        list[ast.FunctionDef | ast.AsyncFunctionDef]:
            按源码顺序收集到的函数节点。
    """
    callables = []

    # -------------------------------------------------------------------------
    # Step 01：收集模块顶层 Function
    # -------------------------------------------------------------------------
    for node in module_tree.body:
        if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            callables.append(
                node
            )
            continue

        if not isinstance(node, ast.ClassDef):
            continue

        # ---------------------------------------------------------------------
        # Step 02：收集 Class 直接定义的方法，不进入嵌套局部函数
        # ---------------------------------------------------------------------
        for child_node in node.body:
            if not isinstance(
                    child_node,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                continue

            callables.append(
                child_node
            )

    return callables


def get_callable_metrics(function_node):
    u"""
    统计函数源码跨度、控制流数量和 Call 数量。

    Args:
        function_node (ast.FunctionDef | ast.AsyncFunctionDef):
            需要统计复杂度的函数节点。

    Returns:
        dict:
            包含 ``line_span``、``control_flow`` 和 ``calls``。
    """
    end_lineno = getattr(
        function_node,
        "end_lineno",
        function_node.lineno
    )
    line_span = end_lineno - function_node.lineno + 1
    control_flow_count = 0
    call_count = 0

    # -------------------------------------------------------------------------
    # Step 01：遍历函数 AST，累计控制流与函数调用数量
    # -------------------------------------------------------------------------
    for node in ast.walk(function_node):
        if isinstance(node, CONTROL_FLOW_TYPES):
            control_flow_count += 1

        if isinstance(node, ast.Call):
            call_count += 1

    # -------------------------------------------------------------------------
    # Step 02：返回与审计脚本统一的复杂度结构
    # -------------------------------------------------------------------------
    return {
        "line_span": line_span,
        "control_flow": control_flow_count,
        "calls": call_count,
    }


def is_complex_callable(metrics):
    u"""
    判断函数是否达到步骤注释整理阈值。

    Args:
        metrics (dict):
            ``get_callable_metrics()`` 返回的复杂度统计。

    Returns:
        bool:
            达到任意复杂度阈值时返回 True。
    """
    if metrics["line_span"] >= 45:
        return True

    if metrics["control_flow"] >= 5:
        return True

    if metrics["calls"] >= 15:
        return True

    return False


def has_step_comments(source_lines, function_node):
    u"""
    判断函数源码范围内是否已经存在 ``Step 01``。

    Args:
        source_lines (list[str]):
            当前文件按行拆分后的源码。
        function_node (ast.FunctionDef | ast.AsyncFunctionDef):
            需要检查的函数节点。

    Returns:
        bool:
            已经存在步骤注释时返回 True。
    """
    start_index = function_node.lineno - 1
    end_lineno = getattr(
        function_node,
        "end_lineno",
        function_node.lineno
    )
    function_text = "\n".join(
        source_lines[start_index:end_lineno]
    )

    return STEP_PATTERN.search(
        function_text
    ) is not None


# =============================================================================
# Semantic Label Inference
# =============================================================================

def get_call_name(call_node):
    u"""
    返回 AST Call 最末级函数名称。

    Args:
        call_node (ast.Call):
            需要分析的函数调用节点。

    Returns:
        str:
            函数或方法名称；无法识别时返回空字符串。
    """
    function_node = call_node.func

    if isinstance(function_node, ast.Name):
        return function_node.id

    if isinstance(function_node, ast.Attribute):
        return function_node.attr

    return ""


def collect_statement_call_names(statement_node):
    u"""
    收集一个顶层 Statement 内调用的方法名称。

    Args:
        statement_node (ast.stmt):
            当前函数体中的顶层 Statement。

    Returns:
        list[str]:
            去重后的 Call 名称列表。
    """
    call_names = []

    for node in ast.walk(statement_node):
        if not isinstance(node, ast.Call):
            continue

        call_name = get_call_name(
            node
        )

        if not call_name:
            continue

        if call_name in call_names:
            continue

        call_names.append(
            call_name
        )

    return call_names


def contains_name_fragment(call_names, fragments):
    u"""
    判断 Call 名称中是否包含指定语义片段。

    Args:
        call_names (list[str]):
            当前 Statement 内的函数调用名称。
        fragments (list[str]):
            需要匹配的名称片段。

    Returns:
        bool:
            任意 Call 命中任意片段时返回 True。
    """
    for call_name in call_names:
        lower_name = call_name.lower()

        for fragment in fragments:
            if fragment in lower_name:
                return True

    return False


def infer_statement_label(statement_node):
    u"""
    根据顶层 Statement 的 AST 形态推断中文流程说明。

    Args:
        statement_node (ast.stmt):
            需要生成步骤标题的顶层 Statement。

    Returns:
        str:
            用于 ``Step XX`` 后面的中文说明。
    """
    call_names = collect_statement_call_names(
        statement_node
    )

    # -------------------------------------------------------------------------
    # Step 01：优先识别具有明确控制流语义的 Statement
    # -------------------------------------------------------------------------
    if isinstance(statement_node, ast.Return):
        return u"整理并返回当前函数的最终结果"

    if isinstance(statement_node, ast.Raise):
        return u"根据无效输入或场景状态抛出明确异常"

    if isinstance(statement_node, (ast.For, ast.While)):
        return u"遍历当前数据集合，并逐项执行核心处理"

    if isinstance(statement_node, ast.Try):
        return u"执行可能失败的操作，并统一处理异常或清理状态"

    if isinstance(statement_node, ast.With):
        return u"在受控上下文中执行当前阶段操作"

    if isinstance(statement_node, ast.If):
        return u"检查当前条件与边界情况，并进入对应处理分支"

    # -------------------------------------------------------------------------
    # Step 02：根据调用的方法名称识别 Maya / Rig 常见阶段
    # -------------------------------------------------------------------------
    if contains_name_fragment(
            call_names,
            ["validate", "normalize", "check", "require"]
    ):
        return u"验证并规范化当前阶段需要的输入数据"

    if contains_name_fragment(
            call_names,
            ["get", "find", "query", "list", "selected", "xform"]
    ):
        return u"查询并整理当前阶段需要的 Maya 场景数据"

    if contains_name_fragment(
            call_names,
            ["create", "build", "duplicate", "add", "ensure"]
    ):
        return u"创建并配置当前阶段需要的 Maya / Rig 对象"

    if contains_name_fragment(
            call_names,
            ["connect", "constraint", "parent", "attach", "bind"]
    ):
        return u"建立当前阶段需要的层级、连接或驱动关系"

    if contains_name_fragment(
            call_names,
            ["set", "apply", "update", "style", "repolish"]
    ):
        return u"应用并更新当前阶段需要的属性或状态"

    if contains_name_fragment(
            call_names,
            ["delete", "remove", "clear", "cleanup", "close"]
    ):
        return u"清理当前阶段不再需要的数据或场景状态"

    # -------------------------------------------------------------------------
    # Step 03：最后回退为不会误导业务语义的通用阶段说明
    # -------------------------------------------------------------------------
    if isinstance(
            statement_node,
            (ast.Assign, ast.AnnAssign, ast.AugAssign)
    ):
        return u"准备当前阶段计算和后续处理需要的数据"

    return u"执行当前阶段的核心处理"


# =============================================================================
# Phase Selection
# =============================================================================

def get_function_body_without_docstring(function_node):
    u"""
    返回排除 Docstring 后的函数顶层 Statement。

    Args:
        function_node (ast.FunctionDef | ast.AsyncFunctionDef):
            当前需要整理的函数节点。

    Returns:
        list[ast.stmt]:
            不包含 Docstring Expr 的函数体。
    """
    statements = []
    body_index = 0

    for statement_node in function_node.body:
        is_docstring = False

        if body_index == 0:
            if isinstance(statement_node, ast.Expr):
                value_node = statement_node.value

                if isinstance(value_node, ast.Constant):
                    if isinstance(value_node.value, str):
                        is_docstring = True

        if not is_docstring:
            statements.append(
                statement_node
            )

        body_index += 1

    return statements


def get_phase_indexes(statement_count):
    u"""
    根据函数顶层 Statement 数量选择最多五个主要阶段起点。

    Args:
        statement_count (int):
            排除 Docstring 后的顶层 Statement 数量。

    Returns:
        list[int]:
            需要插入 Step 注释的 Statement Index。
    """
    if statement_count <= 0:
        return []

    # -------------------------------------------------------------------------
    # Step 01：短函数直接给每个主要顶层块一个步骤，最多五个
    # -------------------------------------------------------------------------
    if statement_count <= MAX_STEPS:
        indexes = []
        index = 0

        while index < statement_count:
            indexes.append(
                index
            )
            index += 1

        return indexes

    # -------------------------------------------------------------------------
    # Step 02：长函数按起点、四分位、中点、末段均匀选择五个阶段
    # -------------------------------------------------------------------------
    candidate_indexes = [
        0,
        int(statement_count * 0.25),
        int(statement_count * 0.50),
        int(statement_count * 0.75),
        statement_count - 1,
    ]
    indexes = []

    for index in candidate_indexes:
        if index in indexes:
            continue

        indexes.append(
            index
        )

    return indexes


def build_step_comment(indent, step_number, label):
    u"""
    构建一个统一格式的三行 Step 注释块。

    Args:
        indent (str):
            当前函数体顶层 Statement 的缩进字符串。
        step_number (int):
            当前步骤序号。
        label (str):
            当前步骤的中文语义说明。

    Returns:
        list[str]:
            可直接插入源码行列表的注释块。
    """
    return [
        indent + "# -------------------------------------------------------------------------",
        indent + "# Step {:02d}：{}".format(
            step_number,
            label
        ),
        indent + "# -------------------------------------------------------------------------",
    ]


# =============================================================================
# Source Rewrite
# =============================================================================

def annotate_source_text(source_text, source_path):
    u"""
    给一个 Runtime Python 文件中的复杂函数补充步骤注释。

    Args:
        source_text (str):
            当前 Python 文件完整源码。
        source_path (str):
            当前源码文件路径，仅用于 AST 错误上下文。

    Returns:
        tuple[str, int]:
            修改后的完整源码和本文件新增步骤注释的函数数量。
    """
    module_tree = ast.parse(
        source_text,
        filename=source_path
    )
    source_lines = source_text.splitlines()
    had_final_newline = source_text.endswith("\n")
    insertion_records = []
    annotated_count = 0

    # -------------------------------------------------------------------------
    # Step 01：找出复杂且尚未人工添加 Step 01 的函数
    # -------------------------------------------------------------------------
    function_nodes = collect_callables(
        module_tree
    )

    for function_node in function_nodes:
        metrics = get_callable_metrics(
            function_node
        )

        if not is_complex_callable(metrics):
            continue

        if has_step_comments(
                source_lines,
                function_node
        ):
            continue

        statements = get_function_body_without_docstring(
            function_node
        )

        if not statements:
            continue

        phase_indexes = get_phase_indexes(
            len(statements)
        )
        step_number = 1

        # ---------------------------------------------------------------------
        # Step 02：只在函数顶层 Statement 起点记录待插入的阶段注释
        # ---------------------------------------------------------------------
        for phase_index in phase_indexes:
            statement_node = statements[phase_index]
            label = infer_statement_label(
                statement_node
            )
            indent = " " * statement_node.col_offset
            comment_lines = build_step_comment(
                indent,
                step_number,
                label
            )
            insertion_records.append({
                "line_index": statement_node.lineno - 1,
                "lines": comment_lines,
            })
            step_number += 1

        annotated_count += 1

    # -------------------------------------------------------------------------
    # Step 03：从源码底部向上插入，避免前面的行号被后续插入偏移
    # -------------------------------------------------------------------------
    insertion_records.sort(
        key=lambda record: record["line_index"],
        reverse=True
    )

    for record in insertion_records:
        line_index = record["line_index"]
        source_lines[line_index:line_index] = record["lines"]

    # -------------------------------------------------------------------------
    # Step 04：恢复原文件换行约定并返回处理结果
    # -------------------------------------------------------------------------
    new_source_text = "\n".join(
        source_lines
    )

    if had_final_newline:
        new_source_text += "\n"

    return new_source_text, annotated_count


def process_repository(write=False):
    u"""
    检查或写入全部 Runtime 文件的步骤注释。

    Args:
        write (bool):
            True 时写回源码；False 时只统计需要修改的函数。

    Returns:
        dict:
            扫描文件数、需要处理函数数和实际修改文件列表。
    """
    project_root = get_project_root()
    source_files = iter_runtime_python_files(
        project_root
    )
    changed_files = []
    function_count = 0

    # -------------------------------------------------------------------------
    # Step 01：逐文件生成只包含注释变化的新源码
    # -------------------------------------------------------------------------
    for source_path in source_files:
        with open(
                source_path,
                "r",
                encoding="utf-8"
        ) as source_file:
            source_text = source_file.read()

        new_source_text, annotated_count = annotate_source_text(
            source_text,
            source_path
        )
        function_count += annotated_count

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
        # Step 02：Write 模式才真正覆盖文件；Check 模式保持仓库不变
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
        "function_count": function_count,
        "changed_files": changed_files,
    }


# =============================================================================
# CLI
# =============================================================================

def main():
    u"""
    命令行入口。

    Returns:
        bool:
            当前检查或写入操作完成后返回 True。
    """
    parser = argparse.ArgumentParser(
        description="Add Chinese Step comments to complex MuziTools runtime functions."
    )
    mode_group = parser.add_mutually_exclusive_group(
        required=True
    )
    mode_group.add_argument(
        "--check",
        action="store_true",
        help="Only report functions that still need generated step comments."
    )
    mode_group.add_argument(
        "--write",
        action="store_true",
        help="Insert comments into complex functions that do not have Step 01 yet."
    )
    arguments = parser.parse_args()

    # -------------------------------------------------------------------------
    # Step 01：根据命令行模式执行全仓扫描或写入
    # -------------------------------------------------------------------------
    result = process_repository(
        write=arguments.write
    )

    print("=" * 78)
    print("Runtime Step Comment Annotator")
    print("=" * 78)
    print(
        "Runtime files:      {}".format(
            result["file_count"]
        )
    )
    print(
        "Functions pending:  {}".format(
            result["function_count"]
        )
    )
    print(
        "Changed files:      {}".format(
            len(result["changed_files"])
        )
    )

    # -------------------------------------------------------------------------
    # Step 02：Check 模式发现待整理函数时返回失败码，方便 CI 作为 Gate 使用
    # -------------------------------------------------------------------------
    if arguments.check:
        if result["function_count"] > 0:
            print("Status:             NEEDS COMMENTS")
            return False

    print("Status:             PASS")
    return True


if __name__ == "__main__":
    success = main()

    if not success:
        sys.exit(1)
