# coding=utf-8
"""animation_utils：供工具 UI 调用的 Maya 操作。"""

from __future__ import print_function
import maya.cmds as cmds
from ..common import file_utils

format_version = 1

format_name = "muzi_animation"

anim_curve_types = [
    "animCurveTA",
    "animCurveTL",
    "animCurveTT",
    "animCurveTU",
]

def get_animation_curves(nodes=None):
    u"""
    获取 AnimCurve 节点。

    Args:
        nodes (list/str/None):
            None：查询整个 Maya 场景中的 AnimCurve； str：查询一个节点的输入动画曲线； list：查询多个节点的输入动画曲线。

    Returns:
        list: 去重后的 AnimCurve 节点列表。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    result = []

    # -------------------------------------------------------------------------
    # 步骤 1：没有指定节点时，按 AnimCurve 类型扫描整个场景。
    #
    # 这样保留了早期 Pipeline.clear_keys() 的全场景使用习惯，
    # 但“查询”和“删除”现在已经拆开，调用方可以先检查结果再决定是否清理。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if nodes is None:
        for anim_curve_type in anim_curve_types:
            curves = cmds.ls(
                type=anim_curve_type,
                long=True
            )

            if curves is None:
                curves = []

            for curve in curves:
                if curve in result:
                    continue

                result.append(curve)

        return result

    # -------------------------------------------------------------------------
    # 步骤 2：统一输入数据结构。
    # 单个字符串转成 list，后面的 Maya 查询只需要维护一套循环。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if isinstance(nodes, str):
        nodes = [nodes]

    # -------------------------------------------------------------------------
    # 步骤 3：逐个节点查询输入 AnimCurve，并去重。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        for anim_curve_type in anim_curve_types:
            curves = cmds.listConnections(
                node,
                source=True,
                destination=False,
                type=anim_curve_type
            )

            if curves is None:
                curves = []

            for curve in curves:
                if curve in result:
                    continue

                result.append(curve)

    # -------------------------------------------------------------------------
    # 步骤 4：返回纯数据结果，不在 Core 中修改 Selection 或弹出窗口。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result

def clear_animation_keys(nodes=None):
    u"""
    删除 AnimCurve，并返回实际删除的曲线节点名称。

    Args:
        nodes (list/str/None):
            None 时删除全场景 AnimCurve； 给定节点时只删除这些节点的输入 AnimCurve。

    Returns:
        list: 实际删除的 AnimCurve 名称。

    Notes:
        这个函数的语义是“删除动画曲线节点”。
                                                                            如果以后需要只删除某一个时间范围的 Key，应新增独立 API，
                                                                            不要让一个函数同时承担两种不同的清理行为。
    """
    # 步骤 1：先查询需要删除的曲线。
    animation_curves = get_animation_curves(
        nodes=nodes
    )

    deleted_curves = []

    # 步骤 2：逐条确认节点仍存在，然后删除。
    for animation_curve in animation_curves:
        if not cmds.objExists(animation_curve):
            continue

        deleted_curves.append(animation_curve)
        cmds.delete(animation_curve)

    # 步骤 3：返回删除记录，方便 Tool 和 Smoke Test 使用。
    return deleted_curves
