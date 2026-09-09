# coding=utf-8
u"""
name_utils：Maya Rig 基础命名工具。

标准命名规则：
    [类型]_[方向]_[部位]_[功能]_[序号]

其中 part 允许使用下划线组成复合部位名称，例如：
    upper_lid
    nose_center
    mouth_corner

例如：
    grp_md_face_master_001
    ctrl_lf_eye_main_001
    jnt_rt_brow_bind_003
    loc_lf_upper_lid_bind_001

方法介绍与使用场景：

    Name.__init__
        创建一个名称对象。
        可以直接传入完整名称，也可以分别传入 type / side / part / function / index。

    Name.decompose_name
        将完整标准名称拆分成 type / side / part / function / index。
        支持 part 中包含下划线，例如 upper_lid、nose_center。
        适合读取已有 Maya 节点名称中的命名信息。

    Name.compose_name
        根据 type / side / part / function / index 组合标准名称。
        适合创建 Joint、Controller、Group、Locator 等节点名称。

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

        name(str): 可选完整标准名称。
        type(str): 节点类型，例如 "ctrl"、"jnt"、"loc"、"grp"。
        side(str): 节点方向，例如 "lf"、"rt"、"md"。
        part(str): 节点部位，允许包含下划线，例如 "upper_lid"。
        function(str): 节点功能，例如 "bind"、"main"、"aim"。
        index(int): 节点序号。

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
        else:
            self.compose_name()

    def decompose_name(self):
        u"""
        将标准名称拆分到当前对象的数据中。

        命名解析规则固定使用：
            第 1 段       -> type
            第 2 段       -> side
            中间所有段    -> part
            倒数第 2 段   -> function
            最后 1 段     -> index

        因此 part 可以安全包含下划线：
            loc_lf_upper_lid_bind_001
                type     = loc
                side     = lf
                part     = upper_lid
                function = bind
                index    = 1

        Returns:
            list: 原始名称按照下划线拆分后的字符串列表。

        Maya 使用示例：

            from muziToolset.core.common import name_utils

            name_object = name_utils.Name(
                name="loc_lf_upper_lid_bind_001"
            )

            print(name_object.type)
            print(name_object.side)
            print(name_object.part)
            print(name_object.function)
            print(name_object.index)
        """

        name_parts = self.name.split("_")

        if len(name_parts) < 5:
            raise ValueError(
                u"名称不符合标准命名规则：{}".format(self.name)
            )

        self.type = name_parts[0]
        self.side = name_parts[1]
        self.part = "_".join(name_parts[2:-2])
        self.function = name_parts[-2]

        if not self.part:
            raise ValueError(
                u"名称中缺少 part：{}".format(self.name)
            )

        try:
            self.index = int(name_parts[-1])
        except ValueError:
            raise ValueError(
                u"名称序号必须是整数：{}".format(self.name)
            )

        return name_parts

    def compose_name(self):
        u"""
        根据当前数据组合标准名称。

        part 可以包含下划线，compose_name() 会将它整体作为部位字段使用。

        Returns:
            str: 组合后的标准名称。

        Maya 使用示例：

            from muziToolset.core.common import name_utils

            name_object = name_utils.Name(
                type="loc",
                side="lf",
                part="upper_lid",
                function="bind",
                index=1
            )

            print(name_object.compose_name())
            # loc_lf_upper_lid_bind_001
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

        Returns:
            str: 翻转后的 side。

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
