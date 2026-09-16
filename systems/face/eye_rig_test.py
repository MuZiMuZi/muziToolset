# coding=utf-8
u"""
Eye Rig Test
============

独立眼球绑定测试模块。

用途：
    1. 不连接 Face Rig UI。
    2. 不修改正式 EyeModule。
    3. 直接复用现有 Eye Guide、RigModule 和 Controller 系统。
    4. 验证 Eye Main Pivot、Aim、World Up、Pose Driver 和 Joint 纯旋转驱动。

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
    Eye Main Transform / Pivot 位于 Eye Ball Guide。
    Eye Main Curve CV 单独偏移到 Iris Guide。
    World Up 使用独立 Transform + objectrotation。
    Eye Joint 只接收 Rotate，不接收 Translate。
"""

import maya.cmds as cmds

from . import eye_module
from ...core.common import name_utils


TEST_MODULE = "eye_test"
SUPPORTED_SIDES = ("lf", "rt")


class EyeRigTest(eye_module.EyeModule):
    u"""用于 Maya 场景直接测试的独立 Eye Rig。"""

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
        u"""统一把 PyNode / Maya Node 转换成 maya.cmds 可使用的字符串名称。"""

        if node is None:
            return None

        return str(node)

    def build(self):
        u"""删除当前侧旧测试节点后重新构建。"""

        delete_test(self.side)
        super(EyeRigTest, self).build()
        return self

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

    @staticmethod
    def _get_local_position(world_target, local_parent):
        u"""获取 world_target 在 local_parent 空间中的位置。"""

        world_target = str(world_target)
        local_parent = str(local_parent)

        temp_node = cmds.createNode(
            "transform",
            name="tmp_eye_test_local_position#"
        )

        try:
            world_position = cmds.xform(
                world_target,
                query=True,
                worldSpace=True,
                translation=True
            )

            cmds.xform(
                temp_node,
                worldSpace=True,
                translation=world_position
            )

            cmds.parent(
                temp_node,
                local_parent
            )

            local_position = cmds.getAttr(
                temp_node + ".translate"
            )[0]

        finally:
            if cmds.objExists(temp_node):
                cmds.delete(temp_node)

        return local_position

    @staticmethod
    def _offset_curve_shapes(transform_name, offset_value):
        u"""只移动 Transform 下的 NurbsCurve CV，不修改 Transform。"""

        transform_name = str(transform_name)

        shape_list = cmds.listRelatives(
            transform_name,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        ) or []

        for shape_name in shape_list:
            if cmds.nodeType(shape_name) != "nurbsCurve":
                continue

            cv_list = cmds.ls(
                shape_name + ".cv[*]",
                flatten=True
            ) or []

            if not cv_list:
                continue

            cmds.move(
                offset_value[0],
                offset_value[1],
                offset_value[2],
                cv_list,
                relative=True,
                objectSpace=True
            )

    def create_ctrls(self):
        u"""
        创建 Main / Aim 控制器，并把 Main 的真实旋转中心改到 Eye Ball。

        EyeModule 原始逻辑先按 Iris 创建 Main Ctrl。
        这里在创建完成后把整个 Main Hierarchy 移到 Ball，
        再只移动 Curve CV 回到 Iris。
        """

        super(EyeRigTest, self).create_ctrls()

        main_zero = self._node_name(
            self.main_ctrl_object.zero_grp
        )
        main_ctrl = self._node_name(
            self.main_ctrl_object.ctrl
        )

        self._set_world_matrix(
            main_zero,
            self.guide_map["ball"]
        )

        iris_local_position = self._get_local_position(
            self.guide_map["iris"],
            main_ctrl
        )

        self.main_ctrl_object.set_ctrl_offset(
            offset_x=iris_local_position[0],
            offset_y=iris_local_position[1],
            offset_z=iris_local_position[2]
        )

        if self.main_ctrl_object.sub_ctrl:
            self._offset_curve_shapes(
                self._node_name(self.main_ctrl_object.sub_ctrl),
                iris_local_position
            )

        return [
            self.main_ctrl_name,
            self.aim_ctrl_name,
        ]

    def _create_world_up(self, source_node):
        u"""创建独立稳定 World Up Transform。"""

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
            source_node
        )

        return self.world_up_name

    def _create_pose_chain(self, main_output):
        u"""创建 Pose Driver / Pose Driven 中间层。"""

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
        建立测试版最终连接。

        Aim Output
            -> Aim Constraint
            -> Main Driven
            -> Main Output
            -> Pose Driver / Pose Driven
            -> Orient Constraint
            -> Eye Joint
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

        world_up = self._create_world_up(
            main_output
        )

        self.aim_constraint_name = name_utils.Name(
            type="con",
            side=self.side,
            part=self.module,
            function="aim",
            index=1
        ).name

        if cmds.objExists(self.aim_constraint_name):
            cmds.delete(self.aim_constraint_name)

        cmds.aimConstraint(
            aim_output,
            main_driven,
            maintainOffset=False,
            offset=(0, 0, 0),
            weight=1,
            aimVector=(1, 0, 0),
            upVector=(0, 1, 0),
            worldUpType="objectrotation",
            worldUpVector=(0, 1, 0),
            worldUpObject=world_up,
            name=self.aim_constraint_name
        )

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

        cmds.orientConstraint(
            self.pose_driven_name,
            self.eye_jnt_name,
            maintainOffset=False,
            weight=1,
            name=self.orient_constraint_name
        )

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


