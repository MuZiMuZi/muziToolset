# coding=utf-8
u"""
Skin Utils
==========

Maya SkinCluster 底层工具。

职责：
    1. 查找 SkinCluster；
    2. 复制 Skin Weight；
    3. XML + Influence JSON 权重导入导出；
    4. 查询影响 Joint；
    5. 归一化权重。

本模块不包含 PySide UI。
"""

from __future__ import print_function

import json
import os

import maya.cmds as cmds
import maya.mel as mel


def get_short_name(node):
    """返回适合节点名和文件名使用的短名称。"""
    return node.split("|")[-1].replace(":", "_")


def find_skin_cluster(geometry):
    """返回 geometry 关联的第一个 SkinCluster。"""
    if not geometry:
        return None

    if not cmds.objExists(geometry):
        return None

    try:
        skin_cluster = mel.eval(
            'findRelatedSkinCluster("{}")'.format(geometry)
        )
    except Exception:
        skin_cluster = None

    if skin_cluster:
        return skin_cluster

    history = cmds.listHistory(geometry)

    if history is None:
        history = []

    skin_clusters = cmds.ls(
        history,
        type="skinCluster"
    )

    if skin_clusters is None:
        skin_clusters = []

    if skin_clusters:
        return skin_clusters[0]

    return None


def get_influences(geometry_or_skin_cluster):
    """返回 Geometry 或 SkinCluster 的影响 Joint。"""
    skin_cluster = geometry_or_skin_cluster

    if not cmds.objExists(skin_cluster):
        return []

    if cmds.nodeType(skin_cluster) != "skinCluster":
        skin_cluster = find_skin_cluster(geometry_or_skin_cluster)

    if not skin_cluster:
        return []

    influences = cmds.skinCluster(
        skin_cluster,
        query=True,
        influence=True
    )

    if influences is None:
        influences = []

    return influences


def copy_skin_weights(source, targets):
    """把 source 的 Skin Weight 复制到多个 targets。"""
    source_skin = find_skin_cluster(source)

    if not source_skin:
        raise RuntimeError(
            u"源模型没有 SkinCluster：{}".format(source)
        )

    influences = get_influences(source_skin)

    if not influences:
        raise RuntimeError(u"源 SkinCluster 没有影响 Joint。")

    results = []

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziCopySkinWeights"
    )

    try:
        for target in targets:
            if not cmds.objExists(target):
                cmds.warning(
                    u"目标模型不存在，跳过：{}".format(target)
                )
                continue

            target_skin = find_skin_cluster(target)

            if target_skin:
                cmds.delete(target_skin)

            target_skin = cmds.skinCluster(
                influences,
                target,
                toSelectedBones=True,
                normalizeWeights=1,
                name="sc_{}".format(get_short_name(target))
            )[0]

            cmds.copySkinWeights(
                sourceSkin=source_skin,
                destinationSkin=target_skin,
                noMirror=True,
                surfaceAssociation="closestPoint",
                influenceAssociation=[
                    "label",
                    "oneToOne",
                    "closestJoint",
                ]
            )

            results.append(target_skin)
    finally:
        cmds.undoInfo(closeChunk=True)

    return results


def get_weight_file_names(geometry):
    """返回一个 Geometry 对应的权重文件名称。"""
    short_name = get_short_name(geometry)

    return {
        "xml": "sc_{}.xml".format(short_name),
        "influences": "sc_{}.infs.json".format(short_name),
    }


def export_skin_weights(geometry, directory):
    """导出 deformerWeights XML 和影响 Joint JSON。"""
    skin_cluster = find_skin_cluster(geometry)

    if not skin_cluster:
        raise RuntimeError(
            u"模型没有 SkinCluster：{}".format(geometry)
        )

    if not os.path.isdir(directory):
        os.makedirs(directory)

    file_names = get_weight_file_names(geometry)

    cmds.deformerWeights(
        file_names["xml"],
        path=directory,
        export=True,
        deformer=skin_cluster,
        method="index"
    )

    influences = get_influences(skin_cluster)
    influence_path = os.path.join(
        directory,
        file_names["influences"]
    )

    with open(influence_path, "w") as file_object:
        json.dump(
            influences,
            file_object,
            ensure_ascii=False,
            indent=4
        )

    return {
        "geometry": geometry,
        "skin_cluster": skin_cluster,
        "xml": os.path.join(
            directory,
            file_names["xml"]
        ),
        "influences": influence_path,
    }


def import_skin_weights(geometry, directory):
    """导入 XML 权重和影响 Joint 列表。"""
    file_names = get_weight_file_names(geometry)
    xml_path = os.path.join(
        directory,
        file_names["xml"]
    )
    influence_path = os.path.join(
        directory,
        file_names["influences"]
    )

    if not os.path.isfile(xml_path):
        raise RuntimeError(
            u"找不到权重 XML：{}".format(xml_path)
        )

    if not os.path.isfile(influence_path):
        raise RuntimeError(
            u"找不到影响 Joint 文件：{}".format(influence_path)
        )

    with open(influence_path, "r") as file_object:
        influences = json.load(file_object)

    valid_influences = []
    missing_influences = []

    for influence in influences:
        if cmds.objExists(influence):
            valid_influences.append(influence)
        else:
            missing_influences.append(influence)

    if missing_influences:
        raise RuntimeError(
            u"场景缺少影响 Joint：{}".format(
                ", ".join(missing_influences)
            )
        )

    if not valid_influences:
        raise RuntimeError(u"没有可用于绑定的影响 Joint。")

    old_skin = find_skin_cluster(geometry)

    if old_skin:
        cmds.delete(old_skin)

    skin_cluster = cmds.skinCluster(
        valid_influences,
        geometry,
        toSelectedBones=True,
        normalizeWeights=1,
        name="sc_{}".format(get_short_name(geometry))
    )[0]

    cmds.deformerWeights(
        file_names["xml"],
        path=directory,
        im=True,
        deformer=skin_cluster,
        method="index"
    )

    normalize_skin_weights(skin_cluster)
    return skin_cluster


def normalize_skin_weights(geometry_or_skin_cluster):
    """强制归一化一个 SkinCluster。"""
    skin_cluster = geometry_or_skin_cluster

    if not cmds.objExists(skin_cluster):
        return False

    if cmds.nodeType(skin_cluster) != "skinCluster":
        skin_cluster = find_skin_cluster(geometry_or_skin_cluster)

    if not skin_cluster:
        return False

    cmds.skinCluster(
        skin_cluster,
        edit=True,
        forceNormalizeWeights=True
    )

    return True


def select_influences(geometries):
    """选择多个 Geometry 的全部影响 Joint。"""
    influences = []

    for geometry in geometries:
        geometry_influences = get_influences(geometry)

        for influence in geometry_influences:
            if influence not in influences:
                influences.append(influence)

    if influences:
        cmds.select(
            influences,
            replace=True
        )

    return influences


def normalize_geometries(geometries):
    """批量归一化多个 Geometry。"""
    normalized = []

    for geometry in geometries:
        if normalize_skin_weights(geometry):
            normalized.append(geometry)

    return normalized


__all__ = [
    "get_short_name",
    "find_skin_cluster",
    "get_influences",
    "copy_skin_weights",
    "get_weight_file_names",
    "export_skin_weights",
    "import_skin_weights",
    "normalize_skin_weights",
    "select_influences",
    "normalize_geometries",
]
