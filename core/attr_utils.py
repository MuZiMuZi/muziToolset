# coding=utf-8
u"""
Attribute Utils
===============

Maya 单节点 Attribute 的通用底层能力模块。

模块职责
--------
- Attribute 存在性查询；
- Attribute 创建；
- Lock / Keyable / Channel Box 状态；
- 普通 Attribute Value 读写；
- Message Attribute 与节点引用；
- Transform Limits。

模块边界
--------
- 通用 Plug -> Plug 连接     -> connection_utils
- Channel Box / Selection UI -> tools
- Transform Reset            -> animation_utils
- 结构化配置语义             -> config_utils

设计原则
--------
1. Attr 是有状态对象，构造时确认当前 Maya Node 有效；
2. Attr(node) 只操作这个 node 自己的 Attribute，不借完整 Plug 越界操作其它节点；
3. 修改 Value 不应顺手改变已有 Attribute 的 Lock / Keyable / Channel Box 状态；
4. 已存在的 Attribute 不因 add_attr() 再次调用而被静默改状态；
5. Message 是 Attribute 的明确语义，可以留在 Attr；通用 DG Connection 只有 connection_utils 一个正式入口。

兼容
----
Maya 2023+ / maya.cmds
"""

from __future__ import print_function

from ast import literal_eval
from collections import OrderedDict

import maya.cmds as cmds

from . import connection_utils
from . import scene_utils


