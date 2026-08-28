#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tools 包初始化文件
功能：自动扫描 tools 目录及其子目录下的所有 .py 工具文件，按分类收集

目录结构示例：
    tools/
        __init__.py
        basic/              <- 基础工具分类
            constraint_tool.py
            rename_tool.py
        joint/              <- 骨骼工具分类
            joint_vis_tool.py
        ctrl/               <- 控制器工具分类
        skin/               <- 蒙皮工具分类
        blendShape/         <- BlendShape工具分类
        clean/              <- 清理工具分类

每个 .py 文件必须暴露 main() 函数作为入口
"""

import os
import importlib

# 获取当前文件所在目录（即 tools/ 目录）
_tools_dir = os.path.dirname(__file__)

# 分类名称映射：文件夹名 -> 显示名称
_CATEGORY_NAMES = {
    "basic"      : "基础工具",
    "joint"      : "骨骼工具",
    "ctrl"       : "控制器工具",
    "skin"       : "蒙皮工具",
    "blendShape" : "BlendShape工具",
    "clean"      : "清理工具",
}

# 存储结构：{分类名: {模块名: main函数}}
_tools_categories = {}


def _get_category_name(folder_name):
    """
    根据文件夹名获取中文分类名称
    如果映射表里没有，就原样返回文件夹名
    """
    return _CATEGORY_NAMES.get(folder_name, folder_name)


def _load_module_tools(module_path, package_prefix):
    """
    从指定目录加载所有带 main() 的工具模块

    Args:
        module_path: 目录的绝对路径
        package_prefix: Python 包路径前缀，例如 "MuziTools.tools.basic"

    Returns:
        dict: {模块名: main函数}
    """
    tools_dict = {}
    if not os.path.isdir(module_path):
        return tools_dict

    for _filename in os.listdir(module_path):
        # 只处理 .py 文件，排除 __init__.py
        if not _filename.endswith(".py") or _filename == "__init__.py":
            continue

        _module_name = _filename[:-3]  # 去掉 .py 后缀
        _full_module_name = f"{package_prefix}.{_module_name}"

        try:
            _module = importlib.import_module(_full_module_name)

            # 检查是否有 main 函数
            if hasattr(_module, "main") and callable(getattr(_module, "main")):
                tools_dict[_module_name] = _module.main
                print(f"[tools] 已加载: {_full_module_name}")
            else:
                print(f"[tools] 跳过 {_full_module_name}：未找到 main() 函数")

        except Exception as _e:
            print(f"[tools] 加载 {_full_module_name} 失败: {_e}")

    return tools_dict


def _discover_tools():
    """
    自动发现 tools 目录下的所有工具
    子文件夹作为分类，根目录下的 .py 文件归入 "其他" 分类
    """
    global _tools_categories

    # 1. 扫描子文件夹（分类）
    for _item in os.listdir(_tools_dir):
        _item_path = os.path.join(_tools_dir, _item)

        # 只处理文件夹，排除 __pycache__ 等特殊目录
        if not os.path.isdir(_item_path) or _item.startswith("__"):
            continue

        # 构建 Python 包路径：假设 tools 的父包是 MuziTools
        # 通过当前包名推导：例如 MuziTools.tools.basic
        _package_prefix = f"{__name__}.{_item}"

        _category_tools = _load_module_tools(_item_path, _package_prefix)

        if _category_tools:
            _category_name = _get_category_name(_item)
            _tools_categories[_category_name] = _category_tools

    # 2. 扫描根目录下的 .py 文件（没有子分类的，归入 "其他"）
    _root_tools = _load_module_tools(_tools_dir, __name__)
    if _root_tools:
        _tools_categories.setdefault("其他", {}).update(_root_tools)


# 模块导入时自动执行发现
_discover_tools()


def get_tools_by_category():
    """
    获取按分类组织的所有工具

    Returns:
        dict: {分类名: {模块名: main函数}}
        例如 {"基础工具": {"constraint_tool": <function>}, ...}
    """
    return _tools_categories.copy()


def get_categories():
    """
    获取所有分类名称列表

    Returns:
        list: 分类名列表
    """
    return list(_tools_categories.keys())


def get_tools_in_category(category_name):
    """
    获取指定分类下的所有工具

    Args:
        category_name: 分类名，例如 "基础工具"

    Returns:
        dict: {模块名: main函数}，如果分类不存在返回空字典
    """
    return _tools_categories.get(category_name, {}).copy()


def run_tool(category_name, tool_name):
    """
    通过分类名和工具名运行指定工具

    Args:
        category_name: 分类名
        tool_name: 模块名
    """
    if category_name not in _tools_categories:
        raise KeyError(f"未找到分类: {category_name}")
    if tool_name not in _tools_categories[category_name]:
        raise KeyError(f"未找到工具: {tool_name}")
    return _tools_categories[category_name][tool_name]()