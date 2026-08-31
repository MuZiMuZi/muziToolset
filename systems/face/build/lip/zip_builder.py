# coding=utf-8
u"""
Face Zip Lip Builder
====================

PyMEL-first 的 Matrix Zip Lip 系统。
"""

from __future__ import print_function

import pymel.core as pm

from .....core import name
from .....core.undo import undo_chunk


def resolve_transform(node, label):
    if node is None:
        raise ValueError(u"{} 不能为空。".format(label))
    if isinstance(node, str):
        if not pm.objExists(node):
            raise RuntimeError(u"{} 不存在：{}".format(label, node))
        node = pm.PyNode(node)
    if node.nodeType() not in ["transform", "joint"]:
        raise TypeError(u"{} 必须是 Transform 或 Joint：{}".format(label, node))
    return node


def validate_joint(joint, label):
    joint = resolve_transform(joint, label)
    if joint.nodeType() != "joint":
        raise TypeError(u"{} 必须是 Joint：{}".format(label, joint))
    return joint


def ensure_float_attribute(
        node,
        attribute_name,
        minimum,
        maximum,
        default_value
):
    node = resolve_transform(node, u"Control")

    if not node.hasAttr(attribute_name):
        node.addAttr(
            attribute_name,
            attributeType="double",
            minValue=float(minimum),
            maxValue=float(maximum),
            defaultValue=float(default_value),
            keyable=True
        )

    plug = node.attr(attribute_name)
    plug.setKeyable(True)
    return plug


def create_name(node_type, function, index=1):
    return name.create_name(
        node_type=node_type,
        side="md",
        part="lip",
        function=function,
        index=index
    )


def insert_zip_offset_group(joint, function, index):
    joint = validate_joint(joint, u"Lip Joint")
    parent = joint.getParent()
    world_matrix = joint.getMatrix(worldSpace=True)
    group_name = create_name("grp", function, index)

    if pm.objExists(group_name):
        raise RuntimeError(u"Zip Offset Group 已存在：{}".format(group_name))

    zip_offset = pm.createNode("transform", name=group_name)
    if parent is not None:
        zip_offset.setParent(parent)
    zip_offset.setMatrix(world_matrix, worldSpace=True)
    joint.setParent(zip_offset)

    return {
        "joint": joint,
        "zip_offset": zip_offset,
        "parent": parent,
    }


def create_rest_world_matrix(zip_offset, parent, function, index):
    local_matrix = zip_offset.getMatrix(worldSpace=False)
    hold_matrix = pm.createNode(
        "holdMatrix",
        name=create_name("hold", "{}_rest".format(function), index)
    )
    hold_matrix.inMatrix.set(local_matrix)

    nodes = [hold_matrix]
    output_plug = hold_matrix.outMatrix

    if parent is not None:
        rest_mult_matrix = pm.createNode(
            "multMatrix",
            name=create_name("mult", "{}_rest_world".format(function), index)
        )
        hold_matrix.outMatrix >> rest_mult_matrix.matrixIn[0]
        parent.worldMatrix[0] >> rest_mult_matrix.matrixIn[1]
        nodes.append(rest_mult_matrix)
        output_plug = rest_mult_matrix.matrixSum

    return {
        "output": output_plug,
        "nodes": nodes,
    }


def connect_world_matrix_to_transform(
        world_matrix_plug,
        transform,
        parent,
        function,
        index
):
    nodes = []
    local_matrix_plug = world_matrix_plug

    if parent is not None:
        local_mult_matrix = pm.createNode(
            "multMatrix",
            name=create_name("mult", "{}_local".format(function), index)
        )
        world_matrix_plug >> local_mult_matrix.matrixIn[0]
        parent.worldInverseMatrix[0] >> local_mult_matrix.matrixIn[1]
        nodes.append(local_mult_matrix)
        local_matrix_plug = local_mult_matrix.matrixSum

    decompose_matrix = pm.createNode(
        "decomposeMatrix",
        name=create_name("dcmp", function, index)
    )
    local_matrix_plug >> decompose_matrix.inputMatrix
    decompose_matrix.outputTranslate >> transform.translate
    decompose_matrix.outputRotate >> transform.rotate
    nodes.append(decompose_matrix)
    return nodes


