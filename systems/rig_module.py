# coding=utf-8
u"""
rig_module：Rig Module 基础类。

负责保存所有 Rig Module 共用的数据，并提供模块级公共构建能力。

方法介绍与使用场景：

    RigModule.__init__
        保存模块名称、方向、Guide、Joint Parent 和 Controller Parent。

    RigModule.get_guides
        从外部传入的 Guide 数据中获取当前模块使用的 Guide。
        只负责通用 Guide 读取，不负责按照特定模块规则猜测 Guide 名称。

    RigModule.create_joint
        创建或获取单个 Joint，并可以将它匹配到指定 Guide。

    RigModule.create_ctrl
        创建或获取单个 Controller，并完成 Shape、颜色、大小、层级和 Guide 匹配。

    RigModule.create_joints
        预留给子类定义整个 Joint System 的创建规则。

    RigModule.create_ctrls
        预留给子类定义整个 Controller System 的创建规则。

    RigModule.connect_rig
        预留给子类定义 Controller、Joint、Deformer 等驱动连接方式。

    RigModule.setup_hierarchy
        创建模块自己的 Joint / Controller 总组，并挂到 jnt_parent / ctrl_parent。

    RigModule.build
        按统一生命周期执行完整模块构建。
"""

import maya.cmds as cmds

from ..core.common import name_utils, hierarchy_utils
from ..core.rigging import jnt_utils, ctrl_utils


