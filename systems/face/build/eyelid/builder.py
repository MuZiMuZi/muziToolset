# coding=utf-8
u"""
Face Eyelid Builder
===================

基于 Curve CV 创建以眼球中心为 Pivot 的放射状 Joint。
"""

from __future__ import print_function

import pymel.core as pm

from .....core import curve
from .....core import name
from .....core.undo import undo_chunk


def resolve_transform(node, label):
    if node is None:
        raise ValueError(u"{} 不能为空。".format(label))
    if isinstance(node, str):
        if not pm.objExists(node):
            raise RuntimeError(u"{} 不存在：{}".format(label, node))
        node = pm.PyNode(node)
    if node.nodeType() not in ["transform", "joint"]:
        raise TypeError(u"{} 必须是 Transform 或 Joint：{}".format(label, node))
    return node


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


def first_constraint(result):
    if isinstance(result, (list, tuple)):
        if not result:
            return None
        return result[0]
    return result


def build_radial_curve_joints(
        curve_node,
        eye_joint,
        up_object,
        side,
        region,
        feature="lid",
        parent_group=None,
        joint_radius=0.2
):
    u"""基于 Curve CV 创建眼区放射状 Joint。"""
    curve_shape = curve.get_curve_shape(curve_node)
    eye_joint = resolve_transform(eye_joint, u"Eye Joint")
    if eye_joint.nodeType() != "joint":
        raise TypeError(u"Eye Joint 必须是 Joint：{}".format(eye_joint))

    up_object = resolve_transform(up_object, u"Up Object")
    if parent_group is not None:
        parent_group = resolve_transform(parent_group, u"Parent Group")

    side = name.normalize_side(side)
    region = name.normalize_name_part(region, "region")
    feature = name.normalize_name_part(feature, "feature")
    cv_positions = curve.get_cv_positions(curve_shape, world_space=True)

    if not cv_positions:
        raise RuntimeError(u"Curve 没有可用于创建 Joint 的 CV：{}".format(curve_shape))

    nodes_group_name = create_rig_name(
        "grp", side, region, feature, "rig_nodes", 1
    )
    attachments_group_name = create_rig_name(
        "grp", side, region, feature, "attaches", 1
    )
    joints_group_name = create_rig_name(
        "grp", side, region, feature, "joints", 1
    )

    for node_name in [nodes_group_name, attachments_group_name, joints_group_name]:
        if pm.objExists(node_name):
            raise RuntimeError(
                u"Eye Area Rig 节点已存在，请先清理旧结果：{}".format(node_name)
            )

    nodes_group = None

    with undo_chunk("build_radial_curve_joints"):
        try:
            nodes_group = pm.createNode(
                "transform",
                name=nodes_group_name,
                parent=parent_group
            )
            attachments_group = pm.createNode(
                "transform",
                name=attachments_group_name,
                parent=nodes_group
            )
            joints_group = pm.createNode(
                "transform",
                name=joints_group_name,
                parent=nodes_group
            )

            joints = []
            aim_groups = []
            attachments = []
            point_on_curve_nodes = []
            attachment_matrix_nodes = []
            aim_constraints = []
            eye_position = eye_joint.getTranslation(space="world")

            index = 0
            while index < len(cv_positions):
                item_index = index + 1
                attachment_result = curve.create_closest_point_attachment(
                    curve_node=curve_shape,
                    world_position=cv_positions[index],
                    name=create_rig_name(
                        "grp", side, region, feature, "attach", item_index
                    ),
                    parent=attachments_group
                )
                attachment = attachment_result["transform"]
                attachments.append(attachment)
                point_on_curve_nodes.append(attachment_result["point_on_curve"])

                for matrix_node in attachment_result["matrix_nodes"]:
                    attachment_matrix_nodes.append(matrix_node)

                aim_group = pm.createNode(
                    "transform",
                    name=create_rig_name(
                        "grp", side, region, feature, "aim", item_index
                    ),
                    parent=joints_group
                )
                aim_group.setTranslation(eye_position, space="world")

                constraint_result = pm.aimConstraint(
                    attachment,
                    aim_group,
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
                        u"Aim Constraint 创建失败：{}".format(aim_group)
                    )

                joint = pm.createNode(
                    "joint",
                    name=create_rig_name(
                        "jnt", side, region, feature, "bind", item_index
                    ),
                    parent=aim_group
                )
                attachment_position = attachment.getTranslation(space="world")
                joint_distance = (attachment_position - eye_position).length()
                joint.translate.set((joint_distance, 0.0, 0.0))
                joint.rotate.set((0.0, 0.0, 0.0))
                joint.radius.set(float(joint_radius))

                joints.append(joint)
                aim_groups.append(aim_group)
                aim_constraints.append(aim_constraint)
                index += 1

            return {
                "curve": curve_shape,
                "eye_joint": eye_joint,
                "up_object": up_object,
                "nodes_group": nodes_group,
                "attachments_group": attachments_group,
                "joints_group": joints_group,
                "attachments": attachments,
                "point_on_curve_nodes": point_on_curve_nodes,
                "attachment_matrix_nodes": attachment_matrix_nodes,
                "aim_groups": aim_groups,
                "aim_constraints": aim_constraints,
                "joints": joints,
                "side": side,
                "region": region,
                "feature": feature,
            }

        except Exception:
            if nodes_group is not None and pm.objExists(nodes_group):
                pm.delete(nodes_group)
            raise


def build_eyelid_joints(
        curve_node,
        eye_joint,
        up_object,
        side,
        region,
        parent_group=None,
        joint_radius=0.2
):
    return build_radial_curve_joints(
        curve_node=curve_node,
        eye_joint=eye_joint,
        up_object=up_object,
        side=side,
        region=region,
        feature="lid",
        parent_group=parent_group,
        joint_radius=joint_radius
    )


def build_eye_bag_joints(
        curve_node,
        eye_joint,
        up_object,
        side,
        region,
        parent_group=None,
        joint_radius=0.2
):
    return build_radial_curve_joints(
        curve_node=curve_node,
        eye_joint=eye_joint,
        up_object=up_object,
        side=side,
        region=region,
        feature="eye_bag",
        parent_group=parent_group,
        joint_radius=joint_radius
    )


__all__ = [
    "build_radial_curve_joints",
    "build_eyelid_joints",
    "build_eye_bag_joints",
]
