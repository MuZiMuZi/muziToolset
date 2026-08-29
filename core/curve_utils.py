# coding=utf-8
u"""
Curve Utils
===========

Maya NURBS Curve 通用底层工具。

从旧 pipelineUtils 中拆出的职责：
    - Curve Shape / Transform 查询；
    - Curve CV 查询；
    - 按长度均匀采样 Point / Tangent；
    - 根据 Maya 节点创建 Curve；
    - 根据当前 Polygon Edge 创建 Curve。

说明：
    Joint 专属逻辑继续留在 jointUtils；
    本模块只提供通用 Curve 数据和创建能力。
"""

from __future__ import print_function

import maya.cmds as cmds
import maya.api.OpenMaya as om


# =============================================================================
# Validate / Query
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


def get_curve_shape(curve):
    """返回 NURBS Curve Shape 长路径。"""
    validate_node(curve)

    if cmds.nodeType(curve) == "nurbsCurve":
        matches = cmds.ls(
            curve,
            long=True
        )

        if matches:
            return matches[0]

        return curve

    shapes = cmds.listRelatives(
        curve,
        shapes=True,
        noIntermediate=True,
        fullPath=True
    )

    if shapes is None:
        shapes = []

    for shape in shapes:
        if cmds.nodeType(shape) == "nurbsCurve":
            return shape

    raise RuntimeError(
        u"节点不是 NURBS Curve：{}".format(curve)
    )


def get_curve_transform(curve):
    """返回 NURBS Curve Transform 长路径。"""
    curve_shape = get_curve_shape(curve)

    parents = cmds.listRelatives(
        curve_shape,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    if not parents:
        raise RuntimeError(
            u"Curve Shape 没有 Transform Parent：{}".format(
                curve_shape
            )
        )

    return parents[0]


def get_curve_cvs(curve):
    """返回 Curve 的全部 CV Component。"""
    curve_shape = get_curve_shape(curve)

    curve_cvs = cmds.ls(
        curve_shape + ".cv[*]",
        flatten=True
    )

    if curve_cvs is None:
        curve_cvs = []

    return curve_cvs


def get_curve_cv_count(curve):
    """返回 Curve CV 数量。"""
    curve_cvs = get_curve_cvs(curve)
    return len(curve_cvs)


def get_curve_cv_positions(
        curve,
        world_space=True
):
    """返回 Curve CV 坐标列表。"""
    curve_cvs = get_curve_cvs(curve)
    positions = []

    for curve_cv in curve_cvs:
        position = cmds.xform(
            curve_cv,
            query=True,
            worldSpace=world_space,
            translation=True
        )

        positions.append(position)

    return positions


# =============================================================================
# Maya API
# =============================================================================

def get_dag_path(node):
    """返回 Maya API 2.0 MDagPath。"""
    validate_node(node)

    selection = om.MSelectionList()
    selection.add(node)

    dag_path = selection.getDagPath(0)
    return dag_path


def get_curve_function(curve):
    """返回 Maya API 2.0 MFnNurbsCurve。"""
    curve_shape = get_curve_shape(curve)
    dag_path = get_dag_path(curve_shape)
    return om.MFnNurbsCurve(dag_path)


# =============================================================================
# Sample
# =============================================================================

def get_even_percentages(sample_count):
    """
    返回 0~1 的均匀百分比。

    例如：
        get_even_percentages(5)
        -> [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    if sample_count < 2:
        raise ValueError(
            u"sample_count 必须大于或等于 2。"
        )

    percentages = []
    gap = 1.0 / float(sample_count - 1)

    index = 0
    while index < sample_count:
        percentages.append(
            index * gap
        )
        index += 1

    return percentages


def sample_curve_by_length(
        curve,
        sample_count,
        world_space=True
):
    """
    按曲线弧长均匀采样 Point 和 Tangent。

    Returns:
        dict:
            {
                "points": [[x, y, z], ...],
                "tangents": [[x, y, z], ...],
                "parameters": [float, ...],
            }
    """
    curve_function = get_curve_function(curve)
    percentages = get_even_percentages(sample_count)

    space = om.MSpace.kObject

    if world_space:
        space = om.MSpace.kWorld

    curve_length = curve_function.length()

    points = []
    tangents = []
    parameters = []

    for percentage in percentages:
        sample_length = curve_length * percentage
        parameter = curve_function.findParamFromLength(
            sample_length
        )
        point = curve_function.getPointAtParam(
            parameter,
            space
        )
        tangent = curve_function.tangent(
            parameter,
            space
        )

        points.append([
            point.x,
            point.y,
            point.z,
        ])
        tangents.append([
            tangent.x,
            tangent.y,
            tangent.z,
        ])
        parameters.append(parameter)

    return {
        "points": points,
        "tangents": tangents,
        "parameters": parameters,
    }


# =============================================================================
# Create
# =============================================================================

def create_curve_from_nodes(
        nodes,
        name,
        degree=3
):
    """根据 Maya 节点的世界位置创建 NURBS Curve。"""
    if nodes is None:
        nodes = []

    if not nodes:
        raise RuntimeError(u"没有给定用于创建 Curve 的节点。")

    if degree < 1:
        raise ValueError(u"Curve degree 不能小于 1。")

    if len(nodes) < degree + 1:
        raise ValueError(
            u"degree={} 至少需要 {} 个点，当前只有 {} 个节点。".format(
                degree,
                degree + 1,
                len(nodes)
            )
        )

    curve_points = []

    for node in nodes:
        validate_node(node)

        position = cmds.xform(
            node,
            query=True,
            worldSpace=True,
            translation=True
        )

        curve_points.append(position)

    curve = cmds.curve(
        point=curve_points,
        degree=degree,
        name=name
    )

    return curve


def create_curve_from_selected_edges(
        name,
        degree=3,
        form=2
):
    """根据当前选择的 Polygon Edge 创建 NURBS Curve。"""
    selected_edges = cmds.filterExpand(
        selectionMask=32,
        expand=True
    )

    if selected_edges is None:
        selected_edges = []

    if not selected_edges:
        raise RuntimeError(
            u"请先选择一个或多个 Polygon Edge。"
        )

    result = cmds.polyToCurve(
        form=form,
        degree=degree,
        constructionHistory=False,
        name=name
    )

    if not result:
        raise RuntimeError(u"Polygon Edge 转 Curve 失败。")

    curve = result[0]
    return curve


__all__ = [
    "validate_node",
    "get_curve_shape",
    "get_curve_transform",
    "get_curve_cvs",
    "get_curve_cv_count",
    "get_curve_cv_positions",
    "get_dag_path",
    "get_curve_function",
    "get_even_percentages",
    "sample_curve_by_length",
    "create_curve_from_nodes",
    "create_curve_from_selected_edges",
]
