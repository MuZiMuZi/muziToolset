# coding=utf-8
u"""
Animation Utils
===============

Maya 动画领域的通用底层工具。

模块职责
--------
这个模块统一管理“动画”这一领域的基础能力，不再把动画操作和动画 JSON IO
拆成两个很小的文件。调用方只需要记住：只要功能属于动画，就优先从
``core.animation_utils`` 中查找。

当前公开方法
------------
AnimCurve 查询与清理：
    get_animation_curves(nodes=None)
        获取全场景或指定节点上的 AnimCurve。

    clear_animation_keys(nodes=None)
        删除 AnimCurve；nodes=None 时可以清理全场景动画曲线。

Transform / Controller Reset：
    can_set_attribute(attribute)
        判断一个 Plug 是否存在、未锁定并且可以直接写值。

    reset_transform_channels(nodes, translate=True, rotate=True, scale=True)
        将 Transform 的 Translate / Rotate / Scale 恢复 Maya 标准默认值。

    reset_controls(controls=None, pattern="ctrl_*")
        批量重置控制器标准 TRS，不处理角色专属自定义属性。

动画数据查询：
    normalize_nodes(nodes)
        把单节点或节点列表整理成有效 Maya 节点列表。

    get_keyed_plugs(node)
        获取节点上真正存在关键帧的可动画 Plug。

    get_attribute_name(plug)
        从完整 Plug 中提取 Attribute 名称。

    get_key_data(plug)
        获取一个 Plug 的基础 Key Time / Value 数据。

    collect_animation(nodes)
        将多个节点的动画整理成可 JSON 序列化的数据结构。

动画 JSON 导出：
    export_animation(nodes, file_path)
        将指定节点动画导出为 Muzi Animation JSON。

    export_selected_animation(file_path)
        将当前 Maya Selection 的动画导出为 JSON。

动画 JSON 导入：
    validate_animation_data(data)
        检查 Muzi Animation JSON 的格式名、版本和数据结构。

    resolve_target_node(source_node, node_map=None)
        根据可选映射表解析动画导入目标节点。

    apply_attribute_keys(target_node, attribute_info, clear_existing=False)
        将一个属性的 Key 数据写回 Maya。

    import_animation(file_path, node_map=None, clear_existing=False, strict=False)
        从 Muzi Animation JSON 恢复动画关键帧。

数据流
------
导出：
    Maya Node
        -> Keyed Plug
        -> Key Time / Value
        -> collect_animation()
        -> file_utils.write_json()

导入：
    JSON File
        -> file_utils.read_json()
        -> validate_animation_data()
        -> Node / Attribute
        -> cmds.setKeyframe()

本模块不负责
------------
- PySide 文件选择窗口；
- 角色专属 IK/FK、Stretch、Follow、Space 等默认值；
- Animation Layer / Trax / Clip 等高级动画系统；
- Constraint、Matrix、Controller Rig 等绑定系统；
- 完整切线、Infinity、Weighted Tangent 等高级动画交换格式。

设计原则
--------
1. Core 不弹 UI，文件路径由上层 Tool / System 提供；
2. JSON 文件读写统一复用 ``core.file_utils``；
3. 不硬编码任何具体角色名称和属性；
4. 普通流程使用完整 for 循环，方便在 Maya Script Editor 中逐步调试；
5. 当前动画 JSON version=1 只保存 Time / Value，未来扩展格式时必须升级版本。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import file_utils


# =============================================================================
# 模块常量
# =============================================================================

# Maya 常见 AnimCurve 类型。
#
# animCurveTA : Angle
# animCurveTL : Linear
# animCurveTT : Time
# animCurveTU : Unitless
#
# 集中维护这个列表，后续查询和清理动画时不需要在多个函数中重复声明。
anim_curve_types = [
    "animCurveTA",
    "animCurveTL",
    "animCurveTT",
    "animCurveTU",
]

# Muzi Animation JSON 的文件标识和版本号。
# 导入阶段会检查这两个值，避免普通 JSON 被误当成动画文件读取。
format_name = "muzi_animation"
format_version = 1


# =============================================================================
# AnimCurve 查询与清理
# =============================================================================

def get_animation_curves(nodes=None):
    u"""
    获取 AnimCurve 节点。

    Args:
        nodes (list/str/None):
            None：查询整个 Maya 场景中的 AnimCurve； str：查询一个节点的输入动画曲线； list：查询多个节点的输入动画曲线。

    Returns:
        list: 去重后的 AnimCurve 节点列表。
    """
    result = []

    # -------------------------------------------------------------------------
    # 步骤 1：没有指定节点时，按 AnimCurve 类型扫描整个场景。
    #
    # 这样保留了早期 Pipeline.clear_keys() 的全场景使用习惯，
    # 但“查询”和“删除”现在已经拆开，调用方可以先检查结果再决定是否清理。
    # -------------------------------------------------------------------------
    if nodes is None:
        for anim_curve_type in anim_curve_types:
            curves = cmds.ls(
                type=anim_curve_type,
                long=True
            )

            if curves is None:
                curves = []

            for curve in curves:
                if curve in result:
                    continue

                result.append(curve)

        return result

    # -------------------------------------------------------------------------
    # 步骤 2：统一输入数据结构。
    # 单个字符串转成 list，后面的 Maya 查询只需要维护一套循环。
    # -------------------------------------------------------------------------
    if isinstance(nodes, str):
        nodes = [nodes]

    # -------------------------------------------------------------------------
    # 步骤 3：逐个节点查询输入 AnimCurve，并去重。
    # -------------------------------------------------------------------------
    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        for anim_curve_type in anim_curve_types:
            curves = cmds.listConnections(
                node,
                source=True,
                destination=False,
                type=anim_curve_type
            )

            if curves is None:
                curves = []

            for curve in curves:
                if curve in result:
                    continue

                result.append(curve)

    # -------------------------------------------------------------------------
    # 步骤 4：返回纯数据结果，不在 Core 中修改 Selection 或弹出窗口。
    # -------------------------------------------------------------------------
    return result


def clear_animation_keys(nodes=None):
    u"""
    删除 AnimCurve，并返回实际删除的曲线节点名称。

    Args:
        nodes (list/str/None):
            None 时删除全场景 AnimCurve； 给定节点时只删除这些节点的输入 AnimCurve。

    Returns:
        list: 实际删除的 AnimCurve 名称。

    Notes:
        这个函数的语义是“删除动画曲线节点”。
            如果以后需要只删除某一个时间范围的 Key，应新增独立 API，
            不要让一个函数同时承担两种不同的清理行为。
    """
    # 步骤 1：先查询需要删除的曲线。
    animation_curves = get_animation_curves(
        nodes=nodes
    )

    deleted_curves = []

    # 步骤 2：逐条确认节点仍存在，然后删除。
    for animation_curve in animation_curves:
        if not cmds.objExists(animation_curve):
            continue

        deleted_curves.append(animation_curve)
        cmds.delete(animation_curve)

    # 步骤 3：返回删除记录，方便 Tool 和 Smoke Test 使用。
    return deleted_curves


# =============================================================================
# Transform / Controller Reset
# =============================================================================

def can_set_attribute(attribute):
    u"""
    判断属性是否可以被安全直接设置。

    属性必须同时满足：
        1. Plug 存在；
        2. Attribute 没有被 Lock；
        3. Maya 当前认为它是 Settable。
    这样可以避免 Reset 时强行覆盖 Constraint、Connection 或锁定通道。

    Args:
        attribute (str):
            Maya Attribute 或完整 Plug 名称。

    Returns:
        bool:
            方法执行后的结果数据。
    """
    # 步骤 1：Plug 不存在时直接返回 False。
    if not cmds.objExists(attribute):
        return False

    # 步骤 2：检查 Lock 和 Settable 状态。
    try:
        if cmds.getAttr(attribute, lock=True):
            return False

        if not cmds.getAttr(attribute, settable=True):
            return False
    except Exception:
        # 特殊 Maya 属性在状态查询时可能抛出异常。
        # Reset 属于批处理操作，这里选择安全跳过，而不是中断整个流程。
        return False

    return True


def reset_transform_channels(
        nodes,
        translate=True,
        rotate=True,
        scale=True
):
    u"""
    将 Transform 的标准 TRS 恢复 Maya 默认值。

    默认值：
        Translate -> 0
        Rotate    -> 0
        Scale     -> 1

    Args:
        nodes (list/str):
            需要重置的 Maya 节点。
        translate (bool):
            是否重置 Translate。
        rotate (bool):
            是否重置 Rotate。
        scale (bool):
            是否重置 Scale。

    Returns:
        list: 至少成功修改过一个属性的节点。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：统一输入格式。
    # -------------------------------------------------------------------------
    if isinstance(nodes, str):
        nodes = [nodes]

    if nodes is None:
        nodes = []

    reset_nodes = []

    # -------------------------------------------------------------------------
    # 步骤 2：根据开关准备需要重置的属性列表。
    #
    # Translate / Rotate 默认值是 0，Scale 默认值是 1，
    # 因此分成两组处理，避免在循环内部反复判断属性类别。
    # -------------------------------------------------------------------------
    zero_attributes = []
    one_attributes = []

    if translate:
        zero_attributes.append("translateX")
        zero_attributes.append("translateY")
        zero_attributes.append("translateZ")

    if rotate:
        zero_attributes.append("rotateX")
        zero_attributes.append("rotateY")
        zero_attributes.append("rotateZ")

    if scale:
        one_attributes.append("scaleX")
        one_attributes.append("scaleY")
        one_attributes.append("scaleZ")

    # -------------------------------------------------------------------------
    # 步骤 3：逐个 Maya 节点执行 Reset。
    # -------------------------------------------------------------------------
    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        changed = False

        # 步骤 3.1：Translate / Rotate 归零。
        for attribute_name in zero_attributes:
            attribute = "{}.{}".format(
                node,
                attribute_name
            )

            if not can_set_attribute(attribute):
                continue

            cmds.setAttr(attribute, 0)
            changed = True

        # 步骤 3.2：Scale 恢复为 1。
        for attribute_name in one_attributes:
            attribute = "{}.{}".format(
                node,
                attribute_name
            )

            if not can_set_attribute(attribute):
                continue

            cmds.setAttr(attribute, 1)
            changed = True

        # 只有真正修改过属性的节点才加入结果。
        if changed:
            reset_nodes.append(node)

    # -------------------------------------------------------------------------
    # 步骤 4：返回实际修改结果。
    # -------------------------------------------------------------------------
    return reset_nodes


