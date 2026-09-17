# coding=utf-8
u"""
rig_module：MuziTools 当前通用 Rig Module 生命周期基础类。

``RigModule`` 不实现某一种具体绑定，而是定义所有正式 Rig Module 可以复用的
Guide 输入、单 Joint / Controller 创建、Module Root Hierarchy 和分阶段 Build 接口。

当前生命周期：

    get_guides()
        ↓
    create_joints()
        ↓
    create_ctrls()
        ↓
    setup_hierarchy()
        ↓
    connect_rig()

为了支持 Rig Library 的四步工作流，又拆成：

    build_outputs()
        只生成 Joint、Controller 和最终 DAG Hierarchy。

    connect_outputs()
        从场景重新读取已经生成的输出，再建立正式驱动连接。

这种拆分允许用户在 Guide / Ctrl 阶段修改定位或显示设置，然后只重建输出，
最后在 Final 阶段重新建立连接。

职责：
    1. 保存 module / side / guide / jnt_parent / ctrl_parent。
    2. 把外部 Guide 输入整理为有序名称列表。
    3. 通过 core.rigging.jnt_utils.Jnt 创建或读取单 Joint。
    4. 通过 core.rigging.ctrl_utils.Ctrl 创建标准 Controller。
    5. 为每个 Module 创建独立 Joint / Controller Master Group。
    6. 提供 build_outputs / connect_outputs / build 三种构建粒度。

设计边界：
    - 不决定某个业务 Module 需要多少 Joint / Controller；
    - 不猜测 Eye / Ear / Tongue 等业务 Guide 语义；
    - 不决定 Constraint / Matrix / Deformer 的具体连接算法；
    - 不负责 Rig Library 配置持久化、Mirror 或 Ownership；
    - 这些业务规则由子类或 systems.rig.library_service 负责。

典型子类：
    systems.face.eye_module.EyeModule
    systems.face.ear_module.EarModule
    systems.face.tongue_module.TongueModule
    systems.components.fk_chain.FKChain
"""

import maya.cmds as cmds

from ..core.common import name_utils, hierarchy_utils
from ..core.rigging import jnt_utils, ctrl_utils


