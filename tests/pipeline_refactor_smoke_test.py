# coding=utf-8
u"""
Pipeline Refactor Smoke Test
============================

验证从旧 pipelineUtils / Legacy Core 重构出来的正式 Core 模块。

测试范围
--------
    scene_utils
        Node / Object Set。

    transform_utils
        Translation / Distance / World Matrix。

    animation_utils
        AnimCurve Clear / Transform Reset。

    connection_utils
        Plug Connect / Query / DG Compute / Disconnect。

    matrix_utils
        Maintain Offset / Parent Hierarchy / offsetParentMatrix Follow / Remove。

    constraint_utils
        Maya Constraint Create / Query / Delete。

    curve_utils
        Curve Shape / CV Count / Arc Length Sample。

    surface_utils
        Curve Loft Surface / Follicle。

    animation_utils - Animation JSON
        JSON Export / Clear / Import。

说明
----
动画 JSON 已经合并回 ``core.animation_utils``，不再依赖单独的
``animation_io_utils.py``。

测试会创建带 ``__muzi_pipeline_test_`` 前缀的临时节点，
结束后自动删除；Animation JSON 会写入系统临时目录并在测试后清理。
"""

from __future__ import print_function

import os
import tempfile
import traceback
import uuid

import maya.cmds as cmds

from ..core import animation_utils
from ..core import connection_utils
from ..core import constraint_utils
from ..core import curve_utils
from ..core import matrix_utils
from ..core import scene_utils
from ..core import surface_utils
from ..core import transform_utils


# =============================================================================
# Helpers - 测试公共辅助
# =============================================================================

def create_token():
    """创建短测试 Token，避免测试节点和用户场景重名。"""
    return uuid.uuid4().hex[:8]


def create_name(token, description):
    """根据 Token 和功能描述生成测试节点名称。"""
    return "__muzi_pipeline_test_{}_{}".format(
        token,
        description
    )


def delete_existing_test_nodes(token):
    """
    删除当前 Token 产生的测试节点。

    DAG 节点按路径深度从深到浅删除，避免先删 Parent 后 Child Path 失效。
    """
    # 步骤 1：查找本轮测试创建的节点。
    pattern = "__muzi_pipeline_test_{}_*".format(token)
    nodes = cmds.ls(
        pattern,
        long=True
    )

    if nodes is None:
        nodes = []

    # 步骤 2：记录 DAG 深度。
    nodes_with_depth = []

    for node in nodes:
        node_data = {
            "node": node,
            "depth": node.count("|"),
        }
        nodes_with_depth.append(node_data)

    def get_depth(node_data):
        return node_data["depth"]

    # 步骤 3：先删除最深层节点。
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
    """向测试报告中追加一条结构化结果。"""
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
    """执行单项测试，并把异常转换成统一报告。"""
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
# Scene Utils
# =============================================================================

def test_scene_utils(token):
    """测试 Node Match 和 Object Set 基础能力。"""
    # 步骤 1：创建 Source Transform。
    source = cmds.createNode(
        "transform",
        name=create_name(token, "scene_source")
    )
    cmds.xform(
        source,
        worldSpace=True,
        translation=[1.0, 2.0, 3.0]
    )

    # 步骤 2：通过 scene_utils 创建并 Match 新节点。
    target = scene_utils.create_node(
        node_type="transform",
        name=create_name(token, "scene_target"),
        match_node=source
    )

    target_position = cmds.xform(
        target,
        query=True,
        worldSpace=True,
        translation=True
    )

    if target_position != [1.0, 2.0, 3.0]:
        raise RuntimeError(
            u"scene_utils.create_node Match 位置错误：{}".format(
                target_position
            )
        )

    # 步骤 3：创建 Object Set 并加入两个节点。
    object_set = scene_utils.ensure_object_set(
        set_name=create_name(token, "set"),
        objects=[source, target]
    )

    members = cmds.sets(
        object_set,
        query=True
    )

    if members is None:
        members = []

    if len(members) != 2:
        raise RuntimeError(
            u"Object Set 成员数量错误：{}".format(
                len(members)
            )
        )

    return u"Node Match + Object Set 成功"


# =============================================================================
# Transform Utils
# =============================================================================

