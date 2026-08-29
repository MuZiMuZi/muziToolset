# coding=utf-8
u"""
Connection Utils
================

Maya 属性连接底层工具。

职责：
    1. 查询 Plug 的输入 / 输出连接；
    2. 安全创建和断开属性连接；
    3. 批量连接 / 断开 Transform 属性；
    4. 复制一个对象已有的输入连接到其它对象；
    5. 批量断开指定属性的输入连接。

本模块只处理 Maya 节点和属性，不包含选择逻辑、Channel Box 或 UI。
"""

from __future__ import print_function

import maya.cmds as cmds


# =============================================================================
# Query
# =============================================================================

def get_input_connections(destination_plug):
    """返回 destination_plug 的全部输入 Plug。"""
    if not destination_plug:
        return []

    if not cmds.objExists(destination_plug):
        return []

    connections = cmds.listConnections(
        destination_plug,
        source=True,
        destination=False,
        plugs=True
    )

    if connections is None:
        connections = []

    return connections


def get_output_connections(source_plug):
    """返回 source_plug 的全部输出 Plug。"""
    if not source_plug:
        return []

    if not cmds.objExists(source_plug):
        return []

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
    """
    返回节点已有的输入连接。

    Returns:
        list(tuple):
            [(source_plug, destination_plug), ...]
    """
    if not node:
        return []

    if not cmds.objExists(node):
        return []

    if attribute_names is None:
        attribute_names = cmds.listAttr(
            node,
            connectable=True,
            inUse=True
        )

        if attribute_names is None:
            attribute_names = []

    result = []

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
# Validate
# =============================================================================

def can_connect(source_plug, destination_plug, force=False):
    """检查两个完整 Plug 当前是否可以建立连接。"""
    if not source_plug or not destination_plug:
        return False

    if not cmds.objExists(source_plug):
        return False

    if not cmds.objExists(destination_plug):
        return False

    if cmds.isConnected(source_plug, destination_plug):
        return True

    existing_inputs = get_input_connections(destination_plug)

    if existing_inputs and not force:
        return False

    return True


# =============================================================================
# Connect / Disconnect
# =============================================================================

def connect_plugs(source_plug, destination_plug, force=False):
    """安全连接两个完整 Plug，成功返回 True。"""
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

    if cmds.isConnected(source_plug, destination_plug):
        return True

    existing_inputs = get_input_connections(destination_plug)

    if existing_inputs and not force:
        cmds.warning(
            u"被驱动属性已有输入连接：{}".format(
                destination_plug
            )
        )
        return False

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
    """断开一条明确的 Plug 连接，成功返回 True。"""
    if not cmds.objExists(source_plug):
        return False

    if not cmds.objExists(destination_plug):
        return False

    if not cmds.isConnected(source_plug, destination_plug):
        return False

    try:
        cmds.disconnectAttr(
            source_plug,
            destination_plug
        )
    except RuntimeError:
        return False

    return True


def disconnect_input(destination_plug):
    """断开 destination_plug 的全部输入连接，返回断开数量。"""
    input_connections = get_input_connections(destination_plug)
    disconnected_count = 0

    for source_plug in input_connections:
        if disconnect_plugs(
                source_plug,
                destination_plug
        ):
            disconnected_count += 1

    return disconnected_count


# =============================================================================
# Batch
# =============================================================================

def connect_attribute_pairs(
        driver,
        driven_objects,
        attribute_pairs,
        force=False
):
    """
    将一个 Driver 的多组属性批量连接给多个 Driven。

    Args:
        driver(str): 驱动节点。
        driven_objects(list): 被驱动节点列表。
        attribute_pairs(list):
            [(source_attr, destination_attr), ...]
        force(bool): 是否覆盖目标已有输入。

    Returns:
        int: 成功连接数量。
    """
    created_count = 0

    for driven_object in driven_objects:
        for source_attribute, destination_attribute in attribute_pairs:
            source_plug = "{}.{}".format(
                driver,
                source_attribute
            )
            destination_plug = "{}.{}".format(
                driven_object,
                destination_attribute
            )

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
    """批量断开一个 Driver 到多个 Driven 的属性连接。"""
    disconnected_count = 0

    for driven_object in driven_objects:
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
    """把一个完整 Source Plug 连接给多个对象的同名属性。"""
    created_count = 0

    for driven_object in driven_objects:
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
    """批量断开多个对象指定属性的全部输入连接。"""
    disconnected_count = 0

    for node in objects:
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
    """复制 source_object 指定属性已有的输入连接到其它对象。"""
    copied_count = 0

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

        source_plug = input_connections[0]

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
