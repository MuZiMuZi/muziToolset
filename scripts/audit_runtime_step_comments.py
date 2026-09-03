# coding=utf-8
u"""
Runtime Step Comment Audit
==========================

扫描 MuziTools 正式 Runtime Python 源码，找出流程较复杂、但还没有中文步骤注释的函数。

这个脚本只做静态分析，不 Import Maya，也不会修改任何 Runtime 业务逻辑。
它的目的不是要求所有小函数都写 ``Step 01``，而是把真正需要流程说明的复杂函数筛出来。

复杂函数判定规则：
    1. 函数源码跨度达到 45 行；或
    2. if / for / while / try / with 等控制流节点累计达到 5 个；或
    3. 函数内部 Call 节点达到 15 个。

复杂函数如果没有 ``Step 01`` 形式的注释，就进入审计报告。

使用方法：
    python scripts/audit_runtime_step_comments.py
    python scripts/audit_runtime_step_comments.py --write-report
"""

from __future__ import print_function

import argparse
import ast
import os
import re


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
    遍历正式 Runtime Python 文件。

    Args:
        project_root (str):
            MuziTools 仓库绝对根目录。

    Returns:
        list[str]:
            按路径排序后的 Runtime Python 文件列表。
    """
    source_files = []

    # -------------------------------------------------------------------------
    # Step 01：按 Runtime 分层目录扫描 Python 文件
    # -------------------------------------------------------------------------
    for root_name in SOURCE_ROOTS:
        source_root = os.path.join(
            project_root,
            root_name
        )

        if not os.path.isdir(source_root):
            continue

        for current_root, directory_names, file_names in os.walk(source_root):
            # -----------------------------------------------------------------
            # Step 02：排除 Python Cache 等非源码目录
            # -----------------------------------------------------------------
            if "__pycache__" in directory_names:
                directory_names.remove(
                    "__pycache__"
                )

            # -----------------------------------------------------------------
            # Step 03：只收集真实 Python 源文件
            # -----------------------------------------------------------------
            for file_name in file_names:
                if not file_name.endswith(".py"):
                    continue

                source_files.append(
                    os.path.join(
                        current_root,
                        file_name
                    )
                )

    source_files.sort()
    return source_files


# =============================================================================
# AST Metrics
# =============================================================================

def get_callable_name(function_node, parent_class=None):
    u"""
    返回适合报告显示的 Function / Method 名称。

    Args:
        function_node (ast.FunctionDef | ast.AsyncFunctionDef):
            当前正在分析的函数 AST 节点。
        parent_class (str | None):
            方法所属 Class 名称；顶层 Function 时为 None。

    Returns:
        str:
            ``Class.method`` 或普通函数名称。
    """
    if parent_class:
        return "{}.{}".format(
            parent_class,
            function_node.name
        )

    return function_node.name


def collect_callables(module_tree):
    u"""
    收集模块中的顶层 Function 和 Class Method。

    Args:
        module_tree (ast.Module):
            Python 文件解析得到的 AST Module。

    Returns:
        list[dict]:
            每个元素包含函数 AST 节点和可读名称。
    """
    result = []

    # -------------------------------------------------------------------------
    # Step 01：扫描模块顶层定义
    # -------------------------------------------------------------------------
    for node in module_tree.body:
        if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            result.append({
                "node": node,
                "name": get_callable_name(node),
            })
            continue

        if not isinstance(node, ast.ClassDef):
            continue

        # ---------------------------------------------------------------------
        # Step 02：扫描 Class 内直接定义的方法
        # ---------------------------------------------------------------------
        for child_node in node.body:
            if not isinstance(
                    child_node,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                continue

            result.append({
                "node": child_node,
                "name": get_callable_name(
                    child_node,
                    parent_class=node.name
                ),
            })

    return result


def get_callable_metrics(function_node):
    u"""
    计算一个函数的源码跨度、控制流数量和 Call 数量。

    Args:
        function_node (ast.FunctionDef | ast.AsyncFunctionDef):
            需要计算复杂度指标的函数 AST 节点。

    Returns:
        dict:
            ``line_span``、``control_flow`` 和 ``calls`` 三项统计。
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
    # Step 01：遍历函数内部全部 AST 节点
    # -------------------------------------------------------------------------
    for node in ast.walk(function_node):
        if isinstance(node, CONTROL_FLOW_TYPES):
            control_flow_count += 1

        if isinstance(node, ast.Call):
            call_count += 1

    # -------------------------------------------------------------------------
    # Step 02：返回统一复杂度数据结构
    # -------------------------------------------------------------------------
    return {
        "line_span": line_span,
        "control_flow": control_flow_count,
        "calls": call_count,
    }


