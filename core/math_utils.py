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
    u"""检查输入是否为包含 3 个数值的 Point / Vector。"""
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


__all__ = [
    "distance_between_points",
]
