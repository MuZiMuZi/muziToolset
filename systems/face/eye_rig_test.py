# coding=utf-8
u"""
Eye Rig Test
============

独立眼球绑定测试模块。

目标：
    1. 不连接 Face Rig UI。
    2. 不修改正式 EyeModule。
    3. Main Ctrl 的可见位置保持在 Iris Guide。
    4. Main Ctrl / Aim 驱动的旋转中心位于 Eye Ball Guide。
    5. Joint 只接收旋转，不接收位移。

测试结构：

    ctrl_<side>_eye_test_aim_001
        -> Aim Constraint
        -> driven_<side>_eye_test_main_001
        -> ctrl_<side>_eye_test_main_001
        -> output_<side>_eye_test_main_001
        -> driver_<side>_eye_test_pose_001
        -> driven_<side>_eye_test_pose_001
        -> Orient Constraint
        -> jnt_<side>_eye_test_bind_001

关键原则：
    Controller Hierarchy 仍然创建在 Iris Guide。
    不再移动 zero Group 到 Eye Ball。
    只把需要旋转的层级 Rotate / Scale Pivot 设置到 Eye Ball。
"""

import maya.cmds as cmds

from . import eye_module
from ...core.common import name_utils


TEST_MODULE = "eye_test"
SUPPORTED_SIDES = ("lf", "rt")


