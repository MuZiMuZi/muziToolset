# coding=utf-8
u"""
Rig Base
========

MuziTools 所有 Rig Object / Module 共用的最底层实例基类。

RigBase 不再是 Name Object，也不保存某一个 Maya Node 的 node_type / function。
它代表一个 Rig 对象自己的 Identity：

    side
    part
    index

标准 Rig Naming：

    [node_type]_[side]_[part]_[function]_[index]

例如：

    ctrl_md_upper_teeth_bind_001
    jnt_lf_brow_bind_003
    grp_md_face_rig_nodes_001

字段边界：
    node_type
        Maya / Rig 节点类型，必须是单一 Token。

    side
        lf / rt / md。

    part
        Rig 部位，允许包含下划线，例如 upper_teeth。

    function
        节点功能，必须是单一 Token。

    index
        001 ~ 999。

核心原则：
    1. RigBase 是可实例化的 Rig 对象基础类；
    2. 实例 Identity 只包含 side / part / index；
    3. create_name() 没有显式覆盖字段时，读取实例 Identity；
    4. parse_name() 只解析输入名称，不修改当前实例；
    5. Rig Naming 属于 systems 层，不属于 core；
    6. Core rename_utils 只负责 Maya Rename / Short Name 等通用操作；
    7. RigBase 不负责 Joint、Controller、Matrix、Config、Hierarchy 或 UI。
"""

from __future__ import print_function

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


class RigBase(object):
    u"""所有 Rig Object 共用的 Identity 与 Naming 基类。"""

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
        u"""
        初始化一个 Rig Object Identity。

        Args:
            side (str):
                Rig Side，支持 lf / rt / md 和常用 Alias。
            part (str):
                Rig Part，例如 jaw / teeth / upper_teeth。
            index (int):
                Rig Object 序号，范围 1 ~ 999。
        """
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
    # Identity
    # =========================================================================

    @property
    def identity(self):
        u"""返回当前 Rig Object Identity。"""
        return {
            "side": self.side,
            "part": self.part,
            "index": self.index,
        }

    def set_identity(
            self,
            side=None,
            part=None,
            index=None
    ):
        u"""显式更新当前 Rig Object Identity。"""
        if side is not None:
            self.side = self.normalize_side(
                side
            )

        if part is not None:
            self.part = self.normalize_part(
                part
            )

        if index is not None:
            self.index = self.validate_index(
                index
            )

        return self.identity

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

    @staticmethod
    def _resolve_node_type_alias(
            node_type,
            kwargs,
            method_name
    ):
        u"""处理 0.4 迁移期间遗留的 type Keyword Alias。"""
        legacy_node_type = kwargs.pop(
            "type",
            None
        )

        if kwargs:
            invalid_keys = []

            for key in kwargs:
                invalid_keys.append(
                    key
                )

            raise TypeError(
                u"{}() 不支持参数：{}".format(
                    method_name,
                    ", ".join(invalid_keys)
                )
            )

        if node_type is None:
            node_type = legacy_node_type
        elif legacy_node_type is not None:
            raise TypeError(
                u"{}() 的 node_type 和旧 type 参数不能同时传入。".format(
                    method_name
                )
            )

        return node_type

    def resolve_identity(
            self,
            side=None,
            part=None,
            index=None
    ):
        u"""解析 Naming 使用的 Identity；None 表示继承当前实例。"""
        if side is None:
            side = self.side

        if part is None:
            part = self.part

        if index is None:
            index = self.index

        return {
            "side": self.normalize_side(
                side
            ),
            "part": self.normalize_part(
                part
            ),
            "index": self.validate_index(
                index
            ),
        }

    # =========================================================================
    # Naming
    # =========================================================================

    def create_name(
            self,
            node_type=None,
            function=None,
            side=None,
            part=None,
            index=None,
            **kwargs
    ):
        u"""
        根据当前 Rig Identity 创建标准 Rig Name。

        side / part / index 没有显式传入时，自动使用当前实例 Identity。

        `type` 仅作为 0.4 迁移期间的旧 Keyword Alias；正式新代码统一使用
        `node_type`。
        """
        node_type = self._resolve_node_type_alias(
            node_type=node_type,
            kwargs=kwargs,
            method_name="create_name"
        )

        node_type = self.normalize_node_type(
            node_type
        )
        function = self.normalize_function(
            function
        )
        identity = self.resolve_identity(
            side=side,
            part=part,
            index=index
        )

        return "{node_type}_{side}_{part}_{function}_{index:03d}".format(
            node_type=node_type,
            side=identity["side"],
            part=identity["part"],
            function=function,
            index=identity["index"]
        )

    @classmethod
    def parse_name(cls, name):
        u"""
        解析标准 Rig Name。

        本方法只返回字段，不修改任何 RigBase 实例。
        """
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
            node_type=None,
            function=None,
            side=None,
            part=None,
            **kwargs
    ):
        u"""返回场景中同一 Naming Base 的下一个可用序号。"""
        if cmds is None:
            raise RuntimeError(
                u"get_next_index() 必须在 Maya 环境中运行。"
            )

        node_type = self._resolve_node_type_alias(
            node_type=node_type,
            kwargs=kwargs,
            method_name="get_next_index"
        )
        node_type = self.normalize_node_type(
            node_type
        )
        function = self.normalize_function(
            function
        )

        identity = self.resolve_identity(
            side=side,
            part=part,
            index=1
        )
        base_name = self.create_name(
            node_type=node_type,
            side=identity["side"],
            part=identity["part"],
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

            if fields["side"] != identity["side"]:
                continue

            if fields["part"] != identity["part"]:
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
            node_type=None,
            function=None,
            side=None,
            part=None,
            **kwargs
    ):
        u"""创建场景中下一个可用的标准 Rig Name。"""
        node_type = self._resolve_node_type_alias(
            node_type=node_type,
            kwargs=kwargs,
            method_name="create_unique_name"
        )

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
        u"""返回相反 Side；md 保持 md，不修改当前实例。"""
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

    def flip_side(self):
        u"""把当前 Rig Object Side 翻转为相反 Side。"""
        self.side = self.get_opposite_side(
            self.side
        )
        return self.side

    def is_left(self):
        u"""当前 Rig Object 是否为 Left。"""
        return self.side == "lf"

    def is_right(self):
        u"""当前 Rig Object 是否为 Right。"""
        return self.side == "rt"

    def is_center(self):
        u"""当前 Rig Object 是否为 Middle / Center。"""
        return self.side == "md"


__all__ = [
    "RigBase",
]
