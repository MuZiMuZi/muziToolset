# coding=utf-8
u"""
Rig Base
========

MuziTools 所有 Rig System / Module 共用的命名基础类。

正式命名规则：

    [type]_[side]_[part]_[function]_[index]

例如：

    ctrl_md_upper_teeth_bind_001
    jnt_lf_brow_bind_003
    grp_md_face_rig_nodes_001

字段边界：
    type
        Maya / Rig 节点类型。

    side
        lf / rt / md。

    part
        Rig 部位，允许包含下划线，例如 upper_teeth。

    function
        单一功能 Token，不允许包含下划线。

    index
        三位整数序号。

设计原则：
    1. Rig 命名属于 systems 层，不再放在 core；
    2. Core rename_utils 只负责 Maya Rename / Short Name 等通用操作；
    3. 不保留 resolution / description 等旧 Naming API；
    4. Module 通过继承 RigBase 直接使用 self.create_name() 等方法；
    5. 模块级 Config 可以直接调用 RigBase.create_name()。
"""

from __future__ import print_function

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


class RigBase(object):
    u"""Rig System / Module 共用的标准命名基础类。"""

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
            part=None,
            function=None,
            index=None
    ):
        u"""初始化 Rig Name 数据；传入 name 时自动解析。"""
        self._name = None
        self.type = type
        self.side = side
        self.part = part
        self.function = function
        self.index = index

        if name is not None:
            self._name = name
            self.decompose()

    # =========================================================================
    # Normalize
    # =========================================================================

    @staticmethod
    def _normalize_token(value):
        u"""规范一个 Naming Token。"""
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
            return "md"

        side = cls._normalize_token(side)

        if side in cls.side_aliases:
            return cls.side_aliases[side]

        raise ValueError(
            u"不支持的 Rig Side：{}".format(side)
        )

    @classmethod
    def _validate_fields(
            cls,
            type,
            side,
            part,
            function,
            index
    ):
        u"""验证正式五段式 Rig Name 字段。"""
        node_type = cls._normalize_token(type)
        normalized_side = cls.normalize_side(side)
        normalized_part = cls._normalize_token(part)
        normalized_function = cls._normalize_token(function)

        if node_type is None:
            raise ValueError(u"Rig Name type 不能为空。")

        if normalized_part is None:
            raise ValueError(u"Rig Name part 不能为空。")

        if normalized_function is None:
            raise ValueError(u"Rig Name function 不能为空。")

        if "_" in normalized_function:
            raise ValueError(
                u"Rig Name function 必须是单一 Token，不能包含下划线：{}".format(
                    normalized_function
                )
            )

        if index is None:
            index = 1

        index = int(index)

        if index < 0:
            raise ValueError(u"Rig Name index 不能小于 0。")

        return {
            "type": node_type,
            "side": normalized_side,
            "part": normalized_part,
            "function": normalized_function,
            "index": index,
        }

    # =========================================================================
    # Create / Parse
    # =========================================================================

    @classmethod
    def create_name(
            cls,
            type,
            side,
            part,
            function,
            index=1
    ):
        u"""根据正式五段式规则创建 Rig Name。"""
        fields = cls._validate_fields(
            type=type,
            side=side,
            part=part,
            function=function,
            index=index
        )

        return "{type}_{side}_{part}_{function}_{index:03d}".format(
            **fields
        )

    @classmethod
    def parse_name(cls, name):
        u"""解析正式 Rig Name 并返回字段字典。"""
        if not isinstance(name, str):
            raise TypeError(u"Rig Name 必须是字符串。")

        short_name = name.split("|")[-1]
        short_name = short_name.split(":")[-1]
        name_parts = short_name.split("_")

        if len(name_parts) < 5:
            raise ValueError(
                u"不是有效的五段式 Rig Name：{}".format(name)
            )

        index_string = name_parts[-1]

        if len(index_string) != 3:
            raise ValueError(
                u"Rig Name index 必须是三位数字：{}".format(name)
            )

        if not index_string.isdigit():
            raise ValueError(
                u"Rig Name index 必须是数字：{}".format(name)
            )

        part = "_".join(
            name_parts[2:-2]
        )

        fields = cls._validate_fields(
            type=name_parts[0],
            side=name_parts[1],
            part=part,
            function=name_parts[-2],
            index=int(index_string)
        )
        return fields

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

    # =========================================================================
    # Unique / Mirror
    # =========================================================================

    @classmethod
    def get_next_index(
            cls,
            type,
            side,
            part,
            function
    ):
        u"""返回场景中同一 Naming Base 的下一个可用序号。"""
        if cmds is None:
            raise RuntimeError(
                u"get_next_index() 必须在 Maya 环境中运行。"
            )

        base_name = cls.create_name(
            type=type,
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

            if not cls.validate_name(short_name):
                continue

            fields = cls.parse_name(short_name)

            if fields["type"] != cls._normalize_token(type):
                continue

            if fields["side"] != cls.normalize_side(side):
                continue

            if fields["part"] != cls._normalize_token(part):
                continue

            if fields["function"] != cls._normalize_token(function):
                continue

            if fields["index"] > max_index:
                max_index = fields["index"]

        return max_index + 1

    @classmethod
    def create_unique_name(
            cls,
            type,
            side,
            part,
            function
    ):
        u"""创建场景中下一个可用的标准 Rig Name。"""
        index = cls.get_next_index(
            type=type,
            side=side,
            part=part,
            function=function
        )

        return cls.create_name(
            type=type,
            side=side,
            part=part,
            function=function,
            index=index
        )

    @classmethod
    def mirror_name(cls, name):
        u"""计算 lf / rt 镜像名称；md 保持不变。"""
        fields = cls.parse_name(
            name
        )

        if fields["side"] == "lf":
            fields["side"] = "rt"
        elif fields["side"] == "rt":
            fields["side"] = "lf"

        return cls.create_name(
            type=fields["type"],
            side=fields["side"],
            part=fields["part"],
            function=fields["function"],
            index=fields["index"]
        )

    # =========================================================================
    # Object API
    # =========================================================================

    @property
    def name(self):
        u"""返回当前字段组合后的正式 Rig Name。"""
        return self.compose()

    def compose(self):
        u"""根据当前对象字段重新组合名称。"""
        self._name = self.create_name(
            type=self.type,
            side=self.side,
            part=self.part,
            function=self.function,
            index=self.index
        )
        return self._name

    def decompose(self):
        u"""把当前 name 解析回对象字段。"""
        fields = self.parse_name(
            self._name
        )

        self.type = fields["type"]
        self.side = fields["side"]
        self.part = fields["part"]
        self.function = fields["function"]
        self.index = fields["index"]
        return True

    def flip(self):
        u"""翻转当前对象 Side。"""
        normalized_side = self.normalize_side(
            self.side
        )

        if normalized_side == "lf":
            self.side = "rt"
        elif normalized_side == "rt":
            self.side = "lf"
        else:
            self.side = "md"

        return self.side


__all__ = [
    "RigBase",
]
