# coding=utf-8
u"""
Pipeline Refactor Smoke Test
============================

验证从旧 pipelineUtils / legacy Core 拆出的正式 Core 模块。

测试范围：
    animation_io_utils
    animation_utils
    connection_utils
    constraint_utils
    curve_utils
    matrix_utils
    scene_utils
    surface_utils
    transform_utils

测试会创建带 __muzi_pipeline_test_ 前缀的临时节点，结束后自动删除。
"""

from __future__ import print_function

import os
import tempfile
import traceback
import uuid

import maya.cmds as cmds

from ..core import animation_io_utils
from ..core import animation_utils
from ..core import connection_utils
from ..core import constraint_utils
from ..core import curve_utils
from ..core import matrix_utils
from ..core import scene_utils
from ..core import surface_utils
from ..core import transform_utils


# =============================================================================
# Helpers
# =============================================================================

def create_token():
    """创建短测试 Token。"""
    token = uuid.uuid4().hex[:8]
    return token


def create_name(token, description):
    """创建不容易和用户场景冲突的测试名称。"""
    return "__muzi_pipeline_test_{}_{}".format(
        token,
        description
    )


def delete_existing_test_nodes(token):
    """删除当前 Token 产生的测试节点。"""
    pattern = "__muzi_pipeline_test_{}_*".format(
        token
    )

    nodes = cmds.ls(
        pattern,
        long=True
    )

    if nodes is None:
        nodes = []

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


def record_result(results, category, name, passed, message, error_text=""):
    """追加一条测试结果。"""
    result = {
        "category": category,
        "name": name,
        "passed": passed,
        "message": message,
        "traceback": error_text,
    }

    results.append(result)
    return result


def run_case(results, token, category, name, test_function):
    """执行单项测试并记录异常。"""
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
# Tests
# =============================================================================

