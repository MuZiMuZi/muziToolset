# coding=utf-8
u"""
EyeModule：眼球 Aim 绑定模块。

当前 Eye 模块只负责眼球本体，不负责 Eyelid。

Guide 语义：
    loc_<side>_eye_ball_001
        眼球旋转中心，用于创建 Eye Joint。
    loc_<side>_eye_iris_001
        眼球前方参考点，用于放置 Eye Main Controller。
    loc_<side>_eye_aim_001
        目光目标点，用于放置 Eye Aim Controller。

控制逻辑：
    ctrl_<side>_eye_aim_001
        动画师移动该控制器即可直接改变目光方向。
    output_<side>_eye_aim_001
        通过 Aim Constraint 驱动 driven_<side>_eye_main_001。
    output_<side>_eye_main_001
        最终通过 Parent Constraint 驱动 jnt_<side>_eye_bind_001。

旧版 Eye 绑定只作为算法参考；当前实现统一使用新版命名、RigModule 生命周期和 Controller 层级。
"""

import maya.cmds as cmds

from .. import rig_module
from . import face_guide_config
from ...core.common import name_utils, hierarchy_utils


class EyeModule(rig_module.RigModule):

    def __init__(
        self,
        module="eye",
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
        u"""初始化眼球 Aim 绑定模块。"""

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

        self.guide_map = {}

        self.eye_jnt_name = None
        self.eye_jnt_object = None

        self.main_ctrl_name = None
        self.main_ctrl_object = None

        self.aim_ctrl_name = None
        self.aim_ctrl_object = None

    @staticmethod
    def _short_name(node_name):
        u"""返回不包含 DAG Path 和 Namespace 的短名称。"""

        short_name = str(node_name)

        if "|" in short_name:
            short_name = short_name.split("|")[-1]

        if ":" in short_name:
            short_name = short_name.rsplit(":", 1)[-1]

        return short_name

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
        外部传入 Guide 时会按照节点标准名称匹配 ball / iris / aim；
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
            circle / X+，位置来自 Iris Guide。
        Aim Controller：
            shape_040 / Z+，位置来自 Aim Guide。
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

        return self.jnt_master_grp, self.ctrl_master_grp

    def load_outputs(self):
        u"""读取 Step 03 已经创建完成的 Eye 输出。"""

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
            self.main_ctrl_name.replace(
                "ctrl_",
                "driven_",
                1
            ),
            self.main_ctrl_name.replace(
                "ctrl_",
                "output_",
                1
            ),
            self.aim_ctrl_name,
            self.aim_ctrl_name.replace(
                "ctrl_",
                "output_",
                1
            ),
        ]

        for node_name in required_nodes:
            if not cmds.objExists(node_name):
                raise RuntimeError(
                    u"找不到已经生成的 Eye 输出：{}".format(
                        node_name
                    )
                )

        return required_nodes

    @staticmethod
    def _long_name(node_name):
        u"""返回节点 Long Name；找不到时保留原名称。"""

        long_names = cmds.ls(
            node_name,
            long=True
        ) or []

        if long_names:
            return long_names[0]

        return node_name

    def _find_constraint(self, driven, driver, constraint_type):
        u"""查找 driven 上是否已经存在由指定 driver 驱动的约束。"""

        constraint_nodes = cmds.listConnections(
            driven,
            source=True,
            destination=False,
            type=constraint_type
        ) or []

        driver_long_name = self._long_name(
            driver
        )

        for constraint_node in constraint_nodes:
            if constraint_type == "parentConstraint":
                target_list = cmds.parentConstraint(
                    constraint_node,
                    query=True,
                    targetList=True
                ) or []
            elif constraint_type == "aimConstraint":
                target_list = cmds.aimConstraint(
                    constraint_node,
                    query=True,
                    targetList=True
                ) or []
            else:
                target_list = []

            for target in target_list:
                target_long_name = self._long_name(
                    target
                )

                if target_long_name == driver_long_name:
                    return constraint_node

        if constraint_nodes:
            raise RuntimeError(
                u"{} 已经存在 {}，但 Driver 不是 {}。".format(
                    driven,
                    constraint_type,
                    driver
                )
            )

        return None

    def connect_rig(self):
        u"""
        建立 Eye Main / Aim / Joint 的最终驱动。

        1. Aim Output 目标约束 Main Driven，移动 Aim Ctrl 即直接控制目光。
        2. Main Output Parent Constraint 到 Eye Joint，保留 Main Ctrl 的局部动画叠加。
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

        aim_constraint = self._find_constraint(
            driven=main_driven,
            driver=aim_output,
            constraint_type="aimConstraint"
        )

        if aim_constraint is None:
            cmds.aimConstraint(
                aim_output,
                main_driven,
                maintainOffset=False,
                offset=(0, 0, 0),
                weight=1,
                aimVector=(1, 0, 0),
                upVector=(0, 1, 0),
                worldUpType="vector",
                worldUpVector=(0, 1, 0)
            )

        parent_constraint = self._find_constraint(
            driven=self.eye_jnt_name,
            driver=main_output,
            constraint_type="parentConstraint"
        )

        if parent_constraint is None:
            cmds.parentConstraint(
                main_output,
                self.eye_jnt_name,
                maintainOffset=True
            )