def reset_controls(
        controls=None,
        pattern="ctrl_*"
):
    u"""
    批量重置控制器标准 TRS。

    Args:
        controls (list/str/None):
            指定时重置给定控制器； None 时按 pattern 从场景中查找 Transform。
        pattern (str):
            controls=None 时使用的 Maya 名称匹配规则。

    Returns:
        list: 实际修改过的控制器。

    Notes:
        这里只重置标准 TRS。
            IkFk、Stretch、Follow、Space 等角色专属属性必须由对应 Rig System
            自己定义默认值，不能再次硬编码到通用 Core。
    """
    # 步骤 1：没有显式传入控制器时，按命名规则自动查找。
    if controls is None:
        controls = cmds.ls(
            pattern,
            type="transform",
            long=True
        )

        if controls is None:
            controls = []

    # 步骤 2：复用标准 Transform Reset。
    return reset_transform_channels(
        nodes=controls,
        translate=True,
        rotate=True,
        scale=True
    )


# =============================================================================
# Animation JSON - 数据查询
# =============================================================================

def normalize_nodes(nodes):
    u"""
    将单个节点或节点列表整理成有效 Maya 节点列表。

    不存在的节点会被跳过，避免批量动画导出因为一个坏节点全部失败。

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object | list:
            方法执行后的结果数据。
    """
    if nodes is None:
        return []

    if isinstance(nodes, str):
        nodes = [nodes]

    valid_nodes = []

    # 步骤 1：逐个检查节点。
    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        valid_nodes.append(node)

    # 步骤 2：返回过滤后的有效节点。
    return valid_nodes


