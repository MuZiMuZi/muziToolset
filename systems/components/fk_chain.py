# coding=utf-8
u"""
fk_chain：标准 FK Chain 构建组件。

适合 Ear、Finger、Tongue、Tail 等线性 FK 结构复用。

方法介绍与使用场景：

    FKChain.__init__
        初始化 FK Chain 的模块信息、Guide 数量和控制器显示设置。

    FKChain.get_guides
        获取当前 FK Chain 使用的 Guide 列表。
        可以使用外部传入的 Guide，也可以按照项目命名规则自动查找。

    FKChain.create_joints
        根据 Guide 创建 Joint，并将每个 Joint 对齐到对应 Guide。

    FKChain.create_ctrls
        根据 Guide 创建 FK Controller，并创建完整 Controller 层级。

    FKChain.connect_rig
        使用每个 Controller 的 Output Group 驱动对应 Joint。

    FKChain.setup_hierarchy
        整理 Joint Chain 和 FK Controller Chain。
        Controller 使用“上一个 Output -> 下一个 Zero”的 FK 层级。
"""

import maya.cmds as cmds

from .. import rig_module
from ...core.common import name_utils, hierarchy_utils
from ...core.rigging import jnt_utils, ctrl_utils


class FKChain(rig_module.RigModule):

    def __init__(
        self,
        module,
        side="md",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None,
        guide_count=1,
        jnt_function="bind",
        ctrl_function="fk",
        ctrl_shape="circle",
        ctrl_color=17,
        ctrl_size=1.0
    ):
        u"""
        初始化一个标准 FK Chain。

        module(str): 模块名称，例如 "ear"、"finger"、"tongue"。
        side(str): 模块方向，例如 "lf"、"rt"、"md"。
        guide(list/str/Guide): 可选 Guide 数据来源。
        jnt_parent(str/PyNode): Joint 总组的可选父节点。
        ctrl_parent(str/PyNode): Controller 总组的可选父节点。
        guide_count(int): 没有传入 Guide 时，根据命名规则查找的 Guide 数量。
        jnt_function(str): Joint 名称中的功能字段，默认 "bind"。
        ctrl_function(str): Controller 名称中的功能字段，默认 "fk"。
        ctrl_shape(str): Controller Shape 名称。
        ctrl_color(int): Controller 颜色索引。
        ctrl_size(float): Controller 显示大小。

        Maya 使用示例：

            from muziToolset.systems.components import fk_chain

            fk_object = fk_chain.FKChain(
                module="ear",
                side="lf",
                guide_count=3
            )

            fk_object.build()
        """

        super(FKChain, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

        self.guide_count = guide_count
        self.jnt_function = jnt_function
        self.ctrl_function = ctrl_function

        self.ctrl_shape = ctrl_shape
        self.ctrl_color = ctrl_color
        self.ctrl_size = ctrl_size

        self.guide_list = []
        self.jnt_list = []
        self.jnt_objects = []
        self.ctrl_list = []
        self.ctrl_objects = []

        self.jnt_master_grp = None
        self.ctrl_master_grp = None

    def get_guides(self):
        u"""
        获取当前 FK Chain 使用的 Guide 列表。

        如果 self.guide 是 Guide 工具对象，则调用它的 get_guides()。
        如果传入的是列表或单个 Maya 节点，则直接使用。
        如果没有传入 Guide，则按照 loc_<side>_<module>_guide_<index> 自动查找。

        Returns:
            list: 按 FK 顺序排列的 Guide 名称列表。

        Maya 使用示例：

            from muziToolset.systems.components import fk_chain

            fk_object = fk_chain.FKChain("ear", "lf", guide_count=3)
            guide_list = fk_object.get_guides()

            print(guide_list)
        """

        self.guide_list = []
        source_guides = []

        if self.guide is not None and hasattr(self.guide, "get_guides"):
            result = self.guide.get_guides(self.module, self.side)
            if result:
                for guide_node in result:
                    source_guides.append(guide_node)

        elif isinstance(self.guide, (list, tuple)):
            for guide_node in self.guide:
                source_guides.append(guide_node)

        elif self.guide is not None:
            source_guides.append(self.guide)

        else:
            for index in range(1, self.guide_count + 1):
                guide_name_object = name_utils.Name(
                    type="loc",
                    side=self.side,
                    part=self.module,
                    function="guide",
                    index=index
                )
                source_guides.append(guide_name_object.name)

        for guide_node in source_guides:
            guide_name = str(guide_node)

            if not cmds.objExists(guide_name):
                raise RuntimeError(u"找不到 FK Guide：{}".format(guide_name))

            self.guide_list.append(guide_name)

        if not self.guide_list:
            raise RuntimeError(u"{} 没有可用的 FK Guide。".format(self.module))

        return self.guide_list

    def create_joints(self):
        u"""
        根据 Guide 创建 Joint Chain 所需的 Joint。

        每一个 Joint 名称由 name_utils.Name 创建，随后使用 Jnt 对象获取或创建 Joint，
        并匹配对应 Guide 的位置和旋转。

        Returns:
            list: 当前 FK Chain 的 Joint 名称列表。

        Maya 使用示例：

            fk_object.create_joints()
            print(fk_object.jnt_list)
        """

        self.jnt_list = []
        self.jnt_objects = []

        for index, guide_name in enumerate(self.guide_list, 1):
            jnt_name_object = name_utils.Name(
                type="jnt",
                side=self.side,
                part=self.module,
                function=self.jnt_function,
                index=index
            )

            jnt_object = jnt_utils.Jnt(jnt_name_object.name)
            jnt_object.set_match_transform(guide_name)

            self.jnt_list.append(jnt_name_object.name)
            self.jnt_objects.append(jnt_object)

        return self.jnt_list

    def create_ctrls(self):
        u"""
        根据 Guide 创建 FK Controller。

        每个 Controller 都会创建完整的 Zero / Driven / Space / Connect / Offset / Ctrl /
        SubCtrl / Output 层级，并匹配对应 Guide。

        Returns:
            list: 当前 FK Chain 的 Controller 名称列表。

        Maya 使用示例：

            fk_object.create_ctrls()
            print(fk_object.ctrl_list)
        """

        self.ctrl_list = []
        self.ctrl_objects = []

        for index, guide_name in enumerate(self.guide_list, 1):
            ctrl_name_object = name_utils.Name(
                type="ctrl",
                side=self.side,
                part=self.module,
                function=self.ctrl_function,
                index=index
            )

            ctrl_object = ctrl_utils.Ctrl(ctrl_name_object.name)
            ctrl_object.create_ctrl(
                shape_name=self.ctrl_shape,
                ctrl_color=self.ctrl_color,
                ctrl_size=self.ctrl_size,
                create_hierarchy=True,
                match_transform_target=guide_name
            )

            self.ctrl_list.append(ctrl_name_object.name)
            self.ctrl_objects.append(ctrl_object)

        return self.ctrl_list

    def connect_rig(self):
        u"""
        将每个 Controller 的 Output Group 连接到对应 Joint。

        Output 是 Controller 层级的最终输出节点，因此主 Ctrl 和 SubCtrl 的变化都会传递到 Joint。

        Returns:
            None

        Maya 使用示例：

            fk_object.connect_rig()
        """

        for index in range(len(self.jnt_objects)):
            jnt_object = self.jnt_objects[index]
            ctrl_object = self.ctrl_objects[index]

            cmds.parentConstraint(
                str(ctrl_object.output_grp),
                str(jnt_object.jnt),
                maintainOffset=True
            )

    def setup_hierarchy(self):
        u"""
        整理 Joint Chain 和 FK Controller Chain。

        Joint 层级：
            jnt_master_grp -> jnt_001 -> jnt_002 -> jnt_003 ...

        Controller 层级：
            ctrl_master_grp -> zero_001
            output_001 -> zero_002
            output_002 -> zero_003
            ...

        Returns:
            None

        Maya 使用示例：

            fk_object.setup_hierarchy()
        """

        jnt_group_name = name_utils.Name(
            type="grp",
            side=self.side,
            part=self.module,
            function="jnt",
            index=1
        ).name

        ctrl_group_name = name_utils.Name(
            type="grp",
            side=self.side,
            part=self.module,
            function="ctrl",
            index=1
        ).name

        self.jnt_master_grp = self._get_or_create_group(jnt_group_name)
        self.ctrl_master_grp = self._get_or_create_group(ctrl_group_name)

        if self.jnt_parent:
            hierarchy_utils.parent(self.jnt_master_grp, self.jnt_parent)

        if self.ctrl_parent:
            hierarchy_utils.parent(self.ctrl_master_grp, self.ctrl_parent)

        if self.jnt_list:
            hierarchy_utils.chain_parent(
                self.jnt_list,
                parent_node=self.jnt_master_grp
            )

        if self.ctrl_objects:
            first_ctrl_object = self.ctrl_objects[0]
            hierarchy_utils.parent(
                first_ctrl_object.zero_grp,
                self.ctrl_master_grp
            )

            for index in range(1, len(self.ctrl_objects)):
                parent_ctrl_object = self.ctrl_objects[index - 1]
                child_ctrl_object = self.ctrl_objects[index]

                hierarchy_utils.parent(
                    child_ctrl_object.zero_grp,
                    parent_ctrl_object.output_grp
                )

    def _get_or_create_group(self, group_name):
        u"""
        获取或创建 FK Chain 使用的总 Group。

        group_name(str): 需要获取或创建的 Transform Group 名称。

        Returns:
            str: Group 名称。

        Maya 使用示例：

            group = fk_object._get_or_create_group("grp_lf_ear_ctrl_001")
            print(group)
        """

        if cmds.objExists(group_name):
            if cmds.nodeType(group_name) != "transform":
                raise TypeError(u"{} 已经存在，但不是 Transform 节点。".format(group_name))

            return group_name

        return cmds.group(empty=True, name=group_name)
