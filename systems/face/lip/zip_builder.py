# coding=utf-8
u"""
Face Zip Lip Builder
====================

Matrix 驱动 Zip Lip 系统。

设计目标：
    1. 上下嘴唇 Joint 数量一致，并按相同顺序成对；
    2. 左 / 右嘴角控制器分别提供 zip 0~1；
    3. Jaw 控制器提供 zipHeight 0~1；
    4. 每对上下嘴唇使用动态 Rest World Matrix 计算闭合中间矩阵；
    5. 每个 Joint 上方插入独立 Zip Offset Group；
    6. Zip Offset 使用 blendMatrix 混合 Rest Matrix 和 Mid Matrix；
    7. 不直接修改 Joint translateY，不把表演微调硬编码进 Zip 系统。

重要边界：
    - Transform 输入和 Matrix 读写统一复用 core.transform_utils；
    - Joint 类型检查统一复用 core.joint_utils；
    - Attribute 创建统一复用 core.attr_utils；
    - DAG Parent / Parent Query 统一复用 core.hierarchy_utils；
    - DG Node 创建统一复用 core.scene_utils；
    - Plug Connection 统一复用 core.connection_utils；
    - Undo Chunk 统一复用 core.scene_utils；
    - Zip Influence、Rest Matrix、Mid Matrix 和 Pairing 算法保留在本 System。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import attr_utils
from ....core import connection_utils
from ....core import hierarchy_utils
from ....core import joint_utils
from ....core import name_utils
from ....core import scene_utils
from ....core import transform_utils


# =============================================================================
# Validate / Attribute
# =============================================================================

def validate_joint(joint, label):
    u"""检查输入节点必须是 Maya Joint。"""
    try:
        # 使用 Joint Core 统一检查节点存在性和 Joint 类型。
        joint_utils.Joint._validate_joint(
            joint
        )
    except RuntimeError as error:
        raise RuntimeError(
            u"{}无效：{}".format(
                label,
                error
            )
        )

    return True


def ensure_float_attribute(
        node,
        attribute,
        minimum,
        maximum,
        default_value
):
    u"""创建或复用一个 Keyable Float Attribute。"""
    # 直接使用 Transform Core 检查 Attribute 所在节点。
    transform_utils.validate_transform(
        node
    )

    # 使用统一 Attr Core 查询 / 创建属性；已有属性不会覆盖当前动画值。
    node_attr = attr_utils.Attr(
        node
    )

    if not node_attr.attr_exists(
            attribute
    ):
        node_attr.add_attr(
            attribute,
            attr_type="double",
            lock=False,
            hide=False,
            default_value=default_value,
            min_value=minimum,
            max_value=maximum
        )

    return "{}.{}".format(
        node,
        attribute
    )


# =============================================================================
# Naming
# =============================================================================

def create_name(
        node_type,
        function,
        index=1
):
    u"""创建 Zip Lip 系统标准名称。"""
    # 使用项目统一五段式 Name API 创建中线 Lip 节点名称。
    return name_utils.Name.create_name(
        node_type=node_type,
        side="md",
        part="lip",
        function=function,
        index=index
    )


# =============================================================================
# Matrix Helpers
# =============================================================================

def get_parent(node):
    u"""
    返回直接 Parent，没有则返回 None。

    保留旧入口，实际 Parent Query 统一由 hierarchy_utils 维护。
    """
    # 使用 Hierarchy Core 获取直接 Parent Long Path。
    return hierarchy_utils.Hierarchy.get_parent(
        node,
        full_path=True
    )


def insert_zip_offset_group(
        joint,
        function,
        index
):
    u"""
    在 Joint 上方插入 Zip Offset Group，并保持 Joint 当前世界姿态。
    """
    # 记录 Joint 原 Parent，Zip Offset 创建后需要插回同一 DAG 层级。
    parent = get_parent(
        joint
    )

    # 使用 Transform Core 保存 Joint 当前完整 World Matrix。
    world_matrix = transform_utils.get_world_matrix(
        joint
    )

    # 生成当前 Joint Pair 对应的 Zip Offset Group 名称。
    group_name = create_name(
        "grp",
        function,
        index
    )

    if cmds.objExists(group_name):
        raise RuntimeError(
            u"Zip Offset Group 已经存在：{}".format(
                group_name
            )
        )

    # 使用 Scene Core 创建新的 Zip Offset Transform。
    zip_offset = scene_utils.create_node(
        "transform",
        group_name
    )

    if parent is not None:
        # 把 Zip Offset 放回 Joint 原 Parent，保留原来的 DAG 结构。
        zip_offset = hierarchy_utils.Hierarchy.parent(
            zip_offset,
            parent
        )

    # 使用 Transform Core 恢复 Joint 原世界矩阵到 Zip Offset。
    transform_utils.set_world_matrix(
        zip_offset,
        world_matrix
    )

    # 把 Joint 放入 Zip Offset，形成独立的 Zip 驱动层。
    joint = hierarchy_utils.Hierarchy.parent(
        joint,
        zip_offset
    )

    return {
        "joint": joint,
        "zip_offset": zip_offset,
        "parent": parent,
    }


def create_rest_world_matrix(
        zip_offset,
        parent,
        function,
        index
):
    u"""
    保存 Zip Offset 的 Rest Local Matrix，并实时组合 Parent World Matrix。
    """
    local_matrix = cmds.xform(
        zip_offset,
        query=True,
        objectSpace=True,
        matrix=True
    )

    # 创建 holdMatrix 保存 Zip Offset 构建时的 Rest Local Matrix。
    hold_matrix = scene_utils.create_node(
        "holdMatrix",
        create_name(
            "hold",
            "{}_rest".format(function),
            index
        )
    )

    cmds.setAttr(
        hold_matrix + ".inMatrix",
        *local_matrix,
        type="matrix"
    )

    nodes = [
        hold_matrix,
    ]

    output_plug = hold_matrix + ".outMatrix"

    if parent is not None:
        # 创建 multMatrix，把固定 Rest Local Matrix 实时组合到 Parent World Space。
        rest_mult_matrix = scene_utils.create_node(
            "multMatrix",
            create_name(
                "mult",
                "{}_rest_world".format(function),
                index
            )
        )

        # 把 Rest Local Matrix 接入 Mult Matrix 第一项。
        connection_utils.connect_plugs(
            hold_matrix + ".outMatrix",
            rest_mult_matrix + ".matrixIn[0]",
            force=True
        )

        # 把 Parent World Matrix 作为第二项，得到动态 Rest World Matrix。
        connection_utils.connect_plugs(
            parent + ".worldMatrix[0]",
            rest_mult_matrix + ".matrixIn[1]",
            force=True
        )

        nodes.append(rest_mult_matrix)
        output_plug = rest_mult_matrix + ".matrixSum"

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
    u"""把 World Matrix 安全转换到 Transform Parent Local Space。"""
    nodes = []
    local_matrix_plug = world_matrix_plug

    if parent is not None:
        # 创建 multMatrix 把目标 World Matrix 转换到当前 Parent Local Space。
        local_mult_matrix = scene_utils.create_node(
            "multMatrix",
            create_name(
                "mult",
                "{}_local".format(function),
                index
            )
        )

        # 输入需要应用到 Transform 的目标 World Matrix。
        connection_utils.connect_plugs(
            world_matrix_plug,
            local_mult_matrix + ".matrixIn[0]",
            force=True
        )

        # 乘以 Parent World Inverse Matrix 得到 Transform Local Matrix。
        connection_utils.connect_plugs(
            parent + ".worldInverseMatrix[0]",
            local_mult_matrix + ".matrixIn[1]",
            force=True
        )

        nodes.append(local_mult_matrix)
        local_matrix_plug = local_mult_matrix + ".matrixSum"

    # 创建 decomposeMatrix，把最终 Local Matrix 拆成 Translate / Rotate。
    decompose_matrix = scene_utils.create_node(
        "decomposeMatrix",
        create_name(
            "dcmp",
            function,
            index
        )
    )

    # 把最终 Local Matrix 输入 decomposeMatrix。
    connection_utils.connect_plugs(
        local_matrix_plug,
        decompose_matrix + ".inputMatrix",
        force=True
    )

    # 用分解出的 Translation 驱动 Zip Offset。
    connection_utils.connect_plugs(
        decompose_matrix + ".outputTranslate",
        transform + ".translate",
        force=True
    )

    # 用分解出的 Rotation 驱动 Zip Offset。
    connection_utils.connect_plugs(
        decompose_matrix + ".outputRotate",
        transform + ".rotate",
        force=True
    )

    nodes.append(decompose_matrix)

    return nodes


# =============================================================================
# Zip Influence
# =============================================================================

def configure_remap(
        remap_node,
        start_position,
        end_position
):
    u"""配置 0~1 的线性 Remap。"""
    if end_position <= start_position:
        end_position = start_position + 0.0001

    if end_position > 1.0:
        end_position = 1.0

    cmds.setAttr(
        remap_node + ".value[0].value_Position",
        start_position
    )
    cmds.setAttr(
        remap_node + ".value[0].value_FloatValue",
        0.0
    )
    cmds.setAttr(
        remap_node + ".value[1].value_Position",
        end_position
    )
    cmds.setAttr(
        remap_node + ".value[1].value_FloatValue",
        1.0
    )
    cmds.setAttr(
        remap_node + ".value[0].value_Interp",
        1
    )


def create_zip_influence(
        left_zip_plug,
        right_zip_plug,
        pair_count,
        pair_index,
        falloff
):
    u"""创建一对嘴唇 Joint 的左右 Zip Influence 0~1。"""
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

    # 创建左右两条 remapValue，用于计算 Zip 从嘴角向中间传播的权重。
    left_remap = scene_utils.create_node(
        "remapValue",
        create_name(
            "remap",
            "zip_left",
            item_number
        )
    )
    right_remap = scene_utils.create_node(
        "remapValue",
        create_name(
            "remap",
            "zip_right",
            item_number
        )
    )

    # 把左右嘴角 Zip 属性分别输入对应 Remap。
    connection_utils.connect_plugs(
        left_zip_plug,
        left_remap + ".inputValue",
        force=True
    )
    connection_utils.connect_plugs(
        right_zip_plug,
        right_remap + ".inputValue",
        force=True
    )

    # 根据当前 Pair 的位置配置左侧 Zip 传播区间。
    configure_remap(
        left_remap,
        left_start,
        left_end
    )

    # 根据镜像位置配置右侧 Zip 传播区间。
    configure_remap(
        right_remap,
        right_start,
        right_end
    )

    # 创建 Add Node，把左右 Zip Influence 合并。
    add_node = scene_utils.create_node(
        "addDoubleLinear",
        create_name(
            "add",
            "zip_weight",
            item_number
        )
    )

    # 创建 Clamp，保证左右 Influence 叠加后最终权重仍在 0~1。
    clamp_node = scene_utils.create_node(
        "clamp",
        create_name(
            "clamp",
            "zip_weight",
            item_number
        )
    )

    # 合并左侧 Remap 输出。
    connection_utils.connect_plugs(
        left_remap + ".outValue",
        add_node + ".input1",
        force=True
    )

    # 合并右侧 Remap 输出。
    connection_utils.connect_plugs(
        right_remap + ".outValue",
        add_node + ".input2",
        force=True
    )

    # 把合并结果输入 Clamp。
    connection_utils.connect_plugs(
        add_node + ".output",
        clamp_node + ".inputR",
        force=True
    )

    cmds.setAttr(
        clamp_node + ".minR",
        0.0
    )
    cmds.setAttr(
        clamp_node + ".maxR",
        1.0
    )

    return {
        "output": clamp_node + ".outputR",
        "nodes": [
            left_remap,
            right_remap,
            add_node,
            clamp_node,
        ],
    }


# =============================================================================
# Pair Build
# =============================================================================

def build_zip_pair(
        upper_joint,
        lower_joint,
        pair_index,
        pair_count,
        zip_height_reverse_plug,
        left_zip_plug,
        right_zip_plug,
        falloff
):
    u"""构建一对 Upper / Lower Lip Joint 的 Matrix Zip 网络。"""
    item_number = pair_index + 1

    # 在 Upper Joint 上方插入独立 Zip Offset 层，隔离闭合驱动和 Joint Local 动画。
    upper_insert = insert_zip_offset_group(
        upper_joint,
        "upper_zip_offset",
        item_number
    )

    # 在 Lower Joint 上方插入独立 Zip Offset 层。
    lower_insert = insert_zip_offset_group(
        lower_joint,
        "lower_zip_offset",
        item_number
    )

    # 创建 Upper Zip Offset 的动态 Rest World Matrix。
    upper_rest = create_rest_world_matrix(
        upper_insert["zip_offset"],
        upper_insert["parent"],
        "upper",
        item_number
    )

    # 创建 Lower Zip Offset 的动态 Rest World Matrix。
    lower_rest = create_rest_world_matrix(
        lower_insert["zip_offset"],
        lower_insert["parent"],
        "lower",
        item_number
    )

    # 创建 Mid Blend，在 Upper / Lower Rest Matrix 之间计算闭合目标矩阵。
    mid_blend = scene_utils.create_node(
        "blendMatrix",
        create_name(
            "blend",
            "zip_mid",
            item_number
        )
    )

    # Upper Rest 作为 Mid Blend 起始矩阵。
    connection_utils.connect_plugs(
        upper_rest["output"],
        mid_blend + ".inputMatrix",
        force=True
    )

    # Lower Rest 作为 Mid Blend Target Matrix。
    connection_utils.connect_plugs(
        lower_rest["output"],
        mid_blend + ".target[0].targetMatrix",
        force=True
    )

    # Zip Height Reverse 决定闭合目标在 Upper / Lower 之间的位置。
    connection_utils.connect_plugs(
        zip_height_reverse_plug,
        mid_blend + ".target[0].weight",
        force=True
    )

    # 创建当前 Pair 的左右 Zip 传播权重。
    influence = create_zip_influence(
        left_zip_plug,
        right_zip_plug,
        pair_count,
        pair_index,
        falloff
    )

    # 创建 Upper / Lower 最终 Zip Blend Matrix。
    upper_zip_blend = scene_utils.create_node(
        "blendMatrix",
        create_name(
            "blend",
            "upper_zip",
            item_number
        )
    )
    lower_zip_blend = scene_utils.create_node(
        "blendMatrix",
        create_name(
            "blend",
            "lower_zip",
            item_number
        )
    )

    # Upper 从自身 Rest Matrix 混合到共同 Mid Matrix。
    connection_utils.connect_plugs(
        upper_rest["output"],
        upper_zip_blend + ".inputMatrix",
        force=True
    )
    connection_utils.connect_plugs(
        mid_blend + ".outputMatrix",
        upper_zip_blend + ".target[0].targetMatrix",
        force=True
    )
    connection_utils.connect_plugs(
        influence["output"],
        upper_zip_blend + ".target[0].weight",
        force=True
    )

    # Lower 从自身 Rest Matrix 混合到同一个 Mid Matrix。
    connection_utils.connect_plugs(
        lower_rest["output"],
        lower_zip_blend + ".inputMatrix",
        force=True
    )
    connection_utils.connect_plugs(
        mid_blend + ".outputMatrix",
        lower_zip_blend + ".target[0].targetMatrix",
        force=True
    )
    connection_utils.connect_plugs(
        influence["output"],
        lower_zip_blend + ".target[0].weight",
        force=True
    )

    # 把 Upper 最终 World Matrix 转成 Zip Offset Parent Local Space 并驱动 Transform。
    upper_output_nodes = connect_world_matrix_to_transform(
        upper_zip_blend + ".outputMatrix",
        upper_insert["zip_offset"],
        upper_insert["parent"],
        "upper_zip_output",
        item_number
    )

    # 把 Lower 最终 World Matrix 转成 Zip Offset Parent Local Space 并驱动 Transform。
    lower_output_nodes = connect_world_matrix_to_transform(
        lower_zip_blend + ".outputMatrix",
        lower_insert["zip_offset"],
        lower_insert["parent"],
        "lower_zip_output",
        item_number
    )

    utility_nodes = []

    for node in upper_rest["nodes"]:
        utility_nodes.append(node)

    for node in lower_rest["nodes"]:
        utility_nodes.append(node)

    for node in influence["nodes"]:
        utility_nodes.append(node)

    utility_nodes.append(mid_blend)
    utility_nodes.append(upper_zip_blend)
    utility_nodes.append(lower_zip_blend)

    for node in upper_output_nodes:
        utility_nodes.append(node)

    for node in lower_output_nodes:
        utility_nodes.append(node)

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


# =============================================================================
# Public Build
# =============================================================================

@scene_utils.undo_chunk
def build_zip_lip(
        upper_joints,
        lower_joints,
        left_zip_control,
        right_zip_control,
        jaw_control,
        zip_height=0.5,
        falloff=3,
        utility_parent=None
):
    u"""创建 Matrix Zip Lip。"""
    if upper_joints is None:
        upper_joints = []

    if lower_joints is None:
        lower_joints = []

    if len(upper_joints) != len(lower_joints):
        raise RuntimeError(
            u"Upper / Lower Lip Joint 数量必须一致：{} / {}".format(
                len(upper_joints),
                len(lower_joints)
            )
        )

    if len(upper_joints) < 2:
        raise RuntimeError(
            u"Zip Lip 至少需要两对 Upper / Lower Joint。"
        )

    index = 0

    # 逐对检查 Upper / Lower 输入确实是有效 Joint。
    while index < len(upper_joints):
        validate_joint(
            upper_joints[index],
            u"Upper Lip Joint"
        )
        validate_joint(
            lower_joints[index],
            u"Lower Lip Joint"
        )
        index += 1

    # 直接使用 Transform Core 检查左右嘴角 Zip Controller。
    transform_utils.validate_transform(
        left_zip_control
    )
    transform_utils.validate_transform(
        right_zip_control
    )

    # 直接使用 Transform Core 检查 Jaw / Mouth 主 Controller。
    transform_utils.validate_transform(
        jaw_control
    )

    if utility_parent is not None:
        # 如果指定 Utility Parent，直接使用 Transform Core 验证 DAG 类型。
        transform_utils.validate_transform(
            utility_parent
        )

    zip_height = float(zip_height)

    if zip_height < 0.0 or zip_height > 1.0:
        raise ValueError(u"zip_height 必须在 0~1 范围内。")

    falloff = int(falloff)

    if falloff < 1:
        raise ValueError(u"falloff 必须大于或等于 1。")

    # 生成 Zip Lip Utility Nodes 顶层 Group 名称。
    node_group_name = create_name(
        "grp",
        "zip_nodes",
        1
    )

    if cmds.objExists(node_group_name):
        raise RuntimeError(
            u"Zip Lip 系统已经存在：{}".format(
                node_group_name
            )
        )

    # 在左右嘴角 Controller 上创建或复用 Zip 属性。
    left_zip_plug = ensure_float_attribute(
        left_zip_control,
        "zip",
        0.0,
        1.0,
        0.0
    )
    right_zip_plug = ensure_float_attribute(
        right_zip_control,
        "zip",
        0.0,
        1.0,
        0.0
    )

    # 在 Jaw Controller 上创建或复用 Zip Height 属性。
    zip_height_plug = ensure_float_attribute(
        jaw_control,
        "zipHeight",
        0.0,
        1.0,
        zip_height
    )

    created_zip_offsets = []
    node_group = None

    try:
        # 使用 Scene Core 创建并隐藏 Zip Lip Utility Transform Group。
        node_group = scene_utils.create_node(
            "transform",
            node_group_name,
            parent=utility_parent
        )

        cmds.setAttr(
            node_group + ".visibility",
            0
        )

        # 创建 Reverse Node，把 zipHeight 转换成 Mid Blend 使用的 Lower 权重。
        height_reverse = scene_utils.create_node(
            "reverse",
            create_name(
                "rvs",
                "zip_height",
                1
            )
        )

        # 把 Jaw zipHeight 输入 Reverse Node。
        connection_utils.connect_plugs(
            zip_height_plug,
            height_reverse + ".inputX",
            force=True
        )

        pairs = []
        utility_nodes = [
            height_reverse,
        ]

        pair_index = 0

        # 按 Upper / Lower Joint 的配对顺序逐个建立 Matrix Zip Pair。
        while pair_index < len(upper_joints):
            pair_result = build_zip_pair(
                upper_joint=upper_joints[pair_index],
                lower_joint=lower_joints[pair_index],
                pair_index=pair_index,
                pair_count=len(upper_joints),
                zip_height_reverse_plug=height_reverse + ".outputX",
                left_zip_plug=left_zip_plug,
                right_zip_plug=right_zip_plug,
                falloff=falloff
            )

            pairs.append(pair_result)
            created_zip_offsets.append(
                pair_result["upper_zip_offset"]
            )
            created_zip_offsets.append(
                pair_result["lower_zip_offset"]
            )

            for utility_node in pair_result["utility_nodes"]:
                utility_nodes.append(utility_node)

            pair_index += 1

        # 只有 DAG Transform Utility 才需要 Parent 到隐藏 Group；DG 节点不参与 DAG Parent。
        for utility_node in utility_nodes:
            if cmds.nodeType(utility_node) != "transform":
                continue

            parent = hierarchy_utils.Hierarchy.get_parent(
                utility_node,
                full_path=True
            )

            if parent:
                continue

            hierarchy_utils.Hierarchy.parent(
                utility_node,
                node_group
            )

        return {
            "node_group": node_group,
            "left_zip_plug": left_zip_plug,
            "right_zip_plug": right_zip_plug,
            "zip_height_plug": zip_height_plug,
            "height_reverse": height_reverse,
            "pairs": pairs,
            "utility_nodes": utility_nodes,
            "zip_offsets": created_zip_offsets,
        }

    except Exception:
        # 构建失败时先删除 Utility Group，清理所有被 Parent 到其中的 DAG 节点。
        if node_group is not None:
            if cmds.objExists(node_group):
                cmds.delete(
                    node_group
                )

        # 把已经插入 Zip Offset 的 Joint 恢复到原 Parent，再删除临时 Offset Group。
        for zip_offset in created_zip_offsets:
            if not cmds.objExists(zip_offset):
                continue

            children = hierarchy_utils.Hierarchy.get_children(
                zip_offset,
                node_type="joint",
                full_path=True
            )

            parent = hierarchy_utils.Hierarchy.get_parent(
                zip_offset,
                full_path=True
            )

            for child_joint in children:
                if parent is None:
                    cmds.parent(
                        child_joint,
                        world=True,
                        absolute=True
                    )
                else:
                    hierarchy_utils.Hierarchy.parent(
                        child_joint,
                        parent
                    )

            if cmds.objExists(zip_offset):
                cmds.delete(
                    zip_offset
                )

        raise


__all__ = [
    "build_zip_lip",
]
