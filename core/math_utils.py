# coding=utf-8
u"""
Math Utils
==========

与 Maya Scene 无关的纯 Python 数学底层工具。

模块职责：
    1. 校验三维 Point / Vector 输入；
    2. 提供三维 Vector 加减、标量乘法、长度、归一化和点积；
    3. 提供 Point 距离、线性插值和平均值计算。

模块边界：
    - 不 import maya.cmds；
    - 不接收 Maya Node 名称；
    - 只处理普通 Python 数值、Point 和 Vector；
    - Maya Transform 数据应先由 transform_utils 读取，再交给本模块计算；
    - Pole Vector、Face Solver 等 Rig 业务流程留在对应 System / Tool。

数据约定：
    - 三维 Point / Vector 均使用长度为 3 的 list / tuple；
    - 对外计算结果统一返回 float 或 ``[x, y, z]`` float 列表；
    - 本模块只做数学运算，不修改调用方传入的原始列表。
"""

from __future__ import print_function

import math


# =============================================================================
# Input Validation
# =============================================================================

def _validate_point3(point, label):
    u"""
    校验三维 Point / Vector，并转换成独立的 float 列表。

    该内部函数是所有 Vector API 的统一输入入口，避免每个数学函数分别维护
    长度检查和数值转换规则。

    Args:
        point (list[float] | tuple[float, float, float]):
            需要验证的三维 Point / Vector。
        label (str):
            输入名称，仅用于生成更明确的异常信息。

    Returns:
        list[float]:
            转换后的 ``[x, y, z]`` float 列表。

    Raises:
        ValueError:
            输入为空、长度不是 3，或任意分量不能转换成 float 时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：先拦截 None，避免后续 len() 产生难理解的 TypeError
    # -------------------------------------------------------------------------
    if point is None:
        raise ValueError(
            u"{} 必须包含 3 个数值。".format(
                label
            )
        )

    # -------------------------------------------------------------------------
    # Step 02：确认输入具有长度，并且严格包含 XYZ 三个分量
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 03：逐个转换为 float，返回新列表而不是修改调用方原数据
    # -------------------------------------------------------------------------
    values = []

    for value in point:
        try:
            float_value = float(
                value
            )
        except (TypeError, ValueError):
            raise ValueError(
                u"{} 必须包含 3 个数值。".format(
                    label
                )
            )

        values.append(
            float_value
        )

    return values


# =============================================================================
# Vector Arithmetic
# =============================================================================

def add_vector3(vector_a, vector_b):
    u"""
    返回两个三维 Vector 的逐分量相加结果。

    Args:
        vector_a (list[float] | tuple[float, float, float]):
            第一个 XYZ Vector。
        vector_b (list[float] | tuple[float, float, float]):
            第二个 XYZ Vector。

    Returns:
        list[float]:
        ``vector_a + vector_b`` 的 XYZ 结果。

    Raises:
        ValueError:
        任意 Vector 不是有效三维数值数据时抛出。
    """
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
    u"""
    返回两个三维 Vector 的逐分量相减结果。

    Args:
        vector_a (list[float] | tuple[float, float, float]):
            被减的 XYZ Vector。
        vector_b (list[float] | tuple[float, float, float]):
            需要从 ``vector_a`` 中减去的 XYZ Vector。

    Returns:
        list[float]:
        ``vector_a - vector_b`` 的 XYZ 结果。

    Raises:
        ValueError:
        任意 Vector 不是有效三维数值数据时抛出。
    """
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
    u"""
    把三维 Vector 的每个分量乘以同一个标量。

    Args:
        vector (list[float] | tuple[float, float, float]):
            需要缩放的 XYZ Vector。
        value (float):
            Vector 缩放倍数。

    Returns:
        list[float]:
        标量乘法后的 XYZ Vector。

    Raises:
        ValueError:
        Vector 无效或 ``value`` 不能转换成 float 时抛出。
    """
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
    u"""
    计算三维 Vector 的欧氏长度。

    Args:
        vector (list[float] | tuple[float, float, float]):
            需要计算长度的 XYZ Vector。

    Returns:
        float:
        ``sqrt(x² + y² + z²)`` 计算得到的 Vector 长度。

    Raises:
        ValueError:
        Vector 不是有效三维数值数据时抛出。
    """
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
    u"""
    把三维 Vector 归一化为单位向量。

    Args:
        vector (list[float] | tuple[float, float, float]):
            需要归一化的 XYZ Vector。
        epsilon (float):
            判断 Vector 是否接近零长度的容差。

    Returns:
        list[float]:
        单位 Vector；长度小于等于 ``epsilon`` 时返回 ``[0, 0, 0]``。

    Raises:
        ValueError:
        Vector 或 ``epsilon`` 不是有效数值时抛出。
    """
    vector = _validate_point3(
        vector,
        "vector"
    )
    epsilon = float(
        epsilon
    )
    length = length_vector3(
        vector
    )

    if length <= epsilon:
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
    u"""
    计算两个三维 Vector 的 Dot Product。

    Args:
        vector_a (list[float] | tuple[float, float, float]):
            第一个 XYZ Vector。
        vector_b (list[float] | tuple[float, float, float]):
            第二个 XYZ Vector。

    Returns:
        float:
        ``ax*bx + ay*by + az*bz`` 的点积结果。

    Raises:
        ValueError:
        任意 Vector 不是有效三维数值数据时抛出。
    """
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


# =============================================================================
# Point Calculation
# =============================================================================

def distance_between_points(point_a, point_b):
    u"""
    计算两个三维 Point 之间的欧氏距离。

    Args:
        point_a (list[float] | tuple[float, float, float]):
            第一个 XYZ Point。
        point_b (list[float] | tuple[float, float, float]):
            第二个 XYZ Point。

    Returns:
        float:
        两个 Point 之间的直线距离。

    Raises:
        ValueError:
        任意 Point 不是有效三维数值数据时抛出。
    """
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
    u"""
    在两个三维 Point / Vector 之间执行线性插值。

    公式为 ``start + (end - start) * ratio``。函数不会限制 ratio 必须位于
    0～1，因此也可以用于区间外推。

    Args:
        start_point (list[float] | tuple[float, float, float]):
            插值起点。
        end_point (list[float] | tuple[float, float, float]):
            插值终点。
        ratio (float):
            插值比例；0 返回 Start，1 返回 End。

    Returns:
        list[float]:
        插值后的 XYZ Point / Vector。

    Raises:
        ValueError:
        Point 无效或 ``ratio`` 不能转换成 float 时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：统一验证起点、终点并把 ratio 转为 float
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 02：按 XYZ 三个轴分别执行同一套线性插值公式
    # -------------------------------------------------------------------------
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
    u"""
    计算一组三维 Point / Vector 的算术平均值。

    Args:
        points (list[list[float] | tuple[float, float, float]]):
            需要求平均的三维 Point / Vector 集合。

    Returns:
        list[float] | None:
        平均 XYZ 值；输入为空时返回 None。

    Raises:
        ValueError:
        集合中的任意 Point / Vector 不是有效三维数值数据时抛出。
    """
    if not points:
        return None

    # -------------------------------------------------------------------------
    # Step 01：逐项验证三维数据，并累计 XYZ 三个轴的总值
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 02：使用实际有效输入数量计算三个轴的算术平均值
    # -------------------------------------------------------------------------
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
