# coding=utf-8
u"""
Controller Component Smoke Test
===============================

验证 Controller System 中从旧 pipelineUtils 提取的 Parent Space Blend。

测试会创建带 __muzi_controller_test_ 前缀的临时节点，结束后自动删除。
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..systems import controller as controller_system


# =============================================================================
# Helpers
# =============================================================================

def create_token():
    """创建短测试 Token。"""
    return uuid.uuid4().hex[:8]


def create_name(token, description):
    """创建测试节点名称。"""
    return "__muzi_controller_test_{}_{}".format(
        token,
        description
    )


def delete_test_nodes(token):
    """删除本轮测试产生的 DAG / DG 节点。"""
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


def almost_equal(value_a, value_b, tolerance=0.0001):
    """浮点比较。"""
    return abs(value_a - value_b) <= tolerance


# =============================================================================
# Test
# =============================================================================

def test_parent_space_blend(token):
    """测试 Follow 0 / 1 的 Parent Space Blend。"""
    driver = cmds.createNode(
        "transform",
        name=create_name(token, "driver")
    )

    target = cmds.createNode(
        "transform",
        name=create_name(token, "target")
    )

    control_result = controller_system.create_controller(
        name="ctrl_{}_follow_001".format(
            create_name(token, "control")
        ),
        shape="circle",
        radius=1.0,
        axis="Y+",
        target=target,
        color=17,
        create_sub_control=False,
        create_extra_groups=True,
        add_to_set=False
    )

    control = control_result["control"]

    blend_result = controller_system.create_parent_space_blend(
        driver=driver,
        control=control,
        weight=1.0,
        attribute_name="follow",
        maintain_offset=True
    )

    constraint = blend_result["constraint"]
    reverse_node = blend_result["reverse"]
    follow_plug = blend_result["follow_plug"]

    if not cmds.objExists(constraint):
        raise RuntimeError(u"Parent Space Constraint 没有创建。")

    if not cmds.objExists(reverse_node):
        raise RuntimeError(u"Follow Reverse 节点没有创建。")

    if not cmds.objExists(follow_plug):
        raise RuntimeError(u"Follow 属性没有创建。")

    # -------------------------------------------------------------------------
    # Follow = 1
    # -------------------------------------------------------------------------
    cmds.setAttr(
        follow_plug,
        1.0
    )

    cmds.xform(
        driver,
        worldSpace=True,
        translation=[3.0, 0.0, 0.0]
    )

    follow_position = cmds.xform(
        control,
        query=True,
        worldSpace=True,
        translation=True
    )

    if not almost_equal(
            follow_position[0],
            3.0
    ):
        raise RuntimeError(
            u"Follow=1 时控制器没有跟随 Driver：{}".format(
                follow_position
            )
        )

    # -------------------------------------------------------------------------
    # Follow = 0
    # -------------------------------------------------------------------------
    cmds.setAttr(
        follow_plug,
        0.0
    )

    no_follow_position = cmds.xform(
        control,
        query=True,
        worldSpace=True,
        translation=True
    )

    if not almost_equal(
            no_follow_position[0],
            0.0
    ):
        raise RuntimeError(
            u"Follow=0 时没有回到 Zero Space：{}".format(
                no_follow_position
            )
        )

    return u"Controller Parent Space Blend Follow 0/1 成功"


# =============================================================================
# Runner
# =============================================================================

def run():
    """运行 Controller Component Smoke Test。"""
    token = create_token()
    passed_count = 0
    failed_count = 0
    error_text = ""

    print("")
    print("=" * 78)
    print("Muzi Toolset - Controller Component Smoke Test")
    print("=" * 78)

    try:
        message = test_parent_space_blend(token)
        passed_count = 1

        print(
            u"[PASS] Controller | Parent Space Blend | {}".format(
                message
            )
        )
    except Exception as error:
        failed_count = 1
        error_text = traceback.format_exc()

        print(
            u"[FAIL] Controller | Parent Space Blend | {}".format(
                error
            )
        )
        print(error_text)
    finally:
        delete_test_nodes(token)

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
