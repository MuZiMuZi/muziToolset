# coding=utf-8
u"""
Curve Utils
===========

Maya NURBS Curve 领域的通用底层工具。

模块职责
--------
这个模块只处理 NURBS Curve 的“查询、采样、Parameter 换算、附着和基础创建”。
Joint、Face、Lip、Eyelid 等更高层绑定逻辑继续放在对应 Core / System 中。

当前公开方法
------------
基础校验与查询：
    scene_utils.validate_node(node)
        检查 Maya 节点是否存在。

    get_curve_shape(curve)
        获取 NURBS Curve Shape 的完整 DAG Path。

    get_curve_transform(curve)
        获取 Curve Transform 的完整 DAG Path。

    get_curve_cvs(curve)
        获取 Curve 全部 CV Component。

    get_curve_cv_count(curve)
        获取 Curve CV 数量。

    get_curve_cv_positions(curve, world_space=True)
        获取 Curve 全部 CV 的坐标。

Maya API：
    get_dag_path(node)
        将 Maya 节点转换为 API 2.0 MDagPath。

    get_curve_function(curve)
        获取 API 2.0 MFnNurbsCurve。

弧长采样与 Parameter：
    get_even_percentages(sample_count)
        生成 0~1 的等间距百分比。

    sample_curve_by_length(curve, sample_count, world_space=True)
        按实际弧长均匀采样 Point / Tangent / Parameter。

    get_closest_parameter(curve, world_position)
        获取世界坐标在 Curve 上最近位置对应的原始 Parameter。

    parameter_to_length_percentage(curve, parameter)
        将 Curve 原始 Parameter 转为 0~1 弧长百分比。

    length_percentage_to_parameter(curve, percentage)
        将 0~1 弧长百分比转回 Curve 原始 Parameter。

Curve Attachment：
    create_point_on_curve_attachment(curve, parameter, name, parent=None)
        创建由 pointOnCurveInfo 驱动的 Transform Attachment。

    create_closest_point_attachment(curve, world_position, name, parent=None)
        在距离指定世界位置最近的 Curve 位置创建 Attachment。

Curve 创建：
    create_curve_from_nodes(nodes, name, degree=3)
        根据一组 Maya 节点的世界位置创建 NURBS Curve。

    create_curve_from_selected_edges(name, degree=3, form=2)
        根据当前 Polygon Edge Selection 创建 Curve。

为什么需要“Parameter”和“弧长百分比”两套概念
---------------------------------------------
Maya NURBS Curve 的原始 Parameter 并不保证是 0~1，也不保证不同 Curve 的
Parameter Domain 相同。

因此当多条 Curve 需要“同一个空间进度”时，不能直接复制 raw parameter：

    Drive Curve Parameter
        -> 转成弧长百分比 0~1
        -> 在 Aim / Up Curve 上重新换算 Parameter

Face Eyelid / Lip / Curve Attachment 会依赖这个规则。

本模块不负责
------------
- Joint 创建和 Joint Orient；
- Face / Eyelid / Lip 的完整绑定；
- Ribbon / Spline IK Workflow；
- Curve UI Tool；
- Surface / Follicle。

模块边界
--------
    Curve 数据 / 采样 / Attachment  -> curve_utils
    NURBS Surface / Follicle         -> surface_utils
    Joint on Curve                   -> jointUtils / 对应 System
    Face Curve Rig                   -> systems.face

设计原则
--------
1. 通用 Curve 数据优先使用 Maya API 2.0；
2. Maya DG Attachment 使用 maya.cmds，方便在 Node Editor 检查网络；
3. 多 Curve 同步时优先使用“弧长百分比”，不共享 raw parameter；
4. Attachment 有 Parent 时必须做 World -> Local 转换，不能把世界坐标直接接 local translate；
5. 不把 Selection 逻辑混进普通 Core API，只有明确命名为 selected 的函数才读取 Selection。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import scene_utils
import maya.api.OpenMaya as om


# =============================================================================
# Validate / Query - Curve 基础校验与查询
# =============================================================================


def get_curve_shape(curve):
    u"""

        返回 NURBS Curve Shape 的完整 DAG Path。

        ``curve`` 可以直接传 Transform，也可以直接传 nurbsCurve Shape。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # -------------------------------------------------------------------------
    # 步骤 1：确认输入节点存在。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    scene_utils.validate_node(curve)

    # -------------------------------------------------------------------------
    # 步骤 2：输入本身就是 nurbsCurve Shape 时直接返回 Long Name。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if cmds.nodeType(curve) == "nurbsCurve":
        matches = cmds.ls(
            curve,
            long=True
        )

        if matches:
            return matches[0]

        return curve

    # -------------------------------------------------------------------------
    # 步骤 3：输入是 Transform 时，寻找非 Intermediate 的 nurbsCurve Shape。
    # -------------------------------------------------------------------------
    shapes = cmds.listRelatives(
        curve,
        shapes=True,
        noIntermediate=True,
        fullPath=True
    )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if shapes is None:
        shapes = []

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for shape in shapes:
        if cmds.nodeType(shape) == "nurbsCurve":
            return shape

    # 步骤 4：没有找到 Curve Shape 时明确报错，不返回 None 让后续函数继续失败。
    # -------------------------------------------------------------------------
    # Step 05：根据无效输入或场景状态抛出明确异常
    # -------------------------------------------------------------------------
    raise RuntimeError(
        u"节点不是 NURBS Curve：{}".format(curve)
    )