def test_transform_utils(token):
    """测试位置、相对移动、距离和 World Matrix。"""
    node_a = cmds.createNode(
        "transform",
        name=create_name(token, "distance_a")
    )
    node_b = cmds.createNode(
        "transform",
        name=create_name(token, "distance_b")
    )

    # 步骤 1：设置两个世界位置，构造 3-4-5 三角形。
    transform_utils.set_world_translation(
        node_a,
        [0.0, 0.0, 0.0]
    )
    transform_utils.set_world_translation(
        node_b,
        [3.0, 4.0, 0.0]
    )

    distance = transform_utils.distance_between(
        node_a,
        node_b
    )

    if abs(distance - 5.0) > 0.0001:
        raise RuntimeError(
            u"Distance 计算错误：{}".format(distance)
        )

    # 步骤 2：测试相对移动。
    transform_utils.move_relative(
        node_a,
        [1.0, 0.0, 0.0]
    )

    position_a = transform_utils.get_world_translation(node_a)

    if abs(position_a[0] - 1.0) > 0.0001:
        raise RuntimeError(
            u"Relative Move 结果错误：{}".format(position_a)
        )

    # 步骤 3：读取 B 的 World Matrix 并写给 A。
    world_matrix = transform_utils.get_world_matrix(node_b)

    if len(world_matrix) != 16:
        raise RuntimeError(u"World Matrix 长度不是 16。")

    transform_utils.set_world_matrix(
        node_a,
        world_matrix
    )

    matched_position = transform_utils.get_world_translation(node_a)

    if abs(matched_position[0] - 3.0) > 0.0001:
        raise RuntimeError(
            u"World Matrix 设置失败：{}".format(
                matched_position
            )
        )

    return u"Distance + Move + World Matrix 成功"


# =============================================================================
# Animation Utils - AnimCurve / Reset
# =============================================================================

def test_animation_utils(token):
    """测试 AnimCurve 查询 / 清除和 Transform Reset。"""
    node = cmds.createNode(
        "transform",
        name=create_name(token, "animation")
    )

    # 步骤 1：创建两帧 Translate X 动画。
    cmds.setKeyframe(
        node,
        attribute="translateX",
        time=1,
        value=0.0
    )
    cmds.setKeyframe(
        node,
        attribute="translateX",
        time=10,
        value=10.0
    )

    animation_curves = animation_utils.get_animation_curves(
        nodes=[node]
    )

    if not animation_curves:
        raise RuntimeError(u"没有找到刚创建的 AnimCurve。")

    # 步骤 2：删除 AnimCurve。
    deleted_curves = animation_utils.clear_animation_keys(
        nodes=[node]
    )

    if not deleted_curves:
        raise RuntimeError(u"没有删除 AnimCurve。")

    # 步骤 3：给 TRS 写入非默认值，再执行 Reset。
    cmds.setAttr(node + ".translateY", 8.0)
    cmds.setAttr(node + ".rotateZ", 25.0)
    cmds.setAttr(node + ".scaleX", 2.0)

    reset_nodes = animation_utils.reset_transform_channels(
        [node]
    )

    if node not in reset_nodes:
        raise RuntimeError(u"Transform Reset 没有返回测试节点。")

    translate_y = cmds.getAttr(node + ".translateY")
    rotate_z = cmds.getAttr(node + ".rotateZ")
    scale_x = cmds.getAttr(node + ".scaleX")

    if translate_y != 0 or rotate_z != 0 or scale_x != 1:
        raise RuntimeError(u"Transform Reset 结果错误。")

    return u"AnimCurve Clear + Transform Reset 成功"


# =============================================================================
# Connection Utils
# =============================================================================

def test_connection_utils(token):
    """测试 Plug 创建、查询、DG 计算和断开连接。"""
    driver = cmds.createNode(
        "transform",
        name=create_name(token, "connection_driver")
    )
    driven = cmds.createNode(
        "transform",
        name=create_name(token, "connection_driven")
    )

    source_plug = driver + ".translateX"
    destination_plug = driven + ".translateY"

    # 步骤 1：创建连接。
    created = connection_utils.connect_plugs(
        source_plug,
        destination_plug
    )

    if not created:
        raise RuntimeError(u"Connection 创建失败。")

    # 步骤 2：分别检查输入和输出查询。
    input_connections = connection_utils.get_input_connections(
        destination_plug
    )

    if source_plug not in input_connections:
        raise RuntimeError(
            u"Input Connection 查询失败：{}".format(
                input_connections
            )
        )

    output_connections = connection_utils.get_output_connections(
        source_plug
    )

    if destination_plug not in output_connections:
        raise RuntimeError(
            u"Output Connection 查询失败：{}".format(
                output_connections
            )
        )

    # 步骤 3：写 Driver，确认 Maya DG 真正传值。
    cmds.setAttr(source_plug, 7.5)
    driven_value = cmds.getAttr(destination_plug)

    if abs(driven_value - 7.5) > 0.0001:
        raise RuntimeError(
            u"Connection DG 计算错误：{}".format(
                driven_value
            )
        )

    # 步骤 4：断开连接。
    disconnected = connection_utils.disconnect_plugs(
        source_plug,
        destination_plug
    )

    if not disconnected:
        raise RuntimeError(u"Connection 断开失败。")

    return u"Connect + Query + DG + Disconnect 成功"


# =============================================================================
# Matrix Utils
# =============================================================================

