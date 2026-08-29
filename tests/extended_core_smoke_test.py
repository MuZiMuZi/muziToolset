# coding=utf-8
u"""
Extended Core Smoke Test
========================

MuziTools Core 第二层 Maya 真机验证。

模块职责
--------
本测试专门验证这次重新整理并统一为 snake_case 的 Core 领域：

attr_utils
    Attribute Value、String Config、Message Config。

hierarchy_utils
    DAG Parent、Extra Group、World Transform 保持。

joint_utils
    Joint Create、Joint Chain、Radius、Maya Joint Label。

name_utils / rename_utils
    五段式标准名称、Side Alias、Parse、Mirror、Maya Rename。

model_check_utils
    Mesh Transform Issue 检查和统一 Issue Schema。

scene_clean_utils
    安全 Freeze Transform 和递归 Empty Group 清理。

和 Pipeline Smoke 的区别
------------------------
``pipeline_refactor_smoke_test.py`` 验证 Scene / Transform / Matrix / Connection / Constraint /
Curve / Surface 等基础 Core。

本文件验证更接近真实资产工作流的 Attribute / DAG / Joint / Naming / Scene Quality 能力。
两个测试分开后，失败时可以快速判断问题属于“基础节点网络”还是“高层场景行为”。

安全原则
--------
1. 所有临时 DAG 都挂在本轮唯一测试 Root 下，结束时删除 Root 即可完整清理；
2. 测试结束后还会按 Token 做一次兜底扫描；
3. 不打开、不保存、不新建用户 Scene；
4. 不修改用户 Selection；
5. 不操作用户节点；
6. 不依赖 PyMel；
7. 单项失败不会阻止后续 Case 执行；
8. 清理动作放在 finally 中，无论成功失败都会执行。

运行方式
--------
Maya Python Script Editor：

    import muziToolset

    report = muziToolset.extended_core_smoke_test()

成功标准
--------

    Total: 6 | Passed: 6 | Failed: 0

兼容
----
Maya 2023+ / Python 3 / maya.cmds
"""

from __future__ import print_function

import traceback
import uuid

import maya.cmds as cmds

from ..core import attr_utils
from ..core import hierarchy_utils
from ..core import joint_utils
from ..core import model_check_utils
from ..core import name_utils
from ..core import rename_utils
from ..core import scene_clean_utils


# =============================================================================
# Common Helpers
# =============================================================================

def create_token():
    """创建短 Token，保证不同测试轮次之间不会重名。"""
    return uuid.uuid4().hex[:8]


def create_name(token, description):
    """生成带统一测试前缀的临时节点名称。"""
    return "__muzi_extended_test_{}_{}".format(
        token,
        description
    )


def create_test_root(token):
    """
    创建本轮测试 Root。

    为什么需要 Root：
        Naming / Joint Label 等 Case 需要创建符合正式命名规则的节点，这些节点名称不一定能使用
        ``__muzi_extended_test_`` 作为开头。把它们全部 Parent 到测试 Root 后，只要最终删除 Root，
        就能保证这些标准命名节点也一起被清理。
    """
    return cmds.createNode(
        "transform",
        name=create_name(token, "root")
    )


def parent_under_test_root(node, test_root):
    """把 DAG 节点放到测试 Root 下，并返回 Maya 最新路径。"""
    if not node or not cmds.objExists(node):
        return node

    result = cmds.parent(
        node,
        test_root,
        absolute=True
    )

    if result:
        return result[0]

    return node


def assert_close(actual, expected, tolerance=0.0001, label=u"数值"):
    """验证两个数值在允许误差内一致。"""
    if abs(actual - expected) > tolerance:
        raise RuntimeError(
            u"{}错误：actual={} expected={}".format(
                label,
                actual,
                expected
            )
        )


def assert_vector_close(actual, expected, tolerance=0.0001, label=u"向量"):
    """逐项验证三维向量。"""
    if len(actual) != len(expected):
        raise RuntimeError(
            u"{}长度错误：actual={} expected={}".format(
                label,
                actual,
                expected
            )
        )

    index = 0

    while index < len(expected):
        assert_close(
            actual[index],
            expected[index],
            tolerance=tolerance,
            label=u"{}[{}]".format(label, index)
        )
        index += 1


