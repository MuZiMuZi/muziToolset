# coding=utf-8
u"""
FKChain：通用线性 FK 绑定模块。

适合：
    Ear、Tongue、Finger、Tail 等“多个 Guide -> 多个 Joint -> 多个 FK Controller”的结构。

核心流程：
    build_rig()
        Guide -> Joint
        Guide -> Controller
        Joint 组成链条
        Controller 组成 FK 层级

    connect_rig()
        Controller Output -> parentConstraint -> Joint

    delete_rig()
        删除当前 FK Chain 创建的 Constraint
        删除当前 FK Chain 的 Joint / Controller 总组

设计原则：
    1. Guide 从外部模板传入，FKChain 不负责自动猜测 Locator。
    2. FKChain 自己创建的节点名称在 __init__() 中一次生成。
    3. build / connect / delete 全部复用这些稳定名称。
    4. 不通过 listConnections() 反查自己创建的 Constraint。
    5. 动态数量的节点统一保存到名称列表中。
"""

import maya.cmds as cmds

from .. import rig_module
from ...core.common import name_utils, hierarchy_utils


class FKChain(rig_module.RigModule):
    u"""标准线性 FK Joint / Controller Chain。"""

    def __init__(
        self,
        module,
        side="md",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None,
        guide_count=1,
        guide_function="bind",
        jnt_function="bind",
        ctrl_function="fk",
        ctrl_shape="circle",
        ctrl_color=17,
        ctrl_size=1.0,
        ctrl_axis="X+"
    ):
        u"""
        初始化 FK Chain 的基础配置和全部稳定节点名称。

        Args:
            module (str):
                当前模块名称，例如 ear、tongue、finger。
            side (str):
                方向，例如 lf、rt、md。
            guide (list[str] | tuple[str] | str | None):
                外部 Guide Template 已经准备好的 Locator 名称。
            jnt_parent (str | None):
                当前模块 Joint 总组需要挂接的上层节点。
            ctrl_parent (str | None):
                当前模块 Controller 总组需要挂接的上层节点。
            guide_count (int):
                当前 FK Chain 预期的 Guide / Joint / Controller 数量。
            guide_function (str):
                Guide 的功能字段。当前主要用于记录模块配置。
            jnt_function (str):
                Joint 命名中的 function 字段。
            ctrl_function (str):
                Controller 命名中的 function 字段。
            ctrl_shape (str):
                Controller Shape 名称。
            ctrl_color (int):
                Controller Maya Index Color。
            ctrl_size (float):
                Controller Shape 大小。
            ctrl_axis (str):
                Controller Shape 轴向。
        """

        # ---------------------------------------------------------------------
        # 初始化 RigModule 的公共参数和模块总组名称。
        # ---------------------------------------------------------------------
        super(FKChain, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

        # ---------------------------------------------------------------------
        # 保存当前 FK Chain 的固定配置。
        # Guide 的实际节点名称由外部模板传入，这里只保存预期数量和命名字段。
        # ---------------------------------------------------------------------
        self.guide_count = guide_count
        self.guide_function = guide_function
        self.jnt_function = jnt_function
        self.ctrl_function = ctrl_function

        # Controller 外观配置。
        self.ctrl_shape = ctrl_shape
        self.ctrl_color = ctrl_color
        self.ctrl_size = ctrl_size
        self.ctrl_axis = ctrl_axis

        # ---------------------------------------------------------------------
        # 动态 Chain 使用名称列表保存所有稳定 Maya 节点。
        # 这些列表只在初始化时生成一次，后面不再重复计算 Naming。
        # ---------------------------------------------------------------------
        self.jnt_names = []
        self.ctrl_names = []
        self.output_names = []
        self.parent_constraint_names = []

        for index in range(1, self.guide_count + 1):
            jnt_name = name_utils.Name(type="jnt", side=self.side, part=self.module, function=self.jnt_function, index=index).name
            ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function=self.ctrl_function, index=index).name
            output_name = ctrl_name.replace("ctrl_", "output_", 1)
            constraint_name = name_utils.Name(type="parentConstraint", side=self.side, part=self.module, function=self.ctrl_function, index=index).name

            self.jnt_names.append(jnt_name)
            self.ctrl_names.append(ctrl_name)
            self.output_names.append(output_name)
            self.parent_constraint_names.append(constraint_name)

        # ---------------------------------------------------------------------
        # 创建阶段使用的工具对象。
        # 名称属于稳定数据，工具对象只属于当前 build_rig() 运行过程。
        # ---------------------------------------------------------------------
        self.jnt_objects = []
        self.ctrl_objects = []

    def get_guides(self):
        u"""
        读取外部传入的 Guide，并检查数量是否符合当前 FK Chain。

        FKChain 不再根据命名规则自动寻找 Locator。
        Guide Template 导入 Maya 文件后，应把已经确定好的 Locator 名称传给 guide。

        Returns:
            list[str]:
            按 FK 顺序排列的 Guide 名称。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """

        # RigModule 只负责把传入的 Guide 整理成字符串列表并检查节点是否存在。
        self.guide_list = super(FKChain, self).get_guides()

        # FK Chain 的 Guide 数量必须和初始化时声明的 guide_count 完全一致。
        # 数量不正确时直接停止，避免后面 Joint / Controller 对应关系错位。
        if len(self.guide_list) != self.guide_count:
            raise RuntimeError(
                u"{} 需要 {} 个 Guide，当前得到 {} 个。".format(
                    self.module,
                    self.guide_count,
                    len(self.guide_list)
                )
            )

        return self.guide_list

    def create_joints(self):
        u"""

                根据 Guide 顺序创建 FK Joint。

                一条 Guide 对应一个已经预先确定名称的 Joint：
                    guide[0] -> jnt_names[0]
                    guide[1] -> jnt_names[1]
                    ...

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。
                
        """

        # 重复 build 前先清空旧的 Python 工具对象引用。
        # jnt_names 不清空，因为它是当前模块的稳定节点名称。
        self.jnt_objects = []

        for index in range(len(self.guide_list)):
            jnt_object = self.create_joint(
                name=self.jnt_names[index],
                guide=self.guide_list[index]
            )

            self.jnt_objects.append(jnt_object)

        return self.jnt_names

    def create_ctrls(self):
        u"""

                根据 Guide 顺序创建 FK Controller。

                一条 Guide 对应一个已经预先确定名称的 Controller。
                Controller 的 Shape / Color / Size / Axis 统一使用当前 FKChain 配置。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。
                
        """

        # 重复 build 前先清空旧的 Python 工具对象引用。
        # ctrl_names / output_names 都是稳定名称，不需要重新生成。
        self.ctrl_objects = []

        for index in range(len(self.guide_list)):
            ctrl_object = self.create_ctrl(
                name=self.ctrl_names[index],
                guide=self.guide_list[index],
                shape_name=self.ctrl_shape,
                ctrl_color=self.ctrl_color,
                ctrl_size=self.ctrl_size,
                ctrl_axis=self.ctrl_axis,
                create_hierarchy=True
            )

            self.ctrl_objects.append(ctrl_object)

        return self.ctrl_names

    def setup_hierarchy(self):
        u"""

                整理 FK Joint Chain 和 Controller Chain。

                Joint：
                    jnt_master_grp
                        └─ jnt_001
                            └─ jnt_002
                                └─ jnt_003
                Controller：
                    ctrl_master_grp
                        └─ zero_001
                            ...
                            output_001
                                └─ zero_002
                                    ...
                                    output_002

                Returns:
                    tuple:
                        按当前 API 约定组织的结果元组。
                
        """

        # 先创建当前模块的 Joint / Controller 总组。
        super(FKChain, self).setup_hierarchy()

        # ---------------------------------------------------------------------
        # Joint 按名称列表顺序组成父子链。
        # 第一个 Joint 挂到当前模块 Joint 总组下面。
        # ---------------------------------------------------------------------
        if self.jnt_names:
            hierarchy_utils.chain_parent(
                self.jnt_names,
                parent_node=self.jnt_master_grp
            )

        # ---------------------------------------------------------------------
        # Controller 使用标准 FK 层级。
        # 第一个 Controller 的 zero 挂到模块总组；
        # 后面的 Controller zero 挂到上一个 Controller output 下。
        # ---------------------------------------------------------------------
        if self.ctrl_objects:
            hierarchy_utils.parent(
                self.ctrl_objects[0].zero_grp,
                self.ctrl_master_grp
            )

            for index in range(1, len(self.ctrl_objects)):
                hierarchy_utils.parent(
                    self.ctrl_objects[index].zero_grp,
                    self.ctrl_objects[index - 1].output_grp
                )

        return self.jnt_master_grp, self.ctrl_master_grp

    def connect_rig(self):
        u"""

                使用每个 Controller Output 的 Parent Constraint 驱动对应 Joint。

                所有 Driver、Driven 和 Constraint 名称都已经在 __init__() 中确定。
                因此这里不再使用 listConnections()、cmds.ls() 等方法反查自己创建的节点。
                重复执行 connect_rig() 时：
                    - 固定名称 Constraint 已存在：直接跳过。
                    - 固定名称 Constraint 不存在：创建。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                
        """

        for index in range(self.guide_count):
            driver = self.output_names[index]
            driven = self.jnt_names[index]
            constraint_name = self.parent_constraint_names[index]

            # 创建连接前确认真正参与连接的 DAG 节点存在。
            if not cmds.objExists(driver):
                raise RuntimeError(u"FK Controller Output 不存在：{}".format(driver))

            if not cmds.objExists(driven):
                raise RuntimeError(u"FK Joint 不存在：{}".format(driven))

            # 当前模块自己的 Constraint 已经存在时直接复用，不重复创建。
            if cmds.objExists(constraint_name):
                continue

            # Controller Output 负责把最终动画结果传给对应 Joint。
            cmds.parentConstraint(
                driver,
                driven,
                maintainOffset=True,
                name=constraint_name
            )

        return self.parent_constraint_names

    def delete_rig(self):
        u"""

                删除当前 FK Chain 自己创建的 Constraint 和 DAG 输出。

                删除逻辑只使用初始化时保存的稳定名称：
                    1. 直接删除 parent_constraint_names 中存在的 Constraint。
                    2. 调用 RigModule.delete_rig() 删除 Joint / Controller 总组。
                    3. 清空当前 Python 工具对象引用。
                不使用 listConnections() 去猜测哪些 Constraint 属于当前模块。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。
                
        """

        # Constraint 是当前 FK Chain 明确拥有的节点，因此直接按稳定名称删除。
        for constraint_name in self.parent_constraint_names:
            if cmds.objExists(constraint_name):
                cmds.delete(constraint_name)

        # 删除当前模块的 Joint / Controller 总组以及其下面全部 DAG 子节点。
        delete_nodes = super(FKChain, self).delete_rig()

        # Maya 节点删除后清空临时工具对象；稳定名称列表继续保留，便于重新 build。
        self.jnt_objects = []
        self.ctrl_objects = []

        return delete_nodes
