# coding=utf-8
u"""
EyeModule：眼球 Aim 绑定模块。

这个模块只负责眼球本身，不处理 Eyelid、Blink、RBF、Corrective。

创建流程：
    build_rig()
        Ball Guide -> Eye Joint
        Iris Guide -> Main Controller
        Aim Guide  -> Aim Controller

连接流程：
    connect_rig()
        Aim Output -> Aim Constraint -> Main Driven
        Main Output -> Parent Constraint -> Eye Joint

删除流程：
    delete_rig()
        删除 Eye Constraint
        删除 Eye Joint / Controller Hierarchy

设计原则：
    EyeModule 自己创建的所有稳定 Maya 节点，都在 __init__() 中先确定名称。
    build / connect / delete 全部直接复用这些名称，不在删除阶段反查场景连接。
"""

import maya.cmds as cmds

from .. import rig_module
from ...core.common import name_utils, hierarchy_utils


class EyeModule(rig_module.RigModule):

    def __init__(
        self,
        module="eye",
        side="lf",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None,
        ctrl_shape="shape_016",
        aim_ctrl_shape="circle",
        ctrl_color=17,
        ctrl_size=18,
        ctrl_axis="Z+",
        aim_ctrl_axis="Z+"
    ):
        u"""初始化 Eye Module 的配置、稳定节点名称和运行时对象。"""

        # ---------------------------------------------------------------------
        # 先初始化 RigModule 的公共数据。
        # module / side / guide / parent 都由基类统一保存。
        # ---------------------------------------------------------------------
        super(EyeModule, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

        # Eye 目前只支持左右两侧，不允许 md，避免生成没有实际意义的中间眼球模块。
        if self.side not in ("lf", "rt"):
            raise ValueError(
                u"Eye Module 只支持 lf / rt，当前值：{}".format(self.side)
            )

        # ---------------------------------------------------------------------
        # Controller 外观设置。
        # 这些值只影响 Controller Shape，不改变 Eye 的连接逻辑。
        # ---------------------------------------------------------------------
        self.ctrl_shape = ctrl_shape
        self.aim_ctrl_shape = aim_ctrl_shape
        self.ctrl_color = ctrl_color
        self.ctrl_size = ctrl_size
        self.ctrl_axis = ctrl_axis
        self.aim_ctrl_axis = aim_ctrl_axis

        # ---------------------------------------------------------------------
        # Eye Module 自己创建的稳定节点名称。
        # 所有名称只在初始化时生成一次，后面的 create / connect / delete 全部复用。
        # 这样不会在不同函数里重复写 Naming 规则，也不需要删除时再查询场景连接。
        # ---------------------------------------------------------------------
        self.eye_jnt_name = name_utils.Name(type="jnt", side=self.side, part=self.module, function="bind", index=1).name
        self.main_ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function="main", index=1).name
        self.aim_ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function="aim", index=1).name

        # Controller 标准层级中的稳定节点名称。
        self.main_driven_name = self.main_ctrl_name.replace("ctrl_", "driven_", 1)
        self.main_output_name = self.main_ctrl_name.replace("ctrl_", "output_", 1)
        self.aim_output_name = self.aim_ctrl_name.replace("ctrl_", "output_", 1)

        # Eye Module 自己创建的两个 Constraint 也使用固定名称。
        # connect_rig() 创建时显式指定这些名称，delete_rig() 可以直接删除。
        self.aim_constraint_name = name_utils.Name(type="aimConstraint", side=self.side, part=self.module, function="main", index=1).name
        self.parent_constraint_name = name_utils.Name(type="parentConstraint", side=self.side, part=self.module, function="bind", index=1).name

        # ---------------------------------------------------------------------
        # 运行时工具对象。
        # build_rig() 创建后保存 Jnt / Ctrl 工具对象，主要用于创建阶段整理层级。
        # 稳定 Maya 节点本身仍然以 *_name 成员作为唯一名称来源。
        # ---------------------------------------------------------------------
        self.eye_jnt_object = None
        self.main_ctrl_object = None
        self.aim_ctrl_object = None

    def create_joints(self):
        u"""
        在 Ball Guide 位置创建 Eye Joint。

        Guide 顺序约定：
            guide_list[0] = Ball
            guide_list[1] = Iris
            guide_list[2] = Aim
        """

        # Eye 必须同时拥有 Ball / Iris / Aim 三个 Guide。
        # 数量不正确时直接停止，避免后面使用错误索引创建节点。
        if len(self.guide_list) != 3:
            raise RuntimeError(
                u"Eye Module 需要 Ball / Iris / Aim 三个 Guide。"
            )

        # Eye Joint 的旋转中心来自 Ball Guide。
        self.eye_jnt_object = self.create_joint(
            name=self.eye_jnt_name,
            guide=self.guide_list[0]
        )

        return [self.eye_jnt_name]

    def create_ctrls(self):
        u"""
        创建 Eye Main Controller 和 Aim Controller。

        Main Controller：
            使用 Iris Guide 作为创建位置。

        Aim Controller：
            使用 Aim Guide 作为目标控制位置。
        """

        # ---------------------------------------------------------------------
        # 创建 Main Controller。
        # Main 负责最终的眼球旋转结果，并通过 output 节点驱动 Eye Joint。
        # ---------------------------------------------------------------------
        self.main_ctrl_object = self.create_ctrl(
            name=self.main_ctrl_name,
            guide=self.guide_list[1],
            shape_name=self.ctrl_shape,
            ctrl_color=self.ctrl_color,
            ctrl_size=self.ctrl_size,
            ctrl_axis=self.ctrl_axis,
            create_hierarchy=True
        )

        # ---------------------------------------------------------------------
        # 创建 Aim Controller。
        # 动画师移动 Aim Ctrl 后，Aim Output 会通过 aimConstraint 驱动 Main Driven。
        # ---------------------------------------------------------------------
        self.aim_ctrl_object = self.create_ctrl(
            name=self.aim_ctrl_name,
            guide=self.guide_list[2],
            shape_name=self.aim_ctrl_shape,
            ctrl_color=self.ctrl_color,
            ctrl_size=self.ctrl_size *0.5,
            ctrl_axis=self.aim_ctrl_axis,
            create_hierarchy=True
        )

        return [
            self.main_ctrl_name,
            self.aim_ctrl_name,
        ]

    def setup_hierarchy(self):
        u"""
        整理 Eye Joint 和两个 Controller 的模块层级。

        最终结构：
            grp_<side>_eye_jnt_001
                jnt_<side>_eye_bind_001

            grp_<side>_eye_ctrl_001
                zero_<side>_eye_main_001
                zero_<side>_eye_aim_001
        """

        # 先让 RigModule 创建当前 Eye Module 的 Joint / Ctrl 总组。
        super(EyeModule, self).setup_hierarchy()

        # 把 Eye Joint 放进当前模块的 Joint 总组。
        hierarchy_utils.parent(
            self.eye_jnt_object.jnt,
            self.jnt_master_grp
        )

        # Controller 必须从 zero 组开始挂接，保持内部标准层级完整。
        hierarchy_utils.parent(
            self.main_ctrl_object.zero_grp,
            self.ctrl_master_grp
        )

        hierarchy_utils.parent(
            self.aim_ctrl_object.zero_grp,
            self.ctrl_master_grp
        )

        return self.jnt_master_grp, self.ctrl_master_grp

    def connect_rig(self):
        u"""
        建立 Aim Controller -> Main Controller -> Eye Joint 的最终驱动。

        驱动关系：
            Aim Output
                -> aimConstraint
                -> Main Driven

            Main Output
                -> parentConstraint
                -> Eye Joint

        所有连接节点都使用 __init__() 中已经确定好的稳定名称。
        connect_rig() 不再通过 listConnections() 反查我们自己创建过的 Constraint。
        """

        # ---------------------------------------------------------------------
        # 连接前先确认 build_rig() 生成的必要 DAG 节点都存在。
        # 这里只检查输入节点，不重新查找或重新计算这些节点的名称。
        # ---------------------------------------------------------------------
        required_nodes = [
            self.eye_jnt_name,
            self.main_ctrl_name,
            self.main_driven_name,
            self.main_output_name,
            self.aim_ctrl_name,
            self.aim_output_name,
        ]

        for node_name in required_nodes:
            if not cmds.objExists(node_name):
                raise RuntimeError(
                    u"Eye Rig 节点不存在：{}".format(node_name)
                )

        # ---------------------------------------------------------------------
        # Aim Output -> Main Driven。
        # Constraint 名称在 __init__() 中已经确定。
        # 如果已经存在就直接复用；不存在时才创建，避免重复执行 connect_rig() 产生副本。
        # ---------------------------------------------------------------------
        if not cmds.objExists(self.aim_constraint_name):
            cmds.aimConstraint(
                self.aim_output_name,
                self.main_driven_name,
                maintainOffset=False,
                aimVector=(1, 0, 0),
                upVector=(0, 1, 0),
                worldUpType="vector",
                worldUpVector=(0, 1, 0),
                name=self.aim_constraint_name
            )

        # ---------------------------------------------------------------------
        # Main Output -> Eye Joint。
        # 同样直接使用固定的 Parent Constraint 名称，不再查询 Joint 的输入连接。
        # ---------------------------------------------------------------------
        if not cmds.objExists(self.parent_constraint_name):
            cmds.parentConstraint(
                self.main_output_name,
                self.eye_jnt_name,
                maintainOffset=True,
                name=self.parent_constraint_name
            )

        # 返回稳定节点名称，方便 Maya Script Editor 中直接检查连接是否创建成功。
        return {
            "aim": self.aim_constraint_name,
            "parent": self.parent_constraint_name,
        }

    def delete_rig(self):
        u"""
        删除 Eye Module 自己创建的 Constraint、Joint 和 Controller Hierarchy。

        删除顺序：
            1. 直接删除固定名称的 Aim Constraint。
            2. 直接删除固定名称的 Parent Constraint。
            3. 调用 RigModule.delete_rig() 删除 Joint / Ctrl 总组。

        因为所有节点名称都由 EyeModule 自己保存，所以删除阶段不需要 listConnections()
        或其他反查逻辑。只删除 EyeModule 明确拥有的节点，也可以避免误删外部连接。
        """

        # 删除 Aim Controller 到 Main Driven 的 Aim Constraint。
        if cmds.objExists(self.aim_constraint_name):
            cmds.delete(self.aim_constraint_name)

        # 删除 Main Output 到 Eye Joint 的 Parent Constraint。
        if cmds.objExists(self.parent_constraint_name):
            cmds.delete(self.parent_constraint_name)

        # 删除当前 Eye Module 的 Joint / Controller 总组及其全部子层级。
        delete_nodes = super(EyeModule, self).delete_rig()

        # 清空创建阶段使用的 Python 工具对象引用。
        # 稳定名称成员不清空，这样同一个 EyeModule 实例仍然可以重新 build_rig()。
        self.eye_jnt_object = None
        self.main_ctrl_object = None
        self.aim_ctrl_object = None

        return delete_nodes
