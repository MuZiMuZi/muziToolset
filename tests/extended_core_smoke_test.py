# coding=utf-8
u"""
Extended Core / RigBase Smoke Test
==================================

Maya 真机验证第二层基础能力：
    - attr_utils
    - hierarchy_utils
    - joint_utils / joint_chain_utils
    - systems.rig_base.RigBase + core.rename_utils
    - model_check_utils
    - scene_utils

架构约定：
    - Rig Naming 统一使用 type / side / part / function / index；
    - 多 Joint / Joint Chain 统一使用 core.joint_chain_utils；
    - Core rename_utils 只负责 Maya Rename / Short Name / 外部名称 Token；
    - Smoke Test 不保留退休 API 的兼容调用。
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..core import attr_utils
from ..core import hierarchy_utils
from ..core import joint_chain_utils
from ..core import joint_utils
from ..core import model_check_utils
from ..core import rename_utils
from ..core import scene_utils
from ..systems.rig_base import RigBase


# =============================================================================
# Common
# =============================================================================

def create_token():
    u"""创建短测试 Token。"""
    return uuid.uuid4().hex[:8]


def create_name(token, description):
    u"""生成临时测试节点名称。"""
    return "__muzi_extended_test_{}_{}".format(
        token,
        description
    )


def create_test_root(token):
    u"""创建本轮测试 Root。"""
    return cmds.createNode(
        "transform",
        name=create_name(token, "root")
    )


def parent_under_test_root(node, test_root):
    u"""把节点放到测试 Root 下。"""
    if not node:
        return node

    if not cmds.objExists(node):
        return node

    result = cmds.parent(
        node,
        test_root,
        absolute=True
    )

    if result:
        return result[0]

    return node


def assert_close(
        actual,
        expected,
        tolerance=0.0001,
        label=u"数值"
):
    u"""浮点断言。"""
    if abs(actual - expected) > tolerance:
        raise RuntimeError(
            u"{}错误：actual={} expected={}".format(
                label,
                actual,
                expected
            )
        )


def assert_vector_close(
        actual,
        expected,
        tolerance=0.0001,
        label=u"向量"
):
    u"""向量断言。"""
    if len(actual) != len(expected):
        raise RuntimeError(
            u"{}长度错误。".format(
                label
            )
        )

    index = 0

    while index < len(expected):
        assert_close(
            actual[index],
            expected[index],
            tolerance=tolerance,
            label=u"{}[{}]".format(
                label,
                index
            )
        )
        index += 1


def cleanup_test_nodes(token, test_root):
    u"""删除本轮所有测试节点。"""
    if test_root:
        if cmds.objExists(test_root):
            try:
                cmds.delete(
                    test_root
                )
            except Exception:
                pass

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


def create_result(category, name, passed, message, traceback_text=""):
    u"""创建测试结果。"""
    return {
        "category": category,
        "name": name,
        "passed": passed,
        "message": message,
        "traceback": traceback_text,
    }


def run_case(
        results,
        token,
        test_root,
        category,
        name,
        test_function
):
    u"""执行一个测试 Case。"""
    try:
        message = test_function(
            token,
            test_root
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


# =============================================================================
# Attr Utils
# =============================================================================

def test_attr_utils(token, test_root):
    u"""验证 Attribute Value / String / Message。"""
    node = cmds.createNode(
        "transform",
        name=create_name(token, "attr_node"),
        parent=test_root
    )
    target = cmds.createNode(
        "transform",
        name=create_name(token, "attr_target"),
        parent=test_root
    )

    node_attr = attr_utils.Attr(
        node
    )
    node_attr.add_attr(
        "weight",
        attr_type="double",
        lock=False,
        hide=False,
        default_value=0.25,
        min_value=0.0,
        max_value=1.0
    )
    cmds.setAttr(
        node + ".weight",
        0.75
    )

    assert_close(
        cmds.getAttr(node + ".weight"),
        0.75,
        label=u"Attr Double"
    )

    node_attr.add_attr(
        "label",
        attr_type="string",
        lock=False,
        hide=True,
        default_value="face"
    )

    if cmds.getAttr(node + ".label") != "face":
        raise RuntimeError(
            u"String Attribute 保存失败。"
        )

    node_attr.connect_message(
        target,
        attr="targetMessage",
        force=True
    )
    message_node = node_attr.get_message(
        "targetMessage"
    )

    if not message_node:
        raise RuntimeError(
            u"Message Attribute 连接失败。"
        )

    return u"Double + String + Message Attribute 成功"


# =============================================================================
# Hierarchy Utils
# =============================================================================

def test_hierarchy_utils(token, test_root):
    u"""验证 Parent / Ensure Group / World Transform 保持。"""
    hierarchy_root = cmds.createNode(
        "transform",
        name=create_name(token, "hierarchy_root"),
        parent=test_root
    )
    target = cmds.createNode(
        "transform",
        name=create_name(token, "hierarchy_target"),
        parent=test_root
    )

    cmds.xform(
        target,
        worldSpace=True,
        translation=[2.0, 3.0, 4.0]
    )
    before_translation = cmds.xform(
        target,
        query=True,
        worldSpace=True,
        translation=True
    )

    target = hierarchy_utils.parent(
        target,
        hierarchy_root
    )
    after_translation = cmds.xform(
        target,
        query=True,
        worldSpace=True,
        translation=True
    )

    assert_vector_close(
        after_translation,
        before_translation,
        label=u"Hierarchy World Translation"
    )

    ensured_name = create_name(
        token,
        "ensure_group"
    )
    ensured_group = hierarchy_utils.ensure_group(
        ensured_name,
        parent_node=hierarchy_root
    )
    ensured_parent = hierarchy_utils.get_parent(
        ensured_group,
        full_path=True
    )

    if not ensured_parent:
        raise RuntimeError(
            u"ensure_group 没有建立 Parent。"
        )

    return u"Parent + Ensure Group + World Transform 保持成功"


# =============================================================================
# Joint Utils / Joint Chain Utils
# =============================================================================

def test_joint_utils(token, test_root):
    u"""验证 Joint Create / Chain / Radius / Label。"""
    root_joint = joint_utils.Joint.create(
        name=create_name(token, "joint_root"),
        position=[0.0, 5.0, 0.0],
        parent=test_root,
        radius=1.5
    )
    child_joint = joint_utils.Joint.create(
        name=create_name(token, "joint_child"),
        position=[3.0, 5.0, 0.0],
        parent=test_root
    )

    chain = joint_chain_utils.parent_joints_as_chain(
        [
            root_joint,
            child_joint,
        ]
    )

    if len(chain) != 2:
        raise RuntimeError(
            u"Joint Chain 返回数量错误。"
        )

    assert_close(
        cmds.getAttr(root_joint + ".radius"),
        1.5,
        label=u"Joint Radius"
    )

    tagged_name = RigBase(
        type="jnt",
        side="lf",
        part=token.lower(),
        function="bind",
        index=1
    ).name
    tagged_joint = joint_utils.Joint.create(
        name=tagged_name,
        position=[0.0, 0.0, 0.0],
        parent=test_root
    )
    tag_data = joint_utils.Joint(
        tagged_joint
    ).tag()

    if tag_data["side"] != 1:
        raise RuntimeError(
            u"Joint Label Side 错误：{}".format(
                tag_data
            )
        )

    if tag_data["type"] != 18:
        raise RuntimeError(
            u"Joint Label Type 错误：{}".format(
                tag_data
            )
        )

    return u"Create + Joint Chain + Radius + Joint Label 成功"


# =============================================================================
# RigBase / Rename Utils
# =============================================================================

def test_naming_utils(token, test_root):
    u"""验证当前 RigBase Naming Object + Maya Rename。"""
    rig_object = RigBase(
        type="jnt",
        side="lf",
        part="upper_arm",
        function="bind",
        index=1
    )
    standard_name = rig_object.name

    if standard_name != "jnt_lf_upper_arm_bind_001":
        raise RuntimeError(
            u"RigBase 标准名称生成错误：{}".format(
                standard_name
            )
        )

    parsed = RigBase.parse_name(
        standard_name
    )

    if parsed["part"] != "upper_arm":
        raise RuntimeError(
            u"RigBase Part Parse 错误：{}".format(
                parsed
            )
        )

    if parsed["type"] != "jnt":
        raise RuntimeError(
            u"RigBase Type Parse 错误：{}".format(
                parsed
            )
        )

    mirror_name = rig_object.mirror_name()

    if mirror_name != "jnt_rt_upper_arm_bind_001":
        raise RuntimeError(
            u"RigBase Mirror Name 错误：{}".format(
                mirror_name
            )
        )

    if rig_object.side != "lf":
        raise RuntimeError(
            u"mirror_name() 不应该修改 RigBase.side。"
        )

    source = cmds.createNode(
        "transform",
        name=create_name(token, "rename_source"),
        parent=test_root
    )
    renamed_name = create_name(
        token,
        "rename_result"
    )
    renamed = rename_utils.rename_node(
        source,
        renamed_name
    )

    if renamed is None:
        raise RuntimeError(
            u"rename_utils.rename_node 返回 None。"
        )

    if not cmds.objExists(renamed_name):
        raise RuntimeError(
            u"Maya 节点没有完成 Rename。"
        )

    return u"RigBase Create / Parse / Mirror + Maya Rename 成功"


# =============================================================================
# Model Check Utils
# =============================================================================

def test_model_check_utils(token, test_root):
    u"""验证未冻结 Mesh Issue。"""
    cube_result = cmds.polyCube(
        name=create_name(token, "model_cube"),
        constructionHistory=True
    )
    cube = parent_under_test_root(
        cube_result[0],
        test_root
    )
    cmds.setAttr(
        cube + ".translateX",
        4.0
    )

    issues = model_check_utils.check_transformations(
        meshes=[cube]
    )

    if not issues:
        raise RuntimeError(
            u"没有发现未冻结 Mesh Transform。"
        )

    required_keys = [
        "node",
        "type",
        "details",
        "fixable",
    ]

    for key in required_keys:
        if key not in issues[0]:
            raise RuntimeError(
                u"Model Check Issue 缺少字段：{}".format(
                    key
                )
            )

    return u"Mesh Transform Issue Schema 成功"


# =============================================================================
# Scene Clean Utils
# =============================================================================

def test_scene_utils(token, test_root):
    u"""验证安全 Freeze 和递归 Empty Group 清理。"""
    cube_result = cmds.polyCube(
        name=create_name(token, "clean_cube"),
        constructionHistory=False
    )
    cube = parent_under_test_root(
        cube_result[0],
        test_root
    )
    cmds.setAttr(
        cube + ".translateX",
        3.0
    )

    frozen_count, skipped_count = scene_utils.freeze_transformations(
        [cube]
    )

    if frozen_count != 1:
        raise RuntimeError(
            u"Freeze 数量错误：{}".format(
                frozen_count
            )
        )

    if skipped_count != 0:
        raise RuntimeError(
            u"普通 Cube 被错误 Skip。"
        )

    empty_parent = cmds.createNode(
        "transform",
        name=create_name(token, "empty_parent"),
        parent=test_root
    )
    empty_child = cmds.createNode(
        "transform",
        name=create_name(token, "empty_child"),
        parent=empty_parent
    )

    deleted_count = scene_utils.delete_empty_groups(
        [empty_child]
    )

    if deleted_count < 2:
        raise RuntimeError(
            u"递归 Empty Group 删除数量错误：{}".format(
                deleted_count
            )
        )

    return u"Safe Freeze + Recursive Empty Group Clean 成功"


# =============================================================================
# Report / Runner
# =============================================================================

def print_report(results):
    u"""打印报告并返回汇总。"""
    print("")
    print("=" * 78)
    print("Muzi Toolset - Extended Core / RigBase Smoke Test")
    print("=" * 78)

    passed_count = 0

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(
            "[{}] {} | {} | {}".format(
                status,
                result["category"],
                result["name"],
                result["message"]
            )
        )

        if result["passed"]:
            passed_count += 1
        else:
            if result["traceback"]:
                print(
                    result["traceback"]
                )

    failed_count = len(results) - passed_count

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
        "total": len(results),
        "passed": passed_count,
        "failed": failed_count,
    }


def run():
    u"""执行全部 Extended Core / RigBase Case。"""
    token = create_token()
    results = []
    test_root = None

    test_cases = [
        ("attr_utils", "Attribute / Config", test_attr_utils),
        ("hierarchy_utils", "DAG / Ensure / Parent", test_hierarchy_utils),
        ("joint_utils", "Joint / Chain / Label", test_joint_utils),
        ("rig_base", "Rig Naming / Maya Rename", test_naming_utils),
        ("model_check_utils", "Model Quality Check", test_model_check_utils),
        ("scene_utils", "Safe Scene Clean", test_scene_utils),
    ]

    try:
        test_root = create_test_root(
            token
        )

        for test_case in test_cases:
            run_case(
                results,
                token,
                test_root,
                test_case[0],
                test_case[1],
                test_case[2]
            )
    finally:
        cleanup_test_nodes(
            token,
            test_root
        )

    return print_report(
        results
    )


if __name__ == "__main__":
    run()