def get_keyed_plugs(node):
    u"""
    返回节点上当前真正存在关键帧的可动画 Plug。

    ``cmds.listAnimatable`` 只能说明属性“可以动画”，并不能说明它已经有 Key。
    因此这里还会使用 ``keyframeCount`` 做第二次过滤。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object | list:
            方法执行后的结果数据。
    """
    if not cmds.objExists(node):
        return []

    # 步骤 1：取得可动画 Plug。
    animatable_plugs = cmds.listAnimatable(node)

    if animatable_plugs is None:
        animatable_plugs = []

    keyed_plugs = []

    # 步骤 2：只保留真正有 Key 的 Plug。
    for plug in animatable_plugs:
        key_count = cmds.keyframe(
            plug,
            query=True,
            keyframeCount=True
        )

        if not key_count:
            continue

        if plug not in keyed_plugs:
            keyed_plugs.append(plug)

    return keyed_plugs


def get_attribute_name(plug):
    u"""
    从 ``node.attribute`` 形式的完整 Plug 中取得 Attribute 名称。

    Args:
        plug (str):
            完整 Maya Plug 名称，例如 node.translateX。

    Returns:
        object | str:
            方法执行后的结果数据。
    """
    if "." not in plug:
        return ""

    return plug.split(".", 1)[1]


