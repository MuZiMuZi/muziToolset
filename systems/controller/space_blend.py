# coding=utf-8
u"""
Controller Space Blend
======================

控制器 Parent Space / Follow 混合系统。

职责：
    1. 使用外部 Driver 和 Controller Zero 共同驱动 Driven Group；
    2. 在控制器上创建 0-1 Follow 属性；
    3. 自动创建反向权重；
    4. 不依赖旧 Pipeline / PyMel。

重要边界：
    - DAG Short Name 统一复用 core.rename_utils；
    - Maya 节点校验统一复用 core.scene_utils；
    - Attribute 创建统一复用 core.attr_utils；
    - Parent Constraint 统一复用 core.constraint_utils；
    - DG Plug Connection 统一复用 core.connection_utils；
    - 本模块只保留 Parent Space / Follow Workflow。

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

from ...core import attr_utils
from ...core import connection_utils
from ...core import constraint_utils
from ...core import rename_utils
from ...core import scene_utils


# =============================================================================
# Name
# =============================================================================

def get_short_name(node):
    u"""
    返回 DAG Short Name。

    保留旧公开入口，实际规则统一由 core.rename_utils 维护。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """
    # 使用统一 Rename Core 提取 DAG Short Name。
    return rename_utils.get_short_name(
        node
    )


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
    # 使用统一 Short Name 入口取得不带 DAG Path 的 Controller 名称。
    short_name = get_short_name(
        control
    )

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
# Validate - Compatibility
# =============================================================================

def validate_node(node, label):
    u"""
    检查必要 Maya 节点。

    保留旧公开入口，实际节点存在性规则统一由 scene_utils 维护。

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

    try:
        # 使用 Scene Core 统一检查节点存在性。
        scene_utils.validate_node(
            node
        )
    except RuntimeError:
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
    # 先确认 Controller 节点有效，再操作其自定义 Attribute。
    validate_node(
        control,
        u"控制器"
    )

    if default_value < 0.0:
        default_value = 0.0

    if default_value > 1.0:
        default_value = 1.0

    # 使用统一 Attr Core 查询 / 创建 Follow Attribute，已有属性不覆盖当前动画值。
    control_attr = attr_utils.Attr(
        control
    )

    if not control_attr.attr_exists(
            attribute_name
    ):
        control_attr.add_attr(
            attribute_name,
            attr_type="double",
            lock=False,
            hide=False,
            default_value=float(default_value),
            min_value=0.0,
            max_value=1.0
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
            作为驱动端的 Maya 节点名称。
        control (str):
            需要处理的控制器 Transform 名称。
        weight (float):
            当前计算、混合或变形使用的权重值。
        attribute_name (str):
            `attribute_name` 对应的 Maya 节点或资源名称。
        zero_group (str):
            当前 Rig / Guide / Controller 层级中的 Maya Group Transform。
        driven_group (str):
            当前 Rig / Guide / Controller 层级中的 Maya Group Transform。
        maintain_offset (bool):
            是否在建立约束或矩阵关系时保持当前偏移。

    Returns:
        dict:
        control / driver / zero / driven / constraint /
        reverse / follow_plug。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 检查外部 Space Driver 是否存在。
    validate_node(
        driver,
        u"Driver"
    )

    # 检查需要增加 Follow 行为的 Controller 是否存在。
    validate_node(
        control,
        u"Controller"
    )

    if zero_group is None:
        # 根据标准 Controller 名称推导对应 Zero Group 名称。
        zero_group = replace_control_prefix(
            control,
            "zero"
        )

    if driven_group is None:
        # 根据标准 Controller 名称推导对应 Driven Group 名称。
        driven_group = replace_control_prefix(
            control,
            "driven"
        )

    # 确认 Controller 原始 Zero Space 节点可用。
    validate_node(
        zero_group,
        u"Zero Group"
    )

    # 确认真正接收 Parent Space 混合的 Driven Group 可用。
    validate_node(
        driven_group,
        u"Driven Group"
    )

    # 创建或复用 Controller 上的 0-1 Follow Attribute。
    follow_plug = ensure_follow_attribute(
        control=control,
        attribute_name=attribute_name,
        default_value=weight
    )

    control_short_name = get_short_name(
        control
    )
    control_name_part = control_short_name.replace(
        "ctrl_",
        "",
        1
    )

    constraint_name = "cns_{}_{}_001".format(
        control_name_part,
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

    # 使用 Constraint Core 让外部 Driver 和原始 Zero Space 共同驱动 Driven Group。
    constraint_nodes = constraint_utils.create_constraint(
        driver_objects=[
            driver,
            zero_group,
        ],
        driven_object=driven_group,
        constraint_type="parentConstraint",
        maintain_offset=maintain_offset,
        name=constraint_name
    )

    if not constraint_nodes:
        raise RuntimeError(
            u"Parent Space Constraint 创建失败：{}".format(
                driven_group
            )
        )

    constraint = constraint_nodes[0]

    weight_aliases = cmds.parentConstraint(
        constraint,
        query=True,
        weightAliasList=True
    )

    if weight_aliases is None:
        weight_aliases = []

    if len(weight_aliases) != 2:
        cmds.delete(
            constraint
        )
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

    # 把 Follow 值直接连接到外部 Driver 的 Constraint Weight。
    connection_utils.connect_plugs(
        follow_plug,
        driver_weight_plug,
        force=True
    )

    reverse_name = "reverse_{}_{}_001".format(
        control_name_part,
        attribute_name
    )

    # 创建 Reverse Node，把 Follow 转换成 Zero Space 的反向权重。
    reverse_node = scene_utils.create_node(
        "reverse",
        reverse_name
    )

    # 把 Follow 输入 Reverse Node，得到 1 - Follow。
    connection_utils.connect_plugs(
        follow_plug,
        reverse_node + ".inputX",
        force=True
    )

    # 把反向权重连接到 Zero Space Constraint Weight。
    connection_utils.connect_plugs(
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
