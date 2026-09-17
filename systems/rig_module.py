# coding=utf-8
u"""
RigModule：通用绑定模块基础类。

这里只保留绑定模块真正共用的能力：
    1. 读取 Guide。
    2. 创建单个 Joint。
    3. 创建单个 Controller。
    4. 创建模块 Joint / Ctrl 根组。
    5. build_rig() 创建绑定输出。
    6. connect_rig() 由子类建立驱动。
    7. delete_rig() 删除当前模块生成结果。

具体 Eye / Ear / Tongue 的 Joint 数量、Controller 数量和连接方式由子类决定。
"""

import maya.cmds as cmds

from ..core.common import name_utils, hierarchy_utils
from ..core.rigging import jnt_utils, ctrl_utils


class RigModule(object):
    u"""所有正式 Rig Module 共用的最小基础类。"""

    def __init__(
        self,
        module=None,
        side="md",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None
    ):
        self.module = module
        self.side = side
        self.guide = guide
        self.jnt_parent = jnt_parent
        self.ctrl_parent = ctrl_parent

        self.guide_list = []
        self.jnt_master_grp = None
        self.ctrl_master_grp = None

    def get_guides(self):
        u"""把传入 Guide 整理为有序节点列表，并检查节点是否存在。"""

        self.guide_list = []

        if self.guide is None:
            return self.guide_list

        source_guides = []

        if hasattr(self.guide, "get_guides"):
            result = self.guide.get_guides(
                self.module,
                self.side
            )

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
                raise RuntimeError(
                    u"找不到 Guide：{}".format(guide_name)
                )

            self.guide_list.append(guide_name)

        return self.guide_list

    def create_joint(self, name, guide=None):
        u"""创建一个 Joint，并可选匹配到 Guide。"""

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
        ctrl_axis="X+",
        create_hierarchy=True
    ):
        u"""创建一个标准 Controller，并可选匹配到 Guide。"""

        ctrl_object = ctrl_utils.Ctrl(name)

        ctrl_object.create_ctrl(
            shape_name=shape_name,
            ctrl_color=ctrl_color,
            ctrl_size=ctrl_size,
            ctrl_axis=ctrl_axis,
            create_hierarchy=create_hierarchy,
            match_transform_target=guide
        )

        return ctrl_object

    def create_joints(self):
        u"""由子类创建当前模块需要的 Joint。"""

        pass

    def create_ctrls(self):
        u"""由子类创建当前模块需要的 Controller。"""

        pass

    def setup_hierarchy(self):
        u"""创建当前模块的 Joint / Controller 根组。"""

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

    def build_rig(self):
        u"""创建 Guide、Joint、Controller 和模块层级，不建立最终驱动。"""

        self.get_guides()
        self.create_joints()
        self.create_ctrls()
        self.setup_hierarchy()

    def connect_rig(self):
        u"""由子类建立当前模块的最终驱动连接。"""

        pass

    def delete_rig(self):
        u"""删除当前模块的 Joint / Controller 根组及其全部子节点。"""

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

        delete_nodes = []

        if cmds.objExists(ctrl_group_name):
            delete_nodes.append(ctrl_group_name)

        if cmds.objExists(jnt_group_name):
            delete_nodes.append(jnt_group_name)

        if delete_nodes:
            cmds.delete(delete_nodes)

        self.jnt_master_grp = None
        self.ctrl_master_grp = None

        return delete_nodes
