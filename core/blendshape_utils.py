# coding=utf-8
u"""
BlendShape Utils
================

Maya BlendShape / Corrective Shape 领域的通用底层工具。

模块职责
--------
这个模块负责 BlendShape 的基础查询、Target 管理、Target 烘焙和 Corrective Shape
反算。它不包含 PySide UI，也不负责面部表情系统的完整控制器逻辑。

当前公开方法
------------
名称 / Mesh 查询：
    get_short_name(node)
        获取适合作为 BlendShape Alias 的短名称。

    get_mesh_shape(node)
        获取 Transform 或 Mesh 对应的可见 Mesh Shape。

    get_transform(node)
        获取 Shape 对应 Transform；Transform 输入则直接返回。

BlendShape 查询：
    find_blendshape(node)
        从 BlendShape 本身或节点 History 中查找第一个 BlendShape。

    get_base_transform(blendshape_node)
        获取 BlendShape 第一个 Base Geometry Transform。

    sort_targets_by_index(targets)
        按真实 weight[index] 对 Target 数据排序。

    get_targets(blendshape_node)
        读取 Maya 真实 alias -> weight[index] 映射。

    get_next_target_index(blendshape_node)
        获取下一个可用 BlendShape Weight Index。

Target 管理：
    remove_target(blendshape_node, target_index, alias_name=None)
        删除指定 Target 的 Alias / inputTargetGroup / 可清理 Weight Element。

    add_or_replace_target(blendshape_node, target_transform)
        按 Target 短名称新增或同名替换 Target。

    duplicate_all_targets(blendshape_node)
        逐 Target 激活权重，从 Base Geometry 烘焙所有 Target Mesh。

Corrective：
    get_vertex_count(node)
        获取 Mesh 顶点数量。

    invert_shapes(base_mesh, corrective_meshes)
        批量调用 Maya invertShape，并检查拓扑点数。

为什么 Target 必须读取真实 Alias / Weight Index
-------------------------------------------------
BlendShape 的 Alias 顺序不等于 ``weight`` Multi Attribute 的数组下标。
如果只按列表顺序猜 Index，删除 / 替换 Target 后很容易操作错 Target。

正式逻辑通过：

    cmds.aliasAttr(query=True)
        -> alias
        -> weight[真实 index]

解析真实映射，再进行删除、替换和烘焙。

本模块不负责
------------
- Face Expression UI；
- Pose Reader；
- RBF；
- Corrective Driver 网络；
- Facial Controller；
- BlendShape Tool UI。

模块边界
--------
    BlendShape / Corrective 基础能力 -> blendshape_utils
    Face Expression Rig             -> systems.face
    BlendShape UI                   -> tools.blendshape

设计原则
--------
1. Target 永远按真实 ``weight[index]`` 操作；
2. 同名替换时先清理旧 Target 数据，再写入新 Mesh；
3. 烘焙全部 Target 后必须恢复原始 Weight 值；
4. invertShape 前先检查 Base / Corrective 顶点数量；
5. 批量场景修改使用 Maya Undo Chunk。
"""

from __future__ import print_function

import re

import maya.cmds as cmds


# =============================================================================
# Name / Mesh Query
# =============================================================================

