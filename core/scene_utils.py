# coding=utf-8
u"""
Scene Utils
===========

Maya Scene 领域的统一底层工具。

模块职责
--------
本模块统一负责 Maya Scene 级别的查询、创建、修改、清理和文件 IO：

    - Undo Chunk；
    - Maya Node 存在性、唯一 DAG Long Path 和节点创建；
    - Scene Availability、Node Type 和 Selection 查询；
    - Object Set 创建与维护；
    - Maya Native Event Callback；
    - 当前 Scene 路径与修改状态；
    - Maya Scene Open / Import / Reference；
    - FBX 等场景导出；
    - 安全范围内的 Scene Cleanup。

模块边界
--------
    Maya Scene / Node / Selection / Scene IO / Export / Cleanup -> scene_utils
    硬盘 Path / Directory / JSON                                -> file_utils
    Transform 空间数据                                           -> transform_utils
    DAG Parent / Child                                           -> hierarchy_utils
    Snap / Match                                                 -> snap_utils
    模型问题检查 / 诊断                                           -> model_check_utils

设计原则
--------
1. Core 不弹确认窗口，交互确认由 Tool / App 负责；
2. 创建函数先处理必要输入，再修改 Maya Scene；
3. validate_node() 只接受 Maya Node，不接受 Plug / Component；
4. ensure_nodes_available() 只检查已有 Scene State，不判断 Rig Naming 格式；
5. 内部 Rig Naming 默认可信，Scene Core 不负责重复验证命名规范；
6. Cleanup 只保护 Scene State：Reference、Animation、Constraint、Rig Deformer 等；
7. Export 接收明确对象列表，不依赖用户当前 Selection，并在结束后恢复 Selection；
8. model_check_utils 保持只读检查职责，不与会修改场景的 Scene API 合并。
"""

from __future__ import print_function

import os
from functools import partial
from functools import wraps

import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel

from . import file_utils


# =============================================================================
# Undo
# =============================================================================

def open_undo_chunk(chunk_name=None):
    u"""
    打开一个 Maya Undo Chunk。

    Args:
        chunk_name (str | None):
            可选 Undo Chunk 名称；None 时使用 Maya 默认命名。

    Returns:
        bool:
        Undo Chunk 成功打开后返回 True。
    """
    kwargs = {
        "openChunk": True,
    }

    if chunk_name:
        kwargs["chunkName"] = chunk_name

    cmds.undoInfo(
        **kwargs
    )
    return True


def close_undo_chunk():
    u"""
    关闭当前 Maya Undo Chunk。

    Returns:
        bool:
        Undo Chunk 成功关闭后返回 True。
    """
    cmds.undoInfo(
        closeChunk=True
    )
    return True


def undo_chunk(function):
    u"""
    把一次完整函数执行包装成一个 Maya Undo Chunk。

    Args:
        function (callable):
            需要在单个 Maya Undo Chunk 中执行的函数。

    Returns:
        callable:
        保留原函数元数据的 Undo Wrapper。
    """

    @wraps(function)
    def wrapped(*args, **kwargs):
        open_undo_chunk(
            function.__name__
        )

        try:
            return function(
                *args,
                **kwargs
            )
        finally:
            close_undo_chunk()

    return wrapped


# =============================================================================
# Node
# =============================================================================

