# coding=utf-8
u"""
Runtime Docstring Normalizer
============================

为 MuziTools 正式运行时代码统一补齐公开 API Docstring。

本脚本只处理文档字符串，不修改 Maya 业务逻辑。
它使用 Python AST 静态分析，因此不需要 Maya / PySide 环境。

规范目标：
    1. 每个公开 Function / Method 都有中文功能摘要；
    2. 每个公开参数都有类型和中文说明；
    3. 有返回值的方法必须说明返回类型和含义；
    4. 显式抛出的异常进入 Raises；
    5. 已有 Example / Notes / Usage 尽量完整保留；
    6. 不使用列表推导式承载主要处理逻辑，保持项目现有可读性习惯。

使用：
    python scripts/normalize_runtime_docstrings.py --check
    python scripts/normalize_runtime_docstrings.py --write
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

SECTION_ALIASES = {
    "args": "args",
    "arguments": "args",
    "parameters": "args",
    "params": "args",
    "参数": "args",
    "参数说明": "args",
    "returns": "returns",
    "return": "returns",
    "返回": "returns",
    "返回值": "returns",
    "raises": "raises",
    "exceptions": "raises",
    "异常": "raises",
    "异常说明": "raises",
    "example": "examples",
    "examples": "examples",
    "示例": "examples",
    "使用示例": "examples",
    "notes": "notes",
    "note": "notes",
    "注意": "notes",
    "说明": "notes",
    "备注": "notes",
    "usage": "usage",
    "use cases": "usage",
    "使用场景": "usage",
    "适用场景": "usage",
}


# =============================================================================
# Project / Source
# =============================================================================

def get_project_root():
    u"""返回 MuziTools 仓库根目录。"""
    script_directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    project_root = os.path.dirname(
        script_directory
    )
    return project_root


def is_runtime_python_file(file_name):
    u"""判断文件是否属于正式 Runtime Python API。"""
    if not file_name.endswith(".py"):
        return False

    if file_name == "__init__.py":
        return True

    if file_name.startswith("_"):
        return False

    return True


def iter_runtime_source_files(project_root):
    u"""扫描正式 Runtime Python 文件。"""
    source_files = []

    for root_name in SOURCE_ROOTS:
        source_root = os.path.join(
            project_root,
            root_name
        )

        if not os.path.isdir(source_root):
            continue

        for current_root, folder_names, file_names in os.walk(source_root):
            if "__pycache__" in folder_names:
                folder_names.remove(
                    "__pycache__"
                )

            for file_name in file_names:
                if not is_runtime_python_file(file_name):
                    continue

                source_path = os.path.join(
                    current_root,
                    file_name
                )
                source_files.append(
                    source_path
                )

    for file_name in ROOT_MODULE_FILES:
        source_path = os.path.join(
            project_root,
            file_name
        )

        if not os.path.isfile(source_path):
            continue

        source_files.append(
            source_path
        )

    source_files.sort()
    return source_files


def read_source_text(source_path):
    u"""读取 UTF-8 Python 源码。"""
    with open(
            source_path,
            "r",
            encoding="utf-8"
    ) as file_object:
        return file_object.read()


def write_source_text(source_path, source_text):
    u"""写入 UTF-8 Python 源码。"""
    with open(
            source_path,
            "w",
            encoding="utf-8",
            newline="\n"
    ) as file_object:
        file_object.write(
            source_text
        )


# =============================================================================
# Docstring Parse
# =============================================================================

def normalize_section_name(text):
    u"""把 Docstring 章节名称转换成内部标准名称。"""
    if not text:
        return None

    normalized_text = text.strip()
    normalized_text = normalized_text.rstrip(":")
    normalized_text = normalized_text.lower()

    return SECTION_ALIASES.get(
        normalized_text
    )


def split_docstring_sections(docstring):
    u"""拆分 Summary / Args / Returns / Raises / Example 等章节。"""
    result = {
        "summary": "",
        "body": "",
        "args": "",
        "returns": "",
        "raises": "",
        "examples": "",
        "notes": "",
        "usage": "",
    }

    if not docstring:
        return result

    raw_lines = docstring.expandtabs(4).strip().splitlines()
    current_section = "body"

    section_lines = {
        "body": [],
        "args": [],
        "returns": [],
        "raises": [],
        "examples": [],
        "notes": [],
        "usage": [],
    }

    for line in raw_lines:
        stripped_line = line.strip()
        section_name = normalize_section_name(
            stripped_line
        )

        if section_name:
            current_section = section_name
            continue

        section_lines[current_section].append(
            line.rstrip()
        )

    body_lines = section_lines["body"]
    summary_lines = []
    remaining_lines = []
    summary_finished = False

    for line in body_lines:
        stripped_line = line.strip()

        if not stripped_line:
            if summary_lines:
                summary_finished = True
            continue

        character_set = set(stripped_line)

        if character_set == set("="):
            continue

        if character_set == set("-"):
            continue

        if not summary_finished:
            summary_lines.append(
                stripped_line
            )
        else:
            remaining_lines.append(
                line
            )

    result["summary"] = " ".join(
        summary_lines
    ).strip()
    result["body"] = "\n".join(
        remaining_lines
    ).strip()

    for section_name in [
        "args",
        "returns",
        "raises",
        "examples",
        "notes",
        "usage",
    ]:
        result[section_name] = "\n".join(
            section_lines[section_name]
        ).strip()

    return result


def parse_argument_descriptions(args_text):
    u"""解析现有 Args 中的类型和参数说明。"""
    descriptions = {}

    if not args_text:
        return descriptions

    argument_pattern = re.compile(
        r"^\s*([*]{0,2}[A-Za-z_][A-Za-z0-9_]*)"
        r"(?:\s*\(([^)]*)\))?\s*:\s*(.*)$"
    )

    current_name = None
    current_type = ""
    current_description = []

    def save_current_argument():
        if current_name is None:
            return

        descriptions[current_name] = {
            "type": current_type,
            "description": " ".join(
                current_description
            ).strip(),
        }

    for line in args_text.splitlines():
        match = argument_pattern.match(
            line
        )

        if match:
            save_current_argument()

            current_name = match.group(1).lstrip("*")
            current_type = match.group(2) or ""
            current_description = []

            inline_description = match.group(3).strip()

            if inline_description:
                current_description.append(
                    inline_description
                )

            continue

        stripped_line = line.strip()

        if current_name is None:
            continue

        if not stripped_line:
            continue

        current_description.append(
            stripped_line
        )

    save_current_argument()
    return descriptions


# =============================================================================
# Type / Description Inference
# =============================================================================

def format_ast_value(node):
    u"""把 AST Annotation / 默认值转换成可读源码字符串。"""
    if node is None:
        return ""

    try:
        return ast.unparse(node)
    except Exception:
        return ""


def get_function_parameters(function_node):
    u"""收集 Function / Method 的参数和默认值。"""
    parameters = []
    arguments = function_node.args
    positional_arguments = []

    for argument in arguments.posonlyargs:
        positional_arguments.append(
            ("positional_only", argument)
        )

    for argument in arguments.args:
        positional_arguments.append(
            ("positional", argument)
        )

    default_count = len(
        arguments.defaults
    )
    first_default_index = len(positional_arguments) - default_count

    for parameter_index, parameter_data in enumerate(positional_arguments):
        parameter_kind = parameter_data[0]
        argument = parameter_data[1]
        default_node = None

        if parameter_index >= first_default_index:
            default_index = parameter_index - first_default_index
            default_node = arguments.defaults[
                default_index
            ]

        parameters.append({
            "name": argument.arg,
            "annotation": argument.annotation,
            "default": default_node,
            "kind": parameter_kind,
        })

    if arguments.vararg is not None:
        parameters.append({
            "name": arguments.vararg.arg,
            "annotation": arguments.vararg.annotation,
            "default": None,
            "kind": "vararg",
        })

    for parameter_index, argument in enumerate(arguments.kwonlyargs):
        parameters.append({
            "name": argument.arg,
            "annotation": argument.annotation,
            "default": arguments.kw_defaults[parameter_index],
            "kind": "keyword_only",
        })

    if arguments.kwarg is not None:
        parameters.append({
            "name": arguments.kwarg.arg,
            "annotation": arguments.kwarg.annotation,
            "default": None,
            "kind": "kwarg",
        })

    return parameters


def infer_type_from_parameter_name(parameter_name):
    u"""根据项目常见参数命名推断基础类型。"""
    name = parameter_name.lower()

    bool_names = [
        "force",
        "lock",
        "hide",
        "keyable",
        "visible",
        "visibility",
        "required",
        "strict",
        "clear_existing",
        "maintain_offset",
        "translate",
        "rotate",
        "scale",
        "world_space",
        "relative",
        "replace",
        "enabled",
        "recursive",
    ]

    if name in bool_names:
        return "bool"

    if name.startswith("is_"):
        return "bool"

    if name.startswith("has_"):
        return "bool"

    if name.startswith("use_"):
        return "bool"

    string_suffixes = [
        "_path",
        "_name",
        "_attr",
        "_plug",
        "_axis",
        "_side",
    ]

    for suffix in string_suffixes:
        if name.endswith(suffix):
            return "str"

    integer_suffixes = [
        "_index",
        "_count",
        "_number",
    ]

    for suffix in integer_suffixes:
        if name.endswith(suffix):
            return "int"

    float_suffixes = [
        "_radius",
        "_size",
        "_weight",
        "_ratio",
        "_distance",
    ]

    for suffix in float_suffixes:
        if name.endswith(suffix):
            return "float"

    if name.endswith("_list"):
        return "list"

    if name.endswith("_dict"):
        return "dict"

    if name.endswith("_map"):
        return "dict"

    if name.endswith("_data"):
        return "dict"

    plural_names = [
        "nodes",
        "objects",
        "transforms",
        "joints",
        "curves",
        "meshes",
        "surfaces",
        "controls",
        "controllers",
        "guides",
        "groups",
        "attrs",
        "attributes",
        "plugs",
        "targets",
        "sources",
        "drivers",
        "drivens",
        "children",
        "parents",
        "influences",
    ]

    if name in plural_names:
        return "str | list[str]"

    string_names = [
        "node",
        "object",
        "transform",
        "joint",
        "curve",
        "mesh",
        "surface",
        "control",
        "controller",
        "guide",
        "group",
        "parent",
        "child",
        "source",
        "target",
        "driver",
        "driven",
        "up_object",
        "attr",
        "attribute",
        "plug",
        "name",
        "side",
        "axis",
        "file_path",
        "directory",
        "pattern",
        "node_type",
        "feature",
        "region",
        "part",
    ]

    if name in string_names:
        return "str"

    integer_names = [
        "index",
        "count",
        "number",
        "step_value",
        "last_step",
    ]

    if name in integer_names:
        return "int"

    float_names = [
        "radius",
        "size",
        "weight",
        "value",
        "offset",
        "distance",
        "ratio",
    ]

    if name in float_names:
        return "float"

    return "object"


def infer_parameter_type(parameter):
    u"""综合 Annotation、默认值和参数名称推断类型。"""
    annotation = parameter["annotation"]

    if annotation is not None:
        annotation_text = format_ast_value(
            annotation
        )

        if annotation_text:
            return annotation_text

    if parameter["kind"] == "vararg":
        return "tuple"

    if parameter["kind"] == "kwarg":
        return "dict"

    default_node = parameter["default"]

    if isinstance(default_node, ast.Constant):
        default_value = default_node.value

        if isinstance(default_value, bool):
            return "bool"

        if isinstance(default_value, int):
            return "int"

        if isinstance(default_value, float):
            return "float"

        if isinstance(default_value, str):
            return "str"

    if isinstance(default_node, ast.List):
        return "list"

    if isinstance(default_node, ast.Tuple):
        return "tuple"

    if isinstance(default_node, ast.Dict):
        return "dict"

    if isinstance(default_node, ast.Set):
        return "set"

    return infer_type_from_parameter_name(
        parameter["name"]
    )


def infer_parameter_description(parameter_name, parameter_type):
    u"""根据常见参数名称生成基础中文说明。"""
    name = parameter_name.lower()

    exact_descriptions = {
        "parent": u"父级 Maya 节点名称。",
        "child": u"需要挂到父级下的子 Maya 节点名称。",
        "source": u"作为输入或驱动来源的 Maya 节点名称。",
        "target": u"接收结果或被处理的目标 Maya 节点名称。",
        "driver": u"作为驱动端的 Maya 节点名称。",
        "driven": u"作为被驱动端的 Maya 节点名称。",
        "node": u"需要查询或处理的 Maya 节点名称。",
        "nodes": u"需要批量查询或处理的 Maya 节点名称或节点列表。",
        "object": u"需要处理的 Maya 场景对象名称。",
        "objects": u"需要批量处理的 Maya 场景对象名称或对象列表。",
        "transform": u"需要处理的 Maya Transform 节点名称。",
        "joint": u"需要处理的 Maya Joint 节点名称。",
        "curve": u"需要处理的 Maya Curve Transform 或 Shape 名称。",
        "mesh": u"需要处理的 Maya Mesh Transform 或 Shape 名称。",
        "surface": u"需要处理的 Maya Surface 节点名称。",
        "control": u"需要处理的控制器 Transform 名称。",
        "controller": u"需要处理的控制器 Transform 名称。",
        "guide": u"需要查询或处理的 Guide Transform 名称。",
        "group": u"需要查询、创建或整理的 Group 名称。",
        "attr": u"Maya Attribute 名称。",
        "attribute": u"Maya Attribute 或完整 Plug 名称。",
        "plug": u"完整 Maya Plug 名称，例如 node.translateX。",
        "name": u"创建或查询时使用的节点名称。",
        "side": u"方向标记，常用值为 lf、rt 或 md。",
        "axis": u"操作使用的轴向标记。",
        "file_path": u"需要读取或写入的文件路径。",
        "directory": u"需要读取或写入的目录路径。",
        "pattern": u"用于筛选 Maya 节点名称的匹配模式。",
        "force": u"是否强制覆盖已有连接、状态或结果。",
        "maintain_offset": u"是否在建立约束或矩阵关系时保持当前偏移。",
        "required": u"目标不存在或数据缺失时是否直接抛出异常。",
        "strict": u"是否使用严格模式处理缺失或无效数据。",
        "clear_existing": u"写入新结果前是否先清理已有数据。",
        "translate": u"是否处理 Translate 通道。",
        "rotate": u"是否处理 Rotate 通道。",
        "scale": u"是否处理 Scale 通道。",
        "index": u"目标元素或节点的序号。",
        "count": u"需要创建、采样或处理的数量。",
        "radius": u"创建节点或控制器使用的半径值。",
        "size": u"创建或显示对象使用的尺寸值。",
        "weight": u"当前计算、混合或变形使用的权重值。",
        "value": u"需要读取、写入或参与计算的数值。",
    }

    if name in exact_descriptions:
        return exact_descriptions[name]

    if name.startswith("is_") or name.startswith("has_") or name.startswith("use_"):
        return u"控制 `{}` 对应功能是否启用。".format(
            parameter_name
        )

    if name.endswith("_path"):
        return u"`{}` 对应的文件或目录路径。".format(
            parameter_name
        )

    if name.endswith("_name"):
        return u"`{}` 对应的 Maya 节点或资源名称。".format(
            parameter_name
        )

    if name.endswith("_list") or parameter_type.startswith("list"):
        return u"`{}` 对应的数据列表。".format(
            parameter_name
        )

    if name.endswith("_dict") or name.endswith("_map") or parameter_type.startswith("dict"):
        return u"`{}` 对应的配置或映射字典。".format(
            parameter_name
        )

    if parameter_type == "bool":
        return u"是否启用 `{}` 对应的处理。".format(
            parameter_name
        )

    if parameter_type == "str":
        return u"`{}` 对应的名称、标记或字符串参数。".format(
            parameter_name
        )

    if parameter_type == "int":
        return u"`{}` 对应的整数参数。".format(
            parameter_name
        )

    if parameter_type == "float":
        return u"`{}` 对应的数值参数。".format(
            parameter_name
        )

    return u"`{}` 对应的输入数据。".format(
        parameter_name
    )


def infer_return_type(function_node):
    u"""根据 Return AST 节点推断基础返回类型。"""
    if function_node.returns is not None:
        annotation_text = format_ast_value(
            function_node.returns
        )

        if annotation_text:
            return annotation_text

    return_nodes = []

    for node in ast.walk(function_node):
        if not isinstance(node, ast.Return):
            continue

        return_nodes.append(
            node
        )

    if not return_nodes:
        return "None"

    inferred_types = []

    for return_node in return_nodes:
        value_node = return_node.value

        if value_node is None:
            inferred_type = "None"
        elif isinstance(value_node, ast.Constant):
            value = value_node.value

            if isinstance(value, bool):
                inferred_type = "bool"
            elif isinstance(value, int):
                inferred_type = "int"
            elif isinstance(value, float):
                inferred_type = "float"
            elif isinstance(value, str):
                inferred_type = "str"
            elif value is None:
                inferred_type = "None"
            else:
                inferred_type = "object"
        elif isinstance(value_node, ast.List):
            inferred_type = "list"
        elif isinstance(value_node, ast.Tuple):
            inferred_type = "tuple"
        elif isinstance(value_node, ast.Dict):
            inferred_type = "dict"
        elif isinstance(value_node, ast.Set):
            inferred_type = "set"
        else:
            inferred_type = "object"

        if inferred_type not in inferred_types:
            inferred_types.append(
                inferred_type
            )

    if len(inferred_types) == 1:
        return inferred_types[0]

    return " | ".join(
        inferred_types
    )


def collect_raise_types(function_node):
    u"""收集方法中显式 raise 的异常类型。"""
    exception_types = []

    for node in ast.walk(function_node):
        if not isinstance(node, ast.Raise):
            continue

        exception_node = node.exc

        if exception_node is None:
            continue

        if isinstance(exception_node, ast.Call):
            exception_name = format_ast_value(
                exception_node.func
            )
        else:
            exception_name = format_ast_value(
                exception_node
            )

        if not exception_name:
            continue

        if exception_name in exception_types:
            continue

        exception_types.append(
            exception_name
        )

    return exception_types


# =============================================================================
# Docstring Build
# =============================================================================

def clean_summary(summary, function_name):
    u"""返回适合作为公开 API 第一行的简短摘要。"""
    if summary:
        summary = " ".join(
            summary.split()
        )

        if len(summary) <= 120:
            return summary

        return summary[:117].rstrip() + "..."

    return u"执行 `{}` 对应的 Maya 工具操作。".format(
        function_name
    )


def build_standard_docstring(function_node):
    u"""根据现有源码和 AST 构建标准公开 API Docstring。"""
    existing_docstring = ast.get_docstring(
        function_node
    ) or ""

    sections = split_docstring_sections(
        existing_docstring
    )
    existing_arguments = parse_argument_descriptions(
        sections["args"]
    )

    lines = []
    summary = clean_summary(
        sections["summary"],
        function_node.name
    )
    lines.append(
        summary
    )

    if sections["body"]:
        lines.append("")
        lines.append(
            sections["body"]
        )

    parameters = get_function_parameters(
        function_node
    )
    visible_parameters = []

    for parameter in parameters:
        if parameter["name"] in ["self", "cls"]:
            continue

        visible_parameters.append(
            parameter
        )

    if visible_parameters:
        lines.append("")
        lines.append("Args:")

        for parameter in visible_parameters:
            parameter_name = parameter["name"]
            existing_info = existing_arguments.get(
                parameter_name
            )

            parameter_type = ""
            parameter_description = ""

            if existing_info:
                parameter_type = existing_info.get(
                    "type",
                    ""
                )
                parameter_description = existing_info.get(
                    "description",
                    ""
                )

            if not parameter_type:
                parameter_type = infer_parameter_type(
                    parameter
                )

            if not parameter_description:
                parameter_description = infer_parameter_description(
                    parameter_name,
                    parameter_type
                )

            lines.append(
                "    {} ({}):".format(
                    parameter_name,
                    parameter_type
                )
            )
            lines.append(
                "        " + parameter_description
            )

    return_type = infer_return_type(
        function_node
    )

    if sections["returns"]:
        lines.append("")
        lines.append("Returns:")

        for return_line in sections["returns"].splitlines():
            lines.append(
                "    " + return_line.strip()
            )
    elif return_type != "None":
        lines.append("")
        lines.append("Returns:")
        lines.append(
            "    {}:".format(
                return_type
            )
        )
        lines.append(
            u"        方法执行后的结果数据。"
        )

    if sections["raises"]:
        lines.append("")
        lines.append("Raises:")

        for raise_line in sections["raises"].splitlines():
            lines.append(
                "    " + raise_line.strip()
            )
    else:
        exception_types = collect_raise_types(
            function_node
        )

        if exception_types:
            lines.append("")
            lines.append("Raises:")

            for exception_type in exception_types:
                lines.append(
                    "    {}:".format(
                        exception_type
                    )
                )
                lines.append(
                    u"        输入数据、场景状态或操作条件不满足要求时抛出。"
                )

    if sections["examples"]:
        lines.append("")
        lines.append("Example:")

        for example_line in sections["examples"].splitlines():
            lines.append(
                "    " + example_line.rstrip()
            )

    if sections["notes"]:
        lines.append("")
        lines.append("Notes:")

        for note_line in sections["notes"].splitlines():
            lines.append(
                "    " + note_line.rstrip()
            )

    if sections["usage"]:
        lines.append("")
        lines.append("Usage:")

        for usage_line in sections["usage"].splitlines():
            lines.append(
                "    " + usage_line.rstrip()
            )

    return "\n".join(
        lines
    ).strip()


def is_public_callable(function_node):
    u"""判断 Function / Method 是否属于公开 API。"""
    if function_node.name == "__init__":
        return True

    if function_node.name.startswith("_"):
        return False

    return True


def collect_public_callables(module_tree):
    u"""按源码顺序收集公开顶层 Function 和 Class Method。"""
    callables = []

    for node in module_tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if is_public_callable(node):
                callables.append(
                    node
                )
            continue

        if not isinstance(node, ast.ClassDef):
            continue

        if node.name.startswith("_"):
            continue

        for child_node in node.body:
            if not isinstance(child_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            if not is_public_callable(child_node):
                continue

            callables.append(
                child_node
            )

    callables.sort(
        key=lambda callable_node: callable_node.lineno,
        reverse=True
    )
    return callables


def get_docstring_statement(function_node):
    u"""返回 Function / Method 当前 Docstring 对应 AST Expr。"""
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


def build_indented_docstring(docstring, indent):
    u"""把标准 Docstring 转换成源码文本。"""
    lines = []
    lines.append(
        indent + 'u"""'
    )

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


