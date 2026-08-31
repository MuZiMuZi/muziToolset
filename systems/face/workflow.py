# coding=utf-8
u"""
Face Workflow State
===================

Face Rig 四步工作流的场景显示状态管理。

职责：
    1. 根据当前查看的 Step 统一切换 Face 功能组 Visibility；
    2. 根据当前 Step 控制 Face Model Group 内部模型分支的显示；
    3. Step 01 / Step 02 只显示 Setup 中明确指定的输入模型；
    4. Step 02 只在 Guide 页面显示 Guide Group；
    5. 为后续 Step 03 / Step 04 保留统一的显示规则入口；
    6. 不保存 Rig 数据，不复制 FaceBase 的 Config CRUD。

设计原则：
    - Workflow Progress 由 FaceBase / Config Node 持久化；
    - 当前 UI 查看页面可以暂时和 Workflow Progress 不同；
    - Scene Visibility 跟随当前 UI 查看页面；
    - 显示切换只处理 Face System 自己管理的节点；
    - 当前 Step 只显示当前工作真正需要观察和选择的内容；
    - Step 03 / Step 04 的模型显示规则在正式 Build / Finalize 内容确定后继续扩展。
"""

from __future__ import print_function

import maya.cmds as cmds


# =============================================================================
# Step Visibility Contract
# =============================================================================

# 每个 Step 描述 Face 顶层功能组的显示意图。
# Model Group 顶层保持显示，内部模型由 step_model_display_rules 进一步过滤。
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


# Model Group 内部使用独立规则。
# setup_sources：只显示 Step 01 保存到 Config 的模型分支。
# preserve：暂时保留上一 Step 的内部显示状态；正式 Step 内容确定后再定义专属规则。
step_model_display_rules = {
    1: "setup_sources",
    2: "setup_sources",
    3: "preserve",
    4: "preserve",
}


# =============================================================================
# Common Visibility
# =============================================================================

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


def get_long_node(node):
    u"""返回唯一 Maya DAG Long Name；无法唯一解析时返回 None。"""
    if not node:
        return None

    matches = cmds.ls(
        node,
        long=True
    )

    if matches is None:
        matches = []

    if len(matches) != 1:
        return None

    return matches[0]


# =============================================================================
# Setup Source Model Visibility
# =============================================================================

def get_setup_source_models(face_context):
    u"""
    从 Face Config 获取 Step 01 正式保存的输入模型。

    Returns:
        list[str]:
            当前仍然存在于场景中的 Setup 输入模型。
    """
    source_models = []

    if face_context is None:
        return source_models

    if not face_context.config_node_exists():
        return source_models

    try:
        setup_data = face_context.get_setup_data(
            refresh=True
        )
    except Exception:
        return source_models

    for attr_name in face_context.setup_message_attr_names:
        model = setup_data.get(
            attr_name
        )

        if not model:
            continue

        if not cmds.objExists(model):
            continue

        source_models.append(
            model
        )

    return source_models


def get_model_root_children(face_context):
    u"""获取 Face Model Group 下第一层 Transform 分支。"""
    if face_context is None:
        return []

    model_root = face_context.face_model_grp

    if not model_root:
        return []

    if not cmds.objExists(model_root):
        return []

    children = cmds.listRelatives(
        model_root,
        children=True,
        type="transform",
        fullPath=True
    )

    if children is None:
        children = []

    return children


def get_model_branch_under_root(
        face_context,
        node
):
    u"""
    返回某个模型在 Face Model Group 下所属的第一层分支。

    例如：
        grp_md_face_model_001
            -> grp_md_face_tweak_001
                -> model_xxx

    对 model_xxx 调用时返回 grp_md_face_tweak_001。
    如果模型本身就是 Face Model Group 的直接子节点，则返回模型本身。
    """
    if face_context is None:
        return None

    model_root = get_long_node(
        face_context.face_model_grp
    )
    current_node = get_long_node(
        node
    )

    if not model_root or not current_node:
        return None

    if current_node == model_root:
        return None

    while current_node:
        parents = cmds.listRelatives(
            current_node,
            parent=True,
            fullPath=True
        )

        if parents is None:
            parents = []

        if not parents:
            return None

        parent = parents[0]

        if parent == model_root:
            return current_node

        current_node = parent

    return None


def apply_setup_source_model_visibility(face_context):
    u"""
    只显示 Step 01 Config 中明确指定的模型分支。

    这会自动隐藏 Tweak / Stretch / Deform Work Model Group，以及任何没有被
    Step 01 Config 引用的其它 Face Model 顶层分支，方便 Guide 阶段选择 Locator。

    如果旧场景没有可恢复的 Setup Model，则保持当前模型显示状态，避免误隐藏全部模型。
    """
    source_models = get_setup_source_models(
        face_context
    )

    result = {
        "applied": False,
        "source_models": source_models,
        "visible_branches": [],
        "hidden_branches": [],
    }

    if not source_models:
        return result

    model_children = get_model_root_children(
        face_context
    )
    visible_branches = []

    for source_model in source_models:
        branch = get_model_branch_under_root(
            face_context,
            source_model
        )

        if not branch:
            continue

        if branch in visible_branches:
            continue

        visible_branches.append(
            branch
        )

    for model_child in model_children:
        visible = model_child in visible_branches

        set_node_visibility(
            model_child,
            visible
        )

        if visible:
            result["visible_branches"].append(
                model_child
            )
        else:
            result["hidden_branches"].append(
                model_child
            )

    # Setup Model 自己如果曾被手工隐藏，也恢复为可见。
    for source_model in source_models:
        set_node_visibility(
            source_model,
            True
        )

    result["applied"] = True
    return result


def apply_step_model_visibility(
        face_context,
        step_value
):
    u"""应用当前 Step 对 Face Model Group 内部模型的显示规则。"""
    display_mode = step_model_display_rules.get(
        step_value,
        "preserve"
    )

    if display_mode == "setup_sources":
        return apply_setup_source_model_visibility(
            face_context
        )

    return {
        "applied": False,
        "mode": display_mode,
    }


# =============================================================================
# Step Visibility
# =============================================================================

def apply_step_scene_visibility(
        face_context,
        step_value
):
    u"""
    根据当前 UI Step 应用 Face System 顶层功能组和模型内部显示状态。

    Args:
        face_context (FaceBase):
            当前 Face System 上下文，需要提供 Face 顶层 Group 名称。
        step_value (int):
            当前 UI 查看 Step，范围 1～4。

    Returns:
        dict:
            本次顶层功能组和 Model Display Rule 的执行结果。
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
    result = {
        "groups": {},
        "models": {},
    }

    # 步骤 1：先控制 Guide / Ctrl / Joint 等 Face 顶层功能组。
    for group_attr_name in visibility_rule:
        visible = visibility_rule.get(
            group_attr_name
        )
        group_name = getattr(
            face_context,
            group_attr_name,
            None
        )

        result["groups"][group_attr_name] = set_node_visibility(
            group_name,
            visible
        )

    # 步骤 2：再根据当前 Step 过滤 Face Model Group 内部具体模型分支。
    result["models"] = apply_step_model_visibility(
        face_context,
        step_value
    )

    return result


__all__ = [
    "step_visibility_rules",
    "step_model_display_rules",
    "set_node_visibility",
    "get_setup_source_models",
    "get_model_root_children",
    "get_model_branch_under_root",
    "apply_setup_source_model_visibility",
    "apply_step_model_visibility",
    "apply_step_scene_visibility",
]