def configure_remap(remap_node, start_position, end_position):
    if end_position <= start_position:
        end_position = start_position + 0.0001
    if end_position > 1.0:
        end_position = 1.0

    remap_node.attr("value[0].value_Position").set(start_position)
    remap_node.attr("value[0].value_FloatValue").set(0.0)
    remap_node.attr("value[1].value_Position").set(end_position)
    remap_node.attr("value[1].value_FloatValue").set(1.0)
    remap_node.attr("value[0].value_Interp").set(1)
    return True


def create_zip_influence(
        left_zip_plug,
        right_zip_plug,
        pair_count,
        pair_index,
        falloff
):
    step = 1.0 / float(pair_count)
    item_number = pair_index + 1
    left_end = step * item_number
    left_start = step * (item_number - falloff)
    if left_start < 0.0:
        left_start = 0.0

    right_number = pair_count - pair_index
    right_end = step * right_number
    right_start = step * (right_number - falloff)
    if right_start < 0.0:
        right_start = 0.0

    left_remap = pm.createNode(
        "remapValue",
        name=create_name("remap", "zip_left", item_number)
    )
    right_remap = pm.createNode(
        "remapValue",
        name=create_name("remap", "zip_right", item_number)
    )
    left_zip_plug >> left_remap.inputValue
    right_zip_plug >> right_remap.inputValue
    configure_remap(left_remap, left_start, left_end)
    configure_remap(right_remap, right_start, right_end)

    add_node = pm.createNode(
        "addDoubleLinear",
        name=create_name("add", "zip_weight", item_number)
    )
    clamp_node = pm.createNode(
        "clamp",
        name=create_name("clamp", "zip_weight", item_number)
    )
    left_remap.outValue >> add_node.input1
    right_remap.outValue >> add_node.input2
    add_node.output >> clamp_node.inputR
    clamp_node.minR.set(0.0)
    clamp_node.maxR.set(1.0)

    return {
        "output": clamp_node.outputR,
        "nodes": [left_remap, right_remap, add_node, clamp_node],
    }


def build_zip_pair(
        upper_joint,
        lower_joint,
        pair_index,
        pair_count,
        zip_height_weight_plug,
        left_zip_plug,
        right_zip_plug,
        falloff
):
    item_number = pair_index + 1
    upper_insert = insert_zip_offset_group(
        upper_joint, "upper_zip_offset", item_number
    )
    lower_insert = insert_zip_offset_group(
        lower_joint, "lower_zip_offset", item_number
    )
    upper_rest = create_rest_world_matrix(
        upper_insert["zip_offset"], upper_insert["parent"], "upper", item_number
    )
    lower_rest = create_rest_world_matrix(
        lower_insert["zip_offset"], lower_insert["parent"], "lower", item_number
    )

    mid_blend = pm.createNode(
        "blendMatrix",
        name=create_name("blend", "zip_mid", item_number)
    )
    upper_rest["output"] >> mid_blend.inputMatrix
    lower_rest["output"] >> mid_blend.target[0].targetMatrix
    zip_height_weight_plug >> mid_blend.target[0].weight

    influence = create_zip_influence(
        left_zip_plug,
        right_zip_plug,
        pair_count,
        pair_index,
        falloff
    )

    upper_zip_blend = pm.createNode(
        "blendMatrix",
        name=create_name("blend", "upper_zip", item_number)
    )
    lower_zip_blend = pm.createNode(
        "blendMatrix",
        name=create_name("blend", "lower_zip", item_number)
    )

    upper_rest["output"] >> upper_zip_blend.inputMatrix
    mid_blend.outputMatrix >> upper_zip_blend.target[0].targetMatrix
    influence["output"] >> upper_zip_blend.target[0].weight
    lower_rest["output"] >> lower_zip_blend.inputMatrix
    mid_blend.outputMatrix >> lower_zip_blend.target[0].targetMatrix
    influence["output"] >> lower_zip_blend.target[0].weight

    upper_output_nodes = connect_world_matrix_to_transform(
        upper_zip_blend.outputMatrix,
        upper_insert["zip_offset"],
        upper_insert["parent"],
        "upper_zip_output",
        item_number
    )
    lower_output_nodes = connect_world_matrix_to_transform(
        lower_zip_blend.outputMatrix,
        lower_insert["zip_offset"],
        lower_insert["parent"],
        "lower_zip_output",
        item_number
    )

    utility_nodes = []
    for utility_node in upper_rest["nodes"]:
        utility_nodes.append(utility_node)
    for utility_node in lower_rest["nodes"]:
        utility_nodes.append(utility_node)
    for utility_node in influence["nodes"]:
        utility_nodes.append(utility_node)
    utility_nodes.append(mid_blend)
    utility_nodes.append(upper_zip_blend)
    utility_nodes.append(lower_zip_blend)
    for utility_node in upper_output_nodes:
        utility_nodes.append(utility_node)
    for utility_node in lower_output_nodes:
        utility_nodes.append(utility_node)

    return {
        "upper_joint": upper_insert["joint"],
        "lower_joint": lower_insert["joint"],
        "upper_zip_offset": upper_insert["zip_offset"],
        "lower_zip_offset": lower_insert["zip_offset"],
        "mid_blend": mid_blend,
        "upper_zip_blend": upper_zip_blend,
        "lower_zip_blend": lower_zip_blend,
        "zip_weight_plug": influence["output"],
        "utility_nodes": utility_nodes,
    }