class EyeRigTest(eye_module.EyeModule):
    u"""用于 Maya 场景直接验证眼球 Aim 绑定的独立测试模块。"""

    def __init__(
        self,
        side="lf",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None,
        ctrl_shape="circle",
        aim_ctrl_shape="shape_040",
        ctrl_color=17,
        ctrl_size=1.0,
        ctrl_axis="X+",
        aim_ctrl_axis="Z+"
    ):
        super(EyeRigTest, self).__init__(
            module=TEST_MODULE,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent,
            ctrl_shape=ctrl_shape,
            aim_ctrl_shape=aim_ctrl_shape,
            ctrl_color=ctrl_color,
            ctrl_size=ctrl_size,
            ctrl_axis=ctrl_axis,
            aim_ctrl_axis=aim_ctrl_axis
        )

        self.world_up_name = None
        self.pose_driver_name = None
        self.pose_driven_name = None
        self.aim_constraint_name = None
        self.orient_constraint_name = None

    @staticmethod
    def _node_name(node):
        u"""统一把 PyNode / Maya Node 转换成 maya.cmds 使用的字符串名称。"""

        if node is None:
            return None

        return str(node)

    @staticmethod
    def _world_position(node_name):
        u"""返回节点的 World Position。"""

        return cmds.xform(
            str(node_name),
            query=True,
            worldSpace=True,
            translation=True
        )

    @staticmethod
    def _world_rotate_pivot(node_name):
        u"""返回节点的 World Rotate Pivot。"""

        return cmds.xform(
            str(node_name),
            query=True,
            worldSpace=True,
            rotatePivot=True
        )

    @staticmethod
    def _set_world_pivot(node_name, pivot_position):
        u"""
        把 Transform 的 Rotate / Scale Pivot 设置到指定世界位置。

        xform 修改 Pivot 时默认 Preserve Transform，
        因此不会因为移动 Pivot 而改变 Controller 当前世界位置。
        """

        node_name = str(node_name)

        cmds.xform(
            node_name,
            worldSpace=True,
            rotatePivot=(
                pivot_position[0],
                pivot_position[1],
                pivot_position[2]
            )
        )

        cmds.xform(
            node_name,
            worldSpace=True,
            scalePivot=(
                pivot_position[0],
                pivot_position[1],
                pivot_position[2]
            )
        )

    @staticmethod
    def _set_world_matrix(node_name, source_name):
        u"""把 source 的 World Matrix 完整复制给 node。"""

        node_name = str(node_name)
        source_name = str(source_name)

        world_matrix = cmds.xform(
            source_name,
            query=True,
            worldSpace=True,
            matrix=True
        )

        cmds.xform(
            node_name,
            worldSpace=True,
            matrix=world_matrix
        )

    def build(self):
        u"""删除当前侧旧测试节点后重新构建。"""

        delete_test(self.side)
        super(EyeRigTest, self).build()
        return self

    def _set_main_rotation_pivots(self):
        u"""
        保持 Main Controller 位于 Iris，只把旋转轴心设置到 Eye Ball。

        driven：Aim Constraint 实际旋转层。
        space / connect / offset：后续 Space、Rig Connection、校正层旋转时也使用球心。
        ctrl / subctrl：动画师手动旋转时使用球心。
        output：保持最终输出层与 Main / SubCtrl 的旋转中心语义一致。
        """

        ball_position = self._world_position(
            self.guide_map["ball"]
        )

        pivot_nodes = [
            self.main_ctrl_object.driven_grp,
            self.main_ctrl_object.space_grp,
            self.main_ctrl_object.connect_grp,
            self.main_ctrl_object.offset_grp,
            self.main_ctrl_object.ctrl,
            self.main_ctrl_object.sub_ctrl,
            self.main_ctrl_object.output_grp,
        ]

        for pivot_node in pivot_nodes:
            if pivot_node is None:
                continue

            self._set_world_pivot(
                self._node_name(pivot_node),
                ball_position
            )

    def create_ctrls(self):
        u"""
        创建 Main / Aim Controller。

        EyeModule 原始逻辑会让 Main Ctrl 按 Iris Guide 创建，
        这个位置正是我们需要的，所以这里不再移动 Zero / Curve。
        创建完成后只调整各旋转层的 Pivot 到 Eye Ball。
        """

        result = super(EyeRigTest, self).create_ctrls()

        self._set_main_rotation_pivots()

        return result

    def _create_world_up(self):
        u"""创建跟随模块父空间、但不跟随眼球 Aim 旋转的 World Up Transform。"""

        self.world_up_name = name_utils.Name(
            type="grp",
            side=self.side,
            part=self.module,
            function="worldup",
            index=1
        ).name

        if cmds.objExists(self.world_up_name):
            cmds.delete(self.world_up_name)

        ctrl_master_grp = self._node_name(
            self.ctrl_master_grp
        )

        self.world_up_name = cmds.createNode(
            "transform",
            name=self.world_up_name,
            parent=ctrl_master_grp
        )

        self._set_world_matrix(
            self.world_up_name,
            self.guide_map["ball"]
        )

        return self.world_up_name

    def _create_pose_chain(self, main_output):
        u"""在 Main Output 下创建 Pose Driver / Pose Driven 中间层。"""

        main_output = self._node_name(
            main_output
        )

        self.pose_driver_name = name_utils.Name(
            type="driver",
            side=self.side,
            part=self.module,
            function="pose",
            index=1
        ).name

        self.pose_driven_name = name_utils.Name(
            type="driven",
            side=self.side,
            part=self.module,
            function="pose",
            index=1
        ).name

        if cmds.objExists(self.pose_driver_name):
            cmds.delete(self.pose_driver_name)

        if cmds.objExists(self.pose_driven_name):
            cmds.delete(self.pose_driven_name)

        self.pose_driver_name = cmds.createNode(
            "transform",
            name=self.pose_driver_name,
            parent=main_output
        )

        self.pose_driven_name = cmds.createNode(
            "transform",
            name=self.pose_driven_name,
            parent=self.pose_driver_name
        )

        return self.pose_driver_name, self.pose_driven_name

    def connect_rig(self):
        u"""
        建立 Eye Aim -> Main -> Pose -> Joint 测试连接。

        Aim Constraint 使用 maintainOffset=True，
        目的是构建时严格保留 Main Ctrl 当前 Iris 初始位置，
        避免约束创建瞬间因为局部轴向差异把控制器甩离 Guide。
        """

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

        world_up = self._create_world_up()

        self.aim_constraint_name = name_utils.Name(
            type="con",
            side=self.side,
            part=self.module,
            function="aim",
            index=1
        ).name

        if cmds.objExists(self.aim_constraint_name):
            cmds.delete(self.aim_constraint_name)

        self.aim_constraint_name = cmds.aimConstraint(
            aim_output,
            main_driven,
            maintainOffset=True,
            weight=1,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="objectrotation",
            worldUpVector=(0, 1, 0),
            worldUpObject=world_up,
            name=self.aim_constraint_name
        )[0]

        self._create_pose_chain(
            main_output
        )

        self.orient_constraint_name = name_utils.Name(
            type="con",
            side=self.side,
            part=self.module,
            function="orient",
            index=1
        ).name

        if cmds.objExists(self.orient_constraint_name):
            cmds.delete(self.orient_constraint_name)

        self.orient_constraint_name = cmds.orientConstraint(
            self.pose_driven_name,
            self.eye_jnt_name,
            maintainOffset=True,
            weight=1,
            name=self.orient_constraint_name
        )[0]

        return {
            "joint": self.eye_jnt_name,
            "main_ctrl": self.main_ctrl_name,
            "aim_ctrl": self.aim_ctrl_name,
            "world_up": self.world_up_name,
            "pose_driver": self.pose_driver_name,
            "pose_driven": self.pose_driven_name,
            "aim_constraint": self.aim_constraint_name,
            "orient_constraint": self.orient_constraint_name,
        }


