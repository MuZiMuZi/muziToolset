# coding=utf-8
u"""
nameUtils：Maya Rig 命名工具。

标准命名规则：
    [类型]_[方向]_[部位]_[功能]_[序号]

例如：
    grp_md_face_master_001
    ctrl_lf_eye_main_001
    jnt_rt_brow_bind_003
    model_md_head_tweak_001

兼容旧版 Name 调用方式：
    Name(type="ctrl", side="lf", resolution="eye", description="main", index=1)

也支持新的语义写法：
    Name.create_name(
        node_type="ctrl",
        side="lf",
        part="eye",
        function="main",
        index=1
    )
"""
from __future__ import print_function

import re
from importlib import reload

import maya.cmds as cmds

from legacy_reference.bake import pipelineUtils


reload(pipelineUtils)


class Name(object):
    u"""Rig 节点命名类。"""

    # ------------------------------------------------------------
    # 常用节点前缀
    # ------------------------------------------------------------

    node_types = [
        "grp",
        "zero",
        "offset",
        "connect",
        "space",
        "driven",
        "ctrl",
        "jnt",
        "loc",
        "set",
        "model",
        "network",
        "crv",
        "mesh",
        "ik",
        "eff",
        "cluster",
        "follicle",
        "rivet",
        "bs",
        "skin",
        "cns",
        "mult",
        "pma",
        "remap",
        "clamp",
        "condition"
    ]

    # ------------------------------------------------------------
    # 标准方向
    # ------------------------------------------------------------

    sides = [
        "lf",
        "rt",
        "md"
    ]

    # ------------------------------------------------------------
    # 方向别名
    # ------------------------------------------------------------

    side_aliases = {
        "l": "lf",
        "left": "lf",
        "lf": "lf",

        "r": "rt",
        "right": "rt",
        "rt": "rt",

        "m": "md",
        "c": "md",
        "mid": "md",
        "middle": "md",
        "center": "md",
        "centre": "md",
        "md": "md"
    }

    def __init__(
        self,
        name=None,
        type=None,
        side=None,
        resolution=None,
        description=None,
        index=None,
        part=None,
        function=None
    ):
        u"""
        初始化当前对象，并准备运行时需要的状态和成员。

        Args:
            name (str):
                已经存在的标准名称。如果给定，会自动拆分。
            type (str):
                旧接口，节点类型。
            side (str):
                方向。
            resolution (str):
                旧接口，对应新的 part。
            description (str):
                旧接口，对应新的 function。
            index (int):
                序号。
            part (str):
                新接口，部位。
            function (str):
                新接口，功能。
        """

        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.nodes = []

        self._type = type
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self._side = side
        self._resolution = resolution
        self._description = description
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self._index = index
        self._name = name

        # 新接口优先覆盖旧接口。
        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if part is not None:
            self._resolution = part

        if function is not None:
            self._description = function

        # -------------------------------------------------------------------------
        # Step 05：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if self._name:
            self.decompose()

    # ============================================================
    # Property
    # ============================================================

    @property
    def type(self):
        u"""
        执行当前 API 的主要处理流程。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        return self._type

    @type.setter
    def type(self, value):
        u"""
        执行当前 API 的主要处理流程。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._type = value

    @property
    def side(self):
        u"""
        执行当前 API 的主要处理流程。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        return self._side

    @side.setter
    def side(self, value):
        u"""
        执行当前 API 的主要处理流程。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._side = value

    @property
    def resolution(self):
        u"""
        执行当前 API 的主要处理流程。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        return self._resolution

    @resolution.setter
    def resolution(self, value):
        u"""
        执行当前 API 的主要处理流程。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._resolution = value

    @property
    def description(self):
        u"""
        执行当前 API 的主要处理流程。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        return self._description

    @description.setter
    def description(self, value):
        u"""
        执行当前 API 的主要处理流程。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._description = value

    @property
    def part(self):
        u"""
        部位。兼容旧版 resolution。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self._resolution

    @part.setter
    def part(self, value):
        u"""
        执行当前 API 的主要处理流程。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._resolution = value

    @property
    def function(self):
        u"""
        功能。兼容旧版 description。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self._description

    @function.setter
    def function(self, value):
        u"""
        执行当前 API 的主要处理流程。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._description = value

    @property
    def index(self):
        u"""
        执行当前 API 的主要处理流程。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        return self._index

    @index.setter
    def index(self, value):
        u"""
        执行当前 API 的主要处理流程。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._index = value

    @property
    def name(self):
        u"""
        执行当前 API 的主要处理流程。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        self.compose()
        return self._name

    # ============================================================
    # 名称基础处理
    # ============================================================

    @staticmethod
    def _normalize_name_part(value):
        u"""统一单个名称字段的格式。"""

        if value is None:
            return None

        value = str(value).strip()

        if value == "":
            return None

        value = value.replace(" ", "_")
        value = value.replace("-", "_")

        while "__" in value:
            value = value.replace("__", "_")

        value = value.strip("_")
        value = value.lower()

        return value

    @classmethod
    def normalize_side(cls, side):
        u"""
        将方向统一成 lf / rt / md。

        示例：
            l       -> lf
            left    -> lf
            r       -> rt
            center  -> md
            m       -> md

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。

        Returns:
            str | object:
            当前 API 查询或处理后得到的字符串结果。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """

        if side is None:
            return "md"

        side = cls._normalize_name_part(side)

        if side in cls.side_aliases:
            return cls.side_aliases[side]

        raise ValueError(
            u"不支持的方向名称: {0}".format(side)
        )

    @classmethod
    def create_name(
        cls,
        node_type,
        side,
        part,
        function,
        index=1
    ):
        u"""
        根据标准规则创建名称。

        标准：
            [类型]_[方向]_[部位]_[功能]_[序号]

        Args:
            node_type (str):
                需要创建、查询或过滤的 Maya Node Type。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            function (str | callable):
                当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。
            index (int):
                目标元素或节点的序号。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """

        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        node_type = cls._normalize_name_part(node_type)
        side = cls.normalize_side(side)
        # -------------------------------------------------------------------------
        # Step 02：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        part = cls._normalize_name_part(part)
        function = cls._normalize_name_part(function)

        if node_type is None:
            raise ValueError(u"node_type 不能为空。")

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if part is None:
            raise ValueError(u"part 不能为空。")

        if function is None:
            raise ValueError(u"function 不能为空。")

        if index is None:
            index = 1

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        index = int(index)

        name = "{0}_{1}_{2}_{3}_{4:03d}".format(
            node_type,
            side,
            part,
            function,
            index
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return name

    @classmethod
    def get_next_index(
        cls,
        node_type,
        side,
        part,
        function
    ):
        u"""
        获取场景中同类名称的下一个可用序号。

        Args:
            node_type (str):
                需要创建、查询或过滤的 Maya Node Type。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            function (str | callable):
                当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """

        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        node_type = cls._normalize_name_part(node_type)
        side = cls.normalize_side(side)
        # -------------------------------------------------------------------------
        # Step 02：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        part = cls._normalize_name_part(part)
        function = cls._normalize_name_part(function)

        base_name = "{0}_{1}_{2}_{3}".format(
            node_type,
            side,
            part,
            function
        )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        search_name = base_name + "_*"

        nodes = cmds.ls(search_name)

        if nodes is None:
            nodes = []

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        max_index = 0

        for node in nodes:

            short_name = node.split("|")[-1]
            short_name = short_name.split(":")[-1]

            name_parts = short_name.split("_")

            if len(name_parts) == 0:
                continue

            index_string = name_parts[-1]

            if not index_string.isdigit():
                continue

            current_index = int(index_string)

            if current_index > max_index:
                max_index = current_index

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return max_index + 1

    @classmethod
    def create_unique_name(
        cls,
        node_type,
        side,
        part,
        function
    ):
        u"""
        创建场景中下一个可用的标准名称。

        Args:
            node_type (str):
                需要创建、查询或过滤的 Maya Node Type。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            function (str | callable):
                当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
        """

        index = cls.get_next_index(
            node_type=node_type,
            side=side,
            part=part,
            function=function
        )

        name = cls.create_name(
            node_type=node_type,
            side=side,
            part=part,
            function=function,
            index=index
        )

        return name

    @classmethod
    def parse_name(cls, name):
        u"""
        将标准名称拆分并返回字典。

        Args:
            name (str):
                创建或查询时使用的节点名称。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        name_object = cls(name=name)

        name_info = {
            "type": name_object.type,
            "side": name_object.side,
            "part": name_object.part,
            "function": name_object.function,
            "index": name_object.index
        }

        return name_info

    @classmethod
    def mirror_name(cls, name):
        u"""
        返回名称的左右镜像名称，不修改 Maya 节点。

        Args:
            name (str):
                创建或查询时使用的节点名称。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        name_object = cls(name=name)
        name_object.flip()

        return name_object.name

    # ============================================================
    # 兼容旧版 compose / decompose
    # ============================================================

    def compose(self):
        u"""
        根据当前成员变量组合名称。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        node_type = self._normalize_name_part(self._type)
        side = self.normalize_side(self._side)
        part = self._normalize_name_part(self._resolution)
        function = self._normalize_name_part(self._description)

        if self._index is None:
            self._index = 1

        self._name = self.create_name(
            node_type=node_type,
            side=side,
            part=part,
            function=function,
            index=self._index
        )

        return self._name

    def decompose(self):
        u"""
        拆分标准名称。

        支持功能字段包含下划线，例如：
            grp_md_face_rig_nodes_001

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """

        if not self._name:
            return False

        short_name = self._name.split("|")[-1]
        short_name = short_name.split(":")[-1]

        name_parts = short_name.split("_")

        # 最少需要：type_side_part_function_index
        if len(name_parts) < 5:
            return False

        index_string = name_parts[-1]

        if not index_string.isdigit():
            return False

        self._type = name_parts[0]
        self._side = name_parts[1]
        self._resolution = name_parts[2]

        function_parts = name_parts[3:-1]
        self._description = "_".join(function_parts)

        self._index = int(index_string)

        return True

    def flip(self):
        u"""
        翻转名称方向：lf <-> rt，同时兼容旧版 l <-> r。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        if self._side == "lf":
            self._side = "rt"

        elif self._side == "rt":
            self._side = "lf"

        elif self._side == "l":
            self._side = "r"

        elif self._side == "r":
            self._side = "l"

        return self._side

    # ============================================================
    # Maya 重命名工具
    # ============================================================

    def set_rename(self, new_name):
        u"""
        将当前选择的节点重命名。

        Args:
            new_name (str):
                `new_name` 对应的 Maya 节点或资源名称。
        """

        names = cmds.ls(sl=True)

        if names is None:
            names = []

        for selected_name in names:
            object_name = selected_name.split("|")[-1]
            self._name = cmds.rename(object_name, new_name)

    @pipelineUtils.Pipeline.make_undo
    def add_prefix(self, prefix):
        u"""
        给当前节点添加前缀。

        Args:
            prefix (str):
                添加到 Maya 节点名称前部的 Prefix。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        self._name = cmds.rename(
            self._name,
            prefix + self._name
        )

        return self._name

    @pipelineUtils.Pipeline.make_undo
    def add_suffix(self, suffix):
        u"""
        给当前节点添加后缀。

        Args:
            suffix (str):
                添加到 Maya 节点名称尾部的 Suffix。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        self._name = cmds.rename(
            self._name,
            self._name + suffix
        )

        return self._name

    def _selection_list_nodes(self):
        u"""返回当前选择及其所有子层级节点。"""

        self.nodes = []

        selected = cmds.ls(sl=True, long=True)

        if selected is None:
            selected = []

        for select in selected:
            self.nodes.append(select)

            children = cmds.listRelatives(
                select,
                allDescendents=True,
                fullPath=True
            )

            if children is None:
                children = []

            for child in children:
                self.nodes.append(child)

        return self.nodes

    @pipelineUtils.Pipeline.make_undo
    def add_hierarchy_prefix(self, prefix):
        u"""
        给当前选择层级添加前缀。

        Args:
            prefix (str):
                添加到 Maya 节点名称前部的 Prefix。
        """

        self.nodes = self._selection_list_nodes()

        # 子层级优先改名，可以减少长路径失效的问题。
        self.nodes.sort(
            key=lambda node: node.count("|"),
            reverse=True
        )

        for node in self.nodes:
            object_name = node.split("|")[-1]
            new_object_name = prefix + object_name
            cmds.rename(node, new_object_name)

    @pipelineUtils.Pipeline.make_undo
    def add_hierarchy_suffix(self, suffix):
        u"""
        给当前选择层级添加后缀。

        Args:
            suffix (str):
                添加到 Maya 节点名称尾部的 Suffix。
        """

        self.nodes = self._selection_list_nodes()

        self.nodes.sort(
            key=lambda node: node.count("|"),
            reverse=True
        )

        for node in self.nodes:
            object_name = node.split("|")[-1]
            new_object_name = object_name + suffix
            cmds.rename(node, new_object_name)

    @pipelineUtils.Pipeline.make_undo
    def search_replace_name(self, search, replace):
        u"""
        根据关键字搜索替换当前节点名称。

        Args:
            search (str):
                节点名称中需要查找并替换的字符串。
            replace (bool):
                替换 Search 内容的新字符串。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        object_name = self._name.split("|")[-1]
        new_name = object_name.replace(search, replace)

        self._name = cmds.rename(
            self._name,
            new_name
        )

        return self._name

    def rename_to_name(self, new_name):
        u"""
        重命名为指定名称。

        Args:
            new_name (str):
                `new_name` 对应的 Maya 节点或资源名称。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        self._name = cmds.rename(
            self._name,
            new_name
        )

        return self._name

    def regex_search_replace_name(self, search, replace):
        u"""
        根据正则表达式搜索替换名称。

        Args:
            search (str):
                节点名称中需要查找并替换的字符串。
            replace (bool):
                替换 Search 内容的新字符串。
        """

        regex_object = re.compile(search)

        nodes = self._selection_list_nodes()

        nodes.sort(
            key=lambda node: node.count("|"),
            reverse=True
        )

        for node in nodes:
            object_name = node.split("|")[-1]
            new_name = regex_object.sub(
                replace,
                object_name
            )

            cmds.rename(
                node,
                new_name
            )

    @staticmethod
    def print_duplicate_object():
        u"""
        检查并列出场景中所有重名节点。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """

        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        all_objects = cmds.ls(long=True)

        if all_objects is None:
            all_objects = []

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        duplicate_object_list = []
        short_name_dict = {}

        # -------------------------------------------------------------------------
        # Step 03：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for object_name in all_objects:
            short_name = object_name.split("|")[-1]

            if short_name not in short_name_dict:
                short_name_dict[short_name] = []

            short_name_dict[short_name].append(object_name)

        for short_name in short_name_dict:
            object_list = short_name_dict[short_name]

            if len(object_list) <= 1:
                continue

            for object_name in object_list:
                duplicate_object_list.append(object_name)
                cmds.warning(
                    u"场景里有重名的物体: {0}".format(
                        object_name
                    )
                )

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if len(duplicate_object_list) == 0:
            cmds.warning(u"场景里没有重名的物体")

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return duplicate_object_list

    @staticmethod
    def rename_duplicate_object():
        u"""
        检查并重新命名场景内所有重名节点。
        """

        duplicate_object_list = Name.print_duplicate_object()

        # 深层节点先处理，避免 DAG 路径在父级改名后失效。
        duplicate_object_list.sort(
            key=lambda node: node.count("|"),
            reverse=True
        )

        rename_count_dict = {}

        for duplicate_object in duplicate_object_list:

            object_name = duplicate_object.split("|")[-1]

            if object_name not in rename_count_dict:
                rename_count_dict[object_name] = 0

            rename_count_dict[object_name] += 1

            count = rename_count_dict[object_name]

            new_object_name = "{0}_{1:03d}".format(
                object_name,
                count
            )

            cmds.rename(
                duplicate_object,
                new_object_name
            )
