# coding=utf-8
u"""
Connection Utils
================

Maya DG Plug 连接领域的通用底层工具。

职责：
    1. 查询 Plug 输入 / 输出；
    2. 建立 / 断开明确的 Plug 连接；
    3. 断开一个 Destination Plug 的全部输入；
    4. 对显式 Plug Pair 做批量连接 / 断开。

边界：
    Attribute 创建 / Value / Message 语义 -> attr_utils
    Matrix / offsetParentMatrix Network    -> matrix_utils
    Maya Constraint                        -> constraint_utils
    Selection / Channel Box / UI           -> tools
    角色专属 Rig 连接规则                  -> systems

设计原则：
    1. 正式 API 只认识完整 node.attribute Plug；
    2. 无效 Plug 属于调用错误，直接抛异常；
    3. 有效但没有连接时查询返回空列表；
    4. 默认保护 Destination 已有输入，只有 force=True 才替换；
    5. 同一条连接已存在时视为成功，保证重复 Build 幂等；
    6. Maya 是否真正允许连接，以 cmds.connectAttr 为最终权威。
"""

from __future__ import print_function

import maya.cmds as cmds


def _validate_plug(plug, label=u"Plug"):
    u"""验证完整 Maya Plug，并返回整理后的字符串。"""
    if plug is None:
        raise ValueError(u"{}不能为空。".format(label))

    plug = str(plug).strip()

    if not plug:
        raise ValueError(u"{}不能为空。".format(label))

    if "." not in plug:
        raise ValueError(
            u"{}必须使用完整 node.attribute：{}".format(label, plug)
        )

    if not cmds.objExists(plug):
        raise RuntimeError(u"{}不存在：{}".format(label, plug))

    return plug


def _normalize_connection_pairs(connection_pairs):
    u"""先验证全部 Plug Pair，再开始批量修改 Maya DG。"""
    result = []

    if connection_pairs is None:
        return result

    for connection_pair in connection_pairs:
        if not isinstance(connection_pair, (list, tuple)):
            raise TypeError(
                u"Connection Pair 必须是 list / tuple：{}".format(
                    connection_pair
                )
            )

        if len(connection_pair) != 2:
            raise ValueError(
                u"Connection Pair 必须包含 Source / Destination 两项：{}".format(
                    connection_pair
                )
            )

        source_plug = _validate_plug(
            connection_pair[0],
            u"Source Plug"
        )
        destination_plug = _validate_plug(
            connection_pair[1],
            u"Destination Plug"
        )
        result.append((source_plug, destination_plug))

    return result


def get_input_connections(destination_plug):
    u"""
    返回 Destination Plug 的全部 Source Plug；无输入时返回空列表。

    Args:
        destination_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        object | list:
        按当前 API 约定顺序返回的结果列表。
    """
    destination_plug = _validate_plug(
        destination_plug,
        u"Destination Plug"
    )
    connections = cmds.listConnections(
        destination_plug,
        source=True,
        destination=False,
        plugs=True
    )

    if connections is None:
        return []

    return list(connections)


def get_output_connections(source_plug):
    u"""
    返回 Source Plug 的全部 Destination Plug；无输出时返回空列表。

    Args:
        source_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        object | list:
        按当前 API 约定顺序返回的结果列表。
    """
    source_plug = _validate_plug(
        source_plug,
        u"Source Plug"
    )
    connections = cmds.listConnections(
        source_plug,
        source=False,
        destination=True,
        plugs=True
    )

    if connections is None:
        return []

    return list(connections)


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
        bool:
        同一条连接已存在或成功建立时 True；
        Destination 已有其它输入且 force=False 时 False。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    # -------------------------------------------------------------------------
    # Step 01：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    source_plug = _validate_plug(source_plug, u"Source Plug")
    # -------------------------------------------------------------------------
    # Step 02：验证并规范化当前阶段需要的输入数据
    # -------------------------------------------------------------------------
    destination_plug = _validate_plug(destination_plug, u"Destination Plug")

    if cmds.isConnected(source_plug, destination_plug):
        return True

    # -------------------------------------------------------------------------
    # Step 03：查询并整理当前阶段需要的 Maya 场景数据
    # -------------------------------------------------------------------------
    existing_inputs = get_input_connections(destination_plug)

    if existing_inputs and not force:
        return False

    # -------------------------------------------------------------------------
    # Step 04：执行可能失败的操作，并统一处理异常或清理状态
    # -------------------------------------------------------------------------
    try:
        cmds.connectAttr(
            source_plug,
            destination_plug,
            force=bool(force)
        )
    except RuntimeError as error:
        raise RuntimeError(
            u"无法建立 Plug 连接：{} -> {} | {}".format(
                source_plug,
                destination_plug,
                error
            )
        )

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return True


def disconnect_plugs(source_plug, destination_plug):
    u"""
    断开一条明确 Plug 连接；本来不存在时返回 False。

    Args:
        source_plug (str):
            完整 Maya Plug，例如 `node.translateX`。
        destination_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        bool:
        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

    Raises:
        RuntimeError:
        输入数据、场景状态或操作条件不满足要求时抛出。
    """
    source_plug = _validate_plug(source_plug, u"Source Plug")
    destination_plug = _validate_plug(destination_plug, u"Destination Plug")

    if not cmds.isConnected(source_plug, destination_plug):
        return False

    try:
        cmds.disconnectAttr(source_plug, destination_plug)
    except RuntimeError as error:
        raise RuntimeError(
            u"无法断开 Plug 连接：{} -> {} | {}".format(
                source_plug,
                destination_plug,
                error
            )
        )

    return True


def disconnect_input(destination_plug):
    u"""
    断开 Destination Plug 的全部输入，并返回实际断开数量。

    Args:
        destination_plug (str):
            完整 Maya Plug，例如 `node.translateX`。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    destination_plug = _validate_plug(destination_plug, u"Destination Plug")
    input_connections = get_input_connections(destination_plug)
    disconnected_count = 0

    for source_plug in input_connections:
        if disconnect_plugs(source_plug, destination_plug):
            disconnected_count += 1

    return disconnected_count


def connect_plug_pairs(connection_pairs, force=False):
    u"""
    批量建立显式 Plug Pair，并返回成功 / 已存在的 Pair 数量。

    Args:
        connection_pairs (object):
            当前方法执行 Maya / Rig 操作时使用的 `connection_pairs` 数据。
        force (bool):
            是否强制覆盖已有连接、状态或结果。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    connection_pairs = _normalize_connection_pairs(connection_pairs)
    connected_count = 0

    for source_plug, destination_plug in connection_pairs:
        if connect_plugs(source_plug, destination_plug, force=force):
            connected_count += 1

    return connected_count


def disconnect_plug_pairs(connection_pairs):
    u"""
    批量断开显式 Plug Pair，并返回实际断开数量。

    Args:
        connection_pairs (object):
            当前方法执行 Maya / Rig 操作时使用的 `connection_pairs` 数据。

    Returns:
        object:
        当前 API 完成处理后返回的结果。
    """
    connection_pairs = _normalize_connection_pairs(connection_pairs)
    disconnected_count = 0

    for source_plug, destination_plug in connection_pairs:
        if disconnect_plugs(source_plug, destination_plug):
            disconnected_count += 1

    return disconnected_count


__all__ = [
    "get_input_connections",
    "get_output_connections",
    "connect_plugs",
    "disconnect_plugs",
    "disconnect_input",
    "connect_plug_pairs",
    "disconnect_plug_pairs",
]