def _test_node_names(side):
    u"""返回当前侧测试 Rig 的关键根节点。"""

    return {
        "jnt_group": name_utils.Name(
            type="grp",
            side=side,
            part=TEST_MODULE,
            function="jnt",
            index=1
        ).name,
        "ctrl_group": name_utils.Name(
            type="grp",
            side=side,
            part=TEST_MODULE,
            function="ctrl",
            index=1
        ).name,
        "aim_constraint": name_utils.Name(
            type="con",
            side=side,
            part=TEST_MODULE,
            function="aim",
            index=1
        ).name,
        "orient_constraint": name_utils.Name(
            type="con",
            side=side,
            part=TEST_MODULE,
            function="orient",
            index=1
        ).name,
    }


def delete_test(side=None):
    u"""删除单侧或双侧 Eye Rig Test。"""

    side_list = []

    if side is None:
        for current_side in SUPPORTED_SIDES:
            side_list.append(current_side)
    else:
        if side not in SUPPORTED_SIDES:
            raise ValueError(
                u"Eye Rig Test 只支持 lf / rt，当前值：{}".format(side)
            )

        side_list.append(side)

    for current_side in side_list:
        node_names = _test_node_names(
            current_side
        )

        delete_list = []

        for key_name in (
            "aim_constraint",
            "orient_constraint",
            "ctrl_group",
            "jnt_group"
        ):
            node_name = node_names[key_name]

            if cmds.objExists(node_name):
                delete_list.append(node_name)

        if delete_list:
            cmds.delete(delete_list)


def build(
    side="lf",
    ctrl_color=17,
    ctrl_size=1.0,
    ctrl_shape="circle",
    aim_ctrl_shape="shape_040",
    jnt_parent=None,
    ctrl_parent=None
):
    u"""构建单侧 Eye Rig Test。"""

    rig_object = EyeRigTest(
        side=side,
        jnt_parent=jnt_parent,
        ctrl_parent=ctrl_parent,
        ctrl_shape=ctrl_shape,
        aim_ctrl_shape=aim_ctrl_shape,
        ctrl_color=ctrl_color,
        ctrl_size=ctrl_size
    )

    rig_object.build()
    return rig_object