def cleanup_test_nodes(token, test_root):
    """
    清理本轮测试产生的所有节点。

    清理分两层：
        1. 先删除 Test Root，它会连同所有标准命名 Child 一起删除；
        2. 再按 Token 扫描一次，清理由异常中断产生且尚未 Parent 到 Root 的节点。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：优先删除 Root。
    # -------------------------------------------------------------------------
    if test_root and cmds.objExists(test_root):
        try:
            cmds.delete(test_root)
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # 步骤 2：Token 兜底扫描，并按 Child First 顺序删除。
    # -------------------------------------------------------------------------
    pattern = "*{}*".format(token)
    nodes = cmds.ls(
        pattern,
        long=True
    ) or []

    nodes_with_depth = []

    for node in nodes:
        node_data = {
            "node": node,
            "depth": node.count("|"),
        }
        nodes_with_depth.append(node_data)

    def get_depth(node_data):
        return node_data["depth"]

    nodes_with_depth.sort(
        key=get_depth,
        reverse=True
    )

    for node_data in nodes_with_depth:
        node = node_data["node"]

        if not cmds.objExists(node):
            continue

        try:
            cmds.delete(node)
        except Exception:
            pass


def record_result(
        results,
        category,
        name,
        passed,
        message,
        error_text=""
):
    """向结果列表追加统一字典。"""
    result = {
        "category": category,
        "name": name,
        "passed": passed,
        "message": message,
        "traceback": error_text,
    }

    results.append(result)
    return result


def run_case(
        results,
        token,
        test_root,
        category,
        name,
        test_function
):
    """执行单项 Case，并把异常转换为统一失败记录。"""
    try:
        message = test_function(
            token,
            test_root
        )

        record_result(
            results,
            category,
            name,
            True,
            message
        )
    except Exception as error:
        record_result(
            results,
            category,
            name,
            False,
            str(error),
            traceback.format_exc()
        )


# =============================================================================
# Attr Utils
# =============================================================================

def test_attr_utils(token, test_root):
    """验证普通属性、String Config 和 Message Config。"""
    config_node = cmds.createNode(
        "transform",
        name=create_name(token, "attr_config"),
        parent=test_root
    )
    source_node = cmds.createNode(
        "transform",
        name=create_name(token, "attr_source"),
        parent=test_root
    )

    attr = attr_utils.Attr(config_node)

    # -------------------------------------------------------------------------
    # 步骤 1：创建并读取普通 Double 属性。
    # -------------------------------------------------------------------------
    value_plug = attr.set_attr_value(
        attr="test_value",
        value=3.5,
        attr_type="double",
        lock=False,
        hide=False
    )

    if not value_plug or not cmds.objExists(value_plug):
        raise RuntimeError(u"普通属性创建失败。")

    assert_close(
        attr.get_attr_value("test_value"),
        3.5,
        label=u"Attribute Value"
    )

    # -------------------------------------------------------------------------
    # 步骤 2：把 Python 基础数据写入 String Config，再恢复原数据。
    # -------------------------------------------------------------------------
    config_data = {
        "mode": "extended_smoke",
        "count": 3,
    }

    attr.add_string_info(
        config_data,
        attr="test_config",
        lock=True,
        hide=True
    )

    restored_data = attr.get_string_info("test_config")

    if restored_data != config_data:
        raise RuntimeError(
            u"String Config 恢复错误：{}".format(restored_data)
        )

    # -------------------------------------------------------------------------
    # 步骤 3：Message 保存节点引用。
    # -------------------------------------------------------------------------
    connected = attr.connect_message(
        source_node=source_node,
        attr="source_node",
        force=True
    )

    if not connected:
        raise RuntimeError(u"Message 连接失败。")

    message_node = attr.get_message(
        attr="source_node",
        plugs=False
    )

    if message_node is None:
        raise RuntimeError(u"Message 查询没有返回来源节点。")

    if message_node.split("|")[-1] != source_node.split("|")[-1]:
        raise RuntimeError(
            u"Message 来源错误：{}".format(message_node)
        )

    return u"Value + String Config + Message Config 成功"


# =============================================================================
# Hierarchy Utils
# =============================================================================

def test_hierarchy_utils(token, test_root):
    """验证 Extra Group 插入后 DAG 关系和对象世界姿态保持。"""
    hierarchy_root = cmds.createNode(
        "transform",
        name=create_name(token, "hierarchy_parent"),
        parent=test_root
    )
    target = cmds.createNode(
        "transform",
        name=create_name(token, "hierarchy_target"),
        parent=hierarchy_root
    )

    cmds.xform(
        hierarchy_root,
        worldSpace=True,
        translation=[10.0, 0.0, 0.0]
    )
    cmds.xform(
        target,
        worldSpace=True,
        translation=[12.0, 3.0, -2.0]
    )
    cmds.xform(
        target,
        worldSpace=True,
        rotation=[15.0, 25.0, 5.0]
    )

    before_translation = cmds.xform(
        target,
        query=True,
        worldSpace=True,
        translation=True
    )
    before_rotation = cmds.xform(
        target,
        query=True,
        worldSpace=True,
        rotation=True
    )

    # -------------------------------------------------------------------------
    # 步骤 1：插入 Extra Group。
    # -------------------------------------------------------------------------
    extra_group = hierarchy_utils.Hierarchy.add_extra_group(
        target,
        create_name(token, "hierarchy_zero"),
        world_orient=False
    )

    if not cmds.objExists(extra_group):
        raise RuntimeError(u"Extra Group 没有创建。")

    # -------------------------------------------------------------------------
    # 步骤 2：重新解析 Target Long Path，确认 Parent 已经是 Extra Group。
    # -------------------------------------------------------------------------
    target_matches = cmds.ls(
        target.split("|")[-1],
        long=True
    ) or []

    if not target_matches:
        raise RuntimeError(u"插组后找不到 Target。")

    target_long = target_matches[0]
    parents = cmds.listRelatives(
        target_long,
        parent=True,
        fullPath=True
    ) or []

    if not parents:
        raise RuntimeError(u"插组后 Target 没有 Parent。")

    extra_matches = cmds.ls(
        extra_group,
        long=True
    ) or []
    extra_long = extra_matches[0] if extra_matches else extra_group

    if parents[0] != extra_long:
        raise RuntimeError(
            u"Target Parent 错误：{}".format(parents[0])
        )

    # -------------------------------------------------------------------------
    # 步骤 3：验证世界姿态没有因插组跳动。
    # -------------------------------------------------------------------------
    after_translation = cmds.xform(
        target_long,
        query=True,
        worldSpace=True,
        translation=True
    )
    after_rotation = cmds.xform(
        target_long,
        query=True,
        worldSpace=True,
        rotation=True
    )

    assert_vector_close(
        after_translation,
        before_translation,
        label=u"Hierarchy World Translation"
    )
    assert_vector_close(
        after_rotation,
        before_rotation,
        tolerance=0.001,
        label=u"Hierarchy World Rotation"
    )

    return u"Extra Group + Parent + World Transform 保持成功"


# =============================================================================
# Joint Utils
# =============================================================================

def test_joint_utils(token, test_root):
    """验证 Joint Create、Chain、Radius 和正式 Maya Joint Label。"""
    root_name = create_name(token, "joint_root")
    child_name = create_name(token, "joint_child")

    root_joint = joint_utils.Joint.create(
        name=root_name,
        position=[0.0, 5.0, 0.0],
        parent=test_root,
        radius=1.5
    )
    child_joint = joint_utils.Joint.create(
        name=child_name,
        position=[3.0, 5.0, 0.0],
        parent=test_root
    )

    # -------------------------------------------------------------------------
    # 步骤 1：把两个 Joint 组成 Chain。
    # -------------------------------------------------------------------------
    chain = joint_utils.JointChain.parent_joints_as_chain(
        [root_joint, child_joint]
    )

    if len(chain) != 2:
        raise RuntimeError(u"Joint Chain 返回数量错误。")

    child_matches = cmds.ls(
        child_name,
        long=True
    ) or []

    if not child_matches:
        raise RuntimeError(u"Joint Parent 后找不到 Child。")

    child_long = child_matches[0]
    parents = cmds.listRelatives(
        child_long,
        parent=True,
        type="joint",
        fullPath=True
    ) or []

    if not parents:
        raise RuntimeError(u"Joint Chain 没有建立 Joint Parent。")

    if parents[0].split("|")[-1] != root_name:
        raise RuntimeError(
            u"Joint Chain Parent 错误：{}".format(parents[0])
        )

    assert_close(
        cmds.getAttr(root_joint + ".radius"),
        1.5,
        label=u"Joint Radius"
    )

    # -------------------------------------------------------------------------
    # 步骤 2：创建符合五段式规则的 Joint，并把它挂到 Test Root 下。
    #
    # 这样既能测试 Joint.tag()，又能确保 finally 删除 Test Root 时不会留下标准命名 Joint。
    # -------------------------------------------------------------------------
    tagged_name = "jnt_lf_{}_bind_001".format(
        token.lower()
    )
    tagged_joint = joint_utils.Joint.create(
        name=tagged_name,
        position=[0.0, 0.0, 0.0],
        parent=test_root
    )

    tag_data = joint_utils.Joint(tagged_joint).tag()

    if tag_data["side"] != 1:
        raise RuntimeError(
            u"Joint Label Side 错误：{}".format(tag_data)
        )

    if tag_data["type"] != 18:
        raise RuntimeError(
            u"Joint Label Type 错误：{}".format(tag_data)
        )

    expected_other_type = "{}_bind".format(token.lower())

    if tag_data["otherType"] != expected_other_type:
        raise RuntimeError(
            u"Joint otherType 错误：{}".format(tag_data)
        )

    return u"Create + Chain + Radius + Joint Label 成功"


# =============================================================================
# Naming / Rename Utils
# =============================================================================

def test_naming_utils(token, test_root):
    """验证五段式名称、Side Alias、Parse、Mirror Name 和 Maya Rename。"""
    # -------------------------------------------------------------------------
    # 步骤 1：left Alias 必须统一成 lf。
    # -------------------------------------------------------------------------
    standard_name = name_utils.Name.create_name(
        node_type="jnt",
        side="left",
        part="arm",
        function="bind",
        index=1
    )

    if standard_name != "jnt_lf_arm_bind_001":
        raise RuntimeError(
            u"标准名称生成错误：{}".format(standard_name)
        )

    # -------------------------------------------------------------------------
    # 步骤 2：Parse 必须完整恢复字段。
    # -------------------------------------------------------------------------
    parsed = name_utils.Name.parse_name(standard_name)
    expected_values = {
        "type": "jnt",
        "side": "lf",
        "part": "arm",
        "function": "bind",
        "index": 1,
    }

    for key in expected_values:
        if parsed.get(key) != expected_values[key]:
            raise RuntimeError(
                u"Name Parse {} 错误：{}".format(
                    key,
                    parsed
                )
            )

    # -------------------------------------------------------------------------
    # 步骤 3：Mirror Name 只翻转 lf / rt。
    # -------------------------------------------------------------------------
    mirror_name = name_utils.Name.mirror_name(standard_name)

    if mirror_name != "jnt_rt_arm_bind_001":
        raise RuntimeError(
            u"Mirror Name 错误：{}".format(mirror_name)
        )

    # -------------------------------------------------------------------------
    # 步骤 4：rename_utils 必须真正 Rename Maya DAG 节点。
    # -------------------------------------------------------------------------
    source = cmds.createNode(
        "transform",
        name=create_name(token, "rename_source"),
        parent=test_root
    )
    renamed_name = create_name(token, "rename_result")

    renamed = rename_utils.rename_node(
        source,
        renamed_name
    )

    if renamed is None:
        raise RuntimeError(u"rename_utils.rename_node 返回 None。")

    if not cmds.objExists(renamed_name):
        raise RuntimeError(u"Maya 节点没有完成 Rename。")

    return u"Create Name + Parse + Mirror + Maya Rename 成功"


# =============================================================================
# Model Check Utils
# =============================================================================

def test_model_check_utils(token, test_root):
    """验证 Model Check 能发现一个明确的未冻结 Mesh。"""
    # -------------------------------------------------------------------------
    # 步骤 1：创建普通 Cube，并放进 Test Root。
    # -------------------------------------------------------------------------
    cube_result = cmds.polyCube(
        name=create_name(token, "model_cube"),
        constructionHistory=True
    )
    cube = parent_under_test_root(
        cube_result[0],
        test_root
    )

    cmds.setAttr(cube + ".translateX", 4.0)
    cmds.setAttr(cube + ".rotateY", 15.0)
    cmds.setAttr(cube + ".scaleZ", 1.5)

    # -------------------------------------------------------------------------
    # 步骤 2：Transform Check 应返回统一 Issue。
    # -------------------------------------------------------------------------
    issues = model_check_utils.check_transformations(
        meshes=[cube]
    )

    if not issues:
        raise RuntimeError(u"没有发现明确的未冻结 Mesh Transform。")

    issue = issues[0]
    required_keys = [
        "node",
        "type",
        "details",
        "fixable",
    ]

    for key in required_keys:
        if key not in issue:
            raise RuntimeError(
                u"Model Check Issue 缺少字段：{}".format(key)
            )

    if issue["type"] != u"Mesh Transform 未冻结":
        raise RuntimeError(
            u"Model Check Issue Type 错误：{}".format(issue)
        )

    if not issue["fixable"]:
        raise RuntimeError(
            u"无 Deformer 的普通 Cube 应允许安全 Freeze：{}".format(issue)
        )

    return u"Mesh Transform Issue + Issue Schema 成功"


# =============================================================================
# Scene Clean Utils
# =============================================================================

def test_scene_clean_utils(token, test_root):
    """验证安全 Freeze Transform 和递归 Empty Group 清理。"""
    # -------------------------------------------------------------------------
    # 步骤 1：创建没有 Animation / Constraint / Deformer 的普通 Mesh。
    # -------------------------------------------------------------------------
    cube_result = cmds.polyCube(
        name=create_name(token, "clean_cube"),
        constructionHistory=False
    )
    cube = parent_under_test_root(
        cube_result[0],
        test_root
    )

    cmds.setAttr(cube + ".translateX", 3.0)
    cmds.setAttr(cube + ".rotateZ", 20.0)
    cmds.setAttr(cube + ".scaleY", 2.0)

    frozen_count, skipped_count = scene_clean_utils.freeze_transformations(
        [cube]
    )

    if frozen_count != 1 or skipped_count != 0:
        raise RuntimeError(
            u"Freeze 统计错误：frozen={} skipped={}".format(
                frozen_count,
                skipped_count
            )
        )

    assert_vector_close(
        cmds.getAttr(cube + ".translate")[0],
        [0.0, 0.0, 0.0],
        label=u"Freeze Translate"
    )
    assert_vector_close(
        cmds.getAttr(cube + ".rotate")[0],
        [0.0, 0.0, 0.0],
        label=u"Freeze Rotate"
    )
    assert_vector_close(
        cmds.getAttr(cube + ".scale")[0],
        [1.0, 1.0, 1.0],
        label=u"Freeze Scale"
    )

    # -------------------------------------------------------------------------
    # 步骤 2：创建 Test Root 下的 Parent -> Child 两层空 Group。
    # -------------------------------------------------------------------------
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

    deleted_count = scene_clean_utils.delete_empty_groups(
        [empty_child]
    )

    if deleted_count < 2:
        raise RuntimeError(
            u"递归 Empty Group 删除数量错误：{}".format(deleted_count)
        )

    if cmds.objExists(empty_parent):
        raise RuntimeError(u"Empty Parent 没有被递归删除。")

    if cmds.objExists(empty_child):
        raise RuntimeError(u"Empty Child 没有被删除。")

    return u"Safe Freeze + Recursive Empty Group Clean 成功"


# =============================================================================
# Report
# =============================================================================

def print_report(results):
    """打印 Maya Script Editor 易读报告，并返回结构化统计。"""
    print("")
    print("=" * 78)
    print("Muzi Toolset - Extended Core Smoke Test")
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
            error_text = result.get("traceback")

            if error_text:
                print(error_text)

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


# =============================================================================
# Public Runner
# =============================================================================

def run():
    """
    执行全部 Extended Core Case。

    执行流程：
        1. 创建唯一 Token 和 Test Root；
        2. 逐项执行六个领域测试；
        3. 单项失败只记录，不阻止下一项；
        4. finally 中完整清理临时节点；
        5. 打印并返回最终报告。
    """
    token = create_token()
    results = []
    test_root = None

    test_cases = [
        (
            "attr_utils",
            "Attribute / Config",
            test_attr_utils,
        ),
        (
            "hierarchy_utils",
            "DAG / Extra Group",
            test_hierarchy_utils,
        ),
        (
            "joint_utils",
            "Joint / Chain / Label",
            test_joint_utils,
        ),
        (
            "naming",
            "Name / Rename",
            test_naming_utils,
        ),
        (
            "model_check_utils",
            "Model Quality Check",
            test_model_check_utils,
        ),
        (
            "scene_clean_utils",
            "Safe Scene Clean",
            test_scene_clean_utils,
        ),
    ]

    try:
        test_root = create_test_root(token)

        for category, name, test_function in test_cases:
            run_case(
                results,
                token,
                test_root,
                category,
                name,
                test_function
            )
    finally:
        cleanup_test_nodes(
            token,
            test_root
        )

    return print_report(results)


if __name__ == "__main__":
    run()
