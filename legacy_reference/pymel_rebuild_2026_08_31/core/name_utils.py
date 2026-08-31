# coding=utf-8
u"""
Name Utils
==========

MuziTools Rig 标准命名模块。

正式模块路径
------------
``muziToolset.core.name_utils`` 是 Rig 名称语义的唯一正式实现。
旧 ``nameUtils.py`` 兼容模块已经完成迁移并删除，正式代码和文档统一使用 snake_case 路径。

标准命名规则
------------
    [类型]_[方向]_[部位]_[功能]_[序号]

例如：
    grp_md_face_master_001
    ctrl_lf_eye_main_001
    jnt_rt_brow_bind_003
    model_md_head_tweak_001

模块职责
--------
本模块负责“名称语义”本身：标准名称生成、解析、Side 规范化、镜像名称、唯一序号、
层级前后缀、正则替换，以及重名 DAG 节点检查。

主要公开 API
------------
Name.create_name(node_type, side, part, function, index=1)
    按正式五段式规则生成名称。

Name.normalize_side(side)
    把 l / left / lf、r / right / rt、m / center / md 等输入统一为 lf / rt / md。

Name.get_next_index(...)
Name.create_unique_name(...)
    查询场景并生成下一个可用序号。

Name.parse_name(name)
    将标准名称解析成 type / side / part / function / index 字典。

Name.mirror_name(name)
    只计算左右镜像名称，不修改 Maya 节点。

Name.compose()
Name.decompose()
Name.flip()
    Name 对象内部的组合、拆分与 Side 翻转。

Name.add_prefix(...)
Name.add_suffix(...)
Name.add_hierarchy_prefix(...)
Name.add_hierarchy_suffix(...)
Name.search_replace_name(...)
Name.regex_search_replace_name(...)
Name.rename_to_name(...)
    Maya Rename 兼容操作。

Name.print_duplicate_object()
Name.rename_duplicate_object()
    检查 / 修复重名 DAG 节点。

和 rename_utils.py 的区别
-------------------------
name_utils.py
    负责“一个 Rig 名称应该是什么”和 Name 对象语义。

rename_utils.py
    负责面向批量操作 / Tool 的 Prefix、Suffix、Search Replace、Auto Number、Pattern Rename。

两个模块名字相近，但职责不同，因此保持独立。

设计原则
--------
1. 当前 Side Token 统一为 lf / rt / md；
2. function 字段允许包含下划线，最后三位数字永远作为 index；
3. Rename 层级时先处理最深子节点，避免 Parent Rename 后旧 DAG Path 失效；
4. 本模块不依赖旧 Pipeline；
5. 模块文件名与所有正式 Import 统一使用 snake_case。
"""

from __future__ import print_function

import re

import maya.cmds as cmds

from . import scene_utils
from . import hierarchy_utils


# =============================================================================
# Undo / DAG Helper
# =============================================================================



# =============================================================================
# Name
# =============================================================================

