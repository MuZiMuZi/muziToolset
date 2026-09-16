# coding=utf-8
u"""
EyeModule：眼球 Aim 绑定模块。

当前模块只负责眼球本体，不负责 Eyelid。

Guide 语义：
    loc_<side>_eye_ball_001
        眼球真实旋转中心，同时用于创建 Eye Joint。
    loc_<side>_eye_iris_001
        眼球前方参考点，用于放置 Eye Main Controller。
    loc_<side>_eye_aim_001
        目光目标点，用于放置 Eye Aim Controller。

最终控制结构：

    ctrl_<side>_eye_aim_001
        -> output_<side>_eye_aim_001
        -> Aim Constraint
        -> driven_<side>_eye_main_001
        -> ctrl_<side>_eye_main_001
        -> output_<side>_eye_main_001
        -> Pose Driver
        -> Pose Driven
        -> Orient Constraint
        -> jnt_<side>_eye_bind_001

核心原则：
    1. Main Controller 的可见位置保持在 Iris Guide。
    2. Main Controller 相关旋转层的 Rotate Pivot 位于 Ball Guide。
    3. Aim 只负责旋转，不改变 Main Controller 的初始位置。
    4. Eye Joint 只接收 Rotate，不接收 Translate。
    5. Pose Driver / Pose Driven 为后续 Eyelid、RBF、Corrective 保留稳定接口。
"""

import maya.cmds as cmds

from .. import rig_module
from . import face_guide_config
from ...core.common import name_utils, hierarchy_utils


