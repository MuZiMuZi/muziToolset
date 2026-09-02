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
scene_utils.validate_node(node, label=u"节点")
    兼容旧调用的基础节点存在性检查。

validate_model_transform(node, label=u"模型")
    检查模型节点是否存在、名称是否唯一，并确认它是 Transform。

 delete_model(model, ignore_missing=True)
    安全删除一个模型 Transform；短名称不唯一时拒绝猜测。

duplicate_model(source_model, new_name, parent=None)
    复制一个独立模型 Transform，可选整理到指定父层级。

典型使用场景
------------
1. Face Setup 验证 Head / Eye / Teeth 等模型输入；
2. Face Setup 生成 Head 工作模型副本；
3. Rig Build 需要保留一份独立 Model 作为 Deformation / Tweak / Reference 使用；
4. 上层 System 需要复制或删除模型，但不希望直接重复 Maya cmds 校验逻辑。

设计边界
--------
- Maya 节点是否存在、DAG 名称是否唯一的基础规则由 scene_utils 提供；
- 本模块在此基础上补充“模型 Transform”语义；
- SkinCluster 操作放在 skin_utils.py；
- BlendShape / Corrective 放在 blendshape_utils.py；
- 模型规范检查放在 model_check_utils.py；
- 场景整体清理放在 scene_clean_utils.py；
- 本模块不读取 UI Selection，也不创建任何工具窗口。

依赖
----
只依赖 maya.cmds 和 core.scene_utils，不依赖 PyMel、Tools、Systems 或 UI。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import scene_utils


# =============================================================================
# Validate
# =============================================================================


def validate_model_transform(node, label=u"模型"):
    u"""
    检查一个节点是否可以安全作为模型 Transform 使用。

    检查内容：
        1. 名称不能为空；
        2. 节点必须存在；
        3. 短名称如果对应多个 DAG 节点则拒绝猜测；
        4. 节点类型必须严格为 transform。

    Args:
        node (str):
            模型 Transform 名称，可以是唯一短名称或 Long DAG Path。
        label (str):
            错误信息中使用的业务说明。

    Returns:
        str:
        唯一解析后的 Long DAG Path。

    Raises:
        RuntimeError:
        节点不存在、名称不唯一或节点类型不是 transform 时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not node:
        raise RuntimeError(
            u"{}不能为空。".format(label)
        )

    # -------------------------------------------------------------------------
    # Step 02：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        long_name = scene_utils.get_long_name(
            node
        )
    except RuntimeError as error:
        raise RuntimeError(
            u"{}无效：{}".format(
                label,
                error
            )
        )

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    node_type = cmds.nodeType(
        long_name
    )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if node_type != "transform":
        raise RuntimeError(
            u"{}必须是 Transform：{} | type={}".format(
                label,
                node,
                node_type
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return long_name


# =============================================================================
# Delete Model
# =============================================================================

def delete_model(model, ignore_missing=True):
    u"""
    安全删除一个模型 Transform。

    Args:
        model (str | None):
            需要删除的模型 Transform。
        ignore_missing (bool):
            True 时，空值或不存在的节点直接返回 False； False 时按照正式校验规则抛出异常。

    Returns:
        bool:
        实际删除节点时返回 True；没有节点可删时返回 False。

    Raises:
        RuntimeError:
        名称不唯一、节点不是 Transform，或 ignore_missing=False 且节点不存在时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not model:
        if ignore_missing:
            return False

        raise RuntimeError(
            u"需要删除的模型不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not cmds.objExists(model):
        if ignore_missing:
            return False

        raise RuntimeError(
            u"需要删除的模型不存在：{}".format(
                model
            )
        )

    # -------------------------------------------------------------------------
    # Step 03：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    long_name = validate_model_transform(
        model,
        label=u"需要删除的模型"
    )

    # -------------------------------------------------------------------------
    # Step 04：清理当前阶段不再需要的数据或场景状态
    # -------------------------------------------------------------------------
    cmds.delete(
        long_name
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
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
        parent (str | None):
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
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    source_model = validate_model_transform(
        source_model,
        label=u"源模型"
    )

    if not new_name:
        raise RuntimeError(
            u"新模型名称不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if parent:
        scene_utils.validate_node(
            parent,
            label=u"父节点"
        )

    if cmds.objExists(new_name):
        raise RuntimeError(
            u"目标名称已经存在：{}".format(
                new_name
            )
        )

    # -------------------------------------------------------------------------
    # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
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
            u"复制模型失败：{}".format(
                source_model
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    duplicated_model = duplicate_result[0]

    if parent:
        parent_result = cmds.parent(
            duplicated_model,
            parent
        )

        if parent_result:
            duplicated_model = parent_result[0]

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return duplicated_model


__all__ = [
    "validate_model_transform",
    "delete_model",
    "duplicate_model",
]
