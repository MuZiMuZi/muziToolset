# coding=utf-8
u"""
Connection Utils
================

Maya DG 属性连接领域的通用底层工具。

模块职责
--------
这个模块只处理 Plug 与 Plug 之间的连接关系，不负责 Selection、Channel Box 或 UI。
上层 Tool 可以根据用户选择决定“连谁”，但真正的连接 / 断开逻辑统一放在这里。

当前公开方法
------------
查询：
    get_input_connections(destination_plug)
        获取一个目标 Plug 的全部输入 Plug。

    get_output_connections(source_plug)
        获取一个源 Plug 的全部输出 Plug。

    get_connected_input_pairs(node, attribute_names=None)
        查询一个节点已经存在的输入连接，返回 (source, destination) 对。

校验：
    can_connect(source_plug, destination_plug, force=False)
        判断当前两个 Plug 是否可以建立连接。

连接 / 断开：
    connect_plugs(source_plug, destination_plug, force=False)
        安全创建一条明确的 Plug 连接。

    disconnect_plugs(source_plug, destination_plug)
        断开一条明确的 Plug 连接。

    disconnect_input(destination_plug)
        断开目标 Plug 的全部输入连接。

批处理：
    connect_attribute_pairs(driver, driven_objects, attribute_pairs, force=False)
        将 Driver 的多组属性批量连接给多个 Driven。

    disconnect_attribute_pairs(driver, driven_objects, attribute_pairs)
        批量断开 Driver 与多个 Driven 的指定属性连接。

    connect_source_to_attributes(source_plug, driven_objects, attribute_names, force=False)
        将一个完整 Source Plug 连接给多个对象的同名属性。

    disconnect_object_inputs(objects, attribute_names)
        批量断开多个对象指定属性的全部输入。

    copy_input_connections(source_object, target_objects, attribute_names, force=True)
        复制 Source Object 指定属性已有的输入连接到其它对象。

本模块不负责
------------
- Maya Selection；
- Channel Box 读取；
- UI 按钮与提示；
- Constraint / Matrix 网络；
- 角色专属 Rig 连接规则。

设计原则
--------
1. Plug 使用完整 ``node.attribute`` 字符串；
2. 默认不覆盖已有输入，除非调用方明确传 ``force=True``；
3. 批处理函数只组合基础 API，不重复写连接判断；
4. Core 返回 True / False / Count，让 UI 自己决定如何显示结果；
5. 不再保留早期 connectionUtils 中模糊的属性类型判断逻辑。
"""

from __future__ import print_function

import maya.cmds as cmds


# =============================================================================
# Query - 输入 / 输出连接查询
# =============================================================================

def get_input_connections(destination_plug):
    u"""
    返回 ``destination_plug`` 的全部输入 Plug。

    Args:
        destination_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        list: Source Plug 列表；无输入时返回空列表。
    """
    # 步骤 1：空参数或不存在的 Plug 直接返回空列表。
    if not destination_plug:
        return []

    if not cmds.objExists(destination_plug):
        return []

    # 步骤 2：只查询 Source -> Destination 方向。
    connections = cmds.listConnections(
        destination_plug,
        source=True,
        destination=False,
        plugs=True
    )

    if connections is None:
        connections = []

    # 步骤 3：统一返回普通 list。
    return connections


def get_output_connections(source_plug):
    u"""
    返回 ``source_plug`` 的全部输出 Plug。

    Args:
        source_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        list: Destination Plug 列表；无输出时返回空列表。
    """
    # 步骤 1：检查 Source Plug。
    if not source_plug:
        return []

    if not cmds.objExists(source_plug):
        return []

    # 步骤 2：只查询 Source -> Destination 输出方向。
    connections = cmds.listConnections(
        source_plug,
        source=False,
        destination=True,
        plugs=True
    )

    if connections is None:
        connections = []

    return connections


def get_connected_input_pairs(node, attribute_names=None):
    u"""
    返回节点当前已有的输入连接。

    Args:
        node (str):
            目标 Maya 节点。
        attribute_names (list/None):
            指定时只检查这些属性； None 时查询节点当前 connectable + inUse 属性。

    Returns:
        list:
        [(source_plug, destination_plug), ...]
    """
    # 步骤 1：节点无效时直接返回空列表。
    if not node:
        return []

    if not cmds.objExists(node):
        return []

    # 步骤 2：没有显式属性列表时，让 Maya 提供当前正在使用的可连接属性。
    if attribute_names is None:
        attribute_names = cmds.listAttr(
            node,
            connectable=True,
            inUse=True
        )

        if attribute_names is None:
            attribute_names = []

    result = []

    # 步骤 3：逐属性查询输入连接，并整理成 Source / Destination Pair。
    for attribute_name in attribute_names:
        destination_plug = "{}.{}".format(
            node,
            attribute_name
        )

        input_connections = get_input_connections(destination_plug)

        for source_plug in input_connections:
            result.append((source_plug, destination_plug))

    return result


# =============================================================================
# Validate - 是否可以建立连接
# =============================================================================

