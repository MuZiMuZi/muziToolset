# coding=utf-8
u"""
Matrix Utils
============

Maya Matrix / offsetParentMatrix 领域的通用底层工具。

模块职责
--------
这个模块专门处理 Matrix 数据和 Matrix DG Network，不负责传统 Maya Constraint。
目前主要用于创建基于 ``multMatrix + offsetParentMatrix`` 的 Parent Matrix Constraint。

当前公开方法
------------
    get_matrix(matrix_plug)
        读取 Maya Matrix Plug，并转换为 maya.api.OpenMaya.MMatrix。

    matrix_to_list(matrix)
        将 MMatrix 转换为 Maya setAttr(type="matrix") 可使用的 16 个数值。

    calculate_parent_offset_matrix(driver, driven)
        计算 Driven 当前相对 Driver 的 World Offset Matrix。

    get_parent(node)
        获取 DAG 节点直接父节点；World 下返回 None。

    create_parent_matrix_constraint(driver, driven, maintain_offset=True, name=None)
        使用 multMatrix + offsetParentMatrix 建立 Parent Matrix Constraint。

    remove_parent_matrix_constraint(driven, delete_node=True)
        断开 offsetParentMatrix 输入，并可删除对应 multMatrix。

核心计算关系
------------
保持 Offset 时：

    drivenLocalInverse
        * offsetMatrix
        * driverWorldMatrix
        * parentWorldInverseMatrix
        -> driven.offsetParentMatrix

为什么不用 driven.parentInverseMatrix
-------------------------------------
``offsetParentMatrix`` 会参与 Driven 自身 Transform Matrix 的求值。
如果网络又从同一个 Driven 的 ``parentInverseMatrix`` 取值并回写 OPM，
Maya Evaluation Graph 可能把这条网络判断为循环依赖。

因此当前实现使用：

    driven 的 Parent.worldInverseMatrix[0]

Driven 位于 World 下时，则不连接最后一项，multMatrix 默认 Identity。

本模块不负责
------------
- parentConstraint / pointConstraint / orientConstraint；
- UI；
- Controller Space Switch 的完整业务流程；
- Matrix Mirror / Blend 等更高层 Rig Workflow。

模块边界
--------
    Transform 数值读写         -> transform_utils
    Matrix / OPM DG 网络       -> matrix_utils
    Maya Constraint Node       -> constraint_utils
    Controller Follow / Space  -> systems.controller

设计原则
--------
1. Matrix 计算使用 Maya API 2.0 ``MMatrix``；
2. Maya DG 网络创建使用 ``maya.cmds``，方便调试和查看 Node Editor；
3. 创建网络前必须检查 Driven 的 offsetParentMatrix 是否已有输入；
4. 不静默覆盖已有 Matrix Rig；
5. 创建 Matrix Constraint 后如果重新 Parent Driven，应重新创建网络。
"""

from __future__ import print_function

import maya.api.OpenMaya as om
import maya.cmds as cmds


# =============================================================================
# Matrix Data - Matrix Plug 读取与格式转换
# =============================================================================

def get_matrix(matrix_plug):
    """
    读取 Maya Matrix Plug，并返回 ``maya.api.OpenMaya.MMatrix``。

    Args:
        matrix_plug(str):
            例如 ``ctrl.worldMatrix[0]``、``group.matrix``。

    Returns:
        maya.api.OpenMaya.MMatrix: 读取后的矩阵。
    """
    # 步骤 1：检查 Plug 参数。
    if not matrix_plug:
        raise ValueError(u"matrix_plug 不能为空。")

    # 步骤 2：确认 Maya 中真实存在这个属性。
    if not cmds.objExists(matrix_plug):
        raise RuntimeError(
            u"Matrix 属性不存在：{}".format(matrix_plug)
        )

    # 步骤 3：读取 Maya Matrix 数据。
    # 某些 Maya 版本会把 Matrix 包成 [(...16 values...)] 的形式，
    # 所以下面会统一拆成一层普通序列。
    matrix_value = cmds.getAttr(matrix_plug)

    if isinstance(matrix_value, (list, tuple)):
        if len(matrix_value) == 1:
            first_value = matrix_value[0]

            if isinstance(first_value, (list, tuple)):
                matrix_value = first_value

    # 步骤 4：转换成 MMatrix，后续可以直接 inverse / multiply。
    return om.MMatrix(matrix_value)


