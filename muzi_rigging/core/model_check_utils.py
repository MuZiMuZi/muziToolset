# coding=utf-8
u"""
Model Check Utils
=================

Maya 模型检查底层模块。

检查项：
    1. Non-Manifold Vertex / Edge；
    2. Lamina Face；
    3. DAG 重名；
    4. 非 Deformer 的遗留建模历史；
    5. Mesh Transform 未冻结；
    6. 锁定法线。

安全原则：
    - 拓扑问题只报告，不自动猜修；
    - SkinCluster / BlendShape 等正常 Rig Deformer 不当作建模历史错误；
    - 带 Deformer 的 Mesh 不自动 Freeze；
    - 引用节点不自动修复。

本模块不包含 PySide UI。
"""

from __future__ import print_function

import maya.cmds as cmds


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


def get_short_name(node):
    """返回 DAG 节点短名称。"""
    return node.split("|")[-1]


def is_referenced(node):
    """判断节点是否来自 Reference。"""
    try:
        return cmds.referenceQuery(
            node,
            isNodeReferenced=True
        )
    except Exception:
        return False


def get_mesh_shapes(nodes=None):
    """把 Transform / Mesh 输入统一转成非 Intermediate Mesh Shape。"""
    if nodes is None:
        meshes = cmds.ls(
            type="mesh",
            long=True,
            noIntermediate=True
        )

        if meshes is None:
            meshes = []

        return meshes

    if isinstance(nodes, str):
        nodes = [nodes]

    result = []

    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
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
            )

            if matches is None:
                matches = []

            resolved = node

            if matches:
                resolved = matches[0]

            if resolved not in result:
                result.append(resolved)

            continue

        if node_type not in [
            "transform",
            "joint",
        ]:
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="mesh"
        )

        if shapes is None:
            shapes = []

        for shape in shapes:
            if shape not in result:
                result.append(shape)

    return result


def get_mesh_transform(mesh_shape):
    """返回 Mesh Shape 对应 Transform。"""
    parents = cmds.listRelatives(
        mesh_shape,
        parent=True,
        fullPath=True
    )

    if parents is None:
        parents = []

    if parents:
        return parents[0]

    return mesh_shape


def get_mesh_transforms(meshes):
    """从 Mesh Shape 列表返回唯一 Transform 列表。"""
    result = []

    for mesh in meshes:
        transform = get_mesh_transform(mesh)

        if transform not in result:
            result.append(transform)

    return result


def get_history_node_types(mesh):
    """返回需要参与检查的 History Node / Type。"""
    history = cmds.listHistory(
        mesh,
        pruneDagObjects=True
    )

    if history is None:
        history = []

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
    """返回非 Deformer 的建模历史。"""
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
    """判断 Mesh 历史中是否存在 Deformer。"""
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


def make_issue(node, issue_type, details, fixable=False):
    """创建统一 Issue 字典。"""
    return {
        "node": node,
        "type": issue_type,
        "details": details,
        "fixable": bool(fixable),
    }


def check_nonmanifold_geometry(meshes=None):
    """检查 Non-Manifold Vertex / Edge。"""
    meshes = get_mesh_shapes(meshes)
    issues = []

    for mesh in meshes:
        try:
            vertices = cmds.polyInfo(
                mesh,
                nonManifoldVertices=True
            )
            edges = cmds.polyInfo(
                mesh,
                nonManifoldEdges=True
            )
        except Exception:
            continue

        if vertices is None:
            vertices = []
        if edges is None:
            edges = []

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
    """检查 Lamina Face。"""
    meshes = get_mesh_shapes(meshes)
    issues = []

    for mesh in meshes:
        try:
            lamina_faces = cmds.polyInfo(
                mesh,
                laminaFaces=True
            )
        except Exception:
            lamina_faces = []

        if lamina_faces is None:
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


def get_dag_nodes(nodes=None):
    """返回用于重名检查的 DAG 范围。"""
    if nodes is None:
        dag_nodes = cmds.ls(
            dag=True,
            long=True
        )

        if dag_nodes is None:
            dag_nodes = []

        return dag_nodes

    dag_nodes = []

    for node in nodes:
        if not cmds.objExists(node):
            continue

        matches = cmds.ls(
            node,
            long=True
        )

        if matches is None:
            matches = []

        resolved = node

        if matches:
            resolved = matches[0]

        if resolved not in dag_nodes:
            dag_nodes.append(resolved)

        descendants = cmds.listRelatives(
            resolved,
            allDescendents=True,
            fullPath=True
        )

        if descendants is None:
            descendants = []

        for descendant in descendants:
            if descendant not in dag_nodes:
                dag_nodes.append(descendant)

    return dag_nodes


