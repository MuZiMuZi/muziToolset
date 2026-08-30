# coding=utf-8
u"""
Face Curve Attachment Rig
=========================

从旧 pipelineUtils.attach_joints_on_curve 迁移出的 Face System 级功能。

职责：
    - 根据 Joint 当前世界位置查找 Drive Curve 最近位置；
    - 使用弧长百分比同步 Drive / Aim / Up Curve；
    - 创建 pointOnCurveInfo Attachment；
    - Drive Attachment 朝 Aim Attachment 定向；
    - 使用 Up Curve 或 Up Object 控制 Aim Roll；
    - 创建 Joint Zero Group，把 Joint 接入 Curve 驱动网络。

说明：
    Curve 参数、采样和 Attachment 节点由 core.curve_utils 负责；
    本模块只负责 Face Rig 的组合关系和层级结构。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import curve_utils
from ...core import name_utils


# =============================================================================
# Validate / Naming
# =============================================================================

def validate_joint(joint):
    """检查 Joint。"""
    if not joint:
        raise RuntimeError(u"Joint 名称不能为空。")

    if not cmds.objExists(joint):
        raise RuntimeError(
            u"Joint 不存在：{}".format(joint)
        )

    if cmds.nodeType(joint) != "joint":
        raise RuntimeError(
            u"节点不是 Joint：{} | type={}".format(
                joint,
                cmds.nodeType(joint)
            )
        )

    return True


def validate_transform(node, label):
    """检查 Transform / Joint 类型。"""
    if not node:
        raise RuntimeError(
            u"{}不能为空。".format(label)
        )

    if not cmds.objExists(node):
        raise RuntimeError(
            u"{}不存在：{}".format(
                label,
                node
            )
        )

    node_type = cmds.nodeType(node)

    if node_type not in ["transform", "joint"]:
        raise RuntimeError(
            u"{}必须是 Transform 或 Joint：{}".format(
                label,
                node
            )
        )

    return True


def normalize_name_part(value, label):
    """清理命名字段。"""
    if value is None:
        raise ValueError(
            u"{}不能为空。".format(label)
        )

    value = str(value).strip().lower()
    value = value.replace(" ", "_")
    value = value.replace("-", "_")

    while "__" in value:
        value = value.replace("__", "_")

    value = value.strip("_")

    if not value:
        raise ValueError(
            u"{}不能为空。".format(label)
        )

    return value


def create_rig_name(
        node_type,
        side,
        region,
        feature,
        role,
        index=1
):
    """创建 Face Curve Rig 标准名称。"""
    side = name_utils.Name.normalize_side(side)
    region = normalize_name_part(
        region,
        "region"
    )
    feature = normalize_name_part(
        feature,
        "feature"
    )
    role = normalize_name_part(
        role,
        "role"
    )

    function_name = "{}_{}".format(
        feature,
        role
    )

    return name_utils.Name.create_name(
        node_type=node_type,
        side=side,
        part=region,
        function=function_name,
        index=index
    )


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
    """创建 Drive / Aim / Up Attachment Group。"""
    group_name = create_rig_name(
        "grp",
        side,
        region,
        feature,
        role,
        1
    )

    if cmds.objExists(group_name):
        raise RuntimeError(
            u"Attachment Group 已经存在：{}".format(
                group_name
            )
        )

    return cmds.createNode(
        "transform",
        name=group_name,
        parent=nodes_group
    )


def create_curve_attachment(
        curve,
        percentage,
        name,
        parent
):
    """按弧长百分比在指定 Curve 创建 Attachment。"""
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

def attach_joints_to_curves(
        joints,
        drive_curve,
        aim_curve,
        side,
        region,
        feature,
        up_object=None,
        up_curve=None,
        parent_group=None,
        preserve_joint_offset=True
):
    """
    把一组 Joint 接入 Drive / Aim Curve 网络。

    Args:
        joints(list): 需要驱动的 Joint。
        drive_curve(str): 决定位置的 Curve。
        aim_curve(str): 决定朝向的 Curve。
        side(str): lf / rt / md。
        region(str): brow / lip / lid 等区域字段。
        feature(str): main / upper / lower 等功能字段。
        up_object(str/None): Object Rotation World Up。
        up_curve(str/None): 如果给定，使用第三条 Curve 作为 World Up。
        parent_group(str/None): Rig Nodes Group Parent。
        preserve_joint_offset(bool):
            True  保留 Joint 原始位置偏移；
            False Joint 直接吸附到 Drive Attachment。

    Returns:
        dict: Rig 节点和 Attachment 数据。
    """
    if joints is None:
        joints = []

    if not joints:
        raise RuntimeError(u"没有给定需要附着的 Joint。")

    for joint in joints:
        validate_joint(joint)

    curve_utils.get_curve_shape(drive_curve)
    curve_utils.get_curve_shape(aim_curve)

    if up_curve is not None:
        curve_utils.get_curve_shape(up_curve)
    else:
        validate_transform(
            up_object,
            u"Up Object"
        )

    if parent_group is not None:
        validate_transform(
            parent_group,
            u"Parent Group"
        )

    side = name_utils.Name.normalize_side(side)
    region = normalize_name_part(
        region,
        "region"
    )
    feature = normalize_name_part(
        feature,
        "feature"
    )

    nodes_group_name = create_rig_name(
        "grp",
        side,
        region,
        feature,
        "rig_nodes",
        1
    )
    joints_group_name = create_rig_name(
        "grp",
        side,
        region,
        feature,
        "attach_joints",
        1
    )

    if cmds.objExists(nodes_group_name):
        raise RuntimeError(
            u"Curve Rig Nodes Group 已经存在：{}".format(
                nodes_group_name
            )
        )

    if cmds.objExists(joints_group_name):
        raise RuntimeError(
            u"Curve Rig Joint Group 已经存在：{}".format(
                joints_group_name
            )
        )

    nodes_group = None

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziFaceCurveAttachment"
    )

    try:
        nodes_group = cmds.createNode(
            "transform",
            name=nodes_group_name,
            parent=parent_group
        )

        joints_group = cmds.createNode(
            "transform",
            name=joints_group_name,
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

        while index < len(joints):
            joint = joints[index]
            item_index = index + 1

            joint_position = cmds.xform(
                joint,
                query=True,
                worldSpace=True,
                translation=True
            )

            drive_parameter = curve_utils.get_closest_parameter(
                drive_curve,
                joint_position
            )
            percentage = curve_utils.parameter_to_length_percentage(
                drive_curve,
                drive_parameter
            )
            percentages.append(percentage)

            drive_attachment_name = create_rig_name(
                "grp",
                side,
                region,
                feature,
                "drive_attach",
                item_index
            )
            aim_attachment_name = create_rig_name(
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

            drive_attachments.append(drive_attachment)
            aim_attachments.append(aim_attachment)

            point_on_curve_nodes.append(
                drive_result["point_on_curve"]
            )
            point_on_curve_nodes.append(
                aim_result["point_on_curve"]
            )

            for matrix_node in drive_result["matrix_nodes"]:
                matrix_nodes.append(matrix_node)

            for matrix_node in aim_result["matrix_nodes"]:
                matrix_nodes.append(matrix_node)

            current_up_attachment = None

            if up_curve is not None:
                up_attachment_name = create_rig_name(
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
                up_attachments.append(current_up_attachment)
                point_on_curve_nodes.append(
                    up_result["point_on_curve"]
                )

                for matrix_node in up_result["matrix_nodes"]:
                    matrix_nodes.append(matrix_node)

            if current_up_attachment is not None:
                aim_constraint = cmds.aimConstraint(
                    aim_attachment,
                    drive_attachment,
                    aimVector=[1.0, 0.0, 0.0],
                    upVector=[0.0, 1.0, 0.0],
                    worldUpType="object",
                    worldUpObject=current_up_attachment,
                    worldUpVector=[0.0, 1.0, 0.0],
                    maintainOffset=False
                )[0]
            else:
                aim_constraint = cmds.aimConstraint(
                    aim_attachment,
                    drive_attachment,
                    aimVector=[1.0, 0.0, 0.0],
                    upVector=[0.0, 1.0, 0.0],
                    worldUpType="objectrotation",
                    worldUpObject=up_object,
                    worldUpVector=[0.0, 1.0, 0.0],
                    maintainOffset=False
                )[0]

            aim_constraints.append(aim_constraint)

            zero_group_name = create_rig_name(
                "zero",
                side,
                region,
                feature,
                "attach",
                item_index
            )
            zero_group = cmds.createNode(
                "transform",
                name=zero_group_name,
                parent=joints_group
            )

            parent_constraint = cmds.parentConstraint(
                drive_attachment,
                zero_group,
                maintainOffset=False
            )[0]

            parent_constraints.append(parent_constraint)
            zero_groups.append(zero_group)

            joint = cmds.parent(
                joint,
                zero_group
            )[0]

            cmds.setAttr(
                joint + ".rotateX",
                0.0
            )
            cmds.setAttr(
                joint + ".rotateY",
                0.0
            )
            cmds.setAttr(
                joint + ".rotateZ",
                0.0
            )

            if not preserve_joint_offset:
                cmds.setAttr(
                    joint + ".translateX",
                    0.0
                )
                cmds.setAttr(
                    joint + ".translateY",
                    0.0
                )
                cmds.setAttr(
                    joint + ".translateZ",
                    0.0
                )

            index += 1

        result = {
            "nodes_group": nodes_group,
            "joints_group": joints_group,
            "drive_group": drive_group,
            "aim_group": aim_group,
            "up_group": up_group,
            "joints": joints,
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

        return result

    except Exception:
        if nodes_group is not None:
            if cmds.objExists(nodes_group):
                cmds.delete(nodes_group)

        raise

    finally:
        cmds.undoInfo(
            closeChunk=True
        )


__all__ = [
    "attach_joints_to_curves",
]
