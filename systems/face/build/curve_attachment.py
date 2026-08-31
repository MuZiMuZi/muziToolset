# coding=utf-8
u"""
Face Curve Attachment
=====================

Face Joint -> Drive / Aim Curve 组合系统。

Maya 节点、属性、层级和 Constraint 直接使用 PyMEL；
Curve 参数和弧长算法由 core.curve 提供。
"""

from __future__ import print_function

import pymel.core as pm

from ....core import curve
from ....core import name
from ....core.undo import undo_chunk


def resolve_transform(node, label):
    if node is None:
        raise ValueError(u"{} 不能为空。".format(label))

    if isinstance(node, str):
        if not pm.objExists(node):
            raise RuntimeError(u"{} 不存在：{}".format(label, node))
        node = pm.PyNode(node)

    if node.nodeType() not in ["transform", "joint"]:
        raise TypeError(
            u"{} 必须是 Transform 或 Joint：{}".format(label, node)
        )

    return node


def validate_joint(joint):
    joint = resolve_transform(joint, u"Joint")
    if joint.nodeType() != "joint":
        raise TypeError(u"输入节点不是 Joint：{}".format(joint))
    return joint


def create_rig_name(node_type, side, region, feature, role, index=1):
    return name.create_name(
        node_type=node_type,
        side=name.normalize_side(side),
        part=name.normalize_name_part(region, "region"),
        function="{}_{}".format(
            name.normalize_name_part(feature, "feature"),
            name.normalize_name_part(role, "role")
        ),
        index=index
    )


def create_attachment_group(nodes_group, side, region, feature, role):
    group_name = create_rig_name(
        "grp", side, region, feature, role, 1
    )
    if pm.objExists(group_name):
        raise RuntimeError(u"Attachment Group 已存在：{}".format(group_name))
    return pm.createNode(
        "transform",
        name=group_name,
        parent=nodes_group
    )


