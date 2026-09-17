# coding=utf-8
u"""
RigModule：通用绑定模块基础类。

这个类只负责所有绑定模块都会重复使用的基础能力，不包含任何具体部位的绑定算法。

主要职责：
    1. 保存 Module 的基础参数。
    2. 读取并验证 Guide。
    3. 创建单个 Joint。
    4. 创建单个 Controller。
    5. 创建当前 Module 的 Joint / Controller 根组。
    6. 提供 build_rig() / connect_rig() / delete_rig() 三个统一生命周期入口。

设计原则：
    - Eye / Ear / Tongue 等模块需要多少 Joint，由子类自己决定。
    - Constraint / Matrix / Deformer 等连接方式，由子类自己决定。
    - RigModule 只保留真正能够复用的底层流程。
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
        # ---------------------------------------------------------------------
        # 保存当前 Module 最基础的数据。
        # 这些参数会贯穿 build / connect / delete 整个生命周期。
        # ---------------------------------------------------------------------
        self.module = module
        self.side = side
        self.guide = guide
        self.jnt_parent = jnt_parent
        self.ctrl_parent = ctrl_parent

        # ---------------------------------------------------------------------
        # 当前 Module 只保留两个总组变量。
        # 变量本身直接保存标准 Maya 节点名称，不再额外保存 *_group_name。
        # setup_hierarchy()、子类整理层级和 delete_rig() 全部复用同一个名称。
        # ---------------------------------------------------------------------
        self.jnt_master_grp = name_utils.Name(type="grp", side=self.side, part=self.module, function="jnt", index=1).name
        self.ctrl_master_grp = name_utils.Name(type="grp", side=self.side, part=self.module, function="ctrl", index=1).name

        # 保存整理后的 Guide 顺序。
        self.guide_list = []

    def get_guides(self):
        u"""
        把外部传入的 Guide 整理成有序列表，并确认 Maya 场景中节点真实存在。

        支持三种输入方式：
            1. Guide 对象：对象本身提供 get_guides(module, side)。
            2. list / tuple：直接按照传入顺序使用。
            3. 单个节点：自动包装成只有一个元素的列表。

        Returns:
            list[str]:
                已经验证存在的 Guide 名称列表。
        """

        # 每次读取 Guide 前先清空旧结果，避免重复 build 时残留上一次的数据。
        self.guide_list = []

        # 没有传 Guide 时直接返回空列表。
        # 某些子类可以自己覆盖 get_guides()，使用自己的查找规则。
        if self.guide is None:
            return self.guide_list

        # 先把不同输入类型统一整理到 source_guides 中。
        source_guides = []

        # Guide Provider 对象：让对象自己返回当前 module / side 对应的 Guide。
        if hasattr(self.guide, "get_guides"):
            result = self.guide.get_guides(
                self.module,
                self.side
            )

            if result:
                for guide_node in result:
                    source_guides.append(guide_node)

        # list / tuple：严格保留用户传入的顺序。
        elif isinstance(self.guide, (list, tuple)):
            for guide_node in self.guide:
                source_guides.append(guide_node)

        # 单个 Guide：包装成一个元素。
        else:
            source_guides.append(self.guide)

        # 把所有 Guide 转换为 maya.cmds 可以直接使用的字符串名称，
        # 同时确认场景中确实存在对应节点。
        for guide_node in source_guides:
            guide_name = str(guide_node)

            if not cmds.objExists(guide_name):
                raise RuntimeError(
                    u"找不到 Guide：{}".format(guide_name)
                )

            self.guide_list.append(guide_name)

        return self.guide_list

    def create_joint(self, name, guide=None):
        u"""
        创建一个 Joint，并根据需要匹配到指定 Guide。

        这里只负责单个 Joint 的创建。
        Joint 数量、父子关系和业务命名仍由具体子类控制。
        """

        # Jnt 工具负责真正创建或读取 Maya Joint。
        jnt_object = jnt_utils.Jnt(name)

        # 如果提供 Guide，就把 Joint 的 Transform 对齐到 Guide。
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
        u"""
        创建一个标准 Controller，并根据需要匹配到指定 Guide。

        Controller Shape、颜色、大小、轴向和标准层级全部交给 Ctrl 工具处理。
        RigModule 这里只提供统一入口。
        """

        # 创建当前 Controller 工具对象。
        ctrl_object = ctrl_utils.Ctrl(name)

        # 创建 Curve、应用显示参数，并建立标准 Controller Hierarchy。
        # match_transform_target 负责把整个 Controller 系统对齐到 Guide。
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
        u"""
        创建当前业务模块需要的 Joint。

        基类不知道具体模块需要几个 Joint，所以这里不实现具体逻辑。
        EyeModule、FKChain 等子类负责覆盖这个方法。
        """

        pass

    def create_ctrls(self):
        u"""
        创建当前业务模块需要的 Controller。

        基类不知道具体模块需要几个 Controller，所以这里不实现具体逻辑。
        """

        pass

    def setup_hierarchy(self):
        u"""
        创建当前 Module 的 Joint / Controller 总组，并挂到指定父组。

        self.jnt_master_grp 和 self.ctrl_master_grp 从初始化开始就保存标准组名，
        因此这里只负责确认 Maya 场景中对应组存在，不再创建第二套名称变量。

        标准结构：
            grp_<side>_<module>_jnt_001
            grp_<side>_<module>_ctrl_001
        """

        # 创建或读取当前 Module 的 Joint 总组。
        hierarchy_utils.get_or_create_group(self.jnt_master_grp)

        # 创建或读取当前 Module 的 Controller 总组。
        hierarchy_utils.get_or_create_group(self.ctrl_master_grp)

        # 如果外部指定了 Joint 总组，就把当前 Module Joint 组挂过去。
        if self.jnt_parent:
            hierarchy_utils.parent(
                self.jnt_master_grp,
                self.jnt_parent
            )

        # 如果外部指定了 Controller 总组，就把当前 Module Ctrl 组挂过去。
        if self.ctrl_parent:
            hierarchy_utils.parent(
                self.ctrl_master_grp,
                self.ctrl_parent
            )

        return self.jnt_master_grp, self.ctrl_master_grp

    def build_rig(self):
        u"""
        创建当前 Module 的绑定输出，但不建立最终驱动连接。

        固定执行顺序：
            1. 读取 Guide。
            2. 创建 Joint。
            3. 创建 Controller。
            4. 整理 Module Hierarchy。

        connect_rig() 单独执行，这样创建和连接可以分别测试。
        """

        # 先取得并验证所有 Guide。
        self.get_guides()

        # 根据 Guide 创建当前模块需要的 Joint。
        self.create_joints()

        # 根据 Guide 创建当前模块需要的 Controller。
        self.create_ctrls()

        # 所有节点创建完成后，再统一整理 DAG Hierarchy。
        self.setup_hierarchy()

    def connect_rig(self):
        u"""
        建立当前 Module 的最终驱动连接。

        具体使用 Constraint、Matrix、Utility Node 或其他方式，全部由子类决定。
        """

        pass

    def delete_rig(self):
        u"""
        删除当前 Module 的 Joint / Controller 总组及其全部子节点。

        具体模块如果还有 Constraint 或额外 DG Node，应在子类 delete_rig() 中
        先删除这些连接节点，然后再调用 super(...).delete_rig() 删除 DAG 输出。

        注意：
            self.jnt_master_grp / self.ctrl_master_grp 保存的是稳定节点名称，
            删除 Maya 节点后不会把这两个成员设为 None，这样同一个 Module 实例
            仍然可以再次执行 build_rig() 重建。
        """

        # 收集当前 Module 实际存在的两个总组。
        # 只删除存在的节点，保证重复调用 delete_rig() 不会报错。
        delete_nodes = []

        if cmds.objExists(self.ctrl_master_grp):
            delete_nodes.append(self.ctrl_master_grp)

        if cmds.objExists(self.jnt_master_grp):
            delete_nodes.append(self.jnt_master_grp)

        # Maya 删除父组时会一起删除组内所有 Joint / Controller 层级。
        if delete_nodes:
            cmds.delete(delete_nodes)

        return delete_nodes
