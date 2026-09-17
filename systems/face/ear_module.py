# coding=utf-8
u"""
EarModule：耳朵三段 FK 绑定模块。

EarModule 本身不重复实现 FK 算法，而是把耳朵的稳定业务配置交给
``systems.components.fk_chain.FKChain``：

    Guide Count     = 3
    Guide Function  = bind
    Joint Function  = bind
    Ctrl Function   = fk
    Ctrl Shape      = circle

标准 Guide：
    loc_<side>_ear_bind_001
    loc_<side>_ear_bind_002
    loc_<side>_ear_bind_003

标准输出：
    jnt_<side>_ear_bind_001 ... 003
    ctrl_<side>_ear_fk_001 ... 003
    grp_<side>_ear_jnt_001
    grp_<side>_ear_ctrl_001

构建与连接生命周期全部继承 FKChain，因此 EarModule 可以直接参与 Rig Library 的
Build / Rebuild / Final 流程。
"""

from ..components import fk_chain


class EarModule(fk_chain.FKChain):
    u"""
    使用标准三段 FK Chain 实现的耳朵 Rig Module。

    这个类的主要职责是固定 Ear 的 Guide 数量、Naming Token 和默认 Controller
    设置；真正的 Guide 查询、Joint / Controller 创建、FK Hierarchy、Output → Joint
    Parent Constraint 和分阶段连接由 ``FKChain`` 负责。

    适用场景：
        - 左 / 右耳朵三段 FK；
        - Rig Library 中需要支持 Guide Mirror 和 Rebuild 的耳朵模块；
        - 希望保持 Ear 与通用 FKChain 使用同一套生命周期时。
    """

    def __init__(
        self,
        module="ear",
        side="md",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None,
        ctrl_axis="X+"
    ):
        u"""
        初始化耳朵 FK Module，并把 Ear 固定配置传给 ``FKChain``。

        Args:
            module (str):
                Module Part Token，默认 ``"ear"``。Rig Library 正式 Ear 模块应保持默认值。
            side (str):
                方向标记。实际角色耳朵通常使用 ``"lf"`` 或 ``"rt"``。
            guide (str | list[str] | tuple[str] | object | None):
                可选 Guide 来源。None 时 FKChain 会按标准 Ear Locator 名称自动查找三项。
            jnt_parent (str | object | None):
                Ear Joint Master Group 的可选上层父节点；Rig Library 通常传入
                ``grp_md_rig_jnt_001``。
            ctrl_parent (str | object | None):
                Ear Controller Master Group 的可选上层父节点；Rig Library 通常传入
                ``grp_md_rig_ctrl_001``。
            ctrl_axis (str):
                Controller Shape 绝对轴向，支持 ``X+ / X- / Y+ / Y- / Z+ / Z-``。

        Example:
            >>> from muziToolset.systems.face import ear_module
            >>> ear = ear_module.EarModule(
            ...     side="lf",
            ...     ctrl_axis="Z+",
            ... )
            >>> ear.build()

        Notes:
            Rig Library 分阶段构建时通常调用继承的 ``build_outputs()``，Final 阶段
            再调用 ``connect_outputs()``，而不是一次执行 ``build()``。
        """

        super(EarModule, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent,
            guide_count=3,
            guide_function="bind",
            jnt_function="bind",
            ctrl_function="fk",
            ctrl_shape="circle",
            ctrl_color=17,
            ctrl_size=1.0,
            ctrl_axis=ctrl_axis
        )
