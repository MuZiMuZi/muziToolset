# coding=utf-8
u"""
Matrix Utils
============

Maya Matrix 数据、矩阵计算和通用 Matrix DG Network 底层工具。

模块职责
--------
- Matrix Plug -> MMatrix；
- MMatrix -> 普通 16 数值 list；
- 通用 Matrix Offset 计算；
- 基于 multMatrix + offsetParentMatrix 的通用 Parent Matrix Network。

模块边界
--------
- Transform World Matrix 读取 / 写入 -> transform_utils；
- DAG Parent 查询 -> hierarchy_utils；
- Plug 查询 / 连接 / 断开 -> connection_utils；
- Maya 原生 Constraint -> constraint_utils；
- Face / Body 专属 Matrix Graph -> systems。
"""

from __future__ import print_function

import maya.api.OpenMaya as om
import maya.cmds as cmds

from . import connection_utils
from . import hierarchy_utils
from . import rename_utils
from . import scene_utils


# =============================================================================
# Matrix Data
# =============================================================================

def get_matrix(matrix_plug):
    u"""
    读取 Maya Matrix Plug，并返回 maya.api.OpenMaya.MMatrix。

    例如：
        node.worldMatrix[0]
        multMatrix1.matrixSum

    Args:
        matrix_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        object:
            方法执行后的结果数据。

    Raises:
        ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    if not matrix_plug:
        raise ValueError(
            u"matrix_plug 不能为空。"
        )

    if not cmds.objExists(matrix_plug):
        raise RuntimeError(
            u"Matrix 属性不存在：{}".format(
                matrix_plug
            )
        )

    matrix_value = cmds.getAttr(
        matrix_plug
    )

    if isinstance(matrix_value, (list, tuple)):
        if len(matrix_value) == 1:
            first_value = matrix_value[0]

            if isinstance(first_value, (list, tuple)):
                matrix_value = first_value

    return om.MMatrix(
        matrix_value
    )


def matrix_to_list(matrix):
    u"""
    将 MMatrix 转换为 16 个数值的普通 list。

    Args:
        matrix (list[float] | maya.api.OpenMaya.MMatrix):
            用于 Transform、Constraint 或空间计算的 4x4 Matrix 数据。

    Returns:
        object:
            方法执行后的结果数据。
    """
    matrix_values = []

    for index in range(16):
        matrix_values.append(
            matrix[index]
        )

    return matrix_values


# =============================================================================
# Matrix Math
# =============================================================================

def calculate_parent_offset_matrix(driver, driven):
    u"""
    计算 Driven 当前相对 Driver 的 World Offset Matrix。

    计算：
        drivenWorld * inverse(driverWorld)

    Args:
        driver (str):
            作为驱动端的 Maya 节点名称。
        driven (str):
            作为被驱动端的 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """
    scene_utils.validate_node(
        driver
    )
    scene_utils.validate_node(
        driven
    )

    driver_world_matrix = get_matrix(
        driver + ".worldMatrix[0]"
    )
    driven_world_matrix = get_matrix(
        driven + ".worldMatrix[0]"
    )

    driver_world_inverse_matrix = driver_world_matrix.inverse()

    return (
        driven_world_matrix
        * driver_world_inverse_matrix
    )


# =============================================================================
# offsetParentMatrix Network
# =============================================================================

def create_parent_matrix_constraint(
        driver,
        driven,
        maintain_offset=True,
        name=None
):
    u"""
    使用 multMatrix + offsetParentMatrix 创建通用 Parent Matrix Network。

    Args:
        driver (str):
            作为驱动端的 Maya 节点名称。
        driven (str):
            作为被驱动端的 Maya 节点名称。
        maintain_offset (bool):
            是否在建立约束或矩阵关系时保持当前偏移。
        name (str):
            创建或查询时使用的节点名称。

    Returns:
        object:
            方法执行后的结果数据。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    scene_utils.validate_node(
        driver
    )
    scene_utils.validate_node(
        driven
    )

    offset_parent_matrix_plug = (
        driven + ".offsetParentMatrix"
    )

    if not cmds.objExists(offset_parent_matrix_plug):
        raise RuntimeError(
            u"节点没有 offsetParentMatrix：{}".format(
                driven
            )
        )

    existing_inputs = connection_utils.get_input_connections(
        offset_parent_matrix_plug
    )

    if existing_inputs:
        raise RuntimeError(
            u"offsetParentMatrix 已经存在输入连接：{} <- {}".format(
                offset_parent_matrix_plug,
                existing_inputs[0]
            )
        )

    driven_local_matrix = get_matrix(
        driven + ".matrix"
    )
    driven_local_inverse_matrix = driven_local_matrix.inverse()

    if maintain_offset:
        offset_matrix = calculate_parent_offset_matrix(
            driver,
            driven
        )
    else:
        offset_matrix = om.MMatrix()

    if name is None:
        driven_short_name = rename_utils.get_short_name(
            driven
        )
        driven_short_name = driven_short_name.replace(
            ":",
            "_"
        )
        name = driven_short_name + "_parent_mm"

    mult_matrix = cmds.createNode(
        "multMatrix",
        name=name
    )

    driven_local_inverse_values = matrix_to_list(
        driven_local_inverse_matrix
    )
    offset_matrix_values = matrix_to_list(
        offset_matrix
    )

    cmds.setAttr(
        mult_matrix + ".matrixIn[0]",
        *driven_local_inverse_values,
        type="matrix"
    )
    cmds.setAttr(
        mult_matrix + ".matrixIn[1]",
        *offset_matrix_values,
        type="matrix"
    )

    connection_utils.connect_plugs(
        driver + ".worldMatrix[0]",
        mult_matrix + ".matrixIn[2]",
        force=True
    )

    driven_parent = hierarchy_utils.get_parent(
        driven,
        full_path=True
    )

    if driven_parent:
        connection_utils.connect_plugs(
            driven_parent + ".worldInverseMatrix[0]",
            mult_matrix + ".matrixIn[3]",
            force=True
        )

    connection_utils.connect_plugs(
        mult_matrix + ".matrixSum",
        offset_parent_matrix_plug,
        force=True
    )

    return mult_matrix


