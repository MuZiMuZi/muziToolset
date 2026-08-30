# coding=utf-8
u"""
Scene Utils
===========

Maya Scene 领域的通用底层工具。

模块职责
--------
这个模块统一管理“场景”这一领域的基础能力，包括：

    - Maya Undo Chunk；
    - Maya 节点创建与基础校验；
    - 当前 Selection 查询；
    - Object Set 创建与维护；
    - Maya Native Event Callback；
    - 当前 Scene 路径与修改状态；
    - Maya Scene 打开 / 导入 / Reference；
    - 当前选择导出 FBX。

原来的 ``scene_io_utils.py`` 与 ``scene_utils.py`` 都围绕 Maya Scene 生命周期工作，
当前规模没有必要拆成两个文件。合并后调用方只需要记住：

    和 Maya Scene 本身有关的操作 -> core.scene_utils
    只和硬盘文件 / JSON 有关的操作 -> core.file_utils

当前公开方法
------------
Undo：
    undo_chunk(function)
        将一个函数执行过程包装成一个 Maya Undo Chunk。

Node：
    validate_node(node)
        检查 Maya 节点是否存在。

    get_long_name(node)
        获取唯一 DAG 长路径；非 DAG 节点返回原名称。

    create_node(node_type, name, match_node=None, parent=None)
        创建 Maya 节点，可匹配另一个 Transform 并指定 Parent。

Selection：
    get_selected_nodes(node_type=None, long=True, flatten=True)
        获取当前 Maya Selection，可按节点类型过滤。

    require_selected_nodes(node_type=None, minimum_count=1)
        获取 Selection，并检查最小选择数量。

Object Set：
    ensure_object_set(set_name, objects=None, parent_set=None)
        创建或复用 Object Set，并可加入对象或父 Set。

Callback：
    create_native_event_callback(event_name, callback)
        创建 Maya MEventMessage Callback，并返回删除 Callback 的函数。

Scene 状态：
    get_current_scene_path()
        获取当前 Maya Scene 的绝对路径。

    is_scene_modified()
        查询当前 Scene 是否存在未保存修改。

    validate_scene_file(file_path)
        检查一个 Maya Scene 文件路径是否真实存在。

Scene IO：
    open_scene(file_path, force=False, ignore_version=True)
        打开 Maya Scene；Core 不弹确认窗口。

    import_scene(file_path, ignore_version=True)
        将 Maya Scene 导入当前场景，并返回新创建节点。

    reference_scene(file_path, namespace=None, group_reference=False,
                    group_name=None, ignore_version=True)
        在当前 Scene 创建 Reference。

FBX：
    ensure_fbx_plugin_loaded()
        确保 Maya fbxmaya 插件已经加载。

    export_selected_fbx(file_path)
        将当前 Selection 导出为 FBX。

本模块不负责
------------
- PySide 文件选择窗口；
- “是否保存当前文件”的 QMessageBox；
- Constraint / Matrix / Curve / Surface / Skin 等具体 Rig 业务；
- 项目级 Publish / Version / Shot 管理。

为什么 Core 不弹保存确认窗口
----------------------------
``open_scene()`` 可能遇到当前 Scene 有未保存修改。
Core 不知道调用它的是批处理、自动测试还是用户点击的 UI，因此不能擅自弹窗口。
正确流程是：

    Tool / App
        -> 询问用户是否继续
        -> 用户确认后传 force=True
        -> scene_utils.open_scene()

这样底层 API 才能同时用于 UI、自动化和测试。
"""

from __future__ import print_function

import os
from functools import partial
from functools import wraps

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

from . import file_utils


# =============================================================================
# Undo
# =============================================================================

def undo_chunk(function):
    u"""
    将一个函数执行过程包装成一个 Maya Undo Chunk。

    Maya 中一个工具通常会创建多个节点、设置多个属性。
    如果每一步都成为独立 Undo，用户需要连续撤销很多次。
    这个 Decorator 可以把整个工具操作合并成一次 Undo。

    Args:
        function (object):
            `function` 对应的输入数据。

    Returns:
        object:
        方法执行后的结果数据。
    """
    @wraps(function)
    def wrapped(*args, **kwargs):
        # 步骤 1：打开 Undo Chunk。
        cmds.undoInfo(
            openChunk=True,
            chunkName=function.__name__
        )

        try:
            # 步骤 2：执行真正的工具逻辑。
            return function(
                *args,
                **kwargs
            )
        finally:
            # 步骤 3：无论函数成功还是抛异常，都必须关闭 Chunk。
            # 如果不使用 finally，异常可能导致 Maya Undo 栈处于错误状态。
            cmds.undoInfo(
                closeChunk=True
            )

    return wrapped


# =============================================================================
# Node - 节点校验与创建
# =============================================================================

