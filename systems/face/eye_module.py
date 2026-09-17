# coding=utf-8
u"""
EyeModule：眼球 Aim 绑定模块。

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
        删除 Eye Constraint、Joint 和 Controller Hierarchy。

Eyelid、Blink、RBF、Corrective 不属于 EyeModule。
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
        u"""初始化 Eye Module。"""

        super(EyeModule, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

        if self.side not in ("lf", "rt"):
            raise ValueError(
                u"Eye Module 只支持 lf / rt，当前值：{}".format(self.side)
            )

        self.ctrl_shape = ctrl_shape
        self.aim_ctrl_shape = aim_ctrl_shape
        self.ctrl_color = ctrl_color
        self.ctrl_size = ctrl_size
        self.ctrl_axis = ctrl_axis
        self.aim_ctrl_axis = aim_ctrl_axis

        self.eye_jnt_name = None
        self.eye_jnt_object = None

        self.main_ctrl_name = None
        self.main_ctrl_object = None

        self.aim_ctrl_name = None
        self.aim_ctrl_object = None

    def create_joints(self):
        u"""在 Ball Guide 位置创建 Eye Joint。"""

        if len(self.guide_list) != 3:
            raise RuntimeError(
                u"Eye Module 需要 Ball / Iris / Aim 三个 Guide。"
            )

        self.eye_jnt_name = name_utils.Name(
            type="jnt",
            side=self.side,
            part=self.module,
            function="bind",
            index=1
        ).name

        self.eye_jnt_object = self.create_joint(
            name=self.eye_jnt_name,
            guide=self.guide_list[0]
        )

        return [self.eye_jnt_name]

    def create_ctrls(self):
        u"""在 Iris / Aim Guide 创建 Main 和 Aim Controller。"""

        self.main_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="main",
            index=1
        ).name

        self.main_ctrl_object = self.create_ctrl(
            name=self.main_ctrl_name,
            guide=self.guide_list[1],
            shape_name=self.ctrl_shape,
            ctrl_color=self.ctrl_color,
            ctrl_size=self.ctrl_size,
            ctrl_axis=self.ctrl_axis,
            create_hierarchy=True
        )

        self.aim_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="aim",
            index=1
        ).name

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
        u"""把 Eye Joint 和两个 Controller 放入模块根组。"""

        super(EyeModule, self).setup_hierarchy()

        hierarchy_utils.parent(
            self.eye_jnt_object.jnt,
            self.jnt_master_grp
        )

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
        u"""建立 Aim Controller -> Main Controller -> Eye Joint 驱动。"""

        self.eye_jnt_name = name_utils.Name(
            type="jnt",
            side=self.side,
            part=self.module,
            function="bind",
            index=1
        ).name

        self.main_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="main",
            index=1
        ).name

        self.aim_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="aim",
            index=1
        ).name

        main_driven = self.main_ctrl_name.replace(
            "ctrl_",
            "driven_",
            1
        )

        main_output = self.main_ctrl_name.replace(
            "ctrl_",
            "output_",
            1
        )

        aim_output = self.aim_ctrl_name.replace(
            "ctrl_",
            "output_",
            1
        )

        required_nodes = [
            self.eye_jnt_name,
            self.main_ctrl_name,
            main_driven,
            main_output,
            self.aim_ctrl_name,
            aim_output,
        ]

        for node_name in required_nodes:
            if not cmds.objExists(node_name):
                raise RuntimeError(
                    u"Eye Rig 节点不存在：{}".format(node_name)
                )

        aim_constraints = cmds.listConnections(
            main_driven,
            source=True,
            destination=False,
            type="aimConstraint"
        ) or []

        if aim_constraints:
            aim_constraint = aim_constraints[0]
        else:
            result = cmds.aimConstraint(
                aim_output,
                main_driven,
                maintainOffset=False,
                aimVector=(1, 0, 0),
                upVector=(0, 1, 0),
                worldUpType="vector",
                worldUpVector=(0, 1, 0)
            )
            aim_constraint = result[0]

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
                main_output,
                self.eye_jnt_name,
                maintainOffset=True
            )
            parent_constraint = result[0]

        return {
            "aim": aim_constraint,
            "parent": parent_constraint,
        }

    def delete_rig(self):
        u"""删除 Eye Constraint 和当前 Eye Module 的全部输出。"""

        eye_jnt_name = name_utils.Name(
            type="jnt",
            side=self.side,
            part=self.module,
            function="bind",
            index=1
        ).name

        main_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="main",
            index=1
        ).name

        main_driven = main_ctrl_name.replace(
            "ctrl_",
            "driven_",
            1
        )

        constraints = []

        if cmds.objExists(main_driven):
            nodes = cmds.listConnections(
                main_driven,
                source=True,
                destination=False,
                type="aimConstraint"
            ) or []

            for node_name in nodes:
                if node_name not in constraints:
                    constraints.append(node_name)

        if cmds.objExists(eye_jnt_name):
            nodes = cmds.listConnections(
                eye_jnt_name,
                source=True,
                destination=False,
                type="parentConstraint"
            ) or []

            for node_name in nodes:
                if node_name not in constraints:
                    constraints.append(node_name)

        if constraints:
            cmds.delete(constraints)

        return super(EyeModule, self).delete_rig()
