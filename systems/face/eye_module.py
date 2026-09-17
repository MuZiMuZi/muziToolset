# coding=utf-8
u"""
EyeModule：眼球 Aim 绑定模块。

这个模块只负责眼球本身，不处理 Eyelid、Blink、RBF、Corrective。

创建流程：
    build_rig()
        Ball Guide -> Ball Joint
        Iris Guide -> Iris Joint
        Ball Guide -> Main Controller
        Aim Guide  -> Aim Controller

Joint 层级：
    grp_<side>_eye_jnt_001
        jnt_<side>_eye_ball_001
            jnt_<side>_eye_iris_001

连接流程：
    connect_rig()
        Aim Output -> Aim Constraint -> Main Driven
        Main Output -> Orient Constraint -> Ball Joint
        Ball Joint -> Hierarchy -> Iris Joint

说明：
    Ball Joint 是整个眼球的旋转中心。
    Iris Joint 位于 Iris Guide，并作为 Ball Joint 的子关节继承眼球旋转。
    Main Controller 与 Ball Joint 使用同一个 Ball Guide，保证旋转中心一致。

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
        u"""
        初始化 Eye Module 的配置、稳定节点名称和运行时对象。

        Args:
            module (str):
                `module` 对应的名称、标记或字符串参数。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            guide (str):
                需要查询或处理的 Guide Transform 名称。
            jnt_parent (object):
                `jnt_parent` 对应的输入数据。
            ctrl_parent (object):
                `ctrl_parent` 对应的输入数据。
            ctrl_shape (str):
                `ctrl_shape` 对应的名称、标记或字符串参数。
            aim_ctrl_shape (str):
                `aim_ctrl_shape` 对应的名称、标记或字符串参数。
            ctrl_color (int):
                `ctrl_color` 对应的整数参数。
            ctrl_size (int):
                `ctrl_size` 对应的整数参数。
            ctrl_axis (str):
                `ctrl_axis` 对应的名称、标记或字符串参数。
            aim_ctrl_axis (str):
                `aim_ctrl_axis` 对应的名称、标记或字符串参数。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """

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

        # ---------------------------------------------------------------------
        # 当前 Eye Module 自己创建的稳定 Maya 节点名称。
        #
        # Ball / Iris 两根 Joint 分别对应 face_guide.ma 中的 Ball / Iris Guide。
        # 不再使用一个泛化的 jnt_*_eye_bind_001，因为 Eye 的两根 Joint 本身拥有
        # 明确且不同的业务语义，后面的创建、连接和删除都直接复用这些固定名称。
        # ---------------------------------------------------------------------
        self.ball_jnt_name = name_utils.Name(type="jnt", side=self.side, part=self.module, function="ball", index=1).name
        self.iris_jnt_name = name_utils.Name(type="jnt", side=self.side, part=self.module, function="iris", index=1).name
        self.main_ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function="main", index=1).name
        self.aim_ctrl_name = name_utils.Name(type="ctrl", side=self.side, part=self.module, function="aim", index=1).name

        # Controller 标准层级中的 Driven / Output 名称由 Controller 名称直接确定。
        self.main_driven_name = self.main_ctrl_name.replace("ctrl_", "driven_", 1)
        self.main_output_name = self.main_ctrl_name.replace("ctrl_", "output_", 1)
        self.aim_output_name = self.aim_ctrl_name.replace("ctrl_", "output_", 1)

        # Eye Module 自己创建的 Constraint 也使用固定名称。
        # Orient Constraint 直接驱动 Ball Joint，因此 function 也使用 ball。
        self.aim_constraint_name = name_utils.Name(type="aimConstraint", side=self.side, part=self.module, function="main", index=1).name
        self.orient_constraint_name = name_utils.Name(type="orientConstraint", side=self.side, part=self.module, function="ball", index=1).name

        # 创建阶段使用的 Python 工具对象。
        # Maya 场景节点的稳定身份仍然以上面的 *_name 成员作为唯一名称来源。
        self.ball_jnt_object = None
        self.iris_jnt_object = None
        self.main_ctrl_object = None
        self.aim_ctrl_object = None

    def create_joints(self):
        u"""

                根据 Ball / Iris Guide 创建两根 Eye Joint。

                Guide 顺序：
                    guide_list[0] = Ball
                    guide_list[1] = Iris
                    guide_list[2] = Aim
                创建结果：
                    Ball Guide -> jnt_<side>_eye_ball_001
                    Iris Guide -> jnt_<side>_eye_iris_001
                Joint 的父子层级会在 setup_hierarchy() 中统一整理。

                Returns:
                    list:
                        按当前 API 约定顺序返回的结果列表。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                
        """

        # Eye Template 必须同时包含 Ball / Iris / Aim 三个 Guide。
        # Aim 虽然不会创建 Joint，但它是当前 Eye Module 的必要输入。
        if len(self.guide_list) != 3:
            raise RuntimeError(u"Eye Module 需要 Ball / Iris / Aim 三个 Guide。")

        # Ball Joint 是整个眼球真正的旋转中心。
        self.ball_jnt_object = self.create_joint(
            name=self.ball_jnt_name,
            guide=self.guide_list[0]
        )

        # Iris Joint 放在虹膜 Guide 位置。
        # 后面会作为 Ball Joint 的子关节，因此能够自然继承整个眼球的旋转。
        self.iris_jnt_object = self.create_joint(
            name=self.iris_jnt_name,
            guide=self.guide_list[1]
        )

        return [
            self.ball_jnt_name,
            self.iris_jnt_name,
        ]

    def create_ctrls(self):
        u"""

                创建 Eye Main Controller 和 Aim Controller。

                Main Controller：
                    和 Ball Joint 使用同一个 Ball Guide。
                    Main Ctrl 的旋转中心必须与眼球 Ball Joint 完全一致，
                    这样后续 Aim 旋转时不会产生额外的眼球偏移。
                Aim Controller：
                    吸附 Aim Guide，作为动画师控制眼球朝向的目标。

                Returns:
                    list:
                        按当前 API 约定顺序返回的结果列表。
                
        """

        # Main Controller 与 Ball Joint 共用 Ball Guide。
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
        u"""

                整理 Eye Joint 和 Controller 的正式模块层级。

                Joint：
                    grp_<side>_eye_jnt_001
                        jnt_<side>_eye_ball_001
                            jnt_<side>_eye_iris_001
                Controller：
                    grp_<side>_eye_ctrl_001
                        zero_<side>_eye_main_001
                        zero_<side>_eye_aim_001

                Returns:
                    tuple:
                        按当前 API 约定组织的结果元组。
                
        """

        # 先创建当前 Eye Module 的 Joint / Controller 总组。
        super(EyeModule, self).setup_hierarchy()

        # Ball Joint 是 Eye Joint Chain 的根节点，所以直接放入 Eye Joint 总组。
        hierarchy_utils.parent(
            self.ball_jnt_object.jnt,
            self.jnt_master_grp
        )

        # Iris Joint 是 Ball Joint 的子节点。
        # Parent 操作保持当前世界位置，因此 Iris 仍然停留在 Iris Guide 上。
        hierarchy_utils.parent(
            self.iris_jnt_object.jnt,
            self.ball_jnt_object.jnt
        )

        # Controller 必须从 Zero Group 开始挂接，保留完整标准控制器层级。
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

                建立 Aim Controller -> Main Controller -> Eye Ball Joint 的基础眼球绑定。

                Aim Output：
                    通过 aimConstraint 驱动 Main Driven，使 Main Controller 层级朝向 Aim。
                    maintainOffset=True 保留 Guide 阶段已经确定好的初始眼球朝向。
                Main Output：
                    通过 orientConstraint 驱动 Ball Joint 的旋转。
                    Ball Joint 不接受 Main Controller 的位移，因此眼球中心始终固定。
                Iris Joint：
                    不需要额外 Constraint。
                    它作为 Ball Joint 的子关节，直接继承 Ball Joint 的眼球旋转结果。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                
        """

        # connect_rig() 只负责连接已经创建好的稳定节点。
        required_nodes = [
            self.ball_jnt_name,
            self.iris_jnt_name,
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
        # 保持初始偏移，避免创建 Constraint 的瞬间改变已经摆好的 Eye 朝向。
        if not cmds.objExists(self.aim_constraint_name):
            cmds.aimConstraint(
                self.aim_output_name,
                self.main_driven_name,
                maintainOffset=True,
                aimVector=(1, 0, 0),
                upVector=(0, 1, 0),
                worldUpType="vector",
                worldUpVector=(0, 1, 0),
                name=self.aim_constraint_name
            )

        # Main Output -> Ball Joint。
        # 只传递旋转，不改变 Ball Joint 的球心位置。
        if not cmds.objExists(self.orient_constraint_name):
            cmds.orientConstraint(
                self.main_output_name,
                self.ball_jnt_name,
                maintainOffset=True,
                name=self.orient_constraint_name
            )

        return {
            "aim": self.aim_constraint_name,
            "orient": self.orient_constraint_name,
        }

    def delete_rig(self):
        u"""

                删除 Eye Constraint、两根 Eye Joint 和 Eye Controller Hierarchy。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。
                
        """

        # Constraint 都是 EyeModule 自己创建的稳定节点，直接按名称删除。
        if cmds.objExists(self.aim_constraint_name):
            cmds.delete(self.aim_constraint_name)

        if cmds.objExists(self.orient_constraint_name):
            cmds.delete(self.orient_constraint_name)

        # 删除 Joint / Controller 两个模块总组。
        # Ball / Iris Joint 都位于 Joint 总组下面，会一起被删除。
        delete_nodes = super(EyeModule, self).delete_rig()

        # 清空创建阶段使用的 Python 工具对象引用。
        # 稳定节点名称不清空，同一个 EyeModule 实例仍然可以再次 build_rig()。
        self.ball_jnt_object = None
        self.iris_jnt_object = None
        self.main_ctrl_object = None
        self.aim_ctrl_object = None

        return delete_nodes
