# coding=utf-8
u"""
Muzi Rigging Tool Registry
==========================

只负责发现独立工具，不在主工具箱启动时提前导入全部工具模块。
真正的模块只在用户点击工具时才 import。

工具发现规则：
    1. 每个工具文件必须提供 main()；
    2. __init__.py、下划线开头文件和 test 文件不会注册；
    3. 一个子目录对应一个工具分类；
    4. 工具模块异常只影响当前工具，不拖垮整个主工具箱；
    5. 工具可以通过顶层常量 TOOL_MODE 声明运行方式；
    6. TOOL_MODE = "action" 表示直接执行，未声明时默认作为 UI 工具。
"""

from __future__ import print_function

import ast
import importlib
import os


TOOL_MODE_UI = "ui"
TOOL_MODE_ACTION = "action"

_valid_tool_modes = [
    TOOL_MODE_UI,
    TOOL_MODE_ACTION,
]

_tools_dir = os.path.dirname(os.path.abspath(__file__))

_category_names = {
    "basic": u"基础工具",
    "joint": u"骨骼工具",
    "controller": u"控制器工具",
    "rig": u"绑定工具",
    "face": u"面部工具",
    "skin": u"蒙皮工具",
    "blendshape": u"BlendShape 工具",
    "clean": u"检查与清理",
}

_category_order = [
    "basic",
    "joint",
    "controller",
    "rig",
    "face",
    "skin",
    "blendshape",
    "clean",
]

_tools_categories = {}
_tool_modules = {}


def _ignore_file(file_name):
    """判断 Python 文件是否不应该被注册为工具。"""
    if file_name == "__init__.py":
        return True

    if file_name.startswith("_"):
        return True

    if file_name.startswith("test"):
        return True

    return False


def _iter_module_names(folder_path):
    """返回目录内可发现的 Python 模块名称。"""
    module_names = []

    if not os.path.isdir(folder_path):
        return module_names

    file_names = os.listdir(folder_path)
    file_names.sort()

    for file_name in file_names:
        if not file_name.endswith(".py"):
            continue

        if _ignore_file(file_name):
            continue

        module_name = os.path.splitext(file_name)[0]
        module_names.append(module_name)

    return module_names


def _get_string_value(ast_node):
    """
    从 AST 常量节点读取字符串。

    同时兼容 Python 3.7 的 ast.Str 和较新 Python 的 ast.Constant。
    """
    if isinstance(ast_node, ast.Str):
        return ast_node.s

    constant_class = getattr(ast, "Constant", None)

    if constant_class is not None:
        if isinstance(ast_node, constant_class):
            if isinstance(ast_node.value, str):
                return ast_node.value

    return None


def _read_tool_mode(module_path):
    """
    静态读取工具文件顶层 TOOL_MODE。

    这里只解析源码 AST，不 import 工具模块，因此不会在主工具箱启动时
    触发 Maya 命令、创建窗口或加载重型依赖。

    Args:
        module_path (str):
            工具 Python 文件绝对路径。

    Returns:
        str:
            `ui` 或 `action`。
    """
    # -------------------------------------------------------------------------
    # Step 01：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        with open(
            module_path,
            "r",
            encoding="utf-8"
        ) as file_object:
            source_text = file_object.read()
    except Exception:
        return TOOL_MODE_UI

    # -------------------------------------------------------------------------
    # Step 02：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        module_tree = ast.parse(
            source_text,
            filename=module_path
        )
    except Exception:
        return TOOL_MODE_UI

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for statement in module_tree.body:
        if not isinstance(statement, ast.Assign):
            continue

        if not statement.targets:
            continue

        value = _get_string_value(
            statement.value
        )

        if value not in _valid_tool_modes:
            continue

        for target in statement.targets:
            if not isinstance(target, ast.Name):
                continue

            if target.id != "TOOL_MODE":
                continue

            return value

    # -------------------------------------------------------------------------
    # Step 04：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return TOOL_MODE_UI


def _make_runner(
    full_module_name,
    tool_mode=TOOL_MODE_UI
):
    """
    创建一个点击时才 import 工具并执行 main() 的函数。

    Runner 同时携带轻量工具元数据，主工具箱可以在不 import 真实工具模块
    的情况下决定显示“打开”还是“执行”。
    """

    def run():
        try:
            module = importlib.import_module(full_module_name)
        except Exception as error:
            raise RuntimeError(
                u"无法加载工具模块 {}：{}".format(
                    full_module_name,
                    error
                )
            )

        main_function = getattr(module, "main", None)

        if not callable(main_function):
            raise RuntimeError(
                u"工具模块没有可调用的 main()：{}".format(
                    full_module_name
                )
            )

        return main_function()

    run.__name__ = "run_{}".format(
        full_module_name.rsplit(".", 1)[-1]
    )

    run.tool_mode = tool_mode
    run.full_module_name = full_module_name

    return run


