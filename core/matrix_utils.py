# coding=utf-8
u"""
Matrix Utils
============

Maya Matrix / offsetParentMatrix 领域的通用底层工具。

模块职责
--------
本模块专门处理 Matrix 数据和 Matrix DG Network，不负责传统 Maya Constraint。
目前主要用于创建基于 ``multMatrix + offsetParentMatrix`` 的 Parent Matrix Constraint。

模块边界
--------
- 节点存在性统一复用 scene_utils；
- DAG Parent 查询统一复用 hierarchy_utils；
- DAG Short Name 统一复用 rename_utils；
- Plug 查询 / 连接 / 断开统一复用 connection_utils；
- MMatrix 数学和 Matrix DG Network 保留在本模块。
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
    u"""读取 Maya Matrix Plug，并返回 maya.api.OpenMaya.MMatrix。"""
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
    u"""将 MMatrix 转换为 16 个数值的普通 list。"""
    matrix_values = []

    for index in range(16):
        matrix_values.append(
            matrix[index]
        )

    return matrix_values


def calculate_parent_offset_matrix(driver, driven):
    u"""
    计算 Driven 当前相对 Driver 的 World Offset Matrix。

    计算：
        drivenWorld * inverse(driverWorld)
    """
    # 使用 Scene Core 统一验证 Driver。
    scene_utils.validate_node(
        driver
    )

    # 使用 Scene Core 统一验证 Driven。
    scene_utils.validate_node(
        driven
    )

    # 读取 Driver / Driven 的 World Matrix。
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
    u"""
    兼容旧调用的直接 Parent 查询入口。

    真正 DAG Parent 查询统一由 hierarchy_utils.Hierarchy.get_parent 维护。
    """
    if not node:
        return None

    if not cmds.objExists(node):
        return None

    # 使用 Hierarchy Core 查询直接 Parent Long Path。
    return hierarchy_utils.Hierarchy.get_parent(
        node,
        full_path=True
    )


# =============================================================================
# offsetParentMatrix Constraint
# =============================================================================

def create_parent_matrix_constraint(
        driver,
        driven,
        maintain_offset=True,
        name=None
):
    u"""
    使用 ``multMatrix + offsetParentMatrix`` 创建 Parent Matrix Constraint。

    计算关系：
        drivenLocalInverse
        * offset
        * driverWorld
        * parentWorldInverse
        -> driven.offsetParentMatrix
    """
    # 使用 Scene Core 统一验证 Driver。
    scene_utils.validate_node(
        driver
    )

    # 使用 Scene Core 统一验证 Driven。
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

    # 使用 Connection Core 查询 OPM 是否已经被其它网络驱动。
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

    # 读取 Driven 当前 Local Matrix，并计算其逆矩阵。
    driven_local_matrix = get_matrix(
        driven + ".matrix"
    )
    driven_local_inverse_matrix = driven_local_matrix.inverse()

    if maintain_offset:
        # 需要保持偏移时计算 Driver / Driven 当前 World Offset。
        offset_matrix = calculate_parent_offset_matrix(
            driver,
            driven
        )
    else:
        # 不保持偏移时使用 Identity Matrix。
        offset_matrix = om.MMatrix()

    if name is None:
        # 使用 Rename Core 统一取得 Driven Short Name。
        driven_short_name = rename_utils.get_short_name(
            driven
        )
        driven_short_name = driven_short_name.replace(
            ":",
            "_"
        )
        name = driven_short_name + "_parent_mm"

    # 创建 Matrix Constraint 的核心 multMatrix 节点。
    mult_matrix = cmds.createNode(
        "multMatrix",
        name=name
    )

    # 转换静态矩阵为 Maya setAttr 可以接收的普通数值。
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

    # 使用 Connection Core 连接 Driver World Matrix。
    connection_utils.connect_plugs(
        driver + ".worldMatrix[0]",
        mult_matrix + ".matrixIn[2]",
        force=True
    )

    # 使用统一 Parent API 获取 Driven Parent。
    driven_parent = get_parent(
        driven
    )

    if driven_parent:
        # 有 Parent 时把 Parent World Inverse 接入 Local Space 转换。
        connection_utils.connect_plugs(
            driven_parent + ".worldInverseMatrix[0]",
            mult_matrix + ".matrixIn[3]",
            force=True
        )

    # 最终 Matrix Sum 驱动 Driven offsetParentMatrix。
    connection_utils.connect_plugs(
        mult_matrix + ".matrixSum",
        offset_parent_matrix_plug,
        force=True
    )

    return mult_matrix


def remove_parent_matrix_constraint(
        driven,
        delete_node=True
):
    u"""
    断开 Driven 的 offsetParentMatrix 输入。

    本方法是可选清理操作，因此目标不存在时返回 False，而不是抛异常。
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

    # 使用 Connection Core 查询当前 OPM 输入。
    input_plugs = connection_utils.get_input_connections(
        offset_parent_matrix_plug
    )

    if not input_plugs:
        return False

    source_plug = input_plugs[0]
    source_node = source_plug.split(".")[0]

    # 使用 Connection Core 断开当前 Matrix 输入。
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
    "get_parent",
    "create_parent_matrix_constraint",
    "remove_parent_matrix_constraint",
]