class RigModule(object):

    def __init__(self, module=None, side="md", guide=None, jnt_parent=None, ctrl_parent=None):
        u"""
        初始化 Rig Module 基础数据。

        module(str): 模块名称，例如 "ear"、"eye"、"brow"。
        side(str): 模块方向，例如 "lf"、"rt"、"md"。
        guide(list/str/Guide): 当前模块使用的 Guide 数据来源。
        jnt_parent(str/PyNode): 当前模块 Joint 总组需要挂载的父节点。
        ctrl_parent(str/PyNode): 当前模块 Controller 总组需要挂载的父节点。

        Maya 使用示例：

            from muziToolset.systems import rig_module

            module_object = rig_module.RigModule(
                module="ear",
                side="lf"
            )
        """

        self.module = module
        self.side = side
        self.guide = guide
        self.jnt_parent = jnt_parent
        self.ctrl_parent = ctrl_parent

        self.guide_list = []
        self.jnt_master_grp = None
        self.ctrl_master_grp = None

    def get_guides(self):
        u"""
        获取当前 Rig Module 使用的 Guide。

        默认实现只处理外部明确传入的 Guide 数据：
            1. Guide 工具对象：调用 get_guides(module, side)。
            2. list / tuple：直接按照传入顺序使用。
            3. 单个 Maya 节点：作为只有一个 Guide 的列表使用。

        如果没有传入 Guide，则返回空列表。
        具体 Component 如果拥有额外的 Guide 查找规则，可以在子类中继续扩展。

        Returns:
            list: 当前模块使用的 Guide 名称列表。

        Maya 使用示例：

            guide_list = module_object.get_guides()
            print(guide_list)
        """

        self.guide_list = []
        source_guides = []

        if self.guide is None:
            return self.guide_list

        if hasattr(self.guide, "get_guides"):
            result = self.guide.get_guides(self.module, self.side)

            if result:
                for guide_node in result:
                    source_guides.append(guide_node)

        elif isinstance(self.guide, (list, tuple)):
            for guide_node in self.guide:
                source_guides.append(guide_node)

        else:
            source_guides.append(self.guide)

        for guide_node in source_guides:
            guide_name = str(guide_node)

            if not cmds.objExists(guide_name):
                raise RuntimeError(u"找不到 Guide：{}".format(guide_name))

            self.guide_list.append(guide_name)

        return self.guide_list

    def create_joint(self, name, guide=None):
        u"""
        创建或获取单个 Joint，并可以匹配到指定 Guide。

        该方法只负责一个 Joint 的基础创建，不决定整个模块的 Joint 数量和拓扑结构。
        Joint Chain、分叉 Joint、Driver Joint 等整体结构由具体子类的 create_joints() 决定。

        name(str): Joint 名称。
        guide(str/PyNode): 可选匹配目标。

        Returns:
            Jnt: 创建或获取到的 Jnt 工具对象。

        Maya 使用示例：

            jnt_object = module_object.create_joint(
                "jnt_lf_ear_bind_001",
                guide="loc_lf_ear_guide_001"
            )

            print(jnt_object.jnt)
        """

        jnt_object = jnt_utils.Jnt(name)

        if guide:
            jnt_object.set_match_transform(guide)

        return jnt_object

    def create_ctrl(
        self,
        name,
        guide=None,
        shape_name="circle",
        ctrl_color=17,
        ctrl_size=1.0,
        create_hierarchy=True
    ):
        u"""
        创建或获取单个 Controller，并完成基础设置。

        该方法只负责一个 Controller 的创建。
        FK、Aim、IK、Face 等整个控制器系统的数量和连接方式由具体子类决定。

        name(str): Controller 名称。
        guide(str/PyNode): 可选匹配目标。
        shape_name(str): Controller Shape 名称，默认 "circle"。
        ctrl_color(int): Controller 颜色索引，默认 17。
        ctrl_size(float): Controller 显示大小，默认 1.0。
        create_hierarchy(bool): 是否创建完整 Controller 层级，默认 True。

        Returns:
            Ctrl: 创建或获取到的 Ctrl 工具对象。

        Maya 使用示例：

            ctrl_object = module_object.create_ctrl(
                "ctrl_lf_ear_fk_001",
                guide="loc_lf_ear_guide_001",
                shape_name="circle",
                ctrl_color=17,
                ctrl_size=1.0
            )

            print(ctrl_object.ctrl)
        """

        ctrl_object = ctrl_utils.Ctrl(name)
        ctrl_object.create_ctrl(
            shape_name=shape_name,
            ctrl_color=ctrl_color,
            ctrl_size=ctrl_size,
            create_hierarchy=create_hierarchy,
            match_transform_target=guide
        )

        return ctrl_object

    def create_joints(self):
        u"""
        创建当前模块完整 Joint System。

        具体 Joint 数量和拓扑结构由子类实现。

        Maya 使用示例：

            module_object.create_joints()
        """

        pass

    def create_ctrls(self):
        u"""
        创建当前模块完整 Controller System。

        具体 Controller 数量和结构由子类实现。

        Maya 使用示例：

            module_object.create_ctrls()
        """

        pass

    def connect_rig(self):
        u"""
        建立当前模块的绑定驱动连接。

        不同模块可能使用 Constraint、Matrix、Utility Node 或 Deformer，
        因此具体连接方式由子类实现。

        Maya 使用示例：

            module_object.connect_rig()
        """

        pass

    def setup_hierarchy(self):
        u"""
        创建并整理当前 Rig Module 的基础总组层级。

        每个模块统一拥有：
            grp_<side>_<module>_jnt_001
            grp_<side>_<module>_ctrl_001

        如果传入 jnt_parent / ctrl_parent，则分别将两个总组挂到对应父节点。
        该方法只负责模块根层级，不决定 Joint Chain 或 Controller Chain 的内部拓扑。

        Returns:
            tuple: (jnt_master_grp, ctrl_master_grp)

        Maya 使用示例：

            jnt_grp, ctrl_grp = module_object.setup_hierarchy()

            print(jnt_grp)
            print(ctrl_grp)
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

        self.jnt_master_grp = hierarchy_utils.get_or_create_group(
            jnt_group_name
        )
        self.ctrl_master_grp = hierarchy_utils.get_or_create_group(
            ctrl_group_name
        )

        if self.jnt_parent:
            hierarchy_utils.parent(
                self.jnt_master_grp,
                self.jnt_parent
            )

        if self.ctrl_parent:
            hierarchy_utils.parent(
                self.ctrl_master_grp,
                self.ctrl_parent
            )

        return self.jnt_master_grp, self.ctrl_master_grp

    def build(self):
        u"""
        按照统一生命周期构建当前 Rig Module。

        执行顺序：
            1. get_guides()
            2. create_joints()
            3. create_ctrls()
            4. connect_rig()
            5. setup_hierarchy()

        Maya 使用示例：

            module_object.build()
        """

        self.get_guides()
        self.create_joints()
        self.create_ctrls()
        self.connect_rig()
        self.setup_hierarchy()
