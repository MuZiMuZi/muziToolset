# coding=utf-8
u"""
MuziTools Tool Registry
=======================

只扫描 ``tools`` 目录结构，不在主工具箱启动时导入所有子工具。
真正的工具模块只在按钮被点击时才 import，从而做到：

    1. 某一个子工具依赖失败不会拖垮整个 Toolbox；
    2. Maya 启动和打开 Toolbox 更快；
    3. 新增符合规范的 ``*.py`` 工具后可通过 ``refresh_tools()`` 重新发现。

每个可发现工具文件必须提供 ``main()``。
"""

from __future__ import print_function

import importlib
import os


_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

_CATEGORY_NAMES = {
    "basic": u"基础工具",
    "joint": u"骨骼工具",
    "ctrl": u"控制器工具",
    "rig": u"绑定工具",
    "face": u"面部工具",
    "skin": u"蒙皮工具",
    "blendShape": u"BlendShape工具",
    "clean": u"清理工具",
}

_CATEGORY_ORDER = [
    "basic",
    "joint",
    "ctrl",
    "rig",
    "face",
    "skin",
    "blendShape",
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


def _make_runner(full_module_name):
    """
    创建一个点击时才 import 模块并执行 ``main()`` 的函数。
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

        main_func = getattr(module, "main", None)

        if not callable(main_func):
            raise RuntimeError(
                u"工具模块没有可调用的 main()：{}".format(
                    full_module_name
                )
            )

        return main_func()

    run.__name__ = "run_{}".format(
        full_module_name.rsplit(".", 1)[-1]
    )

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

        tools[module_name] = _make_runner(full_module_name)
        _tool_modules[full_module_name] = module_name

    return tools


def _discover_tools():
    """根据目录结构重建工具注册表。"""
    global _tools_categories
    global _tool_modules

    _tools_categories = {}
    _tool_modules = {}
    scanned_folders = []

    for folder_name in _CATEGORY_ORDER:
        folder_path = os.path.join(
            _TOOLS_DIR,
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
            category_name = _CATEGORY_NAMES.get(
                folder_name,
                folder_name
            )
            _tools_categories[category_name] = tools

        scanned_folders.append(folder_name)

    folder_names = os.listdir(_TOOLS_DIR)
    folder_names.sort()

    for folder_name in folder_names:
        if folder_name in scanned_folders:
            continue

        if folder_name.startswith("__"):
            continue

        folder_path = os.path.join(
            _TOOLS_DIR,
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
        _TOOLS_DIR,
        __name__
    )

    if root_tools:
        _tools_categories[u"其他"] = root_tools


def refresh_tools():
    """重新扫描磁盘中的工具文件。"""
    _discover_tools()
    return get_tools_by_category()


def get_tools_by_category():
    """返回分类 -> 工具名 -> Runner 的浅拷贝。"""
    result = {}

    for category_name in _tools_categories:
        tools = _tools_categories[category_name]
        result[category_name] = tools.copy()

    return result


def get_categories():
    """返回当前分类顺序。"""
    categories = []

    for category_name in _tools_categories:
        categories.append(category_name)

    return categories


def get_tools_in_category(category_name):
    """返回一个分类下的工具 Runner。"""
    if category_name not in _tools_categories:
        return {}

    return _tools_categories[category_name].copy()


def run_tool(category_name, tool_name):
    """按注册表名称执行工具。"""
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
