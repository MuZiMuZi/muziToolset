# coding=utf-8
u"""
Math Utils
==========

与 Maya Scene 无关的纯 Python 数学底层工具。

模块职责
--------
- 三维 Point / Vector 校验；
- 距离、插值和平均值；
- Vector 加减、标量乘法、长度、归一化和点积。

设计边界
--------
- 不 import maya.cmds；
- 不接收 Maya Node；
- 只处理普通 Python 数值、Point、Vector 等数据；
- Maya Transform 数据先由 transform_utils 读取，再交给本模块计算；
- Rig 专用解算流程留在对应 System / Tool，只把通用数学运算放这里。
"""

from __future__ import print_function

import math


def _validate_point3(point, label):
    u"""检查输入是否为包含 3 个数值的 Point / Vector，并返回 float 列表。"""
    if point is None:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    try:
        value_count = len(
            point
        )
    except TypeError:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    if value_count != 3:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    values = []

    for value in point:
        try:
            values.append(
                float(value)
            )
        except (TypeError, ValueError):
            raise ValueError(
                u"{} 必须包含 3 个数值。".format(
                    label
                )
            )

    return values


def add_vector3(vector_a, vector_b):
    u"""返回两个三维 Vector 相加的结果。"""
    vector_a = _validate_point3(
        vector_a,
        "vector_a"
    )
    vector_b = _validate_point3(
        vector_b,
        "vector_b"
    )

    return [
        vector_a[0] + vector_b[0],
        vector_a[1] + vector_b[1],
        vector_a[2] + vector_b[2],
    ]


def subtract_vector3(vector_a, vector_b):
    u"""返回 vector_a - vector_b。"""
    vector_a = _validate_point3(
        vector_a,
        "vector_a"
    )
    vector_b = _validate_point3(
        vector_b,
        "vector_b"
    )

    return [
        vector_a[0] - vector_b[0],
        vector_a[1] - vector_b[1],
        vector_a[2] - vector_b[2],
    ]


def multiply_vector3(vector, value):
    u"""返回三维 Vector 与标量相乘的结果。"""
    vector = _validate_point3(
        vector,
        "vector"
    )
    value = float(
        value
    )

    return [
        vector[0] * value,
        vector[1] * value,
        vector[2] * value,
    ]


def length_vector3(vector):
    u"""返回三维 Vector 的欧氏长度。"""
    vector = _validate_point3(
        vector,
        "vector"
    )

    return math.sqrt(
        vector[0] * vector[0]
        + vector[1] * vector[1]
        + vector[2] * vector[2]
    )


def normalize_vector3(vector, epsilon=0.000001):
    u"""返回三维单位 Vector；长度接近零时返回 [0, 0, 0]。"""
    vector = _validate_point3(
        vector,
        "vector"
    )
    length = length_vector3(
        vector
    )

    if length <= float(epsilon):
        return [
            0.0,
            0.0,
            0.0,
        ]

    return [
        vector[0] / length,
        vector[1] / length,
        vector[2] / length,
    ]


def dot_vector3(vector_a, vector_b):
    u"""返回两个三维 Vector 的 Dot Product。"""
    vector_a = _validate_point3(
        vector_a,
        "vector_a"
    )
    vector_b = _validate_point3(
        vector_b,
        "vector_b"
    )

    return (
        vector_a[0] * vector_b[0]
        + vector_a[1] * vector_b[1]
        + vector_a[2] * vector_b[2]
    )


def distance_between_points(point_a, point_b):
    u"""返回两个三维 Point 之间的欧氏距离。"""
    delta = subtract_vector3(
        point_b,
        point_a
    )
    return length_vector3(
        delta
    )


def lerp_point3(
        start_point,
        end_point,
        ratio
):
    u"""按 ratio 对两个三维 Point / Vector 做线性插值。"""
    start_point = _validate_point3(
        start_point,
        "start_point"
    )
    end_point = _validate_point3(
        end_point,
        "end_point"
    )
    ratio = float(
        ratio
    )

    result = []
    axis_index = 0

    while axis_index < 3:
        value = start_point[axis_index] + (
            end_point[axis_index] - start_point[axis_index]
        ) * ratio
        result.append(
            value
        )
        axis_index += 1

    return result


def average_point3(points):
    u"""返回一组三维 Point / Vector 的算术平均值；空输入返回 None。"""
    if not points:
        return None

    total_x = 0.0
    total_y = 0.0
    total_z = 0.0
    point_count = 0

    for point in points:
        point = _validate_point3(
            point,
            "point"
        )
        total_x += point[0]
        total_y += point[1]
        total_z += point[2]
        point_count += 1

    count = float(
        point_count
    )

    return [
        total_x / count,
        total_y / count,
        total_z / count,
    ]


__all__ = [
    "add_vector3",
    "subtract_vector3",
    "multiply_vector3",
    "length_vector3",
    "normalize_vector3",
    "dot_vector3",
    "distance_between_points",
    "lerp_point3",
    "average_point3",
]
