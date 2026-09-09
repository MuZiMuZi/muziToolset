from ..components import fk_chain


class TongueModule(fk_chain.FKChain):

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
        初始化耳朵 FK 模块。

        module(str): 模块名称，默认 "ear"。
        side(str): 模块方向，例如 "lf"、"rt"。
        guide(list/str/Guide): 可选 Guide 数据来源。
        jnt_parent(str/PyNode): Joint 总组的可选父节点。
        ctrl_parent(str/PyNode): Controller 总组的可选父节点。
        ctrl_axis(str): 耳朵 Controller Shape 面朝方向，支持 X+ / X- / Y+ / Y- / Z+ / Z-。

        Maya 使用示例：

            from muziToolset.systems.face import ear_module

            ear_object = ear_module.EarModule(
                module="ear",
                side="lf",
                guide=None,
                jnt_parent=None,
                ctrl_parent=None,
                ctrl_axis="Z+"
            )

            ear_object.build()
        """

        super(TongueModule, self).__init__(
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
            ctrl_size=1.0,
            ctrl_axis=ctrl_axis
        )
