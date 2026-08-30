# coding=utf-8
u"""
Config Utils
============

Maya Rig / Tool 通用配置节点底层模块。

模块职责
--------
本模块负责使用 Maya ``network`` Node 保存工具或 Rig System 的持久化配置。

Config 数据分为两类：

1. Message Reference
    保存 Maya 节点引用。对象 Rename 后连接仍然有效，适合保存 Model、Guide、Controller、Joint 等节点。

2. Value Attribute
    保存 int / float / bool / string 等普通配置，例如 Joint 数量、Version、Build State。

公开类
------
ConfigNode
    一个以 Maya Network Node 为上下文的通用 Config 操作对象。

设计边界
--------
- Attribute 创建、读写和 Message 连接由 ``attr_utils.Attr`` 负责；
- ConfigNode 只负责 Config Network Node 生命周期和 Config 语义封装；
- Face / Body / Hand 等具体 System 不应该把通用 Config CRUD 再实现一遍；
- 本模块不依赖 systems、tools 或 ui。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import attr_utils


class ConfigNode(object):
    u"""通用 Maya Network Config Node。"""

    def __init__(self, node):
        u"""
        Args:
            node (str):
                Config Network Node 名称。
        """
        if not node:
            raise ValueError(
                u"Config Node 名称不能为空。"
            )

        self.node = node

    # =========================================================================
    # Node
    # =========================================================================

    def exists(self):
        u"""
        检查 Config Node 是否存在且类型为 network。

        Returns:
            bool:
                有效 Config Node 返回 True。
        """
        if not cmds.objExists(self.node):
            return False

        if cmds.nodeType(self.node) != "network":
            return False

        return True

    def ensure(self):
        u"""
        创建或复用 Config Network Node。

        Returns:
            str:
                Config Node 名称。

        Raises:
            RuntimeError:
                同名节点存在但不是 network 时抛出。
        """
        if cmds.objExists(self.node):
            node_type = cmds.nodeType(
                self.node
            )

            if node_type != "network":
                raise RuntimeError(
                    u"Config Node 名称已被其它类型节点占用：{} | type={}".format(
                        self.node,
                        node_type
                    )
                )

            return self.node

        self.node = cmds.createNode(
            "network",
            name=self.node
        )

        return self.node

    def get_attr(self):
        u"""
        返回当前 Config Node 的 Attr 操作对象。

        Returns:
            attr_utils.Attr
        """
        # 使用统一 Attribute Core 处理当前 Network Node 的所有属性操作。
        return attr_utils.Attr(
            self.node
        )

    # =========================================================================
    # Read
    # =========================================================================

    def get_message(self, attr_name):
        u"""
        读取一个 Message 属性保存的 Maya 节点引用。

        Config Node 不存在时返回 None。
        """
        # 先确认当前 Config Node 有效，避免在不存在的节点上读取 Attribute。
        if not self.exists():
            return None

        # 获取统一 Attr 操作对象，读取目标 Message Attribute 的来源节点。
        config_attr = self.get_attr()

        return config_attr.get_message(
            attr_name
        )

    def get_value(self, attr_name):
        u"""
        读取一个普通 Config Attribute Value。

        Config Node 不存在或属性不存在时返回 None。
        """
        # 先确认当前 Config Node 有效，避免在不存在的节点上读取 Attribute。
        if not self.exists():
            return None

        # 获取统一 Attr 操作对象，读取普通 Config Value。
        config_attr = self.get_attr()

        return config_attr.get_attr_value(
            attr_name
        )

    def get_messages(self, attr_names):
        u"""
        批量读取 Message Config。

        Args:
            attr_names (list[str]):
                需要读取的 Message Attribute 名称。

        Returns:
            dict:
                attr_name -> Maya Node / None
        """
        result = {}

        if not attr_names:
            return result

        # 逐个调用统一 Message 查询入口，保证单个和批量读取使用同一套行为。
        for attr_name in attr_names:
            result[attr_name] = self.get_message(
                attr_name
            )

        return result

    def get_values(self, attr_names):
        u"""批量读取普通 Config Value。"""
        result = {}

        if not attr_names:
            return result

        # 逐个调用统一 Value 查询入口，避免批量 API 维护第二套读取逻辑。
        for attr_name in attr_names:
            result[attr_name] = self.get_value(
                attr_name
            )

        return result

    # =========================================================================
    # Write
    # =========================================================================

    def set_messages(
            self,
            attrs_dict,
            force=True,
            clear_empty=True
    ):
        u"""
        批量保存 Maya 节点引用。

        Args:
            attrs_dict (dict):
                attr_name -> Maya Node。
            force (bool):
                是否覆盖已有 Message 输入。
            clear_empty (bool):
                输入为空时是否断开已有连接。

        Returns:
            dict:
                每个属性的执行结果。
        """
        # 写入前创建或复用 Config Network Node，保证后续 Attribute 操作有稳定目标。
        self.ensure()

        # 获取统一 Attr 操作对象，把节点引用保存成 Message Connection。
        config_attr = self.get_attr()

        return config_attr.connect_messages(
            attrs_dict=attrs_dict,
            force=force,
            clear_empty=clear_empty
        )

    def set_values(
            self,
            attrs_dict,
            attr_types=None,
            lock=False,
            hide=False
    ):
        u"""
        批量保存普通 Config Value。

        Args:
            attrs_dict (dict):
                attr_name -> Python Value。
            attr_types (dict | None):
                可选 attr_name -> Maya Attribute Type。
            lock (bool):
                写入后是否锁定属性。
            hide (bool):
                是否隐藏属性。

        Returns:
            dict:
                每个属性的执行结果。
        """
        # 写入前创建或复用 Config Network Node，保证普通 Value 有持久化节点。
        self.ensure()

        if attr_types is None:
            attr_types = {}

        # 获取统一 Attr 操作对象，批量创建或更新普通配置属性。
        config_attr = self.get_attr()

        return config_attr.set_attr_values(
            attrs_dict=attrs_dict,
            attr_types=attr_types,
            lock=lock,
            hide=hide
        )


__all__ = [
    "ConfigNode",
]
