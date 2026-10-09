# coding=utf-8
"""curve_utils：供工具 UI 调用的 Maya 操作。"""

from __future__ import print_function
import maya.cmds as cmds
from ..common import scene_utils
import maya.api.OpenMaya as om

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
