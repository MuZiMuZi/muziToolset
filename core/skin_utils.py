# coding=utf-8
u"""
Skin Utils
==========

Maya SkinCluster 领域的通用底层工具。

模块职责
--------
这个模块负责 SkinCluster 的查询、复制、权重文件导入导出和归一化。
它只处理 Skin 数据本身，不包含 PySide UI，也不负责自动绑定完整 Workflow。

当前公开方法
------------
名称 / 查询：
    get_short_name(node)
        获取适合 SkinCluster 名称和权重文件名使用的短名称。

    find_skin_cluster(geometry)
        查找 Geometry 关联的第一个 SkinCluster。

    get_influences(geometry_or_skin_cluster)
        获取 Geometry 或 SkinCluster 的全部 Influence Joint。

权重复制：
    copy_skin_weights(source, targets)
        将 Source Skin Weight 复制给多个 Target，并自动重建 Target SkinCluster。

权重文件：
    get_weight_file_names(geometry)
        根据 Geometry 名称生成 XML 和 Influence JSON 文件名。

    export_skin_weights(geometry, directory)
        导出 deformerWeights XML + Influence JSON。

    import_skin_weights(geometry, directory)
        根据 Influence JSON 重建 SkinCluster，再导入 XML 权重。

归一化 / Selection：
    normalize_skin_weights(geometry_or_skin_cluster)
        强制归一化 SkinCluster 权重。

    select_influences(geometries)
        选择多个 Geometry 的全部 Influence Joint。

    normalize_geometries(geometries)
        批量归一化多个 Geometry。

权重文件结构
------------
每一个 Geometry 使用两份文件：

    sc_<geometry>.xml
        Maya deformerWeights 数据。

    sc_<geometry>.infs.json
        Influence Joint 名称列表。

为什么 Influence 要单独保存
---------------------------
``deformerWeights`` 可以保存权重数值，但重新创建 SkinCluster 前仍然需要知道原来的
Influence Joint。单独保存 Influence JSON，可以先恢复正确的 Joint 列表，再把 XML
权重导入新 SkinCluster。

本模块不负责
------------
- Paint Skin Weight UI；
- 自动生成 Joint；
- 自动权重算法；
- Deformer Rig Workflow；
- PySide 文件窗口。

模块边界
--------
    SkinCluster / Weight          -> skin_utils
    纯 JSON / Path                -> file_utils
    Mesh 基础操作                 -> mesh_utils
    完整自动绑定 / 权重 Workflow  -> tools / systems

设计原则
--------
1. 正式代码不使用 PyMel；
2. JSON / 目录操作统一复用 ``file_utils``；
3. Import 前验证所有 Influence 是否存在，避免创建残缺 SkinCluster；
4. Copy Skin Weight 使用一个 Maya Undo Chunk；
5. 查找 SkinCluster 优先使用 Maya 的 ``findRelatedSkinCluster``，失败后再检查 History。
"""

from __future__ import print_function

import os

import maya.cmds as cmds
import maya.mel as mel

from . import file_utils


# =============================================================================
# Name / Query - 名称与 SkinCluster 查询
# =============================================================================

def get_short_name(node):
    """
    返回适合 Maya 节点名和文件名使用的短名称。

    处理规则：
        - 去掉 DAG Path；
        - Namespace 的冒号替换为下划线。
    """
    # 步骤 1：只保留 DAG 最后一段。
    short_name = node.split("|")[-1]

    # 步骤 2：Namespace 冒号不适合直接作为普通文件名的一部分，统一替换。
    return short_name.replace(":", "_")