def test_matrix_utils(token):
    """
    测试有 Parent 层级时的 offsetParentMatrix Parent Matrix Constraint。

    这个测试专门覆盖 ``parent.worldInverseMatrix`` 路径，
    防止未来再次使用 Driven 自己的 parentInverseMatrix 导致 Cycle Warning。
    """
    # 步骤 1：创建 Parent / Driver / Driven。
    driven_parent = cmds.createNode(
        "transform",
        name=create_name(token, "matrix_parent")
    )
    driver = cmds.createNode(
        "transform",
        name=create_name(token, "matrix_driver")
    )
    driven = cmds.createNode(
        "transform",
        name=create_name(token, "matrix_driven")
    )

    cmds.xform(
        driven_parent,
        worldSpace=True,
        translation=[10.0, 0.0, 0.0]
    )

    cmds.parent(
        driven,
        driven_parent
    )

    # 步骤 2：设置建立约束前的 World Position。
    cmds.xform(
        driver,
        worldSpace=True,
        translation=[1.0, 0.0, 0.0]
    )
    cmds.xform(
        driven,
        worldSpace=True,
        translation=[4.0, 2.0, 0.0]
    )

    # 步骤 3：建立 Maintain Offset Matrix Constraint。
    matrix_node = matrix_utils.create_parent_matrix_constraint(
        driver=driver,
        driven=driven,
        maintain_offset=True,
        name=create_name(token, "parent_mm")
    )

    if not cmds.objExists(matrix_node):
        raise RuntimeError(u"multMatrix 创建失败。")

    before_position = cmds.xform(
        driven,
        query=True,
        worldSpace=True,
        translation=True
    )

    if abs(before_position[0] - 4.0) > 0.0001:
        raise RuntimeError(
            u"Maintain Offset 创建后位置改变：{}".format(
                before_position
            )
        )

    # 步骤 4：Driver X 从 1 移动到 3，Driven 应从 4 跟到 6。
    cmds.xform(
        driver,
        worldSpace=True,
        translation=[3.0, 0.0, 0.0]
    )

    after_position = cmds.xform(
        driven,
        query=True,
        worldSpace=True,
        translation=True
    )

    if abs(after_position[0] - 6.0) > 0.0001:
        raise RuntimeError(
            u"Matrix Constraint 跟随结果错误：{}".format(
                after_position
            )
        )

    # 步骤 5：断开并删除 Matrix Node。
    removed = matrix_utils.remove_parent_matrix_constraint(
        driven,
        delete_node=True
    )

    if not removed:
        raise RuntimeError(u"Matrix Constraint 删除失败。")

    return u"Maintain Offset + Parent Hierarchy + OPM Follow + Remove 成功"


# =============================================================================
# Constraint Utils
# =============================================================================

def test_constraint_utils(token):
    """测试标准 Constraint 创建、查询和删除。"""
    driver = cmds.createNode(
        "transform",
        name=create_name(token, "constraint_driver")
    )
    driven = cmds.createNode(
        "transform",
        name=create_name(token, "constraint_driven")
    )

    created_constraints = constraint_utils.create_constraint(
        driver_objects=[driver],
        driven_object=driven,
        constraint_type="parentConstraint",
        maintain_offset=True
    )

    if not created_constraints:
        raise RuntimeError(u"Parent Constraint 创建失败。")

    found_constraints = constraint_utils.get_constraints(
        [driven]
    )

    if not found_constraints:
        raise RuntimeError(u"Constraint 查询失败。")

    deleted_constraints = constraint_utils.delete_constraints(
        [driven]
    )

    if not deleted_constraints:
        raise RuntimeError(u"Constraint 删除失败。")

    return u"Create + Query + Delete Constraint 成功"


# =============================================================================
# Curve / Surface Helpers
# =============================================================================

