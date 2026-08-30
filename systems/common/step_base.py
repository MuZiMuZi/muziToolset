# coding=utf-8
u"""
Step Base
=========

所有“分步骤构建型 System”共享的 Step 生命周期基类。

统一生命周期
------------
    collect_inputs()
    prepare_data()
    process_data()
    finalize_step()

执行入口
--------
    run_step()

职责约定
--------
collect_inputs()
    收集当前 Step 输入，同时完成必要的输入规范化和有效性检查。

prepare_data()
    准备当前 Step 执行所需的层级、名称、中间数据和旧结果清理。

process_data()
    执行当前 Step 的核心处理逻辑。

finalize_step()
    检查最终结果、保存配置、整理状态，并准备交给下一个 Step。

代码可读性规范
--------------
生命周期大方法中调用项目自定义方法时，调用前必须写一行中文注释，说明：
    1. 为什么调用；
    2. 这一调用在当前阶段承担什么作用。

普通变量赋值、简单 if / for 和明显的 Python 基础操作不强制逐行注释，
避免为了注释而注释。

设计边界
--------
- 本类只定义 System Step Workflow，不依赖 Maya；
- Maya 节点、Attribute、Hierarchy、Geometry 等能力继续由 core 提供；
- Face / Body / Hair 等业务规则由具体 System 子类实现。
"""

from __future__ import print_function


class StepBase(object):
    u"""分步骤 Rig System 的统一生命周期基类。"""

    def collect_inputs(self):
        u"""
        收集、规范化并检查当前 Step 输入。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 collect_inputs()。"
        )

    def prepare_data(self):
        u"""
        准备当前 Step 的执行环境和中间数据。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 prepare_data()。"
        )

    def process_data(self):
        u"""
        执行当前 Step 的核心处理逻辑。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 process_data()。"
        )

    def finalize_step(self):
        u"""
        检查、保存并完成当前 Step。

        Raises:
            NotImplementedError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        raise NotImplementedError(
            u"子类必须实现 finalize_step()。"
        )

    def run_step(self):
        u"""
        按照统一生命周期完整执行当前 Step。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # 收集并检查当前 Step 的全部输入，阻止无效数据继续进入后续阶段。
        self.collect_inputs()

        # 准备本次执行需要的层级、名称、中间数据以及旧结果清理。
        self.prepare_data()

        # 执行当前 Step 真正的核心场景或数据处理。
        self.process_data()

        # 检查最终结果、保存配置并完成当前 Step 状态。
        self.finalize_step()

        return True


__all__ = [
    "StepBase",
]
