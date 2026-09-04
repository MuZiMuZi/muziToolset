# coding=utf-8
u"""
name_utils：Maya Rig 基础命名工具。

标准命名规则：
    [类型]_[方向]_[部位]_[功能]_[序号]

例如：
    grp_md_face_master_001
    ctrl_lf_eye_main_001
    jnt_rt_brow_bind_003

当前只负责三件事情：
    1. 拆分名称
    2. 组合名称
    3. 翻转左右方向
"""


class Name(object):

    def __init__(
        self,
        name=None,
        type=None,
        side=None,
        part=None,
        function=None,
        index=None
    ):
        u"""初始化名称数据。"""

        self.name = name
        self.type = type
        self.side = side
        self.part = part
        self.function = function
        self.index = index

        if self.name:
            self.decompose()

    def decompose(self):
        u"""将标准名称拆分到当前对象的数据中。"""

        name_parts = self.name.split("_")

        self.type = name_parts[0]
        self.side = name_parts[1]
        self.part = name_parts[2]
        self.function = name_parts[3]
        self.index = int(name_parts[4])

        return name_parts

    def compose_name(self):
        u"""根据当前数据组合标准名称。"""

        if self.index is None:
            self.index = 1

        self.index = int(self.index)

        self.name = "{0}_{1}_{2}_{3}_{4:03d}".format(
            self.type,
            self.side,
            self.part,
            self.function,
            self.index
        )

        return self.name

    def flip(self):
        u"""翻转左右方向：lf <-> rt。"""

        if self.side == "lf":
            self.side = "rt"

        elif self.side == "rt":
            self.side = "lf"

        return self.side
