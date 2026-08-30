# coding=utf-8
u"""
Controller Space Blend
======================

控制器 Parent Space / Follow 混合系统。

从旧 pipelineUtils.create_doble_constraint() 的思路重构而来。

职责：
    1. 使用外部 Driver 和 Controller Zero 共同驱动 Driven Group；
    2. 在控制器上创建 0-1 Follow 属性；
    3. 自动创建反向权重；
    4. 不依赖旧 Pipeline / PyMel。

标准控制器层级：

    zero
      driven
        space
          connect
            offset
              ctrl

Follow = 1：完全跟随外部 Driver。
Follow = 0：保持在 Zero Space。
"""

from __future__ import print_function

import maya.cmds as cmds


# =============================================================================
# Name
# =============================================================================

def get_short_name(node):
    u"""
    返回 DAG 短名称。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return node.split("|")[-1]


def replace_control_prefix(control, prefix):
    u"""
    根据 ctrl_ 名称生成同层级约定名称。

    Args:
        control (str):
            需要处理的控制器 Transform 名称。
        prefix (str):
            添加到 Maya 节点名称前部的 Prefix。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    short_name = get_short_name(control)

    if not short_name.startswith("ctrl_"):
        raise RuntimeError(
            u"控制器名称必须以 ctrl_ 开头：{}".format(control)
        )

    return short_name.replace(
        "ctrl_",
        prefix + "_",
        1
    )


# =============================================================================
# Validate
# =============================================================================

def validate_node(node, label):
    u"""
    检查必要 Maya 节点。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。
        label (str):
            UI、Rig Node 或日志中展示的简短 Label。

    Returns:
        bool:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
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


# =============================================================================
# Attribute
# =============================================================================

def ensure_follow_attribute(
        control,
        attribute_name="follow",
        default_value=0.5
):
    u"""
    创建或复用 0-1 Follow 属性。

    Args:
        control (str):
            需要处理的控制器 Transform 名称。
        attribute_name (str):
            `attribute_name` 对应的 Maya 节点或资源名称。
        default_value (float):
            新建 Attribute、UI 控件或 Rig 参数使用的默认值。

    Returns:
        object:
        方法执行后的结果数据。
    """
    validate_node(
        control,
        u"控制器"
    )

    if default_value < 0.0:
        default_value = 0.0

    if default_value > 1.0:
        default_value = 1.0

    exists = cmds.attributeQuery(
        attribute_name,
        node=control,
        exists=True
    )

    if not exists:
        cmds.addAttr(
            control,
            longName=attribute_name,
            attributeType="double",
            minValue=0.0,
            maxValue=1.0,
            defaultValue=float(default_value),
            keyable=True
        )

    return "{}.{}".format(
        control,
        attribute_name
    )


# =============================================================================
# Build
# =============================================================================

def create_parent_space_blend(
        driver,
        control,
        weight=0.5,
        attribute_name="follow",
        zero_group=None,
        driven_group=None,
        maintain_offset=True
):
    u"""
    创建 Controller Parent Space Blend。

    Args:
        driver (str):
            外部跟随目标。
        control (str):
            标准 ctrl_ 控制器。
        weight (float):
            初始 Follow 权重，范围 0-1。
        attribute_name (str):
            控制器上的 Follow 属性名。
        zero_group (str/None):
            可显式传入 Zero Group；None 时根据 control 名称推导。
        driven_group (str/None):
            可显式传入 Driven Group；None 时根据 control 名称推导。
        maintain_offset (bool):
            Parent Constraint 是否保持偏移。

    Returns:
        dict:
        control / driver / zero / driven / constraint /
        reverse / follow_plug。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    validate_node(
        driver,
        u"Driver"
    )
    validate_node(
        control,
        u"Controller"
    )

    if zero_group is None:
        zero_group = replace_control_prefix(
            control,
            "zero"
        )

    if driven_group is None:
        driven_group = replace_control_prefix(
            control,
            "driven"
        )

    validate_node(
        zero_group,
        u"Zero Group"
    )
    validate_node(
        driven_group,
        u"Driven Group"
    )

    follow_plug = ensure_follow_attribute(
        control=control,
        attribute_name=attribute_name,
        default_value=weight
    )

    # -------------------------------------------------------------------------
    # Parent Constraint
    #
    # Driver 和 Zero 共同约束 Driven。
    # Zero 作为“原始空间”目标，可以避免 Follow=0 时 Driven 漂移。
    # -------------------------------------------------------------------------
    constraint_name = "cns_{}_{}_001".format(
        get_short_name(control).replace("ctrl_", "", 1),
        attribute_name
    )

    existing_constraints = cmds.ls(
        constraint_name,
        type="parentConstraint"
    )

    if existing_constraints:
        raise RuntimeError(
            u"Controller Space Blend 已存在：{}".format(
                existing_constraints[0]
            )
        )

    constraint = cmds.parentConstraint(
        driver,
        zero_group,
        driven_group,
        maintainOffset=maintain_offset,
        name=constraint_name
    )[0]

    weight_aliases = cmds.parentConstraint(
        constraint,
        query=True,
        weightAliasList=True
    )

    if weight_aliases is None:
        weight_aliases = []

    if len(weight_aliases) != 2:
        cmds.delete(constraint)
        raise RuntimeError(
            u"Parent Constraint 权重目标数量异常：{}".format(
                constraint
            )
        )

    driver_weight_plug = "{}.{}".format(
        constraint,
        weight_aliases[0]
    )

    zero_weight_plug = "{}.{}".format(
        constraint,
        weight_aliases[1]
    )

    # -------------------------------------------------------------------------
    # Follow
    # -------------------------------------------------------------------------
    cmds.connectAttr(
        follow_plug,
        driver_weight_plug,
        force=True
    )

    reverse_name = "reverse_{}_{}_001".format(
        get_short_name(control).replace("ctrl_", "", 1),
        attribute_name
    )

    reverse_node = cmds.createNode(
        "reverse",
        name=reverse_name
    )

    cmds.connectAttr(
        follow_plug,
        reverse_node + ".inputX",
        force=True
    )

    cmds.connectAttr(
        reverse_node + ".outputX",
        zero_weight_plug,
        force=True
    )

    return {
        "driver": driver,
        "control": control,
        "zero": zero_group,
        "driven": driven_group,
        "constraint": constraint,
        "reverse": reverse_node,
        "follow_plug": follow_plug,
    }


__all__ = [
    "get_short_name",
    "replace_control_prefix",
    "validate_node",
    "ensure_follow_attribute",
    "create_parent_space_blend",
]
