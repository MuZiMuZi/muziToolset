# coding=utf-8
u"""
fk_chain：标准 FK Chain 构建组件。

适合 Ear、Finger、Tongue、Tail 等线性 FK 结构复用。

方法介绍与使用场景：

    FKChain.__init__
        初始化 FK Chain 的模块信息、Guide 数量和控制器 Shape、颜色、大小、轴向设置。

    FKChain.get_guides
        优先复用 RigModule.get_guides() 获取外部传入的 Guide。
        没有传入 Guide 时，再按照 FK Chain 命名规则自动查找。

    FKChain.create_joints
        根据 Guide 创建 Joint Chain。
        单个 Joint 创建统一复用 RigModule.create_joint()。

    FKChain.create_ctrls
        根据 Guide 创建 FK Controller Chain。
        单个 Controller 创建统一复用 RigModule.create_ctrl()。

    FKChain.connect_rig
        使用每个 Controller 的 Output Group 驱动对应 Joint。
        重复构建时会复用已经存在且 Driver 正确的 parentConstraint。

    FKChain.setup_hierarchy
        先复用 RigModule.setup_hierarchy() 创建模块总组，
        再整理 FK 专属 Joint Chain 和“上一个 Output -> 下一个 Zero”的 Controller Chain。
"""

import maya.cmds as cmds

