# coding=utf-8
u"""
TongueModule：舌头五段 FK 绑定模块。

TongueModule 本身不重复实现 FK 算法，只负责把舌头的固定配置传给 FKChain。

标准配置：
    Guide Count    = 5
    Joint Function = bind
    Ctrl Function  = fk
    Ctrl Shape     = circle

标准 Guide：
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

生命周期：
    build_rig()   -> 创建 Joint / Controller / FK Hierarchy
    connect_rig() -> 创建 Controller Output 到 Joint 的 Parent Constraint
    delete_rig()  -> 删除 Tongue 自己创建的 Constraint 和 DAG 输出

Guide 的创建和导入以后由 Guide Template 系统负责。
TongueModule 只接收已经确定好的五个 Locator 名称。
"""

from ..components import fk_chain


class TongueModule(fk_chain.FKChain):
    u"""使用标准五段 FKChain 实现的舌头绑定模块。"""

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
        初始化 TongueModule。

        TongueModule 只保存舌头自己的固定业务配置，真正的 Joint、Controller、
        Constraint 创建和删除全部由 FKChain 统一处理。

        Args:
            module (str):
                模块名称，正式舌头模块默认使用 "tongue"。
            side (str):
                舌头通常位于中线，默认使用 "md"。
            guide (list[str] | tuple[str] | None):
                Guide Template 导入完成后提供的五个 Tongue Locator，顺序必须和 FK 链一致。
            jnt_parent (str | None):
                Tongue Joint 总组需要挂接的上层节点。
            ctrl_parent (str | None):
                Tongue Controller 总组需要挂接的上层节点。
            ctrl_axis (str):
                Controller Shape 轴向。
        """

        # ---------------------------------------------------------------------
        # Tongue 是固定五段 FK，因此这里只需要把固定参数交给 FKChain。
        # 后续 build_rig() / connect_rig() / delete_rig() 全部直接继承。
        # ---------------------------------------------------------------------
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
