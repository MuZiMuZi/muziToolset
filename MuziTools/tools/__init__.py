#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import importlib
import os

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
_CATEGORY_NAMES = {
    'basic': '基础工具',
    'joint': '骨骼工具',
    'ctrl': '控制器工具',
    'rig': '绑定工具',
    'face': '面部工具',
    'skin': '蒙皮工具',
    'blendShape': 'BlendShape工具',
    'clean': '清理工具',
}
_CATEGORY_ORDER = ['basic', 'joint', 'ctrl', 'rig', 'face', 'skin', 'blendShape', 'clean']
_tools_categories = {}


def _ignore(name):
    return name == '__init__.py' or name.startswith('_') or name.startswith('test')


def _load(folder_path, package_prefix):
    result = {}
    if not os.path.isdir(folder_path):
        return result
    for file_name in sorted(os.listdir(folder_path)):
        if not file_name.endswith('.py') or _ignore(file_name):
            continue
        module_name = file_name[:-3]
        full_name = '{}.{}'.format(package_prefix, module_name)
        try:
            module = importlib.import_module(full_name)
            main_func = getattr(module, 'main', None)
            if callable(main_func):
                result[module_name] = main_func
                print('[MuziTools] loaded: {}'.format(full_name))
            else:
                print('[MuziTools] skipped {}: no main()'.format(full_name))
        except Exception as error:
            print('[MuziTools] failed {}: {}'.format(full_name, error))
    return result


def _discover_tools():
    global _tools_categories
    _tools_categories = {}
    scanned = set()

    for folder_name in _CATEGORY_ORDER:
        folder_path = os.path.join(_TOOLS_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue
        tools = _load(folder_path, '{}.{}'.format(__name__, folder_name))
        if tools:
            _tools_categories[_CATEGORY_NAMES.get(folder_name, folder_name)] = tools
        scanned.add(folder_name)

    for folder_name in sorted(os.listdir(_TOOLS_DIR)):
        if folder_name in scanned or folder_name.startswith('__'):
            continue
        folder_path = os.path.join(_TOOLS_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue
        tools = _load(folder_path, '{}.{}'.format(__name__, folder_name))
        if tools:
            _tools_categories[folder_name] = tools

    root_tools = _load(_TOOLS_DIR, __name__)
    if root_tools:
        _tools_categories['其他'] = root_tools


def refresh_tools():
    _discover_tools()
    return get_tools_by_category()


def get_tools_by_category():
    result = {}
    for category, tools in _tools_categories.items():
        result[category] = tools.copy()
    return result


def get_categories():
    return list(_tools_categories.keys())


def get_tools_in_category(category_name):
    if category_name not in _tools_categories:
        return {}
    return _tools_categories[category_name].copy()


def run_tool(category_name, tool_name):
    return _tools_categories[category_name][tool_name]()


_discover_tools()
