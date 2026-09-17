# coding=utf-8
u"""
TongueModule：舌头五段 FK 绑定模块。

TongueModule 复用 ``systems.components.fk_chain.FKChain``，只固定舌头自己的业务配置：

    Guide Count     = 5
    Guide Function  = bind
    Joint Function  = bind
    Ctrl Function   = fk
    Ctrl Shape      = circle

当前 Face Guide 模板标准 Locator：
    loc_md_tongue_bind_001
    loc_md_tongue_bind_002
    loc_md_tongue_bind_003
    loc_md_tongue_bind_004
    loc_md_tongue_bind_005

标准输出：
    jnt_md_tongue_bind_001 ... 005
    ctrl_md_tongue_fk_001 ... 005
    grp_md_tongue_jnt_001
    grp_md_tongue_ctrl_001

舌头默认是中线模块，因此正式 Rig Library 配置通常使用 side="md"，不参与左右镜像。
"""

from ..components import fk_chain


class TongueModule(fk_chain.FKChain):
    u"""
    使用标准五段 FK Chain 实现的舌头 Rig Module。

    ``TongueModule`` 负责把 Tongue 的固定 Guide 数量和默认命名传给 FKChain；
    Guide 查询、Joint / Controller 创建、FK 父子层级和最终 Output → Joint 连接都
    复用通用 FKChain，因此它与 Ear / 通用 FK 模块拥有一致的 Build Contract。

    适用场景：
        - Face Rig 中的中线五段舌头 FK；
        - Rig Library 中需要 Build / Rebuild / Final 的 Tongue Module；
        - 希望后续通过统一 FKChain 改善所有线性 FK 模块时。
    """

    def __init__(
        self,
        module="tongue",
        side="md",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None,
        ctrl_axis="X+"
    ):
        u"""
        初始化舌头 FK Module，并把 Tongue 固定配置传给 ``FKChain``。

        Args:
            module (str):
                Module Part Token，默认 ``"tongue"``。
            side (str):
                方向标记。正式 Tongue Module 默认并推荐使用 ``"md"``。
            guide (str | list[str] | tuple[str] | object | None):
                可选 Guide 来源。None 时 FKChain 会按标准 Tongue Locator 名称自动查找五项。
            jnt_parent (str | object | None):
                Tongue Joint Master Group 的可选上层父节点；Rig Library 通常传入
                ``grp_md_rig_jnt_001``。
            ctrl_parent (str | object | None):
                Tongue Controller Master Group 的可选上层父节点；Rig Library 通常传入
                ``grp_md_rig_ctrl_001``。
            ctrl_axis (str):
                Controller Shape 绝对轴向，支持 ``X+ / X- / Y+ / Y- / Z+ / Z-``。

        Example:
            >>> from muziToolset.systems.face import tongue_module
            >>> tongue = tongue_module.TongueModule(
            ...     side="md",
            ...     ctrl_axis="Z+",
            ... )
            >>> tongue.build()

        Notes:
            Tongue 是中央模块。Rig Library 的左右 Mirror 只对 ``lf / rt`` Module 开放，
            因此中央 Tongue 不需要创建配对侧。
        """

        super(TongueModule, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent,
            guide_count=5,
            guide_function="bind",
            jnt_function="bind",
            ctrl_function="fk",
            ctrl_shape="circle",
            ctrl_color=17,
            ctrl_size=1.0,
            ctrl_axis=ctrl_axis
        )