def get_short_name(node):
    u"""
    返回适合作为 Alias / 新 Mesh 名称的短名称。

    DAG Path 被去掉，Namespace 冒号转换成下划线。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    short_name = node.split("|")[-1]
    return short_name.replace(":", "_")


def get_mesh_shape(node):
    u"""
    返回 Transform 或 Mesh 对应的可见 Mesh Shape。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        str/None: 找到 Mesh Shape 时返回节点，否则返回 None。
    """
    # 步骤 1：空参数或不存在节点直接返回 None。
    if not node:
        return None

    if not cmds.objExists(node):
        return None

    # 步骤 2：输入本身就是 Mesh Shape 时直接返回。
    if cmds.nodeType(node) == "mesh":
        return node

    # 步骤 3：Transform 输入时寻找非 Intermediate Mesh Shape。
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
    u"""
    返回节点对应的 Transform；找不到时返回 None。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        None | object:
        方法执行后的结果数据。
    """
    # 步骤 1：过滤无效节点。
    if not node:
        return None

    if not cmds.objExists(node):
        return None

    # 步骤 2：Transform 输入直接返回。
    if cmds.nodeType(node) == "transform":
        return node

    # 步骤 3：Shape / DAG Child 查询直接 Parent。
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


# =============================================================================
# BlendShape Query
# =============================================================================

def find_blendshape(node):
    u"""
    从 BlendShape 本身或节点 History 中寻找第一个 BlendShape。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        str/None: BlendShape 节点。
    """
    # 步骤 1：过滤无效输入。
    if not node:
        return None

    if not cmds.objExists(node):
        return None

    # 步骤 2：输入本身已经是 BlendShape。
    if cmds.nodeType(node) == "blendShape":
        return node

    # 步骤 3：从 History 中按类型过滤。
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
    u"""
    返回 BlendShape 第一个 Base Geometry Transform。

    Args:
        blendshape_node (object):
            `blendshape_node` 对应的输入数据。

    Returns:
        object | None:
        方法执行后的结果数据。
    """
    # 步骤 1：向 BlendShape 查询 Base Geometry。
    geometries = cmds.blendShape(
        blendshape_node,
        query=True,
        geometry=True
    )

    if geometries is None:
        geometries = []

    if not geometries:
        return None

    # 步骤 2：优先转换为 Transform，方便 duplicate / target 命令使用。
    geometry = geometries[0]
    transform = get_transform(geometry)

    if transform:
        return transform

    return geometry


def sort_targets_by_index(targets):
    u"""
    按真实 ``weight[index]`` 升序排序 Target 数据。

    这里故意保留展开的普通循环，避免把 Scene 数据排序逻辑压缩得过于简略。

    Args:
        targets (str | list[str]):
            `targets` 对应的输入数据。

    Returns:
        object:
        方法执行后的结果数据。
    """
    item_count = len(targets)
    outer_index = 0

    # 步骤 1：简单 Bubble Sort，保持逻辑直观。
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
    u"""
    返回 BlendShape 真实 Alias -> Weight Index 映射。

    Args:
        blendshape_node (object):
            `blendshape_node` 对应的输入数据。

    Returns:
        list:
        [
        {
        "alias": "smile",
        "index": 3,
        "plug": "weight[3]",
        },
        ...
        ]
    """
    # 步骤 1：校验 BlendShape。
    if not blendshape_node:
        return []

    if not cmds.objExists(blendshape_node):
        return []

    # -------------------------------------------------------------------------
    # 步骤 2：aliasAttr(query=True) 返回交错列表：
    #
    #     [aliasA, weight[3], aliasB, weight[7], ...]
    # -------------------------------------------------------------------------
    aliases = cmds.aliasAttr(
        blendshape_node,
        query=True
    )

    if aliases is None:
        aliases = []

    targets = []
    index = 0

    # 步骤 3：每两个元素解析一组 Alias / Plug。
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

    # 步骤 4：按真实 Multi Index 排序后返回。
    return sort_targets_by_index(targets)


def get_next_target_index(blendshape_node):
    u"""
    返回下一个可使用的 BlendShape Weight Index。

    Args:
        blendshape_node (object):
            `blendshape_node` 对应的输入数据。

    Returns:
        object | int:
        方法执行后的结果数据。
    """
    # 步骤 1：读取当前 weight Multi Attribute 已存在的 Index。
    indices = cmds.getAttr(
        blendshape_node + ".weight",
        multiIndices=True
    )

    if indices is None:
        indices = []

    # 步骤 2：空 BlendShape 从 0 开始，否则使用最大 Index + 1。
    if not indices:
        return 0

    return max(indices) + 1


# =============================================================================
# Target Remove / Add / Replace
# =============================================================================

def remove_target(
        blendshape_node,
        target_index,
        alias_name=None
):
    u"""
    删除一个 Target 的 Alias、inputTargetGroup 和可清理 Weight Element。

    注意：
        如果 Weight Plug 仍然有输入连接，不会删除该 weight Multi Element，
        避免破坏外部 Driver Network。

    Args:
        blendshape_node (object):
            `blendshape_node` 对应的输入数据。
        target_index (int):
            `target_index` 对应的整数参数。
        alias_name (str):
            `alias_name` 对应的 Maya 节点或资源名称。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：按需要移除 Alias。
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 2：删除该 Target 的 inputTargetGroup。
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 3：Weight 没有外部输入时再删除 Multi Element。
    # -------------------------------------------------------------------------
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
    u"""
    按 Target 短名称新增或同名替换 BlendShape Target。

    Args:
        blendshape_node (object):
            `blendshape_node` 对应的输入数据。
        target_transform (object):
            `target_transform` 对应的输入数据。

    Returns:
        dict: Alias 和真实 Weight Index。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：验证 BlendShape 和 Target Mesh。
    # -------------------------------------------------------------------------
    if not cmds.objExists(blendshape_node):
        raise RuntimeError(
            u"BlendShape 不存在：{}".format(blendshape_node)
        )

    target_shape = get_mesh_shape(target_transform)

    if not target_shape:
        raise RuntimeError(
            u"目标不是 Mesh：{}".format(target_transform)
        )

    # 步骤 2：取得 Base Geometry。
    base_transform = get_base_transform(blendshape_node)

    if not base_transform:
        raise RuntimeError(u"无法获取 BlendShape Base Geometry。")

    # -------------------------------------------------------------------------
    # 步骤 3：用 Target 短名作为 Alias，并查询是否已存在同名 Target。
    # -------------------------------------------------------------------------
    alias_name = get_short_name(target_transform)
    existing_targets = get_targets(blendshape_node)
    target_index = None

    for target_info in existing_targets:
        if target_info["alias"] == alias_name:
            target_index = target_info["index"]
            break

    # 步骤 4：同名则复用真实 Index 并先清旧 Target，否则分配新 Index。
    if target_index is not None:
        remove_target(
            blendshape_node,
            target_index,
            alias_name=alias_name
        )
    else:
        target_index = get_next_target_index(blendshape_node)

    # -------------------------------------------------------------------------
    # 步骤 5：写入 Target。
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # 步骤 6：只在 Maya 当前 Alias 与目标名称不一致时修改 Alias。
    #
    # Maya 2023 在 blendShape(edit=True, target=...) 后通常会自动设置 Alias；
    # 对同一 Plug 再重复 aliasAttr 设置同名 Alias 可能报错，所以先查询。
    # -------------------------------------------------------------------------
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


# =============================================================================
# Target Bake - 烘焙 BlendShape Targets
# =============================================================================

def duplicate_all_targets(blendshape_node):
    u"""
    逐个激活 BlendShape Target，并从 Base Mesh 烘焙出独立 Target Mesh。

    处理期间会临时修改 Weight，finally 中会恢复所有原始值。

    Args:
        blendshape_node (object):
            `blendshape_node` 对应的输入数据。

    Returns:
        object | list:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：取得 Base Geometry 和 Target 列表。
    base_transform = get_base_transform(blendshape_node)

    if not base_transform:
        raise RuntimeError(u"无法获取 BlendShape Base Geometry。")

    targets = get_targets(blendshape_node)

    if not targets:
        return []

    # -------------------------------------------------------------------------
    # 步骤 2：记录所有 Target 原始 Weight。
    # -------------------------------------------------------------------------
    original_values = {}

    for target_info in targets:
        weight_plug = "{}.weight[{}]".format(
            blendshape_node,
            target_info["index"]
        )

        original_values[target_info["index"]] = cmds.getAttr(weight_plug)

    copies = []

    # 步骤 3：整批操作包装为一次 Undo。
    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziDuplicateBlendShapeTargets"
    )

    try:
        for target_info in targets:
            # 步骤 3.1：先把全部 Target 归零。
            for zero_target in targets:
                zero_plug = "{}.weight[{}]".format(
                    blendshape_node,
                    zero_target["index"]
                )
                cmds.setAttr(zero_plug, 0.0)

            # 步骤 3.2：只激活当前 Target。
            active_plug = "{}.weight[{}]".format(
                blendshape_node,
                target_info["index"]
            )
            cmds.setAttr(active_plug, 1.0)

            # 步骤 3.3：按 Alias 命名 Duplicate；重名时加 _copy。
            duplicate_name = target_info["alias"]

            if cmds.objExists(duplicate_name):
                duplicate_name = "{}_copy".format(duplicate_name)

            # 步骤 3.4：复制当前变形后的 Base，并删除 Construction History。
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
        # ---------------------------------------------------------------------
        # 步骤 4：无论中途是否失败，都恢复全部原始 Weight。
        # ---------------------------------------------------------------------
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


