# coding=utf-8
u"""
Rig Integration Test
====================

验证 Muzi Toolset 的基础 Rig 构建链是否能够跨模块协同工作。

测试流程
--------
    Joint
        -> Controller
        -> zero / driven / space / connect / offset
        -> offsetParentMatrix
        -> 移动 Controller
        -> 验证 Joint
        -> 删除 Rig

覆盖模块
--------
    core.joint_utils
    systems.controller
    core.hierarchy_utils
    core.matrix_utils
    core.transform_utils
    core.connection_utils

说明
----
测试只创建带 ``__muzi_rig_integration_test_`` 前缀的临时节点，
不会清空当前场景。测试结束后无论成功失败都会清理本轮节点。
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..core import connection_utils
from ..core import hierarchy_utils
from ..core import joint_utils
from ..core import matrix_utils
from ..core import transform_utils
from ..systems import controller as controller_system


# =============================================================================
# Helpers
# =============================================================================

def create_token():
    """创建短测试 Token，避免与用户场景重名。"""
    return uuid.uuid4().hex[:8]


def create_name(token, description):
    """创建本轮测试使用的唯一节点名称。"""
    return "__muzi_rig_integration_test_{}_{}".format(
        token,
        description
    )


def almost_equal(value_a, value_b, tolerance=0.0001):
    """比较两个浮点数是否在允许误差内。"""
    return abs(value_a - value_b) <= tolerance


def get_parent(node):
    """返回节点直接 Parent 的短名称。"""
    parents = cmds.listRelatives(
        node,
        parent=True,
        fullPath=False
    )

    if parents is None:
        parents = []

    if not parents:
        return None

    return parents[0]


def delete_test_nodes(token):
    """
    删除本轮测试创建的 DAG / DG 节点。

    DAG 节点按照路径深度从深到浅删除。
    """
    nodes = cmds.ls(
        "*{}*".format(token),
        long=True
    )

    if nodes is None:
        nodes = []

    node_data_list = []

    for node in nodes:
        node_data = {
            "node": node,
            "depth": node.count("|"),
        }
        node_data_list.append(node_data)

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
            cmds.delete(node)
        except Exception:
            pass


def assert_parent(child, expected_parent):
    """验证直接父子关系。"""
    actual_parent = get_parent(child)

    if actual_parent != expected_parent:
        raise RuntimeError(
            u"Hierarchy 错误：{} 的 Parent 应为 {}，实际为 {}".format(
                child,
                expected_parent,
                actual_parent
            )
        )


# =============================================================================
# Integration Test
# =============================================================================

def test_rig_integration(token):
    """
    执行完整基础 Rig 集成测试。

    验证：
        1. Joint 创建；
        2. Controller 标准层级创建；
        3. Hierarchy Parent；
        4. Matrix OPM 网络；
        5. Connection Query；
        6. Controller Transform 驱动 Joint；
        7. Matrix 网络移除；
        8. Rig 整体删除。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：创建测试 Rig 根组。
    # -------------------------------------------------------------------------
    rig_root = hierarchy_utils.Hierarchy.create_grp(
        create_name(token, "rig")
    )

    control_group = hierarchy_utils.Hierarchy.create_grp(
        create_name(token, "controls"),
        parent=rig_root
    )

    joint_group = hierarchy_utils.Hierarchy.create_grp(
        create_name(token, "joints"),
        parent=rig_root
    )

    # -------------------------------------------------------------------------
    # 步骤 2：通过 joint_utils 创建 Joint。
    # -------------------------------------------------------------------------
    joint = joint_utils.Joint.create(
        name=create_name(token, "joint"),
        position=[4.0, 2.0, 1.0],
        radius=0.5
    )

    hierarchy_utils.Hierarchy.parent(
        joint,
        joint_group
    )

    initial_joint_position = transform_utils.get_world_translation(
        joint
    )

    expected_initial_position = [4.0, 2.0, 1.0]

    for index in range(3):
        if not almost_equal(
                initial_joint_position[index],
                expected_initial_position[index]
        ):
            raise RuntimeError(
                u"Joint 初始位置错误：{}".format(
                    initial_joint_position
                )
            )

    # -------------------------------------------------------------------------
    # 步骤 3：通过正式 Controller System 创建标准控制器层级。
    # -------------------------------------------------------------------------
    control_result = controller_system.create_controller(
        name="ctrl_{}_main_001".format(
            create_name(token, "control")
        ),
        shape="circle",
        radius=1.0,
        axis="Y+",
        target=joint,
        color=17,
        create_sub_control=False,
        create_extra_groups=True,
        add_to_set=False
    )

    control = control_result["control"]
    top_group = control_result["top_group"]
    groups = control_result["groups"]

    hierarchy_utils.Hierarchy.parent(
        top_group,
        control_group
    )

    # -------------------------------------------------------------------------
    # 步骤 4：验证 Controller 标准层级。
    #
    # zero
    #   driven
    #     space
    #       connect
    #         offset
    #           control
    # -------------------------------------------------------------------------
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
                u"Controller 缺少标准层级：{}".format(
                    group_name
                )
            )

        if not cmds.objExists(groups[group_name]):
            raise RuntimeError(
                u"Controller 层级节点不存在：{}".format(
                    groups[group_name]
                )
            )

    assert_parent(
        control,
        groups["offset"]
    )
    assert_parent(
        groups["offset"],
        groups["connect"]
    )
    assert_parent(
        groups["connect"],
        groups["space"]
    )
    assert_parent(
        groups["space"],
        groups["driven"]
    )
    assert_parent(
        groups["driven"],
        groups["zero"]
    )
    assert_parent(
        groups["zero"],
        control_group
    )
    assert_parent(
        joint,
        joint_group
    )

    # Controller 创建后应该吸附到 Joint，但不能改变 Joint。
    control_initial_position = transform_utils.get_world_translation(
        control
    )

    for index in range(3):
        if not almost_equal(
                control_initial_position[index],
                initial_joint_position[index]
        ):
            raise RuntimeError(
                u"Controller 没有正确吸附 Joint：Control={} | Joint={}".format(
                    control_initial_position,
                    initial_joint_position
                )
            )

    # -------------------------------------------------------------------------
    # 步骤 5：使用 matrix_utils 建立 Controller -> Joint OPM 驱动。
    # -------------------------------------------------------------------------
    matrix_node = matrix_utils.create_parent_matrix_constraint(
        driver=control,
        driven=joint,
        maintain_offset=True,
        name=create_name(token, "joint_parent_mm")
    )

    if not cmds.objExists(matrix_node):
        raise RuntimeError(u"Parent Matrix Constraint 创建失败。")

    # 建立 Maintain Offset 后 Joint 世界位置不能发生跳变。
    constrained_joint_position = transform_utils.get_world_translation(
        joint
    )

    for index in range(3):
        if not almost_equal(
                constrained_joint_position[index],
                initial_joint_position[index]
        ):
            raise RuntimeError(
                u"建立 OPM 后 Joint 发生跳变：Before={} | After={}".format(
                    initial_joint_position,
                    constrained_joint_position
                )
            )

    # -------------------------------------------------------------------------
    # 步骤 6：通过 connection_utils 验证真实 DG / OPM 连接。
    # -------------------------------------------------------------------------
    driver_matrix_source = control + ".worldMatrix[0]"
    driver_matrix_destination = matrix_node + ".matrixIn[2]"

    matrix_inputs = connection_utils.get_input_connections(
        driver_matrix_destination
    )

    if driver_matrix_source not in matrix_inputs:
        raise RuntimeError(
            u"Controller World Matrix 没有进入 multMatrix：{}".format(
                matrix_inputs
            )
        )

    opm_inputs = connection_utils.get_input_connections(
        joint + ".offsetParentMatrix"
    )

    expected_opm_source = matrix_node + ".matrixSum"

    if expected_opm_source not in opm_inputs:
        raise RuntimeError(
            u"Joint offsetParentMatrix 输入错误：{}".format(
                opm_inputs
            )
        )

    # -------------------------------------------------------------------------
    # 步骤 7：移动 Controller，并验证 Joint 世界位移 1:1 跟随。
    # -------------------------------------------------------------------------
    move_delta = [3.0, -1.5, 2.0]

    target_control_position = [
        control_initial_position[0] + move_delta[0],
        control_initial_position[1] + move_delta[1],
        control_initial_position[2] + move_delta[2],
    ]

    transform_utils.set_world_translation(
        control,
        target_control_position
    )

    moved_control_position = transform_utils.get_world_translation(
        control
    )
    moved_joint_position = transform_utils.get_world_translation(
        joint
    )

    expected_joint_position = [
        initial_joint_position[0] + move_delta[0],
        initial_joint_position[1] + move_delta[1],
        initial_joint_position[2] + move_delta[2],
    ]

    for index in range(3):
        if not almost_equal(
                moved_control_position[index],
                target_control_position[index]
        ):
            raise RuntimeError(
                u"Controller 世界位置设置失败：Expected={} | Actual={}".format(
                    target_control_position,
                    moved_control_position
                )
            )

        if not almost_equal(
                moved_joint_position[index],
                expected_joint_position[index]
        ):
            raise RuntimeError(
                u"Joint 没有 1:1 跟随 Controller：Expected={} | Actual={}".format(
                    expected_joint_position,
                    moved_joint_position
                )
            )

    # -------------------------------------------------------------------------
    # 步骤 8：移除 Matrix Constraint，确认 OPM 已断开且 DG 节点已删除。
    # -------------------------------------------------------------------------
    removed = matrix_utils.remove_parent_matrix_constraint(
        joint,
        delete_node=True
    )

    if not removed:
        raise RuntimeError(u"Parent Matrix Constraint 移除失败。")

    if cmds.objExists(matrix_node):
        raise RuntimeError(
            u"Matrix Constraint 移除后 multMatrix 仍然存在：{}".format(
                matrix_node
            )
        )

    remaining_opm_inputs = connection_utils.get_input_connections(
        joint + ".offsetParentMatrix"
    )

    if remaining_opm_inputs:
        raise RuntimeError(
            u"Matrix Constraint 移除后 OPM 仍有输入：{}".format(
                remaining_opm_inputs
            )
        )

    # -------------------------------------------------------------------------
    # 步骤 9：删除整个测试 Rig。
    # -------------------------------------------------------------------------
    if cmds.objExists(rig_root):
        cmds.delete(rig_root)

    deleted_nodes = [
        rig_root,
        control_group,
        joint_group,
        control,
        joint,
        groups["zero"],
        groups["connect"],
        groups["offset"],
    ]

    for node in deleted_nodes:
        if cmds.objExists(node):
            raise RuntimeError(
                u"Rig 删除后仍有 DAG 节点残留：{}".format(node)
            )

    return (
        u"Joint + Controller Hierarchy + OPM + "
        u"Transform Follow + Connection Query + Cleanup 成功"
    )


