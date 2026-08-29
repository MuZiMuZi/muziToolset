# coding=utf-8
u"""
Scene IO Utils
==============

Maya Scene 文件输入输出底层工具。

职责：
    1. 查询当前 Scene 路径；
    2. 打开 / 导入 Maya Scene；
    3. 创建 Reference；
    4. 导出当前选择为 FBX。

本模块不弹出任何 PySide 对话框，路径由调用方提供。
"""

from __future__ import print_function

import os

import maya.cmds as cmds
import maya.mel as mel

from . import file_utils


def get_current_scene_path():
    """返回当前 Maya Scene 的绝对路径；未保存时返回空字符串。"""
    scene_path = cmds.file(
        query=True,
        sceneName=True
    )

    if not scene_path:
        return ""

    return file_utils.normalize_path(scene_path)


def is_scene_modified():
    """返回当前 Maya Scene 是否存在未保存修改。"""
    return bool(
        cmds.file(
            query=True,
            modified=True
        )
    )


def validate_scene_file(file_path):
    """检查 Maya Scene 文件是否存在，并返回规范路径。"""
    normalized_path = file_utils.normalize_path(file_path)

    if not normalized_path:
        raise ValueError(u"file_path 不能为空。")

    if not os.path.isfile(normalized_path):
        raise RuntimeError(
            u"文件不存在：{}".format(normalized_path)
        )

    return normalized_path


def open_scene(file_path, force=False, ignore_version=True):
    """
    打开 Maya Scene。

    当 Scene 有未保存修改且 force=False 时不弹 UI，而是抛出错误，
    由上层 Tool / App 决定是否向用户询问确认。
    """
    normalized_path = validate_scene_file(file_path)

    if is_scene_modified() and not force:
        raise RuntimeError(
            u"当前场景存在未保存修改，请确认后使用 force=True 打开新场景。"
        )

    cmds.file(
        normalized_path,
        open=True,
        ignoreVersion=ignore_version,
        force=force
    )

    return normalized_path


def import_scene(file_path, ignore_version=True):
    """把 Maya Scene 导入当前场景。"""
    normalized_path = validate_scene_file(file_path)

    imported_nodes = cmds.file(
        normalized_path,
        i=True,
        ignoreVersion=ignore_version,
        returnNewNodes=True
    )

    if imported_nodes is None:
        imported_nodes = []

    return imported_nodes


def reference_scene(
        file_path,
        namespace=None,
        group_reference=False,
        group_name=None,
        ignore_version=True
):
    """
    在当前 Maya Scene 中创建 Reference。

    namespace 未给定时使用文件名 Stem。
    """
    normalized_path = validate_scene_file(file_path)

    if namespace is None:
        namespace = file_utils.get_file_stem(normalized_path)

    reference_kwargs = {
        "reference": True,
        "ignoreVersion": ignore_version,
        "namespace": namespace,
        "returnNewNodes": False,
    }

    if group_reference:
        reference_kwargs["groupReference"] = True

        if group_name:
            reference_kwargs["groupName"] = group_name

    reference_node = cmds.file(
        normalized_path,
        **reference_kwargs
    )

    return reference_node


def ensure_fbx_plugin_loaded():
    """确保 Maya FBX 插件已加载。"""
    plugin_name = "fbxmaya"

    if cmds.pluginInfo(
            plugin_name,
            query=True,
            loaded=True
    ):
        return True

    try:
        cmds.loadPlugin(plugin_name)
    except RuntimeError as error:
        raise RuntimeError(
            u"无法加载 FBX 插件：{}".format(error)
        )

    return True


def export_selected_fbx(file_path):
    """把当前 Maya 选择导出为 FBX 文件。"""
    selected_nodes = cmds.ls(
        selection=True,
        long=True
    )

    if selected_nodes is None:
        selected_nodes = []

    if not selected_nodes:
        raise RuntimeError(u"导出 FBX 前请先选择对象。")

    normalized_path = file_utils.normalize_path(file_path)

    if not normalized_path:
        raise ValueError(u"file_path 不能为空。")

    parent_directory = os.path.dirname(normalized_path)

    if parent_directory:
        file_utils.ensure_directory(parent_directory)

    ensure_fbx_plugin_loaded()

    mel.eval(
        'FBXExport -f "{}" -s'.format(normalized_path)
    )

    return normalized_path


__all__ = [
    "get_current_scene_path",
    "is_scene_modified",
    "validate_scene_file",
    "open_scene",
    "import_scene",
    "reference_scene",
    "ensure_fbx_plugin_loaded",
    "export_selected_fbx",
]