def is_complex_callable(metrics):
    u"""
    判断函数是否达到需要步骤式中文注释的复杂度阈值。

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
    检查函数源码范围内是否存在 ``Step 01`` 注释。

    Args:
        source_lines (list[str]):
            当前 Python 文件按行拆分后的源码。
        function_node (ast.FunctionDef | ast.AsyncFunctionDef):
            需要检查的函数 AST 节点。

    Returns:
        bool:
            找到步骤式注释时返回 True。
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
# Repository Audit
# =============================================================================

def audit_file(source_path, project_root):
    u"""
    审计一个 Runtime Python 文件中的复杂函数步骤注释。

    Args:
        source_path (str):
            当前 Python 文件绝对路径。
        project_root (str):
            MuziTools 仓库绝对根目录。

    Returns:
        list[dict]:
            当前文件中需要补充步骤注释的函数记录。
    """
    # -------------------------------------------------------------------------
    # Step 01：读取源码并解析 AST
    # -------------------------------------------------------------------------
    with open(
            source_path,
            "r",
            encoding="utf-8"
    ) as source_file:
        source_text = source_file.read()

    module_tree = ast.parse(
        source_text,
        filename=source_path
    )
    source_lines = source_text.splitlines()
    issues = []

    # -------------------------------------------------------------------------
    # Step 02：逐个检查 Function / Method 的复杂度
    # -------------------------------------------------------------------------
    callable_data_list = collect_callables(
        module_tree
    )

    for callable_data in callable_data_list:
        function_node = callable_data["node"]
        metrics = get_callable_metrics(
            function_node
        )

        if not is_complex_callable(metrics):
            continue

        # ---------------------------------------------------------------------
        # Step 03：复杂函数已经有 Step 注释时直接通过
        # ---------------------------------------------------------------------
        if has_step_comments(
                source_lines,
                function_node
        ):
            continue

        relative_path = os.path.relpath(
            source_path,
            project_root
        ).replace(
            os.sep,
            "/"
        )

        issues.append({
            "file": relative_path,
            "name": callable_data["name"],
            "line": function_node.lineno,
            "line_span": metrics["line_span"],
            "control_flow": metrics["control_flow"],
            "calls": metrics["calls"],
        })

    return issues


def audit_repository():
    u"""
    审计全部 Runtime Python 文件。

    Returns:
        dict:
            文件数量、复杂函数问题数量和详细问题列表。
    """
    project_root = get_project_root()
    source_files = iter_runtime_python_files(
        project_root
    )
    issues = []

    # -------------------------------------------------------------------------
    # Step 01：依次扫描所有 Runtime Python 文件
    # -------------------------------------------------------------------------
    for source_path in source_files:
        file_issues = audit_file(
            source_path,
            project_root
        )

        for issue in file_issues:
            issues.append(
                issue
            )

    # -------------------------------------------------------------------------
    # Step 02：稳定排序，保证每次生成报告的顺序一致
    # -------------------------------------------------------------------------
    issues.sort(
        key=lambda item: (
            item["file"],
            item["line"],
        )
    )

    return {
        "file_count": len(source_files),
        "issue_count": len(issues),
        "issues": issues,
    }


# =============================================================================
# Report
# =============================================================================

def build_report(audit_result):
    u"""
    把审计结果转换成中文 Markdown 报告。

    Args:
        audit_result (dict):
            ``audit_repository()`` 返回的审计结果。

    Returns:
        str:
            可直接写入文档的 Markdown 文本。
    """
    lines = [
        "# Runtime 中文步骤注释审计",
        "",
        "> 本文件由 `scripts/audit_runtime_step_comments.py` 自动生成。",
        "",
        "扫描 Runtime Python 文件：**{}**".format(
            audit_result["file_count"]
        ),
        "",
        "需要补充步骤注释的复杂函数：**{}**".format(
            audit_result["issue_count"]
        ),
        "",
    ]

    if not audit_result["issues"]:
        lines.append(
            "✅ 当前复杂 Runtime 函数都已经包含步骤式中文注释。"
        )
        lines.append("")
        return "\n".join(lines)

    current_file = None

    # -------------------------------------------------------------------------
    # Step 01：按文件分组输出待整理函数
    # -------------------------------------------------------------------------
    for issue in audit_result["issues"]:
        if issue["file"] != current_file:
            current_file = issue["file"]
            lines.append(
                "## `{}`".format(current_file)
            )
            lines.append("")

        lines.append(
            "- `{}` — L{}，{} 行，控制流 {}，Call {}".format(
                issue["name"],
                issue["line"],
                issue["line_span"],
                issue["control_flow"],
                issue["calls"]
            )
        )

    lines.append("")
    return "\n".join(lines)


def write_report(report_text):
    u"""
    把步骤注释审计报告写入开发文档目录。

    Args:
        report_text (str):
            ``build_report()`` 生成的 Markdown 文本。

    Returns:
        str:
            最终报告绝对路径。
    """
    project_root = get_project_root()
    report_path = os.path.join(
        project_root,
        "docs",
        "development",
        "runtime-step-comment-audit.md"
    )

    # -------------------------------------------------------------------------
    # Step 01：确保报告目标目录存在
    # -------------------------------------------------------------------------
    report_directory = os.path.dirname(
        report_path
    )

    if not os.path.isdir(report_directory):
        os.makedirs(
            report_directory
        )

    # -------------------------------------------------------------------------
    # Step 02：以稳定 UTF-8 / LF 格式写入报告
    # -------------------------------------------------------------------------
    with open(
            report_path,
            "w",
            encoding="utf-8",
            newline="\n"
    ) as report_file:
        report_file.write(
            report_text
        )

    return report_path


def main():
    u"""
    运行 Runtime 中文步骤注释审计。

    Returns:
        bool:
            审计执行完成后返回 True。
    """
    parser = argparse.ArgumentParser(
        description="Audit complex runtime functions for Chinese step comments."
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write docs/development/runtime-step-comment-audit.md"
    )
    arguments = parser.parse_args()

    # -------------------------------------------------------------------------
    # Step 01：执行全仓 Runtime 静态审计
    # -------------------------------------------------------------------------
    audit_result = audit_repository()
    report_text = build_report(
        audit_result
    )

    # -------------------------------------------------------------------------
    # Step 02：按用户参数决定打印或写入 Markdown 报告
    # -------------------------------------------------------------------------
    if arguments.write_report:
        report_path = write_report(
            report_text
        )
        print(
            "Step comment audit written: {}".format(
                report_path
            )
        )
    else:
        print(
            report_text
        )

    return True


if __name__ == "__main__":
    main()