def get_curve_transform(curve):
    u"""

        返回 NURBS Curve Transform 的完整 DAG Path。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # 步骤 1：先统一取得 Curve Shape。
    curve_shape = get_curve_shape(curve)

    # 步骤 2：查询 Shape Parent。
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
    u"""

        返回 Curve 全部 CV Component 名称。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    # 步骤 1：取得唯一 Shape Path。
    curve_shape = get_curve_shape(curve)

    # 步骤 2：展开 cv[*] Component。
    curve_cvs = cmds.ls(
        curve_shape + ".cv[*]",
        flatten=True
    )

    if curve_cvs is None:
        curve_cvs = []

    return curve_cvs


def get_curve_cv_count(curve):
    u"""

        返回 Curve CV 数量。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    curve_cvs = get_curve_cvs(curve)
    return len(curve_cvs)


def get_curve_cv_positions(
        curve,
        world_space=True
):
    u"""

        返回 Curve 全部 CV 坐标。

        Args:
            curve (str):
                Curve Transform 或 Shape。
            world_space (bool):
                True 返回世界坐标；False 返回局部坐标。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    curve_cvs = get_curve_cvs(curve)
    positions = []

    # 步骤 1：逐 CV 查询坐标。
    for curve_cv in curve_cvs:
        position = cmds.xform(
            curve_cv,
            query=True,
            worldSpace=world_space,
            translation=True
        )

        positions.append(position)

    # 步骤 2：返回普通 Python list，方便 JSON / Test / System 使用。
    return positions


# =============================================================================
# Maya API - Curve Function Set
# =============================================================================

