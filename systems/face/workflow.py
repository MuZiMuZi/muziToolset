# coding=utf-8
u"""
Face Workflow State
===================

Face Rig 四步工作流的场景显示状态管理。

职责：
    1. 根据当前查看的 Step 统一切换 Face 功能组 Visibility；
    2. Step 02 只在 Guide 页面显示 Guide Group；
    3. 为后续 Step 03 / Step 04 保留统一的显示规则入口；
    4. 不保存 Rig 数据，不复制 FaceBase 的 Config CRUD。

设计原则：
    - Workflow Progress 由 FaceBase / Config Node 持久化；
    - 当前 UI 查看页面可以暂时和 Workflow Progress 不同；
    - Scene Visibility 跟随当前 UI 查看页面；
    - 显示切换只处理 Face System 自己管理的顶层功能组。
"""

from __future__ import print_function

import maya.cmds as cmds


# =============================================================================
# Step Visibility Contract
# =============================================================================

# 每个 Step 只描述 Face 功能组的显示意图。
# Model Group 在四个 Step 中都保持显示，方便定位和检查面部结果。
step_visibility_rules = {
    1: {
        "face_model_grp": True,
        "face_guide_grp": False,
        "face_ctrl_grp": False,
        "face_jnt_grp": False,
        "face_rig_nodes_grp": False,
        "face_pos_driver_grp": False,
    },
    2: {
        "face_model_grp": True,
        "face_guide_grp": True,
        "face_ctrl_grp": False,
        "face_jnt_grp": False,
        "face_rig_nodes_grp": False,
        "face_pos_driver_grp": False,
    },
    3: {
        "face_model_grp": True,
        "face_guide_grp": False,
        "face_ctrl_grp": True,
        "face_jnt_grp": True,
        "face_rig_nodes_grp": False,
        "face_pos_driver_grp": False,
    },
    4: {
        "face_model_grp": True,
        "face_guide_grp": False,
        "face_ctrl_grp": True,
        "face_jnt_grp": False,
        "face_rig_nodes_grp": False,
        "face_pos_driver_grp": False,
    },
}


def set_node_visibility(node, visible):
    u"""
    设置一个 Maya DAG 节点的 Visibility，并保留原来的 Lock 状态。

    Args:
        node (str):
            需要切换显示状态的 Maya DAG 节点。
        visible (bool):
            是否显示节点。

    Returns:
        bool:
            成功设置返回 True；节点不存在或无法设置时返回 False。
    """
    if not node:
        return False

    if not cmds.objExists(node):
        return False

    plug = "{}.visibility".format(
        node
    )

    if not cmds.objExists(plug):
        return False

    try:
        was_locked = cmds.getAttr(
            plug,
            lock=True
        )
    except Exception:
        return False

    if was_locked:
        cmds.setAttr(
            plug,
            lock=False
        )

    try:
        cmds.setAttr(
            plug,
            bool(visible)
        )
    except Exception:
        return False
    finally:
        if was_locked:
            cmds.setAttr(
                plug,
                lock=True
            )

    return True


def apply_step_scene_visibility(
        face_context,
        step_value
):
    u"""
    根据当前 UI Step 应用 Face System 顶层功能组的显示状态。

    Args:
        face_context (FaceBase):
            当前 Face System 上下文，需要提供 Face 顶层 Group 名称。
        step_value (int):
            当前 UI 查看 Step，范围 1～4。

    Returns:
        dict:
            group attribute name -> bool，记录本次实际执行结果。
    """
    if face_context is None:
        raise ValueError(
            u"face_context 不能为空。"
        )

    if step_value not in step_visibility_rules:
        raise ValueError(
            u"Face Step Visibility 只支持 Step 01～04。"
        )

    visibility_rule = step_visibility_rules.get(
        step_value
    )
    result = {}

    for group_attr_name in visibility_rule:
        visible = visibility_rule.get(
            group_attr_name
        )
        group_name = getattr(
            face_context,
            group_attr_name,
            None
        )

        result[group_attr_name] = set_node_visibility(
            group_name,
            visible
        )

    return result


__all__ = [
    "step_visibility_rules",
    "set_node_visibility",
    "apply_step_scene_visibility",
]
