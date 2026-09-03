# coding=utf-8
u"""
Rig Base
========

MuziTools Rig Naming 的基础对象。

标准命名：

    [type]_[side]_[part]_[function]_[index]

例如：

    ctrl_md_jaw_bind_001
    jnt_lf_brow_bind_003
    grp_md_face_rig_001

RigBase 支持两种使用方式：

1. 直接传入五段属性创建名称；
2. 传入已有 name，自动拆分出 type / side / part / function / index。

设计原则：
    1. Rig Naming 来自项目内部统一规则，默认可信；
    2. 不在每个调用层重复做 side / type / function / index 格式防御；
    3. 对已有 Maya 场景进行 Rebuild / Query 时，重点检查真实 Scene State；
    4. part 可以包含下划线；
    5. index 输出固定补齐为三位数字；
    6. RigBase 不负责 Joint、Controller、Matrix、Hierarchy 或 UI。
"""

from __future__ import print_function

try:
    import maya.cmds as cmds
except ImportError:
    cmds = None


class RigBase(object):
    u"""Rig 标准名称对象与基础 Naming 能力。"""

    def __init__(
            self,
            name=None,
            type=None,
            side="md",
            part=None,
            function=None,
            index=1
    ):
        u"""
        创建 RigBase；传入 name 时自动拆分名称。

        Args:
            name (str):
                创建或查询时使用的节点名称。
            type (object):
                当前方法执行 Maya / Rig 操作时使用的 `type` 数据。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            function (str | callable):
                当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。
            index (int):
                目标元素或节点的序号。
        """
        self.type = type
        self.side = side
        self.part = part
        self.function = function
        self.index = index

        if name is not None:
            self.decompose(name)

    # =========================================================================
    # Name
    # =========================================================================

    @property
    def name(self):
        u"""
        根据当前五段属性返回标准 Rig Name。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self.compose()

    def compose(
            self,
            type=None,
            side=None,
            part=None,
            function=None,
            index=None
    ):
        u"""
        组合标准 Rig Name。

        Args:
            type (object):
                当前方法执行 Maya / Rig 操作时使用的 `type` 数据。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            function (str | callable):
                当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。
            index (int):
                目标元素或节点的序号。

        Returns:
            object | None:
            当前 API 完成处理后返回的结果。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if type is None:
            type = self.type

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if side is None:
            side = self.side

        if part is None:
            part = self.part

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if function is None:
            function = self.function

        if index is None:
            index = self.index

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if type is None or part is None or function is None:
            return None

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return "{type}_{side}_{part}_{function}_{index:03d}".format(
            type=type,
            side=side,
            part=part,
            function=function,
            index=index
        )

    def create_name(
            self,
            type=None,
            function=None,
            side=None,
            part=None,
            index=None
    ):
        u"""
        按当前属性或临时覆盖值创建标准 Rig Name。

        Args:
            type (object):
                当前方法执行 Maya / Rig 操作时使用的 `type` 数据。
            function (str | callable):
                当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            index (int):
                目标元素或节点的序号。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
        """
        return self.compose(
            type=type,
            side=side,
            part=part,
            function=function,
            index=index
        )

    @classmethod
    def parse_name(cls, name):
        u"""
        把标准 Rig Name 拆分成五段字段。

        Args:
            name (str):
                创建或查询时使用的节点名称。

        Returns:
            dict:
            包含本次构建、查询或处理结果的结构化字典。
        """
        short_name = name.split("|")[-1]
        short_name = short_name.split(":")[-1]
        name_parts = short_name.split("_")

        return {
            "type": name_parts[0],
            "side": name_parts[1],
            "part": "_".join(name_parts[2:-2]),
            "function": name_parts[-2],
            "index": int(name_parts[-1]),
        }

    def decompose(self, name):
        u"""
        拆分已有名称，并写入当前 RigBase 的五段属性。

        Args:
            name (str):
                创建或查询时使用的节点名称。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        name_data = self.parse_name(name)

        self.type = name_data["type"]
        self.side = name_data["side"]
        self.part = name_data["part"]
        self.function = name_data["function"]
        self.index = name_data["index"]

        return self

    def mirror_name(self, name=None):
        u"""
        返回当前名称或指定名称的左右镜像名称。

        Args:
            name (str):
                创建或查询时使用的节点名称。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        if name is None:
            name = self.name

        name_data = self.parse_name(name)
        mirror_side = self.get_opposite_side(
            name_data["side"]
        )

        return self.create_name(
            type=name_data["type"],
            side=mirror_side,
            part=name_data["part"],
            function=name_data["function"],
            index=name_data["index"]
        )

    # =========================================================================
    # Scene Unique Name
    # =========================================================================

    def get_next_index(
            self,
            type=None,
            function=None,
            side=None,
            part=None
    ):
        u"""
        返回 Maya 场景中同一 Naming Base 的下一个序号。

        这里查询的是已有 Scene State，因此同前缀但不符合数字后缀的外部节点会被跳过，
        不让异常场景名称破坏正常 Rig Build。

        Args:
            type (object):
                当前方法执行 Maya / Rig 操作时使用的 `type` 数据。
            function (str | callable):
                当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if cmds is None:
            raise RuntimeError(
                u"get_next_index() 必须在 Maya 环境中运行。"
            )

        # -------------------------------------------------------------------------
        # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        base_name = self.create_name(
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

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if node_list is None:
            node_list = []

        max_index = 0

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for node in node_list:
            short_name = node.split("|")[-1]
            short_name = short_name.split(":")[-1]
            index_text = short_name.rsplit(
                "_",
                1
            )[-1]

            if not index_text.isdigit():
                continue

            node_index = int(
                index_text
            )

            if node_index > max_index:
                max_index = node_index

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return max_index + 1

    def create_unique_name(
            self,
            type=None,
            function=None,
            side=None,
            part=None
    ):
        u"""
        创建 Maya 场景中下一个可用的标准 Rig Name。

        Args:
            type (object):
                当前方法执行 Maya / Rig 操作时使用的 `type` 数据。
            function (str | callable):
                当前 API 使用的功能 Token 或执行函数；在命名 API 中表示 function 段，在工具 API 中表示 Callable。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
        """
        next_index = self.get_next_index(
            type=type,
            function=function,
            side=side,
            part=part
        )

        return self.create_name(
            type=type,
            function=function,
            side=side,
            part=part,
            index=next_index
        )

    # =========================================================================
    # Side
    # =========================================================================

    def get_opposite_side(self, side=None):
        u"""
        返回相反 Side；md 保持 md。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。

        Returns:
            str:
            当前 API 查询或处理后得到的字符串结果。
        """
        if side is None:
            side = self.side

        if side == "lf":
            return "rt"

        if side == "rt":
            return "lf"

        return "md"


__all__ = [
    "RigBase",
]
