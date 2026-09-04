# coding=utf-8
u"""
Face Build Functional Smoke Test
================================

验证 Face Build Package 的底层构建算法：
    - Eyelid Radial Jnt
    - Multi Curve Attachment
    - Matrix Zip Lip

完整 Jaw / Teeth / Eye 等业务单元统一称为 Module；
本文件只测试可复用 Build Algorithm，因此不使用 Component 术语。

测试辅助逻辑同样优先复用 Core；通用 Point / Vector Math 不在测试文件重复实现。
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..core import math_utils
from ..systems import face as face_system


# =============================================================================
# Helpers
# =============================================================================

def create_namespace():
    u"""创建独立测试 Namespace。"""
    token = uuid.uuid4().hex[:8]
    namespace = "muziFaceBuildSmoke_{}".format(
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
    u"""删除测试 Namespace 及其中全部节点。"""
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
            u"无法删除 Face Build Smoke Namespace {}：{}".format(
                namespace,
                error
            )
        )


def create_transform(name, parent=None, position=None):
    u"""创建测试 Transform。"""
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


def create_jnt(name, parent=None, position=None):
    u"""创建测试 Jnt。"""
    jnt = cmds.createNode(
        "joint",
        name=name,
        parent=parent
    )

    if position is not None:
        cmds.xform(
            jnt,
            worldSpace=True,
            translation=position
        )

    return jnt


def create_curve(name, points):
    u"""创建 Degree 3 测试 Curve。"""
    return cmds.curve(
        name=name,
        degree=3,
        point=points
    )


def run_case(results, name, test_function, root_group):
    u"""执行一个测试 Case。"""
    try:
        message = test_function(
            root_group
        )
        results.append({
            "name": name,
            "passed": True,
            "message": message,
            "traceback": "",
        })
    except Exception as error:
        results.append({
            "name": name,
            "passed": False,
            "message": str(error),
            "traceback": traceback.format_exc(),
        })


# =============================================================================
# Eyelid
# =============================================================================

def test_eyelid_builder(root_group):
    u"""真实创建五点 Upper Lid Radial Jnt Rig。"""
    eye_jnt = create_jnt(
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

    result = face_system.build_eyelid_jnts(
        curve=curve,
        eye_jnt=eye_jnt,
        up_object=up_object,
        side="lf",
        region="upper",
        parent_group=root_group,
        jnt_radius=0.15
    )

    if len(result["jnts"]) != 5:
        raise RuntimeError(
            u"Eyelid Jnt 数量错误：{}".format(
                len(result["jnts"])
            )
        )

    if len(result["attachments"]) != 5:
        raise RuntimeError(
            u"Eyelid Attachment 数量错误。"
        )

    index = 0

    while index < len(result["jnts"]):
        jnt_position = cmds.xform(
            result["jnts"][index],
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

        if math_utils.distance_between_points(
                jnt_position,
                attachment_position
        ) > 0.001:
            raise RuntimeError(
                u"Eyelid Jnt 没有落在 Attachment：{}".format(
                    index
                )
            )

        index += 1

    return u"5 Point Eyelid Radial Jnt Rig 创建成功"


# =============================================================================
# Curve Attachment
# =============================================================================

def test_curve_attachment(root_group):
    u"""测试不同 Curve Domain 下的弧长百分比同步。"""
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

    jnt_positions = [
        [0.25, 0.05, 0.0],
        [1.5, 0.4, 0.0],
        [2.75, 0.05, 0.0],
    ]
    jnts = []
    index = 0

    while index < len(jnt_positions):
        jnts.append(
            create_jnt(
                "jnt_lf_brow_smoke_{:03d}".format(
                    index + 1
                ),
                parent=root_group,
                position=jnt_positions[index]
            )
        )
        index += 1

    result = face_system.attach_jnts_to_curves(
        jnts=jnts,
        drive_curve=drive_curve,
        aim_curve=aim_curve,
        side="lf",
        region="brow",
        feature="smoke",
        up_object=up_object,
        parent_group=root_group,
        preserve_jnt_offset=True
    )

    if len(result["percentages"]) != 3:
        raise RuntimeError(
            u"Curve Attachment 百分比数量错误。"
        )

    for percentage in result["percentages"]:
        if percentage < 0.0 or percentage > 1.0:
            raise RuntimeError(
                u"Curve Attachment Percentage 超出范围：{}".format(
                    percentage
                )
            )

    if len(result["drive_attachments"]) != 3:
        raise RuntimeError(
            u"Drive Attachment 数量错误。"
        )

    if len(result["aim_attachments"]) != 3:
        raise RuntimeError(
            u"Aim Attachment 数量错误。"
        )

    return u"Drive / Aim Curve 弧长同步附着成功"


# =============================================================================
# Zip Lip
# =============================================================================

def test_zip_lip(root_group):
    u"""测试 Matrix Zip Lip 的完整闭合。"""
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

    upper_jnts = []
    lower_jnts = []
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

        upper_jnt = create_jnt(
            "jnt_md_lip_upper_smoke_{:03d}".format(
                item_number
            ),
            parent=upper_parent,
            position=[x_position, 0.5, 0.0]
        )
        lower_jnt = create_jnt(
            "jnt_md_lip_lower_smoke_{:03d}".format(
                item_number
            ),
            parent=lower_parent,
            position=[x_position, -0.5, 0.0]
        )

        upper_jnts.append(
            upper_jnt
        )
        lower_jnts.append(
            lower_jnt
        )
        index += 1

    result = face_system.build_zip_lip(
        upper_jnts=upper_jnts,
        lower_jnts=lower_jnts,
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
            pair["upper_jnt"],
            query=True,
            worldSpace=True,
            translation=True
        )
        lower_position = cmds.xform(
            pair["lower_jnt"],
            query=True,
            worldSpace=True,
            translation=True
        )

        distance = math_utils.distance_between_points(
            upper_position,
            lower_position
        )

        if distance > 0.001:
            raise RuntimeError(
                u"Zip Lip 完全闭合后上下 Jnt 没有重合：index={} distance={}".format(
                    index,
                    distance
                )
            )

        index += 1

    return u"4 Pair Matrix Zip Lip 完整闭合成功"


# =============================================================================
# Runner
# =============================================================================

def run():
    u"""执行 Face Build Functional Smoke Test。"""
    results = []
    namespace = create_namespace()

    print("")
    print("=" * 78)
    print("Muzi Toolset - Face Build Functional Smoke Test")
    print("=" * 78)

    try:
        root_group = cmds.createNode(
            "transform",
            name="grp_md_face_smoke_root_001"
        )

        run_case(
            results,
            "Eyelid Builder",
            test_eyelid_builder,
            root_group
        )
        run_case(
            results,
            "Curve Attachment",
            test_curve_attachment,
            root_group
        )
        run_case(
            results,
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
                u"[PASS] Face Build | {} | {}".format(
                    result["name"],
                    result["message"]
                )
            )
        else:
            failed_count += 1
            print(
                u"[FAIL] Face Build | {} | {}".format(
                    result["name"],
                    result["message"]
                )
            )
            print(
                result["traceback"]
            )

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