def normalize_source_text(source_text, source_path):
    u"""返回补齐公开 API Docstring 后的源码。"""
    module_tree = ast.parse(
        source_text,
        filename=source_path
    )
    source_lines = source_text.splitlines()
    had_final_newline = source_text.endswith("\n")

    public_callables = collect_public_callables(
        module_tree
    )

    for function_node in public_callables:
        standard_docstring = build_standard_docstring(
            function_node
        )

        if not function_node.body:
            continue

        first_body_statement = function_node.body[0]
        indent = " " * first_body_statement.col_offset
        replacement_lines = build_indented_docstring(
            standard_docstring,
            indent
        )

        docstring_statement = get_docstring_statement(
            function_node
        )

        if docstring_statement is not None:
            start_index = docstring_statement.lineno - 1
            end_index = docstring_statement.end_lineno

            source_lines[
                start_index:end_index
            ] = replacement_lines
        else:
            insert_index = first_body_statement.lineno - 1
            source_lines[
                insert_index:insert_index
            ] = replacement_lines + [""]

    normalized_text = "\n".join(
        source_lines
    )

    if had_final_newline:
        normalized_text += "\n"

    return normalized_text


# =============================================================================
# Validation
# =============================================================================

def validate_callable_docstring(function_node, source_path):
    u"""检查一个公开 Function / Method 的参数类型和说明是否完整。"""
    errors = []
    docstring = ast.get_docstring(
        function_node
    ) or ""
    sections = split_docstring_sections(
        docstring
    )

    if not sections["summary"]:
        errors.append(
            u"{}:{} {} 缺少功能摘要".format(
                source_path,
                function_node.lineno,
                function_node.name
            )
        )

    argument_descriptions = parse_argument_descriptions(
        sections["args"]
    )
    parameters = get_function_parameters(
        function_node
    )

    for parameter in parameters:
        parameter_name = parameter["name"]

        if parameter_name in ["self", "cls"]:
            continue

        description_info = argument_descriptions.get(
            parameter_name
        )

        if not description_info:
            errors.append(
                u"{}:{} {}.{} 缺少 Args 说明".format(
                    source_path,
                    function_node.lineno,
                    function_node.name,
                    parameter_name
                )
            )
            continue

        if not description_info.get("type"):
            errors.append(
                u"{}:{} {}.{} 缺少参数类型".format(
                    source_path,
                    function_node.lineno,
                    function_node.name,
                    parameter_name
                )
            )

        if not description_info.get("description"):
            errors.append(
                u"{}:{} {}.{} 缺少参数说明".format(
                    source_path,
                    function_node.lineno,
                    function_node.name,
                    parameter_name
                )
            )

    return_type = infer_return_type(
        function_node
    )

    if return_type != "None":
        if not sections["returns"]:
            errors.append(
                u"{}:{} {} 缺少 Returns 说明".format(
                    source_path,
                    function_node.lineno,
                    function_node.name
                )
            )

    return errors