def _discover_folder(folder_path, package_prefix):
    """扫描一个工具目录并创建懒加载 Runner。"""
    tools = {}
    module_names = _iter_module_names(folder_path)

    for module_name in module_names:
        full_module_name = "{}.{}".format(
            package_prefix,
            module_name
        )

        module_path = os.path.join(
            folder_path,
            "{}.py".format(module_name)
        )

        tool_mode = _read_tool_mode(
            module_path
        )

        tools[module_name] = _make_runner(
            full_module_name,
            tool_mode=tool_mode
        )

        _tool_modules[full_module_name] = module_name

    return tools


def _discover_tools():
    """根据目录结构重新建立工具注册表。"""
    # -------------------------------------------------------------------------
    # Step 01：执行当前阶段的核心处理
    # -------------------------------------------------------------------------
    global _tools_categories
    global _tool_modules

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    _tools_categories = {}
    _tool_modules = {}
    scanned_folders = []

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for folder_name in _category_order:
        folder_path = os.path.join(
            _tools_dir,
            folder_name
        )

        if not os.path.isdir(folder_path):
            continue

        package_prefix = "{}.{}".format(
            __name__,
            folder_name
        )

        tools = _discover_folder(
            folder_path,
            package_prefix
        )

        if tools:
            category_name = _category_names.get(
                folder_name,
                folder_name
            )
            _tools_categories[category_name] = tools

        scanned_folders.append(folder_name)

    folder_names = os.listdir(_tools_dir)
    folder_names.sort()

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for folder_name in folder_names:
        if folder_name in scanned_folders:
            continue

        if folder_name.startswith("__"):
            continue

        folder_path = os.path.join(
            _tools_dir,
            folder_name
        )

        if not os.path.isdir(folder_path):
            continue

        package_prefix = "{}.{}".format(
            __name__,
            folder_name
        )

        tools = _discover_folder(
            folder_path,
            package_prefix
        )

        if tools:
            _tools_categories[folder_name] = tools

    root_tools = _discover_folder(
        _tools_dir,
        __name__
    )

    # -------------------------------------------------------------------------
    # Step 05：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if root_tools:
        _tools_categories[u"其他"] = root_tools


def refresh_tools():
    u"""
    重新扫描磁盘中的工具文件。

    Returns:
        dict:
        分类 -> 工具名 -> Runner。
    """
    _discover_tools()
    return get_tools_by_category()


def get_tools_by_category():
    u"""
    返回分类 -> 工具名 -> Runner 的浅拷贝。

    Runner 上可以读取：
        runner.tool_mode
        runner.full_module_name

    Returns:
        dict:
        当前工具注册表。
    """
    result = {}

    for category_name in _tools_categories:
        tools = _tools_categories[category_name]
        result[category_name] = tools.copy()

    return result


def get_categories():
    u"""
    返回当前工具分类顺序。

    Returns:
        list[str]:
        分类名称列表。
    """
    categories = []

    for category_name in _tools_categories:
        categories.append(category_name)

    return categories


def get_tools_in_category(category_name):
    u"""
    返回一个分类中的工具 Runner。

    Args:
        category_name (str):
            工具分类名称。

    Returns:
        dict:
        工具名 -> Runner。
    """
    if category_name not in _tools_categories:
        return {}

    return _tools_categories[category_name].copy()


def get_tool_mode(category_name, tool_name):
    u"""
    返回一个已注册工具的运行模式。

    Args:
        category_name (str):
            工具分类名称。
        tool_name (str):
            工具模块名称。

    Returns:
        str:
        `ui` 或 `action`。

    Raises:
        KeyError:
        分类或工具不存在时抛出。
    """
    if category_name not in _tools_categories:
        raise KeyError(
            u"工具分类不存在：{}".format(category_name)
        )

    tools = _tools_categories[category_name]

    if tool_name not in tools:
        raise KeyError(
            u"工具不存在：{}/{}".format(
                category_name,
                tool_name
            )
        )

    runner = tools[tool_name]

    return getattr(
        runner,
        "tool_mode",
        TOOL_MODE_UI
    )


def run_tool(category_name, tool_name):
    u"""
    按照注册表名称执行工具。

    Args:
        category_name (str):
            工具分类名称。
        tool_name (str):
            工具模块名称。

    Returns:
        object:
        工具 main() 返回值。

    Raises:
        KeyError:
        分类或工具不存在时抛出。
    """
    if category_name not in _tools_categories:
        raise KeyError(
            u"工具分类不存在：{}".format(category_name)
        )

    tools = _tools_categories[category_name]

    if tool_name not in tools:
        raise KeyError(
            u"工具不存在：{}/{}".format(
                category_name,
                tool_name
            )
        )

    return tools[tool_name]()


_discover_tools()