def test_scene_utils(token):
    """测试 Node / Set 基础能力。"""
    source_name = create_name(
        token,
        "scene_source"
    )
    target_name = create_name(
        token,
        "scene_target"
    )
    set_name = create_name(
        token,
        "set"
    )

    source = cmds.createNode(
        "transform",
        name=source_name
    )
    cmds.xform(
        source,
        worldSpace=True,
        translation=[1.0, 2.0, 3.0]
    )

    target = scene_utils.create_node(
        node_type="transform",
        name=target_name,
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

    object_set = scene_utils.ensure_object_set(
        set_name=set_name,
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


def test_transform_utils(token):
    """测试 Transform 位置、移动、距离和 Matrix。"""
    node_a = cmds.createNode(
        "transform",
        name=create_name(token, "distance_a")
    )
    node_b = cmds.createNode(
        "transform",
        name=create_name(token, "distance_b")
    )

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

    transform_utils.move_relative(
        node_a,
        [1.0, 0.0, 0.0]
    )

    position_a = transform_utils.get_world_translation(
        node_a
    )

    if abs(position_a[0] - 1.0) > 0.0001:
        raise RuntimeError(
            u"Relative Move 结果错误：{}".format(position_a)
        )

    world_matrix = transform_utils.get_world_matrix(
        node_b
    )

    if len(world_matrix) != 16:
        raise RuntimeError(u"World Matrix 长度不是 16。")

    transform_utils.set_world_matrix(
        node_a,
        world_matrix
    )

    matched_position = transform_utils.get_world_translation(
        node_a
    )

    if abs(matched_position[0] - 3.0) > 0.0001:
        raise RuntimeError(
            u"World Matrix 设置失败：{}".format(
                matched_position
            )
        )

    return u"Distance + Move + World Matrix 成功"


def test_animation_utils(token):
    """测试 Key 查询 / 清除和 Transform Reset。"""
    node = cmds.createNode(
        "transform",
        name=create_name(token, "animation")
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

    animation_curves = animation_utils.get_animation_curves(
        nodes=[node]
    )

    if not animation_curves:
        raise RuntimeError(u"没有找到刚创建的 AnimCurve。")

    deleted_curves = animation_utils.clear_animation_keys(
        nodes=[node]
    )

    if not deleted_curves:
        raise RuntimeError(u"没有删除 AnimCurve。")

    cmds.setAttr(
        node + ".translateY",
        8.0
    )
    cmds.setAttr(
        node + ".rotateZ",
        25.0
    )
    cmds.setAttr(
        node + ".scaleX",
        2.0
    )

    reset_nodes = animation_utils.reset_transform_channels(
        [node]
    )

    if node not in reset_nodes:
        raise RuntimeError(u"Transform Reset 没有返回测试节点。")

    translate_y = cmds.getAttr(
        node + ".translateY"
    )
    rotate_z = cmds.getAttr(
        node + ".rotateZ"
    )
    scale_x = cmds.getAttr(
        node + ".scaleX"
    )

    if translate_y != 0 or rotate_z != 0 or scale_x != 1:
        raise RuntimeError(
            u"Transform Reset 结果错误。"
        )

    return u"AnimCurve Clear + Transform Reset 成功"


def test_connection_utils(token):
    """测试 Plug 查询、创建和断开连接。"""
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

    created = connection_utils.connect_plugs(
        source_plug,
        destination_plug
    )

    if not created:
        raise RuntimeError(u"Connection 创建失败。")

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

    cmds.setAttr(
        source_plug,
        7.5
    )

    driven_value = cmds.getAttr(
        destination_plug
    )

    if abs(driven_value - 7.5) > 0.0001:
        raise RuntimeError(
            u"Connection DG 计算错误：{}".format(
                driven_value
            )
        )

    disconnected = connection_utils.disconnect_plugs(
        source_plug,
        destination_plug
    )

    if not disconnected:
        raise RuntimeError(u"Connection 断开失败。")

    return u"Connect + Query + DG + Disconnect 成功"


def test_matrix_utils(token):
    """测试 offsetParentMatrix Parent Matrix Constraint。"""
    driver = cmds.createNode(
        "transform",
        name=create_name(token, "matrix_driver")
    )
    driven = cmds.createNode(
        "transform",
        name=create_name(token, "matrix_driven")
    )

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
            u"Matrix Constraint 跟随结果错误：{}".format(
                after_position
            )
        )

    removed = matrix_utils.remove_parent_matrix_constraint(
        driven,
        delete_node=True
    )

    if not removed:
        raise RuntimeError(u"Matrix Constraint 删除失败。")

    return u"Maintain Offset + OPM Follow + Remove 成功"


def test_constraint_utils(token):
    """测试创建、查询和删除 Constraint。"""
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


def create_test_curve(token):
    """创建供 Curve / Surface 测试使用的曲线。"""
    curve = cmds.curve(
        name=create_name(token, "curve"),
        degree=3,
        point=[
            [0.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [2.0, 1.0, 0.0],
            [3.0, 0.0, 0.0],
        ]
    )

    return curve


def test_curve_utils(token):
    """测试 Curve 查询和等距采样。"""
    curve = create_test_curve(token)

    curve_shape = curve_utils.get_curve_shape(
        curve
    )

    if cmds.nodeType(curve_shape) != "nurbsCurve":
        raise RuntimeError(u"Curve Shape 查询失败。")

    curve_count = curve_utils.get_curve_cv_count(
        curve
    )

    if curve_count != 4:
        raise RuntimeError(
            u"Curve CV 数量错误：{}".format(
                curve_count
            )
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

    surface_shape = surface_utils.get_surface_shape(
        surface
    )

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


def test_animation_io_utils(token):
    """测试动画 JSON 导出、清除和恢复。"""
    node = cmds.createNode(
        "transform",
        name=create_name(token, "animation_io")
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

    file_name = create_name(
        token,
        "animation"
    ) + ".json"

    file_path = os.path.join(
        tempfile.gettempdir(),
        file_name
    )

    try:
        animation_io_utils.export_animation(
            nodes=[node],
            file_path=file_path
        )

        if not os.path.isfile(file_path):
            raise RuntimeError(u"Animation JSON 没有生成。")

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

        import_result = animation_io_utils.import_animation(
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
            "animation_io_utils",
            "Animation JSON",
            test_animation_io_utils
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