def build_zip_lip(
        upper_joints,
        lower_joints,
        left_zip_control,
        right_zip_control,
        jaw_control,
        falloff=2.0
):
    u"""构建完整 Matrix Zip Lip Network。"""
    if not upper_joints:
        raise RuntimeError(u"没有给定 Upper Lip Joints。")
    if lower_joints is None:
        lower_joints = []
    if len(upper_joints) != len(lower_joints):
        raise ValueError(u"Upper / Lower Lip Joint 数量必须一致。")
    if float(falloff) <= 0.0:
        raise ValueError(u"falloff 必须大于 0。")

    resolved_upper_joints = []
    resolved_lower_joints = []
    index = 0
    while index < len(upper_joints):
        resolved_upper_joints.append(
            validate_joint(upper_joints[index], u"Upper Lip Joint")
        )
        resolved_lower_joints.append(
            validate_joint(lower_joints[index], u"Lower Lip Joint")
        )
        index += 1

    left_zip_control = resolve_transform(left_zip_control, u"Left Zip Control")
    right_zip_control = resolve_transform(right_zip_control, u"Right Zip Control")
    jaw_control = resolve_transform(jaw_control, u"Jaw Control")

    with undo_chunk("build_zip_lip"):
        left_zip_plug = ensure_float_attribute(
            left_zip_control, "zip", 0.0, 1.0, 0.0
        )
        right_zip_plug = ensure_float_attribute(
            right_zip_control, "zip", 0.0, 1.0, 0.0
        )
        zip_height_plug = ensure_float_attribute(
            jaw_control, "zip_height", 0.0, 1.0, 0.5
        )

        reverse_node_name = create_name("reverse", "zip_height", 1)
        if pm.objExists(reverse_node_name):
            raise RuntimeError(u"Zip Lip 节点已存在：{}".format(reverse_node_name))

        reverse_node = pm.createNode("reverse", name=reverse_node_name)
        zip_height_plug >> reverse_node.inputX

        pair_results = []
        utility_nodes = [reverse_node]
        pair_count = len(resolved_upper_joints)
        pair_index = 0

        while pair_index < pair_count:
            pair_result = build_zip_pair(
                upper_joint=resolved_upper_joints[pair_index],
                lower_joint=resolved_lower_joints[pair_index],
                pair_index=pair_index,
                pair_count=pair_count,
                zip_height_weight_plug=reverse_node.outputX,
                left_zip_plug=left_zip_plug,
                right_zip_plug=right_zip_plug,
                falloff=float(falloff)
            )
            pair_results.append(pair_result)
            for utility_node in pair_result["utility_nodes"]:
                utility_nodes.append(utility_node)
            pair_index += 1

        return {
            "upper_joints": resolved_upper_joints,
            "lower_joints": resolved_lower_joints,
            "left_zip_control": left_zip_control,
            "right_zip_control": right_zip_control,
            "jaw_control": jaw_control,
            "left_zip_plug": left_zip_plug,
            "right_zip_plug": right_zip_plug,
            "zip_height_plug": zip_height_plug,
            "zip_height_reverse": reverse_node,
            "pair_results": pair_results,
            "utility_nodes": utility_nodes,
        }


__all__ = [
    "build_zip_lip",
]
