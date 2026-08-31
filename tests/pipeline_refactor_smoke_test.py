# coding=utf-8
u"""
Pipeline Refactor Smoke Test
============================

验证当前正式 Core 的关键 Maya 行为。

范围：
    scene_utils                  Node / Object Set
    transform_utils / math_utils Transform / Distance / World Matrix
    animation_utils              AnimCurve / Reset / Animation JSON
    connection_utils             Query / Safe Connect / Force / Plug Pair / Disconnect
    matrix_utils                 offsetParentMatrix Parent Matrix Network
    constraint_utils             Constraint Create / Query / Delete
    curve_utils / surface_utils  Curve / Surface / Follicle

测试只创建带本轮 Token 的临时数据，并在 finally 中清理。
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
from ..core import math_utils
from ..core import matrix_utils
from ..core import scene_utils
from ..core import surface_utils
from ..core import transform_utils


def create_token():
    u"""创建短测试 Token。"""
    return uuid.uuid4().hex[:8]


def create_name(token, description):
    u"""生成当前测试轮次的临时节点名称。"""
    return "__muzi_pipeline_test_{}_{}".format(
        token,
        description
    )


def delete_existing_test_nodes(token):
    u"""按 DAG 深度从深到浅清理当前 Token 的测试节点。"""
    nodes = cmds.ls(
        "__muzi_pipeline_test_{}_*".format(token),
        long=True
    )

    if nodes is None:
        nodes = []

    nodes_with_depth = []

    for node in nodes:
        nodes_with_depth.append({
            "node": node,
            "depth": node.count("|"),
        })

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
    u"""追加统一测试结果。"""
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
    u"""执行单项 Case，并把异常转换为失败记录。"""
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
# Scene
# =============================================================================

def test_scene_utils(token):
    u"""验证 Node Create 和 Object Set。"""
    source = scene_utils.create_node(
        "transform",
        create_name(token, "scene_source")
    )
    target = scene_utils.create_node(
        "transform",
        create_name(token, "scene_target")
    )

    if not cmds.objExists(source) or not cmds.objExists(target):
        raise RuntimeError(u"Scene Node 创建失败。")

    object_set = scene_utils.ensure_object_set(
        create_name(token, "set"),
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
            u"Object Set 成员数量错误：{}".format(len(members))
        )

    return u"Node Create + Object Set 成功"


# =============================================================================
# Transform / Math
# =============================================================================

def test_transform_utils(token):
    u"""验证 Transform 空间数据和纯数学距离。"""
    node_a = scene_utils.create_node(
        "transform",
        create_name(token, "distance_a")
    )
    node_b = scene_utils.create_node(
        "transform",
        create_name(token, "distance_b")
    )

    transform_utils.set_world_translation(
        node_a,
        [0.0, 0.0, 0.0]
    )
    transform_utils.set_world_translation(
        node_b,
        [3.0, 4.0, 0.0]
    )

    position_a = transform_utils.get_world_translation(node_a)
    position_b = transform_utils.get_world_translation(node_b)
    distance = math_utils.distance_between_points(
        position_a,
        position_b
    )

    if abs(distance - 5.0) > 0.0001:
        raise RuntimeError(
            u"Distance 计算错误：{}".format(distance)
        )

    transform_utils.move_relative(
        node_a,
        [1.0, 0.0, 0.0]
    )
    moved_position = transform_utils.get_world_translation(node_a)

    if abs(moved_position[0] - 1.0) > 0.0001:
        raise RuntimeError(
            u"Relative Move 错误：{}".format(moved_position)
        )

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
            u"World Matrix 设置失败：{}".format(matched_position)
        )

    return u"Point Distance + Move + World Matrix 成功"


# =============================================================================
# Animation
# =============================================================================

def test_animation_utils(token):
    u"""验证 AnimCurve Clear 和 Transform Reset。"""
    node = scene_utils.create_node(
        "transform",
        create_name(token, "animation")
    )

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

    if not animation_utils.get_animation_curves(nodes=[node]):
        raise RuntimeError(u"没有找到刚创建的 AnimCurve。")

    if not animation_utils.clear_animation_keys(nodes=[node]):
        raise RuntimeError(u"没有删除 AnimCurve。")

    cmds.setAttr(node + ".translateY", 8.0)
    cmds.setAttr(node + ".rotateZ", 25.0)
    cmds.setAttr(node + ".scaleX", 2.0)

    reset_nodes = animation_utils.reset_transform_channels([node])

    if node not in reset_nodes:
        raise RuntimeError(u"Transform Reset 没有返回测试节点。")

    if cmds.getAttr(node + ".translateY") != 0:
        raise RuntimeError(u"Translate Reset 失败。")

    if cmds.getAttr(node + ".rotateZ") != 0:
        raise RuntimeError(u"Rotate Reset 失败。")

    if cmds.getAttr(node + ".scaleX") != 1:
        raise RuntimeError(u"Scale Reset 失败。")

    return u"AnimCurve Clear + Transform Reset 成功"


# =============================================================================
# Connection
# =============================================================================

def test_connection_utils(token):
    u"""验证正式 Plug Connection Core。"""
    driver_a = scene_utils.create_node(
        "transform",
        create_name(token, "connection_driver_a")
    )
    driver_b = scene_utils.create_node(
        "transform",
        create_name(token, "connection_driver_b")
    )
    driven = scene_utils.create_node(
        "transform",
        create_name(token, "connection_driven")
    )
    pair_target_a = scene_utils.create_node(
        "transform",
        create_name(token, "connection_pair_a")
    )
    pair_target_b = scene_utils.create_node(
        "transform",
        create_name(token, "connection_pair_b")
    )

    source_a = driver_a + ".translateX"
    source_b = driver_b + ".translateX"
    destination = driven + ".translateY"

    # 基础连接 + 幂等。
    if not connection_utils.connect_plugs(source_a, destination):
        raise RuntimeError(u"Connection 创建失败。")

    if not connection_utils.connect_plugs(source_a, destination):
        raise RuntimeError(u"重复 Connection 没有保持幂等。")

    inputs = connection_utils.get_input_connections(destination)

    if source_a not in inputs:
        raise RuntimeError(u"Input Query 失败：{}".format(inputs))

    outputs = connection_utils.get_output_connections(source_a)

    if destination not in outputs:
        raise RuntimeError(u"Output Query 失败：{}".format(outputs))

    cmds.setAttr(source_a, 7.5)

    if abs(cmds.getAttr(destination) - 7.5) > 0.0001:
        raise RuntimeError(u"DG 传值失败。")

    # force=False 必须保护已有输入。
    if connection_utils.connect_plugs(
            source_b,
            destination,
            force=False
    ):
        raise RuntimeError(u"force=False 不应覆盖已有输入。")

    inputs = connection_utils.get_input_connections(destination)

    if source_a not in inputs:
        raise RuntimeError(u"force=False 破坏了原输入。")

    # force=True 明确替换。
    if not connection_utils.connect_plugs(
            source_b,
            destination,
            force=True
    ):
        raise RuntimeError(u"force=True 替换失败。")

    inputs = connection_utils.get_input_connections(destination)

    if source_b not in inputs or source_a in inputs:
        raise RuntimeError(
            u"force=True 后来源错误：{}".format(inputs)
        )

    # 无效 Plug 与“没有连接”必须区分。
    invalid_plug_failed = False

    try:
        connection_utils.get_input_connections(
            driver_a + ".doesNotExist"
        )
    except RuntimeError:
        invalid_plug_failed = True

    if not invalid_plug_failed:
        raise RuntimeError(u"无效 Plug 没有抛 RuntimeError。")

    # 单 Destination 输入断开。
    disconnected_count = connection_utils.disconnect_input(destination)

    if disconnected_count != 1:
        raise RuntimeError(
            u"disconnect_input 数量错误：{}".format(
                disconnected_count
            )
        )

    if connection_utils.get_input_connections(destination):
        raise RuntimeError(u"disconnect_input 后仍存在输入。")

    # 显式 Plug Pair 批处理。
    connection_pairs = [
        (
            driver_a + ".translateY",
            pair_target_a + ".translateY"
        ),
        (
            driver_a + ".translateZ",
            pair_target_b + ".translateZ"
        ),
    ]

    connected_count = connection_utils.connect_plug_pairs(
        connection_pairs
    )

    if connected_count != 2:
        raise RuntimeError(
            u"connect_plug_pairs 数量错误：{}".format(
                connected_count
            )
        )

    disconnected_count = connection_utils.disconnect_plug_pairs(
        connection_pairs
    )

    if disconnected_count != 2:
        raise RuntimeError(
            u"disconnect_plug_pairs 数量错误：{}".format(
                disconnected_count
            )
        )

    return u"Query + Safe Connect + Force + Plug Pair + Disconnect 成功"


# =============================================================================
# Matrix
# =============================================================================

def test_matrix_utils(token):
    u"""验证 Parent Matrix Network 的 Maintain Offset 和 Remove。"""
    driven_parent = scene_utils.create_node(
        "transform",
        create_name(token, "matrix_parent")
    )
    driver = scene_utils.create_node(
        "transform",
        create_name(token, "matrix_driver")
    )
    driven = scene_utils.create_node(
        "transform",
        create_name(token, "matrix_driven")
    )

    cmds.xform(
        driven_parent,
        worldSpace=True,
        translation=[10.0, 0.0, 0.0]
    )
    cmds.parent(driven, driven_parent)
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
            u"Matrix Follow 错误：{}".format(after_position)
        )

    if not matrix_utils.remove_parent_matrix_constraint(
            driven,
            delete_node=True
    ):
        raise RuntimeError(u"Matrix Constraint 删除失败。")

    return u"Maintain Offset + Parent Hierarchy + OPM Follow + Remove 成功"


# =============================================================================
# Constraint
# =============================================================================

def test_constraint_utils(token):
    u"""验证标准 Constraint 创建、查询和删除。"""
    driver = scene_utils.create_node(
        "transform",
        create_name(token, "constraint_driver")
    )
    driven = scene_utils.create_node(
        "transform",
        create_name(token, "constraint_driven")
    )

    created = constraint_utils.create_constraint(
        driver_objects=[driver],
        driven_object=driven,
        constraint_type="parentConstraint",
        maintain_offset=True
    )

    if not created:
        raise RuntimeError(u"Parent Constraint 创建失败。")

    if not constraint_utils.get_constraints([driven]):
        raise RuntimeError(u"Constraint 查询失败。")

    if not constraint_utils.delete_constraints([driven]):
        raise RuntimeError(u"Constraint 删除失败。")

    return u"Create + Query + Delete Constraint 成功"


# =============================================================================
# Curve / Surface
# =============================================================================

def create_test_curve(token):
    u"""创建 Curve / Surface 测试共用曲线。"""
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
    u"""验证 Curve Query 和等弧长采样。"""
    curve = create_test_curve(token)
    curve_shape = curve_utils.get_curve_shape(curve)

    if cmds.nodeType(curve_shape) != "nurbsCurve":
        raise RuntimeError(u"Curve Shape 查询失败。")

    curve_count = curve_utils.get_curve_cv_count(curve)

    if curve_count != 4:
        raise RuntimeError(
            u"Curve CV 数量错误：{}".format(curve_count)
        )

    sample_data = curve_utils.sample_curve_by_length(curve, 5)

    if len(sample_data["points"]) != 5:
        raise RuntimeError(u"Curve Sample Point 数量错误。")

    if len(sample_data["tangents"]) != 5:
        raise RuntimeError(u"Curve Sample Tangent 数量错误。")

    return u"Curve Query + Arc Length Sample 成功"


def test_surface_utils(token):
    u"""验证 Curve Loft Surface 和 Follicle。"""
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

    if not cmds.objExists(follicle_result["transform"]):
        raise RuntimeError(u"Follicle Transform 不存在。")

    if not cmds.objExists(follicle_result["shape"]):
        raise RuntimeError(u"Follicle Shape 不存在。")

    return u"Curve Loft Surface + Follicle 成功"


# =============================================================================
# Animation JSON
# =============================================================================

def test_animation_json(token):
    u"""验证 Animation JSON Export / Clear / Import。"""
    node = scene_utils.create_node(
        "transform",
        create_name(token, "animation_json")
    )
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

    file_path = os.path.join(
        tempfile.gettempdir(),
        create_name(token, "animation") + ".json"
    )

    try:
        animation_utils.export_animation(
            nodes=[node],
            file_path=file_path
        )

        if not os.path.isfile(file_path):
            raise RuntimeError(u"Animation JSON 没有生成。")

        animation_utils.clear_animation_keys(nodes=[node])

        if cmds.keyframe(
                node + ".translateX",
                query=True,
                keyframeCount=True
        ):
            raise RuntimeError(u"导入前关键帧没有清理干净。")

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
    u"""执行 Pipeline Refactor Core Smoke Test。"""
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
        cases = [
            ("scene_utils", "Node / Object Set", test_scene_utils),
            (
                "transform_utils / math_utils",
                "Transform / Math / Matrix",
                test_transform_utils
            ),
            ("animation_utils", "Animation / Reset", test_animation_utils),
            ("connection_utils", "Connections", test_connection_utils),
            ("matrix_utils", "Matrix Constraint", test_matrix_utils),
            ("constraint_utils", "Constraint", test_constraint_utils),
            ("curve_utils", "Curve", test_curve_utils),
            ("surface_utils", "Surface / Follicle", test_surface_utils),
            ("animation_utils", "Animation JSON", test_animation_json),
        ]

        for category, name, test_function in cases:
            run_case(
                results,
                token,
                category,
                name,
                test_function
            )
    finally:
        delete_existing_test_nodes(token)
        cmds.undoInfo(closeChunk=True)

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
