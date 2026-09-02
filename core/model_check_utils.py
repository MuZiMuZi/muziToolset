# coding=utf-8
u"""
Model Check Utils
=================

Maya 模型质量检查模块。

模块职责
--------
本模块负责“尽量只读地发现问题”，并把检查结果统一整理成 Issue 字典。
只有明确标记 ``fixable=True`` 的安全问题才允许通过 ``fix_issue / fix_issues`` 修复。

当前检查项
----------
check_nonmanifold_geometry(meshes=None)
    检查 Non-Manifold Vertex / Edge。

check_lamina_faces(meshes=None)
    检查 Lamina Face。

check_duplicate_names(nodes=None)
    检查 DAG Short Name 冲突。

check_construction_history(meshes=None)
    检查非 Deformer 的遗留建模历史。

check_transformations(meshes=None)
    检查 Mesh Transform 是否未冻结；如果有 Rig Deformer，只报告而不允许自动 Freeze。

check_locked_normals(meshes=None, sample_limit=500)
    采样检查锁定法线。

run_checks(...)
    根据开关组合执行全部检查，并返回统一 Issue 列表。

修复 API
--------
fix_issue(issue)
    只修复 Issue 自己声明为 fixable 的安全问题。

fix_issues(issues)
    在一个 Maya Undo Chunk 中批量修复。

通用辅助
--------
get_mesh_shapes(nodes=None)
get_mesh_transform(mesh_shape)
get_mesh_transforms(meshes)
get_modeling_history(mesh)
has_deformer_history(mesh)
make_issue(node, issue_type, details, fixable=False)
    用于统一检查输入与结果格式。

Issue 数据结构
--------------
{
    "node": "|character|model_md_head_geo_001",
    "type": "遗留建模历史",
    "details": "3 个节点：polyExtrudeFace, polyMergeVert",
    "fixable": True,
}

安全原则
--------
1. Non-Manifold / Lamina 只报告，不猜测拓扑修复方案；
2. SkinCluster / BlendShape / Wrap 等正常 Rig Deformer 不当作建模历史错误；
3. 有 Deformer 的 Mesh 不自动 Freeze；
4. Reference 节点不自动修复；
5. 检查与清理分离：大范围场景清理属于 scene_clean_utils.py；
6. Core 不弹确认窗口，UI 是否允许自动修复由上层 Tool 决定。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import rename_utils

from . import scene_utils


default_cameras = [
    "persp",
    "top",
    "front",
    "side",
]


deformer_types = [
    "skinCluster",
    "blendShape",
    "cluster",
    "wire",
    "ffd",
    "lattice",
    "nonLinear",
    "deltaMush",
    "tension",
    "wrap",
    "proximityWrap",
    "sculpt",
]


history_ignore_types = [
    "mesh",
    "transform",
    "groupId",
    "groupParts",
    "objectSet",
    "shadingEngine",
    "tweak",
]


# =============================================================================
# Common Query
# =============================================================================


def is_referenced(node):
    u"""
    判断节点是否来自 Maya Reference。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object | bool:
        方法执行后的结果数据。
    """
    try:
        return cmds.referenceQuery(
            node,
            isNodeReferenced=True
        )
    except Exception:
        return False


def get_mesh_shapes(nodes=None):
    u"""
    把 Transform / Mesh 输入统一转换成非 Intermediate Mesh Shape Long Path。

    ``nodes=None`` 时扫描全场景 Mesh。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if nodes is None:
        return cmds.ls(
            type="mesh",
            long=True,
            noIntermediate=True
        ) or []

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if isinstance(nodes, str):
        nodes = [nodes]

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    result = []

    # 步骤 1：逐个解析输入类型。
    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in nodes:
        if not node or not cmds.objExists(node):
            continue

        node_type = cmds.nodeType(node)

        if node_type == "mesh":
            try:
                intermediate = cmds.getAttr(
                    node + ".intermediateObject"
                )
            except Exception:
                intermediate = False

            if intermediate:
                continue

            matches = cmds.ls(
                node,
                long=True
            ) or []
            resolved = matches[0] if matches else node

            if resolved not in result:
                result.append(resolved)

            continue

        if node_type not in [
            "transform",
            "joint",
        ]:
            continue

        # 步骤 2：Transform / Joint 输入转为可见 Mesh Shape。
        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="mesh"
        ) or []

        for shape in shapes:
            if shape not in result:
                result.append(shape)

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result