def create_test_curve(token):
    """创建 Curve / Surface 测试共用的三次 NURBS Curve。"""
    return cmds.curve(
        name=create_name(token, "curve"),
        degree=3,
        point=[
            [0.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [2.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
        ]
    )


def test_curve_utils(token):
    """测试 Curve Shape、CV Count 和等弧长采样。"""
    curve = create_test_curve(token)

    curve_shape = curve_utils.get_curve_shape(curve)

    if cmds.nodeType(curve_shape) != "nurbsCurve":
        raise RuntimeError(u"Curve Shape 查询失败。")

    curve_count = curve_utils.get_curve_cv_count(curve)

    if curve_count != 4:
        raise RuntimeError(
            u"Curve CV 数量错误：{}".format(curve_count)
        )

    sample_data = curve_utils.sample_curve_by_length(
        curve,
        5
    )

    if len(sample_data["points"]) != 5:
        raise RuntimeError(u"Curve Sample Point 数量错误。")

    if len(sample_data["tangents"]) != 5:
        raise RuntimeError(u"Curve Sample Tangent 数量错误。")

    return u"Curve Query + Arc Length Sample 成功"


def test_surface_utils(token):
    """测试 Curve Loft Surface 和 Follicle。"""
    curve = create_test_curve(token)

    surface = surface_utils.create_surface_from_curve(
        curve=curve,
        name=create_name(token, "surface"),
        offset=0.25,
        offset_axis="Y"
    )

    surface_shape = surface_utils.get_surface_shape(surface)

    if cmds.nodeType(surface_shape) != "nurbsSurface":
        raise RuntimeError(u"NURBS Surface 创建失败。")

    follicle_result = surface_utils.create_follicle(
        surface=surface,
        name=create_name(token, "follicle"),
        parameter_u=0.5,
        parameter_v=0.5
    )

    follicle_transform = follicle_result["transform"]
    follicle_shape = follicle_result["shape"]

    if not cmds.objExists(follicle_transform):
        raise RuntimeError(u"Follicle Transform 不存在。")

    if not cmds.objExists(follicle_shape):
        raise RuntimeError(u"Follicle Shape 不存在。")

    return u"Curve Loft Surface + Follicle 成功"


# =============================================================================
# Animation Utils - JSON Export / Import
# =============================================================================

def test_animation_json(token):
    """测试合并后的 animation_utils 动画 JSON 导出、清除和恢复。"""
    node = cmds.createNode(
        "transform",
        name=create_name(token, "animation_json")
    )

    # 步骤 1：创建测试 Key。
    cmds.setKeyframe(
        node,
        attribute="translateX",
        time=1,
        value=1.25
    )
    cmds.setKeyframe(
        node,
        attribute="translateX",
        time=8,
        value=4.5
    )

    file_name = create_name(
        token,
        "animation"
    ) + ".json"

    file_path = os.path.join(
        tempfile.gettempdir(),
        file_name
    )

    try:
        # 步骤 2：从 animation_utils 导出 JSON。
        animation_utils.export_animation(
            nodes=[node],
            file_path=file_path
        )

        if not os.path.isfile(file_path):
            raise RuntimeError(u"Animation JSON 没有生成。")

        # 步骤 3：清理 Maya 动画，确保后续 Key 确实来自 Import。
        animation_utils.clear_animation_keys(
            nodes=[node]
        )

        cleared_count = cmds.keyframe(
            node + ".translateX",
            query=True,
            keyframeCount=True
        )

        if cleared_count:
            raise RuntimeError(u"导入前关键帧没有清理干净。")

        # 步骤 4：从同一个 animation_utils 恢复 JSON。
        import_result = animation_utils.import_animation(
            file_path=file_path,
            clear_existing=False,
            strict=True
        )

        if import_result["created_keys"] != 2:
            raise RuntimeError(
                u"恢复关键帧数量错误：{}".format(
                    import_result["created_keys"]
                )
            )

        restored_count = cmds.keyframe(
            node + ".translateX",
            query=True,
            keyframeCount=True
        )

        if restored_count != 2:
            raise RuntimeError(
                u"Maya 中恢复的 Key 数量错误：{}".format(
                    restored_count
                )
            )

    finally:
        # 步骤 5：测试文件属于临时数据，无论成功失败都清理。
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass

    return u"JSON Export + Clear + Import 成功"


# =============================================================================
# Runner
# =============================================================================

def run():
    """执行 Pipeline Refactor Core Smoke Test。"""
    token = create_token()
    results = []

    print("")
    print("=" * 78)
    print("Muzi Toolset - Pipeline Refactor Smoke Test")
    print("=" * 78)

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziPipelineRefactorSmokeTest"
    )

    try:
        run_case(
            results,
            token,
            "scene_utils",
            "Node / Object Set",
            test_scene_utils
        )
        run_case(
            results,
            token,
            "transform_utils",
            "Transform / Matrix",
            test_transform_utils
        )
        run_case(
            results,
            token,
            "animation_utils",
            "Animation / Reset",
            test_animation_utils
        )
        run_case(
            results,
            token,
            "connection_utils",
            "Connections",
            test_connection_utils
        )
        run_case(
            results,
            token,
            "matrix_utils",
            "Matrix Constraint",
            test_matrix_utils
        )
        run_case(
            results,
            token,
            "constraint_utils",
            "Constraint",
            test_constraint_utils
        )
        run_case(
            results,
            token,
            "curve_utils",
            "Curve",
            test_curve_utils
        )
        run_case(
            results,
            token,
            "surface_utils",
            "Surface / Follicle",
            test_surface_utils
        )
        run_case(
            results,
            token,
            "animation_utils",
            "Animation JSON",
            test_animation_json
        )

    finally:
        delete_existing_test_nodes(token)
        cmds.undoInfo(
            closeChunk=True
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
