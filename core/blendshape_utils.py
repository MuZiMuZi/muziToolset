# coding=utf-8
u"""
BlendShape Utils
================

Maya BlendShape / Corrective Shape 底层工具。

职责：
    1. 查找 BlendShape 和 Base Geometry；
    2. 读取真实 alias -> weight[index]；
    3. 添加 / 同名替换 Target；
    4. 从 Base Mesh 烘焙全部 Target；
    5. 批量执行 invertShape。

本模块不包含 PySide UI。
"""

from __future__ import print_function

import re

import maya.cmds as cmds


def get_short_name(node):
    """返回适合 Alias 使用的短名称。"""
    return node.split("|")[-1].replace(":", "_")


def get_mesh_shape(node):
    """返回 Transform 或 Mesh 对应的可见 Mesh Shape。"""
    if not node:
        return None

    if not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "mesh":
        return node

    shapes = cmds.listRelatives(
        node,
        shapes=True,
        noIntermediate=True,
        fullPath=True,
        type="mesh"
    )

    if shapes is None:
        shapes = []

    if shapes:
        return shapes[0]

    return None


def get_transform(node):
    """返回节点对应 Transform。"""
    if not node:
        return None

    if not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "transform":
        return node

    parents = cmds.listRelatives(
        node,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    if parents:
        return parents[0]

    return None


def find_blendshape(node):
    """从节点或历史中寻找第一个 BlendShape。"""
    if not node:
        return None

    if not cmds.objExists(node):
        return None

    if cmds.nodeType(node) == "blendShape":
        return node

    history = cmds.listHistory(node)

    if history is None:
        history = []

    blendshape_nodes = cmds.ls(
        history,
        type="blendShape"
    )

    if blendshape_nodes is None:
        blendshape_nodes = []

    if blendshape_nodes:
        return blendshape_nodes[0]

    return None


def get_base_transform(blendshape_node):
    """返回 BlendShape 第一个 Base Geometry Transform。"""
    geometries = cmds.blendShape(
        blendshape_node,
        query=True,
        geometry=True
    )

    if geometries is None:
        geometries = []

    if not geometries:
        return None

    geometry = geometries[0]
    transform = get_transform(geometry)

    if transform:
        return transform

    return geometry


def sort_targets_by_index(targets):
    """按真实 weight index 升序排序。"""
    item_count = len(targets)
    outer_index = 0

    while outer_index < item_count:
        inner_index = 0

        while inner_index < item_count - 1:
            current_index = targets[inner_index]["index"]
            next_index = targets[inner_index + 1]["index"]

            if current_index > next_index:
                temporary_target = targets[inner_index]
                targets[inner_index] = targets[inner_index + 1]
                targets[inner_index + 1] = temporary_target

            inner_index += 1

        outer_index += 1

    return targets


def get_targets(blendshape_node):
    """返回真实 alias -> weight[index] 映射。"""
    if not blendshape_node:
        return []

    if not cmds.objExists(blendshape_node):
        return []

    aliases = cmds.aliasAttr(
        blendshape_node,
        query=True
    )

    if aliases is None:
        aliases = []

    targets = []
    index = 0

    while index + 1 < len(aliases):
        alias_name = aliases[index]
        plug_name = aliases[index + 1]

        match = re.search(
            r"weight\[(\d+)\]",
            plug_name
        )

        if match:
            target_info = {
                "alias": alias_name,
                "index": int(match.group(1)),
                "plug": plug_name,
            }
            targets.append(target_info)

        index += 2

    return sort_targets_by_index(targets)


def get_next_target_index(blendshape_node):
    """返回下一个可使用的 weight index。"""
    indices = cmds.getAttr(
        blendshape_node + ".weight",
        multiIndices=True
    )

    if indices is None:
        indices = []

    if not indices:
        return 0

    return max(indices) + 1


def remove_target(
        blendshape_node,
        target_index,
        alias_name=None
):
    """删除一个 Target 的 inputTargetGroup 和可清理 weight。"""
    if alias_name:
        alias_plug = "{}.{}".format(
            blendshape_node,
            alias_name
        )

        try:
            cmds.aliasAttr(
                alias_plug,
                remove=True
            )
        except Exception:
            pass

    input_group = "{}.inputTarget[0].inputTargetGroup[{}]".format(
        blendshape_node,
        target_index
    )

    if cmds.objExists(input_group):
        try:
            cmds.removeMultiInstance(
                input_group,
                b=True
            )
        except Exception:
            pass

    weight_plug = "{}.weight[{}]".format(
        blendshape_node,
        target_index
    )

    if cmds.objExists(weight_plug):
        incoming = cmds.listConnections(
            weight_plug,
            source=True,
            destination=False,
            plugs=True
        )

        if incoming is None:
            incoming = []

        if not incoming:
            try:
                cmds.removeMultiInstance(
                    weight_plug,
                    b=True
                )
            except Exception:
                pass


def add_or_replace_target(blendshape_node, target_transform):
    """按 Target 短名称添加或同名替换 BlendShape Target。"""
    if not cmds.objExists(blendshape_node):
        raise RuntimeError(
            u"BlendShape 不存在：{}".format(blendshape_node)
        )

    target_shape = get_mesh_shape(target_transform)

    if not target_shape:
        raise RuntimeError(
            u"目标不是 Mesh：{}".format(target_transform)
        )

    base_transform = get_base_transform(blendshape_node)

    if not base_transform:
        raise RuntimeError(u"无法获取 BlendShape Base Geometry。")

    alias_name = get_short_name(target_transform)
    existing_targets = get_targets(blendshape_node)
    target_index = None

    for target_info in existing_targets:
        if target_info["alias"] == alias_name:
            target_index = target_info["index"]
            break

    if target_index is not None:
        remove_target(
            blendshape_node,
            target_index,
            alias_name=alias_name
        )
    else:
        target_index = get_next_target_index(blendshape_node)

    cmds.blendShape(
        blendshape_node,
        edit=True,
        target=(
            base_transform,
            target_index,
            target_transform,
            1.0
        )
    )

    weight_plug = "{}.weight[{}]".format(
        blendshape_node,
        target_index
    )

    # Maya 在 blendShape(edit=True, target=...) 时通常已经自动使用
    # Target Transform 名称作为 weight alias。重复调用 aliasAttr 设置同名
    # alias 会在 Maya 2023 报“对象不允许设置别名”。
    # 因此先读取当前 alias，只有名称不一致时才主动修改。
    current_alias = cmds.aliasAttr(
        weight_plug,
        query=True
    )

    if current_alias != alias_name:
        if current_alias:
            try:
                cmds.aliasAttr(
                    weight_plug,
                    remove=True
                )
            except Exception:
                pass

        cmds.aliasAttr(
            alias_name,
            weight_plug
        )

    return {
        "alias": alias_name,
        "index": target_index,
    }


def duplicate_all_targets(blendshape_node):
    """逐个激活 Target 权重，从 Base Mesh 烘焙全部 Target。"""
    base_transform = get_base_transform(blendshape_node)

    if not base_transform:
        raise RuntimeError(u"无法获取 BlendShape Base Geometry。")

    targets = get_targets(blendshape_node)

    if not targets:
        return []

    original_values = {}

    for target_info in targets:
        weight_plug = "{}.weight[{}]".format(
            blendshape_node,
            target_info["index"]
        )
        original_values[target_info["index"]] = cmds.getAttr(weight_plug)

    copies = []

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziDuplicateBlendShapeTargets"
    )

    try:
        for target_info in targets:
            for zero_target in targets:
                zero_plug = "{}.weight[{}]".format(
                    blendshape_node,
                    zero_target["index"]
                )
                cmds.setAttr(zero_plug, 0.0)

            active_plug = "{}.weight[{}]".format(
                blendshape_node,
                target_info["index"]
            )
            cmds.setAttr(active_plug, 1.0)

            duplicate_name = target_info["alias"]

            if cmds.objExists(duplicate_name):
                duplicate_name = "{}_copy".format(duplicate_name)

            duplicate = cmds.duplicate(
                base_transform,
                name=duplicate_name,
                returnRootsOnly=True
            )[0]

            cmds.delete(
                duplicate,
                constructionHistory=True
            )
            copies.append(duplicate)

    finally:
        for target_info in targets:
            restore_plug = "{}.weight[{}]".format(
                blendshape_node,
                target_info["index"]
            )
            restore_value = original_values.get(
                target_info["index"],
                0.0
            )
            cmds.setAttr(
                restore_plug,
                restore_value
            )

        cmds.undoInfo(closeChunk=True)

    return copies


