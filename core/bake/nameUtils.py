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

from core.bake import pipelineUtils


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
        Args:
            name(str): 已经存在的标准名称。如果给定，会自动拆分。
            type(str): 旧接口，节点类型。
            side(str): 方向。
            resolution(str): 旧接口，对应新的 part。
            description(str): 旧接口，对应新的 function。
            index(int): 序号。
            part(str): 新接口，部位。
            function(str): 新接口，功能。
        """

        self.nodes = []

        self._type = type
        self._side = side
        self._resolution = resolution
        self._description = description
        self._index = index
        self._name = name

        # 新接口优先覆盖旧接口。
        if part is not None:
            self._resolution = part

        if function is not None:
            self._description = function

        if self._name:
            self.decompose()

    # ============================================================
    # Property
    # ============================================================

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self, value):
        self._side = value

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        self._resolution = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def part(self):
        """部位。兼容旧版 resolution。"""
        return self._resolution

    @part.setter
    def part(self, value):
        self._resolution = value

    @property
    def function(self):
        """功能。兼容旧版 description。"""
        return self._description

    @function.setter
    def function(self, value):
        self._description = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def name(self):
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
        """

        node_type = cls._normalize_name_part(node_type)
        side = cls.normalize_side(side)
        part = cls._normalize_name_part(part)
        function = cls._normalize_name_part(function)

        if node_type is None:
            raise ValueError(u"node_type 不能为空。")

        if part is None:
            raise ValueError(u"part 不能为空。")

        if function is None:
            raise ValueError(u"function 不能为空。")

        if index is None:
            index = 1

        index = int(index)

        name = "{0}_{1}_{2}_{3}_{4:03d}".format(
            node_type,
            side,
            part,
            function,
            index
        )

        return name

    @classmethod
    def get_next_index(
        cls,
        node_type,
        side,
        part,
        function
    ):
        u"""获取场景中同类名称的下一个可用序号。"""

        node_type = cls._normalize_name_part(node_type)
        side = cls.normalize_side(side)
        part = cls._normalize_name_part(part)
        function = cls._normalize_name_part(function)

        base_name = "{0}_{1}_{2}_{3}".format(
            node_type,
            side,
            part,
            function
        )

        search_name = base_name + "_*"

        nodes = cmds.ls(search_name)

        if nodes is None:
            nodes = []

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

        return max_index + 1

    @classmethod
    def create_unique_name(
        cls,
        node_type,
        side,
        part,
        function
    ):
        u"""创建场景中下一个可用的标准名称。"""

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
        u"""将标准名称拆分并返回字典。"""

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
        u"""返回名称的左右镜像名称，不修改 Maya 节点。"""

        name_object = cls(name=name)
        name_object.flip()

        return name_object.name

    # ============================================================
    # 兼容旧版 compose / decompose
    # ============================================================

    def compose(self):
        u"""根据当前成员变量组合名称。"""

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
        u"""翻转名称方向：lf <-> rt，同时兼容旧版 l <-> r。"""

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
        u"""将当前选择的节点重命名。"""

        names = cmds.ls(sl=True)

        if names is None:
            names = []

        for selected_name in names:
            object_name = selected_name.split("|")[-1]
            self._name = cmds.rename(object_name, new_name)

    @pipelineUtils.Pipeline.make_undo
    def add_prefix(self, prefix):
        u"""给当前节点添加前缀。"""

        self._name = cmds.rename(
            self._name,
            prefix + self._name
        )

        return self._name

    @pipelineUtils.Pipeline.make_undo
    def add_suffix(self, suffix):
        u"""给当前节点添加后缀。"""

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
        u"""给当前选择层级添加前缀。"""

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
        u"""给当前选择层级添加后缀。"""

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
        u"""根据关键字搜索替换当前节点名称。"""

        object_name = self._name.split("|")[-1]
        new_name = object_name.replace(search, replace)

        self._name = cmds.rename(
            self._name,
            new_name
        )

        return self._name

    def rename_to_name(self, new_name):
        u"""重命名为指定名称。"""

        self._name = cmds.rename(
            self._name,
            new_name
        )

        return self._name

    def regex_search_replace_name(self, search, replace):
        u"""根据正则表达式搜索替换名称。"""

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
        u"""检查并列出场景中所有重名节点。"""

        all_objects = cmds.ls(long=True)

        if all_objects is None:
            all_objects = []

        duplicate_object_list = []
        short_name_dict = {}

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

        if len(duplicate_object_list) == 0:
            cmds.warning(u"场景里没有重名的物体")

        return duplicate_object_list

    @staticmethod
    def rename_duplicate_object():
        u"""检查并重新命名场景内所有重名节点。"""

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