def find_skin_cluster(geometry):
    """
    返回 Geometry 关联的第一个 SkinCluster；找不到时返回 None。

    查询分两步：
        1. Maya MEL ``findRelatedSkinCluster``；
        2. History 中按 nodeType 再查一次。

    第二步是容错路径，避免某些特殊场景中 MEL 查询没有返回结果。
    """
    # 步骤 1：过滤空参数和不存在节点。
    if not geometry:
        return None

    if not cmds.objExists(geometry):
        return None

    # -------------------------------------------------------------------------
    # 步骤 2：优先使用 Maya 自带的 findRelatedSkinCluster。
    # -------------------------------------------------------------------------
    try:
        skin_cluster = mel.eval(
            'findRelatedSkinCluster("{}")'.format(geometry)
        )
    except Exception:
        skin_cluster = None

    if skin_cluster:
        return skin_cluster

    # -------------------------------------------------------------------------
    # 步骤 3：Fallback - 检查 History 中的 skinCluster。
    # -------------------------------------------------------------------------
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
    """
    返回 Geometry 或 SkinCluster 的 Influence Joint 列表。

    Args:
        geometry_or_skin_cluster(str): Geometry 或 skinCluster。

    Returns:
        list: Influence 节点；无 SkinCluster 时返回空列表。
    """
    # 步骤 1：输入节点必须存在。
    skin_cluster = geometry_or_skin_cluster

    if not cmds.objExists(skin_cluster):
        return []

    # 步骤 2：如果输入不是 skinCluster，则先从 Geometry 查找。
    if cmds.nodeType(skin_cluster) != "skinCluster":
        skin_cluster = find_skin_cluster(geometry_or_skin_cluster)

    if not skin_cluster:
        return []

    # 步骤 3：查询 Influence。
    influences = cmds.skinCluster(
        skin_cluster,
        query=True,
        influence=True
    )

    if influences is None:
        influences = []

    return influences


# =============================================================================
# Copy - Skin Weight 复制
# =============================================================================

def copy_skin_weights(source, targets):
    """
    将 Source 的 Skin Weight 复制给多个 Target。

    处理流程：
        Source SkinCluster
            -> Influence List
            -> 删除 Target 旧 SkinCluster
            -> 使用同一组 Influence 创建 Target SkinCluster
            -> cmds.copySkinWeights()

    Returns:
        list: 新创建的 Target SkinCluster。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：确认 Source 有 SkinCluster。
    # -------------------------------------------------------------------------
    source_skin = find_skin_cluster(source)

    if not source_skin:
        raise RuntimeError(
            u"源模型没有 SkinCluster：{}".format(source)
        )

    # -------------------------------------------------------------------------
    # 步骤 2：读取 Source Influence。
    # -------------------------------------------------------------------------
    influences = get_influences(source_skin)

    if not influences:
        raise RuntimeError(u"源 SkinCluster 没有影响 Joint。")

    results = []

    # -------------------------------------------------------------------------
    # 步骤 3：整个批量复制作为一次 Maya Undo。
    # -------------------------------------------------------------------------
    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziCopySkinWeights"
    )

    try:
        for target in targets:
            # 步骤 3.1：不存在的 Target 跳过，但不中断其它模型。
            if not cmds.objExists(target):
                cmds.warning(
                    u"目标模型不存在，跳过：{}".format(target)
                )
                continue

            # 步骤 3.2：删除 Target 旧 SkinCluster，避免两套 Skin 重叠。
            target_skin = find_skin_cluster(target)

            if target_skin:
                cmds.delete(target_skin)

            # 步骤 3.3：使用 Source 同一组 Influence 重建 SkinCluster。
            target_skin = cmds.skinCluster(
                influences,
                target,
                toSelectedBones=True,
                normalizeWeights=1,
                name="sc_{}".format(get_short_name(target))
            )[0]

            # 步骤 3.4：按最近点匹配 Geometry，并优先按 Label / OneToOne 匹配 Influence。
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
        # 即使某个 Target 报错，也必须关闭 Undo Chunk。
        cmds.undoInfo(closeChunk=True)

    return results


# =============================================================================
# Weight File - 文件名与导出
# =============================================================================

def get_weight_file_names(geometry):
    """
    返回 Geometry 对应的 XML / Influence JSON 文件名称。

    Returns:
        dict: ``xml`` / ``influences``。
    """
    short_name = get_short_name(geometry)

    return {
        "xml": "sc_{}.xml".format(short_name),
        "influences": "sc_{}.infs.json".format(short_name),
    }


def export_skin_weights(geometry, directory):
    """
    导出 Maya ``deformerWeights`` XML 和 Influence JSON。

    Returns:
        dict: Geometry、SkinCluster 和两个输出文件路径。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：确认 Geometry 已经绑定。
    # -------------------------------------------------------------------------
    skin_cluster = find_skin_cluster(geometry)

    if not skin_cluster:
        raise RuntimeError(
            u"模型没有 SkinCluster：{}".format(geometry)
        )

    # -------------------------------------------------------------------------
    # 步骤 2：统一创建 / 规范化输出目录。
    # -------------------------------------------------------------------------
    directory = file_utils.ensure_directory(directory)
    file_names = get_weight_file_names(geometry)

    # -------------------------------------------------------------------------
    # 步骤 3：让 Maya 导出权重 XML。
    # method=index 适合拓扑一致的绑定权重保存 / 恢复。
    # -------------------------------------------------------------------------
    cmds.deformerWeights(
        file_names["xml"],
        path=directory,
        export=True,
        deformer=skin_cluster,
        method="index"
    )

    # -------------------------------------------------------------------------
    # 步骤 4：单独保存 Influence 名称。
    # -------------------------------------------------------------------------
    influences = get_influences(skin_cluster)
    influence_path = os.path.join(
        directory,
        file_names["influences"]
    )

    influence_path = file_utils.write_json(
        file_path=influence_path,
        data=influences,
        indent=4,
        ensure_ascii=False,
        sort_keys=False
    )

    xml_path = file_utils.normalize_path(
        os.path.join(
            directory,
            file_names["xml"]
        )
    )

    return {
        "geometry": geometry,
        "skin_cluster": skin_cluster,
        "xml": xml_path,
        "influences": influence_path,
    }