# =============================================================================
# Runner
# =============================================================================

def run():
    """运行 Rig Integration Test。"""
    token = create_token()
    passed_count = 0
    failed_count = 0
    error_text = ""

    print("")
    print("=" * 78)
    print("Muzi Toolset - Rig Integration Test")
    print("=" * 78)

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRigIntegrationTest"
    )

    try:
        message = test_rig_integration(token)
        passed_count = 1

        print(
            u"[PASS] Rig | Joint -> Controller -> OPM -> Joint | {}".format(
                message
            )
        )
    except Exception as error:
        failed_count = 1
        error_text = traceback.format_exc()

        print(
            u"[FAIL] Rig | Joint -> Controller -> OPM -> Joint | {}".format(
                error
            )
        )
        print(error_text)
    finally:
        delete_test_nodes(token)

        cmds.undoInfo(
            closeChunk=True
        )

    # 最终再次确认本轮 Token 没有残留节点。
    remaining_nodes = cmds.ls(
        "*{}*".format(token),
        long=True
    )

    if remaining_nodes is None:
        remaining_nodes = []

    if remaining_nodes:
        failed_count = 1
        passed_count = 0

        cleanup_message = (
            u"测试结束后仍有节点残留：{}".format(
                remaining_nodes
            )
        )

        if error_text:
            error_text += "\n" + cleanup_message
        else:
            error_text = cleanup_message

        print(
            u"[FAIL] Rig | Cleanup | {}".format(
                cleanup_message
            )
        )

    print("-" * 78)
    print(
        "Total: 1 | Passed: {} | Failed: {}".format(
            passed_count,
            failed_count
        )
    )
    print("=" * 78)

    return {
        "passed": passed_count,
        "failed": failed_count,
        "traceback": error_text,
    }


__all__ = [
    "run",
]