def remove_parent_matrix_constraint(
        driven,
        delete_node=False
):
    u"""
    断开 Driven 的 offsetParentMatrix 输入。

    默认只断开连接，不删除来源节点。只有调用者明确确认来源节点属于当前
    Matrix Network 时，才应传入 ``delete_node=True``。

    Args:
        driven (str):
            作为被驱动端的 Maya 节点名称。
        delete_node (bool):
            当前清理 / 重建流程是否执行 `delete_node` 对应的删除步骤。

    Returns:
        bool:
            方法执行后的结果数据。
    """
    if not driven:
        return False

    if not cmds.objExists(driven):
        return False

    offset_parent_matrix_plug = (
        driven + ".offsetParentMatrix"
    )

    if not cmds.objExists(offset_parent_matrix_plug):
        return False

    input_plugs = connection_utils.get_input_connections(
        offset_parent_matrix_plug
    )

    if not input_plugs:
        return False

    source_plug = input_plugs[0]
    source_node = source_plug.split(".")[0]

    disconnected = connection_utils.disconnect_plugs(
        source_plug,
        offset_parent_matrix_plug
    )

    if not disconnected:
        return False

    if delete_node:
        if cmds.objExists(source_node):
            if cmds.nodeType(source_node) == "multMatrix":
                cmds.delete(
                    source_node
                )

    return True


__all__ = [
    "get_matrix",
    "matrix_to_list",
    "calculate_parent_offset_matrix",
    "create_parent_matrix_constraint",
    "remove_parent_matrix_constraint",
]
