# coding=utf-8
u"""
Config Utils
============

Maya Rig / Tool 通用 Network Config Node 底层模块。

Config 数据分为：
- Message Reference：保存 Maya Node 引用；
- Value Attribute：保存 int / float / bool / string 等普通配置。

模块边界
--------
- Attribute 创建、状态、Value、Message -> attr_utils.Attr
- Config Network Node 生命周期与配置语义 -> ConfigNode
- Face / Body / Hand 只组合这里的 API，不重复实现 Config CRUD
"""

from __future__ import print_function

import maya.cmds as cmds

from . import attr_utils


class ConfigNode(object):
    u"""一个 Maya Network Config Node 的配置语义对象。"""

    def __init__(self, node):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """

        if not node:
            raise ValueError(
                u"Config Node 名称不能为空。"
            )

        self.node = str(node).strip()

        if not self.node:
            raise ValueError(
                u"Config Node 名称不能为空。"
            )

    def exists(self):
        u"""
        检查 Config Node 是否存在且类型为 network。

        Returns:
            object | bool:
                方法执行后的结果数据。
        """
        if not cmds.objExists(self.node):
            return False

        return cmds.nodeType(
            self.node
        ) == "network"

    def ensure(self):
        u"""
        创建或复用 Config Network Node。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
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
            object:
                方法执行后的结果数据。
        """
        return attr_utils.Attr(
            self.node
        )

    def get_message(self, attr_name):
        u"""
        读取一个 Message Attribute 保存的 Maya Node 引用。

        Args:
            attr_name (str):
                `attr_name` 对应的 Maya 节点或资源名称。

        Returns:
            object | None:
                方法执行后的结果数据。
        """
        if not self.exists():
            return None

        config_attr = self.get_attr()
        return config_attr.get_message(
            attr_name
        )

    def get_value(self, attr_name):
        u"""
        读取一个普通 Config Attribute Value。

        Args:
            attr_name (str):
                `attr_name` 对应的 Maya 节点或资源名称。

        Returns:
            object | None:
                方法执行后的结果数据。
        """
        if not self.exists():
            return None

        config_attr = self.get_attr()
        return config_attr.get_value(
            attr_name
        )

    def get_messages(self, attr_names):
        u"""
        批量读取 Message Config。

        Args:
            attr_names (object):
                当前方法执行 Maya / Rig 操作时使用的 `attr_names` 数据。

        Returns:
            object:
                方法执行后的结果数据。
        """
        result = {}

        if not attr_names:
            return result

        for attr_name in attr_names:
            result[attr_name] = self.get_message(
                attr_name
            )

        return result

    def get_values(self, attr_names):
        u"""
        批量读取普通 Config Value。

        Args:
            attr_names (object):
                当前方法执行 Maya / Rig 操作时使用的 `attr_names` 数据。

        Returns:
            object:
                方法执行后的结果数据。
        """
        result = {}

        if not attr_names:
            return result

        for attr_name in attr_names:
            result[attr_name] = self.get_value(
                attr_name
            )

        return result

    def set_messages(
            self,
            attrs_dict,
            force=True,
            clear_empty=True
    ):
        u"""
        批量保存 Maya Node Message 引用。

        Args:
            attrs_dict (dict):
                Attribute 名称到 Value / Config 数据的批量映射。
            force (bool):
                是否强制覆盖已有连接、状态或结果。
            clear_empty (bool):
                批量保存 Message / Config 时，空值是否主动断开旧连接。

        Returns:
            object:
                方法执行后的结果数据。
        """
        self.ensure()
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

        ConfigNode 保留 lock / hide 业务参数，内部转换为 Attr 的明确状态参数。

        Args:
            attrs_dict (dict):
                Attribute 名称到 Value / Config 数据的批量映射。
            attr_types (dict | None):
                Attribute 名称到 Maya Attribute Type 的映射；未指定的属性由调用方默认规则处理。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            hide (bool):
                是否从 Channel Box 隐藏对应 Maya Attribute。

        Returns:
            object:
                方法执行后的结果数据。
        """
        self.ensure()

        if attr_types is None:
            attr_types = {}

        config_attr = self.get_attr()

        return config_attr.set_values(
            attrs_dict=attrs_dict,
            attr_types=attr_types,
            lock=lock,
            keyable=not hide,
            channel_box=not hide
        )


__all__ = [
    "ConfigNode",
]