# =============================================================================
# Corrective / invertShape
# =============================================================================

def get_vertex_count(node):
    u"""
    返回 Mesh 顶点数量；非 Mesh 返回 None。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object | None:
        方法执行后的结果数据。
    """
    shape = get_mesh_shape(node)

    if not shape:
        return None

    return cmds.polyEvaluate(
        shape,
        vertex=True
    )


def invert_shapes(base_mesh, corrective_meshes):
    u"""
    批量执行 Maya ``invertShape``。

    每个 Corrective 在执行前会检查：
        - 节点存在；
        - 是有效 Mesh；
        - 顶点数量和 Base 一致。

    Args:
        base_mesh (object):
            `base_mesh` 对应的输入数据。
        corrective_meshes (object):
            `corrective_meshes` 对应的输入数据。

    Returns:
        list: 成功创建的 Inverted Shape Mesh。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：验证 Base Mesh。
    if not get_mesh_shape(base_mesh):
        raise RuntimeError(
            u"基础模型不是有效 Mesh：{}".format(base_mesh)
        )

    base_vertex_count = get_vertex_count(base_mesh)
    results = []

    # 步骤 2：整批操作作为一次 Undo。
    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziInvertShapes"
    )

    try:
        for corrective in corrective_meshes:
            # 步骤 2.1：过滤空节点 / 不存在节点。
            if not corrective:
                continue

            if not cmds.objExists(corrective):
                continue

            # 步骤 2.2：过滤非 Mesh。
            if not get_mesh_shape(corrective):
                cmds.warning(
                    u"跳过非 Mesh：{}".format(corrective)
                )
                continue

            # 步骤 2.3：拓扑点数必须一致。
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

            # 步骤 2.4：执行 Maya invertShape。
            inverted = cmds.invertShape(
                base_mesh,
                corrective
            )

            if isinstance(inverted, (list, tuple)):
                inverted = inverted[0]

            # 步骤 2.5：创建稳定目标名称，避免 Maya 自动命名不可控。
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
    "sort_targets_by_index",
    "get_targets",
    "get_next_target_index",
    "remove_target",
    "add_or_replace_target",
    "duplicate_all_targets",
    "get_vertex_count",
    "invert_shapes",
]