SUPPORTED_SIDES = ("lf", "rt")


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
        u"""初始化眼球 Aim 绑定模块。"""

        super(EyeModule, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

        if self.side not in SUPPORTED_SIDES:
            raise ValueError(
                u"Eye Module 只支持 lf / rt，当前值：{}".format(self.side)
            )

        # Controller 外观参数。
        # 默认 Shape 保留当前 EyeModule 使用的正式配置。
        self.ctrl_shape = ctrl_shape
        self.aim_ctrl_shape = aim_ctrl_shape
        self.ctrl_color = ctrl_color
        self.ctrl_size = ctrl_size
        self.ctrl_axis = ctrl_axis
        self.aim_ctrl_axis = aim_ctrl_axis

        self.guide_map = {}

        self.eye_jnt_name = None
        self.eye_jnt_object = None

        self.main_ctrl_name = None
        self.main_ctrl_object = None

        self.aim_ctrl_name = None
        self.aim_ctrl_object = None

        self.world_up_name = None
        self.pose_driver_name = None
        self.pose_driven_name = None

        self.aim_constraint_name = None
        self.pose_constraint_name = None
        self.orient_constraint_name = None

    # =========================================================================
    # 基础工具
    # =========================================================================

    @staticmethod
    def _node_name(node):
        u"""统一把 PyNode / Maya Node 转换成 maya.cmds 可使用的字符串名称。"""

        if node is None:
            return None

        return str(node)

    @staticmethod
    def _short_name(node_name):
        u"""返回不包含 DAG Path 和 Namespace 的短名称。"""

        short_name = str(node_name)

        if "|" in short_name:
            short_name = short_name.split("|")[-1]

        if ":" in short_name:
            short_name = short_name.rsplit(":", 1)[-1]

        return short_name

    @staticmethod
    def _world_position(node_name):
        u"""返回节点世界空间位置。"""

        return cmds.xform(
            str(node_name),
            query=True,
            worldSpace=True,
            translation=True
        )

    @staticmethod
    def _world_rotate_pivot(node_name):
        u"""返回节点世界空间 Rotate Pivot。"""

        return cmds.xform(
            str(node_name),
            query=True,
            worldSpace=True,
            rotatePivot=True
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

    @staticmethod
    def _set_world_pivot(node_name, pivot_position):
        u"""
        设置 Transform 的 Rotate / Scale Pivot，同时保持当前世界位置不变化。

        这个方法是 Eye Main 保持在 Iris、但绕 Ball 旋转的关键。
        """

        node_name = str(node_name)

        cmds.xform(
            node_name,
            worldSpace=True,
            preserve=True,
            rotatePivot=(
                pivot_position[0],
                pivot_position[1],
                pivot_position[2]
            )
        )

        cmds.xform(
            node_name,
            worldSpace=True,
            preserve=True,
            scalePivot=(
                pivot_position[0],
                pivot_position[1],
                pivot_position[2]
            )
        )

    @staticmethod
    def _same_position(position_a, position_b, tolerance=0.001):
        u"""比较两个世界坐标是否在允许误差内一致。"""

        for index in range(3):
            if abs(position_a[index] - position_b[index]) > tolerance:
                return False

        return True

    # =========================================================================
    # Guide
    # =========================================================================

    def _expected_guides(self):
        u"""返回当前侧 Eye Ball / Iris / Aim 的固定语义 Guide。"""

        return {
            "ball": face_guide_config.get_eye_locator(
                self.side,
                "ball"
            ),
            "iris": face_guide_config.get_eye_locator(
                self.side,
                "iris"
            ),
            "aim": face_guide_config.get_eye_locator(
                self.side,
                "aim"
            ),
        }

    def get_guides(self):
        u"""
        获取 Eye Ball / Iris / Aim 三个固定语义 Guide。

        Eye 不依赖列表顺序判断语义。
        外部传入 Guide 时按照节点标准名称匹配 ball / iris / aim；
        没有传入 Guide 时直接读取 face_guide_config 中的固定名称。
        """

        expected_guides = self._expected_guides()
        source_guides = super(EyeModule, self).get_guides()

        self.guide_map = {}

        if source_guides:
            for guide_name in source_guides:
                short_name = self._short_name(
                    guide_name
                )
                normalized_name = face_guide_config.normalize_legacy_locator_name(
                    short_name
                )

                matched_function = None

                for function_name in ("ball", "iris", "aim"):
                    expected_name = expected_guides[function_name]

                    if normalized_name == expected_name:
                        matched_function = function_name
                        break

                if matched_function is None:
                    raise RuntimeError(
                        u"Eye Guide 名称不符合当前语义规则：{}".format(
                            guide_name
                        )
                    )

                if matched_function in self.guide_map:
                    raise RuntimeError(
                        u"Eye Guide 语义重复：{}".format(
                            matched_function
                        )
                    )

                self.guide_map[matched_function] = str(
                    guide_name
                )

        else:
            if self.guide is not None:
                raise RuntimeError(
                    u"Eye Module 没有可用的 Guide。"
                )

            for function_name in ("ball", "iris", "aim"):
                guide_name = expected_guides[function_name]

                if not cmds.objExists(guide_name):
                    raise RuntimeError(
                        u"找不到 Eye Guide：{}".format(
                            guide_name
                        )
                    )

                self.guide_map[function_name] = guide_name

        for function_name in ("ball", "iris", "aim"):
            if function_name not in self.guide_map:
                raise RuntimeError(
                    u"Eye Module 缺少 {} Guide。".format(
                        function_name
                    )
                )

        self.guide_list = [
            self.guide_map["ball"],
            self.guide_map["iris"],
            self.guide_map["aim"],
        ]

        return self.guide_list

    # =========================================================================
    # Step 02 / Step 03 输出创建
    # =========================================================================

    def create_joints(self):
        u"""在 Eye Ball Guide 位置创建眼球绑定 Joint。"""

        self.eye_jnt_name = name_utils.Name(
            type="jnt",
            side=self.side,
            part=self.module,
            function="bind",
            index=1
        ).name

        self.eye_jnt_object = self.create_joint(
            name=self.eye_jnt_name,
            guide=self.guide_map["ball"]
        )

        return [
            self.eye_jnt_name
        ]

    def create_ctrls(self):
        u"""
        创建 Eye Main 与 Eye Aim 两个控制器。

        Main Controller：
            使用 Iris Guide 放置，所以 Controller 可见位置始终位于 Iris。
        Aim Controller：
            使用 Aim Guide 放置，动画师移动它控制视线方向。
        """

        self.main_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="main",
            index=1
        ).name

        self.main_ctrl_object = self.create_ctrl(
            name=self.main_ctrl_name,
            guide=self.guide_map["iris"],
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
            guide=self.guide_map["aim"],
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

    def _main_pivot_nodes(self):
        u"""返回 Eye Main 中应该使用 Ball 作为旋转轴心的层级节点。"""

        if not self.main_ctrl_name:
            return []

        node_names = [
            self.main_ctrl_name.replace("ctrl_", "driven_", 1),
            self.main_ctrl_name.replace("ctrl_", "space_", 1),
            self.main_ctrl_name.replace("ctrl_", "connect_", 1),
            self.main_ctrl_name.replace("ctrl_", "offset_", 1),
            self.main_ctrl_name,
            self.main_ctrl_name.replace("ctrl_", "subctrl_", 1),
            self.main_ctrl_name.replace("ctrl_", "output_", 1),
        ]

        return node_names

    def _set_main_rotation_pivots(self):
        u"""
        保持 Main Controller 位于 Iris，只把相关旋转轴心设置到 Eye Ball。

        Zero Group 保持原始 Iris Rest Position，不修改它的 Pivot。
        """

        if not self.guide_map:
            self.get_guides()

        if not self.main_ctrl_name:
            self.main_ctrl_name = name_utils.Name(
                type="ctrl",
                side=self.side,
                part=self.module,
                function="main",
                index=1
            ).name

        ball_position = self._world_position(
            self.guide_map["ball"]
        )

        pivot_nodes = self._main_pivot_nodes()

        for node_name in pivot_nodes:
            if not cmds.objExists(node_name):
                continue

            self._set_world_pivot(
                node_name,
                ball_position
            )

    def setup_hierarchy(self):
        u"""整理 Eye Joint、Main Ctrl 和 Aim Ctrl 的模块层级。"""

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

        # 层级完成以后再设置世界空间 Pivot，避免 Parent 操作影响最终结果。
        self._set_main_rotation_pivots()

        return self.jnt_master_grp, self.ctrl_master_grp

    # =========================================================================
    # Step 04 连接
    # =========================================================================

    def load_outputs(self):
        u"""读取前面步骤已经创建完成的 Eye Joint / Controller 输出。"""

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
                    u"找不到已经生成的 Eye 输出：{}".format(
                        node_name
                    )
                )

        # 从旧场景直接进入 Step 04 时也再次校正 Pivot。
        self.get_guides()
        self._set_main_rotation_pivots()

        return required_nodes

    def _connection_names(self):
        u"""生成 Eye Rig 连接层使用的稳定节点名称。"""

        self.world_up_name = name_utils.Name(
            type="grp",
            side=self.side,
            part=self.module,
            function="worldup",
            index=1
        ).name

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

        self.aim_constraint_name = name_utils.Name(
            type="con",
            side=self.side,
            part=self.module,
            function="aim",
            index=1
        ).name

        self.pose_constraint_name = name_utils.Name(
            type="con",
            side=self.side,
            part=self.module,
            function="pose",
            index=1
        ).name

        self.orient_constraint_name = name_utils.Name(
            type="con",
            side=self.side,
            part=self.module,
            function="orient",
            index=1
        ).name

        return {
            "world_up": self.world_up_name,
            "pose_driver": self.pose_driver_name,
            "pose_driven": self.pose_driven_name,
            "aim_constraint": self.aim_constraint_name,
            "pose_constraint": self.pose_constraint_name,
            "orient_constraint": self.orient_constraint_name,
        }

    def delete_connections(self):
        u"""
        删除当前侧 Eye Step 04 的连接节点。

        不删除 Joint、Main Ctrl、Aim Ctrl，方便用户回到前面步骤调整后重新连接。
        """

        connection_names = self._connection_names()

        delete_order = [
            connection_names["orient_constraint"],
            connection_names["pose_constraint"],
            connection_names["aim_constraint"],
            connection_names["pose_driven"],
            connection_names["pose_driver"],
            connection_names["world_up"],
        ]

        for node_name in delete_order:
            if cmds.objExists(node_name):
                cmds.delete(node_name)

    def _create_world_up(self):
        u"""创建稳定的 Eye World Up Transform。"""

        if not self.guide_map:
            self.get_guides()

        if self.ctrl_master_grp is None:
            self.setup_module_groups()

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

    def _create_pose_nodes(self):
        u"""
        创建 Pose Driver / Pose Driven。

        两个节点都位于 Eye Ball，且处于相同父空间。
        Pose Driver 读取 Main Output 的最终世界旋转；
        Pose Driven 当前先直接继承 Driver Rotate，后续可以替换成 RBF / corrective solver。
        """

        if not self.guide_map:
            self.get_guides()

        if self.ctrl_master_grp is None:
            self.setup_module_groups()

        ctrl_master_grp = self._node_name(
            self.ctrl_master_grp
        )

        self.pose_driver_name = cmds.createNode(
            "transform",
            name=self.pose_driver_name,
            parent=ctrl_master_grp
        )

        self.pose_driven_name = cmds.createNode(
            "transform",
            name=self.pose_driven_name,
            parent=ctrl_master_grp
        )

        self._set_world_matrix(
            self.pose_driver_name,
            self.guide_map["ball"]
        )

        self._set_world_matrix(
            self.pose_driven_name,
            self.guide_map["ball"]
        )

        rotate_order = cmds.getAttr(
            self.pose_driver_name + ".rotateOrder"
        )

        cmds.setAttr(
            self.pose_driven_name + ".rotateOrder",
            rotate_order
        )

        for axis_name in ("X", "Y", "Z"):
            cmds.connectAttr(
                self.pose_driver_name + ".rotate" + axis_name,
                self.pose_driven_name + ".rotate" + axis_name,
                force=True
            )

        return self.pose_driver_name, self.pose_driven_name

    def connect_rig(self):
        u"""
        建立正式 Eye Rig 连接。

        流程：
            Aim Output
                -> Aim Constraint
                -> Main Driven
                -> Main Ctrl / SubCtrl / Output
                -> Pose Driver
                -> Pose Driven
                -> Orient Constraint
                -> Eye Joint

        重新执行时只重建 Step 04 连接层，不删除前面创建并调整过的 Controller / Joint。
        """

        if not self.eye_jnt_name or not self.main_ctrl_name or not self.aim_ctrl_name:
            self.load_outputs()

        if not self.guide_map:
            self.get_guides()

        self._set_main_rotation_pivots()
        self._connection_names()
        self.delete_connections()

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

        # Aim 使用 Main Driven 的 Ball Pivot 作为真实旋转中心。
        # maintainOffset=True 保留当前 Guide / Controller 初始姿态，避免构建时发生跳动。
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

        self._create_pose_nodes()

        # Main Output 只把最终 Orientation 传给 Pose Driver，不传位移。
        self.pose_constraint_name = cmds.orientConstraint(
            main_output,
            self.pose_driver_name,
            maintainOffset=True,
            weight=1,
            name=self.pose_constraint_name
        )[0]

        # Joint 最终同样只接收 Orientation。
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
            "pose_constraint": self.pose_constraint_name,
            "orient_constraint": self.orient_constraint_name,
        }


