# coding=utf-8
u"""
EarModule：耳朵 FK 绑定模块。

EarModule 只负责定义耳朵模块自身的配置，
具体的 Guide、Joint、Controller、连接和 FK 层级构建统一复用 FKChain。
"""

from ..components import fk_chain


class EarModule(fk_chain.FKChain):

    def __init__(
        self,
        module="ear",
        side="md",
        guide=None,
        jnt_parent=None,
        ctrl_parent=None
    ):
        u"""
        初始化耳朵 FK 模块。

        module(str): 模块名称，默认 "ear"。
        side(str): 模块方向，例如 "lf"、"rt"。
        guide(list/str/Guide): 可选 Guide 数据来源。
        jnt_parent(str/PyNode): Joint 总组的可选父节点。
        ctrl_parent(str/PyNode): Controller 总组的可选父节点。

        Maya 使用示例：

            from muziToolset.systems.face import ear_module

            ear_object = ear_module.EarModule(
                module="ear",
                side="lf",
                guide=None,
                jnt_parent=None,
                ctrl_parent=None
            )

            ear_object.build()
        """

        super(EarModule, self).__init__(
            module=module,
            side=side,
            guide=guide,
            jnt_parent=jnt_parent,
            ctrl_parent=ctrl_parent,
            guide_count=3,
            jnt_function="bind",
            ctrl_function="fk",
            ctrl_shape="circle",
            ctrl_color=17,
            ctrl_size=1.0
        )
