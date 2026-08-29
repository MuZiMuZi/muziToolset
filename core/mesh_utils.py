# coding=utf-8
u"""
Mesh Utils
==========

Maya Mesh / Model 通用底层工具。

本模块只使用 maya.cmds，不依赖 UI、Tools、Systems 或 PyMel。
"""

from __future__ import print_function

import maya.cmds as cmds


def validate_node(node, label=u"节点"):
    """检查 Maya 节点是否存在。"""
    if not node:
        raise RuntimeError(
            u"{}不能为空。".format(label)
        )

    if not cmds.objExists(node):
        raise RuntimeError(
            u"{}不存在：{}".format(
                label,
                node
            )
        )

    return True


def duplicate_model(
        source_model,
        new_name,
        parent=None
):
    """复制一个独立的 Maya DAG 模型并整理父层级。

    Args:
        source_model (str): 源模型 Transform。
        new_name (str): 新模型名称。
        parent (str or None): 可选父节点。

    Returns:
        str: 新模型节点名称。
    """
    validate_node(
        source_model,
        label=u"源模型"
    )

    if not new_name:
        raise RuntimeError(u"新模型名称不能为空。")

    if parent:
        validate_node(
            parent,
            label=u"父节点"
        )

    if cmds.objExists(new_name):
        raise RuntimeError(
            u"目标名称已经存在：{}".format(new_name)
        )

    duplicate_result = cmds.duplicate(
        source_model,
        name=new_name,
        returnRootsOnly=True,
        inputConnections=False,
        upstreamNodes=False
    )

    if not duplicate_result:
        raise RuntimeError(
            u"复制模型失败：{}".format(source_model)
        )

    duplicated_model = duplicate_result[0]

    if parent:
        parent_result = cmds.parent(
            duplicated_model,
            parent
        )

        if parent_result:
            duplicated_model = parent_result[0]

    return duplicated_model


__all__ = [
    "validate_node",
    "duplicate_model",
]
