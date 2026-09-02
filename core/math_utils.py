# coding=utf-8
u"""
Math Utils
==========

与 Maya Scene 无关的纯 Python 数学底层工具。

设计边界
--------
- 不 import maya.cmds；
- 不接收 Maya Node；
- 只处理普通 Python 数值、Point、Vector 等数据；
- Maya Transform 数据先由 transform_utils 读取，再交给本模块计算。
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


def distance_between_points(point_a, point_b):
    u"""返回两个三维 Point 之间的欧氏距离。"""
    point_a = _validate_point3(
        point_a,
        "point_a"
    )
    point_b = _validate_point3(
        point_b,
        "point_b"
    )

    delta_x = point_b[0] - point_a[0]
    delta_y = point_b[1] - point_a[1]
    delta_z = point_b[2] - point_a[2]

    distance_squared = (
        delta_x * delta_x
        + delta_y * delta_y
        + delta_z * delta_z
    )

    return math.sqrt(
        distance_squared
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
    "distance_between_points",
    "lerp_point3",
    "average_point3",
]