def get_mesh_transform(mesh_shape):
    u"""
    返回 Mesh Shape 的 Transform Long Path。

    Args:
        mesh_shape (str):
            需要拓扑、Normal 或 History 检查的 Mesh Shape 节点。

    Returns:
        object:
        方法执行后的结果数据。
    """
    parents = cmds.listRelatives(
        mesh_shape,
        parent=True,
        fullPath=True
    ) or []

    if parents:
        return parents[0]

    return mesh_shape


def get_mesh_transforms(meshes):
    u"""
    从 Mesh Shape 列表整理唯一 Transform 列表。

    Args:
        meshes (str | list[str]):
            需要批量检查、清理或处理的 Mesh Transform / Shape 列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    result = []

    for mesh in meshes:
        transform = get_mesh_transform(mesh)

        if transform not in result:
            result.append(transform)

    return result


# =============================================================================
# History Query
# =============================================================================

def get_history_node_types(mesh):
    u"""
    返回参与 Model Check 的 History ``(node, node_type)`` 列表。

    Args:
        mesh (str):
            需要处理的 Maya Mesh Transform 或 Shape 名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    history = cmds.listHistory(
        mesh,
        pruneDagObjects=True
    ) or []

    result = []

    for node in history:
        try:
            node_type = cmds.nodeType(node)
        except Exception:
            continue

        if node_type in history_ignore_types:
            continue

        result.append(
            (node, node_type)
        )

    return result


def get_modeling_history(mesh):
    u"""
    返回非 Deformer 的遗留建模历史。

    geometryFilter 类型即使不在 deformer_types 表里也会被视为正常 Deformer，从而避免误报。

    Args:
        mesh (str):
            需要处理的 Maya Mesh Transform 或 Shape 名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    result = []
    history_nodes = get_history_node_types(mesh)

    for node, node_type in history_nodes:
        if node_type in deformer_types:
            continue

        try:
            if cmds.objectType(
                    node,
                    isAType="geometryFilter"
            ):
                continue
        except Exception:
            pass

        result.append(
            (node, node_type)
        )

    return result


def has_deformer_history(mesh):
    u"""
    判断 Mesh 历史中是否存在需要保护的 Deformer。

    Args:
        mesh (str):
            需要处理的 Maya Mesh Transform 或 Shape 名称。

    Returns:
        bool:
        方法执行后的结果数据。
    """
    history_nodes = get_history_node_types(mesh)

    for node, node_type in history_nodes:
        if node_type in deformer_types:
            return True

        try:
            if cmds.objectType(
                    node,
                    isAType="geometryFilter"
            ):
                return True
        except Exception:
            pass

    return False


# =============================================================================
# Issue Format
# =============================================================================

def make_issue(node, issue_type, details, fixable=False):
    u"""
    创建统一 Issue 字典。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。
        issue_type (str):
            模型检查结果的 Issue 类型标记，例如 NonManifold、History 或 Transform。
        details (str | dict | list):
            模型检查 Issue 的详细节点、Component 或诊断数据。
        fixable (bool):
            当前模型检查 Issue 是否支持由工具自动修复。

    Returns:
        dict:
        方法执行后的结果数据。
    """
    return {
        "node": node,
        "type": issue_type,
        "details": details,
        "fixable": bool(fixable),
    }


# =============================================================================
# Topology Check
# =============================================================================

def check_nonmanifold_geometry(meshes=None):
    u"""
    检查 Non-Manifold Vertex / Edge。只报告，不自动修复。

    Args:
        meshes (str | list[str]):
            需要批量检查、清理或处理的 Mesh Transform / Shape 列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    meshes = get_mesh_shapes(meshes)
    issues = []

    for mesh in meshes:
        try:
            vertices = cmds.polyInfo(
                mesh,
                nonManifoldVertices=True
            ) or []
            edges = cmds.polyInfo(
                mesh,
                nonManifoldEdges=True
            ) or []
        except Exception:
            continue

        if not vertices and not edges:
            continue

        issues.append(
            make_issue(
                get_mesh_transform(mesh),
                u"非流形几何体",
                u"顶点 {} / 边 {}".format(
                    len(vertices),
                    len(edges)
                ),
                fixable=False
            )
        )

    return issues


