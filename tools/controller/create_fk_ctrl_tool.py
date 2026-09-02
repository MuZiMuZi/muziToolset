# coding=utf-8
u"""
FK Control Creator
==================

根据 Maya 当前选择顺序创建 FK Controller Chain。

实际控制器创建统一使用 systems.ctrl_base；
Rig Name 统一使用 systems.rig_base.RigBase；
外部 Maya Name Token 和 Selection 查询统一复用 Core。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import rename_utils
from ...core import scene_utils
from ...systems import ctrl_base
from ...systems.rig_base import RigBase


TOOL_MODE = "action"


def get_fk_ctrl_name(target, fallback_index):
    u"""

        根据 Target 名称生成标准 FK Ctrl Name。

        Args:
            target (str):
                接收结果或被处理的目标 Maya 节点名称。
            fallback_index (int):
                对应 Maya Array Attribute、Target、Guide 或构建元素的逻辑索引。

        Returns:
            object:
                当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    short_name = rename_utils.get_short_name(
        target
    )

    try:
        target_name = RigBase(
            name=short_name
        )
        return target_name.create_name(
            type="ctrl"
        )
    except (IndexError, ValueError):
        pass

    rig_name = RigBase(
        type="ctrl",
        side="md",
        part=rename_utils.get_name_token(
            short_name,
            fallback="fk"
        ),
        function="fk",
        index=fallback_index
    )

    return rig_name.name


def create_fk_controls(
        targets,
        shape="circle",
        radius=1.0,
        axis="Y+",
        constrain=True
):
    u"""

        使用 CtrlBase 创建标准 FK Controller Chain。

        Args:
            targets (str | list[str]):
                需要批量处理的 Target 节点；在 Constraint / BlendShape / Controller API 中保持输入顺序。
            shape (str):
                Controller、Curve 或 Geometry 的 Shape 节点 / Shape 名称。
            radius (float):
                创建节点或控制器使用的半径值。
            axis (str):
                操作使用的轴向标记。
            constrain (bool):
                创建 Controller 后是否建立 Controller / Output 到 Target 的约束关系。

        Returns:
            object | list:
                按当前 API 约定顺序返回的结果列表。

    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not targets:
        return []

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    ctrl_name_list = []
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    target_index = 0

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    while target_index < len(targets):
        ctrl_name = get_fk_ctrl_name(
            targets[target_index],
            target_index + 1
        )
        ctrl_name_list.append(
            ctrl_name
        )
        target_index += 1

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return ctrl_base.create_fk_ctrl(
        target_list=targets,
        ctrl_name_list=ctrl_name_list,
        shape=shape,
        radius=radius,
        axis=axis,
        constrain=constrain,
        add_to_set=True
    )


def main():
    u"""

        按当前 Maya 选择顺序创建 FK Controller Chain。

        Returns:
            object | list:
                按当前 API 约定顺序返回的结果列表。

    """
    selections = scene_utils.get_selected_nodes(
        long=True,
        flatten=True
    )

    if not selections:
        cmds.warning(
            u"请选择多个物体或 Joint 后再创建 FK 控制器。"
        )
        return []

    return create_fk_controls(
        targets=selections,
        shape="circle",
        radius=1.0,
        axis="Y+",
        constrain=True
    )


__all__ = [
    "create_fk_controls",
    "get_fk_ctrl_name",
    "main",
]