def validate_node(node):
    u"""
    检查 Maya 节点是否存在。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        bool: 节点存在时返回 True。

    Raises:
        RuntimeError: 节点名称为空或场景中不存在。
    """
    # 步骤 1：空名称没有任何查询意义，直接报错。
    if not node:
        raise RuntimeError(u"节点名称不能为空。")

    # 步骤 2：使用 objExists 检查 DAG / DG 节点。
    if not cmds.objExists(node):
        raise RuntimeError(
            u"Maya 节点不存在：{}".format(node)
        )

    return True


def get_long_name(node):
    u"""
    返回唯一 Maya DAG 长路径；非 DAG 节点返回原名称。

    当场景存在两个同名 DAG 节点时，只使用短名会造成工具操作对象不确定。
    因此如果查询结果不唯一，本函数会要求调用方提供完整路径。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：先确认节点存在。
    validate_node(node)

    # 步骤 2：要求 Maya 返回 Long Name。
    matches = cmds.ls(
        node,
        long=True
    )

    if matches is None:
        matches = []

    # DG 节点没有 DAG Path，这种情况直接保留原名。
    if not matches:
        return node

    # 步骤 3：短名对应多个节点时拒绝猜测。
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
        match_node=None,
        parent=None
):
    u"""
    创建 Maya 节点，可选择匹配另一个 Transform 并指定 Parent。

    Args:
        node_type (str):
            Maya 节点类型，例如 transform / joint。
        name (str):
            新节点名称。
        match_node (str/None):
            可选匹配目标。
        parent (str/None):
            可选父节点。

    Returns:
        str: 新创建节点名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：检查创建参数。
    # -------------------------------------------------------------------------
    if not node_type:
        raise ValueError(u"node_type 不能为空。")

    if not name:
        raise ValueError(u"节点名称不能为空。")

    if cmds.objExists(name):
        raise RuntimeError(
            u"节点已经存在：{}".format(name)
        )

    # -------------------------------------------------------------------------
    # 步骤 2：创建节点。
    # -------------------------------------------------------------------------
    node = cmds.createNode(
        node_type,
        name=name
    )

    # -------------------------------------------------------------------------
    # 步骤 3：如果提供 match_node，则匹配位置和旋转。
    #
    # Scale 默认不匹配，因为创建 Rig Helper / Group 时通常不希望继承
    # 模型或其它节点的非 1 Scale。
    # -------------------------------------------------------------------------
    if match_node:
        validate_node(match_node)

        cmds.matchTransform(
            node,
            match_node,
            position=True,
            rotation=True,
            scale=False
        )

    # -------------------------------------------------------------------------
    # 步骤 4：如果指定 Parent，则放入层级。
    # Maya parent() 可能返回更新后的 DAG Path，所以使用返回值刷新 node。
    # -------------------------------------------------------------------------
    if parent:
        validate_node(parent)

        parent_result = cmds.parent(
            node,
            parent
        )

        if parent_result:
            node = parent_result[0]

    return node


# =============================================================================
# Selection - 当前选择
# =============================================================================

def get_selected_nodes(
        node_type=None,
        long=True,
        flatten=True
):
    u"""
    返回当前 Maya Selection，可按节点类型过滤。

    Component Selection 在指定 node_type 时会被跳过，
    因为 component 本身不是一个可直接 nodeType 查询的 DG 节点。

    Args:
        node_type (str):
            `node_type` 对应的名称、标记或字符串参数。
        long (bool):
            是否启用 `long` 对应的处理。
        flatten (bool):
            是否启用 `flatten` 对应的处理。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 步骤 1：获取当前 Selection。
    selected_nodes = cmds.ls(
        selection=True,
        long=long,
        flatten=flatten
    )

    if selected_nodes is None:
        selected_nodes = []

    # 步骤 2：没有类型要求时直接返回。
    if node_type is None:
        return selected_nodes

    # 步骤 3：按 Maya nodeType 过滤。
    filtered_nodes = []

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

        filtered_nodes.append(selected_node)

    return filtered_nodes


def require_selected_nodes(
        node_type=None,
        minimum_count=1
):
    u"""
    获取当前选择，并检查最小数量。

    这个函数适合 Tool 在执行前快速做输入检查。
    不满足要求时会抛 RuntimeError，由 UI 层决定如何显示错误。

    Args:
        node_type (str):
            `node_type` 对应的名称、标记或字符串参数。
        minimum_count (int):
            `minimum_count` 对应的整数参数。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：调用统一 Selection 查询。
    selected_nodes = get_selected_nodes(
        node_type=node_type,
        long=True,
        flatten=True
    )

    # 步骤 2：检查数量。
    if len(selected_nodes) < minimum_count:
        if node_type:
            raise RuntimeError(
                u"请至少选择 {} 个 {} 节点。".format(
                    minimum_count,
                    node_type
                )
            )

        raise RuntimeError(
            u"请至少选择 {} 个 Maya 节点。".format(
                minimum_count
            )
        )

    return selected_nodes


