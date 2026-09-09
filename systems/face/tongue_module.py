# coding=utf-8
u"""
TongueModule：舌头 FK 绑定模块。

TongueModule 复用标准 FKChain。
当前 Face Guide 模板包含 5 个 Tongue Bind Locator：
    loc_md_tongue_bind_001
    loc_md_tongue_bind_002
    loc_md_tongue_bind_003
    loc_md_tongue_bind_004
    loc_md_tongue_bind_005
"""

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
        初始化舌头 FK 模块。

        module(str): 模块名称，默认 "tongue"。
        side(str): 模块方向，舌头默认使用 "md"。
        guide(list/str/Guide): 可选 Guide 数据来源。
        jnt_parent(str/PyNode): Joint 总组的可选父节点。
        ctrl_parent(str/PyNode): Controller 总组的可选父节点。
        ctrl_axis(str): 舌头 Controller Shape 面朝方向，支持 X+ / X- / Y+ / Y- / Z+ / Z-。

        Maya 使用示例：

            from muziToolset.systems.face import tongue_module

            tongue_object = tongue_module.TongueModule(
                module="tongue",
                side="md",
                guide=None,
                jnt_parent=None,
                ctrl_parent=None,
                ctrl_axis="Z+"
            )

            tongue_object.build()
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