def matrix_to_list(matrix):
    """
    将 ``MMatrix`` 转换为 16 个浮点数的普通 list。

    Maya ``setAttr(..., type='matrix')`` 需要 16 个独立数值，
    因此在写入 multMatrix.matrixIn 时统一通过这个函数转换。
    """
    matrix_values = []

    # 步骤 1：按 MMatrix 的 16 个元素顺序展开。
    for index in range(16):
        matrix_values.append(matrix[index])

    # 步骤 2：返回普通 Python 数据。
    return matrix_values


def calculate_parent_offset_matrix(driver, driven):
    """
    计算 Driven 当前相对 Driver 的 World Offset Matrix。

    计算方式：

        drivenWorld * inverse(driverWorld)

    这个 Offset 会在 maintain_offset=True 时写入 multMatrix，
    用来保持建立约束前 Driven 当前的世界姿态。
    """
    # 步骤 1：确认 Driver 存在。
    if not cmds.objExists(driver):
        raise RuntimeError(
            u"Driver 不存在：{}".format(driver)
        )

    # 步骤 2：确认 Driven 存在。
    if not cmds.objExists(driven):
        raise RuntimeError(
            u"Driven 不存在：{}".format(driven)
        )

    # 步骤 3：读取 Driver / Driven 的 World Matrix。
    driver_world_matrix = get_matrix(
        driver + ".worldMatrix[0]"
    )
    driven_world_matrix = get_matrix(
        driven + ".worldMatrix[0]"
    )

    # 步骤 4：计算 Driver World 的逆矩阵。
    driver_world_inverse_matrix = driver_world_matrix.inverse()

    # 步骤 5：计算 Driven 相对 Driver 的 Offset。
    return (
        driven_world_matrix
        * driver_world_inverse_matrix
    )


