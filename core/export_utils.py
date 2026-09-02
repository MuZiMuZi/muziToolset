# coding=utf-8
u"""
Export Utils
============

Maya 文件格式导出通用底层工具。

模块职责
--------
当前模块负责显式对象列表的文件格式导出。

目前正式支持：
    - FBX Export。

模块边界
--------
    当前 Maya Scene / Selection 查询 -> scene_utils
    硬盘 Path / Directory             -> file_utils
    FBX / Alembic / USD 等格式导出    -> export_utils

设计原则
--------
1. 正式导出 API 接收明确 objects，不依赖当前用户 Selection；
2. 导出过程中可以临时修改 Maya Selection，但结束后必须恢复；
3. Plugin 加载与文件格式命令保留在本模块；
4. Tool 负责文件选择窗口和用户提示。
"""

from __future__ import print_function

import os

import maya.cmds as cmds
import maya.mel as mel

from . import file_utils
from . import scene_utils


def ensure_fbx_plugin_loaded():
    u"""

        确保 Maya FBX Plugin ``fbxmaya`` 已加载。

        Returns:
            bool:
                当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。

    """
    plugin_name = "fbxmaya"

    if cmds.pluginInfo(
            plugin_name,
            query=True,
            loaded=True
    ):
        return True

    try:
        cmds.loadPlugin(
            plugin_name
        )
    except RuntimeError as error:
        raise RuntimeError(
            u"无法加载 FBX 插件：{}".format(
                error
            )
        )

    return True


def export_fbx(
        objects,
        file_path
):
    u"""
    把明确给定的 Maya Node 导出为 FBX，并恢复调用前 Selection。

    Args:
        objects (str | list[str]):
            需要导出的 Maya Node。
        file_path (str):
            最终 FBX 文件路径。

    Returns:
        str:
        规范化后的最终输出路径。

    Raises:
        ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not objects:
        raise ValueError(
            u"objects 不能为空。"
        )

    if isinstance(objects, str):
        objects = [
            objects
        ]

    export_objects = []

    # -------------------------------------------------------------------------
    # Step 02：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for scene_object in objects:
        if not scene_object:
            continue

        scene_utils.validate_node(
            scene_object
        )

        export_objects.append(
            scene_object
        )

    if not export_objects:
        raise ValueError(
            u"没有可导出的 Maya Node。"
        )

    normalized_path = file_utils.normalize_path(
        file_path
    )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not normalized_path:
        raise ValueError(
            u"file_path 不能为空。"
        )

    parent_directory = os.path.dirname(
        normalized_path
    )

    if parent_directory:
        file_utils.ensure_directory(
            parent_directory
        )

    # -------------------------------------------------------------------------
    # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    ensure_fbx_plugin_loaded()

    previous_selection = scene_utils.get_selected_nodes(
        long=True,
        flatten=False
    )

    try:
        cmds.select(
            export_objects,
            replace=True
        )

        escaped_path = normalized_path.replace(
            '"',
            '\\"'
        )

        mel.eval(
            'FBXExport -f "{}" -s'.format(
                escaped_path
            )
        )
    finally:
        if previous_selection:
            cmds.select(
                previous_selection,
                replace=True
            )
        else:
            cmds.select(
                clear=True
            )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return normalized_path


__all__ = [
    "ensure_fbx_plugin_loaded",
    "export_fbx",
]