def check_lamina_faces(meshes=None):
    u"""
    检查 Lamina Face。只报告，不自动修复。

    Args:
        meshes (str | list[str]):
            需要批量检查、清理或处理的 Mesh Transform / Shape 列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    meshes = get_mesh_shapes(meshes)
    issues = []

    for mesh in meshes:
        try:
            lamina_faces = cmds.polyInfo(
                mesh,
                laminaFaces=True
            ) or []
        except Exception:
            lamina_faces = []

        if not lamina_faces:
            continue

        issues.append(
            make_issue(
                get_mesh_transform(mesh),
                u"薄片面",
                u"数量 {}".format(len(lamina_faces)),
                fixable=False
            )
        )

    return issues


# =============================================================================
# Duplicate DAG Name Check
# =============================================================================

def get_dag_nodes(nodes=None):
    u"""
    返回重名检查使用的 DAG Long Path 范围。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if nodes is None:
        return cmds.ls(
            dag=True,
            long=True
        ) or []

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    dag_nodes = []

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in nodes:
        if not cmds.objExists(node):
            continue

        matches = cmds.ls(
            node,
            long=True
        ) or []
        resolved = matches[0] if matches else node

        if resolved not in dag_nodes:
            dag_nodes.append(resolved)

        descendants = cmds.listRelatives(
            resolved,
            allDescendents=True,
            fullPath=True
        ) or []

        for descendant in descendants:
            if descendant not in dag_nodes:
                dag_nodes.append(descendant)

    # -------------------------------------------------------------------------
    # Step 04：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return dag_nodes


