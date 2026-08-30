# coding=utf-8
u"""
Mesh Utils
==========

Maya Mesh / Model 通用底层工具。

模块职责
--------
本模块负责和“模型 Transform / Mesh 副本”直接相关的轻量底层操作。
当前模块刻意保持很小，避免把 Skin、BlendShape、Model Check 等职责重新混在一起。

公开方法
--------
validate_node(node, label=u"节点")
    检查 Maya 节点是否存在，并在失败时提供更明确的中文错误信息。

duplicate_model(source_model, new_name, parent=None)
    复制一个独立模型 Transform，可选整理到指定父层级。

典型使用场景
------------
1. Face Setup 生成 Head / Mouth 等工作模型副本；
2. Rig Build 需要保留一份独立 Model 作为 Deformation / Tweak / Reference 使用；
3. 上层 System 需要复制模型，但不希望复制输入连接和上游历史网络。

设计边界
--------
- SkinCluster 操作放在 skin_utils.py；
- BlendShape / Corrective 放在 blendshape_utils.py；
- 模型规范检查放在 model_check_utils.py；
- 场景清理放在 scene_clean_utils.py；
- 本模块不读取 UI Selection，也不创建任何工具窗口。

依赖
----
只依赖 maya.cmds，不依赖 PyMel、Tools、Systems 或 UI。
"""

from __future__ import print_function

import maya.cmds as cmds


# =============================================================================
# Validate
# =============================================================================

def validate_node(node, label=u"节点"):
    u"""
    检查 Maya 节点是否存在。

    Args:
        node (str):
            需要验证的 Maya 节点。
        label (str):
            错误信息中使用的中文说明，例如“源模型”“父节点”。

    Returns:
        bool:
        验证通过返回 True。

    Raises:
        RuntimeError:
        节点名称为空或场景中不存在时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：先判断调用者有没有提供节点名称。
    # -------------------------------------------------------------------------
    if not node:
        raise RuntimeError(
            u"{}不能为空。".format(label)
        )

    # -------------------------------------------------------------------------
    # 步骤 2：确认 Maya 场景中确实存在该节点。
    # -------------------------------------------------------------------------
    if not cmds.objExists(node):
        raise RuntimeError(
            u"{}不存在：{}".format(
                label,
                node
            )
        )

    return True


# =============================================================================
# Duplicate Model
# =============================================================================

def duplicate_model(
        source_model,
        new_name,
        parent=None
):
    u"""
    复制一个独立的 Maya DAG 模型并整理父层级。

    Args:
        source_model (str):
            源模型 Transform。
        new_name (str):
            新模型名称。
        parent (str/None):
            可选父节点。给定时会在复制完成后重新 Parent。

    Returns:
        str:
        最终复制模型节点名称。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。

    Notes:
        这里明确关闭 inputConnections / upstreamNodes，目的是得到相对独立的模型副本，
                避免把旧 Rig / Deformer / DG 输入网络一起复制到新的工作模型上。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：验证源模型。
    # -------------------------------------------------------------------------
    validate_node(
        source_model,
        label=u"源模型"
    )

    if not new_name:
        raise RuntimeError(u"新模型名称不能为空。")

    # -------------------------------------------------------------------------
    # 步骤 2：如果要求整理到指定层级，先确认 Parent 有效。
    # -------------------------------------------------------------------------
    if parent:
        validate_node(
            parent,
            label=u"父节点"
        )

    # -------------------------------------------------------------------------
    # 步骤 3：正式创建前检查目标名称。
    #
    # 为什么不让 Maya 自动加数字后缀：
    # Rig 构建依赖稳定命名。静默得到 xxx1 / xxx2 很容易让后续查找错误节点。
    # -------------------------------------------------------------------------
    if cmds.objExists(new_name):
        raise RuntimeError(
            u"目标名称已经存在：{}".format(new_name)
        )

    # -------------------------------------------------------------------------
    # 步骤 4：复制模型根节点，并明确不要复制输入 DG 网络和上游节点。
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 5：根据调用者要求整理父层级。
    #
    # cmds.parent 可能返回新的 DAG Path，所以后续统一使用 Maya 返回值，而不是继续使用
    # Parent 前的旧路径。
    # -------------------------------------------------------------------------
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
