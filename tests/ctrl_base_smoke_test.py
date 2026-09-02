# coding=utf-8
u"""
CtrlBase Smoke Test
===================

验证 systems.ctrl_base 的标准 Controller 创建和 Follow。
测试结束后删除临时节点。
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..systems import ctrl_base


# =============================================================================
# Helpers
# =============================================================================

def create_token():
    u"""创建短测试 Token。"""
    return uuid.uuid4().hex[:8]


def delete_test_nodes(token):
    u"""删除本轮测试产生的 DAG / DG 节点。"""
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


def almost_equal(value_a, value_b, tolerance=0.0001):
    u"""浮点比较。"""
    return abs(value_a - value_b) <= tolerance


# =============================================================================
# Test
# =============================================================================

def test_follow(token):
    u"""测试 CtrlBase Follow 0 / 1。"""
    driver = cmds.createNode(
        "transform",
        name="grp_md_{}_driver_001".format(token)
    )
    target = cmds.createNode(
        "transform",
        name="grp_md_{}_target_001".format(token)
    )

    ctrl_result = ctrl_base.create_ctrl(
        name="ctrl_md_{}_follow_001".format(token),
        shape="circle",
        radius=1.0,
        axis="Y+",
        target_node=target,
        color=17,
        create_sub_ctrl=False,
        add_to_set=False
    )

    ctrl_node = ctrl_result["ctrl_node"]

    follow_result = ctrl_base.create_follow(
        driver_node=driver,
        ctrl_dict=ctrl_result,
        weight=1.0,
        attr_name="follow",
        maintain_offset=True
    )

    constraint_node = follow_result["constraint_node"]
    reverse_node = follow_result["reverse_node"]
    follow_plug = follow_result["follow_plug"]

    if not cmds.objExists(constraint_node):
        raise RuntimeError(
            u"Follow Constraint 没有创建。"
        )

    if not cmds.objExists(reverse_node):
        raise RuntimeError(
            u"Follow Reverse 节点没有创建。"
        )

    if not cmds.objExists(follow_plug):
        raise RuntimeError(
            u"Follow 属性没有创建。"
        )

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
        ctrl_node,
        query=True,
        worldSpace=True,
        translation=True
    )

    if not almost_equal(
            follow_position[0],
            3.0
    ):
        raise RuntimeError(
            u"Follow=1 时 Ctrl 没有跟随 Driver：{}".format(
                follow_position
            )
        )

    cmds.setAttr(
        follow_plug,
        0.0
    )

    no_follow_position = cmds.xform(
        ctrl_node,
        query=True,
        worldSpace=True,
        translation=True
    )

    if not almost_equal(
            no_follow_position[0],
            0.0
    ):
        raise RuntimeError(
            u"Follow=0 时 Ctrl 没有回到 Zero Space：{}".format(
                no_follow_position
            )
        )

    return u"CtrlBase Create + Follow 0/1 成功"


# =============================================================================
# Runner
# =============================================================================

def run():
    u"""运行 CtrlBase Smoke Test。"""
    token = create_token()
    passed_count = 0
    failed_count = 0
    error_text = ""

    print("")
    print("=" * 78)
    print("Muzi Toolset - CtrlBase Smoke Test")
    print("=" * 78)

    try:
        message = test_follow(
            token
        )
        passed_count = 1

        print(
            u"[PASS] CtrlBase | Follow | {}".format(
                message
            )
        )
    except Exception as error:
        failed_count = 1
        error_text = traceback.format_exc()

        print(
            u"[FAIL] CtrlBase | Follow | {}".format(
                error
            )
        )
        print(
            error_text
        )
    finally:
        delete_test_nodes(
            token
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