def check_duplicate_names(nodes=None):
    u"""
    检查 DAG Short Name 冲突。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    dag_nodes = get_dag_nodes(nodes)
    name_map = {}

    # 步骤 1：按 Short Name 分组。
    # -------------------------------------------------------------------------
    # Step 02：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in dag_nodes:
        short_name = rename_utils.get_short_name(node)

        if short_name in default_cameras:
            continue

        if short_name not in name_map:
            name_map[short_name] = []

        name_map[short_name].append(node)

    # 步骤 2：数量大于 1 的名称生成 Issue。
    issues = []
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    short_names = []

    for short_name in name_map:
        short_names.append(short_name)

    # -------------------------------------------------------------------------
    # Step 04：执行当前阶段的核心处理
    # -------------------------------------------------------------------------
    short_names.sort()

    for short_name in short_names:
        matches = name_map[short_name]

        if len(matches) <= 1:
            continue

        issues.append(
            make_issue(
                matches[0],
                u"重名",
                u"{} 出现 {} 次".format(
                    short_name,
                    len(matches)
                ),
                fixable=False
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return issues


# =============================================================================
# Construction History Check
# =============================================================================

def check_construction_history(meshes=None):
    u"""
    检查非 Deformer 的遗留建模历史。

    Args:
        meshes (str | list[str]):
            需要批量检查、清理或处理的 Mesh Transform / Shape 列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    meshes = get_mesh_shapes(meshes)
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    issues = []

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for mesh in meshes:
        history = get_modeling_history(mesh)

        if not history:
            continue

        history_types = []

        for history_node, node_type in history:
            if node_type not in history_types:
                history_types.append(node_type)

        display_types = []
        type_index = 0

        while type_index < len(history_types):
            if type_index >= 6:
                break

            display_types.append(history_types[type_index])
            type_index += 1

        issues.append(
            make_issue(
                get_mesh_transform(mesh),
                u"遗留建模历史",
                u"{} 个节点：{}".format(
                    len(history),
                    ", ".join(display_types)
                ),
                fixable=True
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return issues


# =============================================================================
# Transform Check
# =============================================================================

def _vector_has_nonzero(values, tolerance=0.001):
    """判断向量是否存在超过容差的非零值。"""
    for value in values:
        if abs(value) > tolerance:
            return True

    return False


def _scale_is_nondefault(values, tolerance=0.001):
    """判断 Scale 是否偏离默认值 1。"""
    for value in values:
        if abs(value - 1.0) > tolerance:
            return True

    return False


def _round_values(values):
    """返回三位小数显示值。"""
    result = []

    for value in values:
        result.append(
            round(value, 3)
        )

    return result


def check_transformations(meshes=None):
    u"""
    检查 Mesh Transform 是否未冻结。

    有 Deformer 时仍然报告，但 ``fixable=False``，避免自动 Freeze 破坏绑定。

    Args:
        meshes (str | list[str]):
            需要批量检查、清理或处理的 Mesh Transform / Shape 列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    meshes = get_mesh_shapes(meshes)
    # -------------------------------------------------------------------------
    # Step 02：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    transforms = get_mesh_transforms(meshes)
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    issues = []

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in transforms:
        if rename_utils.get_short_name(node) in default_cameras:
            continue

        try:
            translate = cmds.getAttr(
                node + ".translate"
            )[0]
            rotate = cmds.getAttr(
                node + ".rotate"
            )[0]
            scale = cmds.getAttr(
                node + ".scale"
            )[0]
        except Exception:
            continue

        translation_bad = _vector_has_nonzero(translate)
        rotation_bad = _vector_has_nonzero(rotate)
        scale_bad = _scale_is_nondefault(scale)

        if not translation_bad and not rotation_bad and not scale_bad:
            continue

        fixable = not has_deformer_history(node)
        suffix = ""

        if not fixable:
            suffix = u" | 有 Deformer，不自动 Freeze"

        issues.append(
            make_issue(
                node,
                u"Mesh Transform 未冻结",
                u"T {} | R {} | S {}{}".format(
                    _round_values(translate),
                    _round_values(rotate),
                    _round_values(scale),
                    suffix
                ),
                fixable=fixable
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return issues


# =============================================================================
# Normal Check
# =============================================================================

def check_locked_normals(meshes=None, sample_limit=500):
    u"""
    采样检查锁定法线。

    大模型默认只检查前 500 个 Vertex，避免 Model Checker 因逐点查询导致明显卡顿。

    Args:
        meshes (str | list[str]):
            需要批量检查、清理或处理的 Mesh Transform / Shape 列表。
        sample_limit (int):
            模型检查报告中单类问题最多展示的 Component 样本数量。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    meshes = get_mesh_shapes(meshes)
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    issues = []

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for mesh in meshes:
        vertices = cmds.ls(
            mesh + ".vtx[*]",
            flatten=True
        ) or []

        if not vertices:
            continue

        sample_count = min(
            len(vertices),
            int(sample_limit)
        )
        locked_vertex_count = 0
        index = 0

        while index < sample_count:
            vertex = vertices[index]

            try:
                locked_values = cmds.polyNormalPerVertex(
                    vertex,
                    query=True,
                    freezeNormal=True
                ) or []
            except Exception:
                locked_values = []

            is_locked = False

            for value in locked_values:
                if value:
                    is_locked = True
                    break

            if is_locked:
                locked_vertex_count += 1

            index += 1

        if locked_vertex_count <= 0:
            continue

        details = u"采样 {} 个点，发现 {} 个锁定法线点".format(
            sample_count,
            locked_vertex_count
        )

        if len(vertices) > sample_count:
            details += u"（总点数 {}）".format(len(vertices))

        issues.append(
            make_issue(
                get_mesh_transform(mesh),
                u"法线被锁定",
                details,
                fixable=True
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return issues


# =============================================================================
# Runner
# =============================================================================

def run_checks(
        nodes=None,
        check_nonmanifold=True,
        check_lamina=True,
        check_duplicates=True,
        check_history=True,
        check_transform=True,
        check_normals=True
):
    u"""
    根据开关执行模型检查，按顺序合并成一个 Issue 列表。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。
        check_nonmanifold (bool):
            是否检查 Nonmanifold Vertex / Edge。
        check_lamina (bool):
            是否检查 Lamina Face。
        check_duplicates (bool):
            是否检查重复模型、重复 Shape 或重复命名问题。
        check_history (bool):
            是否检查不需要的 Modeling History。
        check_transform (bool):
            是否检查异常 Translate / Rotate / Scale / Pivot。
        check_normals (bool):
            是否检查 Mesh Normal 方向和相关异常。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    issues = []
    meshes = get_mesh_shapes(nodes)

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    check_results = []

    if check_nonmanifold:
        check_results.append(
            check_nonmanifold_geometry(meshes)
        )

    if check_lamina:
        check_results.append(
            check_lamina_faces(meshes)
        )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if check_duplicates:
        check_results.append(
            check_duplicate_names(nodes)
        )

    if check_history:
        check_results.append(
            check_construction_history(meshes)
        )

    if check_transform:
        check_results.append(
            check_transformations(meshes)
        )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if check_normals:
        check_results.append(
            check_locked_normals(meshes)
        )

    for result in check_results:
        for issue in result:
            issues.append(issue)

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return issues


# =============================================================================
# Safe Fix
# =============================================================================

def fix_issue(issue):
    u"""
    修复一个明确允许自动修复的 Issue。

    Args:
        issue (dict | object):
            单条模型检查 Issue 数据。

    Returns:
        bool:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    node = issue.get("node")
    issue_type = issue.get("type")

    # 步骤 1：Issue 自己必须声明 fixable。
    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not issue.get("fixable"):
        return False

    if not node or not cmds.objExists(node):
        return False

    # 步骤 2：Reference 节点永远不由本地 Model Checker 修改。
    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if is_referenced(node):
        return False

    # 步骤 3：根据 Issue Type 执行白名单修复。
    if issue_type == u"遗留建模历史":
        cmds.bakePartialHistory(
            node,
            prePostDeformers=True
        )
        return True

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if issue_type == u"Mesh Transform 未冻结":
        if has_deformer_history(node):
            return False

        cmds.makeIdentity(
            node,
            apply=True,
            translate=True,
            rotate=True,
            scale=True,
            normal=False,
            preserveNormals=True
        )
        return True

    if issue_type == u"法线被锁定":
        cmds.polyNormalPerVertex(
            node,
            unFreezeNormal=True
        )
        return True

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return False


@scene_utils.undo_chunk
def fix_issues(issues):
    u"""
    批量修复允许自动修复的 Issue，并返回成功数量。

    Args:
        issues (list):
            模型检查产生的 Issue 结果列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    fixed_count = 0

    for issue in issues:
        try:
            if fix_issue(issue):
                fixed_count += 1
        except Exception as error:
            cmds.warning(str(error))

    return fixed_count


__all__ = [
    "get_mesh_shapes",
    "get_mesh_transform",
    "get_mesh_transforms",
    "get_modeling_history",
    "has_deformer_history",
    "make_issue",
    "check_nonmanifold_geometry",
    "check_lamina_faces",
    "check_duplicate_names",
    "check_construction_history",
    "check_transformations",
    "check_locked_normals",
    "run_checks",
    "fix_issue",
    "fix_issues",
]