def get_vertex_count(node):
    """返回 Mesh 顶点数量。"""
    shape = get_mesh_shape(node)

    if not shape:
        return None

    return cmds.polyEvaluate(
        shape,
        vertex=True
    )


def invert_shapes(base_mesh, corrective_meshes):
    """批量执行 Maya invertShape。"""
    if not get_mesh_shape(base_mesh):
        raise RuntimeError(
            u"基础模型不是有效 Mesh：{}".format(base_mesh)
        )

    base_vertex_count = get_vertex_count(base_mesh)
    results = []

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziInvertShapes"
    )

    try:
        for corrective in corrective_meshes:
            if not corrective:
                continue

            if not cmds.objExists(corrective):
                continue

            if not get_mesh_shape(corrective):
                cmds.warning(
                    u"跳过非 Mesh：{}".format(corrective)
                )
                continue

            corrective_vertex_count = get_vertex_count(corrective)

            if corrective_vertex_count != base_vertex_count:
                cmds.warning(
                    u"拓扑点数不一致，跳过 {}：base={} / corrective={}".format(
                        corrective,
                        base_vertex_count,
                        corrective_vertex_count
                    )
                )
                continue

            inverted = cmds.invertShape(
                base_mesh,
                corrective
            )

            if isinstance(inverted, (list, tuple)):
                inverted = inverted[0]

            target_name = "{}_invert_geo".format(
                get_short_name(corrective)
            )

            if cmds.objExists(target_name):
                suffix = 1

                while cmds.objExists(
                        "{}_{:03d}".format(
                            target_name,
                            suffix
                        )
                ):
                    suffix += 1

                target_name = "{}_{:03d}".format(
                    target_name,
                    suffix
                )

            inverted = cmds.rename(
                inverted,
                target_name
            )
            results.append(inverted)

    finally:
        cmds.undoInfo(closeChunk=True)

    return results


__all__ = [
    "get_short_name",
    "get_mesh_shape",
    "get_transform",
    "find_blendshape",
    "get_base_transform",
    "get_targets",
    "get_next_target_index",
    "remove_target",
    "add_or_replace_target",
    "duplicate_all_targets",
    "get_vertex_count",
    "invert_shapes",
]