def validate_node(node, label=None):
    u"""
    检查输入是否为真实存在的 Maya Node。

    Plug / Component 不属于 Node，因此例如 ``pCube1.translateX`` 和
    ``pCube1.vtx[0]`` 都会被拒绝。

    Args:
        node (str):
            需要验证的 Maya Node 名称或唯一 DAG Path。
        label (str | None):
            可选错误提示标签；None 时使用“ Maya 节点”。

    Returns:
        bool:
        节点存在且输入不是 Plug / Component 时返回 True。

    Raises:
        RuntimeError:
        名称为空、输入为 Plug / Component，或 Maya Node 不存在时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    display_label = label or u"Maya 节点"

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if node is None:
        raise RuntimeError(
            u"{}名称不能为空。".format(
                display_label
            )
        )

    node = str(node).strip()

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not node:
        raise RuntimeError(
            u"{}名称不能为空。".format(
                display_label
            )
        )

    if "." in node:
        raise RuntimeError(
            u"{}必须是 Maya Node，不能是 Plug / Component：{}".format(
                display_label,
                node
            )
        )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not cmds.objExists(node):
        raise RuntimeError(
            u"{}不存在：{}".format(
                display_label,
                node
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True


def ensure_nodes_available(node_names, label=u"待创建节点"):
    u"""
    确保一组准备创建的 Maya 节点名称当前都没有被 Scene 占用。

    Args:
        node_names (str | list[str] | None):
            准备创建的一个或多个 Maya Node 名称；None 时直接视为可用。
        label (str):
            节点被占用时用于错误信息的业务标签。

    Returns:
        bool:
        所有有效名称都未被当前 Scene 占用时返回 True。

    Raises:
        RuntimeError:
        任意名称已经对应现有 Maya Node 时抛出，并列出全部冲突名称。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if node_names is None:
        return True

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if isinstance(node_names, str):
        node_names = [
            node_names
        ]

    existing_nodes = []

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node_name in node_names:
        if not node_name:
            continue

        if cmds.objExists(node_name):
            existing_nodes.append(
                node_name
            )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if existing_nodes:
        raise RuntimeError(
            u"{}已存在：{}".format(
                label,
                ", ".join(existing_nodes)
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True


def get_long_name(node):
    u"""
    返回唯一 Maya DAG Long Path；非 DAG 节点返回 Maya 查询得到的节点名。

    Args:
        node (str):
            需要解析的 Maya Node 名称或唯一 DAG Path。

    Returns:
        str:
        DAG 节点的唯一 Long Path，或非 DAG 节点的 Maya 节点名。

    Raises:
        RuntimeError:
        节点不存在，或输入短名称对应多个 DAG 节点时抛出。
    """
    validate_node(
        node
    )

    matches = cmds.ls(
        node,
        long=True
    )

    if matches is None:
        matches = []

    if not matches:
        return str(node)

    if len(matches) > 1:
        raise RuntimeError(
            u"节点名称不唯一，请使用完整路径：{}".format(
                node
            )
        )

    return matches[0]


def create_node(
        node_type,
        name,
        parent=None
):
    u"""
    创建一个 Maya Node，可选在创建时指定 DAG Parent。

    本函数不负责 Match / Snap。已经存在节点的 Reparent 统一交给
    ``hierarchy_utils.parent()``。

    Args:
        node_type (str):
            Maya Node Type，例如 ``transform``、``network`` 或 ``multMatrix``。
        name (str):
            新节点名称；当前场景中不能已经存在同名节点。
        parent (str | None):
            仅在创建 DAG Node 时使用的可选 Parent；None 表示不指定 Parent。

    Returns:
        str:
        Maya 创建后返回的节点名称。

    Raises:
        ValueError:
        ``node_type`` 或 ``name`` 为空时抛出。
        RuntimeError:
        同名节点已经存在，或指定 Parent 不存在时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not node_type:
        raise ValueError(
            u"node_type 不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not name:
        raise ValueError(
            u"节点名称不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    ensure_nodes_available(
        name,
        label=u"节点"
    )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if parent is not None:
        validate_node(
            parent,
            u"Parent"
        )

        return cmds.createNode(
            node_type,
            name=name,
            parent=parent
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return cmds.createNode(
        node_type,
        name=name
    )


def get_nodes_by_type(
        node_type,
        long=True
):
    u"""
    返回当前 Maya Scene 中指定 Node Type 的全部节点。

    Args:
        node_type (str):
            需要查询的 Maya Node Type，例如 ``joint`` 或 ``transform``。
        long (bool):
            是否让 Maya 对 DAG Node 返回 Long Path。

    Returns:
        list[str]:
        指定类型的 Maya Node 列表；没有匹配节点时返回空列表。

    Raises:
        ValueError:
        ``node_type`` 为空时抛出。
    """
    if not node_type:
        raise ValueError(
            u"node_type 不能为空。"
        )

    nodes = cmds.ls(
        type=node_type,
        long=long
    )

    if nodes is None:
        nodes = []

    return nodes


# =============================================================================
# Selection
# =============================================================================

def get_selected_nodes(
        node_type=None,
        long=True,
        flatten=True
):
    u"""
    返回当前 Maya Selection，可选按 Maya Node Type 过滤。

    未指定 ``node_type`` 时保留 Maya 当前 Selection Item，因此 Component
    Selection 也可能出现在结果中；指定 ``node_type`` 后 Component 会被忽略。

    Args:
        node_type (str | None):
            可选 Maya Node Type；None 时不过滤当前 Selection Item。
        long (bool):
            是否让 Maya 尽量返回 DAG Long Path。
        flatten (bool):
            是否展开 Maya Component Selection。

    Returns:
        list[str]:
        当前 Selection；没有选择或过滤后没有匹配项时返回空列表。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    selected_nodes = cmds.ls(
        selection=True,
        long=long,
        flatten=flatten
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if selected_nodes is None:
        selected_nodes = []

    if node_type is None:
        return selected_nodes

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    filtered_nodes = []

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for selected_node in selected_nodes:
        if "." in selected_node:
            continue

        try:
            selected_type = cmds.nodeType(
                selected_node
            )
        except Exception:
            continue

        if selected_type != node_type:
            continue

        filtered_nodes.append(
            selected_node
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return filtered_nodes


# =============================================================================
# Object Set
# =============================================================================

def ensure_object_set(
        set_name,
        objects=None,
        parent_set=None
):
    u"""
    创建或复用 Object Set，并可安全加入对象和父 Set。

    Args:
        set_name (str):
            需要创建或复用的 Maya Object Set 名称。
        objects (str | list[str] | None):
            可选需要加入 Set 的 Maya Node；None 时只确保 Set 本身存在。
        parent_set (str | None):
            可选父 Object Set；不存在时会自动创建。

    Returns:
        str:
        已确认存在并完成成员维护的 Object Set 名称。

    Raises:
        ValueError:
        ``set_name`` 为空时抛出。
        RuntimeError:
        Set 名称或 Parent Set 名称被非 Object Set 节点占用，或成员节点无效时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not set_name:
        raise ValueError(
            u"Set 名称不能为空。"
        )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if cmds.objExists(set_name):
        if cmds.nodeType(set_name) != "objectSet":
            raise RuntimeError(
                u"同名节点不是 Object Set：{}".format(
                    set_name
                )
            )
    else:
        set_name = cmds.sets(
            name=set_name,
            empty=True
        )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if objects is not None:
        if isinstance(objects, str):
            objects = [
                objects
            ]

        for scene_object in objects:
            if not scene_object:
                continue

            validate_node(
                scene_object
            )

            cmds.sets(
                scene_object,
                edit=True,
                addElement=set_name
            )

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if parent_set:
        if cmds.objExists(parent_set):
            if cmds.nodeType(parent_set) != "objectSet":
                raise RuntimeError(
                    u"父 Set 名称被非 Object Set 节点占用：{}".format(
                        parent_set
                    )
                )
        else:
            parent_set = cmds.sets(
                name=parent_set,
                empty=True
            )

        cmds.sets(
            set_name,
            edit=True,
            addElement=parent_set
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return set_name


# =============================================================================
# Maya Native Callback
# =============================================================================

def create_native_event_callback(
        event_name,
        callback
):
    u"""
    创建 Maya ``MEventMessage`` Callback，并返回对应删除函数。

    Args:
        event_name (str):
            Maya Native Event 名称，例如 ``SelectionChanged``。
        callback (callable):
            Event 触发时由 Maya 调用的函数。

    Returns:
        callable:
        无参数删除函数；调用后移除本次创建的 Maya Callback。

    Raises:
        ValueError:
        ``event_name`` 为空时抛出。
        TypeError:
        ``callback`` 不是可调用对象时抛出。
    """
    if not event_name:
        raise ValueError(
            u"event_name 不能为空。"
        )

    if not callable(callback):
        raise TypeError(
            u"callback 必须是可调用对象。"
        )

    callback_id = om.MEventMessage.addEventCallback(
        event_name,
        callback
    )

    remove_callback = partial(
        om.MMessage.removeCallback,
        callback_id
    )

    return remove_callback


# =============================================================================
# Scene State
# =============================================================================

def get_current_scene_path():
    u"""
    返回当前 Maya Scene 的规范路径；未保存时返回空字符串。

    Returns:
        str:
        当前 Scene 的规范化文件路径；Untitled Scene 返回空字符串。
    """
    scene_path = cmds.file(
        query=True,
        sceneName=True
    )

    if not scene_path:
        return ""

    return file_utils.normalize_path(
        scene_path
    )


def is_scene_modified():
    u"""
    返回当前 Maya Scene 是否存在未保存修改。

    Returns:
        bool:
        当前 Scene 有未保存修改时返回 True，否则返回 False。
    """
    return bool(
        cmds.file(
            query=True,
            modified=True
        )
    )


def validate_scene_file(file_path):
    u"""
    检查 Maya Scene 输入文件是否存在，并返回规范化路径。

    Args:
        file_path (str):
            需要 Open / Import / Reference 的文件路径。

    Returns:
        str:
        经过 ``file_utils.normalize_path()`` 处理后的现有文件路径。

    Raises:
        ValueError:
        ``file_path`` 为空时抛出。
        RuntimeError:
        规范化后的文件路径不存在时抛出。
    """
    normalized_path = file_utils.normalize_path(
        file_path
    )

    if not normalized_path:
        raise ValueError(
            u"file_path 不能为空。"
        )

    if not os.path.isfile(normalized_path):
        raise RuntimeError(
            u"文件不存在：{}".format(
                normalized_path
            )
        )

    return normalized_path


# =============================================================================
# Scene IO
# =============================================================================

def open_scene(
        file_path,
        force=False,
        ignore_version=True
):
    u"""
    打开 Maya Scene；Core 不弹保存确认窗口。

    Args:
        file_path (str):
            需要打开的 Maya Scene 文件路径。
        force (bool):
            是否允许 Maya 强制打开文件；False 时若当前 Scene 有未保存修改会先拒绝操作。
        ignore_version (bool):
            是否让 Maya 忽略文件版本差异。

    Returns:
        str:
        成功打开后的规范化 Scene 文件路径。

    Raises:
        RuntimeError:
        文件不存在，或当前 Scene 有未保存修改且 ``force=False`` 时抛出。
    """
    normalized_path = validate_scene_file(
        file_path
    )

    if is_scene_modified() and not force:
        raise RuntimeError(
            u"当前场景存在未保存修改，请确认后使用 force=True 打开新场景。"
        )

    cmds.file(
        normalized_path,
        open=True,
        ignoreVersion=ignore_version,
        force=force
    )

    return normalized_path


def import_scene(
        file_path,
        ignore_version=True
):
    u"""
    将 Maya Scene 导入当前场景，并返回本次新创建节点。

    Args:
        file_path (str):
            需要 Import 的 Maya Scene 文件路径。
        ignore_version (bool):
            是否让 Maya 忽略文件版本差异。

    Returns:
        list[str]:
        本次 Import 新创建的 Maya Node；没有新节点时返回空列表。

    Raises:
        RuntimeError:
        输入文件不存在时抛出。
    """
    normalized_path = validate_scene_file(
        file_path
    )

    imported_nodes = cmds.file(
        normalized_path,
        i=True,
        ignoreVersion=ignore_version,
        returnNewNodes=True
    )

    if imported_nodes is None:
        imported_nodes = []

    return imported_nodes


def reference_scene(
        file_path,
        namespace=None,
        group_reference=False,
        group_name=None,
        ignore_version=True
):
    u"""
    在当前 Maya Scene 创建 Reference，并返回 Maya Reference Node。

    ``namespace`` 未指定时使用输入文件名 Stem。

    Args:
        file_path (str):
            需要 Reference 的 Maya Scene 文件路径。
        namespace (str | None):
            Reference Namespace；None 时使用文件名 Stem。
        group_reference (bool):
            是否让 Maya 为本次 Reference 创建 Reference Group。
        group_name (str | None):
            ``group_reference=True`` 时可选的 Reference Group 名称。
        ignore_version (bool):
            是否让 Maya 忽略文件版本差异。

    Returns:
        str:
        Maya 为本次 Reference 创建的 Reference Node 名称。

    Raises:
        RuntimeError:
        输入文件不存在时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    normalized_path = validate_scene_file(
        file_path
    )

    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if namespace is None:
        namespace = file_utils.get_file_stem(
            normalized_path
        )

    reference_kwargs = {
        "reference": True,
        "ignoreVersion": ignore_version,
        "namespace": namespace,
        "returnNewNodes": False,
    }

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if group_reference:
        reference_kwargs["groupReference"] = True

        if group_name:
            reference_kwargs["groupName"] = group_name

    reference_file = cmds.file(
        normalized_path,
        **reference_kwargs
    )

    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    reference_node = cmds.file(
        reference_file,
        query=True,
        referenceNode=True
    )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return reference_node

# =============================================================================
# Export
# =============================================================================

def ensure_fbx_plugin_loaded():
    u"""

        确保 Maya FBX Plugin ``fbxmaya`` 已加载。

        Returns:
            bool:
                当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。

    """
    plugin_name = "fbxmaya"

    if cmds.pluginInfo(
            plugin_name,
            query=True,
            loaded=True
    ):
        return True

    try:
        cmds.loadPlugin(
            plugin_name
        )
    except RuntimeError as error:
        raise RuntimeError(
            u"无法加载 FBX 插件：{}".format(
                error
            )
        )

    return True


def export_fbx(
        objects,
        file_path
):
    u"""
    把明确给定的 Maya Node 导出为 FBX，并恢复调用前 Selection。

    Args:
        objects (str | list[str]):
            需要导出的 Maya Node。
        file_path (str):
            最终 FBX 文件路径。

    Returns:
        str:
        规范化后的最终输出路径。

    Raises:
        ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not objects:
        raise ValueError(
            u"objects 不能为空。"
        )

    if isinstance(objects, str):
        objects = [
            objects
        ]

    export_objects = []

    # -------------------------------------------------------------------------
    # Step 02：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for scene_object in objects:
        if not scene_object:
            continue

        validate_node(
            scene_object
        )

        export_objects.append(
            scene_object
        )

    if not export_objects:
        raise ValueError(
            u"没有可导出的 Maya Node。"
        )

    normalized_path = file_utils.normalize_path(
        file_path
    )

    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if not normalized_path:
        raise ValueError(
            u"file_path 不能为空。"
        )

    parent_directory = os.path.dirname(
        normalized_path
    )

    if parent_directory:
        file_utils.ensure_directory(
            parent_directory
        )

    # -------------------------------------------------------------------------
    # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    ensure_fbx_plugin_loaded()

    previous_selection = get_selected_nodes(
        long=True,
        flatten=False
    )

    try:
        cmds.select(
            export_objects,
            replace=True
        )

        escaped_path = normalized_path.replace(
            '"',
            '\\"'
        )

        mel.eval(
            'FBXExport -f "{}" -s'.format(
                escaped_path
            )
        )
    finally:
        if previous_selection:
            cmds.select(
                previous_selection,
                replace=True
            )
        else:
            cmds.select(
                clear=True
            )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return normalized_path

# =============================================================================
# Scene Cleanup
# =============================================================================

default_cameras = [
    "persp",
    "top",
    "front",
    "side",
]

rig_history_types = [
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
]

constraint_types = [
    "parentConstraint",
    "pointConstraint",
    "orientConstraint",
    "scaleConstraint",
    "aimConstraint",
    "poleVectorConstraint",
]

anim_curve_types = [
    "animCurveTA",
    "animCurveTL",
    "animCurveTT",
    "animCurveTU",
]


# =============================================================================
# Common Query
# =============================================================================


def is_default_camera(node):
    u"""

        判断节点是否为 Maya 默认相机 Transform。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    short_name = str(node).rsplit("|", 1)[-1]
    return short_name in default_cameras


def is_referenced(node):
    u"""

        判断节点是否来自 Reference。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            object | bool:
            条件成立时返回 True，否则返回 False。

    """
    try:
        return cmds.referenceQuery(
            node,
            isNodeReferenced=True
        )
    except Exception:
        return False


def existing_nodes(nodes):
    u"""

        过滤不存在的节点、转换为 Long Path 并去重。

        该步骤在真正修改场景前统一执行，避免调用过程中遇到已经被前一个清理动作删除的节点。

        Args:
            nodes (str | list[str]):
                需要批量查询或处理的 Maya 节点名称或节点列表。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    result = []

    if not nodes:
        return result

    for node in nodes:
        if not node or not cmds.objExists(node):
            continue

        matches = cmds.ls(
            node,
            long=True
        ) or []
        resolved = matches[0] if matches else node

        if resolved not in result:
            result.append(resolved)

    return result


def all_transform_nodes():
    u"""

        返回全场景 Transform Long Path。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    return cmds.ls(
        type="transform",
        long=True
    ) or []


def sort_child_first(nodes):
    u"""

        按 DAG 深度从深到浅排序。

        Args:
            nodes (str | list[str]):
                需要批量查询或处理的 Maya 节点名称或节点列表。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    result = []

    for node in nodes:
        if node not in result:
            result.append(node)

    def get_depth(node):
        return node.count("|")

    result.sort(
        key=get_depth,
        reverse=True
    )

    return result


# =============================================================================
# Protection Query
# =============================================================================

def has_incoming_animation(node):
    u"""

        判断 Transform 是否存在 AnimCurve 输入。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            bool:
            条件成立时返回 True，否则返回 False。

    """
    for anim_type in anim_curve_types:
        connections = cmds.listConnections(
            node,
            source=True,
            destination=False,
            type=anim_type
        ) or []

        if connections:
            return True

    return False


def has_constraint(node):
    u"""

        判断节点是否存在常见 Constraint 输入。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            bool:
            条件成立时返回 True，否则返回 False。

    """
    connections = cmds.listConnections(
        node,
        source=True,
        destination=False
    ) or []

    for connection in connections:
        try:
            node_type = cmds.nodeType(connection)
        except Exception:
            continue

        if node_type in constraint_types:
            return True

    return False


def has_rig_history(node):
    u"""

        判断历史中是否存在需要保护的 Rig Deformer。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            bool:
            条件成立时返回 True，否则返回 False。

    """
    # -------------------------------------------------------------------------
    # Step 01：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    history = cmds.listHistory(
        node,
        pruneDagObjects=True
    ) or []

    # -------------------------------------------------------------------------
    # Step 02：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for history_node in history:
        try:
            node_type = cmds.nodeType(history_node)
        except Exception:
            continue

        if node_type in rig_history_types:
            return True

        # 未列进白名单但属于 geometryFilter 的节点同样按 Deformer 保护。
        try:
            if cmds.objectType(
                    history_node,
                    isAType="geometryFilter"
            ):
                return True
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # Step 03：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return False


def can_modify_transform(node):
    u"""

        判断节点是否允许进入 Transform 类清理操作。

        默认相机、Reference、非 Transform 都返回 False。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。

    """
    if not cmds.objExists(node):
        return False

    if is_default_camera(node):
        return False

    if is_referenced(node):
        return False

    if cmds.nodeType(node) != "transform":
        return False

    return True


# =============================================================================
# Delete Empty Group
# =============================================================================

def _collect_parent_candidates(nodes):
    """把输入节点一直向上追溯到 Root，收集可能在清理后变空的 Parent。"""
    parent_candidates = []

    for node in nodes:
        current = node

        while current:
            parents = cmds.listRelatives(
                current,
                parent=True,
                fullPath=True
            ) or []

            if not parents:
                break

            current = parents[0]

            if current not in parent_candidates:
                parent_candidates.append(current)

    return parent_candidates


def delete_empty_groups(nodes=None):
    u"""

        递归删除空 Transform Group。

        ``nodes=None`` 时扫描全场景；给定 nodes 时还会自动把它们的 Parent 加入候选，
        因为删除 Child 后原本非空的 Parent 可能变成空组。

        Args:
            nodes (str | list[str]):
                需要批量查询或处理的 Maya 节点名称或节点列表。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    # -------------------------------------------------------------------------
    # 步骤 1：建立候选节点列表。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if nodes is None:
        candidates = all_transform_nodes()
    else:
        candidates = existing_nodes(nodes)
        parent_candidates = _collect_parent_candidates(candidates)

        for parent in parent_candidates:
            if parent not in candidates:
                candidates.append(parent)

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    deleted_count = 0
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    changed = True

    # -------------------------------------------------------------------------
    # 步骤 2：循环检查直到本轮没有删除任何节点。
    #
    # 为什么需要循环：
    # Child 空组删除后，Parent 可能才刚刚变成空组，需要下一轮继续处理。
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    while changed:
        changed = False
        current_candidates = []

        for node in candidates:
            if cmds.objExists(node):
                current_candidates.append(node)

        current_candidates = sort_child_first(current_candidates)

        for node in current_candidates:
            if not can_modify_transform(node):
                continue

            shapes = cmds.listRelatives(
                node,
                shapes=True,
                fullPath=True
            ) or []
            children = cmds.listRelatives(
                node,
                children=True,
                fullPath=True
            ) or []

            if shapes or children:
                continue

            try:
                cmds.delete(node)
                deleted_count += 1
                changed = True
            except Exception as error:
                cmds.warning(
                    u"无法删除空组 {}：{}".format(
                        node,
                        error
                    )
                )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return deleted_count


# =============================================================================
# Delete History
# =============================================================================

def delete_history(nodes):
    u"""
    删除安全范围内的 Construction History。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        tuple: ``(processed_count, skipped_count)``。
    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    nodes = existing_nodes(nodes)
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    deleted_count = 0
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    skipped_count = 0

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in nodes:
        if not can_modify_transform(node):
            skipped_count += 1
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        ) or []

        if not shapes:
            continue

        # Rig Deformer 比建模 History 更重要，发现后整个对象跳过 Delete History。
        if has_rig_history(node):
            skipped_count += 1
            continue

        try:
            cmds.delete(
                node,
                constructionHistory=True
            )
            deleted_count += 1
        except Exception as error:
            cmds.warning(
                u"无法删除历史 {}：{}".format(
                    node,
                    error
                )
            )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return deleted_count, skipped_count


# =============================================================================
# Freeze Transform
# =============================================================================

def freeze_transformations(nodes):
    u"""

        Freeze 安全范围内的 Transform。

        有 Animation、Constraint 或 Rig Deformer 的节点一律跳过。

        Args:
            nodes (str | list[str]):
                需要批量查询或处理的 Maya 节点名称或节点列表。

        Returns:
            tuple:
            按当前 API 约定组织的结果元组。

    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    nodes = existing_nodes(nodes)
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    frozen_count = 0
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    skipped_count = 0

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in nodes:
        # 步骤 1：基础保护。
        if not can_modify_transform(node):
            skipped_count += 1
            continue

        # 步骤 2：Animation / Constraint / Deformer 保护。
        if has_incoming_animation(node):
            skipped_count += 1
            continue

        if has_constraint(node):
            skipped_count += 1
            continue

        if has_rig_history(node):
            skipped_count += 1
            continue

        # 步骤 3：正式 Freeze，并保留 Normal。
        try:
            cmds.makeIdentity(
                node,
                apply=True,
                translate=True,
                rotate=True,
                scale=True,
                normal=False,
                preserveNormals=True
            )
            frozen_count += 1
        except Exception as error:
            cmds.warning(
                u"无法冻结变换 {}：{}".format(
                    node,
                    error
                )
            )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return frozen_count, skipped_count


# =============================================================================
# Attribute / Pivot
# =============================================================================

def unlock_and_show_attributes(nodes):
    u"""

        解锁并显示标准 Translate / Rotate / Scale / Visibility 通道。

        Args:
            nodes (str | list[str]):
                需要批量查询或处理的 Maya 节点名称或节点列表。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    nodes = existing_nodes(nodes)
    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    attrs = [
        "tx",
        "ty",
        "tz",
        "rx",
        "ry",
        "rz",
        "sx",
        "sy",
        "sz",
        "v",
    ]
    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    changed_count = 0

    # -------------------------------------------------------------------------
    # Step 04：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in nodes:
        if is_referenced(node):
            continue

        for attr in attrs:
            if not cmds.attributeQuery(
                    attr,
                    node=node,
                    exists=True
            ):
                continue

            plug = "{}.{}".format(
                node,
                attr
            )

            try:
                cmds.setAttr(
                    plug,
                    lock=False
                )
                cmds.setAttr(
                    plug,
                    keyable=True
                )
                changed_count += 1
            except Exception:
                pass

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return changed_count


def center_pivot(nodes):
    u"""

        把可编辑、带 Shape 的 Transform Pivot 居中。

        Args:
            nodes (str | list[str]):
                需要批量查询或处理的 Maya 节点名称或节点列表。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    nodes = existing_nodes(nodes)
    centered_count = 0

    for node in nodes:
        if not can_modify_transform(node):
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        ) or []

        if not shapes:
            continue

        try:
            cmds.xform(
                node,
                centerPivots=True
            )
            centered_count += 1
        except Exception:
            pass

    return centered_count


# =============================================================================
# Unknown Node
# =============================================================================

def delete_unknown_nodes(nodes=None):
    u"""

        删除非 Reference Unknown 节点。

        Args:
            nodes (str | list[str]):
                需要批量查询或处理的 Maya 节点名称或节点列表。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if nodes is None:
        unknown_nodes = cmds.ls(
            type="unknown",
            long=True
        ) or []
    else:
        unknown_nodes = []

        for node in existing_nodes(nodes):
            if cmds.nodeType(node) == "unknown":
                unknown_nodes.append(node)

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    deleted_count = 0

    # -------------------------------------------------------------------------
    # Step 03：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
    for node in unknown_nodes:
        if is_referenced(node):
            continue

        try:
            cmds.delete(node)
            deleted_count += 1
        except Exception as error:
            cmds.warning(
                u"无法删除 Unknown 节点 {}：{}".format(
                    node,
                    error
                )
            )

    # -------------------------------------------------------------------------
    # Step 04：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return deleted_count


# =============================================================================
# Cleanup Runner
# =============================================================================

@undo_chunk
def run_cleanup(
        nodes,
        selected_only=True,
        delete_empty=True,
        delete_history_enabled=False,
        freeze_enabled=False,
        unlock_enabled=False,
        center_pivot_enabled=False,
        delete_unknown_enabled=True
):
    u"""

        按配置执行一次安全清理并返回统计字典。

        整个 Cleanup 被包装为一次 Maya Undo，方便用户完整回退一次清理操作。

        Args:
            nodes (str | list[str]):
                需要批量查询或处理的 Maya 节点名称或节点列表。
            selected_only (bool):
                清理 / 检查范围是否限制为当前 Maya Selection。
            delete_empty (bool):
                场景清理时是否删除确认无 Child / Shape 的空 Transform。
            delete_history_enabled (bool):
                清理流程是否执行 Modeling History 删除。
            freeze_enabled (bool):
                清理流程是否执行 Freeze Transform。
            unlock_enabled (bool):
                清理流程是否解除可安全处理的 Locked Channel。
            center_pivot_enabled (bool):
                清理流程是否执行 Center Pivot。
            delete_unknown_enabled (bool):
                清理流程是否删除确认无用的 Unknown Node。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

    """
    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    result = {}

    # 步骤 1：空组与 Unknown 可以根据 selected_only 决定局部 / 全场景范围。
    if delete_empty:
        empty_scope = nodes

        if not selected_only:
            empty_scope = None

        result["empty_groups"] = delete_empty_groups(
            empty_scope
        )

    # 步骤 2：History / Freeze 始终针对明确传入节点，并返回 Processed / Skipped。
    # -------------------------------------------------------------------------
    # Step 02：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if delete_history_enabled:
        deleted_count, skipped_count = delete_history(nodes)
        result["history"] = {
            "processed": deleted_count,
            "skipped": skipped_count,
        }

    if freeze_enabled:
        frozen_count, skipped_count = freeze_transformations(nodes)
        result["freeze"] = {
            "processed": frozen_count,
            "skipped": skipped_count,
        }

    # 步骤 3：其它安全清理。
    # -------------------------------------------------------------------------
    # Step 03：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if unlock_enabled:
        result["attributes"] = unlock_and_show_attributes(nodes)

    if center_pivot_enabled:
        result["pivot"] = center_pivot(nodes)

    # -------------------------------------------------------------------------
    # Step 04：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
    if delete_unknown_enabled:
        unknown_scope = nodes

        if not selected_only:
            unknown_scope = None

        result["unknown"] = delete_unknown_nodes(
            unknown_scope
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result

__all__ = [
    "open_undo_chunk",
    "close_undo_chunk",
    "undo_chunk",
    "validate_node",
    "ensure_nodes_available",
    "get_long_name",
    "create_node",
    "get_nodes_by_type",
    "get_selected_nodes",
    "ensure_object_set",
    "create_native_event_callback",
    "get_current_scene_path",
    "is_scene_modified",
    "validate_scene_file",
    "open_scene",
    "import_scene",
    "reference_scene",
    "ensure_fbx_plugin_loaded",
    "export_fbx",
    "is_default_camera",
    "is_referenced",
    "existing_nodes",
    "all_transform_nodes",
    "sort_child_first",
    "has_incoming_animation",
    "has_constraint",
    "has_rig_history",
    "can_modify_transform",
    "delete_empty_groups",
    "delete_history",
    "freeze_transformations",
    "unlock_and_show_attributes",
    "center_pivot",
    "delete_unknown_nodes",
    "run_cleanup",
]