def get_dag_path(node):
    u"""

        返回 Maya API 2.0 ``MDagPath``。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    # 步骤 1：确认节点存在。
    scene_utils.validate_node(node)

    # 步骤 2：通过 SelectionList 取得 DagPath。
    selection = om.MSelectionList()
    selection.add(node)

    return selection.getDagPath(0)


def get_curve_function(curve):
    u"""

        返回 Maya API 2.0 ``MFnNurbsCurve``。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    """
    # 步骤 1：取得 Curve Shape。
    curve_shape = get_curve_shape(curve)

    # 步骤 2：Shape -> DagPath -> MFnNurbsCurve。
    dag_path = get_dag_path(curve_shape)
    return om.MFnNurbsCurve(dag_path)


# =============================================================================
# Sample - 弧长采样与 Parameter 换算
# =============================================================================

def get_even_percentages(sample_count):
    u"""

        返回包含头尾的 0~1 等间距百分比。

        Args:
            sample_count (int):
                当前构建、采样或查询过程使用的元素数量。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。

        Example:
            get_even_percentages(5)
                                                                            -> [0.0, 0.25, 0.5, 0.75, 1.0]

    """
    # 步骤 1：至少需要首尾两个采样点。
    if sample_count < 2:
        raise ValueError(
            u"sample_count 必须大于或等于 2。"
        )

    # 步骤 2：计算相邻百分比间距。
    percentages = []
    gap = 1.0 / float(sample_count - 1)

    # 步骤 3：使用普通 while 保证每一步易于调试。
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
    u"""
    按 Curve 实际弧长均匀采样 Point、Tangent 和原始 Parameter。

    Args:
        curve (str):
            需要处理的 Maya Curve Transform 或 Shape 名称。
        sample_count (int):
            当前构建、采样或查询过程使用的元素数量。
        world_space (bool):
            是否使用 Maya World Space，而不是 Local / Parent Space。

    Returns:
        dict:
        {
        "points": [[x, y, z], ...],
        "tangents": [[x, y, z], ...],
        "parameters": [float, ...],
        }
    """
    # -------------------------------------------------------------------------
    # 步骤 1：准备 Curve API Function 和等分百分比。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    curve_function = get_curve_function(curve)
    percentages = get_even_percentages(sample_count)

    # -------------------------------------------------------------------------
    # 步骤 2：确定 API 查询空间。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    space = om.MSpace.kObject

    if world_space:
        space = om.MSpace.kWorld

    # -------------------------------------------------------------------------
    # 步骤 3：取得 Curve 总弧长。
    # -------------------------------------------------------------------------
    curve_length = curve_function.length()

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    points = []
    tangents = []
    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    parameters = []

    # -------------------------------------------------------------------------
    # 步骤 4：百分比 -> 实际长度 -> 原始 Parameter -> Point / Tangent。
    #
    # 这和直接平均 Parameter 不同，可以真正得到空间上均匀的采样点。
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return {
        "points": points,
        "tangents": tangents,
        "parameters": parameters,
    }


def get_closest_parameter(
        curve,
        world_position
):
    u"""

        返回世界坐标在 Curve 上最近点对应的原始 Parameter。

        这里使用临时 ``nearestPointOnCurve`` 节点。
        原因是后续 ``pointOnCurveInfo.parameter`` 需要 Maya Curve 的原始 Parameter，
        而不是简单的 0~1 百分比。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。
            world_position (list[float] | tuple[float, float, float]):
                用于 Curve 最近点、参数查询或节点放置的 World Space Position。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # 步骤 1：验证世界坐标格式。
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if world_position is None:
        raise ValueError(u"world_position 不能为空。")

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if len(world_position) != 3:
        raise ValueError(u"world_position 必须包含 x / y / z 三个数值。")

    # 步骤 2：取得 Curve Shape 并创建临时查询节点。
    curve_shape = get_curve_shape(curve)
    # -------------------------------------------------------------------------
    # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    nearest_node = cmds.createNode(
        "nearestPointOnCurve"
    )

    # -------------------------------------------------------------------------
    # Step 04：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        # 步骤 3：连接世界空间 Curve，并写入查询位置。
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

        # 步骤 4：读取最近位置对应的 Parameter。
        parameter = cmds.getAttr(
            nearest_node + ".parameter"
        )

    finally:
        # 步骤 5：查询节点只用于一次计算，必须清理，不能污染用户场景。
        if cmds.objExists(nearest_node):
            cmds.delete(nearest_node)

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return parameter


