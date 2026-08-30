# coding=utf-8
u"""
Face Eyelid Builder
===================

把旧 pipelineUtils.create_eyelid_joints_on_curve 的有效算法迁入正式 Face System。

设计边界：
    1. Curve 查询和 Attachment 创建交给 core.curve_utils；
    2. Transform / Joint 输入校验交给 core.transform_utils；
    3. 通用 Transform Group 创建交给 core.scene_utils；
    4. Aim Constraint 创建交给 core.constraint_utils；
    5. Maya Undo Chunk 交给 core.scene_utils；
    6. Joint 使用眼球中心作为 Pivot，沿 Local X 放射到 Curve Attachment；
    7. 眼皮和眼袋使用同一套构建函数；
    8. 构建失败时自动清理本次创建的 Rig Nodes Group。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import constraint_utils
from ....core import curve_utils
from ....core import name_utils
from ....core import scene_utils
from ....core import transform_utils


# =============================================================================
# Validate
# =============================================================================

def validate_transform(node, label):
    u"""
    检查 Transform / Joint 输入。

    保留旧公开入口，实际节点类型校验统一由 transform_utils 维护。
    """
    if not node:
        raise RuntimeError(
            u"{}不能为空。".format(label)
        )

    try:
        # 使用 Transform Core 统一检查节点存在性和 Transform / Joint 类型。
        transform_utils.validate_transform(
            node
        )
    except RuntimeError as error:
        raise RuntimeError(
            u"{}无效：{}".format(
                label,
                error
            )
        )

    return True


def validate_side(side):
    u"""把方向统一成 lf / rt / md。"""
    # 使用统一 Rig Naming API 规范 Side Token。
    return name_utils.Name.normalize_side(
        side
    )


def normalize_name_part(value, label):
    u"""清理用于 Rig 命名的字段。"""
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
    u"""
    创建 Eye Area Rig 名称。

    例如：
        grp_lf_upper_lid_rig_nodes_001
        grp_lf_lower_eye_bag_attach_003
        jnt_lf_upper_lid_bind_005
    """
    # 统一规范 Side，避免 l / left / lf 等不同输入产生多套命名。
    side = validate_side(
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

    # 使用项目正式五段式命名 API 创建最终节点名称。
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

@scene_utils.undo_chunk
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
    u"""
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
    Joint 只沿 Local X 放置到眼皮 / 眼袋位置。
    """
    # 使用 Curve Core 验证输入 Curve，并取得真实 NURBS Curve Shape。
    curve_utils.get_curve_shape(
        curve
    )

    # 检查眼球中心 Joint / Transform 是否可以参与空间计算。
    validate_transform(
        eye_joint,
        u"Eye Joint"
    )

    # 检查 Aim Constraint 使用的 Up Object。
    validate_transform(
        up_object,
        u"Up Object"
    )

    if parent_group is not None:
        # 如果提供父层级，先确认它是有效 Transform / Joint。
        validate_transform(
            parent_group,
            u"Parent Group"
        )

    # 规范 Side / Region / Feature，保证本次创建的全部节点命名一致。
    side = validate_side(
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

    # 获取 Curve 全部 CV 世界位置，每个 CV 对应一个放射 Joint。
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

    # 生成本次 Eye Area Rig 的三个主层级名称。
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

    try:
        # 使用 Scene Core 创建 Eye Area Rig 顶层 Nodes Group。
        nodes_group = scene_utils.create_node(
            "transform",
            nodes_group_name,
            parent=parent_group
        )

        # 创建所有 Curve Attachment 的统一容器。
        attachments_group = scene_utils.create_node(
            "transform",
            attachments_group_name,
            parent=nodes_group
        )

        # 创建 Aim Group / Bind Joint 的统一容器。
        joints_group = scene_utils.create_node(
            "transform",
            joints_group_name,
            parent=nodes_group
        )

        joints = []
        aim_groups = []
        attachments = []
        point_on_curve_nodes = []
        attachment_matrix_nodes = []
        aim_constraints = []

        # 使用 Transform Core 读取眼球中心世界位置，所有 Aim Group 都从此 Pivot 出发。
        eye_position = transform_utils.get_world_translation(
            eye_joint
        )

        index = 0

        while index < len(cv_positions):
            item_index = index + 1
            cv_position = cv_positions[index]

            # 生成当前 CV 对应的 Curve Attachment 名称。
            attachment_name = create_rig_name(
                "grp",
                side,
                region,
                feature,
                "attach",
                item_index
            )

            # 使用 Curve Core 在最接近当前 CV 的位置创建稳定 Attachment。
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

            # 生成当前放射 Joint 使用的 Aim Group 名称。
            aim_group_name = create_rig_name(
                "grp",
                side,
                region,
                feature,
                "aim",
                item_index
            )

            # 创建 Aim Group，并把 Pivot 放在眼球中心位置。
            aim_group = scene_utils.create_node(
                "transform",
                aim_group_name,
                parent=joints_group
            )

            transform_utils.set_world_translation(
                aim_group,
                eye_position
            )

            # 使用 Constraint Core 让 Aim Group 指向对应 Curve Attachment。
            aim_constraint_nodes = constraint_utils.create_constraint(
                driver_objects=attachment,
                driven_object=aim_group,
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
                        aim_group
                    )
                )

            aim_constraint = aim_constraint_nodes[0]

            # 生成当前放射 Bind Joint 的正式名称。
            joint_name = create_rig_name(
                "jnt",
                side,
                region,
                feature,
                "bind",
                item_index
            )

            # Joint 必须直接创建在 Aim Group 下，保持 Local Transform 从零开始。
            joint = cmds.createNode(
                "joint",
                name=joint_name,
                parent=aim_group
            )

            # 计算眼球中心到当前 Attachment 的距离，作为 Joint Local X 长度。
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

        return {
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

    except Exception:
        # 构建失败时删除本次顶层 Nodes Group，同时清理其全部子节点。
        if nodes_group is not None:
            if cmds.objExists(nodes_group):
                cmds.delete(
                    nodes_group
                )

        raise


def build_eyelid_joints(
        curve,
        eye_joint,
        up_object,
        side,
        region,
        parent_group=None,
        joint_radius=0.2
):
    u"""眼皮专用入口。"""
    # 复用统一 Radial Curve Joint Builder，只把 Feature 固定为 lid。
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
    u"""眼袋专用入口。"""
    # 复用统一 Radial Curve Joint Builder，只把 Feature 固定为 eye_bag。
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
