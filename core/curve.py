# coding=utf-8
u"""
Curve Algorithms
================

NURBS Curve 的通用采样和 Attachment 算法。

场景节点和属性直接使用 PyMEL；几何参数计算使用 Maya API 2.0。
"""

from __future__ import print_function

import maya.api.OpenMaya as om
import pymel.core as pm


def get_curve_shape(curve_node):
    u"""返回有效的 NurbsCurve Shape PyNode。"""
    if isinstance(curve_node, str):
        if not pm.objExists(curve_node):
            raise RuntimeError(
                u"Curve 不存在：{}".format(curve_node)
            )
        curve_node = pm.PyNode(curve_node)

    if curve_node.nodeType() == "nurbsCurve":
        return curve_node

    if curve_node.nodeType() != "transform":
        raise TypeError(
            u"输入必须是 Curve Transform 或 NurbsCurve Shape：{}".format(
                curve_node
            )
        )

    for shape in curve_node.getShapes(noIntermediate=True):
        if shape.nodeType() == "nurbsCurve":
            return shape

    raise TypeError(
        u"Transform 下没有有效 NurbsCurve Shape：{}".format(curve_node)
    )


def get_curve_transform(curve_node):
    shape = get_curve_shape(curve_node)
    return shape.getParent()


def get_curve_function(curve_node):
    u"""返回 Maya API 2.0 MFnNurbsCurve。"""
    shape = get_curve_shape(curve_node)
    selection = om.MSelectionList()
    selection.add(
        shape.longName()
    )
    dag_path = selection.getDagPath(0)
    return om.MFnNurbsCurve(
        dag_path
    )


def get_cv_positions(
        curve_node,
        world_space=True
):
    u"""返回 Curve CV 坐标。"""
    curve_function = get_curve_function(
        curve_node
    )

    space = om.MSpace.kObject
    if world_space:
        space = om.MSpace.kWorld

    points = curve_function.cvPositions(
        space
    )
    result = []

    for point in points:
        result.append(
            (point.x, point.y, point.z)
        )

    return result


def get_closest_parameter(
        curve_node,
        world_position
):
    curve_function = get_curve_function(
        curve_node
    )
    point = om.MPoint(
        world_position[0],
        world_position[1],
        world_position[2]
    )
    closest = curve_function.closestPoint(
        point,
        space=om.MSpace.kWorld
    )
    return float(
        closest[1]
    )


def parameter_to_length_percentage(
        curve_node,
        parameter
):
    curve_function = get_curve_function(
        curve_node
    )
    total_length = curve_function.length()

    if total_length <= 0.0:
        return 0.0

    length = curve_function.findLengthFromParam(
        float(parameter)
    )
    return float(length) / float(total_length)


def length_percentage_to_parameter(
        curve_node,
        percentage
):
    curve_function = get_curve_function(
        curve_node
    )
    percentage = max(
        0.0,
        min(1.0, float(percentage))
    )
    target_length = curve_function.length() * percentage
    return float(
        curve_function.findParamFromLength(target_length)
    )


def _create_attachment_transform(
        name,
        parent=None
):
    if pm.objExists(name):
        raise RuntimeError(
            u"Curve Attachment 已经存在：{}".format(name)
        )

    attachment = pm.createNode(
        "transform",
        name=name
    )

    if parent is not None:
        attachment.setParent(parent)

    return attachment


def create_point_attachment(
        curve_node,
        parameter,
        name,
        parent=None
):
    u"""按 Curve Parameter 创建 Position Attachment。"""
    curve_shape = get_curve_shape(
        curve_node
    )
    attachment = _create_attachment_transform(
        name,
        parent
    )

    point_on_curve = pm.createNode(
        "pointOnCurveInfo",
        name="{}_poci".format(name)
    )
    compose_matrix = pm.createNode(
        "composeMatrix",
        name="{}_compose".format(name)
    )
    decompose_matrix = pm.createNode(
        "decomposeMatrix",
        name="{}_decompose".format(name)
    )

    curve_shape.worldSpace[0] >> point_on_curve.inputCurve
    point_on_curve.parameter.set(
        float(parameter)
    )
    point_on_curve.position >> compose_matrix.inputTranslate

    matrix_nodes = [
        compose_matrix,
        decompose_matrix,
    ]
    output_matrix = compose_matrix.outputMatrix

    if parent is not None:
        mult_matrix = pm.createNode(
            "multMatrix",
            name="{}_local_mult".format(name)
        )
        compose_matrix.outputMatrix >> mult_matrix.matrixIn[0]
        parent.worldInverseMatrix[0] >> mult_matrix.matrixIn[1]
        output_matrix = mult_matrix.matrixSum
        matrix_nodes.append(
            mult_matrix
        )

    output_matrix >> decompose_matrix.inputMatrix
    decompose_matrix.outputTranslate >> attachment.translate

    return {
        "transform": attachment,
        "point_on_curve": point_on_curve,
        "matrix_nodes": matrix_nodes,
    }


def create_percentage_attachment(
        curve_node,
        percentage,
        name,
        parent=None
):
    parameter = length_percentage_to_parameter(
        curve_node,
        percentage
    )
    return create_point_attachment(
        curve_node=curve_node,
        parameter=parameter,
        name=name,
        parent=parent
    )


def create_closest_point_attachment(
        curve_node,
        world_position,
        name,
        parent=None
):
    parameter = get_closest_parameter(
        curve_node,
        world_position
    )
    return create_point_attachment(
        curve_node=curve_node,
        parameter=parameter,
        name=name,
        parent=parent
    )


__all__ = [
    "get_curve_shape",
    "get_curve_transform",
    "get_curve_function",
    "get_cv_positions",
    "get_closest_parameter",
    "parameter_to_length_percentage",
    "length_percentage_to_parameter",
    "create_point_attachment",
    "create_percentage_attachment",
    "create_closest_point_attachment",
]