# =============================================================================
# Object Set
# =============================================================================

def ensure_object_set(
        set_name,
        objects=None,
        parent_set=None
):
    u"""
    创建或复用 Object Set，并可加入对象和父 Set。

    Args:
        set_name (str):
            Set 名称。
        objects (list/str/None):
            可选需要加入 Set 的对象。
        parent_set (str/None):
            可选父 Set。

    Returns:
        str: Object Set 名称。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：创建或验证目标 Set。
    # -------------------------------------------------------------------------
    if not set_name:
        raise ValueError(u"Set 名称不能为空。")

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
    # 步骤 2：把对象加入 Set。
    # -------------------------------------------------------------------------
    if objects is not None:
        if isinstance(objects, str):
            objects = [objects]

        for scene_object in objects:
            if not scene_object:
                continue

            validate_node(scene_object)

            cmds.sets(
                scene_object,
                edit=True,
                forceElement=set_name
            )

    # -------------------------------------------------------------------------
    # 步骤 3：如果需要，再创建 / 验证父 Set，并把子 Set 加进去。
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
            forceElement=parent_set
        )

    return set_name


# =============================================================================
# Maya Native Callback
# =============================================================================

def create_native_event_callback(
        event_name,
        callback
):
    u"""
    创建 Maya MEventMessage Callback。

    Args:
        event_name (str):
            Maya Event 名称。
        callback (callable):
            Event 触发后执行的函数。

    Returns:
        callable: 调用返回函数即可删除这个 Callback。

        为什么返回 remove 函数：
        Tool / System 不需要保存 OpenMaya callback id 的实现细节，
        只需要在关闭或销毁时调用返回值即可清理监听。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        TypeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：验证输入。
    if not event_name:
        raise ValueError(u"event_name 不能为空。")

    if not callable(callback):
        raise TypeError(u"callback 必须是可调用对象。")

    # 步骤 2：向 Maya 注册 Native Callback。
    callback_id = om.MEventMessage.addEventCallback(
        event_name,
        callback
    )

    # 步骤 3：包装删除行为并返回。
    remove_callback = partial(
        om.MMessage.removeCallback,
        callback_id
    )

    return remove_callback


# =============================================================================
# Scene 状态与文件路径
# =============================================================================

def get_current_scene_path():
    u"""
    返回当前 Maya Scene 的规范绝对路径；未保存时返回空字符串。

    Returns:
        object | str:
        方法执行后的结果数据。
    """
    # 步骤 1：向 Maya 查询当前 Scene 文件名。
    scene_path = cmds.file(
        query=True,
        sceneName=True
    )

    if not scene_path:
        return ""

    # 步骤 2：路径格式统一交给 file_utils。
    return file_utils.normalize_path(scene_path)


def is_scene_modified():
    u"""
    返回当前 Maya Scene 是否存在未保存修改。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return bool(
        cmds.file(
            query=True,
            modified=True
        )
    )


def validate_scene_file(file_path):
    u"""
    检查 Maya Scene 文件是否存在，并返回规范化路径。

    这里不强制检查 .ma / .mb 扩展名，因为 Maya 还可能通过插件读取其它格式。
    Core 只负责确认路径真实存在。

    Args:
        file_path (str):
            需要读取或写入的文件路径。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：先统一路径分隔符和绝对路径格式。
    normalized_path = file_utils.normalize_path(file_path)

    if not normalized_path:
        raise ValueError(u"file_path 不能为空。")

    # 步骤 2：确认硬盘文件存在。
    if not os.path.isfile(normalized_path):
        raise RuntimeError(
            u"文件不存在：{}".format(normalized_path)
        )

    return normalized_path


# =============================================================================
# Scene IO - Open / Import / Reference
# =============================================================================