# =============================================================================
# Weight File - 导入
# =============================================================================

def import_skin_weights(geometry, directory):
    """
    导入 XML 权重和 Influence Joint 列表。

    流程：
        Influence JSON
            -> 验证 Joint 全部存在
            -> 删除旧 SkinCluster
            -> 创建新 SkinCluster
            -> Import XML
            -> Normalize
    """
    # 步骤 1：整理文件路径。
    directory = file_utils.normalize_path(directory)
    file_names = get_weight_file_names(geometry)

    xml_path = file_utils.normalize_path(
        os.path.join(
            directory,
            file_names["xml"]
        )
    )

    influence_path = file_utils.normalize_path(
        os.path.join(
            directory,
            file_names["influences"]
        )
    )

    # 步骤 2：两个文件缺一不可。
    if not os.path.isfile(xml_path):
        raise RuntimeError(
            u"找不到权重 XML：{}".format(xml_path)
        )

    if not os.path.isfile(influence_path):
        raise RuntimeError(
            u"找不到影响 Joint 文件：{}".format(influence_path)
        )

    # 步骤 3：读取 Influence JSON。
    influences = file_utils.read_json(influence_path)

    valid_influences = []
    missing_influences = []

    # 步骤 4：Import 前确认所有 Influence 都存在。
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

    # 步骤 5：删除旧 SkinCluster。
    old_skin = find_skin_cluster(geometry)

    if old_skin:
        cmds.delete(old_skin)

    # 步骤 6：根据保存的 Influence 重建 SkinCluster。
    skin_cluster = cmds.skinCluster(
        valid_influences,
        geometry,
        toSelectedBones=True,
        normalizeWeights=1,
        name="sc_{}".format(get_short_name(geometry))
    )[0]

    # 步骤 7：导入 XML 权重。
    cmds.deformerWeights(
        file_names["xml"],
        path=directory,
        im=True,
        deformer=skin_cluster,
        method="index"
    )

    # 步骤 8：最终强制归一化。
    normalize_skin_weights(skin_cluster)
    return skin_cluster


# =============================================================================
# Normalize / Selection
# =============================================================================

def normalize_skin_weights(geometry_or_skin_cluster):
    """
    强制归一化一个 SkinCluster。

    Returns:
        bool: 找到并完成归一化时返回 True。
    """
    # 步骤 1：解析 SkinCluster。
    skin_cluster = geometry_or_skin_cluster

    if not cmds.objExists(skin_cluster):
        return False

    if cmds.nodeType(skin_cluster) != "skinCluster":
        skin_cluster = find_skin_cluster(geometry_or_skin_cluster)

    if not skin_cluster:
        return False

    # 步骤 2：使用 Maya SkinCluster 强制 Normalize。
    cmds.skinCluster(
        skin_cluster,
        edit=True,
        forceNormalizeWeights=True
    )

    return True


def select_influences(geometries):
    """
    选择多个 Geometry 的全部 Influence Joint。

    这是明确带 ``select`` 语义的 Core 辅助函数，因此允许修改 Maya Selection。
    """
    influences = []

    # 步骤 1：收集并去重 Influence。
    for geometry in geometries:
        geometry_influences = get_influences(geometry)

        for influence in geometry_influences:
            if influence not in influences:
                influences.append(influence)

    # 步骤 2：有结果时替换当前 Selection。
    if influences:
        cmds.select(
            influences,
            replace=True
        )

    return influences


def normalize_geometries(geometries):
    """批量归一化多个 Geometry，并返回实际成功的 Geometry。"""
    normalized = []

    # 步骤 1：逐 Geometry 调用统一 Normalize API。
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