def validate_source_text(source_text, source_path):
    u"""检查一个 Runtime Python 文件的公开 API Docstring。"""
    module_tree = ast.parse(
        source_text,
        filename=source_path
    )
    errors = []
    public_callables = collect_public_callables(
        module_tree
    )

    for function_node in public_callables:
        callable_errors = validate_callable_docstring(
            function_node,
            source_path
        )

        for error in callable_errors:
            errors.append(
                error
            )

    return errors


# =============================================================================
# Main
# =============================================================================

def run(write=False):
    u"""执行 Runtime Docstring 规范化或检查。"""
    project_root = get_project_root()
    source_files = iter_runtime_source_files(
        project_root
    )

    changed_files = []
    validation_errors = []

    for source_path in source_files:
        source_text = read_source_text(
            source_path
        )

        if write:
            normalized_text = normalize_source_text(
                source_text,
                source_path
            )

            if normalized_text != source_text:
                write_source_text(
                    source_path,
                    normalized_text
                )
                changed_files.append(
                    source_path
                )
                source_text = normalized_text

        source_errors = validate_source_text(
            source_text,
            source_path
        )

        for error in source_errors:
            validation_errors.append(
                error
            )

    print("=" * 78)
    print("Runtime Docstring Standard")
    print("=" * 78)
    print(
        "Runtime files:  {}".format(
            len(source_files)
        )
    )
    print(
        "Changed files:  {}".format(
            len(changed_files)
        )
    )
    print(
        "Errors:         {}".format(
            len(validation_errors)
        )
    )

    if changed_files:
        print("Changed:")

        for source_path in changed_files:
            relative_path = os.path.relpath(
                source_path,
                project_root
            )
            print(
                "  - " + relative_path
            )

    if validation_errors:
        print("Validation errors:")

        for error in validation_errors:
            print(
                "  - " + error
            )

        print("=" * 78)
        return False

    print("Status:         PASS")
    print("=" * 78)
    return True


def main():
    u"""命令行入口。"""
    parser = argparse.ArgumentParser(
        description="Normalize MuziTools runtime public API docstrings."
    )
    mode_group = parser.add_mutually_exclusive_group(
        required=True
    )
    mode_group.add_argument(
        "--check",
        action="store_true",
        help="Only validate runtime docstrings."
    )
    mode_group.add_argument(
        "--write",
        action="store_true",
        help="Rewrite runtime public API docstrings and validate them."
    )

    arguments = parser.parse_args()

    success = run(
        write=arguments.write
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
