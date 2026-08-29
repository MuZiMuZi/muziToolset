# coding=utf-8
u"""
Extended Core Smoke Test
========================

MuziTools Core 第二层 Maya 真机验证。

测试目的
--------
Pipeline Refactor Smoke Test 负责验证从旧 Pipeline 拆出的基础能力，例如 Scene、Transform、Matrix、
Connection、Constraint、Curve 和 Surface。

本测试专门验证这次重新整理的较高层 Core 领域：

    attr_utils
        Attribute / String Config / Message Config。

    hierarchy_utils
        DAG Parent / Extra Group / World Transform 保持。

    joint_utils
        Joint Create / Joint Chain / Joint Label。

    name_utils + rename_utils
        五段式命名、Side 规范化、Mirror Name、Maya Rename。

    model_check_utils
        Mesh Transform Issue 检查与 Issue 数据结构。

    scene_clean_utils
        Freeze Transform 与递归 Empty Group 清理。

为什么单独建立 Extended Smoke
----------------------------
这些模块比基础 Math / DG Utility 更接近真实 Maya 场景行为。如果把它们全部塞回
``pipeline_refactor_smoke_test.py``，基础 Core 与场景质量工具会重新混在一起，失败时也更难定位。

因此质量门槛分成两层：

    Pipeline Smoke
        验证基础 Core 拆分和节点网络。

    Extended Core Smoke
        验证 Attribute / DAG / Joint / Naming / Model Quality / Scene Clean。

安全原则
--------
1. 所有测试节点都使用唯一 ``__muzi_extended_test_<token>_`` 前缀；
2. 测试结束后无论成功还是失败都会尝试清理临时节点；
3. 不打开 / 保存用户 Scene；
4. 不删除用户节点；
5. 不依赖 PyMel；
6. 不测试 UI，不需要用户 Selection；
7. 每个测试只验证稳定公开行为，不依赖 Maya 内部临时节点名称。

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
# Helpers - 公共测试辅助
# =============================================================================

def create_token():
    """创建短 Token，让测试节点不会与用户场景或另一轮测试重名。"""
    return uuid.uuid4().hex[:8]


def create_name(token, description):
    """生成当前测试轮次专用的临时节点名称。"""
    return "__muzi_extended_test_{}_{}".format(
        token,
        description
    )


def assert_close(actual, expected, tolerance=0.0001, label=u"数值"):
    """验证两个数值在给定容差内相等。"""
    if abs(actual - expected) > tolerance:
        raise RuntimeError(
            u"{}错误：actual={} expected={}".format(
                label,
                actual,
                expected
            )
        )


def assert_vector_close(actual, expected, tolerance=0.0001, label=u"向量"):
    """逐项验证 Maya 三维向量。"""
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


def delete_existing_test_nodes(token):
    """
    删除当前 Token 创建的测试节点。

    DAG 节点必须先删除最深层 Child，再删除 Parent；否则 Parent 删除后原 Child Long Path 会失效。
    """
    pattern = "__muzi_extended_test_{}_*".format(token)
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
    """追加一条结构化测试结果。"""
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
        category,
        name,
        test_function
):
    """运行一项测试，把 Python 异常转换为统一失败记录。"""
    try:
        message = test_function(token)

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

def test_attr_utils(token):
    """
    验证普通属性、String Config 和 Message Config。

    Message 是 Rig Setup 保存 Maya 节点引用的重要方式，因此除了“连接成功”，还要验证 Rename 前后
    仍然可以通过 Message 找到来源节点。
    """
    config_node = cmds.createNode(
        "transform",
        name=create_name(token, "attr_config")
    )
    source_node = cmds.createNode(
        "transform",
        name=create_name(token, "attr_source")
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

    value = attr.get_attr_value("test_value")
    assert_close(value, 3.5, label=u"Attribute Value")

    # -------------------------------------------------------------------------
    # 步骤 2：保存 Python 基础数据到 String Config，并恢复成原字典。
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
            u"String Config 恢复结果错误：{}".format(restored_data)
        )

    # -------------------------------------------------------------------------
    # 步骤 3：建立 Message 引用并验证来源节点。
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

    # Maya 可能返回 Short Name 或 Long Path，因此统一比较 Short Name。
    message_short_name = message_node.split("|")[-1]
    source_short_name = source_node.split("|")[-1]

    if message_short_name != source_short_name:
        raise RuntimeError(
            u"Message 来源错误：{}".format(message_node)
        )

    return u"Value + String Config + Message Config 成功"


# =============================================================================
# Hierarchy Utils
# =============================================================================

def test_hierarchy_utils(token):
    """验证 Extra Group 插入后 DAG 关系和对象世界姿态保持。"""
    root = cmds.createNode(
        "transform",
        name=create_name(token, "hierarchy_root")
    )
    target = cmds.createNode(
        "transform",
        name=create_name(token, "hierarchy_target")
    )

    cmds.xform(
        root,
        worldSpace=True,
        translation=[10.0, 0.0, 0.0]
    )
    cmds.parent(
        target,
        root,
        absolute=True
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
    # 步骤 1：在 Target 上方插入 Extra Group。
    # -------------------------------------------------------------------------
    extra_group = hierarchy_utils.Hierarchy.add_extra_group(
        target,
        create_name(token, "hierarchy_zero"),
        world_orient=False
    )

    if not cmds.objExists(extra_group):
        raise RuntimeError(u"Extra Group 没有创建。")

    # -------------------------------------------------------------------------
    # 步骤 2：验证 Target 已经成为 Extra Group 的直接 Child。
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
    # 步骤 3：插组不应该改变 Target 的世界位置和世界旋转。
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

def test_joint_utils(token):
    """验证 Joint 创建、Chain Parent、Radius 和 Joint Label。"""
    root_name = create_name(token, "joint_root")
    child_name = create_name(token, "joint_child")

    root_joint = joint_utils.Joint.create(
        name=root_name,
        position=[0.0, 5.0, 0.0],
        radius=1.5
    )
    child_joint = joint_utils.Joint.create(
        name=child_name,
        position=[3.0, 5.0, 0.0]
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
        raise RuntimeError(u"Joint Chain 没有建立 Parent。")

    if parents[0].split("|")[-1] != root_name:
        raise RuntimeError(
            u"Joint Chain Parent 错误：{}".format(parents[0])
        )

    radius = cmds.getAttr(root_joint + ".radius")
    assert_close(radius, 1.5, label=u"Joint Radius")

    # -------------------------------------------------------------------------
    # 步骤 2：单独创建正式命名 Joint，验证 lf Side 的 Maya Joint Label。
    # -------------------------------------------------------------------------
    tagged_name = "jnt_lf_{}_bind_001".format(
        token.lower()
    )
    tagged_joint = joint_utils.Joint.create(
        name=tagged_name,
        position=[0.0, 0.0, 0.0]
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

def test_naming_utils(token):
    """验证正式五段式名称、Side Alias、Mirror Name 和 Maya Rename。"""
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

    expected_name = "jnt_lf_arm_bind_001"

    if standard_name != expected_name:
        raise RuntimeError(
            u"标准名称生成错误：{}".format(standard_name)
        )

    # -------------------------------------------------------------------------
    # 步骤 2：Parse 后字段必须完整恢复。
    # -------------------------------------------------------------------------
    parsed = name_utils.Name.parse_name(standard_name)

    if parsed["type"] != "jnt":
        raise RuntimeError(u"Name Parse type 错误。")

    if parsed["side"] != "lf":
        raise RuntimeError(u"Name Parse side 错误。")

    if parsed["part"] != "arm":
        raise RuntimeError(u"Name Parse part 错误。")

    if parsed["function"] != "bind":
        raise RuntimeError(u"Name Parse function 错误。")

    if parsed["index"] != 1:
        raise RuntimeError(u"Name Parse index 错误。")

    # -------------------------------------------------------------------------
    # 步骤 3：Mirror Name 只改变 lf / rt，不改其它字段。
    # -------------------------------------------------------------------------
    mirror_name = name_utils.Name.mirror_name(standard_name)

    if mirror_name != "jnt_rt_arm_bind_001":
        raise RuntimeError(
            u"Mirror Name 错误：{}".format(mirror_name)
        )

    # -------------------------------------------------------------------------
    # 步骤 4：rename_utils.rename_node 必须真正修改 Maya DAG 节点。
    # -------------------------------------------------------------------------
    source = cmds.createNode(
        "transform",
        name=create_name(token, "rename_source")
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

def test_model_check_utils(token):
    """验证 Mesh Transform 检查能够发现一个明确的未冻结模型。"""
    # -------------------------------------------------------------------------
    # 步骤 1：创建带 Construction History 的普通 Poly Cube。
    # -------------------------------------------------------------------------
    cube_result = cmds.polyCube(
        name=create_name(token, "model_cube"),
        constructionHistory=True
    )
    cube = cube_result[0]

    cmds.setAttr(cube + ".translateX", 4.0)
    cmds.setAttr(cube + ".rotateY", 15.0)
    cmds.setAttr(cube + ".scaleZ", 1.5)

    # -------------------------------------------------------------------------
    # 步骤 2：Transform Check 应该返回一个统一 Issue。
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

def test_scene_clean_utils(token):
    """验证安全 Freeze Transform 和递归 Empty Group 清理。"""
    # -------------------------------------------------------------------------
    # 步骤 1：创建一个没有 Animation / Constraint / Deformer 的普通 Mesh。
    # -------------------------------------------------------------------------
    cube_result = cmds.polyCube(
        name=create_name(token, "clean_cube"),
        constructionHistory=False
    )
    cube = cube_result[0]

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

    translate = cmds.getAttr(cube + ".translate")[0]
    rotate = cmds.getAttr(cube + ".rotate")[0]
    scale = cmds.getAttr(cube + ".scale")[0]

    assert_vector_close(
        translate,
        [0.0, 0.0, 0.0],
        label=u"Freeze Translate"
    )
    assert_vector_close(
        rotate,
        [0.0, 0.0, 0.0],
        label=u"Freeze Rotate"
    )
    assert_vector_close(
        scale,
        [1.0, 1.0, 1.0],
        label=u"Freeze Scale"
    )

    # -------------------------------------------------------------------------
    # 步骤 2：创建 Parent -> Child 两层空 Group。
    # 删除 Child 后 Parent 才会变空，所以能验证递归循环逻辑。
    # -------------------------------------------------------------------------
    empty_parent = cmds.createNode(
        "transform",
        name=create_name(token, "empty_parent")
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
# Runner / Report
# =============================================================================

def print_report(results):
    """把结构化测试结果打印成 Maya Script Editor 易读格式。"""
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


def run():
    """
    执行 Extended Core Smoke Test。

    每一项 Case 独立记录错误；即使前面某项失败，后面的领域仍然继续执行，便于一次看到完整结果。
    测试结束后统一清理本轮 Token 创建的节点。
    """
    token = create_token()
    results = []

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
        for category, name, test_function in test_cases:
            run_case(
                results,
                token,
                category,
                name,
                test_function
            )
    finally:
        delete_existing_test_nodes(token)

    return print_report(results)


if __name__ == "__main__":
    run()
