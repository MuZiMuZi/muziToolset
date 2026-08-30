# coding=utf-8
u"""
Attribute Utils
===============

Maya Attribute / Plug 通用操作模块。

正式模块路径
------------
``muziToolset.core.attr_utils`` 是 Attribute 能力的唯一正式实现。
旧 ``attrUtils.py`` 兼容模块已经完成迁移并删除，新代码和文档统一使用 snake_case 路径。

模块职责
--------
本模块负责一个 Maya 节点上的属性创建、属性状态、属性值、Message 配置、字符串配置、
Transform Limits，以及为了兼容早期工具保留的 Channel Box 辅助入口。

公开类
------
Attr
    以一个 Maya 节点为上下文执行属性操作。

Attr 主要公开方法
-----------------
object_exists()
    检查当前节点是否存在。

attr_exists(attr=None)
    检查属性 Plug 是否存在。

lock_and_hide_attr(attr, lock=True, hide=True)
lock_and_hide_attrs(attrs_list, lock=True, hide=True)
    设置单个 / 多个属性的 Lock、Keyable 与 Channel Box 状态。

add_attr(...)
    创建 string / double / long / bool / enum / message 等自定义属性。

connect_attr(output_attr, input_attr, force=True)
disconnect_attr(output_attr, input_attr)
get_attr_input(attr=None, plugs=True)
get_attr_output(attr=None, plugs=True)
    兼容早期 Attr API；底层连接逻辑统一复用 connection_utils。

set_attr_value(...)
get_attr_value(attr=None)
set_attr_values(...)
    创建并读写普通属性值。

add_message_attr(attr, multi=False)
disconnect_attr_inputs(attr=None)
connect_message(...)
connect_messages(...)
get_message(attr=None, plugs=False)
    使用 Maya message 连接保存节点引用，适合 Rig Config / Setup 数据。

add_string_info(information, attr=None, lock=True, hide=True)
get_string_info(attr=None)
    在 string 属性中保存 / 恢复 Python 基础数据。

set_attrs_limits(attrs_dict)
get_attrs_limits(attrs_list=None)
get_unwanted_attrs(attrs_list)
    Transform Limits 与通道筛选。

兼容辅助方法
------------
get_channelBox_attrs()
move_channelBox_attr(up=True, down=False)
set_lock_attr(...)
set_hide_attr(...)
set_key_attr(...)
lock_hide_attr(...)
reset_attr(node)
    来自早期 Core 的 API。为了不破坏旧工具继续保留，但新代码不应继续扩张这些 UI 相关能力。

设计原则
--------
1. 属性连接底层只维护一份：connection_utils.py；
2. Transform Reset 底层只维护一份：animation_utils.py；
3. Config 保存 Maya 节点引用优先使用 Message，而不是把节点名写进 String；
4. 模块文件名与所有正式 import 统一使用 snake_case；
5. Channel Box 属于 UI 语义，本模块仅保留旧兼容入口，不再新增同类 API。

兼容
----
Maya 2023+ / maya.cmds
"""

from __future__ import print_function

from ast import literal_eval
from collections import OrderedDict

import maya.cmds as cmds

from . import animation_utils
from . import connection_utils


