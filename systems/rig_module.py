# coding=utf-8
u"""
RigModule：通用绑定模块基础类。

这个类只负责所有绑定模块都会重复使用的基础能力，不包含任何具体部位的绑定算法。

主要职责：
    1. 保存 Module 的基础参数。
    2. 接收已经确定好的 Guide 名称。
    3. 创建单个 Joint。
    4. 创建单个 Controller。
    5. 创建当前 Module 的 Joint / Controller 总组。
    6. 提供 build_rig() / connect_rig() / delete_rig() 三个统一生命周期入口。

设计原则：
    - Guide 的创建、模板导入、镜像和默认位置以后统一由 Guide Template 系统负责。
    - RigModule 不负责在场景里搜索、猜测或生成 Guide，只使用外部已经准备好的 Guide。
    - Eye / Ear / Tongue 等模块需要多少 Joint，由具体子类自己决定。
    - Constraint / Matrix / Deformer 等连接方式，由具体子类自己决定。
    - RigModule 只保留真正能够复用的底层流程，避免把模板、UI、业务逻辑混在一起。
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
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

                Args:
                    module (object):
                        `module` 对应的输入数据。
                    side (str):
                        方向标记，常用值为 lf、rt 或 md。
                    guide (str):
                        需要查询或处理的 Guide Transform 名称。
                    jnt_parent (object):
                        `jnt_parent` 对应的输入数据。
                    ctrl_parent (object):
                        `ctrl_parent` 对应的输入数据。
                
        """

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

        # ---------------------------------------------------------------------
        # 保存当前 Module 真正使用的 Guide 顺序。
        # Guide Template 导入完成后，会把已经确定好的 Locator 名称传进来。
        # 这里不负责寻找 Locator，只保存最终使用结果。
        # ---------------------------------------------------------------------
        self.guide_list = []

    def get_guides(self):
        u"""
        读取当前 Module 已经确定好的 Guide 名称。

        以后 Guide 的来源会统一改成 Maya Guide Template，例如：
            eye_guide.ma
            brow_guide.ma
            mouth_guide.ma
        Template 系统负责：
            1. 导入对应的 Maya 模板文件。
            2. 创建或恢复模板里的 Locator。
            3. 处理 Locator 的默认位置、镜像和模板结构。
            4. 把当前 Module 需要使用的 Locator 名称传给 Rig Module。
        因此 RigModule 不再需要：
            - 根据 module / side 自动搜索 Guide；
            - 调用额外的 Guide Provider 对象；
            - 猜测当前场景中哪些 Locator 属于这个 Module。
        这个方法现在只做两件事情：
            1. 把传进来的 Guide 名称整理成统一的列表格式。
            2. 在真正开始 Build 前检查这些 Maya 节点是否存在。

        Returns:
            list[str]:
            当前 Module 按绑定顺序使用的 Guide 名称列表。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """

        # ---------------------------------------------------------------------
        # 每次执行 build_rig() 时都会重新调用 get_guides()。
        # 所以先清空上一次保存的结果，避免重复 Build 时出现旧数据残留。
        # ---------------------------------------------------------------------
        self.guide_list = []

        # ---------------------------------------------------------------------
        # 如果当前没有传入 Guide，就直接返回空列表。
        # 是否允许没有 Guide，由具体业务模块自己决定。
        # 例如 EyeModule 会在 create_joints() 中明确检查是否有 3 个 Guide。
        # ---------------------------------------------------------------------
        if self.guide is None:
            return self.guide_list

        # ---------------------------------------------------------------------
        # Guide Template 通常会直接传入一个已经排好顺序的 list / tuple。
        # 这里严格保留这个顺序，因为 Joint / Controller 的创建顺序会直接依赖它。
        #
        # 例如 Eye：
        #     [0] Ball
        #     [1] Iris
        #     [2] Aim
        # ---------------------------------------------------------------------
        if isinstance(self.guide, (list, tuple)):
            for guide_name in self.guide:
                self.guide_list.append(str(guide_name))
        else:
            # 只有一个 Guide 的模块也允许直接传入单个 Locator 名称。
            self.guide_list.append(str(self.guide))

        # ---------------------------------------------------------------------
        # RigModule 不负责“寻找”Guide，但仍然需要做最基础的安全检查。
        # 如果模板传进来的 Locator 名称不存在，就立即停止 Build。
        # 这样错误会发生在最前面，而不是等到创建 Joint / Controller 时才报错。
        # ---------------------------------------------------------------------
        for guide_name in self.guide_list:
            if not cmds.objExists(guide_name):
                raise RuntimeError(u"找不到 Guide：{}".format(guide_name))

        return self.guide_list

    def create_joint(self, name, guide=None):
        u"""

                创建一个 Joint，并根据需要匹配到指定 Guide。

                这里只负责单个 Joint 的创建。
                Joint 数量、父子关系和业务命名仍由具体子类控制。

                Args:
                    name (str):
                        创建或查询时使用的节点名称。
                    guide (str):
                        需要查询或处理的 Guide Transform 名称。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。
                
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

                Args:
                    name (str):
                        创建或查询时使用的节点名称。
                    guide (str):
                        需要查询或处理的 Guide Transform 名称。
                    shape_name (str):
                        `shape_name` 对应的 Maya 节点或资源名称。
                    ctrl_color (int):
                        `ctrl_color` 对应的整数参数。
                    ctrl_size (float):
                        `ctrl_size` 对应的数值参数。
                    ctrl_axis (str):
                        `ctrl_axis` 对应的名称、标记或字符串参数。
                    create_hierarchy (bool):
                        是否启用 `create_hierarchy` 对应的处理。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。
                
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

                Returns:
                    tuple:
                        按当前 API 约定组织的结果元组。
                
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

        # 先取得并验证外部已经准备好的 Guide。
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

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。
                
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
