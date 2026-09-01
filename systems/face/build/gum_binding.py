# coding=utf-8
u"""
Gum Binding
===========

Face Teeth Component 使用的 Gum 自动刚性权重算法。

职责
----
本模块只处理一个明确场景：

    一个 Gum Transform
        -> 一个有效 Mesh Shape
        -> 两个或多个断开的 Connected Mesh Shell
        -> 每个 Shell 完整归属 Upper 或 Lower Teeth Joint

算法
----
1. 使用 Maya API 读取 Mesh Vertex 邻接关系；
2. 用显式 BFS 把 Vertex 划分成 Connected Shell；
3. 计算每个 Shell 的世界空间中心；
4. 比较 Shell Center 到 Upper / Lower Reference 的距离；
5. 整个 Shell 赋给更近的一侧；
6. 创建双 Influence SkinCluster，并把每个 Shell 写成 1.0 / 0.0 刚性权重。

边界
----
- 不处理单一连通 Gum Mesh 的自动切分；
- 不做 Smooth Bind 猜权重；
- 不覆盖已有 SkinCluster；
- 不负责创建 Teeth Joint / Controller；
- 不属于 Core，因为这是明确的 Face Rig 业务规则。
"""

from __future__ import print_function

import maya.api.OpenMaya as om
import maya.cmds as cmds

from ....core import skin_utils
from ....core import transform_utils


# =============================================================================
# Mesh Helper
# =============================================================================


def _get_mesh_shape(model):
    u"""返回 Gum Model 唯一的非 Intermediate Mesh Shape。"""
    mesh_shapes = cmds.listRelatives(
        model,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="mesh"
    )

    if mesh_shapes is None:
        mesh_shapes = []

    if len(mesh_shapes) != 1:
        raise RuntimeError(
            u"Gum Model 必须包含且只包含一个有效 Mesh Shape：{} | shapes={}".format(
                model,
                len(mesh_shapes)
            )
        )

    return mesh_shapes[0]


def _distance_squared(point_a, point_b):
    u"""返回两个三维点之间的平方距离。"""
    delta_x = point_a[0] - point_b[0]
    delta_y = point_a[1] - point_b[1]
    delta_z = point_a[2] - point_b[2]

    return (
        delta_x * delta_x +
        delta_y * delta_y +
        delta_z * delta_z
    )


def _get_mesh_shell_data(model):
    u"""使用 Maya API 读取模型 Connected Vertex Shell 及世界空间中心。"""
    mesh_shape = _get_mesh_shape(
        model
    )

    selection = om.MSelectionList()
    selection.add(
        mesh_shape
    )
    mesh_path = selection.getDagPath(
        0
    )

    mesh_function = om.MFnMesh(
        mesh_path
    )
    world_points = mesh_function.getPoints(
        om.MSpace.kWorld
    )

    # -------------------------------------------------------------------------
    # 步骤 1：建立完整 Vertex 邻接表。
    # -------------------------------------------------------------------------
    adjacency = {}
    vertex_iterator = om.MItMeshVertex(
        mesh_path
    )

    while not vertex_iterator.isDone():
        vertex_index = vertex_iterator.index()
        connected_vertices = vertex_iterator.getConnectedVertices()
        adjacency[vertex_index] = []

        for connected_vertex in connected_vertices:
            adjacency[vertex_index].append(
                connected_vertex
            )

        vertex_iterator.next()

    # -------------------------------------------------------------------------
    # 步骤 2：显式 BFS 划分 Connected Shell。
    # -------------------------------------------------------------------------
    visited_vertices = set()
    shell_data = []
    vertex_count = mesh_function.numVertices
    vertex_index = 0

    while vertex_index < vertex_count:
        if vertex_index in visited_vertices:
            vertex_index += 1
            continue

        pending_vertices = [
            vertex_index
        ]
        shell_vertices = []

        while pending_vertices:
            current_vertex = pending_vertices.pop()

            if current_vertex in visited_vertices:
                continue

            visited_vertices.add(
                current_vertex
            )
            shell_vertices.append(
                current_vertex
            )

            connected_vertices = adjacency.get(
                current_vertex,
                []
            )

            for connected_vertex in connected_vertices:
                if connected_vertex in visited_vertices:
                    continue

                pending_vertices.append(
                    connected_vertex
                )

        # ---------------------------------------------------------------------
        # 步骤 3：计算当前 Shell 的世界空间中心。
        # ---------------------------------------------------------------------
        center_x = 0.0
        center_y = 0.0
        center_z = 0.0

        for shell_vertex in shell_vertices:
            point = world_points[shell_vertex]
            center_x += point.x
            center_y += point.y
            center_z += point.z

        shell_vertex_count = len(
            shell_vertices
        )

        if shell_vertex_count > 0:
            shell_center = [
                center_x / shell_vertex_count,
                center_y / shell_vertex_count,
                center_z / shell_vertex_count,
            ]

            shell_data.append({
                "vertices": shell_vertices,
                "center": shell_center,
                "side": None,
            })

        vertex_index += 1

    return shell_data