def first_constraint(result):
    if isinstance(result, (list, tuple)):
        if not result:
            return None
        return result[0]
    return result


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
    if not joints:
        raise RuntimeError(u"没有给定需要附着的 Joint。")

    resolved_joints = []
    for joint in joints:
        resolved_joints.append(validate_joint(joint))

    drive_curve_shape = curve.get_curve_shape(drive_curve)
    aim_curve_shape = curve.get_curve_shape(aim_curve)

    up_curve_shape = None
    if up_curve is not None:
        up_curve_shape = curve.get_curve_shape(up_curve)
    else:
        up_object = resolve_transform(up_object, u"Up Object")

    if parent_group is not None:
        parent_group = resolve_transform(parent_group, u"Parent Group")

    side = name.normalize_side(side)
    region = name.normalize_name_part(region, "region")
    feature = name.normalize_name_part(feature, "feature")

    nodes_group_name = create_rig_name(
        "grp", side, region, feature, "rig_nodes", 1
    )
    joints_group_name = create_rig_name(
        "grp", side, region, feature, "attach_joints", 1
    )

    for node_name in [nodes_group_name, joints_group_name]:
        if pm.objExists(node_name):
            raise RuntimeError(
                u"Curve Attachment 节点已存在：{}".format(node_name)
            )

    nodes_group = None

    with undo_chunk("attach_joints_to_curves"):
        try:
            nodes_group = pm.createNode(
                "transform",
                name=nodes_group_name,
                parent=parent_group
            )
            joints_group = pm.createNode(
                "transform",
                name=joints_group_name,
                parent=nodes_group
            )
            drive_group = create_attachment_group(
                nodes_group, side, region, feature, "drive_attaches"
            )
            aim_group = create_attachment_group(
                nodes_group, side, region, feature, "aim_attaches"
            )

            up_group = None
            if up_curve_shape is not None:
                up_group = create_attachment_group(
                    nodes_group, side, region, feature, "up_attaches"
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
            while index < len(resolved_joints):
                joint = resolved_joints[index]
                item_index = index + 1
                joint_position = tuple(joint.getTranslation(space="world"))
                drive_parameter = curve.get_closest_parameter(
                    drive_curve_shape,
                    joint_position
                )
                percentage = curve.parameter_to_length_percentage(
                    drive_curve_shape,
                    drive_parameter
                )
                percentages.append(percentage)

                drive_result = curve.create_percentage_attachment(
                    curve_node=drive_curve_shape,
                    percentage=percentage,
                    name=create_rig_name(
                        "grp", side, region, feature, "drive_attach", item_index
                    ),
                    parent=drive_group
                )
                aim_result = curve.create_percentage_attachment(
                    curve_node=aim_curve_shape,
                    percentage=percentage,
                    name=create_rig_name(
                        "grp", side, region, feature, "aim_attach", item_index
                    ),
                    parent=aim_group
                )

                drive_attachment = drive_result["transform"]
                aim_attachment = aim_result["transform"]
                drive_attachments.append(drive_attachment)
                aim_attachments.append(aim_attachment)
                point_on_curve_nodes.append(drive_result["point_on_curve"])
                point_on_curve_nodes.append(aim_result["point_on_curve"])

                for matrix_node in drive_result["matrix_nodes"]:
                    matrix_nodes.append(matrix_node)
                for matrix_node in aim_result["matrix_nodes"]:
                    matrix_nodes.append(matrix_node)

                current_up_attachment = None
                if up_curve_shape is not None:
                    up_result = curve.create_percentage_attachment(
                        curve_node=up_curve_shape,
                        percentage=percentage,
                        name=create_rig_name(
                            "grp", side, region, feature, "up_attach", item_index
                        ),
                        parent=up_group
                    )
                    current_up_attachment = up_result["transform"]
                    up_attachments.append(current_up_attachment)
                    point_on_curve_nodes.append(up_result["point_on_curve"])
                    for matrix_node in up_result["matrix_nodes"]:
                        matrix_nodes.append(matrix_node)

                if current_up_attachment is not None:
                    constraint_result = pm.aimConstraint(
                        aim_attachment,
                        drive_attachment,
                        maintainOffset=False,
                        aimVector=(1.0, 0.0, 0.0),
                        upVector=(0.0, 1.0, 0.0),
                        worldUpType="object",
                        worldUpObject=current_up_attachment,
                        worldUpVector=(0.0, 1.0, 0.0)
                    )
                else:
                    constraint_result = pm.aimConstraint(
                        aim_attachment,
                        drive_attachment,
                        maintainOffset=False,
                        aimVector=(1.0, 0.0, 0.0),
                        upVector=(0.0, 1.0, 0.0),
                        worldUpType="objectrotation",
                        worldUpObject=up_object,
                        worldUpVector=(0.0, 1.0, 0.0)
                    )

                aim_constraint = first_constraint(constraint_result)
                if aim_constraint is None:
                    raise RuntimeError(
                        u"Aim Constraint 创建失败：{}".format(drive_attachment)
                    )
                aim_constraints.append(aim_constraint)

                zero_group = pm.createNode(
                    "transform",
                    name=create_rig_name(
                        "zero", side, region, feature, "attach", item_index
                    ),
                    parent=joints_group
                )
                parent_result = pm.parentConstraint(
                    drive_attachment,
                    zero_group,
                    maintainOffset=False
                )
                parent_constraint = first_constraint(parent_result)
                if parent_constraint is None:
                    raise RuntimeError(
                        u"Parent Constraint 创建失败：{}".format(zero_group)
                    )

                parent_constraints.append(parent_constraint)
                zero_groups.append(zero_group)
                joint.setParent(zero_group)
                joint.rotate.set((0.0, 0.0, 0.0))

                if not preserve_joint_offset:
                    joint.translate.set((0.0, 0.0, 0.0))

                index += 1

            return {
                "nodes_group": nodes_group,
                "joints_group": joints_group,
                "drive_group": drive_group,
                "aim_group": aim_group,
                "up_group": up_group,
                "joints": resolved_joints,
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
            if nodes_group is not None and pm.objExists(nodes_group):
                pm.delete(nodes_group)
            raise


__all__ = [
    "attach_joints_to_curves",
]
