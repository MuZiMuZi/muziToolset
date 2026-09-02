# coding=utf-8
u"""
Rig Base
========

MuziTools 所有 Rig Object / Module 共用的最底层实例基类。

RigBase 只保存最基础的 Rig Object 属性：

    side
    part
    index

这些值直接作为实例属性使用，不额外包装 get / set / identity 方法。

标准 Rig Naming：

    [node_type]_[side]_[part]_[function]_[index]

例如：

    ctrl_md_upper_teeth_bind_001
    jnt_lf_brow_bind_003
    grp_md_face_rig_nodes_001

核心原则：
    1. RigBase 是可实例化的 Rig 对象基础类；
    2. side / part / index 直接通过实例属性读取；
    3. create_name() 没有显式覆盖时使用当前实例属性；
    4. node_type / function 描述具体 Maya 节点，不属于 Rig Object 属性；
    5. parse_name() 只解析输入名称，不修改当前实例；
    6. Rig Naming 属于 systems 层，不属于 core；
    7. RigBase 不负责 Joint、Controller、Matrix、Config、Hierarchy 或 UI。
"""

from __future__ import print_function

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


class RigBase(object):
    u"""所有 Rig Object 共用的基础属性与 Naming 基类。"""

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
            side="md",
            part=None,
            index=1
    ):
        u"""初始化 Rig Object 的基础属性。"""
        self.side = self.normalize_side(
            side
        )
        self.part = self.normalize_part(
            part
        )
        self.index = self.validate_index(
            index
        )

    # =========================================================================
    # Normalize / Validate
    # =========================================================================

    @staticmethod
    def _normalize_token(value):
        u"""规范一个 Naming Token / Part 字符串。"""
        if value is None:
            return None

        value = str(value).strip()

        if not value:
            return None

        value = value.replace(" ", "_")
        value = value.replace("-", "_")

        while "__" in value:
            value = value.replace("__", "_")

        return value.strip("_").lower()

    @classmethod
    def normalize_side(cls, side):
        u"""把 Side Alias 统一为 lf / rt / md。"""
        if side is None:
            side = "md"

        side = cls._normalize_token(
            side
        )

        if side in cls.side_aliases:
            return cls.side_aliases[side]

        raise ValueError(
            u"不支持的 Rig Side：{}".format(
                side
            )
        )

    @classmethod
    def normalize_part(cls, part):
        u"""规范 Rig Part；Part 可以包含下划线。"""
        part = cls._normalize_token(
            part
        )

        if part is None:
            raise ValueError(
                u"Rig Part 不能为空。"
            )

        return part

    @classmethod
    def normalize_node_type(cls, node_type):
        u"""规范 Node Type，并保证它是单一 Token。"""
        node_type = cls._normalize_token(
            node_type
        )

        if node_type is None:
            raise ValueError(
                u"Rig Name node_type 不能为空。"
            )

        if "_" in node_type:
            raise ValueError(
                u"Rig Name node_type 必须是单一 Token：{}".format(
                    node_type
                )
            )

        return node_type

    @classmethod
    def normalize_function(cls, function):
        u"""规范 Function，并保证它是单一 Token。"""
        function = cls._normalize_token(
            function
        )

        if function is None:
            raise ValueError(
                u"Rig Name function 不能为空。"
            )

        if "_" in function:
            raise ValueError(
                u"Rig Name function 必须是单一 Token：{}".format(
                    function
                )
            )

        return function

    @staticmethod
    def validate_index(index):
        u"""验证三位 Rig Index，并返回 int。"""
        if isinstance(index, bool):
            raise TypeError(
                u"Rig Index 必须是整数，不能是 bool。"
            )

        if isinstance(index, float):
            if not index.is_integer():
                raise TypeError(
                    u"Rig Index 必须是整数，不能是小数：{}".format(
                        index
                    )
                )

        try:
            index = int(
                index
            )
        except (TypeError, ValueError):
            raise TypeError(
                u"Rig Index 必须是整数。"
            )

        if index < 1 or index > 999:
            raise ValueError(
                u"Rig Index 必须在 1 ~ 999，当前值：{}".format(
                    index
                )
            )

        return index

    # =========================================================================
    # Naming
    # =========================================================================

    def create_name(
            self,
            node_type,
            function,
            side=None,
            part=None,
            index=None
    ):
        u"""根据实例属性创建标准 Rig Name。"""
        if side is None:
            side = self.side

        if part is None:
            part = self.part

        if index is None:
            index = self.index

        node_type = self.normalize_node_type(
            node_type
        )
        side = self.normalize_side(
            side
        )
        part = self.normalize_part(
            part
        )
        function = self.normalize_function(
            function
        )
        index = self.validate_index(
            index
        )

        return "{node_type}_{side}_{part}_{function}_{index:03d}".format(
            node_type=node_type,
            side=side,
            part=part,
            function=function,
            index=index
        )

    @classmethod
    def parse_name(cls, name):
        u"""解析标准 Rig Name，不修改任何 RigBase 实例。"""
        if not isinstance(name, str):
            raise TypeError(
                u"Rig Name 必须是字符串。"
            )

        short_name = name.split("|")[-1]
        short_name = short_name.split(":")[-1]
        name_parts = short_name.split("_")

        if len(name_parts) < 5:
            raise ValueError(
                u"不是有效的五段式 Rig Name：{}".format(
                    name
                )
            )

        index_string = name_parts[-1]

        if len(index_string) != 3:
            raise ValueError(
                u"Rig Name index 必须是三位数字：{}".format(
                    name
                )
            )

        if not index_string.isdigit():
            raise ValueError(
                u"Rig Name index 必须是数字：{}".format(
                    name
                )
            )

        node_type = cls.normalize_node_type(
            name_parts[0]
        )
        side = cls.normalize_side(
            name_parts[1]
        )
        part = cls.normalize_part(
            "_".join(
                name_parts[2:-2]
            )
        )
        function = cls.normalize_function(
            name_parts[-2]
        )
        index = cls.validate_index(
            int(index_string)
        )

        return {
            "node_type": node_type,
            "side": side,
            "part": part,
            "function": function,
            "index": index,
        }

    @classmethod
    def validate_name(cls, name):
        u"""检查输入是否符合正式 Rig Naming Convention。"""
        try:
            cls.parse_name(
                name
            )
        except (TypeError, ValueError):
            return False

        return True

    def mirror_name(self, name):
        u"""返回 lf / rt 镜像名称；md 名称保持 md。"""
        fields = self.parse_name(
            name
        )
        mirrored_side = self.get_opposite_side(
            fields["side"]
        )

        return self.create_name(
            node_type=fields["node_type"],
            side=mirrored_side,
            part=fields["part"],
            function=fields["function"],
            index=fields["index"]
        )

    # =========================================================================
    # Scene Unique Name
    # =========================================================================

    def get_next_index(
            self,
            node_type,
            function,
            side=None,
            part=None
    ):
        u"""返回场景中同一 Naming Base 的下一个可用序号。"""
        if cmds is None:
            raise RuntimeError(
                u"get_next_index() 必须在 Maya 环境中运行。"
            )

        if side is None:
            side = self.side

        if part is None:
            part = self.part

        node_type = self.normalize_node_type(
            node_type
        )
        side = self.normalize_side(
            side
        )
        part = self.normalize_part(
            part
        )
        function = self.normalize_function(
            function
        )

        base_name = self.create_name(
            node_type=node_type,
            side=side,
            part=part,
            function=function,
            index=1
        ).rsplit(
            "_",
            1
        )[0]

        node_list = cmds.ls(
            base_name + "_*"
        )

        if node_list is None:
            node_list = []

        max_index = 0

        for node in node_list:
            short_name = node.split("|")[-1]
            short_name = short_name.split(":")[-1]

            if not self.validate_name(short_name):
                continue

            fields = self.parse_name(
                short_name
            )

            if fields["node_type"] != node_type:
                continue

            if fields["side"] != side:
                continue

            if fields["part"] != part:
                continue

            if fields["function"] != function:
                continue

            if fields["index"] > max_index:
                max_index = fields["index"]

        next_index = max_index + 1

        if next_index > 999:
            raise RuntimeError(
                u"Rig Naming Index 已超过 999：{}_{}".format(
                    base_name,
                    next_index
                )
            )

        return next_index

    def create_unique_name(
            self,
            node_type,
            function,
            side=None,
            part=None
    ):
        u"""创建场景中下一个可用的标准 Rig Name。"""
        next_index = self.get_next_index(
            node_type=node_type,
            function=function,
            side=side,
            part=part
        )

        return self.create_name(
            node_type=node_type,
            function=function,
            side=side,
            part=part,
            index=next_index
        )

    # =========================================================================
    # Side
    # =========================================================================

    def get_opposite_side(self, side=None):
        u"""返回相反 Side；md 保持 md，不修改实例属性。"""
        if side is None:
            side = self.side

        side = self.normalize_side(
            side
        )

        if side == "lf":
            return "rt"

        if side == "rt":
            return "lf"

        return "md"


__all__ = [
    "RigBase",
]
