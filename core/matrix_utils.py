# coding=utf-8
u"""
Matrix Utils
============

Maya Matrix / offsetParentMatrix 底层工具。

职责：
    1. 读取 Maya Matrix Plug；
    2. 在 MMatrix 和 Maya setAttr 数据之间转换；
    3. 计算 Parent Matrix Constraint 的 Offset；
    4. 使用 multMatrix + offsetParentMatrix 创建 Parent Matrix Constraint。

本模块不创建 UI，也不负责传统 parentConstraint / pointConstraint 等命令式约束。
"""

from __future__ import print_function

import maya.api.OpenMaya as om
import maya.cmds as cmds


# =============================================================================
# Matrix data
# =============================================================================

def get_matrix(matrix_plug):
    """读取 Matrix Plug，并返回 maya.api.OpenMaya.MMatrix。"""
    if not matrix_plug:
        raise ValueError(u"matrix_plug 不能为空。")

    if not cmds.objExists(matrix_plug):
        raise RuntimeError(
            u"Matrix 属性不存在：{}".format(matrix_plug)
        )

    matrix_value = cmds.getAttr(matrix_plug)

    if isinstance(matrix_value, (list, tuple)):
        if len(matrix_value) == 1:
            first_value = matrix_value[0]

            if isinstance(first_value, (list, tuple)):
                matrix_value = first_value

    return om.MMatrix(matrix_value)


def matrix_to_list(matrix):
    """将 MMatrix 转换为 Maya setAttr 可使用的 16 个浮点数。"""
    matrix_values = []

    for index in range(16):
        matrix_values.append(matrix[index])

    return matrix_values


def calculate_parent_offset_matrix(driver, driven):
    """计算 Driven 当前相对 Driver 的 World Offset Matrix。"""
    if not cmds.objExists(driver):
        raise RuntimeError(
            u"Driver 不存在：{}".format(driver)
        )

    if not cmds.objExists(driven):
        raise RuntimeError(
            u"Driven 不存在：{}".format(driven)
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


def get_parent(node):
    """返回 DAG 节点的直接父节点；World 下返回 None。"""
    if not cmds.objExists(node):
        return None

    parents = cmds.listRelatives(
        node,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    if not parents:
        return None

    return parents[0]


# =============================================================================
# offsetParentMatrix constraint
# =============================================================================

def create_parent_matrix_constraint(
        driver,
        driven,
        maintain_offset=True,
        name=None
):
    """
    使用 multMatrix + offsetParentMatrix 创建 Parent Matrix Constraint。

    计算关系：

        drivenLocalInverse
        * offset
        * driverWorld
        * parentWorldInverse
        -> driven.offsetParentMatrix

    注意：
        不直接连接 driven.parentInverseMatrix[0]。

        offsetParentMatrix 本身会参与 Driven Transform 的矩阵计算，如果同时
        从同一个 Driven 的 parentInverseMatrix 输出回读到 multMatrix，Maya
        Evaluation Graph 可能将网络判断为循环依赖。

        因此这里在 Driven 有父节点时直接读取父节点的
        worldInverseMatrix[0]；Driven 位于 World 下时最后一项保持 Identity。

        如果创建 Matrix Constraint 后重新 Parent Driven，应重新创建这条
        Matrix Constraint，让网络连接到新的 Parent。

    Args:
        driver(str): 驱动 Transform / Joint。
        driven(str): 被驱动 Transform / Joint。
        maintain_offset(bool): 是否保持创建前的相对位置。
        name(str): 可选的 multMatrix 节点名称。

    Returns:
        str: 创建出来的 multMatrix 节点。
    """
    if not cmds.objExists(driver):
        raise RuntimeError(
            u"Driver 不存在：{}".format(driver)
        )

    if not cmds.objExists(driven):
        raise RuntimeError(
            u"Driven 不存在：{}".format(driven)
        )

    offset_parent_matrix_plug = (
        driven + ".offsetParentMatrix"
    )

    if not cmds.objExists(offset_parent_matrix_plug):
        raise RuntimeError(
            u"节点没有 offsetParentMatrix：{}".format(driven)
        )

    existing_inputs = cmds.listConnections(
        offset_parent_matrix_plug,
        source=True,
        destination=False,
        plugs=True
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
        driven_short_name = driven.split("|")[-1]
        driven_short_name = driven_short_name.replace(":", "_")
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

    cmds.connectAttr(
        driver + ".worldMatrix[0]",
        mult_matrix + ".matrixIn[2]",
        force=True
    )

    driven_parent = get_parent(driven)

    if driven_parent:
        cmds.connectAttr(
            driven_parent + ".worldInverseMatrix[0]",
            mult_matrix + ".matrixIn[3]",
            force=True
        )

    cmds.connectAttr(
        mult_matrix + ".matrixSum",
        offset_parent_matrix_plug,
        force=True
    )

    return mult_matrix


def remove_parent_matrix_constraint(driven, delete_node=True):
    """
    断开 Driven 的 offsetParentMatrix 输入。

    如果输入节点是 multMatrix 且 delete_node=True，则一并删除该节点。
    不修改 Driven 的 TRS 数值。
    """
    if not cmds.objExists(driven):
        return False

    offset_parent_matrix_plug = driven + ".offsetParentMatrix"

    if not cmds.objExists(offset_parent_matrix_plug):
        return False

    input_plugs = cmds.listConnections(
        offset_parent_matrix_plug,
        source=True,
        destination=False,
        plugs=True
    )

    if input_plugs is None:
        input_plugs = []

    if not input_plugs:
        return False

    source_plug = input_plugs[0]
    source_node = source_plug.split(".")[0]

    try:
        cmds.disconnectAttr(
            source_plug,
            offset_parent_matrix_plug
        )
    except RuntimeError:
        return False

    if delete_node:
        if cmds.objExists(source_node):
            if cmds.nodeType(source_node) == "multMatrix":
                cmds.delete(source_node)

    return True


__all__ = [
    "get_matrix",
    "matrix_to_list",
    "calculate_parent_offset_matrix",
    "get_parent",
    "create_parent_matrix_constraint",
    "remove_parent_matrix_constraint",
]
