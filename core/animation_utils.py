# coding=utf-8
u"""
Animation Utils
===============

Maya 动画与绑定控制器的基础动画操作。

从旧 pipelineUtils 中拆出的职责：
    - 清除 AnimCurve；
    - 重置 Transform 标准通道；
    - 批量重置控制器。

说明：
    - 不依赖 UI；
    - 不硬编码某一个角色的 IK/FK 自定义属性；
    - 只修改未锁定并且当前可设置的属性。
"""

from __future__ import print_function

import maya.cmds as cmds


anim_curve_types = [
    "animCurveTA",
    "animCurveTL",
    "animCurveTT",
    "animCurveTU",
]


# =============================================================================
# Anim Curve
# =============================================================================

def get_animation_curves(nodes=None):
    """
    获取 AnimCurve 节点。

    Args:
        nodes(list/str/None):
            None 时返回全场景 AnimCurve；
            给定节点时只查询这些节点的输入动画曲线。
    """
    result = []

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

    if isinstance(nodes, str):
        nodes = [nodes]

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

    return result


def clear_animation_keys(nodes=None):
    """
    删除 AnimCurve，并返回实际删除的节点名称。

    nodes=None 时等同于旧 Pipeline.clear_keys() 的全场景行为。
    """
    animation_curves = get_animation_curves(
        nodes=nodes
    )

    deleted_curves = []

    for animation_curve in animation_curves:
        if not cmds.objExists(animation_curve):
            continue

        deleted_curves.append(
            animation_curve
        )

        cmds.delete(
            animation_curve
        )

    return deleted_curves


# =============================================================================
# Reset Transform
# =============================================================================

def can_set_attribute(attribute):
    """判断属性存在、未锁定并且当前可直接设置。"""
    if not cmds.objExists(attribute):
        return False

    try:
        if cmds.getAttr(attribute, lock=True):
            return False

        if not cmds.getAttr(attribute, settable=True):
            return False
    except Exception:
        return False

    return True


def reset_transform_channels(
        nodes,
        translate=True,
        rotate=True,
        scale=True
):
    """
    把给定 Transform 的标准 TRS 通道恢复默认值。

    Returns:
        list: 成功修改过至少一个属性的节点。
    """
    if isinstance(nodes, str):
        nodes = [nodes]

    if nodes is None:
        nodes = []

    reset_nodes = []

    zero_attributes = []
    one_attributes = []

    if translate:
        zero_attributes.append("translateX")
        zero_attributes.append("translateY")
        zero_attributes.append("translateZ")

    if rotate:
        zero_attributes.append("rotateX")
        zero_attributes.append("rotateY")
        zero_attributes.append("rotateZ")

    if scale:
        one_attributes.append("scaleX")
        one_attributes.append("scaleY")
        one_attributes.append("scaleZ")

    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        changed = False

        for attribute_name in zero_attributes:
            attribute = "{}.{}".format(
                node,
                attribute_name
            )

            if not can_set_attribute(attribute):
                continue

            cmds.setAttr(
                attribute,
                0
            )
            changed = True

        for attribute_name in one_attributes:
            attribute = "{}.{}".format(
                node,
                attribute_name
            )

            if not can_set_attribute(attribute):
                continue

            cmds.setAttr(
                attribute,
                1
            )
            changed = True

        if changed:
            reset_nodes.append(node)

    return reset_nodes


def reset_controls(
        controls=None,
        pattern="ctrl_*"
):
    """
    批量重置控制器标准 TRS。

    controls=None 时按命名 Pattern 从场景查找控制器。
    不再保留旧 pipelineUtils 中针对某一个 IKFK 属性的硬编码。
    """
    if controls is None:
        controls = cmds.ls(
            pattern,
            type="transform",
            long=True
        )

        if controls is None:
            controls = []

    return reset_transform_channels(
        nodes=controls,
        translate=True,
        rotate=True,
        scale=True
    )


__all__ = [
    "anim_curve_types",
    "get_animation_curves",
    "clear_animation_keys",
    "can_set_attribute",
    "reset_transform_channels",
    "reset_controls",
]