def can_connect(source_plug, destination_plug, force=False):
    u"""
    检查两个完整 Plug 当前是否可以建立连接。

    已经存在同一条连接时返回 True；
    Destination 已有其它输入并且 force=False 时返回 False。

    Args:
        source_plug (str):
            完整 Maya Plug，例如 `node.translateX`。
        destination_plug (str):
            完整 Maya Plug，例如 `node.translateX`。
        force (bool):
            是否强制覆盖已有连接、状态或结果。

    Returns:
        bool:
        方法执行后的结果数据。
    """
    # 步骤 1：两个 Plug 都必须存在。
    if not source_plug or not destination_plug:
        return False

    if not cmds.objExists(source_plug):
        return False

    if not cmds.objExists(destination_plug):
        return False

    # 步骤 2：连接本来就存在时视为可用状态。
    if cmds.isConnected(source_plug, destination_plug):
        return True

    # 步骤 3：检查目标是否已有其它输入。
    existing_inputs = get_input_connections(destination_plug)

    if existing_inputs and not force:
        return False

    return True


# =============================================================================
# Connect / Disconnect - 基础连接 API
# =============================================================================

def connect_plugs(source_plug, destination_plug, force=False):
    u"""
    安全连接两个完整 Plug。

    Args:
        source_plug (str):
            完整 Maya Plug，例如 `node.translateX`。
        destination_plug (str):
            完整 Maya Plug，例如 `node.translateX`。
        force (bool):
            是否强制覆盖已有连接、状态或结果。

    Returns:
        bool: 成功建立或连接本来已存在时返回 True。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：检查 Source / Destination 是否存在。
    # -------------------------------------------------------------------------
    if not cmds.objExists(source_plug):
        cmds.warning(
            u"驱动属性不存在：{}".format(source_plug)
        )
        return False

    if not cmds.objExists(destination_plug):
        cmds.warning(
            u"被驱动属性不存在：{}".format(destination_plug)
        )
        return False

    # -------------------------------------------------------------------------
    # 步骤 2：同一条连接已经存在时不重复创建。
    # -------------------------------------------------------------------------
    if cmds.isConnected(source_plug, destination_plug):
        return True

    # -------------------------------------------------------------------------
    # 步骤 3：默认保护 Destination 的现有输入。
    # force=False 时绝不静默覆盖已有 Rig 连接。
    # -------------------------------------------------------------------------
    existing_inputs = get_input_connections(destination_plug)

    if existing_inputs and not force:
        cmds.warning(
            u"被驱动属性已有输入连接：{}".format(
                destination_plug
            )
        )
        return False

    # -------------------------------------------------------------------------
    # 步骤 4：执行 Maya connectAttr。
    # -------------------------------------------------------------------------
    try:
        cmds.connectAttr(
            source_plug,
            destination_plug,
            force=force
        )
    except RuntimeError as error:
        cmds.warning(str(error))
        return False

    return True


def disconnect_plugs(source_plug, destination_plug):
    u"""
    断开一条明确的 Plug 连接。

    Args:
        source_plug (str):
            完整 Maya Plug，例如 `node.translateX`。
        destination_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        bool: 实际断开成功时返回 True。
    """
    # 步骤 1：检查 Plug。
    if not cmds.objExists(source_plug):
        return False

    if not cmds.objExists(destination_plug):
        return False

    # 步骤 2：连接不存在时不做无意义操作。
    if not cmds.isConnected(source_plug, destination_plug):
        return False

    # 步骤 3：执行 disconnectAttr。
    try:
        cmds.disconnectAttr(
            source_plug,
            destination_plug
        )
    except RuntimeError:
        return False

    return True


def disconnect_input(destination_plug):
    u"""
    断开一个 Destination Plug 的全部输入连接。

    Args:
        destination_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        int: 实际断开的连接数量。
    """
    # 步骤 1：查询全部 Source Plug。
    input_connections = get_input_connections(destination_plug)
    disconnected_count = 0

    # 步骤 2：逐条复用 disconnect_plugs。
    for source_plug in input_connections:
        if disconnect_plugs(
                source_plug,
                destination_plug
        ):
            disconnected_count += 1

    return disconnected_count


# =============================================================================
# Batch - 批量连接 / 断开
# =============================================================================

def connect_attribute_pairs(
        driver,
        driven_objects,
        attribute_pairs,
        force=False
):
    u"""
    将一个 Driver 的多组属性批量连接给多个 Driven。

    Args:
        driver (str):
            驱动节点。
        driven_objects (list):
            被驱动节点列表。
        attribute_pairs (list):
            [(source_attr, destination_attr), ...]
        force (bool):
            是否覆盖目标已有输入。

    Returns:
        int: 成功连接数量。
    """
    created_count = 0

    # 步骤 1：遍历所有 Driven。
    for driven_object in driven_objects:
        # 步骤 2：对每个 Driven 应用全部属性 Pair。
        for source_attribute, destination_attribute in attribute_pairs:
            source_plug = "{}.{}".format(
                driver,
                source_attribute
            )
            destination_plug = "{}.{}".format(
                driven_object,
                destination_attribute
            )

            # 步骤 3：基础安全检查统一交给 connect_plugs。
            if connect_plugs(
                    source_plug,
                    destination_plug,
                    force=force
            ):
                created_count += 1

    return created_count


def disconnect_attribute_pairs(
        driver,
        driven_objects,
        attribute_pairs
):
    u"""
    批量断开一个 Driver 到多个 Driven 的指定属性连接。

    Args:
        driver (str):
            作为驱动端的 Maya 节点名称。
        driven_objects (str | list[str]):
            需要批量接收驱动结果的 Driven 节点或节点列表。
        attribute_pairs (list[tuple[str, str]] | dict):
            需要批量建立连接的 Source Plug / Destination Plug 配对数据。

    Returns:
        object:
        方法执行后的结果数据。
    """
    disconnected_count = 0

    # 步骤 1：逐 Driven。
    for driven_object in driven_objects:
        # 步骤 2：逐 Attribute Pair。
        for source_attribute, destination_attribute in attribute_pairs:
            source_plug = "{}.{}".format(
                driver,
                source_attribute
            )
            destination_plug = "{}.{}".format(
                driven_object,
                destination_attribute
            )

            if disconnect_plugs(
                    source_plug,
                    destination_plug
            ):
                disconnected_count += 1

    return disconnected_count


def connect_source_to_attributes(
        source_plug,
        driven_objects,
        attribute_names,
        force=False
):
    u"""
    将一个完整 Source Plug 连接给多个对象的同名属性。

    常见用途：
        一个 Visibility / Enable / GlobalScale 属性驱动多个节点。

    Args:
        source_plug (str):
            完整 Maya Plug，例如 `node.translateX`。
        driven_objects (str | list[str]):
            需要批量接收驱动结果的 Driven 节点或节点列表。
        attribute_names (str | list[str]):
            需要查询、复制或批量连接的 Maya Attribute 名称列表。
        force (bool):
            是否强制覆盖已有连接、状态或结果。

    Returns:
        object:
        方法执行后的结果数据。
    """
    created_count = 0

    # 步骤 1：遍历所有 Driven Object。
    for driven_object in driven_objects:
        # 步骤 2：遍历需要连接的属性名称。
        for attribute_name in attribute_names:
            destination_plug = "{}.{}".format(
                driven_object,
                attribute_name
            )

            if connect_plugs(
                    source_plug,
                    destination_plug,
                    force=force
            ):
                created_count += 1

    return created_count


def disconnect_object_inputs(objects, attribute_names):
    u"""
    批量断开多个对象指定属性的全部输入连接。

    Args:
        objects (str | list[str]):
            需要批量处理的 Maya 场景对象名称或对象列表。
        attribute_names (str | list[str]):
            需要查询、复制或批量连接的 Maya Attribute 名称列表。

    Returns:
        int: 实际断开的总连接数量。
    """
    disconnected_count = 0

    # 步骤 1：逐对象。
    for node in objects:
        # 步骤 2：逐属性调用 disconnect_input。
        for attribute_name in attribute_names:
            destination_plug = "{}.{}".format(
                node,
                attribute_name
            )
            disconnected_count += disconnect_input(
                destination_plug
            )

    return disconnected_count


def copy_input_connections(
        source_object,
        target_objects,
        attribute_names,
        force=True
):
    u"""
    复制 ``source_object`` 指定属性已有的输入连接到其它对象。

    例如 Source.translateX 已经由某个 Utility Node 驱动，
    本函数可以把同一个 Source Plug 接到多个 Target.translateX。

    Args:
        source_object (str):
            提供 Attribute、Transform 或连接数据的 Source Maya 对象。
        target_objects (str | list[str]):
            接收 Source 数据或连接的一个或多个 Target Maya 对象。
        attribute_names (str | list[str]):
            需要查询、复制或批量连接的 Maya Attribute 名称列表。
        force (bool):
            是否强制覆盖已有连接、状态或结果。

    Returns:
        int: 成功复制的连接数量。
    """
    copied_count = 0

    # 步骤 1：逐属性读取 Source Object 当前输入。
    for attribute_name in attribute_names:
        source_destination_plug = "{}.{}".format(
            source_object,
            attribute_name
        )

        input_connections = get_input_connections(
            source_destination_plug
        )

        if not input_connections:
            continue

        # 当前属性只复制第一条输入。
        # Maya 普通非 Multi Attribute 通常也只有一条有效输入。
        source_plug = input_connections[0]

        # 步骤 2：将同一个 Source Plug 复制给全部 Target。
        for target_object in target_objects:
            destination_plug = "{}.{}".format(
                target_object,
                attribute_name
            )

            if connect_plugs(
                    source_plug,
                    destination_plug,
                    force=force
            ):
                copied_count += 1

    return copied_count


__all__ = [
    "get_input_connections",
    "get_output_connections",
    "get_connected_input_pairs",
    "can_connect",
    "connect_plugs",
    "disconnect_plugs",
    "disconnect_input",
    "connect_attribute_pairs",
    "disconnect_attribute_pairs",
    "connect_source_to_attributes",
    "disconnect_object_inputs",
    "copy_input_connections",
]
