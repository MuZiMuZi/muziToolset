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
        -> 可选保留 Rig / 自动删除 Rig

覆盖模块
--------
    core.joint_utils
    systems.controller
    core.hierarchy_utils
    core.matrix_utils
    core.transform_utils
    core.connection_utils

观察模式
--------
默认 ``keep_result=False``，测试结束后自动清理测试节点。

如果使用::

    muziToolset.rig_integration_test(keep_result=True)

测试通过后会保留 Joint、Controller、标准控制器层级和 multMatrix OPM 网络，
并自动选择 Controller，方便直接在 Maya 视图中拖动控制器观察 Joint 跟随。

Maya 对 Array Plug 的 ``listConnections(plugs=True)`` 返回值并不总是保留
显式索引。例如真实连接可能是 ``worldMatrix[0] -> matrixIn[2]``，查询时
却返回 ``worldMatrix``。因此本测试使用 ``cmds.isConnected`` 判断精确连接，
同时保留 connection_utils 查询来验证 Core Query API 确实能找到输入。
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


def assert_vector_equal(actual, expected, label):
    """验证两个三维数值向量一致。"""
    for index in range(3):
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


def assert_exact_connection(source_plug, destination_plug, query_inputs=None):
    """
    验证 Maya 中真实存在 Source -> Destination 连接。

    ``cmds.isConnected`` 用于精确判定；``query_inputs`` 只用于错误报告和
    验证 connection_utils 至少能够查询到输入，不直接依赖 Maya 对 Array
    Plug 是否保留 ``[0]`` 的字符串表现形式。
    """
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
# Integration Test
# =============================================================================

def test_rig_integration(token, keep_result=False):
    """
    执行完整基础 Rig 集成测试。

    Args:
        token(str):
            本轮测试唯一 Token。

        keep_result(bool):
            False：完成验证后移除 Matrix 并删除测试 Rig。
            True：保留完整绑定结果，方便在 Maya 中观察和手动操作。

    验证：
        1. Joint 创建；
        2. Controller 标准层级创建；
        3. Hierarchy Parent；
        4. Matrix OPM 网络；
        5. Connection Query；
        6. Controller Transform 驱动 Joint；
        7. 非观察模式下移除 Matrix 网络；
        8. 非观察模式下删除整个 Rig。
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

    assert_vector_equal(
        initial_joint_position,
        expected_initial_position,
        u"Joint 初始位置错误"
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

    assert_vector_equal(
        control_initial_position,
        initial_joint_position,
        u"Controller 没有正确吸附 Joint"
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

    assert_vector_equal(
        constrained_joint_position,
        initial_joint_position,
        u"建立 OPM 后 Joint 发生跳变"
    )

    # -------------------------------------------------------------------------
    # 步骤 6：验证真实 DG / OPM 连接。
    # -------------------------------------------------------------------------
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

    assert_vector_equal(
        moved_control_position,
        target_control_position,
        u"Controller 世界位置设置失败"
    )

    assert_vector_equal(
        moved_joint_position,
        expected_joint_position,
        u"Joint 没有 1:1 跟随 Controller"
    )

    # -------------------------------------------------------------------------
    # 步骤 8：观察模式下保留真实绑定结果。
    # -------------------------------------------------------------------------
    if keep_result:
        cmds.select(
            control,
            replace=True
        )

        return {
            "message": (
                u"Joint + Controller Hierarchy + OPM + "
                u"Transform Follow + Connection Query 成功，测试 Rig 已保留"
            ),
            "rig_root": rig_root,
            "control_group": control_group,
            "joint_group": joint_group,
            "control": control,
            "joint": joint,
            "matrix_node": matrix_node,
            "groups": groups,
            "kept": True,
        }

    # -------------------------------------------------------------------------
    # 步骤 9：标准测试模式下移除 Matrix Constraint。
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
    # 步骤 10：删除整个测试 Rig。
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

    return {
        "message": (
            u"Joint + Controller Hierarchy + OPM + "
            u"Transform Follow + Connection Query + Cleanup 成功"
        ),
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
    """
    运行 Rig Integration Test。

    Args:
        keep_result(bool):
            True 时保留测试通过后的绑定结果，并自动选择 Controller。
    """
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

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRigIntegrationTest"
    )

    try:
        test_result = test_rig_integration(
            token,
            keep_result=keep_result
        )
        passed_count = 1

        print(
            u"[PASS] Rig | Joint -> Controller -> OPM -> Joint | {}".format(
                test_result["message"]
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
        # 默认自动化测试继续保持完全清理。
        # 观察模式明确要求保留，因此成功或失败都不自动删除，方便检查现场。
        if not keep_result:
            delete_test_nodes(token)

        cmds.undoInfo(
            closeChunk=True
        )

    # -------------------------------------------------------------------------
    # 标准模式：最终确认没有测试节点残留。
    # -------------------------------------------------------------------------
    if not keep_result:
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

    # -------------------------------------------------------------------------
    # 观察模式：打印保留节点，方便在 Outliner / Node Editor 中查找。
    # -------------------------------------------------------------------------
    if keep_result:
        print("-" * 78)
        print(u"[KEEP] Test Token : {}".format(token))

        if test_result is not None:
            print(u"[KEEP] Rig Root   : {}".format(test_result["rig_root"]))
            print(u"[KEEP] Controller : {}".format(test_result["control"]))
            print(u"[KEEP] Joint      : {}".format(test_result["joint"]))
            print(u"[KEEP] multMatrix : {}".format(test_result["matrix_node"]))
            print(u"[KEEP] Controller 已自动选中，可以直接移动观察 Joint 跟随。")
        else:
            print(u"[KEEP] 测试发生异常，保留当前 Token 节点用于排查。")

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
        "token": token,
        "kept": bool(keep_result),
        "result": test_result,
    }


__all__ = [
    "run",
]
