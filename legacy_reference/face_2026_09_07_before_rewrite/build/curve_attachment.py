# coding=utf-8
u"""
Face Curve Attachment Rig
=========================

Face Jnt -> Drive / Aim Curve 组合系统。

职责：
    - 根据 Jnt 当前世界位置查找 Drive Curve 最近位置；
    - 使用弧长百分比同步 Drive / Aim / Up Curve；
    - 创建 pointOnCurveInfo Attachment；
    - Drive Attachment 朝 Aim Attachment 定向；
    - 使用 Up Curve 或 Up Object 控制 Aim Roll；
    - 创建 Jnt Zero Group，把 Jnt 接入 Curve 驱动网络。

重要边界：
    - Curve 参数、采样和 Attachment 节点由 core.curve_utils 负责；
    - Transform 输入和世界位置由 core.transform_utils 负责；
    - Jnt 类型检查复用 core.jnt_utils.Jnt；
    - Group 创建和 Scene Availability 由 core.scene_utils 负责；
    - Parent 由 core.hierarchy_utils 负责；
    - Constraint 由 core.constraint_utils 负责；
    - Face Builder Naming 统一复用 systems.face.naming；
    - Undo Chunk 由 core.scene_utils 负责；
    - 本模块只负责 Face Curve Attachment 的组合关系。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import constraint_utils
from ....core import curve_utils
from ....core import hierarchy_utils
from ....core import jnt_utils
from ....core import scene_utils
from ....core import transform_utils
from .. import naming as face_naming


# =============================================================================
# Internal Helpers
# =============================================================================

def create_attachment_group(
        nodes_group,
        side,
        region,
        feature,
        role
):
    u"""
    创建 Drive / Aim / Up Attachment Group。

    Args:
        nodes_group (str):
            当前 Rig / Guide / Controller 层级中的 Maya Group Transform。
        side (str):
            方向标记，常用值为 lf、rt 或 md。
        region (str):
            Face Component 的区域标记，例如 upper、lower、inner、outer。
        feature (str):
            Face Component 的功能部位标记，例如 lid、bag、lip。
        role (str):
            当前 UI / Rig 元素的语义角色，用于命名、Style 或构建分类。

    Returns:
        object:
        创建或构建完成后的 Maya / Rig 对象或 Build Result。
    """
    group_name = face_naming.create_feature_name(
        "grp",
        side,
        region,
        feature,
        role,
        1
    )

    return scene_utils.create_node(
        "transform",
        group_name,
        parent=nodes_group
    )


def create_curve_attachment(
        curve,
        percentage,
        name,
        parent
):
    u"""
    按弧长百分比在指定 Curve 创建 Attachment。

    Args:
        curve (str):
            需要处理的 Maya Curve Transform 或 Shape 名称。
        percentage (float):
            沿 Curve 或数据范围的归一化百分比，通常为 0.0～1.0。
        name (str):
            创建或查询时使用的节点名称。
        parent (str):
            父级 Maya 节点名称。

    Returns:
        object:
        创建或构建完成后的 Maya / Rig 对象或 Build Result。
    """
    parameter = curve_utils.length_percentage_to_parameter(
        curve,
        percentage
    )

    return curve_utils.create_point_on_curve_attachment(
        curve=curve,
        parameter=parameter,
        name=name,
        parent=parent
    )


# =============================================================================
# Public Build
# =============================================================================

@scene_utils.undo_chunk
def attach_jnts_to_curves(
        jnts,
        drive_curve,
        aim_curve,
        side,
        region,
        feature,
        up_object=None,
        up_curve=None,
        parent_group=None,
        preserve_jnt_offset=True
):
    u"""
    把一组 Jnt 接入 Drive / Aim Curve 网络。

    Args:
        jnts (str | list[str]):
            需要批量处理的 Maya Jnt 节点或 Jnt Chain。
        drive_curve (str):
            当前采样、附着或驱动使用的 NURBS Curve。
        aim_curve (str):
            当前采样、附着或驱动使用的 NURBS Curve。
        side (str):
            方向标记，常用值为 lf、rt 或 md。
        region (str):
            Face Component 的区域标记，例如 upper、lower、inner、outer。
        feature (str):
            Face Component 的功能部位标记，例如 lid、bag、lip。
        up_object (str):
            Eyelid / Radial Jnt Aim 系统用于稳定 Orientation 的 Up Object。
        up_curve (str):
            当前采样、附着或驱动使用的 NURBS Curve。
        parent_group (str | None):
            新节点或新层级需要挂接的 Parent Group；None 表示不额外指定父级。
        preserve_jnt_offset (bool):
            控制当前方法中的 `preserve_jnt_offset` 选项是否启用。

    Returns:
        dict:
        包含本次构建、查询或处理结果的结构化字典。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if jnts is None:
        jnts = []

    if not jnts:
        raise RuntimeError(
            u"没有给定需要附着的 Jnt。"
        )

    for jnt in jnts:
        jnt_utils.Jnt(
            jnt
        )

    # -------------------------------------------------------------------------
    # Step 02：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    curve_utils.get_curve_shape(
        drive_curve
    )
    curve_utils.get_curve_shape(
        aim_curve
    )

    if up_curve is not None:
        curve_utils.get_curve_shape(
            up_curve
        )
    else:
        transform_utils.validate_transform(
            up_object
        )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if parent_group is not None:
        transform_utils.validate_transform(
            parent_group
        )

    nodes_group_name = face_naming.create_feature_name(
        "grp",
        side,
        region,
        feature,
        "rig_nodes",
        1
    )
    jnts_group_name = face_naming.create_feature_name(
        "grp",
        side,
        region,
        feature,
        "attach_jnts",
        1
    )

    # -------------------------------------------------------------------------
    # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    scene_utils.ensure_nodes_available(
        [
            nodes_group_name,
            jnts_group_name,
        ],
        label=u"Curve Attachment Build Node"
    )

    nodes_group = None

    # -------------------------------------------------------------------------
    # Step 05：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        nodes_group = scene_utils.create_node(
            "transform",
            nodes_group_name,
            parent=parent_group
        )
        jnts_group = scene_utils.create_node(
            "transform",
            jnts_group_name,
            parent=nodes_group
        )
        drive_group = create_attachment_group(
            nodes_group,
            side,
            region,
            feature,
            "drive_attaches"
        )
        aim_group = create_attachment_group(
            nodes_group,
            side,
            region,
            feature,
            "aim_attaches"
        )

        up_group = None

        if up_curve is not None:
            up_group = create_attachment_group(
                nodes_group,
                side,
                region,
                feature,
                "up_attaches"
            )

        zero_groups = []
        drive_attachments = []
        aim_attachments = []
        up_attachments = []
        point_on_curve_nodes = []
        matrix_nodes = []
        aim_constraints = []
        parent_constraints = []
        percentages = []

        index = 0

        while index < len(jnts):
            jnt = jnts[index]
            item_index = index + 1
            jnt_position = transform_utils.get_world_translation(
                jnt
            )
            drive_parameter = curve_utils.get_closest_parameter(
                drive_curve,
                jnt_position
            )
            percentage = curve_utils.parameter_to_length_percentage(
                drive_curve,
                drive_parameter
            )
            percentages.append(
                percentage
            )

            drive_attachment_name = face_naming.create_feature_name(
                "grp",
                side,
                region,
                feature,
                "drive_attach",
                item_index
            )
            aim_attachment_name = face_naming.create_feature_name(
                "grp",
                side,
                region,
                feature,
                "aim_attach",
                item_index
            )

            drive_result = create_curve_attachment(
                drive_curve,
                percentage,
                drive_attachment_name,
                drive_group
            )
            aim_result = create_curve_attachment(
                aim_curve,
                percentage,
                aim_attachment_name,
                aim_group
            )

            drive_attachment = drive_result["transform"]
            aim_attachment = aim_result["transform"]
            drive_attachments.append(
                drive_attachment
            )
            aim_attachments.append(
                aim_attachment
            )
            point_on_curve_nodes.append(
                drive_result["point_on_curve"]
            )
            point_on_curve_nodes.append(
                aim_result["point_on_curve"]
            )

            for matrix_node in drive_result["matrix_nodes"]:
                matrix_nodes.append(
                    matrix_node
                )

            for matrix_node in aim_result["matrix_nodes"]:
                matrix_nodes.append(
                    matrix_node
                )

            current_up_attachment = None

            if up_curve is not None:
                up_attachment_name = face_naming.create_feature_name(
                    "grp",
                    side,
                    region,
                    feature,
                    "up_attach",
                    item_index
                )
                up_result = create_curve_attachment(
                    up_curve,
                    percentage,
                    up_attachment_name,
                    up_group
                )
                current_up_attachment = up_result["transform"]
                up_attachments.append(
                    current_up_attachment
                )
                point_on_curve_nodes.append(
                    up_result["point_on_curve"]
                )

                for matrix_node in up_result["matrix_nodes"]:
                    matrix_nodes.append(
                        matrix_node
                    )

            if current_up_attachment is not None:
                aim_constraint_nodes = constraint_utils.create_constraint(
                    driver_objects=aim_attachment,
                    driven_object=drive_attachment,
                    constraint_type="aimConstraint",
                    maintain_offset=False,
                    aimVector=[1.0, 0.0, 0.0],
                    upVector=[0.0, 1.0, 0.0],
                    worldUpType="object",
                    worldUpObject=current_up_attachment,
                    worldUpVector=[0.0, 1.0, 0.0]
                )
            else:
                aim_constraint_nodes = constraint_utils.create_constraint(
                    driver_objects=aim_attachment,
                    driven_object=drive_attachment,
                    constraint_type="aimConstraint",
                    maintain_offset=False,
                    aimVector=[1.0, 0.0, 0.0],
                    upVector=[0.0, 1.0, 0.0],
                    worldUpType="objectrotation",
                    worldUpObject=up_object,
                    worldUpVector=[0.0, 1.0, 0.0]
                )

            if not aim_constraint_nodes:
                raise RuntimeError(
                    u"Aim Constraint 创建失败：{}".format(
                        drive_attachment
                    )
                )

            aim_constraint = aim_constraint_nodes[0]
            aim_constraints.append(
                aim_constraint
            )

            zero_group_name = face_naming.create_feature_name(
                "zero",
                side,
                region,
                feature,
                "attach",
                item_index
            )
            zero_group = scene_utils.create_node(
                "transform",
                zero_group_name,
                parent=jnts_group
            )

            parent_constraint_nodes = constraint_utils.create_constraint(
                driver_objects=drive_attachment,
                driven_object=zero_group,
                constraint_type="parentConstraint",
                maintain_offset=False
            )

            if not parent_constraint_nodes:
                raise RuntimeError(
                    u"Parent Constraint 创建失败：{}".format(
                        zero_group
                    )
                )

            parent_constraint = parent_constraint_nodes[0]
            parent_constraints.append(
                parent_constraint
            )
            zero_groups.append(
                zero_group
            )

            jnt = hierarchy_utils.parent(
                jnt,
                zero_group
            )

            cmds.setAttr(
                jnt + ".rotateX",
                0.0
            )
            cmds.setAttr(
                jnt + ".rotateY",
                0.0
            )
            cmds.setAttr(
                jnt + ".rotateZ",
                0.0
            )

            if not preserve_jnt_offset:
                cmds.setAttr(
                    jnt + ".translateX",
                    0.0
                )
                cmds.setAttr(
                    jnt + ".translateY",
                    0.0
                )
                cmds.setAttr(
                    jnt + ".translateZ",
                    0.0
                )

            index += 1

        return {
            "nodes_group": nodes_group,
            "jnts_group": jnts_group,
            "drive_group": drive_group,
            "aim_group": aim_group,
            "up_group": up_group,
            "jnts": jnts,
            "zero_groups": zero_groups,
            "drive_attachments": drive_attachments,
            "aim_attachments": aim_attachments,
            "up_attachments": up_attachments,
            "point_on_curve_nodes": point_on_curve_nodes,
            "matrix_nodes": matrix_nodes,
            "aim_constraints": aim_constraints,
            "parent_constraints": parent_constraints,
            "percentages": percentages,
        }

    except Exception:
        if nodes_group is not None:
            if cmds.objExists(nodes_group):
                cmds.delete(
                    nodes_group
                )

        raise


__all__ = [
    "attach_jnts_to_curves",
]
