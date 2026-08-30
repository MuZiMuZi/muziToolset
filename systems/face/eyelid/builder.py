# coding=utf-8
u"""
Face Eyelid Builder
===================

把旧 pipelineUtils.create_eyelid_joints_on_curve 的有效算法迁入正式 Face System。

设计变化：
    1. Curve 查询和 Attachment 创建交给 core.curve_utils；
    2. 不再修改或重新 Parent 输入 Curve；
    3. 不再创建临时 nearestPointOnCurve 的重复代码；
    4. Joint 使用眼球中心作为 Pivot，Aim Group 指向 Curve Attachment；
    5. 眼皮和眼袋使用同一套构建函数；
    6. 构建失败时自动清理本次创建的 Rig Nodes Group。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import curve_utils
from ....core import name_utils
from ....core import transform_utils


# =============================================================================
# Validate
# =============================================================================

def validate_transform(node, label):
    """检查 Transform / Joint 输入。"""
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
            u"{}必须是 Transform 或 Joint：{} | type={}".format(
                label,
                node,
                node_type
            )
        )

    return True


def validate_side(side):
    """把方向统一成 lf / rt / md。"""
    return name_utils.Name.normalize_side(side)


def normalize_name_part(value, label):
    """清理用于 Rig 命名的字段。"""
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


# =============================================================================
# Naming
# =============================================================================

def create_rig_name(
        node_type,
        side,
        region,
        feature,
        role,
        index=1
):
    """
    创建 Eye Area Rig 名称。

    例如：
        grp_lf_upper_lid_rig_nodes_001
        grp_lf_lower_eye_bag_attach_003
        jnt_lf_upper_lid_bind_005
    """
    side = validate_side(side)
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
# Build
# =============================================================================

def build_radial_curve_joints(
        curve,
        eye_joint,
        up_object,
        side,
        region,
        feature="lid",
        parent_group=None,
        joint_radius=0.2
):
    """
    基于 Curve CV 创建眼区放射状 Joint。

    适用：
        upper lid
        lower lid
        upper eye bag
        lower eye bag

    原理：
        Eye Center
            -> Aim Group
                -> Bind Joint

        Curve
            -> pointOnCurveInfo
                -> Attachment
                    -> Aim Constraint -> Aim Group

    Joint 本身不承担 Aim Constraint，Aim Group 负责方向；
    Joint 只沿 Local X 放置到眼皮 / 眼袋位置，便于后续蒙皮和驱动。

    Args:
        curve(str): 眼皮 / 眼袋驱动 Curve。
        eye_joint(str): 眼球中心 Joint 或 Transform。
        up_object(str): Aim Constraint World Up 参考物体。
        side(str): lf / rt / md。
        region(str): upper / lower。
        feature(str): lid / eye_bag 等。
        parent_group(str/None): Rig Nodes Group 的父组。
        joint_radius(float): Joint 显示半径。

    Returns:
        dict: 构建结果。
    """
    curve_utils.get_curve_shape(curve)
    validate_transform(
        eye_joint,
        u"Eye Joint"
    )
    validate_transform(
        up_object,
        u"Up Object"
    )

    if parent_group is not None:
        validate_transform(
            parent_group,
            u"Parent Group"
        )

    side = validate_side(side)
    region = normalize_name_part(
        region,
        "region"
    )
    feature = normalize_name_part(
        feature,
        "feature"
    )

    cv_positions = curve_utils.get_curve_cv_positions(
        curve,
        world_space=True
    )

    if not cv_positions:
        raise RuntimeError(
            u"Curve 没有可用于创建 Joint 的 CV：{}".format(
                curve
            )
        )

    nodes_group_name = create_rig_name(
        "grp",
        side,
        region,
        feature,
        "rig_nodes",
        1
    )
    attachments_group_name = create_rig_name(
        "grp",
        side,
        region,
        feature,
        "attaches",
        1
    )
    joints_group_name = create_rig_name(
        "grp",
        side,
        region,
        feature,
        "joints",
        1
    )

    names_to_check = [
        nodes_group_name,
        attachments_group_name,
        joints_group_name,
    ]

    for node_name in names_to_check:
        if cmds.objExists(node_name):
            raise RuntimeError(
                u"Eye Area Rig 节点已经存在，请先清理旧结果：{}".format(
                    node_name
                )
            )

    nodes_group = None

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziFaceEyelidBuild"
    )

    try:
        nodes_group = cmds.createNode(
            "transform",
            name=nodes_group_name,
            parent=parent_group
        )

        attachments_group = cmds.createNode(
            "transform",
            name=attachments_group_name,
            parent=nodes_group
        )

        joints_group = cmds.createNode(
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

        eye_position = cmds.xform(
            eye_joint,
            query=True,
            worldSpace=True,
            translation=True
        )

        index = 0

        while index < len(cv_positions):
            item_index = index + 1
            cv_position = cv_positions[index]

            attachment_name = create_rig_name(
                "grp",
                side,
                region,
                feature,
                "attach",
                item_index
            )

            attachment_result = curve_utils.create_closest_point_attachment(
                curve=curve,
                world_position=cv_position,
                name=attachment_name,
                parent=attachments_group
            )

            attachment = attachment_result["transform"]
            attachments.append(attachment)
            point_on_curve_nodes.append(
                attachment_result["point_on_curve"]
            )

            for matrix_node in attachment_result["matrix_nodes"]:
                attachment_matrix_nodes.append(matrix_node)

            aim_group_name = create_rig_name(
                "grp",
                side,
                region,
                feature,
                "aim",
                item_index
            )

            aim_group = cmds.createNode(
                "transform",
                name=aim_group_name,
                parent=joints_group
            )

            cmds.xform(
                aim_group,
                worldSpace=True,
                translation=eye_position
            )

            aim_constraint = cmds.aimConstraint(
                attachment,
                aim_group,
                aimVector=[1.0, 0.0, 0.0],
                upVector=[0.0, 1.0, 0.0],
                worldUpType="objectrotation",
                worldUpObject=up_object,
                worldUpVector=[0.0, 1.0, 0.0],
                maintainOffset=False
            )[0]

            joint_name = create_rig_name(
                "jnt",
                side,
                region,
                feature,
                "bind",
                item_index
            )

            joint = cmds.createNode(
                "joint",
                name=joint_name,
                parent=aim_group
            )

            joint_distance = transform_utils.distance_between(
                eye_joint,
                attachment
            )

            cmds.setAttr(
                joint + ".translateX",
                joint_distance
            )
            cmds.setAttr(
                joint + ".translateY",
                0.0
            )
            cmds.setAttr(
                joint + ".translateZ",
                0.0
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
            cmds.setAttr(
                joint + ".radius",
                joint_radius
            )

            joints.append(joint)
            aim_groups.append(aim_group)
            aim_constraints.append(aim_constraint)

            index += 1

        result = {
            "curve": curve,
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


def build_eyelid_joints(
        curve,
        eye_joint,
        up_object,
        side,
        region,
        parent_group=None,
        joint_radius=0.2
):
    """眼皮专用入口。"""
    return build_radial_curve_joints(
        curve=curve,
        eye_joint=eye_joint,
        up_object=up_object,
        side=side,
        region=region,
        feature="lid",
        parent_group=parent_group,
        joint_radius=joint_radius
    )


def build_eye_bag_joints(
        curve,
        eye_joint,
        up_object,
        side,
        region,
        parent_group=None,
        joint_radius=0.2
):
    """眼袋专用入口。"""
    return build_radial_curve_joints(
        curve=curve,
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