def build_both(
    ctrl_color=17,
    ctrl_size=1.0,
    ctrl_shape="circle",
    aim_ctrl_shape="shape_040",
    jnt_parent=None,
    ctrl_parent=None
):
    u"""一次构建左右两侧 Eye Rig Test。"""

    result = {}

    for side in SUPPORTED_SIDES:
        result[side] = build(
            side=side,
            ctrl_color=ctrl_color,
            ctrl_size=ctrl_size,
            ctrl_shape=ctrl_shape,
            aim_ctrl_shape=aim_ctrl_shape,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

    return result


def _distance(point_a, point_b):
    u"""返回两个 XYZ 点之间的距离。"""

    delta_x = point_a[0] - point_b[0]
    delta_y = point_a[1] - point_b[1]
    delta_z = point_a[2] - point_b[2]

    return (
        delta_x * delta_x
        + delta_y * delta_y
        + delta_z * delta_z
    ) ** 0.5


def validate(side="lf", tolerance=0.001):
    u"""
    检查 Main Ctrl 的位置和旋转轴心是否符合测试目标。

    重点：
        main_ctrl_at_iris
            Main Ctrl Transform 世界位置是否在 Iris Guide。
        main_ctrl_pivot_at_ball
            Main Ctrl Rotate Pivot 是否在 Ball Guide。
        main_driven_pivot_at_ball
            Aim 实际旋转层 Driven 的 Rotate Pivot 是否在 Ball Guide。
        joint_at_ball
            Eye Joint 是否在 Ball Guide。
        joint_translate_has_input
            Joint Translate 是否被外部节点驱动；正常应为 False。
    """

    if side not in SUPPORTED_SIDES:
        raise ValueError(
            u"Eye Rig Test 只支持 lf / rt，当前值：{}".format(side)
        )

    rig_object = EyeRigTest(
        side=side
    )
    rig_object.get_guides()

    main_ctrl = name_utils.Name(
        type="ctrl",
        side=side,
        part=TEST_MODULE,
        function="main",
        index=1
    ).name

    main_driven = main_ctrl.replace(
        "ctrl_",
        "driven_",
        1
    )

    eye_joint = name_utils.Name(
        type="jnt",
        side=side,
        part=TEST_MODULE,
        function="bind",
        index=1
    ).name

    required_nodes = [
        main_ctrl,
        main_driven,
        eye_joint,
    ]

    for node_name in required_nodes:
        if not cmds.objExists(node_name):
            raise RuntimeError(
                u"找不到测试节点：{}".format(node_name)
            )

    iris_position = rig_object._world_position(
        rig_object.guide_map["iris"]
    )
    ball_position = rig_object._world_position(
        rig_object.guide_map["ball"]
    )

    main_ctrl_position = rig_object._world_position(
        main_ctrl
    )
    joint_position = rig_object._world_position(
        eye_joint
    )

    main_ctrl_pivot = rig_object._world_rotate_pivot(
        main_ctrl
    )
    main_driven_pivot = rig_object._world_rotate_pivot(
        main_driven
    )

    translate_inputs = []

    for axis_name in ("X", "Y", "Z"):
        attr_name = eye_joint + ".translate" + axis_name
        input_nodes = cmds.listConnections(
            attr_name,
            source=True,
            destination=False
        ) or []

        for input_node in input_nodes:
            if input_node not in translate_inputs:
                translate_inputs.append(input_node)

    result = {
        "main_ctrl_at_iris": _distance(
            main_ctrl_position,
            iris_position
        ) <= tolerance,
        "main_ctrl_pivot_at_ball": _distance(
            main_ctrl_pivot,
            ball_position
        ) <= tolerance,
        "main_driven_pivot_at_ball": _distance(
            main_driven_pivot,
            ball_position
        ) <= tolerance,
        "joint_at_ball": _distance(
            joint_position,
            ball_position
        ) <= tolerance,
        "joint_translate_has_input": bool(
            translate_inputs
        ),
    }

    print(u"\n========== Eye Rig Test Validate ==========")

    for key_name in (
        "main_ctrl_at_iris",
        "main_ctrl_pivot_at_ball",
        "main_driven_pivot_at_ball",
        "joint_at_ball",
        "joint_translate_has_input"
    ):
        print(u"{}: {}".format(
            key_name,
            result[key_name]
        ))

    print(u"===========================================\n")

    return result
