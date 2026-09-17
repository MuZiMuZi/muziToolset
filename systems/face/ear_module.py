# coding=utf-8
u"""
EarModule：耳朵三段 FK 绑定模块。

EarModule 本身不重复实现 FK 算法，只负责把耳朵的固定配置传给 FKChain。

标准配置：
    Guide Count    = 3
    Joint Function = bind
    Ctrl Function  = fk
    Ctrl Shape     = circle

标准 Guide：
    loc_<side>_ear_bind_001
    loc_<side>_ear_bind_002
    loc_<side>_ear_bind_003

标准输出：
    jnt_<side>_ear_bind_001 ... 003
    ctrl_<side>_ear_fk_001 ... 003
    grp_<side>_ear_jnt_001
    grp_<side>_ear_ctrl_001

生命周期：
    build_rig()   -> 创建 Joint / Controller / FK Hierarchy
    connect_rig() -> 创建 Controller Output 到 Joint 的 Parent Constraint
    delete_rig()  -> 删除 Ear 自己创建的 Constraint 和 DAG 输出

Guide 的创建和导入以后由 Guide Template 系统负责。
EarModule 只接收已经确定好的三个 Locator 名称。
"""

from ..components import fk_chain


class EarModule(fk_chain.FKChain):
    u"""使用标准三段 FKChain 实现的耳朵绑定模块。"""

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
        初始化 EarModule。

        EarModule 只保存耳朵自己的固定业务配置，真正的 Joint、Controller、
        Constraint 创建和删除全部由 FKChain 统一处理。

        Args:
            module (str):
                模块名称，正式耳朵模块默认使用 "ear"。
            side (str):
                左右方向，正式角色通常使用 "lf" 或 "rt"。
            guide (list[str] | tuple[str] | None):
                Guide Template 导入完成后提供的三个 Ear Locator，顺序必须和 FK 链一致。
            jnt_parent (str | None):
                Ear Joint 总组需要挂接的上层节点。
            ctrl_parent (str | None):
                Ear Controller 总组需要挂接的上层节点。
            ctrl_axis (str):
                Controller Shape 轴向。
        """

        # ---------------------------------------------------------------------
        # Ear 是固定三段 FK，因此这里只需要把固定参数交给 FKChain。
        # 后续 build_rig() / connect_rig() / delete_rig() 全部直接继承。
        # ---------------------------------------------------------------------
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