def get_key_data(plug):
    u"""
    获取一个 Plug 的基础 Key Time / Value 数据。

    Args:
        plug (str):
            完整 Maya Plug 名称，例如 node.translateX。

    Returns:
        list:
        [
        {"time": 1.0, "value": 0.0},
        {"time": 10.0, "value": 5.0},
        ]

        当前 version=1 只保存 Time / Value。
        如果未来增加 Tangent / Infinity 等字段，必须同步升级 format_version。
    """
    # 步骤 1：分别查询关键帧时间和值。
    times = cmds.keyframe(
        plug,
        query=True,
        timeChange=True
    )

    values = cmds.keyframe(
        plug,
        query=True,
        valueChange=True
    )

    if times is None:
        times = []

    if values is None:
        values = []

    # 步骤 2：取最小长度，防止异常数据造成数组越界。
    key_count = min(
        len(times),
        len(values)
    )

    # 步骤 3：整理为可直接 JSON 序列化的数据。
    keys = []
    key_index = 0

    while key_index < key_count:
        key_info = {
            "time": float(times[key_index]),
            "value": float(values[key_index]),
        }

        keys.append(key_info)
        key_index += 1

    return keys


def collect_animation(nodes):
    u"""
    将多个 Maya 节点的动画整理成结构化数据。

    数据层级：
        Animation File
            -> Node
                -> Attribute
                    -> Key

    Args:
        nodes (str | list[str]):
            需要批量查询或处理的 Maya 节点名称或节点列表。

    Returns:
        object:
            方法执行后的结果数据。
    """
    # 步骤 1：整理输入节点。
    valid_nodes = normalize_nodes(nodes)
    animation_nodes = []

    # 步骤 2：逐节点收集有 Key 的属性。
    for node in valid_nodes:
        keyed_plugs = get_keyed_plugs(node)
        attributes = []

        for plug in keyed_plugs:
            attribute_name = get_attribute_name(plug)

            if not attribute_name:
                continue

            keys = get_key_data(plug)

            if not keys:
                continue

            attribute_info = {
                "name": attribute_name,
                "keys": keys,
            }

            attributes.append(attribute_info)

        # 没有任何关键帧的节点不写入文件，避免产生无意义数据。
        if not attributes:
            continue

        node_info = {
            "name": node,
            "attributes": attributes,
        }

        animation_nodes.append(node_info)

    # 步骤 3：写入格式名和版本，给未来兼容升级留下空间。
    data = {
        "format": format_name,
        "version": format_version,
        "nodes": animation_nodes,
    }

    return data


