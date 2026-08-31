# coding=utf-8
u"""
Component Base
==============

所有 Rig System 共用的构建生命周期。

这一层是纯 Python 业务架构，不包装 Maya Node，也不依赖 PyMEL。
具体 Component 自己决定如何使用 PyMEL 创建和操作 Maya 节点。
"""

from __future__ import print_function


class ComponentBase(object):
    u"""所有 System Component 共用的四阶段生命周期。"""

    def collect_inputs(self):
        u"""收集并验证当前 Component 的输入。"""
        raise NotImplementedError(
            u"子类必须实现 collect_inputs()。"
        )

    def prepare_data(self):
        u"""准备名称、数据和本次构建环境。"""
        raise NotImplementedError(
            u"子类必须实现 prepare_data()。"
        )

    def process_data(self):
        u"""执行当前 Component 的核心构建。"""
        raise NotImplementedError(
            u"子类必须实现 process_data()。"
        )

    def finalize_step(self):
        u"""检查并完成当前 Component。"""
        raise NotImplementedError(
            u"子类必须实现 finalize_step()。"
        )

    def run_step(self):
        u"""按照统一生命周期完整执行当前 Component。"""
        self.collect_inputs()
        self.prepare_data()
        self.process_data()
        self.finalize_step()
        return True


class RigComponentBase(ComponentBase):
    u"""具有 Joint / Controller / Connection 阶段的 Rig Component。"""

    def process_data(self):
        u"""按照标准 Rig 构建顺序执行三个核心阶段。"""
        self.create_joint()
        self.create_controller()
        self.create_connection()
        return True

    def create_joint(self):
        u"""创建当前 Component 所需的 Joint。"""
        raise NotImplementedError(
            u"子类必须实现 create_joint()。"
        )

    def create_controller(self):
        u"""创建当前 Component 所需的 Controller。"""
        raise NotImplementedError(
            u"子类必须实现 create_controller()。"
        )

    def create_connection(self):
        u"""建立当前 Component 的驱动和连接关系。"""
        raise NotImplementedError(
            u"子类必须实现 create_connection()。"
        )


__all__ = [
    "ComponentBase",
    "RigComponentBase",
]
