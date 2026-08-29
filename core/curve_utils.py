# coding=utf-8
u"""
Curve Utils
===========

Maya NURBS Curve 通用底层工具。

从旧 pipelineUtils 中拆出的职责：
    - Curve Shape / Transform 查询；
    - Curve CV 查询；
    - 按长度均匀采样 Point / Tangent；
    - Curve Parameter 与弧长百分比互转；
    - 查询世界位置在 Curve 上最近的 Parameter；
    - 创建 pointOnCurveInfo 附着节点；
    - 根据 Maya 节点创建 Curve；
    - 根据当前 Polygon Edge 创建 Curve。

说明：
    Joint 专属逻辑继续留在 jointUtils；
    Face / Eyelid / Lip 等完整绑定逻辑留在对应 System；
    本模块只提供通用 Curve 数据、采样和附着能力。
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


def get_closest_parameter(
        curve,
        world_position
):
    """
    返回世界坐标在 Curve 上最近点的 Parameter。

    这里使用临时 nearestPointOnCurve 节点，原因是 Maya 2023 中
    pointOnCurveInfo 使用原始 Curve Parameter，而不是 0~1 百分比。
    """
    if world_position is None:
        raise ValueError(u"world_position 不能为空。")

    if len(world_position) != 3:
        raise ValueError(u"world_position 必须包含 x / y / z 三个数值。")

    curve_shape = get_curve_shape(curve)
    nearest_node = cmds.createNode(
        "nearestPointOnCurve"
    )

    try:
        cmds.connectAttr(
            curve_shape + ".worldSpace[0]",
            nearest_node + ".inputCurve",
            force=True
        )

        cmds.setAttr(
            nearest_node + ".inPosition",
            world_position[0],
            world_position[1],
            world_position[2],
            type="double3"
        )

        parameter = cmds.getAttr(
            nearest_node + ".parameter"
        )
    finally:
        if cmds.objExists(nearest_node):
            cmds.delete(nearest_node)

    return parameter


def parameter_to_length_percentage(
        curve,
        parameter
):
    """把 Curve 原始 Parameter 转换成 0~1 弧长百分比。"""
    curve_function = get_curve_function(curve)
    curve_length = curve_function.length()

    if curve_length <= 0.000001:
        raise RuntimeError(
            u"Curve 长度为 0，无法换算 Parameter：{}".format(
                curve
            )
        )

    parameter_length = curve_function.findLengthFromParam(
        parameter
    )
    percentage = parameter_length / curve_length

    if percentage < 0.0:
        percentage = 0.0

    if percentage > 1.0:
        percentage = 1.0

    return percentage


def length_percentage_to_parameter(
        curve,
        percentage
):
    """把 0~1 弧长百分比转换成 Curve 原始 Parameter。"""
    percentage = float(percentage)

    if percentage < 0.0 or percentage > 1.0:
        raise ValueError(
            u"percentage 必须在 0~1 范围内：{}".format(
                percentage
            )
        )

    curve_function = get_curve_function(curve)
    curve_length = curve_function.length()
    target_length = curve_length * percentage

    parameter = curve_function.findParamFromLength(
        target_length
    )

    return parameter


# =============================================================================
# Attach
# =============================================================================

def create_point_on_curve_attachment(
        curve,
        parameter,
        name,
        parent=None
):
    """
    创建一个由 pointOnCurveInfo 驱动的 Transform。

    当 attachment 有 Parent 时，pointOnCurveInfo.position 是世界空间值，
    不能直接连接到子节点的本地 translate。因此会自动建立：

        pointOnCurveInfo.position
            -> composeMatrix
            -> multMatrix(parent.worldInverseMatrix)
            -> decomposeMatrix
            -> attachment.translate

    Returns:
        dict:
            {
                "transform": str,
                "point_on_curve": str,
                "matrix_nodes": [str, ...],
                "parameter": float,
            }
    """
    curve_shape = get_curve_shape(curve)

    if parent is not None:
        validate_node(parent)

    attachment = cmds.createNode(
        "transform",
        name=name,
        parent=parent
    )

    point_on_curve = cmds.createNode(
        "pointOnCurveInfo",
        name="poci_{}".format(name)
    )

    cmds.connectAttr(
        curve_shape + ".worldSpace[0]",
        point_on_curve + ".inputCurve",
        force=True
    )
    cmds.setAttr(
        point_on_curve + ".parameter",
        parameter
    )

    matrix_nodes = []

    if parent is None:
        cmds.connectAttr(
            point_on_curve + ".position",
            attachment + ".translate",
            force=True
        )
    else:
        compose_matrix = cmds.createNode(
            "composeMatrix",
            name="cmp_{}".format(name)
        )
        mult_matrix = cmds.createNode(
            "multMatrix",
            name="mult_{}".format(name)
        )
        decompose_matrix = cmds.createNode(
            "decomposeMatrix",
            name="dcmp_{}".format(name)
        )

        matrix_nodes.append(compose_matrix)
        matrix_nodes.append(mult_matrix)
        matrix_nodes.append(decompose_matrix)

        cmds.connectAttr(
            point_on_curve + ".position",
            compose_matrix + ".inputTranslate",
            force=True
        )
        cmds.connectAttr(
            compose_matrix + ".outputMatrix",
            mult_matrix + ".matrixIn[0]",
            force=True
        )
        cmds.connectAttr(
            parent + ".worldInverseMatrix[0]",
            mult_matrix + ".matrixIn[1]",
            force=True
        )
        cmds.connectAttr(
            mult_matrix + ".matrixSum",
            decompose_matrix + ".inputMatrix",
            force=True
        )
        cmds.connectAttr(
            decompose_matrix + ".outputTranslate",
            attachment + ".translate",
            force=True
        )

    return {
        "transform": attachment,
        "point_on_curve": point_on_curve,
        "matrix_nodes": matrix_nodes,
        "parameter": parameter,
    }


def create_closest_point_attachment(
        curve,
        world_position,
        name,
        parent=None
):
    """在 Curve 上离 world_position 最近的位置创建 Attachment。"""
    parameter = get_closest_parameter(
        curve,
        world_position
    )

    return create_point_on_curve_attachment(
        curve=curve,
        parameter=parameter,
        name=name,
        parent=parent
    )


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
    "get_closest_parameter",
    "parameter_to_length_percentage",
    "length_percentage_to_parameter",
    "create_point_on_curve_attachment",
    "create_closest_point_attachment",
    "create_curve_from_nodes",
    "create_curve_from_selected_edges",
]