def _get_test_node_names(side):
    u"""返回当前侧测试模块需要清理的关键节点。"""

    result = []

    node_data = (
        ("grp", "jnt"),
        ("grp", "ctrl"),
        ("con", "aim"),
        ("con", "orient"),
    )

    for node_type, function_name in node_data:
        node_name = name_utils.Name(
            type=node_type,
            side=side,
            part=TEST_MODULE,
            function=function_name,
            index=1
        ).name
        result.append(node_name)

    return result


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
        delete_list = []
        node_names = _get_test_node_names(
            current_side
        )

        for node_name in node_names:
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


def validate(side="lf"):
    u"""检查测试绑定关键结构，并把结果打印到 Script Editor。"""

    if side not in SUPPORTED_SIDES:
        raise ValueError(
            u"Eye Rig Test 只支持 lf / rt，当前值：{}".format(side)
        )

    main_ctrl = name_utils.Name(
        type="ctrl",
        side=side,
        part=TEST_MODULE,
        function="main",
        index=1
    ).name

    aim_ctrl = name_utils.Name(
        type="ctrl",
        side=side,
        part=TEST_MODULE,
        function="aim",
        index=1
    ).name

    eye_jnt = name_utils.Name(
        type="jnt",
        side=side,
        part=TEST_MODULE,
        function="bind",
        index=1
    ).name

    pose_driver = name_utils.Name(
        type="driver",
        side=side,
        part=TEST_MODULE,
        function="pose",
        index=1
    ).name

    pose_driven = name_utils.Name(
        type="driven",
        side=side,
        part=TEST_MODULE,
        function="pose",
        index=1
    ).name

    translate_inputs = []

    for axis_name in ("X", "Y", "Z"):
        plug_name = eye_jnt + ".translate" + axis_name
        input_list = cmds.listConnections(
            plug_name,
            source=True,
            destination=False,
            plugs=True
        ) or []

        for input_plug in input_list:
            translate_inputs.append(input_plug)

    result = {
        "main_ctrl_exists": cmds.objExists(main_ctrl),
        "aim_ctrl_exists": cmds.objExists(aim_ctrl),
        "joint_exists": cmds.objExists(eye_jnt),
        "pose_driver_exists": cmds.objExists(pose_driver),
        "pose_driven_exists": cmds.objExists(pose_driven),
        "joint_translate_has_input": bool(translate_inputs),
    }

    print(u"=" * 60)
    print(u"Eye Rig Test Validate : {}".format(side))

    for key_name in (
        "main_ctrl_exists",
        "aim_ctrl_exists",
        "joint_exists",
        "pose_driver_exists",
        "pose_driven_exists",
        "joint_translate_has_input",
    ):
        print(u"{} : {}".format(
            key_name,
            result[key_name]
        ))

    print(u"=" * 60)

    return result