from .. import rig_module
from ...core.common import name_utils, hierarchy_utils


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
        ctrl_size=1.0,
        ctrl_axis="X+"
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
        ctrl_axis(str): Controller Shape 面朝方向，支持 X+ / X- / Y+ / Y- / Z+ / Z-。

        Maya 使用示例：

            from muziToolset.systems.components import fk_chain

            fk_object = fk_chain.FKChain(
                module="ear",
                side="lf",
                guide_count=3,
                ctrl_axis="Z+"
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
        self.ctrl_axis = ctrl_axis

        self.jnt_list = []
        self.jnt_objects = []
        self.ctrl_list = []
        self.ctrl_objects = []

    def get_guides(self):
        u"""
        获取当前 FK Chain 使用的 Guide 列表。

        优先调用 RigModule.get_guides() 处理外部明确传入的 Guide 数据。
        如果没有传入 Guide，则 FK Chain 再按照：
            loc_<side>_<module>_guide_<index>
        自动查找线性 Chain 使用的 Guide。

        Returns:
            list: 按 FK 顺序排列的 Guide 名称列表。

        Maya 使用示例：

            from muziToolset.systems.components import fk_chain

            fk_object = fk_chain.FKChain(
                module="ear",
                side="lf",
                guide_count=3
            )

            guide_list = fk_object.get_guides()
            print(guide_list)
        """

        self.guide_list = super(FKChain, self).get_guides()

        # 外部已经明确提供 Guide 时，直接使用 RigModule 的通用读取结果。
        if self.guide_list:
            return self.guide_list

        # 明确传入了 Guide 数据但没有找到结果时，不再猜测名称。
        if self.guide is not None:
            raise RuntimeError(u"{} 没有可用的 FK Guide。".format(self.module))

        # 没有传入 Guide 时，才使用 FK Chain 自己的线性命名规则。
        for index in range(1, self.guide_count + 1):
            guide_name_object = name_utils.Name(
                type="loc",
                side=self.side,
                part=self.module,
                function="guide",
                index=index
            )

            guide_name = guide_name_object.name

            if not cmds.objExists(guide_name):
                raise RuntimeError(u"找不到 FK Guide：{}".format(guide_name))

            self.guide_list.append(guide_name)

        if not self.guide_list:
            raise RuntimeError(u"{} 没有可用的 FK Guide。".format(self.module))

        return self.guide_list

    def create_joints(self):
        u"""
        根据 Guide 创建当前 FK Joint Chain 所需的 Joint。

        FKChain 只负责决定“一条 Guide 对应一条 Joint Chain”的整体规则，
        单个 Joint 的创建和 Guide 匹配统一交给 RigModule.create_joint()。

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

            jnt_object = self.create_joint(
                name=jnt_name_object.name,
                guide=guide_name
            )

            self.jnt_list.append(jnt_name_object.name)
            self.jnt_objects.append(jnt_object)

        return self.jnt_list

    def create_ctrls(self):
        u"""
        根据 Guide 创建当前 FK Controller Chain。

        FKChain 只负责决定“一条 Guide 对应一组 FK Controller”的整体规则，
        单个 Controller 的 Shape、颜色、大小、轴向、层级和 Guide 匹配统一交给
        RigModule.create_ctrl()。

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

            ctrl_object = self.create_ctrl(
                name=ctrl_name_object.name,
                guide=guide_name,
                shape_name=self.ctrl_shape,
                ctrl_color=self.ctrl_color,
                ctrl_size=self.ctrl_size,
                ctrl_axis=self.ctrl_axis,
                create_hierarchy=True
            )

            self.ctrl_list.append(ctrl_name_object.name)
            self.ctrl_objects.append(ctrl_object)

        return self.ctrl_list

    def connect_rig(self):
        u"""
        将每个 Controller 的 Output Group 连接到对应 Joint。

        Output 是 Controller 层级的最终输出节点，因此主 Ctrl 和 SubCtrl 的变化都会传递到 Joint。

        重复执行时会先检查 Joint 当前连接的 parentConstraint：
            1. 已经存在由当前 Output 驱动的 parentConstraint，则直接复用，不重复创建。
            2. Joint 已经存在其他 parentConstraint，但没有当前 Output Driver，则抛出错误，
               避免新的 Constraint 覆盖或污染已有绑定关系。
            3. 没有 parentConstraint 时才创建新的 Constraint。

        Returns:
            None

        Maya 使用示例：

            fk_object.connect_rig()
            fk_object.connect_rig()
        """

        for index in range(len(self.jnt_objects)):
            jnt_object = self.jnt_objects[index]
            ctrl_object = self.ctrl_objects[index]

            driver = str(ctrl_object.output_grp)
            driven = str(jnt_object.jnt)

            # 获取当前 Joint 已经存在的 Parent Constraint。
            constraint_nodes = cmds.listConnections(
                driven,
                source=True,
                destination=False,
                type="parentConstraint"
            )

            if constraint_nodes is None:
                constraint_nodes = []

            # 统一获取 Driver 的 Long Name，避免短名称和完整 DAG 路径比较不一致。
            driver_long_names = cmds.ls(
                driver,
                long=True
            )

            if driver_long_names:
                driver_long_name = driver_long_names[0]
            else:
                driver_long_name = driver

            matched_constraint = None

            # 检查已有 Constraint 是否已经包含当前 Output Driver。
            for constraint_node in constraint_nodes:
                target_list = cmds.parentConstraint(
                    constraint_node,
                    query=True,
                    targetList=True
                )

                if target_list is None:
                    target_list = []

                for target in target_list:
                    target_long_names = cmds.ls(
                        target,
                        long=True
                    )

                    if target_long_names:
                        target_long_name = target_long_names[0]
                    else:
                        target_long_name = target

                    if target_long_name == driver_long_name:
                        matched_constraint = constraint_node
                        break

                if matched_constraint:
                    break

            # 已经存在正确 Driver 的 Constraint 时直接复用。
            if matched_constraint:
                continue

            # Joint 上已经有其他 Parent Constraint 时，不静默覆盖已有绑定关系。
            if constraint_nodes:
                raise RuntimeError(
                    u"{} 已经存在 Parent Constraint，但 Driver 不是 {}。".format(
                        driven,
                        driver
                    )
                )

            # 没有 Parent Constraint 时才真正创建驱动关系。
            cmds.parentConstraint(
                driver,
                driven,
                maintainOffset=True
            )

    def setup_hierarchy(self):
        u"""
        整理当前 FK Chain 的模块总组和内部 FK 层级。

        RigModule.setup_hierarchy() 负责：
            jnt_parent -> jnt_master_grp
            ctrl_parent -> ctrl_master_grp

        FKChain 在此基础上继续负责：
            jnt_master_grp -> jnt_001 -> jnt_002 -> jnt_003 ...

            ctrl_master_grp -> zero_001
            output_001 -> zero_002
            output_002 -> zero_003
            ...

        Returns:
            None

        Maya 使用示例：

            fk_object.setup_hierarchy()
        """

        # 先建立所有 Rig Module 都共有的 Joint / Controller 根层级。
        super(FKChain, self).setup_hierarchy()

        # FK Joint 按顺序组成 Joint Chain。
        if self.jnt_list:
            hierarchy_utils.chain_parent(
                self.jnt_list,
                parent_node=self.jnt_master_grp
            )

        # 第一个 Controller 的 Zero 放到模块 Controller 总组下面。
        if self.ctrl_objects:
            first_ctrl_object = self.ctrl_objects[0]

            hierarchy_utils.parent(
                first_ctrl_object.zero_grp,
                self.ctrl_master_grp
            )

            # 后续 Controller 使用“上一个 Output -> 下一个 Zero”的 FK 层级。
            for index in range(1, len(self.ctrl_objects)):
                parent_ctrl_object = self.ctrl_objects[index - 1]
                child_ctrl_object = self.ctrl_objects[index]

                hierarchy_utils.parent(
                    child_ctrl_object.zero_grp,
                    parent_ctrl_object.output_grp
                )
