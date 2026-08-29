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
    4. 工具模块异常只影响当前工具，不拖垮整个主工具箱。
"""

from __future__ import print_function

import importlib
import os


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


def _make_runner(full_module_name):
    """创建一个点击时才 import 工具并执行 main() 的函数。"""

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
    """根据目录结构重新建立工具注册表。"""
    global _tools_categories
    global _tool_modules

    _tools_categories = {}
    _tool_modules = {}
    scanned_folders = []

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
    """返回当前工具分类顺序。"""
    categories = []

    for category_name in _tools_categories:
        categories.append(category_name)

    return categories


def get_tools_in_category(category_name):
    """返回一个分类中的工具 Runner。"""
    if category_name not in _tools_categories:
        return {}

    return _tools_categories[category_name].copy()


def run_tool(category_name, tool_name):
    """按照注册表名称执行工具。"""
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
