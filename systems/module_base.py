# coding=utf-8
u"""
Module Base
===========

所有 MuziTools Rig Module 共用的统一构建规范。

术语统一：
    Component -> Module

标准 Module 生命周期：

    collect_inputs()
    prepare_data()
    process_data()
    finalize_step()

统一执行入口：

    run_step()

真正涉及 Joint、Controller 和 Connection 的 Rig Module 使用 RigModuleBase：

    create_joint()
    create_controller()
    create_connection()

Rig Module 同时继承 RigBase，因此可以直接使用：

    self.create_name()
    self.parse_name()
    self.normalize_side()
    self.mirror_name()
"""

from __future__ import print_function

from .rig_base import RigBase


class ModuleBase(RigBase):
    u"""所有 Rig Module 共用的四阶段生命周期基础类。"""

    def collect_inputs(self):
        u"""收集、规范化并检查当前 Module 输入。"""
        raise NotImplementedError(
            u"子类必须实现 collect_inputs()。"
        )

    def prepare_data(self):
        u"""准备当前 Module 的执行环境和中间数据。"""
        raise NotImplementedError(
            u"子类必须实现 prepare_data()。"
        )

    def process_data(self):
        u"""执行当前 Module 的核心处理逻辑。"""
        raise NotImplementedError(
            u"子类必须实现 process_data()。"
        )

    def finalize_step(self):
        u"""检查、保存并完成当前 Module。"""
        raise NotImplementedError(
            u"子类必须实现 finalize_step()。"
        )

    def run_step(self):
        u"""按照统一生命周期完整执行当前 Module。"""
        self.collect_inputs()
        self.prepare_data()
        self.process_data()
        self.finalize_step()
        return True


class RigModuleBase(ModuleBase):
    u"""需要 Joint、Controller 和 Connection 的标准 Rig Module 基类。"""

    def process_data(self):
        u"""按标准顺序执行 Rig Module 的核心构建。"""
        self.create_joint()
        self.create_controller()
        self.create_connection()
        return True

    def create_joint(self):
        u"""创建当前 Rig Module 所需的 Joint。"""
        raise NotImplementedError(
            u"子类必须实现 create_joint()。"
        )

    def create_controller(self):
        u"""创建当前 Rig Module 所需的 Controller。"""
        raise NotImplementedError(
            u"子类必须实现 create_controller()。"
        )

    def create_connection(self):
        u"""建立当前 Rig Module 的最终驱动关系。"""
        raise NotImplementedError(
            u"子类必须实现 create_connection()。"
        )


__all__ = [
    "ModuleBase",
    "RigModuleBase",
]