# =============================================================================
# Animation JSON - 导出
# =============================================================================

def export_animation(nodes, file_path):
    u"""
    将给定 Maya 节点的关键帧动画导出成 JSON。

    Args:
        nodes (list/str):
            要导出的 Maya 节点。
        file_path (str):
            JSON 输出路径。

    Returns:
        str: 最终写入的文件路径。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：确保至少有一个有效 Maya 节点。
    valid_nodes = normalize_nodes(nodes)

    if not valid_nodes:
        raise RuntimeError(u"没有可导出的 Maya 节点。")

    # 步骤 2：收集动画数据。
    data = collect_animation(valid_nodes)

    if not data["nodes"]:
        raise RuntimeError(u"给定节点上没有可导出的关键帧。")

    # 步骤 3：文件系统操作交给 file_utils，Animation 只负责动画语义。
    return file_utils.write_json(
        file_path=file_path,
        data=data,
        indent=4,
        ensure_ascii=False,
        sort_keys=False
    )


def export_selected_animation(file_path):
    u"""
    将当前 Maya Selection 中节点的动画导出为 JSON。

    Args:
        file_path (str):
            需要读取或写入的文件路径。

    Returns:
        object:
            方法执行后的结果数据。
    """
    # 步骤 1：读取当前选择。
    selected_nodes = cmds.ls(
        selection=True,
        long=True
    )

    if selected_nodes is None:
        selected_nodes = []

    # 步骤 2：复用统一导出入口。
    return export_animation(
        nodes=selected_nodes,
        file_path=file_path
    )


# =============================================================================
# Animation JSON - 导入
# =============================================================================

def validate_animation_data(data):
    u"""
    检查 Muzi Animation JSON 的格式名、版本和基础数据结构。

    数据结构错误时直接抛异常，因为继续往 Maya Scene 写入会产生
    “部分导入、部分失败”的脏状态。

    Args:
        data (object):
            `data` 对应的输入数据。

    Returns:
        bool:
            方法执行后的结果数据。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # 步骤 1：根对象必须是 dict。
    if not isinstance(data, dict):
        raise RuntimeError(u"动画 JSON 根数据必须是字典。")

    # 步骤 2：检查文件格式标识。
    if data.get("format") != format_name:
        raise RuntimeError(
            u"不是 Muzi Animation JSON：{}".format(
                data.get("format")
            )
        )

    # 步骤 3：检查版本。
    version = data.get("version")

    if version != format_version:
        raise RuntimeError(
            u"不支持的动画 JSON 版本：{}".format(version)
        )

    # 步骤 4：nodes 必须为 list。
    nodes = data.get("nodes")

    if not isinstance(nodes, list):
        raise RuntimeError(u"动画 JSON 缺少有效 nodes 列表。")

    return True


def resolve_target_node(source_node, node_map=None):
    u"""
    根据可选 node_map 解析动画导入目标节点。

    Args:
        source_node (object):
            `source_node` 对应的输入数据。
        node_map (dict):
            `node_map` 对应的配置或映射字典。

    Returns:
        object:
            方法执行后的结果数据。

    Example:
        {
                "ctrl_lf_arm_001": "characterA:ctrl_lf_arm_001"
            }
    """
    if node_map is None:
        return source_node

    if source_node in node_map:
        return node_map[source_node]

    return source_node