class Attr(object):
    """以一个 Maya 节点为上下文的属性操作类。"""

    transform_attrs = (
        "translateX",
        "translateY",
        "translateZ",
        "rotateX",
        "rotateY",
        "rotateZ",
        "scaleX",
        "scaleY",
        "scaleZ",
    )

    limit_flags = OrderedDict([
        ("translateX", ("tx", "etx")),
        ("translateY", ("ty", "ety")),
        ("translateZ", ("tz", "etz")),
        ("rotateX", ("rx", "erx")),
        ("rotateY", ("ry", "ery")),
        ("rotateZ", ("rz", "erz")),
        ("scaleX", ("sx", "esx")),
        ("scaleY", ("sy", "esy")),
        ("scaleZ", ("sz", "esz")),
    ])

    limit_attr_aliases = {
        "tx": "translateX",
        "ty": "translateY",
        "tz": "translateZ",
        "rx": "rotateX",
        "ry": "rotateY",
        "rz": "rotateZ",
        "sx": "scaleX",
        "sy": "scaleY",
        "sz": "scaleZ",
    }

    def __init__(self, object, attr=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            object (str):
                Maya 节点名称。
            attr (str/None):
                默认属性名称。

        Notes:
            参数名 ``object`` 来自早期 API。虽然它会遮蔽 Python 内置名称，但为了兼容现有调用，
                                这里暂时不改名。
        """
        self.object = object
        self.attr = attr

        # 早期公开成员，继续保留以避免旧调用报错。
        self.minValue = None
        self.maxValue = None
        self.info = None

    # =========================================================================
    # Validate / Plug
    # =========================================================================

    def object_exists(self):
        u"""
        检查当前 Maya 节点是否存在。

        Returns:
            object:
            方法执行后的结果数据。
        """
        return cmds.objExists(self.object)

    def _get_plug(self, attr=None):
        """把 ``translateX`` 这类短属性整理成完整 ``node.translateX`` Plug。"""
        if attr is None:
            attr = self.attr

        if not attr:
            raise ValueError(u"没有指定需要操作的属性。")

        if "." in attr:
            return attr

        return "{}.{}".format(
            self.object,
            attr
        )

    def attr_exists(self, attr=None):
        u"""
        检查属性 Plug 是否存在。

        Args:
            attr (str):
                Maya Attribute 名称。

        Returns:
            object | bool:
            方法执行后的结果数据。
        """
        try:
            plug = self._get_plug(attr)
        except ValueError:
            return False

        return cmds.objExists(plug)

    # =========================================================================
    # Lock / Hide / Keyable
    # =========================================================================

    def lock_and_hide_attr(self, attr, lock=True, hide=True):
        u"""
        设置单个属性的 Lock / Keyable / Channel Box 状态。

        步骤：
            1. 整理完整 Plug；
            2. 设置 Lock；
            3. 根据 hide 决定是否允许 Key 和是否显示在 Channel Box。

        Args:
            attr (str):
                Maya Attribute 名称。
            lock (bool):
                是否启用 `lock` 对应的处理。
            hide (bool):
                是否启用 `hide` 对应的处理。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        plug = self._get_plug(attr)

        if not cmds.objExists(plug):
            cmds.warning(
                u"【Attr】属性不存在: {}".format(plug)
            )
            return False

        cmds.setAttr(
            plug,
            lock=lock
        )

        if hide:
            cmds.setAttr(
                plug,
                keyable=False,
                channelBox=False
            )
        else:
            cmds.setAttr(
                plug,
                keyable=True,
                channelBox=True
            )

        return True

    def lock_and_hide_attrs(self, attrs_list, lock=True, hide=True):
        u"""
        批量设置属性状态，并返回每个属性的执行结果。

        Args:
            attrs_list (list):
                `attrs_list` 对应的数据列表。
            lock (bool):
                是否启用 `lock` 对应的处理。
            hide (bool):
                是否启用 `hide` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        result = []

        if not attrs_list:
            return result

        for attr in attrs_list:
            state = self.lock_and_hide_attr(
                attr,
                lock=lock,
                hide=hide
            )
            result.append(state)

        return result

    # =========================================================================
    # Create Attribute
    # =========================================================================

    def add_attr(
            self,
            attr,
            attr_type="string",
            lock=True,
            hide=True,
            default_value=None,
            min_value=None,
            max_value=None,
            enum_name=None,
            multi=False,
            **kwargs
    ):
        u"""
        创建自定义属性。

        为兼容早期代码，同时支持 ``attr_type="double"`` 和 ``type="double"`` 两种写法。

        Args:
            attr (str):
                Maya Attribute 名称。
            attr_type (str):
                `attr_type` 对应的名称、标记或字符串参数。
            lock (bool):
                是否启用 `lock` 对应的处理。
            hide (bool):
                是否启用 `hide` 对应的处理。
            default_value (object):
                `default_value` 对应的输入数据。
            min_value (object):
                `min_value` 对应的输入数据。
            max_value (object):
                `max_value` 对应的输入数据。
            enum_name (str):
                `enum_name` 对应的 Maya 节点或资源名称。
            multi (bool):
                是否启用 `multi` 对应的处理。
            kwargs (dict):
                `kwargs` 对应的配置或映射字典。

        Returns:
            object | None:
            方法执行后的结果数据。
        """
        # ---------------------------------------------------------------------
        # 步骤 1：兼容旧参数并验证节点。
        # ---------------------------------------------------------------------
        legacy_type = kwargs.pop("type", None)

        if legacy_type is not None:
            attr_type = legacy_type

        if not self.object_exists():
            cmds.warning(
                u"【Attr】对象不存在: {}".format(self.object)
            )
            return None

        plug = self._get_plug(attr)

        # ---------------------------------------------------------------------
        # 步骤 2：属性已经存在时不重复创建，只同步显示状态。
        # ---------------------------------------------------------------------
        if cmds.objExists(plug):
            self.lock_and_hide_attr(
                attr,
                lock=lock,
                hide=hide
            )
            return plug

        # ---------------------------------------------------------------------
        # 步骤 3：组织 Maya addAttr 参数。
        # String 使用 dataType，其它常规类型使用 attributeType。
        # ---------------------------------------------------------------------
        add_kwargs = {
            "longName": attr,
            "multi": multi,
        }

        if attr_type == "string":
            add_kwargs["dataType"] = "string"
        else:
            add_kwargs["attributeType"] = attr_type

        if default_value is not None and attr_type != "string":
            add_kwargs["defaultValue"] = default_value

        if min_value is not None:
            add_kwargs["minValue"] = min_value

        if max_value is not None:
            add_kwargs["maxValue"] = max_value

        if attr_type == "enum":
            if enum_name is None:
                enum_name = "off:on"
            add_kwargs["enumName"] = enum_name

        for key in kwargs:
            add_kwargs[key] = kwargs[key]

        cmds.addAttr(
            self.object,
            **add_kwargs
        )

        # ---------------------------------------------------------------------
        # 步骤 4：String 默认值必须在属性创建后单独 setAttr。
        # ---------------------------------------------------------------------
        if attr_type == "string" and default_value is not None:
            cmds.setAttr(
                plug,
                str(default_value),
                type="string"
            )

        # ---------------------------------------------------------------------
        # 步骤 5：统一设置 Lock / Hide 状态。
        # ---------------------------------------------------------------------
        self.lock_and_hide_attr(
            attr,
            lock=lock,
            hide=hide
        )

        return plug

    # =========================================================================
    # Connection - 兼容入口，底层统一复用 connection_utils
    # =========================================================================

    def connect_attr(self, output_attr, input_attr, force=True):
        u"""
        连接两个属性；底层使用 ``connection_utils.connect_plugs``。

        Args:
            output_attr (str):
                `output_attr` 对应的名称、标记或字符串参数。
            input_attr (str):
                `input_attr` 对应的名称、标记或字符串参数。
            force (bool):
                是否强制覆盖已有连接、状态或结果。

        Returns:
            object:
            方法执行后的结果数据。
        """
        output_plug = self._get_plug(output_attr)
        input_plug = self._get_plug(input_attr)

        return connection_utils.connect_plugs(
            output_plug,
            input_plug,
            force=force
        )

    def disconnect_attr(self, output_attr, input_attr):
        u"""
        断开两个属性；底层使用 ``connection_utils.disconnect_plugs``。

        Args:
            output_attr (str):
                `output_attr` 对应的名称、标记或字符串参数。
            input_attr (str):
                `input_attr` 对应的名称、标记或字符串参数。

        Returns:
            object:
            方法执行后的结果数据。
        """
        output_plug = self._get_plug(output_attr)
        input_plug = self._get_plug(input_attr)

        return connection_utils.disconnect_plugs(
            output_plug,
            input_plug
        )

    def get_attr_input(self, attr=None, plugs=True):
        u"""
        获取属性输入连接。

        Args:
            attr (str):
                Maya Attribute 名称。
            plugs (bool):
                是否启用 `plugs` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        plug = self._get_plug(attr)

        if plugs:
            return connection_utils.get_input_connections(plug)

        return cmds.listConnections(
            plug,
            source=True,
            destination=False,
            plugs=False
        ) or []

    def get_attr_output(self, attr=None, plugs=True):
        u"""
        获取属性输出连接。

        Args:
            attr (str):
                Maya Attribute 名称。
            plugs (bool):
                是否启用 `plugs` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        plug = self._get_plug(attr)

        if plugs:
            return connection_utils.get_output_connections(plug)

        return cmds.listConnections(
            plug,
            source=False,
            destination=True,
            plugs=False
        ) or []

    # =========================================================================
    # Common Attribute Value
    # =========================================================================

    @staticmethod
    def _infer_attr_type(value):
        """根据 Python 基础值推断 Maya 属性类型。"""
        if isinstance(value, bool):
            return "bool"

        if isinstance(value, int):
            return "long"

        if isinstance(value, float):
            return "double"

        if isinstance(value, str):
            return "string"

        raise TypeError(
            u"【Attr】无法根据数值自动判断 Maya 属性类型: {}".format(
                type(value)
            )
        )

    def set_attr_value(
            self,
            attr,
            value,
            attr_type=None,
            lock=False,
            hide=False,
            min_value=None,
            max_value=None,
            enum_name=None
    ):
        u"""
        如果属性不存在则创建，然后设置属性值。

        Args:
            attr (str):
                Maya Attribute 名称。
            value (float):
                需要读取、写入或参与计算的数值。
            attr_type (object):
                `attr_type` 对应的输入数据。
            lock (bool):
                是否启用 `lock` 对应的处理。
            hide (bool):
                是否启用 `hide` 对应的处理。
            min_value (object):
                `min_value` 对应的输入数据。
            max_value (object):
                `max_value` 对应的输入数据。
            enum_name (str):
                `enum_name` 对应的 Maya 节点或资源名称。

        Returns:
            object | None:
            方法执行后的结果数据。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if value is None:
            return None

        if attr_type is None:
            attr_type = self._infer_attr_type(value)

        if attr_type == "message":
            raise ValueError(
                u"【Attr】message 属性不能使用 set_attr_value，请使用 connect_message。"
            )

        plug = self._get_plug(attr)

        # 步骤 1：确保属性存在，并在写值前解锁。
        if not cmds.objExists(plug):
            self.add_attr(
                attr,
                attr_type=attr_type,
                lock=False,
                hide=hide,
                min_value=min_value,
                max_value=max_value,
                enum_name=enum_name
            )
        else:
            cmds.setAttr(
                plug,
                lock=False
            )

        # 步骤 2：String 与普通数值属性使用不同写法。
        if attr_type == "string":
            cmds.setAttr(
                plug,
                str(value),
                type="string"
            )
        else:
            cmds.setAttr(
                plug,
                value
            )

        # 步骤 3：恢复调用者要求的属性状态。
        self.lock_and_hide_attr(
            attr,
            lock=lock,
            hide=hide
        )

        return plug

    def get_attr_value(self, attr=None):
        u"""
        读取普通 Maya 属性值；属性不存在时返回 None。

        Args:
            attr (str):
                Maya Attribute 名称。

        Returns:
            object | None:
            方法执行后的结果数据。
        """
        plug = self._get_plug(attr)

        if not cmds.objExists(plug):
            return None

        return cmds.getAttr(plug)

    def set_attr_values(
            self,
            attrs_dict,
            attr_types=None,
            lock=False,
            hide=False
    ):
        u"""
        批量创建并设置属性值。

        Args:
            attrs_dict (dict):
                `attrs_dict` 对应的配置或映射字典。
            attr_types (object):
                `attr_types` 对应的输入数据。
            lock (bool):
                是否启用 `lock` 对应的处理。
            hide (bool):
                是否启用 `hide` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        result = {}

        if not attrs_dict:
            return result

        if attr_types is None:
            attr_types = {}

        for attr in attrs_dict:
            result[attr] = self.set_attr_value(
                attr=attr,
                value=attrs_dict.get(attr),
                attr_type=attr_types.get(attr),
                lock=lock,
                hide=hide
            )

        return result

    # =========================================================================
    # Message Configuration
    # =========================================================================

    def add_message_attr(self, attr, multi=False):
        u"""
        创建 Message 属性；已存在时直接返回。

        Args:
            attr (str):
                Maya Attribute 名称。
            multi (bool):
                是否启用 `multi` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        plug = self._get_plug(attr)

        if cmds.objExists(plug):
            return plug

        return self.add_attr(
            attr,
            attr_type="message",
            lock=False,
            hide=True,
            multi=multi
        )

    def disconnect_attr_inputs(self, attr=None):
        u"""
        断开指定属性的全部输入连接。

        Args:
            attr (str):
                Maya Attribute 名称。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        input_plug = self._get_plug(attr)

        if not cmds.objExists(input_plug):
            return False

        connection_utils.disconnect_input(
            input_plug
        )
        return True

    def connect_message(
            self,
            source_node,
            attr=None,
            force=True,
            clear_empty=False
    ):
        u"""
        把 ``source_node.message`` 保存到当前节点的 Message 属性。

        Message 连接比保存节点名称字符串更可靠，因为 Maya Rename 后会自动维护连接关系。

        Args:
            source_node (object):
                `source_node` 对应的输入数据。
            attr (str):
                Maya Attribute 名称。
            force (bool):
                是否强制覆盖已有连接、状态或结果。
            clear_empty (bool):
                是否启用 `clear_empty` 对应的处理。

        Returns:
            object | bool:
            方法执行后的结果数据。
        """
        input_plug = self._get_plug(attr)
        attr_name = input_plug.split(".", 1)[1]

        # 步骤 1：处理 UI 清空模型等空值情况。
        if source_node is None or source_node == "":
            if not clear_empty:
                return False

            if not cmds.objExists(input_plug):
                self.add_message_attr(attr_name)

            self.disconnect_attr_inputs(input_plug)
            return True

        # 步骤 2：验证来源节点并确保 Message 属性存在。
        if not cmds.objExists(source_node):
            cmds.warning(
                u"【Attr】Message 来源节点不存在: {}".format(source_node)
            )
            return False

        if not cmds.objExists(input_plug):
            self.add_message_attr(attr_name)

        # 步骤 3：建立 source.message -> config.messageAttr。
        source_plug = "{}.message".format(source_node)

        return self.connect_attr(
            source_plug,
            input_plug,
            force=force
        )

    def connect_messages(
            self,
            attrs_dict,
            force=True,
            clear_empty=False
    ):
        u"""
        批量保存多个 Maya 节点 Message 引用。

        Args:
            attrs_dict (dict):
                `attrs_dict` 对应的配置或映射字典。
            force (bool):
                是否强制覆盖已有连接、状态或结果。
            clear_empty (bool):
                是否启用 `clear_empty` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        result = {}

        if not attrs_dict:
            return result

        for attr in attrs_dict:
            result[attr] = self.connect_message(
                source_node=attrs_dict.get(attr),
                attr=attr,
                force=force,
                clear_empty=clear_empty
            )

        return result

    def get_message(self, attr=None, plugs=False):
        u"""
        读取 Message 属性的第一个来源节点或来源 Plug。

        Args:
            attr (str):
                Maya Attribute 名称。
            plugs (bool):
                是否启用 `plugs` 对应的处理。

        Returns:
            object | None:
            方法执行后的结果数据。
        """
        connections = self.get_attr_input(
            attr=attr,
            plugs=plugs
        )

        if not connections:
            return None

        return connections[0]

    # =========================================================================
    # String Configuration
    # =========================================================================

    def add_string_info(self, information, attr=None, lock=True, hide=True):
        u"""
        把 Python 基础数据保存到 Maya String 属性。

        list / tuple / dict 等通过 repr() 保存，读取时使用 literal_eval() 安全恢复。

        Args:
            information (object):
                `information` 对应的输入数据。
            attr (str):
                Maya Attribute 名称。
            lock (bool):
                是否启用 `lock` 对应的处理。
            hide (bool):
                是否启用 `hide` 对应的处理。

        Returns:
            object:
            方法执行后的结果数据。
        """
        plug = self._get_plug(attr)
        attr_name = plug.split(".", 1)[1]

        if not cmds.objExists(plug):
            self.add_attr(
                attr_name,
                attr_type="string",
                lock=False,
                hide=hide
            )

        cmds.setAttr(
            plug,
            lock=False
        )

        if information is None:
            string_information = ""
        elif isinstance(information, str):
            string_information = information
        else:
            string_information = repr(information)

        cmds.setAttr(
            plug,
            string_information,
            type="string"
        )

        if hide:
            cmds.setAttr(
                plug,
                keyable=False,
                channelBox=False
            )
        else:
            cmds.setAttr(
                plug,
                keyable=False,
                channelBox=True
            )

        cmds.setAttr(
            plug,
            lock=lock
        )

        return plug

    def get_string_info(self, attr=None):
        u"""
        读取 String 信息，并尽量恢复为原 Python 基础数据。

        Args:
            attr (str):
                Maya Attribute 名称。

        Returns:
            None | object:
            方法执行后的结果数据。
        """
        plug = self._get_plug(attr)

        if not cmds.objExists(plug):
            return None

        string_information = cmds.getAttr(plug)

        if string_information is None or string_information == "":
            return None

        try:
            return literal_eval(string_information)
        except (ValueError, SyntaxError, TypeError):
            return string_information

    # =========================================================================
    # Transform Limits
    # =========================================================================

    def _get_limit_attr_name(self, attr):
        """把 tx / ry / sz 等短属性名转换成长名称。"""
        if attr in self.limit_attr_aliases:
            return self.limit_attr_aliases[attr]

        return attr

    def set_attrs_limits(self, attrs_dict):
        u"""
        批量设置 Transform Limits。

        Args:
            attrs_dict (dict):
                `attrs_dict` 对应的配置或映射字典。

        Returns:
            bool:
            方法执行后的结果数据。

        Example:
            {
                                    "translateY": [(True, True), (-10.0, 10.0)],
                                    "rotateX": [(True, False), (-45.0, 0.0)],
                                }
        """
        if not self.object_exists():
            cmds.warning(
                u"【Attr】对象不存在: {}".format(self.object)
            )
            return False

        if not attrs_dict:
            return True

        for attr in attrs_dict:
            attr_name = self._get_limit_attr_name(attr)

            if attr_name not in self.limit_flags:
                cmds.warning(
                    u"【Attr】不支持 transformLimits 的属性: {}".format(attr)
                )
                continue

            limit_data = attrs_dict[attr]

            if not isinstance(limit_data, (list, tuple)) or len(limit_data) != 2:
                cmds.warning(
                    u"【Attr】属性限制数据格式错误: {}".format(attr)
                )
                continue

            limit_state = limit_data[0]
            limits = limit_data[1]

            if len(limit_state) != 2 or len(limits) != 2:
                cmds.warning(
                    u"【Attr】属性限制必须包含两个开关和两个数值: {}".format(attr)
                )
                continue

            value_flag = self.limit_flags[attr_name][0]
            enable_flag = self.limit_flags[attr_name][1]

            cmds.transformLimits(
                self.object,
                **{
                    enable_flag: (
                        bool(limit_state[0]),
                        bool(limit_state[1]),
                    ),
                    value_flag: (
                        limits[0],
                        limits[1],
                    ),
                }
            )

        return True

    def get_attrs_limits(self, attrs_list=None):
        u"""
        读取 Transform Limits，统一返回 OrderedDict。

        Args:
            attrs_list (list):
                `attrs_list` 对应的数据列表。

        Returns:
            object:
            方法执行后的结果数据。
        """
        result = OrderedDict()

        if not self.object_exists():
            return result

        if attrs_list is None:
            attrs_list = []

            for attr in self.transform_attrs:
                attrs_list.append(attr)

        for attr in attrs_list:
            attr_name = self._get_limit_attr_name(attr)

            if attr_name not in self.limit_flags:
                continue

            value_flag = self.limit_flags[attr_name][0]
            enable_flag = self.limit_flags[attr_name][1]

            limit_state = cmds.transformLimits(
                self.object,
                query=True,
                **{enable_flag: True}
            )
            limit_value = cmds.transformLimits(
                self.object,
                query=True,
                **{value_flag: True}
            )

            result[attr_name] = (
                (
                    bool(limit_state[0]),
                    bool(limit_state[1]),
                ),
                (
                    limit_value[0],
                    limit_value[1],
                ),
            )

        return result

    def get_unwanted_attrs(self, attrs_list):
        u"""
        根据需要保留的 Transform 属性，返回其它需要锁定 / 隐藏的通道。

        Args:
            attrs_list (list):
                `attrs_list` 对应的数据列表。

        Returns:
            object:
            方法执行后的结果数据。
        """
        attrs_to_lock = []

        for attr in self.transform_attrs:
            attrs_to_lock.append(attr)

        if not attrs_list:
            return attrs_to_lock

        for attr in attrs_list:
            attr_name = self._get_limit_attr_name(attr)

            if attr_name in attrs_to_lock:
                attrs_to_lock.remove(attr_name)

        return attrs_to_lock

    # =========================================================================
    # Channel Box - Legacy Compatibility
    # =========================================================================

    @staticmethod
    def get_channelBox_attrs():
        u"""
        返回 Maya Main Channel Box 当前选中的属性长名称。

        该 API 涉及 Maya UI 状态，正式新代码应优先把这类逻辑放到 Tool 层；这里只为旧工具兼容保留。

        Returns:
            object:
            方法执行后的结果数据。
        """
        query_pairs = [
            ("mainObjectList", "selectedMainAttributes"),
            ("historyObjectList", "selectedHistoryAttributes"),
            ("shapeObjectList", "selectedShapeAttributes"),
        ]

        attr_names = []

        for object_flag, attr_flag in query_pairs:
            objects = cmds.channelBox(
                "mainChannelBox",
                query=True,
                **{object_flag: True}
            ) or []
            attrs = cmds.channelBox(
                "mainChannelBox",
                query=True,
                **{attr_flag: True}
            ) or []

            if not attrs:
                continue

            for node_name in objects:
                for attr in attrs:
                    try:
                        long_name = cmds.attributeQuery(
                            attr,
                            node=node_name,
                            longName=True
                        )
                    except RuntimeError:
                        continue

                    if long_name not in attr_names:
                        attr_names.append(long_name)

        if not attr_names:
            cmds.warning(u"请在通道盒中选择属性")

        return attr_names

    @staticmethod
    def move_channelBox_attr(up=True, down=False):
        u"""
        调整当前节点一个 User Defined 属性在 Channel Box 中的顺序。

        这是 Maya 的历史兼容技巧：利用 deleteAttr + undo 改变 User Defined 属性顺序。
        新代码如果不需要这种行为，不建议依赖此方法。

        Args:
            up (bool):
                是否启用 `up` 对应的处理。
            down (bool):
                是否启用 `down` 对应的处理。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        selections = cmds.ls(
            selection=True,
            long=True
        ) or []

        if not selections:
            cmds.warning(u"请先选择一个对象。")
            return False

        selected_attrs = cmds.channelBox(
            "mainChannelBox",
            query=True,
            selectedMainAttributes=True
        ) or []

        if not selected_attrs:
            cmds.warning(u"请在 Channel Box 中选择一个自定义属性。")
            return False

        node = selections[0]
        selected_attr = selected_attrs[0]
        selected_plug = "{}.{}".format(
            node,
            selected_attr
        )

        if cmds.getAttr(
                selected_plug,
                lock=True
        ):
            cmds.warning(
                u"{} 属性不可以被编辑".format(selected_plug)
            )
            return False

        attr_list = cmds.listAttr(
            node,
            userDefined=True
        ) or []

        if selected_attr not in attr_list:
            return False

        selected_index = attr_list.index(selected_attr)

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziMoveChannelBoxAttr"
        )

        try:
            if up and selected_index > 0:
                previous_attr = attr_list[selected_index - 1]
                cmds.deleteAttr(
                    "{}.{}".format(node, previous_attr)
                )
                cmds.undo()

                index = selected_index + 1

                while index < len(attr_list):
                    cmds.deleteAttr(
                        "{}.{}".format(node, attr_list[index])
                    )
                    cmds.undo()
                    index += 1

            if down and selected_index < len(attr_list) - 1:
                cmds.deleteAttr(selected_plug)
                cmds.undo()

                index = selected_index + 2

                while index < len(attr_list):
                    cmds.deleteAttr(
                        "{}.{}".format(node, attr_list[index])
                    )
                    cmds.undo()
                    index += 1
        finally:
            cmds.undoInfo(
                closeChunk=True
            )

        return True

    # =========================================================================
    # Legacy Static Wrappers
    # =========================================================================

    @staticmethod
    def set_lock_attr(node, attr, lock=True):
        u"""
        兼容旧 API：设置属性 Lock 状态。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。
            attr (str):
                Maya Attribute 名称。
            lock (bool):
                是否启用 `lock` 对应的处理。
        """
        cmds.setAttr(
            "{}.{}".format(node, attr),
            lock=lock
        )

    @staticmethod
    def set_hide_attr(node, attr, hide=True):
        u"""
        兼容旧 API：隐藏或显示属性。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。
            attr (str):
                Maya Attribute 名称。
            hide (bool):
                是否启用 `hide` 对应的处理。
        """
        plug = "{}.{}".format(node, attr)

        if hide:
            cmds.setAttr(
                plug,
                keyable=False,
                channelBox=False
            )
        else:
            cmds.setAttr(
                plug,
                keyable=True,
                channelBox=True
            )

    @staticmethod
    def set_key_attr(node, attr, keyable=True):
        u"""
        兼容旧 API：设置属性是否 Keyable。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。
            attr (str):
                Maya Attribute 名称。
            keyable (bool):
                是否启用 `keyable` 对应的处理。
        """
        cmds.setAttr(
            "{}.{}".format(node, attr),
            keyable=keyable
        )

    @staticmethod
    def lock_hide_attr(node, attr, lock=True, hide=True):
        u"""
        兼容旧 API：组合设置 Lock 与 Hide。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。
            attr (str):
                Maya Attribute 名称。
            lock (bool):
                是否启用 `lock` 对应的处理。
            hide (bool):
                是否启用 `hide` 对应的处理。
        """
        Attr.set_lock_attr(
            node,
            attr,
            lock=lock
        )
        Attr.set_hide_attr(
            node,
            attr,
            hide=hide
        )

    @staticmethod
    def reset_attr(node):
        u"""
        兼容旧 API：重置节点 TRS。

        底层统一转调 animation_utils.reset_transform_channels，避免维护第二套 Reset 算法。

        Args:
            node (str):
                需要查询或处理的 Maya 节点名称。

        Returns:
            object:
            方法执行后的结果数据。
        """
        result = animation_utils.reset_transform_channels(
            [node]
        )

        return node in result


__all__ = [
    "Attr",
]
