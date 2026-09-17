# coding=utf-8
u"""
EyeModule：眼球 Aim 绑定模块。

职责保持简单：
    1. Ball Guide 创建 Eye Joint。
    2. Iris Guide 创建 Main Controller。
    3. Aim Guide 创建 Aim Controller。
    4. Final 阶段使用 Aim Constraint 控制目光方向。
    5. Main Output 使用 Parent Constraint 驱动 Eye Joint。

Guide 顺序由 Rig Library 统一提供：
    0 = Ball
    1 = Iris
    2 = Aim

Eyelid、Blink、RBF、Corrective 等功能不放在 EyeModule 中。
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
        u"""在 Ball Guide 位置创建眼球 Joint。"""

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
        u"""创建 Main Controller 和 Aim Controller。"""

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
        u"""把 Eye Joint 和两个 Controller 放入模块组。"""

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

    def load_outputs(self):
        u"""读取 Step 03 已经创建好的 Eye 输出。"""

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

        required_nodes = [
            self.eye_jnt_name,
            self.main_ctrl_name,
            self.main_ctrl_name.replace("ctrl_", "driven_", 1),
            self.main_ctrl_name.replace("ctrl_", "output_", 1),
            self.aim_ctrl_name,
            self.aim_ctrl_name.replace("ctrl_", "output_", 1),
        ]

        for node_name in required_nodes:
            if not cmds.objExists(node_name):
                raise RuntimeError(
                    u"找不到已经生成的 Eye 输出：{}".format(node_name)
                )

        return required_nodes

    def connect_rig(self):
        u"""创建 Aim Controller → Main Controller → Eye Joint 的最终连接。"""

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

        aim_constraints = cmds.listConnections(
            main_driven,
            source=True,
            destination=False,
            type="aimConstraint"
        ) or []

        if not aim_constraints:
            cmds.aimConstraint(
                aim_output,
                main_driven,
                maintainOffset=False,
                aimVector=(1, 0, 0),
                upVector=(0, 1, 0),
                worldUpType="vector",
                worldUpVector=(0, 1, 0)
            )

        parent_constraints = cmds.listConnections(
            self.eye_jnt_name,
            source=True,
            destination=False,
            type="parentConstraint"
        ) or []

        if not parent_constraints:
            cmds.parentConstraint(
                main_output,
                self.eye_jnt_name,
                maintainOffset=True
            )

        return {
            "aim": aim_constraints,
            "parent": parent_constraints,
        }
