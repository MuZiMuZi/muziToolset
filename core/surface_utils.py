# coding=utf-8
u"""
Surface Utils
=============

Maya NURBS Surface / Follicle 通用底层工具。

从旧 pipelineUtils 中拆出的职责：
    - 根据 Curve 建立简单 Loft Surface；
    - 查询 NURBS Surface Shape；
    - 在 NURBS Surface 上创建 Follicle；
    - 批量按 U / V 均匀创建 Follicle。

说明：
    旧 create_joint_follicle_on_surface() 同时创建 Joint、Controller、Set 和 Rig Group，
    职责过重。正式 Core 只负责 Surface / Follicle，Joint 和 Controller 由上层系统决定。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import curve_utils


# =============================================================================
# Query
# =============================================================================

def validate_node(node):
    """检查 Maya 节点是否存在。"""
    if not node:
        raise RuntimeError(u"节点名称不能为空。")

    if not cmds.objExists(node):
        raise RuntimeError(
            u"Maya 节点不存在：{}".format(node)
        )

    return True


def get_surface_shape(surface):
    """返回 NURBS Surface Shape 长路径。"""
    validate_node(surface)

    if cmds.nodeType(surface) == "nurbsSurface":
        matches = cmds.ls(
            surface,
            long=True
        )

        if matches:
            return matches[0]

        return surface

    shapes = cmds.listRelatives(
        surface,
        shapes=True,
        noIntermediate=True,
        fullPath=True
    )

    if shapes is None:
        shapes = []

    for shape in shapes:
        if cmds.nodeType(shape) == "nurbsSurface":
            return shape

    raise RuntimeError(
        u"节点不是 NURBS Surface：{}".format(surface)
    )


def get_surface_transform(surface):
    """返回 NURBS Surface Transform 长路径。"""
    surface_shape = get_surface_shape(surface)

    parents = cmds.listRelatives(
        surface_shape,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    if not parents:
        raise RuntimeError(
            u"Surface Shape 没有 Transform Parent：{}".format(
                surface_shape
            )
        )

    return parents[0]


# =============================================================================
# Loft
# =============================================================================

def move_curve_copy(
        curve,
        axis,
        distance
):
    """沿自身 Object Space 指定轴移动 Curve 副本。"""
    axis = axis.upper()

    move_x = 0.0
    move_y = 0.0
    move_z = 0.0

    if axis == "X":
        move_x = distance
    elif axis == "Y":
        move_y = distance
    elif axis == "Z":
        move_z = distance
    else:
        raise ValueError(
            u"offset_axis 只支持 X / Y / Z，当前为：{}".format(
                axis
            )
        )

    cmds.move(
        move_x,
        move_y,
        move_z,
        curve,
        relative=True,
        objectSpace=True,
        worldSpaceDistance=True
    )

    return curve


def create_surface_from_curve(
        curve,
        name,
        offset=0.2,
        offset_axis="Y",
        degree=3
):
    """
    复制给定 Curve 两次并 Loft 成 NURBS Surface。

    与旧 pipelineUtils 不同：
        不移动原 Curve；
        不删除原 Curve；
        临时副本在 Loft 完成后删除。
    """
    curve_transform = curve_utils.get_curve_transform(
        curve
    )

    positive_copy = cmds.duplicate(
        curve_transform,
        renameChildren=True
    )[0]
    negative_copy = cmds.duplicate(
        curve_transform,
        renameChildren=True
    )[0]

    try:
        move_curve_copy(
            positive_copy,
            offset_axis,
            offset
        )
        move_curve_copy(
            negative_copy,
            offset_axis,
            -offset
        )

        result = cmds.loft(
            positive_copy,
            negative_copy,
            constructionHistory=False,
            uniform=True,
            degree=degree,
            sectionSpans=1,
            range=False,
            polygon=0,
            name=name
        )

        if not result:
            raise RuntimeError(u"Curve Loft Surface 创建失败。")

        surface = result[0]
    finally:
        if cmds.objExists(positive_copy):
            cmds.delete(positive_copy)

        if cmds.objExists(negative_copy):
            cmds.delete(negative_copy)

    return surface


# =============================================================================
# Follicle
# =============================================================================

def create_follicle(
        surface,
        name,
        parameter_u=0.5,
        parameter_v=0.5,
        parent=None
):
    """在 NURBS Surface 上创建一个 Follicle。"""
    surface_shape = get_surface_shape(surface)

    follicle_shape = cmds.createNode(
        "follicle",
        name="{}Shape".format(name)
    )

    parents = cmds.listRelatives(
        follicle_shape,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    if not parents:
        raise RuntimeError(u"创建 Follicle Transform 失败。")

    follicle_transform = cmds.rename(
        parents[0],
        name
    )

    cmds.connectAttr(
        surface_shape + ".local",
        follicle_shape + ".inputSurface",
        force=True
    )
    cmds.connectAttr(
        surface_shape + ".worldMatrix[0]",
        follicle_shape + ".inputWorldMatrix",
        force=True
    )
    cmds.connectAttr(
        follicle_shape + ".outTranslate",
        follicle_transform + ".translate",
        force=True
    )
    cmds.connectAttr(
        follicle_shape + ".outRotate",
        follicle_transform + ".rotate",
        force=True
    )

    cmds.setAttr(
        follicle_shape + ".parameterU",
        parameter_u
    )
    cmds.setAttr(
        follicle_shape + ".parameterV",
        parameter_v
    )

    if parent:
        validate_node(parent)
        follicle_transform = cmds.parent(
            follicle_transform,
            parent
        )[0]

    return {
        "transform": follicle_transform,
        "shape": follicle_shape,
    }


def create_even_follicles(
        surface,
        count,
        name_prefix="fol_surface",
        direction="U",
        fixed_parameter=0.5,
        parent=None
):
    """
    在 Surface 的 U 或 V 方向均匀创建 Follicle。

    count=1 时放在 0.5；count>=2 时覆盖 0~1。
    """
    if count < 1:
        raise ValueError(u"Follicle 数量不能小于 1。")

    direction = direction.upper()

    if direction != "U" and direction != "V":
        raise ValueError(u"direction 只支持 U 或 V。")

    percentages = []

    if count == 1:
        percentages.append(0.5)
    else:
        percentages = curve_utils.get_even_percentages(
            count
        )

    results = []

    index = 0
    while index < count:
        percentage = percentages[index]

        parameter_u = fixed_parameter
        parameter_v = fixed_parameter

        if direction == "U":
            parameter_u = percentage
        else:
            parameter_v = percentage

        follicle_name = "{}_{:03d}".format(
            name_prefix,
            index + 1
        )

        result = create_follicle(
            surface=surface,
            name=follicle_name,
            parameter_u=parameter_u,
            parameter_v=parameter_v,
            parent=parent
        )

        results.append(result)
        index += 1

    return results


__all__ = [
    "validate_node",
    "get_surface_shape",
    "get_surface_transform",
    "move_curve_copy",
    "create_surface_from_curve",
    "create_follicle",
    "create_even_follicles",
]
