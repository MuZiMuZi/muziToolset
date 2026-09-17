# coding=utf-8
u"""
fk_chain：MuziTools 标准线性 FK Chain Rig Component。

适合：
    Ear、Tongue、Finger、Tail 或其他“一组有序 Guide → 一组 Joint → 一组 FK Ctrl”
    的线性结构。

核心数据流：

    Guide 001
        ↓
    Joint 001  ←  Output Ctrl 001
        ↓                 ↓
    Joint 002  ←  Output Ctrl 002
        ↓                 ↓
    Joint 003  ←  Output Ctrl 003

构建职责：
    1. 获取显式 Guide，或按标准 Locator Naming 自动查找 Guide。
    2. 一条 Guide 对应一个 Joint。
    3. 一条 Guide 对应一个 FK Controller。
    4. Joint 按 Guide 顺序组成 Joint Chain。
    5. Controller 使用“上一个 Output → 下一个 Zero”的 FK DAG 结构。
    6. 每个 Controller Output 使用 parentConstraint 驱动对应 Joint。
    7. Final 阶段可以通过 load_outputs() 从已有场景恢复连接所需状态。

设计边界：
    - FKChain 不负责复杂 IK、Spline IK、Stretch 或 Twist；
    - 不负责特殊 Eye Aim / Pose Driver 结构；
    - 不负责 Rig Library 的 JSON、Mirror、Ownership 与 UI；
    - 单 Joint / Controller Primitive 继续复用 RigModule。

当前直接复用 FKChain 的正式 Face Module：
    systems.face.ear_module.EarModule
    systems.face.tongue_module.TongueModule
"""

import maya.cmds as cmds

from .. import rig_module
from ...core.common import name_utils, hierarchy_utils


