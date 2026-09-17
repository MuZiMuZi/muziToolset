# coding=utf-8
u"""
EyeModule：正式眼球 Aim 绑定模块。

Guide：
    loc_<side>_eye_ball_001
        眼球真实旋转中心，同时用于创建 Eye Joint。
    loc_<side>_eye_iris_001
        Eye Main Controller 的可见位置。
    loc_<side>_eye_aim_001
        Eye Aim Controller 的位置。

正式驱动结构：

    ctrl_<side>_eye_aim_001
        -> output_<side>_eye_aim_001
        -> Aim Constraint
        -> driven_<side>_eye_main_001
        -> ctrl_<side>_eye_main_001
        -> output_<side>_eye_main_001
        -> driver_<side>_eye_pose_001
        -> driven_<side>_eye_pose_001
        -> Orient Constraint
        -> jnt_<side>_eye_bind_001

关键规则：
    1. Main Ctrl Transform 保持在 Iris Guide。
    2. Main Ctrl 相关旋转层的 Rotate Pivot 位于 Ball Guide。
    3. Aim 只驱动旋转，不驱动位移。
    4. Eye Joint 只接收 Rotate，不接收 Translate。
    5. Pose Driver / Pose Driven 作为 Eyelid、RBF、Corrective 的稳定接口。
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
        u"""
        初始化正式 Eye Rig。

        Args:
            module (str):
                当前 Maya / Rig 操作使用的 `module` 名称或标记。
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            guide (str):
                需要查询或处理的 Guide Transform 名称。
            jnt_parent (str | None):
                新建 Jnt Chain 的父 Jnt / Parent Transform；None 表示保持在世界层级。
            ctrl_parent (object):
                当前方法执行 Maya / Rig 操作时使用的 `ctrl_parent` 数据。
            ctrl_shape (str):
                当前 Maya / Rig 操作使用的 `ctrl_shape` 名称或标记。
            aim_ctrl_shape (str):
                当前 Maya / Rig 操作使用的 `aim_ctrl_shape` 名称或标记。
            ctrl_color (int):
                当前 Maya / Rig 操作使用的 `ctrl_color` 整数参数。
            ctrl_size (float):
                当前 Maya / Rig 计算使用的 `ctrl_size` 数值参数。
            ctrl_axis (str):
                当前 Maya / Rig 操作使用的 `ctrl_axis` 名称或标记。
            aim_ctrl_axis (str):
                当前 Maya / Rig 操作使用的 `aim_ctrl_axis` 名称或标记。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """

        # -------------------------------------------------------------------------
        # Step 01：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
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

        # Controller 外观设置。
        self.ctrl_shape = ctrl_shape
        self.aim_ctrl_shape = aim_ctrl_shape
        self.ctrl_color = ctrl_color
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.ctrl_size = ctrl_size
        self.ctrl_axis = ctrl_axis
        self.aim_ctrl_axis = aim_ctrl_axis

        self.guide_map = {}

        self.eye_jnt_name = None
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.eye_jnt_object = None

        self.main_ctrl_name = None
        self.main_ctrl_object = None

        self.aim_ctrl_name = None
        self.aim_ctrl_object = None

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.world_up_name = None
        self.pose_driver_name = None
        self.pose_driven_name = None

        self.aim_constraint_name = None
        self.pose_constraint_name = None
        # -------------------------------------------------------------------------
        # Step 05：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.orient_constraint_name = None

    # =========================================================================
    # 通用工具
    # =========================================================================

    @staticmethod
    def _node_name(node):
        u"""把 PyNode / Maya Node 统一转换成 maya.cmds 使用的字符串名称。"""

        if node is None:
            return None

        return str(node)

    @staticmethod
    def _short_name(node_name):
        u"""返回去掉 DAG Path 和 Namespace 的短名称。"""

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
        u"""把 source 的 World Matrix 复制给 node。"""

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
        设置 Transform 的 Rotate / Scale Pivot，同时保持 Transform 当前世界位置。
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
        u"""比较两个世界空间坐标是否一致。"""

        for index in range(3):
            if abs(position_a[index] - position_b[index]) > tolerance:
                return False

        return True

    def _ensure_module_groups(self):
        u"""
        确保当前 Eye Module 的 Jnt / Ctrl Master Group 已经存在。

        这里直接调用 RigModule.setup_hierarchy()，只创建模块根组，
        不调用 EyeModule.setup_hierarchy()，因此也适用于从已有场景直接进入 Step 04。
        """

        jnt_group_valid = False
        ctrl_group_valid = False

        if self.jnt_master_grp is not None:
            jnt_group_valid = cmds.objExists(
                self._node_name(self.jnt_master_grp)
            )

        if self.ctrl_master_grp is not None:
            ctrl_group_valid = cmds.objExists(
                self._node_name(self.ctrl_master_grp)
            )

        if not jnt_group_valid or not ctrl_group_valid:
            rig_module.RigModule.setup_hierarchy(self)

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

                Returns:
                    object:
                        当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """

        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        expected_guides = self._expected_guides()
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        source_guides = super(EyeModule, self).get_guides()

        self.guide_map = {}

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.guide_list = [
            self.guide_map["ball"],
            self.guide_map["iris"],
            self.guide_map["aim"],
        ]

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.guide_list

    # =========================================================================
    # Joint / Controller
    # =========================================================================

    def create_joints(self):
        u"""

                在 Eye Ball Guide 创建眼球绑定 Joint。

                Returns:
                    list:
                        按当前 API 约定顺序返回的结果列表。

        """

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

                创建 Eye Main / Eye Aim Controller。

                Main Ctrl 使用 Iris Guide 创建，因此可见位置保持在 Iris。
                Aim Ctrl 使用 Aim Guide 创建。

                Returns:
                    list:
                        按当前 API 约定顺序返回的结果列表。

        """

        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.main_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="main",
            index=1
        ).name

        # -------------------------------------------------------------------------
        # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.main_ctrl_object = self.create_ctrl(
            name=self.main_ctrl_name,
            guide=self.guide_map["iris"],
            shape_name=self.ctrl_shape,
            ctrl_color=self.ctrl_color,
            ctrl_size=self.ctrl_size,
            ctrl_axis=self.ctrl_axis,
            create_hierarchy=True
        )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.aim_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="aim",
            index=1
        ).name

        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.aim_ctrl_object = self.create_ctrl(
            name=self.aim_ctrl_name,
            guide=self.guide_map["aim"],
            shape_name=self.aim_ctrl_shape,
            ctrl_color=self.ctrl_color,
            ctrl_size=self.ctrl_size,
            ctrl_axis=self.aim_ctrl_axis,
            create_hierarchy=True
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return [
            self.main_ctrl_name,
            self.aim_ctrl_name,
        ]

    def _main_pivot_nodes(self):
        u"""返回 Main Controller 中需要以 Ball 为轴心的节点。"""

        if not self.main_ctrl_name:
            return []

        return [
            self.main_ctrl_name.replace("ctrl_", "driven_", 1),
            self.main_ctrl_name.replace("ctrl_", "space_", 1),
            self.main_ctrl_name.replace("ctrl_", "connect_", 1),
            self.main_ctrl_name.replace("ctrl_", "offset_", 1),
            self.main_ctrl_name,
            self.main_ctrl_name.replace("ctrl_", "subctrl_", 1),
            self.main_ctrl_name.replace("ctrl_", "output_", 1),
        ]

    def _set_main_rotation_pivots(self):
        u"""
        保持 Main Controller 位于 Iris，只把相关 Rotate Pivot 设置到 Ball。
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
        u"""

                整理 Eye Joint、Main Ctrl、Aim Ctrl 的模块层级。

                Returns:
                    tuple:
                        按当前 API 约定组织的结果元组。

        """

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

        # 完成最终 Parent 后再设置 World Pivot。
        self._set_main_rotation_pivots()

        return self.jnt_master_grp, self.ctrl_master_grp

    # =========================================================================
    # Step 04 输出读取 / 连接
    # =========================================================================

    def load_outputs(self):
        u"""

                读取已经创建好的 Eye Joint / Controller 输出。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """

        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 03：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for node_name in required_nodes:
            if not cmds.objExists(node_name):
                raise RuntimeError(
                    u"找不到已经生成的 Eye 输出：{}".format(
                        node_name
                    )
                )

        self.get_guides()
        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self._ensure_module_groups()
        self._set_main_rotation_pivots()

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return required_nodes

    def _connection_names(self):
        u"""生成当前侧 Eye Step 04 的稳定连接节点名。"""

        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.world_up_name = name_utils.Name(
            type="grp",
            side=self.side,
            part=self.module,
            function="worldup",
            index=1
        ).name

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.orient_constraint_name = name_utils.Name(
            type="con",
            side=self.side,
            part=self.module,
            function="orient",
            index=1
        ).name

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return {
            "world_up": self.world_up_name,
            "pose_driver": self.pose_driver_name,
            "pose_driven": self.pose_driven_name,
            "aim_constraint": self.aim_constraint_name,
            "pose_constraint": self.pose_constraint_name,
            "orient_constraint": self.orient_constraint_name,
        }

    @staticmethod
    def _delete_constraints(node_name, constraint_types):
        u"""删除指定节点上的旧约束，用于兼容旧 Eye 版本。"""

        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not node_name:
            return

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not cmds.objExists(node_name):
            return

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        delete_nodes = []

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for constraint_type in constraint_types:
            constraint_nodes = cmds.listConnections(
                node_name,
                source=True,
                destination=False,
                type=constraint_type
            ) or []

            for constraint_node in constraint_nodes:
                if constraint_node not in delete_nodes:
                    delete_nodes.append(constraint_node)

        # -------------------------------------------------------------------------
        # Step 05：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for constraint_node in delete_nodes:
            if cmds.objExists(constraint_node):
                cmds.delete(constraint_node)

    def delete_connections(self):
        u"""
        删除当前侧 Eye 的 Step 04 连接层。

        Joint / Controller 不删除，因此前面步骤调整完成以后可以安全重新连接。
        同时清理旧 EyeModule 曾经创建的 Parent / Aim Constraint。
        """

        # -------------------------------------------------------------------------
        # Step 01：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        connection_names = self._connection_names()

        # 先清理旧版本可能留下的匿名约束。
        main_ctrl_name = name_utils.Name(
            type="ctrl",
            side=self.side,
            part=self.module,
            function="main",
            index=1
        ).name

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        eye_jnt_name = name_utils.Name(
            type="jnt",
            side=self.side,
            part=self.module,
            function="bind",
            index=1
        ).name

        main_driven = main_ctrl_name.replace(
            "ctrl_",
            "driven_",
            1
        )

        # -------------------------------------------------------------------------
        # Step 03：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        self._delete_constraints(
            main_driven,
            ("aimConstraint",)
        )

        self._delete_constraints(
            eye_jnt_name,
            ("parentConstraint", "orientConstraint")
        )

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        delete_order = [
            connection_names["orient_constraint"],
            connection_names["pose_constraint"],
            connection_names["aim_constraint"],
            connection_names["pose_driven"],
            connection_names["pose_driver"],
            connection_names["world_up"],
        ]

        # -------------------------------------------------------------------------
        # Step 05：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for node_name in delete_order:
            if cmds.objExists(node_name):
                cmds.delete(node_name)

    def _create_world_up(self):
        u"""创建稳定 World Up Transform。"""

        if not self.guide_map:
            self.get_guides()

        self._ensure_module_groups()

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

        两个节点都位于 Eye Ball，并且处于相同父空间。
        Pose Driver 读取 Main Output 的最终世界旋转。
        Pose Driven 当前直接继承 Driver Rotate；以后可以在两者之间加入 RBF / Corrective。
        """

        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self.guide_map:
            self.get_guides()

        self._ensure_module_groups()

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.pose_driver_name, self.pose_driven_name

    def connect_rig(self):
        u"""

                建立正式 Eye Rig 连接。

                Aim Output -> Main Driven -> Main Output -> Pose Driver -> Pose Driven -> Eye Joint。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

        """

        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self.eye_jnt_name or not self.main_ctrl_name or not self.aim_ctrl_name:
            self.load_outputs()

        if not self.guide_map:
            self.get_guides()

        self._ensure_module_groups()
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self._set_main_rotation_pivots()

        self._connection_names()
        self.delete_connections()

        main_driven = self.main_ctrl_name.replace(
            "ctrl_",
            "driven_",
            1
        )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        # Aim Driven 的 Pivot 已经位于 Ball。
        # maintainOffset=True 保留 Guide 创建出来的初始姿态，避免绑定生成瞬间跳动。
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

        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self._create_pose_nodes()

        # Main Output 只传 Orientation 到 Pose Driver。
        self.pose_constraint_name = cmds.orientConstraint(
            main_output,
            self.pose_driver_name,
            maintainOffset=True,
            weight=1,
            name=self.pose_constraint_name
        )[0]

        # Eye Joint 最终只接收 Orientation，不接收 Translate。
        self.orient_constraint_name = cmds.orientConstraint(
            self.pose_driven_name,
            self.eye_jnt_name,
            maintainOffset=True,
            weight=1,
            name=self.orient_constraint_name
        )[0]

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
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

    def build(self):
        u"""

                完整重建当前侧 Eye Rig。

                先删除旧 Step 04 连接，再重新生成 Joint / Controller / Hierarchy / Connection，
                避免旧约束影响 Guide Match 和 Controller 重建。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

        """

        self.delete_connections()
        super(EyeModule, self).build()
        return self


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
    u"""

        完整构建单侧 Eye Rig。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            ctrl_shape (str):
                当前 Maya / Rig 操作使用的 `ctrl_shape` 名称或标记。
            aim_ctrl_shape (str):
                当前 Maya / Rig 操作使用的 `aim_ctrl_shape` 名称或标记。
            ctrl_color (int):
                当前 Maya / Rig 操作使用的 `ctrl_color` 整数参数。
            ctrl_size (float):
                当前 Maya / Rig 计算使用的 `ctrl_size` 数值参数。
            ctrl_axis (str):
                当前 Maya / Rig 操作使用的 `ctrl_axis` 名称或标记。
            aim_ctrl_axis (str):
                当前 Maya / Rig 操作使用的 `aim_ctrl_axis` 名称或标记。
            jnt_parent (str | None):
                新建 Jnt Chain 的父 Jnt / Parent Transform；None 表示保持在世界层级。
            ctrl_parent (object):
                当前方法执行 Maya / Rig 操作时使用的 `ctrl_parent` 数据。

        Returns:
            object:
                当前 API 完成处理后返回的结果。

    """

    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
    # -------------------------------------------------------------------------
    rig_object.build()
    # -------------------------------------------------------------------------
    # Step 03：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return rig_object


def connect(side="lf", jnt_parent=None, ctrl_parent=None):
    u"""

        只重建指定侧 Step 04 连接。

        用于用户在 Step 02 / Step 03 修改 Controller、Joint 后重新生成最终驱动。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            jnt_parent (str | None):
                新建 Jnt Chain 的父 Jnt / Parent Transform；None 表示保持在世界层级。
            ctrl_parent (object):
                当前方法执行 Maya / Rig 操作时使用的 `ctrl_parent` 数据。

        Returns:
            object:
                当前 API 完成处理后返回的结果。

    """

    rig_object = EyeModule(
        side=side,
        jnt_parent=jnt_parent,
        ctrl_parent=ctrl_parent
    )

    rig_object.connect_outputs()
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
    u"""

        完整构建左右两侧 Eye Rig。

        Args:
            ctrl_shape (str):
                当前 Maya / Rig 操作使用的 `ctrl_shape` 名称或标记。
            aim_ctrl_shape (str):
                当前 Maya / Rig 操作使用的 `aim_ctrl_shape` 名称或标记。
            ctrl_color (int):
                当前 Maya / Rig 操作使用的 `ctrl_color` 整数参数。
            ctrl_size (float):
                当前 Maya / Rig 计算使用的 `ctrl_size` 数值参数。
            ctrl_axis (str):
                当前 Maya / Rig 操作使用的 `ctrl_axis` 名称或标记。
            aim_ctrl_axis (str):
                当前 Maya / Rig 操作使用的 `aim_ctrl_axis` 名称或标记。
            jnt_parent (str | None):
                新建 Jnt Chain 的父 Jnt / Parent Transform；None 表示保持在世界层级。
            ctrl_parent (object):
                当前方法执行 Maya / Rig 操作时使用的 `ctrl_parent` 数据。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """

    # -------------------------------------------------------------------------
    # Step 01：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
    result = {}

    # -------------------------------------------------------------------------
    # Step 02：遍历当前数据集合，并逐项执行核心处理
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 03：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result


def delete_connections(side="lf"):
    u"""
    删除指定侧 Step 04 连接，保留 Joint / Controller。

    Args:
        side (str):
            方向标记，常用值为 lf、rt 或 md。
    """

    rig_object = EyeModule(
        side=side
    )

    rig_object.delete_connections()


def validate(side="lf"):
    u"""

        检查 Eye Rig 的位置、Pivot 和主要连接。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。

        Returns:
            object:
                当前 API 完成处理后返回的结果。

        Raises:
            ValueError:
                输入数据、场景状态或操作条件不满足要求时抛出。
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。

    """

    # -------------------------------------------------------------------------
    # Step 01：检查当前条件与边界情况，并进入对应处理分支
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 02：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 03：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Step 04：准备当前阶段计算和后续处理需要的数据
    # -------------------------------------------------------------------------
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

    print_order = [
        "main_ctrl_at_iris",
        "main_ctrl_pivot_at_ball",
        "main_driven_pivot_at_ball",
        "joint_at_ball",
        "aim_constraint_exists",
        "pose_constraint_exists",
        "orient_constraint_exists",
        "joint_translate_has_input",
    ]

    for key_name in print_order:
        print(u"{} : {}".format(
            key_name,
            result[key_name]
        ))

    print(u"=============================================\n")

    # -------------------------------------------------------------------------
    # Step 05：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return result
