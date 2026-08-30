# coding=utf-8
u"""
Face Curve Attachment Rig
=========================

Face Joint -> Drive / Aim Curve 组合系统。

职责：
    - 根据 Joint 当前世界位置查找 Drive Curve 最近位置；
    - 使用弧长百分比同步 Drive / Aim / Up Curve；
    - 创建 pointOnCurveInfo Attachment；
    - Drive Attachment 朝 Aim Attachment 定向；
    - 使用 Up Curve 或 Up Object 控制 Aim Roll；
    - 创建 Joint Zero Group，把 Joint 接入 Curve 驱动网络。

重要边界：
    - Curve 参数、采样和 Attachment 节点由 core.curve_utils 负责；
    - Transform 输入和世界位置由 core.transform_utils 负责；
    - Joint 类型校验由 core.joint_utils 负责；
    - Group 创建由 core.scene_utils 负责；
    - Parent 由 core.hierarchy_utils 负责；
    - Constraint 由 core.constraint_utils 负责；
    - Undo Chunk 由 core.scene_utils 负责；
    - 本模块只负责 Face Curve Attachment 的组合关系。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import constraint_utils
from ....core import curve_utils
from ....core import hierarchy_utils
from ....core import joint_utils
from ....core import name_utils
from ....core import scene_utils
from ....core import transform_utils


# =============================================================================
# Validate / Naming
# =============================================================================

def validate_joint(joint):
    u"""检查输入节点必须是 Maya Joint。"""
    try:
        joint_utils.Joint._validate_joint(
            joint
        )
    except RuntimeError as error:
        raise RuntimeError(
            u"Joint 无效：{}".format(
                error
            )
        )

    return True


def normalize_name_part(value, label):
    u"""清理用于 Face Curve Rig 命名的字段。"""
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
    u"""创建 Face Curve Rig 标准名称。"""
    side = name_utils.Name.normalize_side(
        side
    )
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
    u"""创建 Drive / Aim / Up Attachment Group。"""
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
    u"""按弧长百分比在指定 Curve 创建 Attachment。"""
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
    u"""把一组 Joint 接入 Drive / Aim Curve 网络。"""
    if joints is None:
        joints = []

    if not joints:
        raise RuntimeError(u"没有给定需要附着的 Joint。")

    for joint in joints:
        validate_joint(
            joint
        )

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

    if parent_group is not None:
        transform_utils.validate_transform(
            parent_group
        )

    side = name_utils.Name.normalize_side(
        side
    )
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

    try:
        nodes_group = scene_utils.create_node(
            "transform",
            nodes_group_name,
            parent=parent_group
        )
        joints_group = scene_utils.create_node(
            "transform",
            joints_group_name,
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
            joint_position = transform_utils.get_world_translation(
                joint
            )
            drive_parameter = curve_utils.get_closest_parameter(
                drive_curve,
                joint_position
            )
            percentage = curve_utils.parameter_to_length_percentage(
                drive_curve,
                drive_parameter
            )
            percentages.append(
                percentage
            )

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

            zero_group_name = create_rig_name(
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
                parent=joints_group
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

            joint = hierarchy_utils.Hierarchy.parent(
                joint,
                zero_group
            )

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

        return {
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

    except Exception:
        if nodes_group is not None:
            if cmds.objExists(nodes_group):
                cmds.delete(
                    nodes_group
                )

        raise


__all__ = [
    "attach_joints_to_curves",
]
