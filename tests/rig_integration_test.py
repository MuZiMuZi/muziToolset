# coding=utf-8
u"""
Rig Integration Test
====================

验证 Muzi Toolset 的基础 Rig 构建链是否能够跨模块协同工作。

测试链：

    RigBase Naming
        ↓
    Joint
        ↓
    CtrlBase
        ↓
    zero / driven / space / connect / offset / ctrl / output
        ↓
    offsetParentMatrix
        ↓
    Joint Follow

覆盖：
    systems.rig_base
    systems.ctrl_base
    core.joint_utils
    core.hierarchy_utils
    core.matrix_utils
    core.transform_utils
    core.connection_utils
    core.scene_utils
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..core import connection_utils
from ..core import hierarchy_utils
from ..core import jnt_utils
from ..core import matrix_utils
from ..core import rename_utils
from ..core import scene_utils
from ..core import transform_utils
from ..systems import ctrl_base
from ..systems.rig_base import RigBase


# =============================================================================
# Helpers
# =============================================================================

def create_token():
    u"""创建短测试 Token。"""
    return "rig_integration_{}".format(
        uuid.uuid4().hex[:8]
    )


def create_temp_name(token, description):
    u"""创建非 Rig 标准的测试辅助节点名。"""
    return "__muzi_{}_{}".format(
        token,
        description
    )


def almost_equal(value_a, value_b, tolerance=0.0001):
    u"""浮点比较。"""
    return abs(value_a - value_b) <= tolerance


def delete_test_nodes(token):
    u"""删除本轮测试创建的 DAG / DG 节点。"""
    nodes = cmds.ls(
        "*{}*".format(token),
        long=True
    )

    if nodes is None:
        nodes = []

    node_data_list = []

    for node in nodes:
        node_data_list.append({
            "node": node,
            "depth": node.count("|"),
        })

    def get_depth(node_data):
        return node_data["depth"]

    node_data_list.sort(
        key=get_depth,
        reverse=True
    )

    for node_data in node_data_list:
        node = node_data["node"]

        if not cmds.objExists(node):
            continue

        try:
            cmds.delete(
                node
            )
        except Exception:
            pass


def assert_parent(child, expected_parent):
    u"""验证直接父子关系。"""
    actual_parent = hierarchy_utils.get_parent(
        child,
        full_path=False
    )
    expected_short_name = rename_utils.get_short_name(
        expected_parent
    )

    if actual_parent != expected_short_name:
        raise RuntimeError(
            u"Hierarchy 错误：{} 的 Parent 应为 {}，实际为 {}".format(
                child,
                expected_short_name,
                actual_parent
            )
        )


def assert_vector_equal(actual, expected, label):
    u"""验证两个三维向量一致。"""
    index = 0

    while index < 3:
        if not almost_equal(
                actual[index],
                expected[index]
        ):
            raise RuntimeError(
                u"{}：Expected={} | Actual={}".format(
                    label,
                    expected,
                    actual
                )
            )

        index += 1


def assert_exact_connection(
        source_plug,
        destination_plug,
        query_inputs=None
):
    u"""验证真实 Source -> Destination DG 连接。"""
    if query_inputs is None:
        query_inputs = connection_utils.get_input_connections(
            destination_plug
        )

    if not query_inputs:
        raise RuntimeError(
            u"Connection Query 没有找到输入：{}".format(
                destination_plug
            )
        )

    if not cmds.isConnected(
            source_plug,
            destination_plug
    ):
        raise RuntimeError(
            u"真实 DG 连接不存在：{} -> {} | Query={}".format(
                source_plug,
                destination_plug,
                query_inputs
            )
        )


# =============================================================================
# Integration
# =============================================================================

def test_rig_integration(token, keep_result=False):
    u"""执行完整基础 Rig 集成测试。"""
    rig_root = hierarchy_utils.ensure_group(
        create_temp_name(token, "rig")
    )
    control_group = hierarchy_utils.ensure_group(
        create_temp_name(token, "controls"),
        parent_node=rig_root
    )
    joint_group = hierarchy_utils.ensure_group(
        create_temp_name(token, "joints"),
        parent_node=rig_root
    )

    rig_identity = RigBase(
        side="md",
        part=token,
        index=1
    )

    joint_name = rig_identity.create_name(
        type="jnt",
        function="bind"
    )
    joint = joint_utils.Joint.create(
        name=joint_name,
        position=[4.0, 2.0, 1.0],
        radius=0.5,
        parent=joint_group
    )

    initial_joint_position = transform_utils.get_world_translation(
        joint
    )
    expected_initial_position = [
        4.0,
        2.0,
        1.0,
    ]
    assert_vector_equal(
        initial_joint_position,
        expected_initial_position,
        u"Joint 初始位置错误"
    )

    control_name = rig_identity.create_name(
        type="ctrl",
        function="main"
    )
    control_result = ctrl_base.create_ctrl(
        name=control_name,
        shape="circle",
        radius=1.0,
        axis="Y+",
        target_node=joint,
        parent_node=control_group,
        color=17,
        create_sub_ctrl=False,
        add_to_set=False
    )

    control = control_result["ctrl_node"]
    top_group = control_result["top_grp"]
    groups = control_result["grp_dict"]

    required_groups = [
        "zero",
        "driven",
        "space",
        "connect",
        "offset",
    ]

    for group_name in required_groups:
        if group_name not in groups:
            raise RuntimeError(
                u"CtrlBase 缺少标准层级：{}".format(
                    group_name
                )
            )

        if not cmds.objExists(
                groups[group_name]
        ):
            raise RuntimeError(
                u"CtrlBase 层级节点不存在：{}".format(
                    groups[group_name]
                )
            )

    assert_parent(control, groups["offset"])
    assert_parent(groups["offset"], groups["connect"])
    assert_parent(groups["connect"], groups["space"])
    assert_parent(groups["space"], groups["driven"])
    assert_parent(groups["driven"], groups["zero"])
    assert_parent(groups["zero"], control_group)
    assert_parent(joint, joint_group)

    if top_group != groups["zero"]:
        raise RuntimeError(
            u"CtrlBase top_grp 不是 Zero Group。"
        )

    control_initial_position = transform_utils.get_world_translation(
        control
    )
    assert_vector_equal(
        control_initial_position,
        initial_joint_position,
        u"Controller 没有正确吸附 Joint"
    )

    matrix_name = rig_identity.create_name(
        type="mult",
        function="parent"
    )
    matrix_node = matrix_utils.create_parent_matrix_constraint(
        driver=control,
        driven=joint,
        maintain_offset=True,
        name=matrix_name
    )

    if not cmds.objExists(matrix_node):
        raise RuntimeError(
            u"Parent Matrix Constraint 创建失败。"
        )

    constrained_joint_position = transform_utils.get_world_translation(
        joint
    )
    assert_vector_equal(
        constrained_joint_position,
        initial_joint_position,
        u"建立 OPM 后 Joint 发生跳变"
    )

    driver_matrix_source = control + ".worldMatrix[0]"
    driver_matrix_destination = matrix_node + ".matrixIn[2]"
    matrix_inputs = connection_utils.get_input_connections(
        driver_matrix_destination
    )
    assert_exact_connection(
        driver_matrix_source,
        driver_matrix_destination,
        query_inputs=matrix_inputs
    )

    opm_source = matrix_node + ".matrixSum"
    opm_destination = joint + ".offsetParentMatrix"
    opm_inputs = connection_utils.get_input_connections(
        opm_destination
    )
    assert_exact_connection(
        opm_source,
        opm_destination,
        query_inputs=opm_inputs
    )

    move_delta = [
        3.0,
        -1.5,
        2.0,
    ]
    target_control_position = [
        control_initial_position[0] + move_delta[0],
        control_initial_position[1] + move_delta[1],
        control_initial_position[2] + move_delta[2],
    ]
    transform_utils.set_world_translation(
        control,
        target_control_position
    )

    moved_joint_position = transform_utils.get_world_translation(
        joint
    )
    expected_joint_position = [
        initial_joint_position[0] + move_delta[0],
        initial_joint_position[1] + move_delta[1],
        initial_joint_position[2] + move_delta[2],
    ]
    assert_vector_equal(
        moved_joint_position,
        expected_joint_position,
        u"Joint 没有 1:1 跟随 Controller"
    )

    if keep_result:
        cmds.select(
            control,
            replace=True
        )
        return {
            "message": u"RigBase + CtrlBase + OPM Integration 成功，测试 Rig 已保留",
            "rig_root": rig_root,
            "control": control,
            "joint": joint,
            "matrix_node": matrix_node,
            "groups": groups,
            "kept": True,
        }

    removed = matrix_utils.remove_parent_matrix_constraint(
        joint,
        delete_node=True
    )

    if not removed:
        raise RuntimeError(
            u"Parent Matrix Constraint 移除失败。"
        )

    if cmds.objExists(matrix_node):
        raise RuntimeError(
            u"Matrix Constraint 删除后节点仍存在。"
        )

    if cmds.objExists(rig_root):
        cmds.delete(
            rig_root
        )

    if cmds.objExists(control):
        raise RuntimeError(
            u"Rig Cleanup 后 Controller 仍存在。"
        )

    if cmds.objExists(joint):
        raise RuntimeError(
            u"Rig Cleanup 后 Joint 仍存在。"
        )

    return {
        "message": u"RigBase + CtrlBase + OPM + Cleanup 成功",
        "rig_root": None,
        "control": None,
        "joint": None,
        "matrix_node": None,
        "groups": {},
        "kept": False,
    }


# =============================================================================
# Runner
# =============================================================================

def run(keep_result=False):
    u"""运行 Rig Integration Test。"""
    token = create_token()
    passed_count = 0
    failed_count = 0
    error_text = ""
    test_result = None

    print("")
    print("=" * 78)
    print("Muzi Toolset - Rig Integration Test")
    print("=" * 78)

    if keep_result:
        print("Mode: KEEP RESULT")
        print("-" * 78)

    scene_utils.open_undo_chunk(
        "MuziRigIntegrationTest"
    )

    try:
        test_result = test_rig_integration(
            token,
            keep_result=keep_result
        )
        passed_count = 1

        print(
            u"[PASS] Rig | RigBase -> CtrlBase -> OPM -> Joint | {}".format(
                test_result["message"]
            )
        )
    except Exception as error:
        failed_count = 1
        error_text = traceback.format_exc()

        print(
            u"[FAIL] Rig | RigBase -> CtrlBase -> OPM -> Joint | {}".format(
                error
            )
        )
        print(
            error_text
        )
    finally:
        if not keep_result:
            delete_test_nodes(
                token
            )

        scene_utils.close_undo_chunk()

    print("-" * 78)
    print(
        "Total: 1 | Passed: {} | Failed: {}".format(
            passed_count,
            failed_count
        )
    )
    print("=" * 78)

    return {
        "result": test_result,
        "passed": passed_count,
        "failed": failed_count,
        "traceback": error_text,
    }


__all__ = [
    "run",
]
