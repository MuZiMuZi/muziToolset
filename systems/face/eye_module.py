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
        aim_ctrl_shape="shape_040",
        ctrl_color=17,
        ctrl_size=1.0,
        ctrl_axis="X+",
        aim_ctrl_axis="Z+"
    ):
        u"""初始化 Eye Module 的配置、稳定名称和运行时对象。"""

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
        # 当前 Eye Module 的稳定名称只生成一次。
        # 后面的 create / connect / delete 全部直接复用这些成员，
        # 不再在每个函数里重新写一遍 name_utils.Name(...)。
        # ---------------------------------------------------------------------
        self.eye_jnt_name = name_utils.Name(type="jnt", side=self.side, part=self.module, function="bind", index=1).name
        self.main_ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function="main", index=1).name
        self.aim_ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function="aim", index=1).name

        # ---------------------------------------------------------------------
        # Controller 标准层级中的稳定节点名称。
        # 这些名称由 Ctrl 的标准命名规则决定，因此直接从 ctrl 名称替换前缀即可。
        # ---------------------------------------------------------------------
        self.main_driven_name = self.main_ctrl_name.replace("ctrl_", "driven_", 1)
        self.main_output_name = self.main_ctrl_name.replace("ctrl_", "output_", 1)
        self.aim_output_name = self.aim_ctrl_name.replace("ctrl_", "output_", 1)

        # ---------------------------------------------------------------------
        # 运行时对象引用。
        # build_rig() 创建后会保存真正的 Jnt / Ctrl 工具对象。
        # delete_rig() 完成后会重新清空这些引用。
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
        # 数量不正确时直接停止，避免后面用错误索引创建节点。
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
            ctrl_size=self.ctrl_size,
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

        # 先让 RigModule 创建当前 Eye Module 的 Joint / Ctrl 根组。
        super(EyeModule, self).setup_hierarchy()

        # 把 Eye Joint 放进当前模块的 Joint 根组。
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

        connect_rig() 可以在新的 EyeModule 实例上执行，因此这里直接使用稳定名称
        查找 Maya 场景节点，不依赖 build_rig() 时保存的 Python 对象引用。
        """

        # ---------------------------------------------------------------------
        # 连接前先确认所有必要节点都已经存在。
        # 如果 build_rig() 没有完整执行，就在这里明确报出缺失节点。
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
        # Aim Output -> Main Driven
        # 如果已经存在 aimConstraint，就直接复用，避免重复创建约束。
        # ---------------------------------------------------------------------
        aim_constraints = cmds.listConnections(
            self.main_driven_name,
            source=True,
            destination=False,
            type="aimConstraint"
        ) or []

        if aim_constraints:
            aim_constraint = aim_constraints[0]
        else:
            result = cmds.aimConstraint(
                self.aim_output_name,
                self.main_driven_name,
                maintainOffset=False,
                aimVector=(1, 0, 0),
                upVector=(0, 1, 0),
                worldUpType="vector",
                worldUpVector=(0, 1, 0)
            )
            aim_constraint = result[0]

        # ---------------------------------------------------------------------
        # Main Output -> Eye Joint
        # Main Ctrl 的最终动画结果通过 output 节点传给 Eye Joint。
        # maintainOffset=True 用来保留 Joint 和 Controller 初始空间关系。
        # ---------------------------------------------------------------------
        parent_constraints = cmds.listConnections(
            self.eye_jnt_name,
            source=True,
            destination=False,
            type="parentConstraint"
        ) or []

        if parent_constraints:
            parent_constraint = parent_constraints[0]
        else:
            result = cmds.parentConstraint(
                self.main_output_name,
                self.eye_jnt_name,
                maintainOffset=True
            )
            parent_constraint = result[0]

        # 返回当前 Eye Rig 的主要连接节点，方便 Maya 测试时检查。
        return {
            "aim": aim_constraint,
            "parent": parent_constraint,
        }

    def delete_rig(self):
        u"""
        删除 Eye Module 创建的 Constraint、Joint 和 Controller Hierarchy。

        删除顺序：
            1. 先删除 Aim / Parent Constraint。
            2. 再调用 RigModule.delete_rig() 删除 Joint / Ctrl 根组。
            3. 最后清空 Python 运行时对象引用。
        """

        # 保存需要单独删除的 Constraint。
        # Constraint 属于 DG 节点，不一定会随着我们预期的 DAG 根组一起安全清理，
        # 因此这里先明确找到并删除。
        constraints = []

        # 查找 Main Driven 上的 aimConstraint。
        if cmds.objExists(self.main_driven_name):
            nodes = cmds.listConnections(
                self.main_driven_name,
                source=True,
                destination=False,
                type="aimConstraint"
            ) or []

            for node_name in nodes:
                if node_name not in constraints:
                    constraints.append(node_name)

        # 查找 Eye Joint 上的 parentConstraint。
        if cmds.objExists(self.eye_jnt_name):
            nodes = cmds.listConnections(
                self.eye_jnt_name,
                source=True,
                destination=False,
                type="parentConstraint"
            ) or []

            for node_name in nodes:
                if node_name not in constraints:
                    constraints.append(node_name)

        # 先删除当前 Eye Module 自己的连接节点。
        if constraints:
            cmds.delete(constraints)

        # 再交给 RigModule 删除 Joint / Controller 根组及其全部子节点。
        delete_nodes = super(EyeModule, self).delete_rig()

        # Maya 节点已经删除后，清空 Python 中保存的工具对象引用。
        self.eye_jnt_object = None
        self.main_ctrl_object = None
        self.aim_ctrl_object = None

        return delete_nodes
