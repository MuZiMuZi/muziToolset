# coding=utf-8
u"""
Surface Utils
=============

Maya NURBS Surface / Follicle 领域的通用底层工具。

模块职责
--------
这个模块只处理 NURBS Surface 和 Follicle 的基础能力：

    - Surface Shape / Transform 查询；
    - 根据 Curve 创建简单 Loft Surface；
    - 在 Surface 上创建 Follicle；
    - 按 U / V 方向批量均匀创建 Follicle。

当前公开方法
------------
基础查询：
    scene_utils.validate_node(node)
        检查 Maya 节点是否存在。

    get_surface_shape(surface)
        获取 NURBS Surface Shape 的完整 DAG Path。

    get_surface_transform(surface)
        获取 NURBS Surface Transform 的完整 DAG Path。

Loft：
    move_curve_copy(curve, axis, distance)
        沿 Curve 自身 Object Space 指定轴移动临时副本。

    create_surface_from_curve(curve, name, offset=0.2,
                              offset_axis="Y", degree=3)
        复制输入 Curve 两次并 Loft 成 NURBS Surface。

Follicle：
    create_follicle(surface, name, parameter_u=0.5,
                    parameter_v=0.5, parent=None)
        在 NURBS Surface 上创建一个 Follicle。

    create_even_follicles(surface, count, name_prefix="fol_surface",
                          direction="U", fixed_parameter=0.5, parent=None)
        沿 Surface U 或 V 均匀创建多个 Follicle。

为什么旧 create_joint_follicle_on_surface 不保留在 Core
--------------------------------------------------------
早期函数会一次性创建：

    Surface
    Follicle
    Joint
    Controller
    Group
    Set

这已经是完整 Rig Workflow，而不是通用 Surface API。

正式边界改成：

    surface_utils
        -> Surface / Follicle

    System
        -> Joint / Controller / Rig Hierarchy

这样 Face、Ribbon、Skirt 等系统可以复用同一套 Follicle 能力，而不被某一种 Rig
层级结构绑死。

本模块不负责
------------
- Joint；
- Controller；
- SkinCluster；
- Ribbon / Face / Skirt 完整绑定；
- UI。

模块边界
--------
    NURBS Curve 数据       -> curve_utils
    NURBS Surface/Follicle -> surface_utils
    完整 Rig Workflow      -> systems/

设计原则
--------
1. Loft 时绝不修改或删除用户传入的原始 Curve；
2. 临时 Duplicate 无论成功或失败都通过 finally 清理；
3. Loft 只在 Maya 自动材质分配所需的短时间内临时解锁默认 Shading Group，并恢复原状态；
4. Follicle Core 只返回 Transform / Shape，不擅自创建 Joint / Controller；
5. 批量 Follicle 使用稳定的 001 / 002 / 003 编号；
6. 保留普通 while / for 流程，方便在 Maya 中逐步调试。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import curve_utils
from . import scene_utils
from . import shading_utils


# =============================================================================
# Query - Surface 基础查询
# =============================================================================


def get_surface_shape(surface):
    u"""
    返回 NURBS Surface Shape 的完整 DAG Path。

    ``surface`` 可以是 Transform，也可以直接是 nurbsSurface Shape。

    Args:
        surface (str):
            需要处理的 Maya Surface 节点名称。

    Returns:
        object:
        当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：校验输入节点。
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    scene_utils.validate_node(surface)

    # 步骤 2：输入已经是 Shape 时直接转 Long Name。
    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if cmds.nodeType(surface) == "nurbsSurface":
        matches = cmds.ls(
            surface,
            long=True
        )

        if matches:
            return matches[0]

        return surface

    # 步骤 3：输入是 Transform 时寻找非 Intermediate Surface Shape。
    shapes = cmds.listRelatives(
        surface,
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
        if cmds.nodeType(shape) == "nurbsSurface":
            return shape

    # 步骤 4：找不到有效 Shape 时明确报错。
    # -------------------------------------------------------------------------
    # Step 05：根据无效输入或场景状态抛出明确异常
    # -------------------------------------------------------------------------
    raise RuntimeError(
        u"节点不是 NURBS Surface：{}".format(surface)
    )


def get_surface_transform(surface):
    u"""
    返回 NURBS Surface Transform 的完整 DAG Path。

    Args:
        surface (str):
            需要处理的 Maya Surface 节点名称。

    Returns:
        object:
        当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：先统一取得 Surface Shape。
    surface_shape = get_surface_shape(surface)

    # 步骤 2：查询 Shape Parent。
    parents = cmds.listRelatives(
        surface_shape,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    if not parents:
        raise RuntimeError(
            u"Surface Shape 没有 Transform Parent：{}".format(
                surface_shape
            )
        )

    return parents[0]


# =============================================================================
# Loft - Curve -> Surface
# =============================================================================

def move_curve_copy(
        curve,
        axis,
        distance
):
    u"""
    沿 Curve 自身 Object Space 指定轴移动 Curve 副本。

    Args:
        curve (str):
            通常是 create_surface_from_curve() 创建的临时 Duplicate。
        axis (str):
            X / Y / Z。
        distance (float):
            移动距离，可以为负数。

    Returns:
        object:
        当前 API 完成处理后的结果。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：把轴向统一成大写。
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    axis = axis.upper()

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    move_x = 0.0
    move_y = 0.0
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    move_z = 0.0

    # 步骤 2：把单轴距离转换成 cmds.move 的 XYZ 参数。
    if axis == "X":
        move_x = distance
    elif axis == "Y":
        move_y = distance
    elif axis == "Z":
        move_z = distance
    else:
        raise ValueError(
            u"offset_axis 只支持 X / Y / Z，当前为：{}".format(
                axis
            )
        )

    # 步骤 3：使用 Object Space 轴向移动，但距离保持世界单位。
    # -------------------------------------------------------------------------
    # Step 04：执行当前阶段的核心处理
    # -------------------------------------------------------------------------
    cmds.move(
        move_x,
        move_y,
        move_z,
        curve,
        relative=True,
        objectSpace=True,
        worldSpaceDistance=True
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return curve


def create_surface_from_curve(
        curve,
        name,
        offset=0.2,
        offset_axis="Y",
        degree=3
):
    u"""
    复制输入 Curve 两次，并 Loft 成 NURBS Surface。

    与早期 Pipeline 版本不同：
        - 不移动原 Curve；
        - 不删除原 Curve；
        - 只操作两个临时 Duplicate；
        - Loft 完成后自动删除临时 Duplicate；
        - Maya 默认 Shading Group 被锁定时，只在 Loft 期间临时解锁并恢复。

    Args:
        curve (str):
            需要处理的 Maya Curve Transform 或 Shape 名称。
        name (str):
            创建或查询时使用的节点名称。
        offset (float):
            当前 Rig / Shape / Surface 操作使用的 Offset 数值或偏移向量。
        offset_axis (str):
            应用 Surface / Attachment Offset 的轴向。
        degree (int):
            创建或重建 NURBS Curve 使用的 Degree。

    Returns:
        str: 新创建的 NURBS Surface Transform。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：取得 Curve Transform。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    curve_transform = curve_utils.get_curve_transform(
        curve
    )

    # -------------------------------------------------------------------------
    # 步骤 2：创建正负两份临时 Curve。
    #
    # 这里绝不直接移动用户输入 Curve，避免底层工具产生破坏性副作用。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    positive_copy = cmds.duplicate(
        curve_transform,
        renameChildren=True
    )[0]

    # -------------------------------------------------------------------------
    # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    negative_copy = cmds.duplicate(
        curve_transform,
        renameChildren=True
    )[0]

    # -------------------------------------------------------------------------
    # Step 04：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        # ---------------------------------------------------------------------
        # 步骤 3：沿指定 Object Axis 向两侧偏移。
        # ---------------------------------------------------------------------
        move_curve_copy(
            positive_copy,
            offset_axis,
            offset
        )

        move_curve_copy(
            negative_copy,
            offset_axis,
            -offset
        )

        # ---------------------------------------------------------------------
        # 步骤 4：使用两个临时 Curve Loft。
        #
        # Maya 创建 NURBS Surface Shape 时会自动把 Shape 加入
        # initialShadingGroup。如果默认 Shading Group 或其 Container 被锁定，
        # cmds.loft() 会因为无法写入 dagSetMembers 而整体失败。
        #
        # 这里只在 Loft 的最小作用域内临时解锁，并在 finally 中严格恢复原状态。
        # ---------------------------------------------------------------------
        shading_group_state = shading_utils.unlock_default_shading_group()

        try:
            result = cmds.loft(
                positive_copy,
                negative_copy,
                constructionHistory=False,
                uniform=True,
                degree=degree,
                sectionSpans=1,
                range=False,
                polygon=0,
                name=name
            )
        finally:
            shading_utils.restore_default_shading_group(
                shading_group_state
            )

        if not result:
            raise RuntimeError(u"Curve Loft Surface 创建失败。")

        surface = result[0]

    finally:
        # ---------------------------------------------------------------------
        # 步骤 5：无论 Loft 成功还是失败，都删除临时 Curve。
        # ---------------------------------------------------------------------
        if cmds.objExists(positive_copy):
            cmds.delete(positive_copy)

        if cmds.objExists(negative_copy):
            cmds.delete(negative_copy)

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return surface


# =============================================================================
# Follicle - Surface Attachment
# =============================================================================

def create_follicle(
        surface,
        name,
        parameter_u=0.5,
        parameter_v=0.5,
        parent=None
):
    u"""
    在 NURBS Surface 上创建一个 Follicle。

    网络：
        surfaceShape.local
            -> follicleShape.inputSurface
        surfaceShape.worldMatrix[0]
            -> follicleShape.inputWorldMatrix
        follicleShape.outTranslate
            -> follicleTransform.translate
        follicleShape.outRotate
            -> follicleTransform.rotate

    Args:
        surface (str):
            需要处理的 Maya Surface 节点名称。
        name (str):
            创建或查询时使用的节点名称。
        parameter_u (float):
            NURBS Surface U 方向 Parameter。
        parameter_v (float):
            NURBS Surface V 方向 Parameter。
        parent (str):
            父级 Maya 节点名称。

    Returns:
        dict:
        {
        "transform": follicle_transform,
        "shape": follicle_shape,
        }

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：取得 Surface Shape。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    surface_shape = get_surface_shape(surface)

    # -------------------------------------------------------------------------
    # 步骤 2：创建 Follicle Shape。
    # Maya 创建 Shape 时会自动生成一个 Parent Transform。
    # -------------------------------------------------------------------------
    follicle_shape = cmds.createNode(
        "follicle",
        name="{}Shape".format(name)
    )

    parents = cmds.listRelatives(
        follicle_shape,
        parent=True,
        fullPath=True
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if parents is None:
        parents = []

    if not parents:
        raise RuntimeError(u"创建 Follicle Transform 失败。")

    # 步骤 3：把 Maya 自动生成的 Transform 改成正式名称。
    follicle_transform = cmds.rename(
        parents[0],
        name
    )

    # -------------------------------------------------------------------------
    # 步骤 4：连接 Surface 输入。
    # local 提供 NURBS 数据，worldMatrix 提供 Surface 世界变换。
    # -------------------------------------------------------------------------
    cmds.connectAttr(
        surface_shape + ".local",
        follicle_shape + ".inputSurface",
        force=True
    )

    # -------------------------------------------------------------------------
    # Step 03：建立当前阶段需要的层级、连接或驱动关系
    # -------------------------------------------------------------------------
    cmds.connectAttr(
        surface_shape + ".worldMatrix[0]",
        follicle_shape + ".inputWorldMatrix",
        force=True
    )

    # -------------------------------------------------------------------------
    # 步骤 5：让 Follicle 计算结果驱动自身 Transform。
    # -------------------------------------------------------------------------
    cmds.connectAttr(
        follicle_shape + ".outTranslate",
        follicle_transform + ".translate",
        force=True
    )

    cmds.connectAttr(
        follicle_shape + ".outRotate",
        follicle_transform + ".rotate",
        force=True
    )

    # -------------------------------------------------------------------------
    # 步骤 6：设置 Surface UV Parameter。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 04：应用并更新当前阶段需要的属性或状态
    # -------------------------------------------------------------------------
    cmds.setAttr(
        follicle_shape + ".parameterU",
        parameter_u
    )

    cmds.setAttr(
        follicle_shape + ".parameterV",
        parameter_v
    )

    # -------------------------------------------------------------------------
    # 步骤 7：按需要整理 Parent。
    # -------------------------------------------------------------------------
    if parent:
        scene_utils.validate_node(parent)

        follicle_transform = cmds.parent(
            follicle_transform,
            parent
        )[0]

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return {
        "transform": follicle_transform,
        "shape": follicle_shape,
    }


def create_even_follicles(
        surface,
        count,
        name_prefix="fol_surface",
        direction="U",
        fixed_parameter=0.5,
        parent=None
):
    u"""
    沿 Surface 的 U 或 V 方向均匀创建多个 Follicle。

    Args:
        surface (str):
            NURBS Surface。
        count (int):
            Follicle 数量。
        name_prefix (str):
            名称前缀。
        direction (str):
            U 或 V。
        fixed_parameter (float):
            未被分布的另一个方向固定值。
        parent (str/None):
            可选父节点。 规则： count=1：放在 0.5； count>=2：覆盖 0~1。

    Returns:
        object:
        创建或构建完成后的 Maya / Rig 对象或 Build Result。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：验证数量和方向。
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if count < 1:
        raise ValueError(u"Follicle 数量不能小于 1。")

    direction = direction.upper()

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if direction != "U" and direction != "V":
        raise ValueError(u"direction 只支持 U 或 V。")

    # 步骤 2：准备均匀百分比。
    percentages = []

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if count == 1:
        percentages.append(0.5)
    else:
        percentages = curve_utils.get_even_percentages(
            count
        )

    results = []

    # 步骤 3：逐个百分比创建 Follicle。
    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    index = 0

    while index < count:
        percentage = percentages[index]

        parameter_u = fixed_parameter
        parameter_v = fixed_parameter

        if direction == "U":
            parameter_u = percentage
        else:
            parameter_v = percentage

        # 使用三位数编号，保证 Outliner 排序稳定。
        follicle_name = "{}_{:03d}".format(
            name_prefix,
            index + 1
        )

        result = create_follicle(
            surface=surface,
            name=follicle_name,
            parameter_u=parameter_u,
            parameter_v=parameter_v,
            parent=parent
        )

        results.append(result)
        index += 1

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return results


__all__ = [
    "get_surface_shape",
    "get_surface_transform",
    "move_curve_copy",
    "create_surface_from_curve",
    "create_follicle",
    "create_even_follicles",
]