def open_scene(file_path, force=False, ignore_version=True):
    u"""
    打开 Maya Scene。

    当当前 Scene 有未保存修改并且 force=False 时，本函数不会弹 UI，
    而是抛出 RuntimeError。上层 Tool / App 可以先询问用户，再重新调用 force=True。

    Args:
        file_path (str):
            需要读取或写入的文件路径。
        force (bool):
            是否强制覆盖已有连接、状态或结果。
        ignore_version (bool):
            是否启用 `ignore_version` 对应的处理。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：检查目标文件。
    normalized_path = validate_scene_file(file_path)

    # 步骤 2：保护当前未保存场景。
    if is_scene_modified() and not force:
        raise RuntimeError(
            u"当前场景存在未保存修改，请确认后使用 force=True 打开新场景。"
        )

    # 步骤 3：执行 Maya Scene Open。
    cmds.file(
        normalized_path,
        open=True,
        ignoreVersion=ignore_version,
        force=force
    )

    return normalized_path


def import_scene(file_path, ignore_version=True):
    u"""
    将 Maya Scene 导入当前场景。

    Args:
        file_path (str):
            需要读取或写入的文件路径。
        ignore_version (bool):
            是否启用 `ignore_version` 对应的处理。

    Returns:
        list: Maya 本次 Import 新创建的节点。
    """
    # 步骤 1：验证文件。
    normalized_path = validate_scene_file(file_path)

    # 步骤 2：导入并要求 Maya 返回新节点列表。
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
    在当前 Maya Scene 中创建 Reference。

    namespace 未指定时，默认使用文件名 Stem。

    Args:
        file_path (str):
            需要读取或写入的文件路径。
        namespace (object):
            `namespace` 对应的输入数据。
        group_reference (bool):
            是否启用 `group_reference` 对应的处理。
        group_name (str):
            `group_name` 对应的 Maya 节点或资源名称。
        ignore_version (bool):
            是否启用 `ignore_version` 对应的处理。

    Returns:
        object:
        方法执行后的结果数据。
    """
    # 步骤 1：验证文件路径。
    normalized_path = validate_scene_file(file_path)

    # 步骤 2：没有指定 Namespace 时，从文件名自动生成。
    if namespace is None:
        namespace = file_utils.get_file_stem(normalized_path)

    # 步骤 3：准备 Maya cmds.file Reference 参数。
    reference_kwargs = {
        "reference": True,
        "ignoreVersion": ignore_version,
        "namespace": namespace,
        "returnNewNodes": False,
    }

    # 步骤 4：按需要把 Reference 放入指定 Group。
    if group_reference:
        reference_kwargs["groupReference"] = True

        if group_name:
            reference_kwargs["groupName"] = group_name

    # 步骤 5：创建 Reference。
    reference_node = cmds.file(
        normalized_path,
        **reference_kwargs
    )

    return reference_node


# =============================================================================
# FBX Export
# =============================================================================

def ensure_fbx_plugin_loaded():
    u"""
    确保 Maya FBX 插件 fbxmaya 已加载。

    Returns:
        bool: 成功加载或本来已加载时返回 True。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    plugin_name = "fbxmaya"

    # 步骤 1：插件已经加载时直接返回。
    if cmds.pluginInfo(
            plugin_name,
            query=True,
            loaded=True
    ):
        return True

    # 步骤 2：尝试加载插件，并把 Maya RuntimeError 转成更明确的错误。
    try:
        cmds.loadPlugin(plugin_name)
    except RuntimeError as error:
        raise RuntimeError(
            u"无法加载 FBX 插件：{}".format(error)
        )

    return True


def export_selected_fbx(file_path):
    u"""
    将当前 Maya Selection 导出为 FBX 文件。

    Args:
        file_path (str):
            输出 FBX 路径。

    Returns:
        str: 规范化后的最终输出路径。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：读取并验证当前 Selection。
    # -------------------------------------------------------------------------
    selected_nodes = cmds.ls(
        selection=True,
        long=True
    )

    if selected_nodes is None:
        selected_nodes = []

    if not selected_nodes:
        raise RuntimeError(u"导出 FBX 前请先选择对象。")

    # -------------------------------------------------------------------------
    # 步骤 2：整理输出路径，并确保父目录存在。
    # -------------------------------------------------------------------------
    normalized_path = file_utils.normalize_path(file_path)

    if not normalized_path:
        raise ValueError(u"file_path 不能为空。")

    parent_directory = os.path.dirname(normalized_path)

    if parent_directory:
        file_utils.ensure_directory(parent_directory)

    # -------------------------------------------------------------------------
    # 步骤 3：确保 FBX Plugin 已经加载。
    # -------------------------------------------------------------------------
    ensure_fbx_plugin_loaded()

    # -------------------------------------------------------------------------
    # 步骤 4：使用 Maya FBXExport MEL 命令导出当前选择。
    #
    # FBX 插件的完整导出接口主要通过 MEL 暴露，因此这里保留 mel.eval，
    # 而不是为了形式统一强行改成不存在的 cmds API。
    # -------------------------------------------------------------------------
    mel.eval(
        'FBXExport -f "{}" -s'.format(normalized_path)
    )

    return normalized_path


__all__ = [
    "undo_chunk",
    "validate_node",
    "get_long_name",
    "create_node",
    "get_selected_nodes",
    "require_selected_nodes",
    "ensure_object_set",
    "create_native_event_callback",
    "get_current_scene_path",
    "is_scene_modified",
    "validate_scene_file",
    "open_scene",
    "import_scene",
    "reference_scene",
    "ensure_fbx_plugin_loaded",
    "export_selected_fbx",
]
