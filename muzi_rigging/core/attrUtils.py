# coding=utf-8
u"""
attrUtils
=========

Maya 属性操作工具。

主要功能：
    1. 检查对象和属性是否存在
    2. 锁定 / 解锁属性
    3. 隐藏 / 显示属性
    4. 批量处理属性
    5. 添加自定义属性
    6. 连接 / 断开属性
    7. 获取属性输入 / 输出连接
    8. 保存 / 读取字符串信息
    9. 设置 / 获取 Transform 属性限制

兼容：Maya 2023+ / maya.cmds
"""

from ast import literal_eval
from collections import OrderedDict

import maya.cmds as cmds


class Attr(object):
    """Maya 属性操作类。"""

    # Transform 可以设置 transformLimits 的标准属性。
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

    # transformLimits 使用的值查询 flag 和开关查询 flag。
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

    # transformLimits 的短属性名兼容。
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
        """
        Args:
            object (str): Maya 节点名称。
            attr (str or None): 默认需要操作的属性名称。
        """
        # 为了兼容你原来项目中的 self.object，这里继续保留这个变量名。
        self.object = object
        self.attr = attr

        # 保留原类中的变量，避免外部代码如果已经使用它们时出现兼容问题。
        self.minValue = None
        self.maxValue = None
        self.info = None

    # -------------------------------------------------------------------------
    # 基础检查
    # -------------------------------------------------------------------------

    def object_exists(self):
        """检查当前 Maya 节点是否存在。"""
        return cmds.objExists(self.object)

    def _get_plug(self, attr=None):
        """把属性名称统一转换成完整 plug，例如 ctrl.translateX。"""
        if attr is None:
            attr = self.attr

        if not attr:
            raise ValueError(u"没有指定需要操作的属性。")

        # 如果已经是 node.attr 形式，就直接使用。
        if "." in attr:
            return attr

        return "{}.{}".format(self.object, attr)

    def attr_exists(self, attr=None):
        """检查属性是否存在。"""
        try:
            plug = self._get_plug(attr)
        except ValueError:
            return False

        return cmds.objExists(plug)

    # -------------------------------------------------------------------------
    # 属性锁定 / 隐藏
    # -------------------------------------------------------------------------

    def lock_and_hide_attr(self, attr, lock=True, hide=True):
        u"""锁定或解锁、隐藏或显示单个属性。

        Args:
            attr (str): 属性名称，可以是 translateX，也可以是 node.translateX。
            lock (bool): True 锁定，False 解锁。
            hide (bool): True 从 Channel Box 隐藏，False 显示并允许 Key。

        Returns:
            bool: 操作是否成功。
        """
        plug = self._get_plug(attr)

        if not cmds.objExists(plug):
            cmds.warning(u"【Attr】属性不存在: {}".format(plug))
            return False

        # 锁定状态可以直接一次设置，不需要拆成四个 if。
        cmds.setAttr(plug, lock=lock)

        if hide:
            cmds.setAttr(
                plug,
                keyable=False,
                channelBox=False,
            )
        else:
            cmds.setAttr(
                plug,
                keyable=True,
                channelBox=True,
            )

        return True

    def lock_and_hide_attrs(self, attrs_list, lock=True, hide=True):
        u"""批量锁定 / 解锁、隐藏 / 显示属性。"""
        result = []

        if not attrs_list:
            return result

        for attr in attrs_list:
            state = self.lock_and_hide_attr(
                attr,
                lock=lock,
                hide=hide,
            )
            result.append(state)

        return result

    # -------------------------------------------------------------------------
    # 添加属性
    # -------------------------------------------------------------------------

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
        u"""添加自定义属性。

        Args:
            attr (str): 属性名称。
            attr_type (str): 属性类型，例如 string / double / long / bool / enum / message。
            lock (bool): 创建后是否锁定。
            hide (bool): 创建后是否隐藏。
            default_value: 默认值。
            min_value: 最小值。
            max_value: 最大值。
            enum_name (str): enum 字符串，例如 "A:B:C"。
            multi (bool): 是否创建 multi 属性。

        Notes:
            为了兼容旧代码，也支持：
                add_attr("test", type="double")
        """
        # 兼容原来的 type= 参数写法。
        legacy_type = kwargs.pop("type", None)
        if legacy_type is not None:
            attr_type = legacy_type

        if not self.object_exists():
            cmds.warning(u"【Attr】对象不存在: {}".format(self.object))
            return None

        plug = self._get_plug(attr)

        # 已存在时不重复创建，只更新锁定 / 显示状态。
        if cmds.objExists(plug):
            self.lock_and_hide_attr(
                attr,
                lock=lock,
                hide=hide,
            )
            return plug

        add_kwargs = {
            "longName": attr,
            "multi": multi,
        }

        # string 必须使用 dataType，而不是 attributeType。
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

        # 允许调用者继续传入 Maya addAttr 支持的额外参数。
        for key in kwargs:
            add_kwargs[key] = kwargs[key]

        cmds.addAttr(
            self.object,
            **add_kwargs
        )

        # string 的默认值不能放在 addAttr(defaultValue=...) 中，需要单独 setAttr。
        if attr_type == "string" and default_value is not None:
            cmds.setAttr(
                plug,
                str(default_value),
                type="string",
            )

        self.lock_and_hide_attr(
            attr,
            lock=lock,
            hide=hide,
        )

        return plug

    # -------------------------------------------------------------------------
    # 属性连接
    # -------------------------------------------------------------------------

    def connect_attr(self, output_attr, input_attr, force=True):
        u"""连接两个属性。

        Args:
            output_attr (str): 输出属性。
            input_attr (str): 输入属性。
            force (bool): 输入属性已经存在其他连接时是否强制替换。

        Returns:
            bool: 是否完成连接。
        """
        output_plug = self._get_plug(output_attr)
        input_plug = self._get_plug(input_attr)

        if not cmds.objExists(output_plug):
            cmds.warning(u"【Attr】输出属性不存在: {}".format(output_plug))
            return False

        if not cmds.objExists(input_plug):
            cmds.warning(u"【Attr】输入属性不存在: {}".format(input_plug))
            return False

        input_connections = cmds.listConnections(
            input_plug,
            source=True,
            destination=False,
            plugs=True,
        )

        if input_connections:
            # 如果已经是目标连接，不重复执行 connectAttr。
            for connection in input_connections:
                if connection == output_plug:
                    return True

            if not force:
                cmds.warning(
                    u"【Attr】输入属性已经存在连接: {}".format(input_plug)
                )
                return False

        cmds.connectAttr(
            output_plug,
            input_plug,
            force=force,
        )

        return True

    def disconnect_attr(self, output_attr, input_attr):
        u"""断开两个指定属性之间的连接。"""
        output_plug = self._get_plug(output_attr)
        input_plug = self._get_plug(input_attr)

        if not cmds.objExists(output_plug):
            return False

        if not cmds.objExists(input_plug):
            return False

        if not cmds.isConnected(output_plug, input_plug):
            return False

        cmds.disconnectAttr(
            output_plug,
            input_plug,
        )

        return True

    def get_attr_input(self, attr=None, plugs=True):
        u"""获取属性的输入连接。

        Args:
            attr (str or None): 属性名称。None 时使用 self.attr。
            plugs (bool):
                True  -> 返回完整属性，例如 multiplyDivide1.outputX
                False -> 只返回节点，例如 multiplyDivide1

        Returns:
            list: 输入连接列表，没有连接时返回 []。
        """
        plug = self._get_plug(attr)

        if not cmds.objExists(plug):
            return []

        input_connections = cmds.listConnections(
            plug,
            source=True,
            destination=False,
            plugs=plugs,
        )

        if input_connections is None:
            return []

        return input_connections

    def get_attr_output(self, attr=None, plugs=True):
        u"""获取属性的输出连接。

        Args:
            attr (str or None): 属性名称。None 时使用 self.attr。
            plugs (bool):
                True  -> 返回完整属性，例如 joint1.rotateX
                False -> 只返回节点，例如 joint1

        Returns:
            list: 输出连接列表，没有连接时返回 []。
        """
        plug = self._get_plug(attr)

        if not cmds.objExists(plug):
            return []

        output_connections = cmds.listConnections(
            plug,
            source=False,
            destination=True,
            plugs=plugs,
        )

        if output_connections is None:
            return []

        return output_connections

    # -------------------------------------------------------------------------
    # 通用属性值 / Message 配置
    # -------------------------------------------------------------------------

    @staticmethod
    def _infer_attr_type(value):
        u"""根据 Python 值推断 Maya 属性类型。"""
        if isinstance(value, bool):
            return "bool"

        if isinstance(value, int):
            return "long"

        if isinstance(value, float):
            return "double"

        if isinstance(value, str):
            return "string"

        raise TypeError(
            u"【Attr】无法根据数值自动判断 Maya 属性类型: {0}".format(
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
        u"""创建属性并设置属性值。

        如果属性不存在则自动创建；如果已经存在则直接设置。

        Args:
            attr (str): 属性名称。
            value: 需要写入的值。
            attr_type (str or None): Maya 属性类型。None 时根据 value 自动判断。
            lock (bool): 设置完成后是否锁定。
            hide (bool): 设置完成后是否隐藏。
            min_value: 最小值。
            max_value: 最大值。
            enum_name (str or None): enum 选项字符串。

        Returns:
            str or None: 完整属性 plug。
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

        if not cmds.objExists(plug):
            self.add_attr(
                attr,
                attr_type=attr_type,
                lock=False,
                hide=hide,
                min_value=min_value,
                max_value=max_value,
                enum_name=enum_name,
            )
        else:
            cmds.setAttr(
                plug,
                lock=False,
            )

        if attr_type == "string":
            cmds.setAttr(
                plug,
                str(value),
                type="string",
            )
        else:
            cmds.setAttr(
                plug,
                value,
            )

        self.lock_and_hide_attr(
            attr,
            lock=lock,
            hide=hide,
        )

        return plug

    def get_attr_value(self, attr=None):
        u"""读取普通 Maya 属性值。"""
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
        u"""批量创建并设置普通属性。

        Example:
            attrs_dict = {
                "mouth_jnt_number": 12,
                "step_value": 1,
            }

            attr_types = {
                "mouth_jnt_number": "long",
                "step_value": "long",
            }
        """
        result = {}

        if not attrs_dict:
            return result

        if attr_types is None:
            attr_types = {}

        for attr in attrs_dict:
            value = attrs_dict.get(attr)
            attr_type = attr_types.get(attr)

            plug = self.set_attr_value(
                attr=attr,
                value=value,
                attr_type=attr_type,
                lock=lock,
                hide=hide,
            )

            result[attr] = plug

        return result

    def add_message_attr(self, attr, multi=False):
        u"""创建 message 属性。"""
        plug = self._get_plug(attr)

        if cmds.objExists(plug):
            return plug

        plug = self.add_attr(
            attr,
            attr_type="message",
            lock=False,
            hide=True,
            multi=multi,
        )

        return plug

    def disconnect_attr_inputs(self, attr=None):
        u"""断开指定属性的所有输入连接。

        Args:
            attr (str or None):
                属性名称。
                可以是 "face_head_model"，
                也可以是 "network1.face_head_model"。

        Returns:
            bool:
                True  -> 已经完成处理。
                False -> 属性不存在。
        """

        input_plug = self._get_plug(attr)

        if not cmds.objExists(input_plug):
            return False

        input_connections = cmds.listConnections(
            input_plug,
            source=True,
            destination=False,
            plugs=True
        )

        if not input_connections:
            return True

        for output_plug in input_connections:

            if not cmds.isConnected(
                output_plug,
                input_plug
            ):
                continue

            cmds.disconnectAttr(
                output_plug,
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
        u"""把 Maya 节点的 message 连接到当前节点的 message 属性。

        Args:
            source_node (str or None):
                需要保存的 Maya 节点。

            attr (str or None):
                当前节点上的 message 属性名称。

            force (bool):
                当前属性已经存在旧连接时，是否替换旧连接。

            clear_empty (bool):
                当 source_node 为 None 或空字符串时，
                是否断开该 message 属性之前保存的旧连接。

        Example:
            config_attr = Attr(
                "network_md_face_config_001"
            )

            config_attr.connect_message(
                source_node="model_md_head_base_001",
                attr="face_head_model",
                force=True,
                clear_empty=True
            )
        """

        input_plug = self._get_plug(attr)

        attr_name = input_plug.split(
            ".",
            1
        )[1]

        # ------------------------------------------------------------
        # 空值
        # ------------------------------------------------------------

        if source_node is None or source_node == "":

            if not clear_empty:
                return False

            # 即使当前没有模型，也保留 Config 的 message 属性。
            if not cmds.objExists(input_plug):

                self.add_message_attr(
                    attr_name
                )

            # 用户把 UI 中的模型清空时，
            # 同时清除 Config Node 中之前保存的旧连接。
            self.disconnect_attr_inputs(
                input_plug
            )

            return True

        # ------------------------------------------------------------
        # 检查来源节点
        # ------------------------------------------------------------

        if not cmds.objExists(source_node):

            cmds.warning(
                u"【Attr】Message 来源节点不存在: {0}".format(
                    source_node
                )
            )

            return False

        # ------------------------------------------------------------
        # 创建 Config Message 属性
        # ------------------------------------------------------------

        if not cmds.objExists(input_plug):

            self.add_message_attr(
                attr_name
            )

        source_plug = "{}.message".format(
            source_node
        )

        # ------------------------------------------------------------
        # 建立 / 更新连接
        # ------------------------------------------------------------

        state = self.connect_attr(
            source_plug,
            input_plug,
            force=force
        )

        return state

    def connect_messages(
        self,
        attrs_dict,
        force=True,
        clear_empty=False
    ):
        u"""批量保存 Maya 节点的 message 连接。

        Args:
            attrs_dict (dict):
                key:
                    Config Node 上的 message 属性名称。

                value:
                    需要保存的 Maya 节点名称。

            force (bool):
                是否替换已有输入连接。

            clear_empty (bool):
                value 为 None 或空字符串时，
                是否清除该属性之前保存的旧 message 连接。

        Example:
            model_config_dict = {
                "face_head_model": "head_geo",
                "face_lf_eye_model": "lf_eye_geo",
                "face_tongue_model": None
            }

            config_attr.connect_messages(
                model_config_dict,
                force=True,
                clear_empty=True
            )
        """

        result = {}

        if not attrs_dict:
            return result

        for attr in attrs_dict:

            source_node = attrs_dict.get(
                attr
            )

            state = self.connect_message(
                source_node=source_node,
                attr=attr,
                force=force,
                clear_empty=clear_empty
            )

            result[attr] = state

        return result

    def get_message(self, attr=None, plugs=False):
        u"""读取当前 message 属性连接的来源节点。

        Args:
            attr (str or None):
                message 属性名称。

            plugs (bool):
                False -> 返回节点名称。
                True  -> 返回完整 plug。

        Returns:
            str or None:
                没有连接时返回 None。
        """

        connections = self.get_attr_input(
            attr=attr,
            plugs=plugs
        )

        if not connections:
            return None

        return connections[0]

    # -------------------------------------------------------------------------
    # 字符串信息属性
    # -------------------------------------------------------------------------

    def add_string_info(self, information, attr=None, lock=True, hide=True):
        u"""把 Python 信息保存到 Maya string 属性中。

        支持：
            str / int / float / bool / list / tuple / dict / None

        对 list / tuple / dict 等对象使用 repr() 保存，读取时再通过 literal_eval() 恢复。
        """
        plug = self._get_plug(attr)
        attr_name = plug.split(".", 1)[1]

        if not cmds.objExists(plug):
            self.add_attr(
                attr_name,
                attr_type="string",
                lock=False,
                hide=hide,
            )

        # 写入前必须先解锁。
        cmds.setAttr(
            plug,
            lock=False,
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
            type="string",
        )

        # 信息属性通常不需要动画 Key，因此这里直接使用 hide 控制 Channel Box 显示。
        if hide:
            cmds.setAttr(
                plug,
                keyable=False,
                channelBox=False,
            )
        else:
            cmds.setAttr(
                plug,
                keyable=False,
                channelBox=True,
            )

        cmds.setAttr(
            plug,
            lock=lock,
        )

        return plug

    def get_string_info(self, attr=None):
        u"""读取 Maya string 属性，并尝试恢复成原来的 Python 数据。"""
        plug = self._get_plug(attr)

        if not cmds.objExists(plug):
            return None

        string_info_message = cmds.getAttr(plug)

        if string_info_message is None:
            return None

        if string_info_message == "":
            return None

        # dict/list/tuple/int/float/bool 等 repr 字符串可以恢复。
        try:
            info = literal_eval(string_info_message)
            return info
        except (ValueError, SyntaxError, TypeError):
            # 普通字符串例如 "hello" 不是合法 Python literal 时，直接返回原字符串。
            return string_info_message

    # -------------------------------------------------------------------------
    # Transform Limits
    # -------------------------------------------------------------------------

    def _get_limit_attr_name(self, attr):
        """把 tx / ry 这样的短名称统一转换成长名称。"""
        if attr in self.limit_attr_aliases:
            return self.limit_attr_aliases[attr]

        return attr

    def set_attrs_limits(self, attrs_dict):
        u"""批量设置 Transform 属性最大值 / 最小值限制。

        格式：
            {
                "translateY": [(True, True), (-10.0, 10.0)],
                "rotateX": [(True, False), (-45.0, 0.0)],
            }

        每个 value：
            (
                (是否启用最小限制, 是否启用最大限制),
                (最小值, 最大值)
            )
        """
        if not self.object_exists():
            cmds.warning(u"【Attr】对象不存在: {}".format(self.object))
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

            transform_limit_kwargs = {
                enable_flag: (
                    bool(limit_state[0]),
                    bool(limit_state[1]),
                ),
                value_flag: (
                    limits[0],
                    limits[1],
                ),
            }

            cmds.transformLimits(
                self.object,
                **transform_limit_kwargs
            )

        return True

    def get_attrs_limits(self, attrs_list=None):
        u"""获取 Transform 属性最大值 / 最小值限制。

        Args:
            attrs_list (list or None):
                None 时获取全部 translate / rotate / scale 轴向限制。

        Returns:
            OrderedDict:
                {
                    "translateX": ((False, False), (-1.0, 1.0)),
                    ...
                }
        """
        attrs_limits_dict = OrderedDict()

        if not self.object_exists():
            return attrs_limits_dict

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

            limit_num = cmds.transformLimits(
                self.object,
                query=True,
                **{value_flag: True}
            )

            # 统一转换成 tuple，后续保存配置时更稳定。
            limit_state_tuple = (
                bool(limit_state[0]),
                bool(limit_state[1]),
            )

            limit_num_tuple = (
                limit_num[0],
                limit_num[1],
            )

            attrs_limits_dict[attr_name] = (
                limit_state_tuple,
                limit_num_tuple,
            )

        return attrs_limits_dict

    # -------------------------------------------------------------------------
    # 属性筛选
    # -------------------------------------------------------------------------

    def get_unwanted_attrs(self, attrs_list):
        u"""根据需要保留的 Transform 属性，返回剩余属性列表。

        Example:
            输入：
                ["translateX", "rotateY"]

            返回：
                除 translateX / rotateY 之外的其它 Transform 通道。
        """
        attrs_to_lock_list = []

        for attr in self.transform_attrs:
            attrs_to_lock_list.append(attr)

        if not attrs_list:
            return attrs_to_lock_list

        for attr in attrs_list:
            attr_name = self._get_limit_attr_name(attr)

            if attr_name in attrs_to_lock_list:
                attrs_to_lock_list.remove(attr_name)

        return attrs_to_lock_list


    # 从Maya的主通道框中检索选定属性的长名称，可以选择通道盒上的属性，也可以选择历史记录上的属性，也可以选择形状历史上的属性
    @staticmethod
    def get_channelBox_attrs () :
        """从Maya的主通道框中检索选定属性的长名称，可以选择通道盒上的属性，也可以选择历史记录上的属性，也可以选择形状历史上的属性
        selAttrs = mel.eval('selectedChannelBoxAttributes')
        return：
        attr_names(list/str): 长属性名称列表，例如[“translateX”，“rotateX”]

        """
        # transfrom节点的属性获取
        # 获取当前主通道框中选择的主要对象（transfrom节点）
        main_objs = cmds.channelBox ("mainChannelBox" , query = True , mainObjectList = True)
        # 获取当前主通道框中选择的主要对象（transfrom节点）选定的属性
        main_attrs = cmds.channelBox ("mainChannelBox" , query = True , selectedMainAttributes = True)

        # history历史通道的节点的属性获取
        # 获取当前在主通道框中选择的历史记录（输入历史记录）对象。
        hist_objs = cmds.channelBox ("mainChannelBox" , query = True , historyObjectList = True)
        # 获取当前在主通道框中选择的历史记录（输入历史记录）对象的选定属性
        hist_attrs = cmds.channelBox ("mainChannelBox" , query = True , selectedHistoryAttributes = True)

        # shape历史通道的节点的属性获取
        # 获取当前在主通道框中选择的形状对象（几何体节点）
        shape_objs = cmds.channelBox ("mainChannelBox" , query = True , shapeObjectList = True)
        # 获取当前在主通道框中选择的形状对象（几何体节点）的选定属性。
        shape_attrs = cmds.channelBox ("mainChannelBox" , query = True , selectedShapeAttributes = True)
        # 现在组合并获得长名称
        attr_names = []
        for pair in ((main_objs , main_attrs) , (hist_objs , hist_attrs) , (shape_objs , shape_attrs)) :
            objs , attrs = pair
            if attrs is not None :
                for nodeName in objs :
                    # 获取长名称，而不是短名称
                    resultList = list ()
                    for attr in attrs :
                        try :
                            longName = cmds.attributeQuery (attr , node = nodeName , longName = True)
                            resultList.append (longName)
                        # 属性可能不存在多个选定对象。
                        except RuntimeError :
                            pass
                    attr_names += resultList
        # 删除重复项
        attr_names = list (set (attr_names))
        if not attr_names :
            cmds.warning ("请在通道盒中选择属性")
        return attr_names


    # 获取通道盒内所有的属性列表，查询需要位移的属性在列表的位置信息，之后进行通道盒属性位移
    @staticmethod
    def move_channelBox_attr (up = True , down = False) :
        """
        获取通道盒内所有的属性列表，查询需要位移的属性在列表的位置信息，之后进行通道盒属性位移
        up(bool):属性是否向上位移,默认为True
        down(bool):属性是否向下位移
        思路：以原本属性列表[A,B,C,D]为例。需要位移的属性为B

        上移的话：[A,B,C,D]---->[B,A,C,D]
                1.删除所选择的需要位移的属性B的上一个属性A，然后撤回，这个时候属性A会在最后一个位置,现在属性列表为[B,C,D,A]
                2.删除在之前列表中位移的属性B之后的所有属性，然后撤回,这个时候属性B会在对应的位置，现在属性列表为[B,A,C,D]


        下移的话: [A,B,C,D]---->[A,C,B,D]
                1.删除所选择的需要位移的属性B，然后撤回，这个时候属性B会在最后一个位置，现在属性列表为[A,C,D,B]
                2.删除在之前列表后位移的属性B后两位到最末尾的属性D，这个时候属性D会在最后一个位置，现在属性列表为[A,C,B,D]
        """
        obj = cmds.ls (sl = 1) [0]
        select_attr = cmds.channelBox ('mainChannelBox' , q = 1 , sma = 1) [0]
        # 先判断选择的属性是否可以被编辑,当属性不可以被编辑的时候报告错误信息并终止运行
        if cmds.getAttr (obj + '.' + select_attr , lock = True) :
            cmds.warning ('{}.{}属性不可以被编辑'.format (obj , select_attr))
            pass
        else :
            # 属性可以被编辑的情况运行下方代码，获取所有可见的属性，以及获取所选择的属性的编号
            attrList = cmds.listAttr (obj , userDefined = True)
            select_attr_index = attrList.index (select_attr)
            # 将撤销队列设置打开
            cmds.undoInfo (openChunk = True)
            ###思路：以原本属性列表[A,B,C,D]为例。需要位移的属性为B###
            # 上移的话：[A , B , C , D] - --->[B , A , C , D]
            if up :
                delete_attr_index = select_attr_index - 1
                if select_attr_index == 0 :
                    pass
                else :
                    # 1.删除所选择的需要位移的属性B的上一个属性A，然后撤回，这个时候属性A会在最后一个位置,现在属性列表为[B,C,D,A]
                    cmds.deleteAttr (obj + "." + attrList [delete_attr_index])
                    cmds.undo ()
                    # 2.删除位移的属性B之后的所有属性，然后撤回,这个时候属性B会在对应的位置，现在属性列表为[B,A,C,D]
                    for index in range ((select_attr_index + 1) , len (attrList)) :
                        cmds.deleteAttr (obj + "." + attrList [index])
                        cmds.undo ()

            # 下移的话: [A , B , C , D] - --->[A , C , B , D]
            if down :
                if select_attr_index == len (attrList) :
                    return
                else :
                    # 1.删除所选择的需要位移的属性B，然后撤回，这个时候属性B会在最后一个位置，现在属性列表为 [A , C , D , B]
                    cmds.deleteAttr (obj + "." + attrList [select_attr_index])
                    cmds.undo ()
                    # 删除在之前列表后位移的属性B后两位到最末尾的属性D，这个时候属性D会在最后一个位置，现在属性列表为[A,C,B,D]
                    for index in range ((select_attr_index + 2) , len (attrList)) :
                        cmds.deleteAttr (obj + "." + attrList [index])
                        cmds.undo ()


    # 锁住物体需要隐藏的属性
    @staticmethod
    def set_lock_attr (node , attr , lock = True) :
        """
        锁住物体需要隐藏的属性
        node(str):maya节点
        attr(str):需要隐藏的属性
        hide(bool):是否进行隐藏
        keyable(bool):是否能够k动画帧
        """
        cmds.setAttr ("{}.{}".format (node , attr) , lock = lock , keyable = True)


    # 隐藏物体需要隐藏的属性
    @staticmethod
    def set_hide_attr (node , attr , hide = True) :
        """
        隐藏物体需要隐藏的属性
        node(str):maya节点
        attr(str):需要隐藏的属性
        hide(bool):是否进行隐藏
        keyable(bool):是否能够k动画帧
        """
        if hide :
            cmds.setAttr ("{}.{}".format (node , attr) , keyable = False , channelBox = False)
        else :
            cmds.setAttr ("{}.{}".format (node , attr) , keyable = True , channelBox = True)
            cmds.setAttr ("{}.{}".format (node , attr) , keyable = True)


    # 设置属性是否可以k动画帧
    @staticmethod
    def set_key_attr (node , attr , keyable = True) :
        """
        设置属性是否可以k动画帧
        node(str):maya节点，需要锁定或隐藏属性的物体
        attr(str):需要隐藏的属性
        hide(bool):是否进行隐藏
        keyable(bool):是否能够k动画帧
        """
        cmds.setAttr ("{}.{}".format (node , attr) , keyable = keyable)


    # 锁定或隐藏需要的属性
    @staticmethod
    def lock_hide_attr (node , attr , lock = True , hide = True) :
        '''
        锁定或隐藏需要的属性
        node(str):需要锁定或隐藏属性的物体
        attr(str)：需要锁定或隐藏属性的属性
        '''
        Attr.set_lock_attr (node , attr , lock = lock)
        Attr.set_hide_attr (node , attr , hide = hide)


    # 重置所选择的物体的默认属性
    @staticmethod
    def reset_attr (node) :

        """
        重置所选择的物体的默认属性
        """
        # 重置 X、Y、Z 轴的平移和旋转属性
        for attr in ['translate' , 'rotate'] :
            for axis in ['X' , 'Y' , 'Z'] :
                try :
                    # 尝试将属性设置为 0
                    cmds.setAttr (node + '.{}{}'.format (attr , axis) , 0)
                except :
                    # 如果属性不存在，则捕获异常
                    pass

        # 重置 X、Y、Z 轴的缩放属性
        for axis in ['X' , 'Y' , 'Z'] :
            try :
                # 尝试将属性设置为 1
                cmds.setAttr (node + '.scale{}'.format (axis) , 1)
            except :
                # 如果属性不存在，则捕获异常
                pass