def parameter_to_length_percentage(
        curve,
        parameter
):
    u"""

        将 Curve 原始 Parameter 转换成 0~1 弧长百分比。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。
            parameter (float):
                NURBS Curve / Surface 参数空间中的 Parameter 值。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # 步骤 1：取得 API Function 和总弧长。
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    curve_function = get_curve_function(curve)
    curve_length = curve_function.length()

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if curve_length <= 0.000001:
        raise RuntimeError(
            u"Curve 长度为 0，无法换算 Parameter：{}".format(
                curve
            )
        )

    # 步骤 2：计算该 Parameter 对应的弧长。
    parameter_length = curve_function.findLengthFromParam(
        parameter
    )

    # 步骤 3：转换成 0~1 百分比。
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    percentage = parameter_length / curve_length

    # 数值误差可能产生极小越界，最终 Clamp 到 0~1。
    if percentage < 0.0:
        percentage = 0.0

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if percentage > 1.0:
        percentage = 1.0

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return percentage


def length_percentage_to_parameter(
        curve,
        percentage
):
    u"""

        将 0~1 弧长百分比转换成 Curve 原始 Parameter。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。
            percentage (float):
                沿 Curve 或数据范围的归一化百分比，通常为 0.0～1.0。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # 步骤 1：统一成 float，并验证范围。
    percentage = float(percentage)

    if percentage < 0.0 or percentage > 1.0:
        raise ValueError(
            u"percentage 必须在 0~1 范围内：{}".format(
                percentage
            )
        )

    # 步骤 2：百分比 -> 目标弧长。
    curve_function = get_curve_function(curve)
    curve_length = curve_function.length()
    target_length = curve_length * percentage

    # 步骤 3：目标弧长 -> 原始 Parameter。
    return curve_function.findParamFromLength(
        target_length
    )


# =============================================================================
# Attach - Curve Attachment
# =============================================================================