def get_parent(node):
    """
    返回 DAG 节点的直接父节点。

    Returns:
        str/None:
            有 Parent 时返回完整 DAG Path；
            位于 World 下时返回 None。
    """
    # 步骤 1：节点不存在时直接返回 None。
    if not cmds.objExists(node):
        return None

    # 步骤 2：查询直接父节点，并要求 fullPath，避免同名 DAG 节点歧义。
    parents = cmds.listRelatives(
        node,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    # 步骤 3：没有父节点表示节点在 World 下。
    if not parents:
        return None

    return parents[0]


# =============================================================================
# offsetParentMatrix Constraint
# =============================================================================

def create_parent_matrix_constraint(
        driver,
        driven,
        maintain_offset=True,
        name=None
):
    """
    使用 ``multMatrix + offsetParentMatrix`` 创建 Parent Matrix Constraint。

    Args:
        driver(str): 驱动 Transform / Joint。
        driven(str): 被驱动 Transform / Joint。
        maintain_offset(bool): 是否保持建立前的相对位置。
        name(str/None): 可选 multMatrix 节点名称。

    Returns:
        str: 创建出的 multMatrix 节点。

    计算关系：
        drivenLocalInverse
        * offset
        * driverWorld
        * parentWorldInverse
        -> driven.offsetParentMatrix

    注意：
        不直接连接 ``driven.parentInverseMatrix[0]``。
        这是为了避免 Maya Evaluation Graph 把 Driven 自己的矩阵输出
        再回写自身 OPM 判断为潜在循环。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：检查 Driver / Driven。
    # -------------------------------------------------------------------------
    if not cmds.objExists(driver):
        raise RuntimeError(
            u"Driver 不存在：{}".format(driver)
        )

    if not cmds.objExists(driven):
        raise RuntimeError(
            u"Driven 不存在：{}".format(driven)
        )

    # -------------------------------------------------------------------------
    # 步骤 2：确认 Driven 支持 offsetParentMatrix。
    # -------------------------------------------------------------------------
    offset_parent_matrix_plug = (
        driven + ".offsetParentMatrix"
    )

    if not cmds.objExists(offset_parent_matrix_plug):
        raise RuntimeError(
            u"节点没有 offsetParentMatrix：{}".format(driven)
        )

    # -------------------------------------------------------------------------
    # 步骤 3：检查 OPM 是否已经被其它网络驱动。
    #
    # Core 不允许静默 force 覆盖已有 Rig，否则很容易破坏场景中原来的
    # Space Switch / Matrix Constraint。
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 4：计算 Driven Local Inverse。
    #
    # OPM 位于 Transform 局部矩阵计算链中，因此需要先抵消 Driven 当前
    # Local Matrix，避免连接后发生双重 Transform。
    # -------------------------------------------------------------------------
    driven_local_matrix = get_matrix(
        driven + ".matrix"
    )
    driven_local_inverse_matrix = driven_local_matrix.inverse()

    # -------------------------------------------------------------------------
    # 步骤 5：根据 maintain_offset 决定 Offset Matrix。
    # -------------------------------------------------------------------------
    if maintain_offset:
        offset_matrix = calculate_parent_offset_matrix(
            driver,
            driven
        )
    else:
        # MMatrix() 默认是 Identity Matrix。
        offset_matrix = om.MMatrix()

    # -------------------------------------------------------------------------
    # 步骤 6：生成 multMatrix 名称并创建节点。
    # -------------------------------------------------------------------------
    if name is None:
        driven_short_name = driven.split("|")[-1]
        driven_short_name = driven_short_name.replace(":", "_")
        name = driven_short_name + "_parent_mm"

    mult_matrix = cmds.createNode(
        "multMatrix",
        name=name
    )

    # -------------------------------------------------------------------------
    # 步骤 7：把静态矩阵写入 matrixIn[0] / matrixIn[1]。
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 8：连接 Driver World Matrix。
    # -------------------------------------------------------------------------
    cmds.connectAttr(
        driver + ".worldMatrix[0]",
        mult_matrix + ".matrixIn[2]",
        force=True
    )

    # -------------------------------------------------------------------------
    # 步骤 9：如果 Driven 有 Parent，连接 Parent World Inverse。
    #
    # 注意这里故意不使用 driven.parentInverseMatrix[0]，原因见模块说明。
    # -------------------------------------------------------------------------
    driven_parent = get_parent(driven)

    if driven_parent:
        cmds.connectAttr(
            driven_parent + ".worldInverseMatrix[0]",
            mult_matrix + ".matrixIn[3]",
            force=True
        )

    # -------------------------------------------------------------------------
    # 步骤 10：最终 Matrix Sum 驱动 offsetParentMatrix。
    # -------------------------------------------------------------------------
    cmds.connectAttr(
        mult_matrix + ".matrixSum",
        offset_parent_matrix_plug,
        force=True
    )

    return mult_matrix


def remove_parent_matrix_constraint(driven, delete_node=True):
    """
    断开 Driven 的 offsetParentMatrix 输入。

    Args:
        driven(str): 被驱动节点。
        delete_node(bool):
            True 时，如果输入节点是 multMatrix，则一并删除该节点。

    Returns:
        bool: 成功断开时返回 True；没有输入或失败时返回 False。

    Note:
        本函数只负责断开网络，不修改 Driven 当前 TRS 数值。
    """
    # 步骤 1：Driven 不存在时没有任何可清理内容。
    if not cmds.objExists(driven):
        return False

    offset_parent_matrix_plug = driven + ".offsetParentMatrix"

    # 步骤 2：确认节点有 OPM。
    if not cmds.objExists(offset_parent_matrix_plug):
        return False

    # 步骤 3：查询当前 OPM 输入 Plug。
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

    # 步骤 4：先断开连接。
    try:
        cmds.disconnectAttr(
            source_plug,
            offset_parent_matrix_plug
        )
    except RuntimeError:
        return False

    # 步骤 5：按需要清理 multMatrix。
    # 这里只删除明确确认类型为 multMatrix 的输入节点，避免误删其它网络。
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