class RigModule(object):
    u"""
    所有正式 Rig Module 共用的基础构建类。

    子类通常只需要实现：

        create_joints()
        create_ctrls()
        load_outputs()
        connect_rig()

    如果业务拥有固定 Guide 语义，也可以覆盖 ``get_guides()``；例如 Eye Module
    会把 Ball / Iris / Aim 映射成明确的 ``guide_map``，而不是依赖列表顺序猜测。

    ``RigModule`` 支持两种调用方式：

    1. ``build()``：一次完成输出创建和正式连接；
    2. ``build_outputs()`` + ``connect_outputs()``：供 Rig Library 分阶段构建。

    Notes:
        ``RigModule`` 本身可以实例化，但 ``create_joints``、``create_ctrls``、
        ``load_outputs`` 和 ``connect_rig`` 的业务实现需要由子类提供。
    """

    def __init__(self, module=None, side="md", guide=None, jnt_parent=None, ctrl_parent=None):
        u"""
        初始化 Rig Module 的公共输入和运行时状态。

        Args:
            module (str | None):
                Module 业务名称，例如 ``"eye"``、``"ear"``、``"tongue"``。
                该值会进入模块根组和子类输出节点的标准命名。
            side (str):
                Module 方向，当前常用值为 ``lf``、``rt``、``md``。
            guide (str | list[str] | tuple[str] | object | None):
                Guide 数据来源。可以是单节点、按顺序排列的名称列表，或提供
                ``get_guides(module, side)`` 方法的 Guide 对象。
            jnt_parent (str | object | None):
                Module Joint Master Group 的可选父节点；None 表示不额外挂接。
            ctrl_parent (str | object | None):
                Module Controller Master Group 的可选父节点；None 表示不额外挂接。

        Example:
            >>> from muziToolset.systems import rig_module
            >>> module = rig_module.RigModule(
            ...     module="ear",
            ...     side="lf",
            ...     guide=[
            ...         "loc_lf_ear_bind_001",
            ...         "loc_lf_ear_bind_002",
            ...     ],
            ... )
        """

        self.module = module
        self.side = side
        self.guide = guide
        self.jnt_parent = jnt_parent
        self.ctrl_parent = ctrl_parent

        self.guide_list = []
        self.jnt_master_grp = None
        self.ctrl_master_grp = None

    def get_guides(self):
        u"""
        把外部 Guide 输入规范化为有序 Maya 节点名称列表。

        默认实现支持三种来源：

        1. Guide 工具对象：调用 ``get_guides(module, side)``；
        2. list / tuple：严格保留传入顺序；
        3. 单个 Maya 节点：包装成只有一个元素的列表。

        ``guide`` 为 None 时返回空列表。默认实现不会根据 Module 名称去猜测场景
        节点；拥有固定语义规则的业务子类应覆盖本方法。

        Returns:
            list[str]:
                已验证存在的 Guide 名称列表，顺序与输入或 Guide Provider 一致。

        Raises:
            RuntimeError:
                任意输入 Guide 在当前 Maya 场景中不存在时抛出。

        Example:
            >>> module.guide = [
            ...     "loc_lf_ear_bind_001",
            ...     "loc_lf_ear_bind_002",
            ... ]
            >>> guides = module.get_guides()
        """

        self.guide_list = []
        source_guides = []

        if self.guide is None:
            return self.guide_list

        if hasattr(self.guide, "get_guides"):
            result = self.guide.get_guides(self.module, self.side)

            if result:
                for guide_node in result:
                    source_guides.append(guide_node)

        elif isinstance(self.guide, (list, tuple)):
            for guide_node in self.guide:
                source_guides.append(guide_node)

        else:
            source_guides.append(self.guide)

        for guide_node in source_guides:
            guide_name = str(guide_node)

            if not cmds.objExists(guide_name):
                raise RuntimeError(u"找不到 Guide：{}".format(guide_name))

            self.guide_list.append(guide_name)

        return self.guide_list

    def create_joint(self, name, guide=None):
        u"""
        创建或读取一个 Joint，并可选匹配到指定 Guide。

        该方法只处理**单 Joint Primitive**。Joint 数量、链条拓扑、Driver / Bind
        语义以及父子关系仍由子类 ``create_joints()`` 决定。

        Args:
            name (str):
                Joint 标准节点名称，例如 ``jnt_lf_ear_bind_001``。
            guide (str | object | None):
                可选匹配目标。提供时会通过 ``Jnt.set_match_transform()`` 对齐。

        Returns:
            jnt_utils.Jnt:
                当前 Joint 的工具对象；实际 Maya Joint 可通过 ``result.jnt`` 访问。

        Raises:
            TypeError:
                场景中存在同名对象但不是 Joint 时，由 ``jnt_utils.Jnt`` 抛出。

        Example:
            >>> jnt_object = module.create_joint(
            ...     name="jnt_lf_ear_bind_001",
            ...     guide="loc_lf_ear_bind_001",
            ... )
            >>> print(jnt_object.jnt)
        """

        jnt_object = jnt_utils.Jnt(name)

        if guide:
            jnt_object.set_match_transform(guide)

        return jnt_object

    def create_ctrl(
        self,
        name,
        guide=None,
        shape_name="circle",
        ctrl_color=17,
        ctrl_size=1.0,
        ctrl_axis="X+",
        create_hierarchy=True
    ):
        u"""
        创建或读取一个标准 Controller，并应用外观、层级和 Guide Match。

        Controller 的 Shape / Color / Size / Axis / SubCtrl / Output 等底层行为由
        ``core.rigging.ctrl_utils.Ctrl`` 负责。本方法只为 Module 提供统一调度入口。

        Args:
            name (str):
                Controller 标准节点名称，例如 ``ctrl_lf_ear_fk_001``。
            guide (str | object | None):
                可选位置与旋转匹配目标。
            shape_name (str):
                ``resources/controller_shapes`` 中的 Shape 名称。
            ctrl_color (int):
                Maya Drawing Override Index Color。
            ctrl_size (float):
                Controller Curve CV 的显示缩放倍率，不写入 Transform Scale。
            ctrl_axis (str):
                Shape 绝对轴向，支持 ``X+ / X- / Y+ / Y- / Z+ / Z-``。
            create_hierarchy (bool):
                True 时创建标准 zero / driven / space / connect / offset / ctrl / output
                层级，并按当前 Ctrl 实现创建 SubCtrl。

        Returns:
            ctrl_utils.Ctrl:
                当前 Controller 工具对象，可读取 ``ctrl``、``zero_grp``、
                ``output_grp`` 等运行时成员。

        Raises:
            TypeError:
                场景中存在同名对象但不是可用 Transform 时，由 ``Ctrl`` 抛出。

        Example:
            >>> ctrl_object = module.create_ctrl(
            ...     name="ctrl_lf_ear_fk_001",
            ...     guide="loc_lf_ear_bind_001",
            ...     shape_name="shape_016",
            ...     ctrl_color=17,
            ...     ctrl_size=1.0,
            ...     ctrl_axis="X+",
            ... )
        """

        ctrl_object = ctrl_utils.Ctrl(name)
        ctrl_object.create_ctrl(
            shape_name=shape_name,
            ctrl_color=ctrl_color,
            ctrl_size=ctrl_size,
            ctrl_axis=ctrl_axis,
            create_hierarchy=create_hierarchy,
            match_transform_target=guide
        )

        return ctrl_object

    def create_joints(self):
        u"""
        创建当前业务 Module 的完整 Joint System。

        子类覆盖此方法决定 Joint Count、Naming、Guide Mapping 和内部拓扑。
        基类不创建任何节点。

        Returns:
            None:
                基类只提供扩展点；具体子类可以按需要返回 Joint List。
        """

        pass

    def create_ctrls(self):
        u"""
        创建当前业务 Module 的完整 Controller System。

        子类覆盖此方法决定 Main / FK / Aim 等 Controller 的数量和参数。
        基类不创建任何节点。

        Returns:
            None:
                基类只提供扩展点；具体子类可以按需要返回 Controller List。
        """

        pass

    def connect_rig(self):
        u"""
        建立当前业务 Module 的正式驱动连接。

        Constraint、Matrix、Utility Node、RBF 或 Deformer 等连接方式完全由子类决定。
        基类不建立连接。

        Returns:
            None:
                基类只提供扩展点；具体子类可以返回连接结果字典。
        """

        pass

    def setup_hierarchy(self):
        u"""
        创建并整理当前 Module 的 Joint / Controller Master Group。

        标准名称：

            grp_<side>_<module>_jnt_001
            grp_<side>_<module>_ctrl_001

        如果提供 ``jnt_parent`` / ``ctrl_parent``，对应 Master Group 会挂到绑定库
        或上层 System 指定的父节点。该方法不修改子类内部 Joint Chain 或 Controller
        Hierarchy 的结构。

        Returns:
            tuple[object, object]:
                ``(jnt_master_grp, ctrl_master_grp)``。

        Example:
            >>> jnt_grp, ctrl_grp = module.setup_hierarchy()
        """

        jnt_group_name = name_utils.Name(
            type="grp",
            side=self.side,
            part=self.module,
            function="jnt",
            index=1
        ).name

        ctrl_group_name = name_utils.Name(
            type="grp",
            side=self.side,
            part=self.module,
            function="ctrl",
            index=1
        ).name

        self.jnt_master_grp = hierarchy_utils.get_or_create_group(
            jnt_group_name
        )
        self.ctrl_master_grp = hierarchy_utils.get_or_create_group(
            ctrl_group_name
        )

        if self.jnt_parent:
            hierarchy_utils.parent(
                self.jnt_master_grp,
                self.jnt_parent
            )

        if self.ctrl_parent:
            hierarchy_utils.parent(
                self.ctrl_master_grp,
                self.ctrl_parent
            )

        return self.jnt_master_grp, self.ctrl_master_grp

    def build_outputs(self):
        u"""
        创建 Guide 驱动的 Joint、Controller 和最终 DAG Hierarchy，但不连接 Rig。

        执行顺序固定为：

            get_guides()
            create_joints()
            create_ctrls()
            setup_hierarchy()

        这是 Rig Library Step 02 完成定位后生成可检查输出时使用的核心入口。
        输出生成后，用户可以在 Step 03 调整 Controller / Joint 显示，再进入 Final。

        Returns:
            None:
                结果保存在子类运行时成员和 Maya 场景节点中。
        """
        self.get_guides()
        self.create_joints()
        self.create_ctrls()
        self.setup_hierarchy()

    def load_outputs(self):
        u"""
        从 Maya 场景读取当前 Module 已经生成的输出节点。

        子类必须根据自己的 Naming Contract 验证 Joint、Controller、Output 等节点，
        并恢复 ``connect_rig()`` 所需的运行时成员。基类不猜测输出名称。

        Returns:
            None:
                基类只提供扩展点。
        """
        pass

    def connect_outputs(self):
        u"""
        读取已生成输出，并建立当前 Module 的正式驱动连接。

        执行：

            load_outputs()
                ↓
            connect_rig()

        该入口允许一个新的 Python Module 实例在不重新创建 Joint / Controller 的情况下，
        直接进入 Rig Library Final 阶段。

        Returns:
            None:
                连接结果由具体子类写入 Maya 场景并可选保存到成员。
        """
        self.load_outputs()
        self.connect_rig()

    def build(self):
        u"""
        一次完成当前 Rig Module 的输出创建与最终连接。

        等价于：

            build_outputs()
                ↓
            connect_outputs()

        先完成最终 DAG Hierarchy，再创建 Constraint / Matrix / Utility Node 等连接，
        可以避免连接建立后继续 Parent 导致空间偏移或重复计算。

        Rig Library 通常使用分阶段入口；独立测试或一次性 Module Build 可以直接使用
        ``build()``。

        Returns:
            None:
                构建结果存在于 Maya 场景和具体子类成员中。

        Example:
            >>> from muziToolset.systems.face import eye_module
            >>> eye = eye_module.EyeModule(side="lf")
            >>> eye.build()
        """

        self.build_outputs()
        self.connect_outputs()