# =============================================================================
# Maya 直接测试入口
# =============================================================================


def build(
    side="lf",
    ctrl_shape="shape_016",
    aim_ctrl_shape="shape_040",
    ctrl_color=17,
    ctrl_size=1.0,
    ctrl_axis="X+",
    aim_ctrl_axis="Z+",
    jnt_parent=None,
    ctrl_parent=None
):
    u"""直接构建单侧正式 EyeModule，方便 Maya 中快速测试。"""

    rig_object = EyeModule(
        side=side,
        jnt_parent=jnt_parent,
        ctrl_parent=ctrl_parent,
        ctrl_shape=ctrl_shape,
        aim_ctrl_shape=aim_ctrl_shape,
        ctrl_color=ctrl_color,
        ctrl_size=ctrl_size,
        ctrl_axis=ctrl_axis,
        aim_ctrl_axis=aim_ctrl_axis
    )

    rig_object.build()
    return rig_object


def build_both(
    ctrl_shape="shape_016",
    aim_ctrl_shape="shape_040",
    ctrl_color=17,
    ctrl_size=1.0,
    ctrl_axis="X+",
    aim_ctrl_axis="Z+",
    jnt_parent=None,
    ctrl_parent=None
):
    u"""依次构建左右两侧正式 EyeModule。"""

    result = {}

    for side in SUPPORTED_SIDES:
        result[side] = build(
            side=side,
            ctrl_shape=ctrl_shape,
            aim_ctrl_shape=aim_ctrl_shape,
            ctrl_color=ctrl_color,
            ctrl_size=ctrl_size,
            ctrl_axis=ctrl_axis,
            aim_ctrl_axis=aim_ctrl_axis,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

    return result


def delete_connections(side="lf"):
    u"""删除指定侧 Eye Step 04 连接层，保留 Joint / Controller。"""

    rig_object = EyeModule(
        side=side
    )
    rig_object.delete_connections()


def validate(side="lf"):
    u"""
    检查 EyeModule 的关键结构。

    重点验证：
        Main Ctrl 是否位于 Iris。
        Main Ctrl / Main Driven Pivot 是否位于 Ball。
        Eye Joint 是否位于 Ball。
        Joint Translate 是否没有输入连接。
        Aim / Pose / Orient 三段连接是否存在。
    """

    if side not in SUPPORTED_SIDES:
        raise ValueError(
            u"Eye Module 只支持 lf / rt，当前值：{}".format(side)
        )

    ball_guide = face_guide_config.get_eye_locator(
        side,
        "ball"
    )
    iris_guide = face_guide_config.get_eye_locator(
        side,
        "iris"
    )

    main_ctrl = name_utils.Name(
        type="ctrl",
        side=side,
        part="eye",
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
        part="eye",
        function="bind",
        index=1
    ).name

    connection_object = EyeModule(
        side=side
    )
    connection_names = connection_object._connection_names()

    required_nodes = [
        ball_guide,
        iris_guide,
        main_ctrl,
        main_driven,
        eye_joint,
    ]

    for node_name in required_nodes:
        if not cmds.objExists(node_name):
            raise RuntimeError(
                u"Eye Validate 找不到节点：{}".format(node_name)
            )

    ball_position = EyeModule._world_position(
        ball_guide
    )
    iris_position = EyeModule._world_position(
        iris_guide
    )
    main_position = EyeModule._world_position(
        main_ctrl
    )
    joint_position = EyeModule._world_position(
        eye_joint
    )
    main_pivot = EyeModule._world_rotate_pivot(
        main_ctrl
    )
    driven_pivot = EyeModule._world_rotate_pivot(
        main_driven
    )

    joint_translate_has_input = False

    for axis_name in ("X", "Y", "Z"):
        source_connections = cmds.listConnections(
            eye_joint + ".translate" + axis_name,
            source=True,
            destination=False,
            plugs=True
        ) or []

        if source_connections:
            joint_translate_has_input = True
            break

    result = {
        "main_ctrl_at_iris": EyeModule._same_position(
            main_position,
            iris_position
        ),
        "main_ctrl_pivot_at_ball": EyeModule._same_position(
            main_pivot,
            ball_position
        ),
        "main_driven_pivot_at_ball": EyeModule._same_position(
            driven_pivot,
            ball_position
        ),
        "joint_at_ball": EyeModule._same_position(
            joint_position,
            ball_position
        ),
        "aim_constraint_exists": cmds.objExists(
            connection_names["aim_constraint"]
        ),
        "pose_constraint_exists": cmds.objExists(
            connection_names["pose_constraint"]
        ),
        "orient_constraint_exists": cmds.objExists(
            connection_names["orient_constraint"]
        ),
        "joint_translate_has_input": joint_translate_has_input,
    }

    print(u"\n========== EyeModule Validate : {} ==========".format(side))

    for key_name in (
        "main_ctrl_at_iris",
        "main_ctrl_pivot_at_ball",
        "main_driven_pivot_at_ball",
        "joint_at_ball",
        "aim_constraint_exists",
        "pose_constraint_exists",
        "orient_constraint_exists",
        "joint_translate_has_input"
    ):
        print(u"{} : {}".format(
            key_name,
            result[key_name]
        ))

    print(u"=============================================\n")

    return result
