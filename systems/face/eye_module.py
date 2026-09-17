# coding=utf-8
u"""
EyeModule：眼球 Aim 绑定模块。

这个模块只负责眼球本身，不处理 Eyelid、Blink、RBF、Corrective。

创建流程：
    build_rig()
        Ball Guide -> Eye Joint
        Ball Guide -> Main Controller
        Aim Guide  -> Aim Controller

连接流程：
    connect_rig()
        Aim Output -> Aim Constraint -> Main Driven
        Main Output -> Orient Constraint -> Eye Joint

说明：
    Iris Guide 继续保留在 face_guide.ma 中，后续可以用于 Iris、Pupil、
    Eye Look Direction 等功能，但基础 Eye Aim 绑定不使用它作为 Main Ctrl 的位置。

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

        # RigModule 统一保存 module、side、Guide 和父层级设置。
        super(EyeModule, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

        # Eye 只允许创建左眼或右眼，不使用中间侧 md。
        if self.side not in ("lf", "rt"):
            raise ValueError(u"Eye Module 只支持 lf / rt，当前值：{}".format(self.side))

        # Controller 外观设置只控制 Shape，不参与绑定连接计算。
        self.ctrl_shape = ctrl_shape
        self.aim_ctrl_shape = aim_ctrl_shape
        self.ctrl_color = ctrl_color
        self.ctrl_size = ctrl_size
        self.ctrl_axis = ctrl_axis
        self.aim_ctrl_axis = aim_ctrl_axis

        # 当前 Eye Module 自己创建的稳定节点名称只生成一次。
        # build_rig()、connect_rig()、delete_rig() 后面全部直接复用这些名称。
        self.eye_jnt_name = name_utils.Name(type="jnt", side=self.side, part=self.module, function="bind", index=1).name
        self.main_ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function="main", index=1).name
        self.aim_ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function="aim", index=1).name

        # Controller 标准层级中的 Driven / Output 名称由 Controller 名称直接确定。
        self.main_driven_name = self.main_ctrl_name.replace("ctrl_", "driven_", 1)
        self.main_output_name = self.main_ctrl_name.replace("ctrl_", "output_", 1)
        self.aim_output_name = self.aim_ctrl_name.replace("ctrl_", "output_", 1)

        # Eye Module 自己创建的 Constraint 也使用固定名称。
        # 删除时直接按这些名字删除，不需要再通过 listConnections() 反查。
        self.aim_constraint_name = name_utils.Name(type="aimConstraint", side=self.side, part=self.module, function="main", index=1).name
        self.orient_constraint_name = name_utils.Name(type="orientConstraint", side=self.side, part=self.module, function="bind", index=1).name

        # 这些是创建阶段使用的 Python 工具对象。
        # Maya 场景节点的稳定身份仍然以上面的 *_name 变量为准。
        self.eye_jnt_object = None
        self.main_ctrl_object = None
        self.aim_ctrl_object = None

    def create_joints(self):
        u"""
        在 Ball Guide 位置创建 Eye Bind Joint。

        Guide 顺序：
            guide_list[0] = Ball
            guide_list[1] = Iris
            guide_list[2] = Aim
        """

        # Eye Template 必须同时包含 Ball / Iris / Aim 三个 Guide。
        if len(self.guide_list) != 3:
            raise RuntimeError(u"Eye Module 需要 Ball / Iris / Aim 三个 Guide。")

        # Bind Joint 的中心就是眼球旋转中心，因此直接吸附 Ball Guide。
        self.eye_jnt_object = self.create_joint(
            name=self.eye_jnt_name,
            guide=self.guide_list[0]
        )

        return [self.eye_jnt_name]

    def create_ctrls(self):
        u"""
        创建 Eye Main Controller 和 Aim Controller。

        Main Controller：
            和 Eye Bind Joint 使用同一个 Ball Guide。
            Main Ctrl 的旋转中心必须与眼球 Joint 完全一致，
            这样后续 Aim 旋转时不会产生额外的眼球偏移。

        Aim Controller：
            吸附 Aim Guide，作为动画师控制眼球朝向的目标。

        Iris Guide：
            当前基础 Eye Aim 绑定暂时不参与 Main Ctrl 的位置计算，
            后续可以继续用于 Iris / Pupil / Look Direction 等功能。
        """

        # Main Controller 与 Bind Joint 共用 Ball Guide。
        # 这里不能使用 Iris Guide，否则 Main Ctrl 的旋转中心会偏离眼球中心。
        self.main_ctrl_object = self.create_ctrl(
            name=self.main_ctrl_name,
            guide=self.guide_list[0],
            shape_name=self.ctrl_shape,
            ctrl_color=self.ctrl_color,
            ctrl_size=self.ctrl_size,
            ctrl_axis=self.ctrl_axis,
            create_hierarchy=True
        )

        # Aim Controller 放在 Aim Guide，用来控制眼球最终朝向。
        self.aim_ctrl_object = self.create_ctrl(
            name=self.aim_ctrl_name,
            guide=self.guide_list[2],
            shape_name=self.aim_ctrl_shape,
            ctrl_color=self.ctrl_color,
            ctrl_size=self.ctrl_size * 0.5,
            ctrl_axis=self.aim_ctrl_axis,
            create_hierarchy=True
        )

        return [
            self.main_ctrl_name,
            self.aim_ctrl_name,
        ]

    def setup_hierarchy(self):
        u"""把 Eye Joint 和两个 Controller 放入当前 Eye Module 的总组。"""

        # 先创建当前 Eye Module 的 Joint / Controller 总组。
        super(EyeModule, self).setup_hierarchy()

        # Eye Joint 放入 Eye Joint 总组。
        hierarchy_utils.parent(self.eye_jnt_object.jnt, self.jnt_master_grp)

        # Controller 必须从 Zero Group 开始挂接，保留完整标准控制器层级。
        hierarchy_utils.parent(self.main_ctrl_object.zero_grp, self.ctrl_master_grp)
        hierarchy_utils.parent(self.aim_ctrl_object.zero_grp, self.ctrl_master_grp)

        return self.jnt_master_grp, self.ctrl_master_grp

    def connect_rig(self):
        u"""
        建立 Aim Controller -> Main Controller -> Eye Joint 的基础眼球绑定。

        Aim Output：
            通过 aimConstraint 驱动 Main Driven，使 Main Controller 层级朝向 Aim。

        Main Output：
            只通过 orientConstraint 驱动 Eye Joint 的旋转。
            Eye Joint 不接受 Main Controller 的位移，因此眼球中心始终保持在 Ball 位置。
        """

        # connect_rig() 只负责连接已经创建好的节点。
        # 如果 build_rig() 没有完成，就直接报出缺少的具体节点。
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
                raise RuntimeError(u"Eye Rig 节点不存在：{}".format(node_name))

        # Aim Output -> Main Driven。
        # Constraint 已经存在时直接复用，避免重复 connect 产生新的节点。
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

        # Main Output -> Eye Joint。
        # 这里只传递旋转，不让控制器改变眼球 Joint 的球心位置。
        if not cmds.objExists(self.orient_constraint_name):
            cmds.orientConstraint(
                self.main_output_name,
                self.eye_jnt_name,
                maintainOffset=True,
                name=self.orient_constraint_name
            )

        return {
            "aim": self.aim_constraint_name,
            "orient": self.orient_constraint_name,
        }

    def delete_rig(self):
        u"""删除 Eye Constraint、Eye Joint 和 Eye Controller Hierarchy。"""

        # Constraint 都是 EyeModule 自己创建的稳定节点，直接按名称删除。
        if cmds.objExists(self.aim_constraint_name):
            cmds.delete(self.aim_constraint_name)

        if cmds.objExists(self.orient_constraint_name):
            cmds.delete(self.orient_constraint_name)

        # 删除 Joint / Controller 两个模块总组以及下面的全部子节点。
        delete_nodes = super(EyeModule, self).delete_rig()

        # 清空临时 Python 工具对象引用。
        # 稳定节点名称不清空，同一个 EyeModule 实例仍然可以再次 build_rig()。
        self.eye_jnt_object = None
        self.main_ctrl_object = None
        self.aim_ctrl_object = None

        return delete_nodes