# =============================================================================
# Public - Shell Classification
# =============================================================================


def prepare_gum_shell_data(
        model,
        upper_reference,
        lower_reference
):
    u"""
    把 Gum Connected Shell 预分类为 Upper / Lower。

    Args:
        model (str | None):
            Step 01 保存的 Gum Model Transform；为空时返回空列表。
        upper_reference (str):
            Upper Teeth Guide 或其它用于代表上牙床位置的 Transform。
        lower_reference (str):
            Lower Teeth Guide 或其它用于代表下牙床位置的 Transform。

    Returns:
        list[dict]:
            每个字典包含 vertices、center 和 side。side 为 upper 或 lower。

    Raises:
        RuntimeError:
            Gum 不是单一有效 Mesh、少于两个 Connected Shell，或无法同时分类出上下两组时抛出。
    """
    if not model:
        return []

    shell_data = _get_mesh_shell_data(
        model
    )

    if len(shell_data) < 2:
        raise RuntimeError(
            u"Gum Model 至少需要两个断开的 Mesh Shell 才能自动区分上下牙龈：{}".format(
                model
            )
        )

    upper_position = transform_utils.get_world_translation(
        upper_reference
    )
    lower_position = transform_utils.get_world_translation(
        lower_reference
    )

    upper_shell_count = 0
    lower_shell_count = 0

    for shell in shell_data:
        shell_center = shell["center"]

        upper_distance = _distance_squared(
            shell_center,
            upper_position
        )
        lower_distance = _distance_squared(
            shell_center,
            lower_position
        )

        if upper_distance <= lower_distance:
            shell["side"] = "upper"
            upper_shell_count += 1
        else:
            shell["side"] = "lower"
            lower_shell_count += 1

    if upper_shell_count == 0 or lower_shell_count == 0:
        raise RuntimeError(
            u"Gum Shell 自动分类失败，必须至少存在一组 Upper 和一组 Lower Shell。"
        )

    return shell_data


# =============================================================================
# Public - Skin
# =============================================================================


def create_gum_skin_cluster(
        model,
        upper_joint,
        lower_joint,
        skin_name,
        shell_data
):
    u"""
    创建双 Influence Gum SkinCluster，并把每个 Connected Shell 刚性分配给一侧。

    Args:
        model (str | None):
            需要绑定的 Gum Model；为空时返回 None。
        upper_joint (str):
            Upper Teeth Bind Joint。
        lower_joint (str):
            Lower Teeth Bind Joint。
        skin_name (str):
            新 Gum SkinCluster 的确定性名称。
        shell_data (list[dict]):
            prepare_gum_shell_data() 返回的 Shell 分类结果。

    Returns:
        str | None:
            创建完成的 SkinCluster 名称；没有 Gum Model 时返回 None。

    Raises:
        RuntimeError:
            缺少 Shell 数据、模型已有 SkinCluster、创建失败或存在未分类 Shell 时抛出。
    """
    if not model:
        return None

    if not shell_data:
        raise RuntimeError(
            u"没有可用于 Gum 绑定的 Shell 数据。"
        )

    existing_skin_cluster = skin_utils.find_skin_cluster(
        model
    )

    if existing_skin_cluster:
        raise RuntimeError(
            u"Gum Model 已经存在 SkinCluster：{}".format(
                existing_skin_cluster
            )
        )

    skin_result = cmds.skinCluster(
        [
            upper_joint,
            lower_joint,
        ],
        model,
        name=skin_name,
        toSelectedBones=True,
        bindMethod=0,
        skinMethod=0,
        normalizeWeights=1,
        maximumInfluences=1,
        obeyMaxInfluences=True
    )

    if not skin_result:
        raise RuntimeError(
            u"创建 Gum SkinCluster 失败：{}".format(
                model
            )
        )

    skin_cluster = skin_result[0]

    for shell in shell_data:
        vertex_components = []

        for vertex_index in shell["vertices"]:
            vertex_components.append(
                "{}.vtx[{}]".format(
                    model,
                    vertex_index
                )
            )

        if shell["side"] == "upper":
            transform_values = [
                (upper_joint, 1.0),
                (lower_joint, 0.0),
            ]
        elif shell["side"] == "lower":
            transform_values = [
                (upper_joint, 0.0),
                (lower_joint, 1.0),
            ]
        else:
            raise RuntimeError(
                u"Gum Shell 没有 Upper / Lower 分类结果。"
            )

        cmds.skinPercent(
            skin_cluster,
            vertex_components,
            transformValue=transform_values,
            normalize=True
        )

    return skin_cluster


__all__ = [
    "prepare_gum_shell_data",
    "create_gum_skin_cluster",
]
