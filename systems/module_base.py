# coding=utf-8
u"""
Module Base
===========

所有 MuziTools Rig Module 共用的统一构建规范。

继承关系：

    RigBase
        ↓
    ModuleBase
        ↓
    RigModuleBase

ModuleBase 不重新定义 Rig Identity。
每个具体 Module 在初始化时把自己的 side / part / index 交给 RigBase。

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
"""

from __future__ import print_function

from .rig_base import RigBase


class ModuleBase(RigBase):
    u"""所有 Rig Module 共用的 Identity + 四阶段生命周期基础类。"""

    def __init__(
            self,
            side="md",
            part=None,
            index=1
    ):
        u"""
        初始化 Module Identity。

        Args:
            side (str):
                方向标记，常用值为 lf、rt 或 md。
            part (str):
                Face / Rig 命名中的部位 Token，例如 lip、brow、eye、jaw。
            index (int):
                目标元素或节点的序号。
        """
        super(ModuleBase, self).__init__(
            side=side,
            part=part,
            index=index
        )

    def collect_inputs(self):
        u"""
        收集、规范化并检查当前 Module 输入。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 collect_inputs()。"
        )

    def prepare_data(self):
        u"""
        准备当前 Module 的执行环境和中间数据。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 prepare_data()。"
        )

    def process_data(self):
        u"""
        执行当前 Module 的核心处理逻辑。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 process_data()。"
        )

    def finalize_step(self):
        u"""
        检查、保存并完成当前 Module。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 finalize_step()。"
        )

    def run_step(self):
        u"""
        按照统一生命周期完整执行当前 Module。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        self.collect_inputs()
        self.prepare_data()
        self.process_data()
        self.finalize_step()
        return True


class RigModuleBase(ModuleBase):
    u"""需要 Joint、Controller 和 Connection 的标准 Rig Module 基类。"""

    def process_data(self):
        u"""
        按标准顺序执行 Rig Module 的核心构建。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        self.create_joint()
        self.create_controller()
        self.create_connection()
        return True

    def create_joint(self):
        u"""
        创建当前 Rig Module 所需的 Joint。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 create_joint()。"
        )

    def create_controller(self):
        u"""
        创建当前 Rig Module 所需的 Controller。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 create_controller()。"
        )

    def create_connection(self):
        u"""
        建立当前 Rig Module 的最终驱动关系。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 create_connection()。"
        )


__all__ = [
    "ModuleBase",
    "RigModuleBase",
]