def create_point_on_curve_attachment(
        curve,
        parameter,
        name,
        parent=None
):
    u"""
    创建由 ``pointOnCurveInfo`` 驱动的 Transform Attachment。

    Parent=None：
        pointOnCurveInfo.position
            -> attachment.translate
    有 Parent：
        pointOnCurveInfo.position          # 世界位置
            -> composeMatrix
            -> multMatrix
               × parent.worldInverseMatrix # World -> Parent Local
            -> decomposeMatrix
            -> attachment.translate
    为什么有 Parent 时不能直接连接：
        ``pointOnCurveInfo.position`` 来自 worldSpace Curve，结果是世界坐标；
        子节点 ``translate`` 是 Parent Local 坐标。直接连接会发生空间不匹配。

    Args:
        curve (str):
            需要处理的 Maya Curve Transform 或 Shape 名称。
        parameter (float):
            NURBS Curve / Surface 参数空间中的 Parameter 值。
        name (str):
            创建或查询时使用的节点名称。
        parent (str):
            父级 Maya 节点名称。

    Returns:
        dict:
        transform / point_on_curve / matrix_nodes / parameter。
    """
    # 步骤 1：取得 Curve Shape，并校验可选 Parent。
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    curve_shape = get_curve_shape(curve)

    if parent is not None:
        scene_utils.validate_node(parent)

    # 步骤 2：创建 Attachment Transform。
    # -------------------------------------------------------------------------
    # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    attachment = cmds.createNode(
        "transform",
        name=name,
        parent=parent
    )

    # 步骤 3：创建 pointOnCurveInfo 并连接 worldSpace Curve。
    point_on_curve = cmds.createNode(
        "pointOnCurveInfo",
        name="poci_{}".format(name)
    )

    # -------------------------------------------------------------------------
    # Step 03：建立当前阶段需要的层级、连接或驱动关系
    # -------------------------------------------------------------------------
    cmds.connectAttr(
        curve_shape + ".worldSpace[0]",
        point_on_curve + ".inputCurve",
        force=True
    )

    cmds.setAttr(
        point_on_curve + ".parameter",
        parameter
    )

    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    matrix_nodes = []

    # -------------------------------------------------------------------------
    # 步骤 4A：World 下的 Attachment 可以直接接世界 Position。
    # -------------------------------------------------------------------------
    if parent is None:
        cmds.connectAttr(
            point_on_curve + ".position",
            attachment + ".translate",
            force=True
        )

    # -------------------------------------------------------------------------
    # 步骤 4B：有 Parent 时建立 World -> Local Matrix 网络。
    # -------------------------------------------------------------------------
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

        # 世界 Position 先组成 Matrix。
        cmds.connectAttr(
            point_on_curve + ".position",
            compose_matrix + ".inputTranslate",
            force=True
        )

        # 世界 Matrix × Parent World Inverse = Parent Local Matrix。
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

        # Local Matrix 再拆成 Local Translate。
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

    # 步骤 5：返回完整构建结果，让 System 可以继续组织 / 清理这些节点。
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
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
    u"""

        在 Curve 上距离 world_position 最近的位置创建 Attachment。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。
            world_position (list[float] | tuple[float, float, float]):
                用于 Curve 最近点、参数查询或节点放置的 World Space Position。
            name (str):
                创建或查询时使用的节点名称。
            parent (str):
                父级 Maya 节点名称。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    # 步骤 1：先得到最近位置的原始 Parameter。
    parameter = get_closest_parameter(
        curve,
        world_position
    )

    # 步骤 2：复用标准 Attachment 创建入口。
    return create_point_on_curve_attachment(
        curve=curve,
        parameter=parameter,
        name=name,
        parent=parent
    )


# =============================================================================
# Create - 基础 Curve 创建
# =============================================================================

def create_curve_from_nodes(
        nodes,
        name,
        degree=3
):
    u"""
    根据 Maya 节点的世界位置创建 NURBS Curve。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。
        name (str):
            创建或查询时使用的节点名称。
        degree (int):
            创建或重建 NURBS Curve 使用的 Degree。

    Returns:
        str: 新 Curve Transform。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：验证输入节点数量和 Degree。
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if nodes is None:
        nodes = []

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not nodes:
        raise RuntimeError(u"没有给定用于创建 Curve 的节点。")

    if degree < 1:
        raise ValueError(u"Curve degree 不能小于 1。")

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if len(nodes) < degree + 1:
        raise ValueError(
            u"degree={} 至少需要 {} 个点，当前只有 {} 个节点。".format(
                degree,
                degree + 1,
                len(nodes)
            )
        )

    # 步骤 2：逐节点读取世界位置。
    curve_points = []

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in nodes:
        scene_utils.validate_node(node)

        position = cmds.xform(
            node,
            query=True,
            worldSpace=True,
            translation=True
        )

        curve_points.append(position)

    # 步骤 3：使用这些世界点创建 Curve。
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return cmds.curve(
        point=curve_points,
        degree=degree,
        name=name
    )


def create_curve_from_selected_edges(
        name,
        degree=3,
        form=2
):
    u"""

        根据当前选择的 Polygon Edge 创建 NURBS Curve。

        这是本模块少数明确读取 Selection 的函数，因为函数名已经写明 selected_edges。

        Args:
            name (str):
                创建或查询时使用的节点名称。
            degree (int):
                创建或重建 NURBS Curve 使用的 Degree。
            form (int):
                NURBS Curve Form 枚举值，用于区分 Open、Closed 或 Periodic Curve。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。

    """
    # 步骤 1：只展开 Polygon Edge Selection。
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    selected_edges = cmds.filterExpand(
        selectionMask=32,
        expand=True
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if selected_edges is None:
        selected_edges = []

    if not selected_edges:
        raise RuntimeError(
            u"请先选择一个或多个 Polygon Edge。"
        )

    # 步骤 2：调用 Maya polyToCurve。
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    result = cmds.polyToCurve(
        form=form,
        degree=degree,
        constructionHistory=False,
        name=name
    )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not result:
        raise RuntimeError(u"Polygon Edge 转 Curve 失败。")

    # Maya 返回列表，第一项为创建出来的 Curve Transform。
    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result[0]


__all__ = [
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
