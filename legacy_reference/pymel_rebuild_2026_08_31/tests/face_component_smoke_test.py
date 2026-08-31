# coding=utf-8
u"""
Face Component Functional Smoke Test
====================================

验证从旧 pipelineUtils 迁出的正式 Face Component System：
    - systems.face.eyelid
    - systems.face.curve_attachment
    - systems.face.lip

测试原则：
    1. 在临时 Maya Namespace 中创建测试节点；
    2. 不依赖用户当前选择；
    3. 测试结束后删除整个临时 Namespace；
    4. 不保存场景；
    5. 建议在空场景执行，方便查看失败时的残留节点。
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..systems import face as face_system


# =============================================================================
# Helpers
# =============================================================================

def create_namespace():
    """创建独立测试 Namespace。"""
    token = uuid.uuid4().hex[:8]
    namespace = "muziFaceSmoke_{}".format(
        token
    )

    cmds.namespace(
        add=namespace
    )
    cmds.namespace(
        set=namespace
    )

    return namespace


def remove_namespace(namespace):
    """删除测试 Namespace 及其中全部节点。"""
    try:
        cmds.namespace(
            set=":"
        )
    except Exception:
        pass

    if not cmds.namespace(
            exists=namespace
    ):
        return

    try:
        cmds.namespace(
            removeNamespace=namespace,
            deleteNamespaceContent=True
        )
    except Exception as error:
        cmds.warning(
            u"无法删除 Face Smoke Test Namespace {}：{}".format(
                namespace,
                error
            )
        )


def create_result(category, name, passed, message, traceback_text=""):
    """创建测试结果。"""
    return {
        "category": category,
        "name": name,
        "passed": passed,
        "message": message,
        "traceback": traceback_text,
    }


def run_case(results, category, name, test_function, root_group):
    """执行一个测试函数。"""
    try:
        message = test_function(
            root_group
        )
        results.append(
            create_result(
                category,
                name,
                True,
                message
            )
        )
    except Exception as error:
        results.append(
            create_result(
                category,
                name,
                False,
                str(error),
                traceback.format_exc()
            )
        )


def create_curve(name, points):
    """创建 Degree 3 测试 Curve。"""
    return cmds.curve(
        name=name,
        degree=3,
        point=points
    )


def create_transform(name, parent=None, position=None):
    """创建测试 Transform。"""
    transform = cmds.createNode(
        "transform",
        name=name,
        parent=parent
    )

    if position is not None:
        cmds.xform(
            transform,
            worldSpace=True,
            translation=position
        )

    return transform


def create_joint(name, parent=None, position=None):
    """创建测试 Joint。"""
    joint = cmds.createNode(
        "joint",
        name=name,
        parent=parent
    )

    if position is not None:
        cmds.xform(
            joint,
            worldSpace=True,
            translation=position
        )

    return joint


def distance_between_points(point_a, point_b):
    """简单计算两点距离，避免测试反向依赖待测 Transform Utils。"""
    delta_x = point_b[0] - point_a[0]
    delta_y = point_b[1] - point_a[1]
    delta_z = point_b[2] - point_a[2]

    distance = (
        delta_x * delta_x
        + delta_y * delta_y
        + delta_z * delta_z
    ) ** 0.5

    return distance


# =============================================================================
# Eyelid
# =============================================================================

def test_eyelid_builder(root_group):
    """真实创建五点 Upper Lid Radial Joint Rig。"""
    eye_joint = create_joint(
        "jnt_lf_eye_center_smoke_001",
        parent=root_group,
        position=[0.0, 0.0, 0.0]
    )
    up_object = create_transform(
        "loc_lf_eye_up_smoke_001",
        parent=root_group,
        position=[0.0, 3.0, 0.0]
    )

    curve = create_curve(
        "crv_lf_upper_lid_smoke_001",
        [
            [3.0, -1.0, 0.0],
            [3.2, -0.5, 0.3],
            [3.3, 0.0, 0.5],
            [3.2, 0.5, 0.3],
            [3.0, 1.0, 0.0],
        ]
    )
    curve = cmds.parent(
        curve,
        root_group
    )[0]

    result = face_system.build_eyelid_joints(
        curve=curve,
        eye_joint=eye_joint,
        up_object=up_object,
        side="lf",
        region="upper",
        parent_group=root_group,
        joint_radius=0.15
    )

    if len(result["joints"]) != 5:
        raise RuntimeError(
            u"Eyelid Joint 数量错误：{}".format(
                len(result["joints"])
            )
        )

    if len(result["attachments"]) != 5:
        raise RuntimeError(
            u"Eyelid Attachment 数量错误。"
        )

    index = 0

    while index < len(result["joints"]):
        joint_position = cmds.xform(
            result["joints"][index],
            query=True,
            worldSpace=True,
            translation=True
        )
        attachment_position = cmds.xform(
            result["attachments"][index],
            query=True,
            worldSpace=True,
            translation=True
        )

        distance = distance_between_points(
            joint_position,
            attachment_position
        )

        if distance > 0.001:
            raise RuntimeError(
                u"Eyelid Joint 没有落在 Attachment：index={} distance={}".format(
                    index,
                    distance
                )
            )

        index += 1

    return u"5 Point Eyelid Radial Joint Rig 创建成功"


# =============================================================================
# Multi Curve Attachment
# =============================================================================

def test_curve_attachment(root_group):
    """测试不同 Curve Domain 下的弧长百分比同步。"""
    drive_curve = create_curve(
        "crv_lf_brow_drive_smoke_001",
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.3, 0.0],
            [2.0, 0.4, 0.0],
            [3.0, 0.0, 0.0],
        ]
    )
    aim_curve = create_curve(
        "crv_lf_brow_aim_smoke_001",
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.6, 1.2],
            [2.0, 0.6, 1.2],
            [3.0, 0.0, 1.0],
        ]
    )

    drive_curve = cmds.parent(
        drive_curve,
        root_group
    )[0]
    aim_curve = cmds.parent(
        aim_curve,
        root_group
    )[0]

    up_object = create_transform(
        "loc_lf_brow_up_smoke_001",
        parent=root_group,
        position=[0.0, 3.0, 0.0]
    )

    joints = []
    joint_positions = [
        [0.25, 0.05, 0.0],
        [1.5, 0.4, 0.0],
        [2.75, 0.05, 0.0],
    ]

    index = 0

    while index < len(joint_positions):
        joint = create_joint(
            "jnt_lf_brow_smoke_{:03d}".format(
                index + 1
            ),
            parent=root_group,
            position=joint_positions[index]
        )
        joints.append(joint)
        index += 1

    result = face_system.attach_joints_to_curves(
        joints=joints,
        drive_curve=drive_curve,
        aim_curve=aim_curve,
        side="lf",
        region="brow",
        feature="smoke",
        up_object=up_object,
        parent_group=root_group,
        preserve_joint_offset=True
    )

    if len(result["percentages"]) != 3:
        raise RuntimeError(u"Curve Attachment 百分比数量错误。")

    for percentage in result["percentages"]:
        if percentage < 0.0 or percentage > 1.0:
            raise RuntimeError(
                u"Curve Attachment Percentage 超出范围：{}".format(
                    percentage
                )
            )

    if len(result["drive_attachments"]) != 3:
        raise RuntimeError(u"Drive Attachment 数量错误。")

    if len(result["aim_attachments"]) != 3:
        raise RuntimeError(u"Aim Attachment 数量错误。")

    return u"Drive / Aim Curve 弧长同步附着成功"


# =============================================================================
# Zip Lip
# =============================================================================

def test_zip_lip(root_group):
    """测试 Matrix Zip Lip 的完整闭合。"""
    left_control = create_transform(
        "ctrl_lf_lip_corner_smoke_001",
        parent=root_group
    )
    right_control = create_transform(
        "ctrl_rt_lip_corner_smoke_001",
        parent=root_group
    )
    jaw_control = create_transform(
        "ctrl_md_jaw_smoke_001",
        parent=root_group
    )

    upper_joints = []
    lower_joints = []
    x_positions = [
        -3.0,
        -1.0,
        1.0,
        3.0,
    ]

    index = 0

    while index < len(x_positions):
        item_number = index + 1
        x_position = x_positions[index]

        upper_parent = create_transform(
            "grp_md_lip_upper_smoke_{:03d}".format(
                item_number
            ),
            parent=root_group
        )
        lower_parent = create_transform(
            "grp_md_lip_lower_smoke_{:03d}".format(
                item_number
            ),
            parent=root_group
        )

        upper_joint = create_joint(
            "jnt_md_lip_upper_smoke_{:03d}".format(
                item_number
            ),
            parent=upper_parent,
            position=[x_position, 0.5, 0.0]
        )
        lower_joint = create_joint(
            "jnt_md_lip_lower_smoke_{:03d}".format(
                item_number
            ),
            parent=lower_parent,
            position=[x_position, -0.5, 0.0]
        )

        upper_joints.append(upper_joint)
        lower_joints.append(lower_joint)
        index += 1

    result = face_system.build_zip_lip(
        upper_joints=upper_joints,
        lower_joints=lower_joints,
        left_zip_control=left_control,
        right_zip_control=right_control,
        jaw_control=jaw_control,
        zip_height=0.5,
        falloff=2,
        utility_parent=root_group
    )

    if len(result["pairs"]) != 4:
        raise RuntimeError(
            u"Zip Lip Pair 数量错误：{}".format(
                len(result["pairs"])
            )
        )

    cmds.setAttr(
        result["left_zip_plug"],
        1.0
    )
    cmds.setAttr(
        result["right_zip_plug"],
        1.0
    )
    cmds.setAttr(
        result["zip_height_plug"],
        0.5
    )

    cmds.dgdirty(
        allPlugs=True
    )

    index = 0

    while index < len(result["pairs"]):
        pair = result["pairs"][index]

        upper_position = cmds.xform(
            pair["upper_joint"],
            query=True,
            worldSpace=True,
            translation=True
        )
        lower_position = cmds.xform(
            pair["lower_joint"],
            query=True,
            worldSpace=True,
            translation=True
        )

        distance = distance_between_points(
            upper_position,
            lower_position
        )

        if distance > 0.001:
            raise RuntimeError(
                u"Zip Lip 完全闭合后上下 Joint 没有重合：index={} distance={}".format(
                    index,
                    distance
                )
            )

        if abs(upper_position[1]) > 0.001:
            raise RuntimeError(
                u"zipHeight=0.5 时闭合位置没有位于中间：{}".format(
                    upper_position
                )
            )

        index += 1

    return u"4 Pair Matrix Zip Lip 完整闭合成功"


# =============================================================================
# Runner
# =============================================================================

def run():
    """执行 Face Component Functional Smoke Test。"""
    results = []
    namespace = create_namespace()

    print("")
    print("=" * 78)
    print("Muzi Toolset - Face Component Functional Smoke Test")
    print("=" * 78)

    try:
        root_group = cmds.createNode(
            "transform",
            name="grp_md_face_smoke_root_001"
        )

        run_case(
            results,
            "Face",
            "Eyelid Builder",
            test_eyelid_builder,
            root_group
        )
        run_case(
            results,
            "Face",
            "Curve Attachment",
            test_curve_attachment,
            root_group
        )
        run_case(
            results,
            "Face",
            "Matrix Zip Lip",
            test_zip_lip,
            root_group
        )
    finally:
        remove_namespace(
            namespace
        )

    passed_count = 0
    failed_count = 0

    for result in results:
        if result["passed"]:
            passed_count += 1
            print(
                u"[PASS] {} | {} | {}".format(
                    result["category"],
                    result["name"],
                    result["message"]
                )
            )
        else:
            failed_count += 1
            print(
                u"[FAIL] {} | {} | {}".format(
                    result["category"],
                    result["name"],
                    result["message"]
                )
            )
            print(result["traceback"])

    print("-" * 78)
    print(
        "Total: {} | Passed: {} | Failed: {}".format(
            len(results),
            passed_count,
            failed_count
        )
    )
    print("=" * 78)

    return {
        "results": results,
        "passed": passed_count,
        "failed": failed_count,
    }


__all__ = [
    "run",
]