def check_duplicate_names(nodes=None):
    """检查 DAG 短名称冲突。"""
    dag_nodes = get_dag_nodes(nodes)
    name_map = {}

    for node in dag_nodes:
        short_name = get_short_name(node)

        if short_name in default_cameras:
            continue

        if short_name not in name_map:
            name_map[short_name] = []

        name_map[short_name].append(node)

    issues = []
    short_names = []

    for short_name in name_map:
        short_names.append(short_name)

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

    return issues


def check_construction_history(meshes=None):
    """检查非 Deformer 的遗留建模历史。"""
    meshes = get_mesh_shapes(meshes)
    issues = []

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

    return issues


def _vector_has_nonzero(values, tolerance=0.001):
    """判断向量是否存在超过容差的非零值。"""
    for value in values:
        if abs(value) > tolerance:
            return True

    return False


def _scale_is_nondefault(values, tolerance=0.001):
    """判断 Scale 是否偏离 1。"""
    for value in values:
        if abs(value - 1.0) > tolerance:
            return True

    return False


def _round_values(values):
    """返回三位小数显示值，不使用列表推导。"""
    result = []

    for value in values:
        result.append(
            round(value, 3)
        )

    return result


def check_transformations(meshes=None):
    """检查 Mesh Transform 是否未冻结。"""
    meshes = get_mesh_shapes(meshes)
    transforms = get_mesh_transforms(meshes)
    issues = []

    for node in transforms:
        if get_short_name(node) in default_cameras:
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

    return issues


def check_locked_normals(meshes=None, sample_limit=500):
    """采样检查锁定法线。"""
    meshes = get_mesh_shapes(meshes)
    issues = []

    for mesh in meshes:
        vertices = cmds.ls(
            mesh + ".vtx[*]",
            flatten=True
        )

        if vertices is None:
            vertices = []

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
                )
            except Exception:
                locked_values = []

            if locked_values is None:
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

    return issues


def run_checks(
        nodes=None,
        check_nonmanifold=True,
        check_lamina=True,
        check_duplicates=True,
        check_history=True,
        check_transform=True,
        check_normals=True
):
    """按配置执行模型检查。"""
    issues = []
    meshes = get_mesh_shapes(nodes)

    if check_nonmanifold:
        result = check_nonmanifold_geometry(meshes)
        for issue in result:
            issues.append(issue)

    if check_lamina:
        result = check_lamina_faces(meshes)
        for issue in result:
            issues.append(issue)

    if check_duplicates:
        result = check_duplicate_names(nodes)
        for issue in result:
            issues.append(issue)

    if check_history:
        result = check_construction_history(meshes)
        for issue in result:
            issues.append(issue)

    if check_transform:
        result = check_transformations(meshes)
        for issue in result:
            issues.append(issue)

    if check_normals:
        result = check_locked_normals(meshes)
        for issue in result:
            issues.append(issue)

    return issues


def fix_issue(issue):
    """修复一个允许自动修复的问题。"""
    node = issue.get("node")
    issue_type = issue.get("type")

    if not issue.get("fixable"):
        return False

    if not node:
        return False

    if not cmds.objExists(node):
        return False

    if is_referenced(node):
        return False

    if issue_type == u"遗留建模历史":
        cmds.bakePartialHistory(
            node,
            prePostDeformers=True
        )
        return True

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

    return False


def fix_issues(issues):
    """批量修复 Issue 列表中允许自动修复的项目。"""
    fixed_count = 0

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziModelCheckerFix"
    )

    try:
        for issue in issues:
            try:
                if fix_issue(issue):
                    fixed_count += 1
            except Exception as error:
                cmds.warning(str(error))
    finally:
        cmds.undoInfo(closeChunk=True)

    return fixed_count


__all__ = [
    "get_mesh_shapes",
    "get_mesh_transform",
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