class Name(object):
    """Rig 标准名称对象。"""

    node_types = [
        "grp",
        "zero",
        "offset",
        "connect",
        "space",
        "driven",
        "output",
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
        "attach",
        "bs",
        "skin",
        "cns",
        "mult",
        "pma",
        "remap",
        "clamp",
        "condition",
    ]

    sides = [
        "lf",
        "rt",
        "md",
    ]

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
        "md": "md",
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
        创建 Name 对象。

        Args:
            name (str/None):
                已存在的标准名称；给定时自动 decompose。
            type (str/None):
                旧接口，节点类型。
            side (str/None):
                方向。
            resolution (str/None):
                旧接口，对应当前 part。
            description (str/None):
                旧接口，对应当前 function。
            index (int/None):
                序号。
            part (str/None):
                当前接口，部位。
            function (str/None):
                当前接口，功能。

        Notes:
            resolution / description 继续保留，只为了兼容早期调用；新代码应优先使用 part / function。
        """
        self.nodes = []

        self._type = type
        self._side = side
        self._resolution = resolution
        self._description = description
        self._index = index
        self._name = name

        if part is not None:
            self._resolution = part

        if function is not None:
            self._description = function

        if self._name:
            self.decompose()

    # =========================================================================
    # Property - 旧字段和新字段保持兼容
    # =========================================================================

    @property
    def type(self):
        u"""
        执行 `type` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self._type

    @type.setter
    def type(self, value):
        u"""
        执行 `type` 对应的 Maya 工具操作。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._type = value

    @property
    def side(self):
        u"""
        执行 `side` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self._side

    @side.setter
    def side(self, value):
        u"""
        执行 `side` 对应的 Maya 工具操作。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._side = value

    @property
    def resolution(self):
        u"""
        执行 `resolution` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self._resolution

    @resolution.setter
    def resolution(self, value):
        u"""
        执行 `resolution` 对应的 Maya 工具操作。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._resolution = value

    @property
    def description(self):
        u"""
        执行 `description` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self._description

    @description.setter
    def description(self, value):
        u"""
        执行 `description` 对应的 Maya 工具操作。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._description = value

    @property
    def part(self):
        u"""
        部位字段；内部与旧 resolution 共用存储。

        Returns:
            object:
            方法执行后的结果数据。
        """
        return self._resolution

    @part.setter
    def part(self, value):
        u"""
        执行 `part` 对应的 Maya 工具操作。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._resolution = value

    @property
    def function(self):
        u"""
        功能字段；内部与旧 description 共用存储。

        Returns:
            object:
            方法执行后的结果数据。
        """
        return self._description

    @function.setter
    def function(self, value):
        u"""
        执行 `function` 对应的 Maya 工具操作。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._description = value

    @property
    def index(self):
        u"""
        执行 `index` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self._index

    @index.setter
    def index(self, value):
        u"""
        执行 `index` 对应的 Maya 工具操作。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """

        self._index = value

    @property
    def name(self):
        u"""
        根据当前字段重新 compose 并返回完整名称。

        Returns:
            object:
            方法执行后的结果数据。
        """
        self.compose()
        return self._name

    # =========================================================================
    # Normalize / Build / Parse
    # =========================================================================

    @staticmethod
    def _normalize_name_part(value):
        """
        规范单个名称字段。

        处理规则：Trim -> 空格 / 横线转下划线 -> 合并连续下划线 -> lower-case。
        """
        if value is None:
            return None

        value = str(value).strip()

        if value == "":
            return None

        value = value.replace(" ", "_")
        value = value.replace("-", "_")

        while "__" in value:
            value = value.replace("__", "_")

        return value.strip("_").lower()

    @classmethod
    def normalize_side(cls, side):
        u"""
        把方向统一为正式 ``lf / rt / md`` Token。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。

        Returns:
            str | object:
            方法执行后的结果数据。

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
            u"不支持的方向名称: {}".format(side)
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
        根据五段式规则创建标准名称。

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
            方法执行后的结果数据。

        Raises:
            ValueError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 步骤 1：所有字段先规范化，避免不同 Tool 产生大小写 / 空格差异。
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

        # 步骤 2：序号固定三位，保证 Outliner 字符串排序稳定。
        return "{0}_{1}_{2}_{3}_{4:03d}".format(
            node_type,
            side,
            part,
            function,
            index
        )

    @classmethod
    def get_next_index(
            cls,
            node_type,
            side,
            part,
            function
    ):
        u"""
        查询场景中同类标准名称，并返回下一个可用序号。

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
            方法执行后的结果数据。
        """
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

        nodes = cmds.ls(
            base_name + "_*"
        ) or []

        max_index = 0

        for node in nodes:
            short_name = node.split("|")[-1]
            short_name = short_name.split(":")[-1]
            name_parts = short_name.split("_")

            if not name_parts:
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
        u"""
        生成场景中下一个可用的标准名称。

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
            方法执行后的结果数据。
        """
        index = cls.get_next_index(
            node_type=node_type,
            side=side,
            part=part,
            function=function
        )

        return cls.create_name(
            node_type=node_type,
            side=side,
            part=part,
            function=function,
            index=index
        )

    @classmethod
    def parse_name(cls, name):
        u"""
        把标准名称解析成字典。

        Args:
            name (str):
                创建或查询时使用的节点名称。

        Returns:
            dict:
            方法执行后的结果数据。
        """
        name_object = cls(name=name)

        return {
            "type": name_object.type,
            "side": name_object.side,
            "part": name_object.part,
            "function": name_object.function,
            "index": name_object.index,
        }

    @classmethod
    def mirror_name(cls, name):
        u"""
        计算镜像名称，不修改 Maya 节点。

        Args:
            name (str):
                创建或查询时使用的节点名称。

        Returns:
            object:
            方法执行后的结果数据。
        """
        name_object = cls(name=name)
        name_object.flip()
        return name_object.name

    def compose(self):
        u"""
        根据当前对象字段重新组合标准名称。

        Returns:
            object:
            方法执行后的结果数据。
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

        function 允许包含多个下划线，因此规则固定为：
            第 1 段 type；第 2 段 side；第 3 段 part；最后一段 index；中间全部属于 function。

        Returns:
            bool:
            方法执行后的结果数据。
        """
        if not self._name:
            return False

        short_name = self._name.split("|")[-1]
        short_name = short_name.split(":")[-1]
        name_parts = short_name.split("_")

        if len(name_parts) < 5:
            return False

        index_string = name_parts[-1]

        if not index_string.isdigit():
            return False

        self._type = name_parts[0]
        self._side = self.normalize_side(name_parts[1])
        self._resolution = name_parts[2]
        self._description = "_".join(name_parts[3:-1])
        self._index = int(index_string)

        return True

    def flip(self):
        u"""
        翻转 lf <-> rt；md 保持不变。

        Returns:
            object:
            方法执行后的结果数据。
        """
        normalized_side = self.normalize_side(self._side)

        if normalized_side == "lf":
            self._side = "rt"
        elif normalized_side == "rt":
            self._side = "lf"
        else:
            self._side = "md"

        return self._side

    # =========================================================================
    # Maya Rename - 兼容 API
    # =========================================================================

    def set_rename(self, new_name):
        u"""
        把当前 Selection 节点依次重命名为 new_name。

        Args:
            new_name (str):
                `new_name` 对应的 Maya 节点或资源名称。

        Returns:
            object:
            方法执行后的结果数据。
        """
        names = cmds.ls(
            selection=True,
            long=True
        ) or []

        for selected_name in names:
            self._name = cmds.rename(
                selected_name,
                new_name
            )

        return self._name

    @scene_utils.undo_chunk
    def add_prefix(self, prefix):
        u"""
        给当前 Name 节点添加前缀。

        Args:
            prefix (str):
                添加到 Maya 节点名称前部的 Prefix。

        Returns:
            object:
            方法执行后的结果数据。
        """
        self._name = cmds.rename(
            self._name,
            prefix + self._name.split("|")[-1]
        )
        return self._name

    @scene_utils.undo_chunk
    def add_suffix(self, suffix):
        u"""
        给当前 Name 节点添加后缀。

        Args:
            suffix (str):
                添加到 Maya 节点名称尾部的 Suffix。

        Returns:
            object:
            方法执行后的结果数据。
        """
        short_name = self._name.split("|")[-1]
        self._name = cmds.rename(
            self._name,
            short_name + suffix
        )
        return self._name

    def _selection_list_nodes(self):
        """返回当前 Selection 及其全部后代，自动去重。"""
        self.nodes = []
        selected_nodes = cmds.ls(
            selection=True,
            long=True
        ) or []

        for selected_node in selected_nodes:
            if selected_node not in self.nodes:
                self.nodes.append(selected_node)

            children = cmds.listRelatives(
                selected_node,
                allDescendents=True,
                fullPath=True
            ) or []

            for child in children:
                if child not in self.nodes:
                    self.nodes.append(child)

        return self.nodes

    @scene_utils.undo_chunk
    def add_hierarchy_prefix(self, prefix):
        u"""
        给当前 Selection 整个层级添加前缀。

        Args:
            prefix (str):
                添加到 Maya 节点名称前部的 Prefix。
        """
        self.nodes = self._selection_list_nodes()
        self.nodes.sort(
            key=hierarchy_utils.Hierarchy.get_dag_depth,
            reverse=True
        )

        # 子节点先改名，避免 Parent 改名后旧 Child Long Path 失效。
        for node in self.nodes:
            object_name = node.split("|")[-1]
            cmds.rename(
                node,
                prefix + object_name
            )

    @scene_utils.undo_chunk
    def add_hierarchy_suffix(self, suffix):
        u"""
        给当前 Selection 整个层级添加后缀。

        Args:
            suffix (str):
                添加到 Maya 节点名称尾部的 Suffix。
        """
        self.nodes = self._selection_list_nodes()
        self.nodes.sort(
            key=hierarchy_utils.Hierarchy.get_dag_depth,
            reverse=True
        )

        for node in self.nodes:
            object_name = node.split("|")[-1]
            cmds.rename(
                node,
                object_name + suffix
            )

    @scene_utils.undo_chunk
    def search_replace_name(self, search, replace):
        u"""
        对当前 Name 节点执行普通字符串 Search / Replace。

        Args:
            search (str):
                节点名称中需要查找并替换的字符串。
            replace (bool):
                替换 Search 内容的新字符串。

        Returns:
            object:
            方法执行后的结果数据。
        """
        object_name = self._name.split("|")[-1]
        new_name = object_name.replace(
            search,
            replace
        )

        self._name = cmds.rename(
            self._name,
            new_name
        )
        return self._name

    def rename_to_name(self, new_name):
        u"""
        把当前 Name 节点重命名为明确名称。

        Args:
            new_name (str):
                `new_name` 对应的 Maya 节点或资源名称。

        Returns:
            object:
            方法执行后的结果数据。
        """
        self._name = cmds.rename(
            self._name,
            new_name
        )
        return self._name

    @scene_utils.undo_chunk
    def regex_search_replace_name(self, search, replace):
        u"""
        使用正则表达式 Search / Replace 当前 Selection 层级。

        Args:
            search (str):
                节点名称中需要查找并替换的字符串。
            replace (bool):
                替换 Search 内容的新字符串。
        """
        regex_object = re.compile(search)
        nodes = self._selection_list_nodes()
        nodes.sort(
            key=hierarchy_utils.Hierarchy.get_dag_depth,
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

    # =========================================================================
    # Duplicate DAG Name
    # =========================================================================

    @staticmethod
    def print_duplicate_object():
        u"""
        检查并返回场景中所有重名 DAG 节点 Long Path。

        Returns:
            object:
            方法执行后的结果数据。
        """
        all_objects = cmds.ls(
            long=True,
            dagObjects=True
        ) or []

        short_name_dict = {}

        # 步骤 1：按 Short Name 建立 Long Path 分组。
        for object_name in all_objects:
            short_name = object_name.split("|")[-1]

            if short_name not in short_name_dict:
                short_name_dict[short_name] = []

            short_name_dict[short_name].append(object_name)

        # 步骤 2：只有同名数量 > 1 才属于 Duplicate。
        duplicate_object_list = []

        for short_name in short_name_dict:
            object_list = short_name_dict[short_name]

            if len(object_list) <= 1:
                continue

            for object_name in object_list:
                duplicate_object_list.append(object_name)
                cmds.warning(
                    u"场景里有重名的物体: {}".format(object_name)
                )

        if not duplicate_object_list:
            cmds.warning(u"场景里没有重名的物体")

        return duplicate_object_list

    @staticmethod
    @scene_utils.undo_chunk
    def rename_duplicate_object():
        u"""
        给场景中重名 DAG 节点追加三位数字后缀。
        """
        duplicate_object_list = Name.print_duplicate_object()
        duplicate_object_list.sort(
            key=hierarchy_utils.Hierarchy.get_dag_depth,
            reverse=True
        )

        rename_count_dict = {}

        for duplicate_object in duplicate_object_list:
            if not cmds.objExists(duplicate_object):
                continue

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


__all__ = [
    "Name",
]
