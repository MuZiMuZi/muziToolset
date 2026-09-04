# coding=utf-8
u"""
name_utils：Maya Rig 基础命名工具。

标准命名规则：
    [类型]_[方向]_[部位]_[功能]_[序号]

例如：
    grp_md_face_master_001
    ctrl_lf_eye_main_001
    jnt_rt_brow_bind_003

方法介绍与使用场景：

    Name.__init__
        创建一个名称对象。
        可以直接传入完整名称，也可以分别传入 type / side / part / function / index。

    Name.decompose_name
        将完整标准名称拆分成 type / side / part / function / index。
        适合读取已有 Maya 节点名称中的命名信息。

    Name.compose_name
        根据 type / side / part / function / index 组合标准名称。
        适合创建 Joint、Controller、Group 等节点名称。

    Name.flip
        翻转左右方向 lf / rt。
        适合镜像 Rig、Joint、Controller 等左右结构时使用。
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
        u"""
        初始化名称数据。

        Maya 使用示例：

            from muziToolset.core.common import name_utils

            name_object = name_utils.Name(
                type="ctrl",
                side="lf",
                part="eye",
                function="main",
                index=1
            )
        """

        self.name = name
        self.type = type
        self.side = side
        self.part = part
        self.function = function
        self.index = index

        if self.name:
            self.decompose_name()

    def decompose_name(self):
        u"""
        将标准名称拆分到当前对象的数据中。

        Maya 使用示例：

            from muziToolset.core.common import name_utils

            name_object = name_utils.Name(
                name="jnt_rt_brow_bind_003"
            )

            print(name_object.type)
            print(name_object.side)
            print(name_object.part)
            print(name_object.function)
            print(name_object.index)
        """

        name_parts = self.name.split("_")

        self.type = name_parts[0]
        self.side = name_parts[1]
        self.part = name_parts[2]
        self.function = name_parts[3]
        self.index = int(name_parts[4])

        return name_parts

    def compose_name(self):
        u"""
        根据当前数据组合标准名称。

        Maya 使用示例：

            from muziToolset.core.common import name_utils

            name_object = name_utils.Name(
                type="ctrl",
                side="lf",
                part="eye",
                function="main",
                index=1
            )

            print(name_object.compose_name())
            # ctrl_lf_eye_main_001
        """

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
        u"""
        翻转左右方向：lf <-> rt。

        Maya 使用示例：

            from muziToolset.core.common import name_utils

            name_object = name_utils.Name(
                type="ctrl",
                side="lf",
                part="eye",
                function="main",
                index=1
            )

            name_object.flip()
            print(name_object.side)
            # rt
        """

        if self.side == "lf":
            self.side = "rt"

        elif self.side == "rt":
            self.side = "lf"

        return self.side