def apply_attribute_keys(
        target_node,
        attribute_info,
        clear_existing=False
):
    u"""
    将一个属性的 Key 数据写入目标 Maya 节点。

    Args:
        target_node (object):
            `target_node` 对应的输入数据。
        attribute_info (object):
            `attribute_info` 对应的输入数据。
        clear_existing (bool):
            写入新结果前是否先清理已有数据。

    Returns:
        int: 实际成功创建的 Key 数量。
    """
    # 步骤 1：读取并验证属性数据。
    attribute_name = attribute_info.get("name")
    keys = attribute_info.get("keys")

    if not attribute_name:
        return 0

    if not isinstance(keys, list):
        return 0

    plug = "{}.{}".format(
        target_node,
        attribute_name
    )

    if not cmds.objExists(plug):
        return 0

    # 步骤 2：根据参数决定是否先清理目标属性的已有 Key。
    if clear_existing:
        try:
            cmds.cutKey(
                plug,
                clear=True
            )
        except RuntimeError:
            pass

    # 步骤 3：逐条写入关键帧。
    created_count = 0

    for key_info in keys:
        if not isinstance(key_info, dict):
            continue

        if "time" not in key_info:
            continue

        if "value" not in key_info:
            continue

        key_time = float(key_info["time"])
        key_value = float(key_info["value"])

        try:
            cmds.setKeyframe(
                target_node,
                attribute=attribute_name,
                time=key_time,
                value=key_value
            )
            created_count += 1
        except RuntimeError:
            # 单个属性写入失败时继续处理其它 Key。
            # 上层可以通过 created_count 判断实际恢复数量。
            continue

    # 步骤 4：返回实际创建数量。
    return created_count


def import_animation(
        file_path,
        node_map=None,
        clear_existing=False,
        strict=False
):
    u"""
    从 Muzi Animation JSON 导入关键帧。

    Args:
        file_path (str):
            JSON 文件路径。
        node_map (dict/None):
            可选节点映射表。
        clear_existing (bool):
            导入某个属性前是否清除已有 Key。
        strict (bool):
            True：缺失目标节点立即报错； False：记录缺失节点并继续导入其它节点。

    Returns:
        dict:
        created_keys   - 实际创建 Key 数量；
        imported_nodes - 成功写入动画的节点；
        missing_nodes  - 文件中存在但场景找不到的目标节点。

    Raises:
        RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：读取 JSON，并验证格式。
    # -------------------------------------------------------------------------
    data = file_utils.read_json(file_path)
    validate_animation_data(data)

    created_keys = 0
    imported_nodes = []
    missing_nodes = []

    animation_nodes = data.get("nodes")

    # -------------------------------------------------------------------------
    # 步骤 2：逐节点解析动画。
    # -------------------------------------------------------------------------
    for node_info in animation_nodes:
        if not isinstance(node_info, dict):
            continue

        source_node = node_info.get("name")

        if not source_node:
            continue

        # 步骤 2.1：应用可选节点映射。
        target_node = resolve_target_node(
            source_node=source_node,
            node_map=node_map
        )

        # 步骤 2.2：处理目标节点不存在的情况。
        if not cmds.objExists(target_node):
            missing_nodes.append(target_node)

            if strict:
                raise RuntimeError(
                    u"导入动画时找不到目标节点：{}".format(
                        target_node
                    )
                )

            continue

        attributes = node_info.get("attributes")

        if not isinstance(attributes, list):
            continue

        node_created_keys = 0

        # 步骤 2.3：逐属性恢复 Key。
        for attribute_info in attributes:
            node_created_keys += apply_attribute_keys(
                target_node=target_node,
                attribute_info=attribute_info,
                clear_existing=clear_existing
            )

        if node_created_keys > 0:
            created_keys += node_created_keys
            imported_nodes.append(target_node)

    # -------------------------------------------------------------------------
    # 步骤 3：返回结构化结果，让上层决定如何显示成功 / 缺失信息。
    # -------------------------------------------------------------------------
    return {
        "created_keys": created_keys,
        "imported_nodes": imported_nodes,
        "missing_nodes": missing_nodes,
    }


__all__ = [
    "anim_curve_types",
    "format_name",
    "format_version",
    "get_animation_curves",
    "clear_animation_keys",
    "can_set_attribute",
    "reset_transform_channels",
    "reset_controls",
    "normalize_nodes",
    "get_keyed_plugs",
    "get_attribute_name",
    "get_key_data",
    "collect_animation",
    "export_animation",
    "export_selected_animation",
    "validate_animation_data",
    "resolve_target_node",
    "apply_attribute_keys",
    "import_animation",
]