class Attr(object):
    u"""以一个有效 Maya Node 为上下文的 Attribute 操作对象。"""

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

    _legacy_string_prefix = "__muzi_string__:"
    _legacy_repr_prefix = "__muzi_repr__:"

    def __init__(self, node=None, attr=None, **kwargs):
        u"""
        创建 Attribute 操作对象。

        Args:
            node (str):
                Maya Node 名称。
            attr (str | None):
                可选默认 Attribute 名称。
            kwargs (dict):
                继续传递给底层 maya.cmds、Qt 或 Builder API 的关键字参数。

        Raises:
            TypeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。

        Notes:
            旧代码如果仍使用 ``Attr(object=node)``，这里暂时接受该关键字；
                    正式新代码统一使用 ``node``。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        legacy_object = kwargs.pop(
            "object",
            None
        )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if kwargs:
            unknown_keys = []

            for key in kwargs:
                unknown_keys.append(
                    key
                )

            raise TypeError(
                u"Attr 不支持参数：{}".format(
                    ", ".join(unknown_keys)
                )
            )

        if node is None:
            node = legacy_object
        elif legacy_object is not None and legacy_object != node:
            raise ValueError(
                u"node 与旧 object 参数不能指向不同节点。"
            )

        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.node = scene_utils.get_long_name(
            node
        )
        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.attr = attr

        # -------------------------------------------------------------------------
        # Step 05：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.object = self.node

    def _get_plug(self, attr=None):
        u"""把短 Attribute 名称整理为当前节点的完整 Plug。"""
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if attr is None:
            attr = self.attr

        if not attr:
            raise ValueError(
                u"没有指定需要操作的 Attribute。"
            )

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        attr = str(attr).strip()

        if not attr:
            raise ValueError(
                u"没有指定需要操作的 Attribute。"
            )

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if "." not in attr:
            return "{}.{}".format(
                self.node,
                attr
            )

        plug_node = attr.split(
            ".",
            1
        )[0]
        # -------------------------------------------------------------------------
        # Step 04：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        plug_node = scene_utils.get_long_name(
            plug_node
        )

        if plug_node != self.node:
            raise ValueError(
                u"Attr({}) 不能操作其它节点的 Plug：{}".format(
                    self.node,
                    attr
                )
            )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return attr

    def _get_attr_name(self, attr=None):
        u"""返回当前节点 Plug 中的 Attribute 名称部分。"""
        plug = self._get_plug(
            attr
        )
        return plug.split(
            ".",
            1
        )[1]

    def attr_exists(self, attr=None):
        u"""
        检查当前节点的 Attribute Plug 是否存在。

        Args:
            attr (str):
                Maya Attribute 名称。

        Returns:
            object | bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        try:
            plug = self._get_plug(
                attr
            )
        except ValueError:
            return False

        return bool(
            cmds.objExists(
                plug
            )
        )

    def set_attr_state(
            self,
            attr,
            lock=None,
            keyable=None,
            channel_box=None
    ):
        u"""
        明确修改一个 Attribute 的状态；None 表示不修改对应状态。

        Args:
            attr (str):
                Maya Attribute 名称。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            keyable (bool):
                对应 Maya Attribute 是否允许 Animator Keyframe。
            channel_box (object):
                当前方法执行 Maya / Rig 操作时使用的 `channel_box` 数据。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        plug = self._get_plug(
            attr
        )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not cmds.objExists(plug):
            cmds.warning(
                u"【Attr】Attribute 不存在：{}".format(
                    plug
                )
            )
            return False

        if lock is not None:
            cmds.setAttr(
                plug,
                lock=bool(lock)
            )

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if keyable is not None:
            cmds.setAttr(
                plug,
                keyable=bool(keyable)
            )

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if channel_box is not None:
            cmds.setAttr(
                plug,
                channelBox=bool(channel_box)
            )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def set_attrs_state(
            self,
            attrs,
            lock=None,
            keyable=None,
            channel_box=None
    ):
        u"""
        批量修改多个 Attribute 的状态。

        Args:
            attrs (str | list[str]):
                当前方法按顺序处理的 `attrs` 数据集合。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            keyable (bool):
                对应 Maya Attribute 是否允许 Animator Keyframe。
            channel_box (object):
                当前方法执行 Maya / Rig 操作时使用的 `channel_box` 数据。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。
        """
        result = []

        if not attrs:
            return result

        for attr in attrs:
            state = self.set_attr_state(
                attr,
                lock=lock,
                keyable=keyable,
                channel_box=channel_box
            )
            result.append(
                state
            )

        return result

    @staticmethod
    def _build_add_attr_kwargs(
            attr,
            attr_type,
            default_value=None,
            min_value=None,
            max_value=None,
            enum_name=None,
            multi=False,
            extra_kwargs=None
    ):
        u"""组织 maya.cmds.addAttr 所需参数。"""
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        add_kwargs = {
            "longName": attr,
            "multi": bool(multi),
        }

        if attr_type == "string":
            add_kwargs["dataType"] = "string"
        else:
            add_kwargs["attributeType"] = attr_type

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if default_value is not None and attr_type != "string":
            add_kwargs["defaultValue"] = default_value

        if min_value is not None:
            add_kwargs["minValue"] = min_value

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if max_value is not None:
            add_kwargs["maxValue"] = max_value

        if attr_type == "enum":
            if enum_name is None:
                enum_name = "off:on"
            add_kwargs["enumName"] = enum_name

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if extra_kwargs:
            for key in extra_kwargs:
                add_kwargs[key] = extra_kwargs[key]

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return add_kwargs

    def _create_attr(
            self,
            attr,
            attr_type,
            default_value=None,
            min_value=None,
            max_value=None,
            enum_name=None,
            multi=False,
            extra_kwargs=None
    ):
        u"""只创建 Attribute Definition，不修改 Channel 状态。"""
        add_kwargs = self._build_add_attr_kwargs(
            attr=attr,
            attr_type=attr_type,
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            enum_name=enum_name,
            multi=multi,
            extra_kwargs=extra_kwargs
        )

        cmds.addAttr(
            self.node,
            **add_kwargs
        )

        plug = self._get_plug(
            attr
        )

        if attr_type == "string" and default_value is not None:
            cmds.setAttr(
                plug,
                str(default_value),
                type="string"
            )

        return plug

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
            keyable=None,
            channel_box=None,
            **kwargs
    ):
        u"""
        创建自定义 Attribute；已存在时只返回 Plug，不静默修改原状态。

        Args:
            attr (str):
                Maya Attribute 名称。
            attr_type (str):
                创建 Maya Attribute 使用的数据类型，例如 double、long、bool、string 或 message。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            hide (bool):
                是否从 Channel Box 隐藏对应 Maya Attribute。
            default_value (object):
                新建 Attribute、UI 控件或 Rig 参数使用的默认值。
            min_value (float | int | None):
                Attribute / UI 数值允许的最小值；None 表示不设置下限。
            max_value (float | int | None):
                Attribute / UI 数值允许的最大值；None 表示不设置上限。
            enum_name (str):
                `enum_name` 对应的 Maya 节点或资源名称。
            multi (bool):
                创建 Maya Attribute 时是否使用 Multi / Array Attribute。
            keyable (bool):
                对应 Maya Attribute 是否允许 Animator Keyframe。
            channel_box (object):
                当前方法执行 Maya / Rig 操作时使用的 `channel_box` 数据。
            kwargs (dict):
                继续传递给底层 maya.cmds、Qt 或 Builder API 的关键字参数。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        legacy_type = kwargs.pop(
            "type",
            None
        )

        if legacy_type is not None:
            attr_type = legacy_type

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        attr_name = self._get_attr_name(
            attr
        )
        plug = self._get_plug(
            attr_name
        )

        if cmds.objExists(plug):
            existing_type = cmds.getAttr(
                plug,
                type=True
            )

            if existing_type != attr_type:
                raise RuntimeError(
                    u"Attribute 已存在但类型不同：{} | existing={} requested={}".format(
                        plug,
                        existing_type,
                        attr_type
                    )
                )

            return plug

        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        plug = self._create_attr(
            attr=attr_name,
            attr_type=attr_type,
            default_value=default_value,
            min_value=min_value,
            max_value=max_value,
            enum_name=enum_name,
            multi=multi,
            extra_kwargs=kwargs
        )

        if keyable is None:
            keyable = not bool(hide)

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if channel_box is None:
            channel_box = not bool(hide)

        self.set_attr_state(
            attr_name,
            lock=lock,
            keyable=keyable,
            channel_box=channel_box
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return plug

    @staticmethod
    def _infer_attr_type(value):
        u"""根据 Python 基础值推断常用 Maya Attribute Type。"""
        if isinstance(value, bool):
            return "bool"
        if isinstance(value, int):
            return "long"
        if isinstance(value, float):
            return "double"
        if isinstance(value, str):
            return "string"

        raise TypeError(
            u"【Attr】无法根据数值自动判断 Maya Attribute Type：{}".format(
                type(value)
            )
        )

    @staticmethod
    def _set_plug_value(plug, value, attr_type):
        u"""按 Maya Attribute Type 写入单个 Plug Value。"""
        if attr_type == "string":
            cmds.setAttr(
                plug,
                str(value),
                type="string"
            )
            return

        cmds.setAttr(
            plug,
            value
        )

    def set_value(
            self,
            attr,
            value,
            attr_type=None,
            min_value=None,
            max_value=None,
            enum_name=None,
            lock=None,
            keyable=None,
            channel_box=None
    ):
        u"""
        创建或写入普通 Attribute Value，并保留未显式要求修改的原状态。

        Args:
            attr (str):
                Maya Attribute 名称。
            value (float):
                需要读取、写入或参与计算的数值。
            attr_type (str):
                创建 Maya Attribute 使用的数据类型，例如 double、long、bool、string 或 message。
            min_value (float | int | None):
                Attribute / UI 数值允许的最小值；None 表示不设置下限。
            max_value (float | int | None):
                Attribute / UI 数值允许的最大值；None 表示不设置上限。
            enum_name (str):
                `enum_name` 对应的 Maya 节点或资源名称。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            keyable (bool):
                对应 Maya Attribute 是否允许 Animator Keyframe。
            channel_box (object):
                当前方法执行 Maya / Rig 操作时使用的 `channel_box` 数据。

        Returns:
            object | None:
            完成设置或应用后的目标对象 / 状态结果。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if value is None:
            return None

        attr_name = self._get_attr_name(
            attr
        )
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        plug = self._get_plug(
            attr_name
        )
        attr_exists = cmds.objExists(
            plug
        )

        if attr_exists:
            existing_type = cmds.getAttr(
                plug,
                type=True
            )
            if attr_type is None:
                attr_type = existing_type
        else:
            if attr_type is None:
                attr_type = self._infer_attr_type(
                    value
                )

            if attr_type == "message":
                raise ValueError(
                    u"Message Attribute 不能通过 set_value() 写值，请使用 connect_message()。"
                )

            self._create_attr(
                attr=attr_name,
                attr_type=attr_type,
                min_value=min_value,
                max_value=max_value,
                enum_name=enum_name
            )

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if attr_type == "message":
            raise ValueError(
                u"Message Attribute 不能通过 set_value() 写值，请使用 connect_message()。"
            )

        original_lock = bool(
            cmds.getAttr(
                plug,
                lock=True
            )
        )

        if original_lock:
            cmds.setAttr(
                plug,
                lock=False
            )

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            self._set_plug_value(
                plug,
                value,
                attr_type
            )
        finally:
            if original_lock:
                cmds.setAttr(
                    plug,
                    lock=True
                )

        self.set_attr_state(
            attr_name,
            lock=lock,
            keyable=keyable,
            channel_box=channel_box
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return plug

    def get_value(self, attr=None):
        u"""
        读取当前节点 Attribute Value；属性不存在时返回 None。

        Args:
            attr (str):
                Maya Attribute 名称。

        Returns:
            object | None:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        plug = self._get_plug(
            attr
        )
        if not cmds.objExists(plug):
            return None
        return cmds.getAttr(
            plug
        )

    def set_values(
            self,
            attrs_dict,
            attr_types=None,
            lock=None,
            keyable=None,
            channel_box=None
    ):
        u"""
        批量创建或写入普通 Attribute Value。

        Args:
            attrs_dict (dict):
                Attribute 名称到 Value / Config 数据的批量映射。
            attr_types (dict | None):
                Attribute 名称到 Maya Attribute Type 的映射；未指定的属性由调用方默认规则处理。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            keyable (bool):
                对应 Maya Attribute 是否允许 Animator Keyframe。
            channel_box (object):
                当前方法执行 Maya / Rig 操作时使用的 `channel_box` 数据。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        result = {}
        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not attrs_dict:
            return result
        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if attr_types is None:
            attr_types = {}

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for attr in attrs_dict:
            result[attr] = self.set_value(
                attr=attr,
                value=attrs_dict.get(attr),
                attr_type=attr_types.get(attr),
                lock=lock,
                keyable=keyable,
                channel_box=channel_box
            )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return result

    def add_message_attr(self, attr, multi=False):
        u"""
        创建 Message Attribute；已存在时验证类型并直接返回。

        Args:
            attr (str):
                Maya Attribute 名称。
            multi (bool):
                创建 Maya Attribute 时是否使用 Multi / Array Attribute。

        Returns:
            object:
            当前 API 完成处理后返回的结果。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        attr_name = self._get_attr_name(
            attr
        )
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        plug = self._get_plug(
            attr_name
        )

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if cmds.objExists(plug):
            existing_type = cmds.getAttr(
                plug,
                type=True
            )
            if existing_type != "message":
                raise RuntimeError(
                    u"Attribute 已存在但不是 Message：{} | type={}".format(
                        plug,
                        existing_type
                    )
                )
            return plug

        # -------------------------------------------------------------------------
        # Step 04：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.add_attr(
            attr_name,
            attr_type="message",
            lock=False,
            hide=True,
            multi=multi
        )

    def connect_message(
            self,
            source_node,
            attr=None,
            force=True,
            clear_empty=False
    ):
        u"""
        把 source_node.message 保存到当前节点的 Message Attribute。

        Args:
            source_node (str):
                作为数据来源、复制来源或驱动来源的 Maya 节点。
            attr (str):
                Maya Attribute 名称。
            force (bool):
                是否强制覆盖已有连接、状态或结果。
            clear_empty (bool):
                批量保存 Message / Config 时，空值是否主动断开旧连接。

        Returns:
            object | bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        attr_name = self._get_attr_name(
            attr
        )
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        destination_plug = self._get_plug(
            attr_name
        )

        if source_node is None or source_node == "":
            if not clear_empty:
                return False

            if not cmds.objExists(destination_plug):
                self.add_message_attr(
                    attr_name
                )

            connection_utils.disconnect_input(
                destination_plug
            )
            return True

        # -------------------------------------------------------------------------
        # Step 03：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            source_node = scene_utils.get_long_name(
                source_node
            )
        except RuntimeError as error:
            cmds.warning(
                str(error)
            )
            return False

        if not cmds.objExists(destination_plug):
            self.add_message_attr(
                attr_name
            )

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        source_plug = "{}.message".format(
            source_node
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return connection_utils.connect_plugs(
            source_plug,
            destination_plug,
            force=force
        )

    def connect_messages(
            self,
            attrs_dict,
            force=True,
            clear_empty=False
    ):
        u"""
        批量保存多个 Maya Node Message 引用。

        Args:
            attrs_dict (dict):
                Attribute 名称到 Value / Config 数据的批量映射。
            force (bool):
                是否强制覆盖已有连接、状态或结果。
            clear_empty (bool):
                批量保存 Message / Config 时，空值是否主动断开旧连接。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
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
        读取 Message Attribute 的第一个来源 Node 或来源 Plug。

        Args:
            attr (str):
                Maya Attribute 名称。
            plugs (bool):
                查询连接时是否返回完整 Plug；False 时通常只返回节点名称。

        Returns:
            object | None:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        destination_plug = self._get_plug(
            attr
        )
        if not cmds.objExists(destination_plug):
            return None

        connections = connection_utils.get_input_connections(
            destination_plug
        )
        if not connections:
            return None

        source_plug = connections[0]
        if plugs:
            return source_plug

        return source_plug.split(
            ".",
            1
        )[0]

    def _get_limit_attr_name(self, attr):
        u"""把 tx / ry / sz 等短名称转换为长 Attribute 名称。"""
        if attr in self.limit_attr_aliases:
            return self.limit_attr_aliases[attr]
        return attr

    def _validate_transform_limits_node(self):
        u"""确认当前节点可以使用 cmds.transformLimits。"""
        node_type = cmds.nodeType(
            self.node
        )
        if node_type not in ["transform", "joint"]:
            raise RuntimeError(
                u"Transform Limits 只支持 Transform / Joint：{} | type={}".format(
                    self.node,
                    node_type
                )
            )

    def set_attrs_limits(self, attrs_dict):
        u"""
        批量设置 Transform Limits。

        Args:
            attrs_dict (dict):
                Attribute 名称到 Value / Config 数据的批量映射。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self._validate_transform_limits_node()
        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not attrs_dict:
            return True

        # -------------------------------------------------------------------------
        # Step 03：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for attr in attrs_dict:
            attr_name = self._get_limit_attr_name(
                attr
            )
            if attr_name not in self.limit_flags:
                cmds.warning(
                    u"【Attr】不支持 transformLimits 的 Attribute：{}".format(
                        attr
                    )
                )
                continue

            limit_data = attrs_dict[attr]
            if not isinstance(limit_data, (list, tuple)) or len(limit_data) != 2:
                cmds.warning(
                    u"【Attr】Transform Limit 数据格式错误：{}".format(
                        attr
                    )
                )
                continue

            limit_state = limit_data[0]
            limits = limit_data[1]
            if len(limit_state) != 2 or len(limits) != 2:
                cmds.warning(
                    u"【Attr】Transform Limit 必须包含两个开关和两个数值：{}".format(
                        attr
                    )
                )
                continue

            value_flag = self.limit_flags[attr_name][0]
            enable_flag = self.limit_flags[attr_name][1]
            cmds.transformLimits(
                self.node,
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

        # -------------------------------------------------------------------------
        # Step 04：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def get_attrs_limits(self, attrs_list=None):
        u"""
        读取 Transform Limits，并返回 OrderedDict。

        Args:
            attrs_list (list):
                需要批量查询、Lock、Hide 或处理的 Attribute 名称列表。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self._validate_transform_limits_node()
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        result = OrderedDict()

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if attrs_list is None:
            attrs_list = []
            for attr in self.transform_attrs:
                attrs_list.append(
                    attr
                )

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for attr in attrs_list:
            attr_name = self._get_limit_attr_name(
                attr
            )
            if attr_name not in self.limit_flags:
                continue

            value_flag = self.limit_flags[attr_name][0]
            enable_flag = self.limit_flags[attr_name][1]
            limit_state = cmds.transformLimits(
                self.node,
                query=True,
                **{enable_flag: True}
            )
            limit_value = cmds.transformLimits(
                self.node,
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

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return result

    # Legacy Compatibility -----------------------------------------------------
    def lock_and_hide_attr(self, attr, lock=True, hide=True):
        u"""
        旧 API：请新代码改用 set_attr_state()。

        Args:
            attr (str):
                Maya Attribute 名称。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            hide (bool):
                是否从 Channel Box 隐藏对应 Maya Attribute。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self.set_attr_state(
            attr,
            lock=lock,
            keyable=not hide,
            channel_box=not hide
        )

    def lock_and_hide_attrs(self, attrs_list, lock=True, hide=True):
        u"""
        旧 API：请新代码改用 set_attrs_state()。

        Args:
            attrs_list (list):
                需要批量查询、Lock、Hide 或处理的 Attribute 名称列表。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            hide (bool):
                是否从 Channel Box 隐藏对应 Maya Attribute。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self.set_attrs_state(
            attrs_list,
            lock=lock,
            keyable=not hide,
            channel_box=not hide
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
        旧 API：请新代码改用 set_value()。

        Args:
            attr (str):
                Maya Attribute 名称。
            value (float):
                需要读取、写入或参与计算的数值。
            attr_type (str):
                创建 Maya Attribute 使用的数据类型，例如 double、long、bool、string 或 message。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            hide (bool):
                是否从 Channel Box 隐藏对应 Maya Attribute。
            min_value (float | int | None):
                Attribute / UI 数值允许的最小值；None 表示不设置下限。
            max_value (float | int | None):
                Attribute / UI 数值允许的最大值；None 表示不设置上限。
            enum_name (str):
                `enum_name` 对应的 Maya 节点或资源名称。

        Returns:
            object:
            完成设置或应用后的目标对象 / 状态结果。
        """
        # -------------------------------------------------------------------------
        # Step 01：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.set_value(
            attr=attr,
            value=value,
            attr_type=attr_type,
            min_value=min_value,
            max_value=max_value,
            enum_name=enum_name,
            lock=lock,
            keyable=not hide,
            channel_box=not hide
        )

    def get_attr_value(self, attr=None):
        u"""
        旧 API：请新代码改用 get_value()。

        Args:
            attr (str):
                Maya Attribute 名称。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        return self.get_value(
            attr
        )

    def set_attr_values(
            self,
            attrs_dict,
            attr_types=None,
            lock=False,
            hide=False
    ):
        u"""
        旧 API：请新代码改用 set_values()。

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
            完成设置或应用后的目标对象 / 状态结果。
        """
        return self.set_values(
            attrs_dict=attrs_dict,
            attr_types=attr_types,
            lock=lock,
            keyable=not hide,
            channel_box=not hide
        )

    def add_string_info(
            self,
            information,
            attr=None,
            lock=True,
            hide=True
    ):
        u"""
        旧结构化 String API；新写入增加类型前缀，避免字符串被误解析成其它 Python 类型。

        Args:
            information (dict | list | object):
                需要写入、恢复或应用到 Maya Attribute 的结构化信息。
            attr (str):
                Maya Attribute 名称。
            lock (bool):
                是否 Lock 对应 Maya Channel / Attribute。
            hide (bool):
                是否从 Channel Box 隐藏对应 Maya Attribute。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        if isinstance(information, str):
            serialized_value = self._legacy_string_prefix + information
        else:
            serialized_value = self._legacy_repr_prefix + repr(
                information
            )

        return self.set_value(
            attr=attr,
            value=serialized_value,
            attr_type="string",
            lock=lock,
            keyable=not hide,
            channel_box=not hide
        )

    def get_string_info(self, attr=None):
        u"""
        旧结构化 String API；新代码应使用普通 Value 或 Config 语义。

        Args:
            attr (str):
                Maya Attribute 名称。

        Returns:
            None | object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        string_information = self.get_value(
            attr
        )
        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if string_information is None or string_information == "":
            return None
        if not isinstance(string_information, str):
            return string_information

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if string_information.startswith(self._legacy_string_prefix):
            return string_information[len(self._legacy_string_prefix):]

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if string_information.startswith(self._legacy_repr_prefix):
            serialized_value = string_information[len(self._legacy_repr_prefix):]
            try:
                return literal_eval(
                    serialized_value
                )
            except (ValueError, SyntaxError, TypeError):
                return serialized_value

        # -------------------------------------------------------------------------
        # Step 05：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            return literal_eval(
                string_information
            )
        except (ValueError, SyntaxError, TypeError):
            return string_information


__all__ = [
    "Attr",
]