class FKChain(rig_module.RigModule):
    u"""
    标准线性 FK Joint / Controller Chain 构建器。

    ``FKChain`` 是 ``RigModule`` 的业务实现之一。它把有序 Guide 转换成同长度的
    Joint 和 FK Controller，并建立可重复检查的 Hierarchy / Constraint Contract。

    典型结构：

        jnt_master_grp
        └── jnt_001
            └── jnt_002
                └── jnt_003

        ctrl_master_grp
        └── zero_001
            └── ... ctrl_001
                └── output_001
                    └── zero_002
                        └── ... ctrl_002
                            └── output_002

    Final Connection：

        output_001 -> parentConstraint -> jnt_001
        output_002 -> parentConstraint -> jnt_002
        ...

    已经存在正确 Driver 的 Constraint 会被复用；存在其他 Parent Constraint 时会
    抛出错误，而不是静默覆盖已有 Rig。
    """

    def __init__(
        self,
        module,
        side="md",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None,
        guide_count=1,
        guide_function="bind",
        jnt_function="bind",
        ctrl_function="fk",
        ctrl_shape="circle",
        ctrl_color=17,
        ctrl_size=1.0,
        ctrl_axis="X+"
    ):
        u"""
        初始化标准 FK Chain 的 Naming、Guide Count 和 Controller 外观配置。

        Args:
            module (str):
                Module Part Token，例如 ``"ear"``、``"tongue"``、``"finger"``。
            side (str):
                方向标记，常用 ``lf``、``rt``、``md``。
            guide (str | list[str] | tuple[str] | object | None):
                可选 Guide 来源。None 时根据标准 Locator Naming 自动查找。
            jnt_parent (str | object | None):
                Module Joint Master Group 的可选上层父节点。
            ctrl_parent (str | object | None):
                Module Controller Master Group 的可选上层父节点。
            guide_count (int):
                自动按名称查找 Guide 时的预期数量。
            guide_function (str):
                Guide Locator Naming 中的 function Token，当前普通绑定 Guide 默认 ``bind``。
            jnt_function (str):
                输出 Joint Naming 中的 function Token，默认 ``bind``。
            ctrl_function (str):
                输出 Controller Naming 中的 function Token，默认 ``fk``。
            ctrl_shape (str):
                Controller Shape Library 名称。
            ctrl_color (int):
                Maya Drawing Override Index Color。
            ctrl_size (float):
                Controller Curve CV 显示大小倍率。
            ctrl_axis (str):
                Controller Shape 绝对轴向，支持 ``X+ / X- / Y+ / Y- / Z+ / Z-``。

        Example:
            >>> from muziToolset.systems.components import fk_chain
            >>> fk = fk_chain.FKChain(
            ...     module="ear",
            ...     side="lf",
            ...     guide_count=3,
            ...     guide_function="bind",
            ...     ctrl_axis="Z+",
            ... )
            >>> fk.build()

        Notes:
            Rig Library 会在实例化后覆盖 ``ctrl_size`` / ``ctrl_color``，因此这些成员
            也是模块外观配置的稳定运行时接口。
        """

        super(FKChain, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent
        )

        self.guide_count = guide_count
        self.guide_function = guide_function
        self.jnt_function = jnt_function
        self.ctrl_function = ctrl_function

        self.ctrl_shape = ctrl_shape
        self.ctrl_color = ctrl_color
        self.ctrl_size = ctrl_size
        self.ctrl_axis = ctrl_axis

        self.jnt_list = []
        self.jnt_objects = []
        self.ctrl_list = []
        self.ctrl_objects = []

    def get_guides(self):
        u"""
        返回当前 FK Chain 的有序 Guide 列表。

        优先级：

        1. 复用 ``RigModule.get_guides()`` 读取显式传入的数据；
        2. 没有传入 ``guide`` 时，按
           ``loc_<side>_<module>_<guide_function>_<index>`` 自动查找；
        3. 显式传入了 Guide 但结果为空时直接报错，不再退回名称猜测。

        Returns:
            list[str]:
                按 FK Chain 顺序排列的 Guide 名称。

        Raises:
            RuntimeError:
                标准名称对应的 Guide 缺失，或显式 Guide 来源没有得到有效结果时抛出。

        Example:
            >>> fk = FKChain(
            ...     module="ear",
            ...     side="lf",
            ...     guide_count=3,
            ... )
            >>> guides = fk.get_guides()
            >>> print(guides)
            ['loc_lf_ear_bind_001', 'loc_lf_ear_bind_002', 'loc_lf_ear_bind_003']
        """

        self.guide_list = super(FKChain, self).get_guides()

        if self.guide_list:
            return self.guide_list

        if self.guide is not None:
            raise RuntimeError(u"{} 没有可用的 FK Guide。".format(self.module))

        for index in range(1, self.guide_count + 1):
            guide_name_object = name_utils.Name(
                type="loc",
                side=self.side,
                part=self.module,
                function=self.guide_function,
                index=index
            )

            guide_name = guide_name_object.name

            if not cmds.objExists(guide_name):
                raise RuntimeError(u"找不到 FK Guide：{}".format(guide_name))

            self.guide_list.append(guide_name)

        if not self.guide_list:
            raise RuntimeError(u"{} 没有可用的 FK Guide。".format(self.module))

        return self.guide_list

    def create_joints(self):
        u"""
        按 Guide 顺序创建当前 FK Chain 的 Joint 列表。

        每条 Guide 创建一个标准 ``jnt_<side>_<module>_<function>_<index>`` Joint，
        单 Joint 创建和 Guide Match 统一调用 ``RigModule.create_joint()``。

        Returns:
            list[str]:
                当前 Chain 的 Joint 名称列表。

        Example:
            >>> fk.get_guides()
            >>> joints = fk.create_joints()
        """

        self.jnt_list = []
        self.jnt_objects = []

        for index, guide_name in enumerate(self.guide_list, 1):
            jnt_name_object = name_utils.Name(
                type="jnt",
                side=self.side,
                part=self.module,
                function=self.jnt_function,
                index=index
            )

            jnt_object = self.create_joint(
                name=jnt_name_object.name,
                guide=guide_name
            )

            self.jnt_list.append(jnt_name_object.name)
            self.jnt_objects.append(jnt_object)

        return self.jnt_list

    def create_ctrls(self):
        u"""
        按 Guide 顺序创建当前 FK Chain 的标准 Controller 列表。

        每条 Guide 创建一个 ``ctrl_<side>_<module>_<ctrl_function>_<index>``，并通过
        ``RigModule.create_ctrl()`` 统一应用 Shape、Color、Size、Axis、Hierarchy 和
        Guide Match。

        Returns:
            list[str]:
                当前 Chain 的 Controller 名称列表。

        Example:
            >>> fk.get_guides()
            >>> controls = fk.create_ctrls()
        """

        self.ctrl_list = []
        self.ctrl_objects = []

        for index, guide_name in enumerate(self.guide_list, 1):
            ctrl_name_object = name_utils.Name(
                type="ctrl",
                side=self.side,
                part=self.module,
                function=self.ctrl_function,
                index=index
            )

            ctrl_object = self.create_ctrl(
                name=ctrl_name_object.name,
                guide=guide_name,
                shape_name=self.ctrl_shape,
                ctrl_color=self.ctrl_color,
                ctrl_size=self.ctrl_size,
                ctrl_axis=self.ctrl_axis,
                create_hierarchy=True
            )

            self.ctrl_list.append(ctrl_name_object.name)
            self.ctrl_objects.append(ctrl_object)

        return self.ctrl_list

    def connect_rig(self):
        u"""
        用每个 Controller Output 的 Parent Constraint 驱动对应 Joint。

        重复执行规则：

        - Joint 已有由当前 Output 驱动的 ``parentConstraint``：直接复用；
        - Joint 已有其他 Parent Constraint：抛出 ``RuntimeError``，不覆盖；
        - Joint 没有 Parent Constraint：创建新的 ``maintainOffset=True`` Constraint。

        Returns:
            None:
                Connection 直接创建在 Maya Scene 中。

        Raises:
            RuntimeError:
                Joint 已存在其他 Driver 的 Parent Constraint 时抛出。

        Notes:
            Driver 使用 Controller ``output_grp``，而不是直接使用可见 Ctrl Transform，
            因此主 Ctrl / SubCtrl 的最终动画结果可以通过稳定 Output 接口传给 Joint。
        """

        for index in range(len(self.jnt_objects)):
            jnt_object = self.jnt_objects[index]
            ctrl_object = self.ctrl_objects[index]

            driver = str(ctrl_object.output_grp)
            driven = str(jnt_object.jnt)

            constraint_nodes = cmds.listConnections(
                driven,
                source=True,
                destination=False,
                type="parentConstraint"
            )

            if constraint_nodes is None:
                constraint_nodes = []

            driver_long_names = cmds.ls(
                driver,
                long=True
            )

            if driver_long_names:
                driver_long_name = driver_long_names[0]
            else:
                driver_long_name = driver

            matched_constraint = None

            for constraint_node in constraint_nodes:
                target_list = cmds.parentConstraint(
                    constraint_node,
                    query=True,
                    targetList=True
                )

                if target_list is None:
                    target_list = []

                for target in target_list:
                    target_long_names = cmds.ls(
                        target,
                        long=True
                    )

                    if target_long_names:
                        target_long_name = target_long_names[0]
                    else:
                        target_long_name = target

                    if target_long_name == driver_long_name:
                        matched_constraint = constraint_node
                        break

                if matched_constraint:
                    break

            if matched_constraint:
                continue

            if constraint_nodes:
                raise RuntimeError(
                    u"{} 已经存在 Parent Constraint，但 Driver 不是 {}。".format(
                        driven,
                        driver
                    )
                )

            cmds.parentConstraint(
                driver,
                driven,
                maintainOffset=True
            )

    def load_outputs(self):
        u"""
        从场景恢复已经 Build 的 FK Joint、Controller 和 Output 列表。

        该方法用于 Rig Library Final：新的 Python Builder 实例不重新创建输出，而是按
        当前 Guide Count / Naming Contract 查找已有节点，并构造 ``connect_rig()`` 所需
        的轻量对象。

        Returns:
            tuple[list[str], list[str]]:
                ``(jnt_list, ctrl_list)``。

        Raises:
            RuntimeError:
                任意预期 Joint、Controller 或 Output 不存在时抛出。

        Notes:
            ``load_outputs()`` 不修改 Joint / Controller DAG，也不会建立 Constraint。
        """
        self.get_guides()
        self.jnt_list = []
        self.jnt_objects = []
        self.ctrl_list = []
        self.ctrl_objects = []

        class ExistingJoint(object):
            def __init__(self, name):
                self.jnt = name

        class ExistingController(object):
            def __init__(self, name, output_name):
                self.ctrl = name
                self.output_grp = output_name

        for index in range(1, len(self.guide_list) + 1):
            joint_name = name_utils.Name(
                type="jnt", side=self.side, part=self.module,
                function=self.jnt_function, index=index
            ).name
            control_name = name_utils.Name(
                type="ctrl", side=self.side, part=self.module,
                function=self.ctrl_function, index=index
            ).name
            output_name = control_name.replace("ctrl_", "output_", 1)
            for node_name in (joint_name, control_name, output_name):
                if not cmds.objExists(node_name):
                    raise RuntimeError(u"找不到已经生成的模块输出：{}".format(node_name))
            self.jnt_list.append(joint_name)
            self.jnt_objects.append(ExistingJoint(joint_name))
            self.ctrl_list.append(control_name)
            self.ctrl_objects.append(ExistingController(control_name, output_name))

        return self.jnt_list, self.ctrl_list

    def setup_hierarchy(self):
        u"""
        创建 Module Master Group，并整理 Joint Chain 与 Controller FK Chain。

        Joint：

            jnt_master_grp
                ↓
            jnt_001 -> jnt_002 -> jnt_003 ...

        Controller：

            ctrl_master_grp
                ↓
            zero_001
                ↓
            output_001 -> zero_002
                ↓
            output_002 -> zero_003

        Returns:
            None:
                Hierarchy 直接修改 Maya DAG；Master Group 保存在继承成员中。
        """

        super(FKChain, self).setup_hierarchy()

        if self.jnt_list:
            hierarchy_utils.chain_parent(
                self.jnt_list,
                parent_node=self.jnt_master_grp
            )

        if self.ctrl_objects:
            first_ctrl_object = self.ctrl_objects[0]

            hierarchy_utils.parent(
                first_ctrl_object.zero_grp,
                self.ctrl_master_grp
            )

            for index in range(1, len(self.ctrl_objects)):
                parent_ctrl_object = self.ctrl_objects[index - 1]
                child_ctrl_object = self.ctrl_objects[index]

                hierarchy_utils.parent(
                    child_ctrl_object.zero_grp,
                    parent_ctrl_object.output_grp
                )
