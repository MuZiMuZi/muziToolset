# coding=utf-8
u"""
Component Base Contract Test
============================

检查所有 Component 共用的四阶段生命周期，以及标准 Rig Component 的三阶段构建顺序。

本测试不依赖 Maya，可以直接在普通 Python 环境中运行。
"""

from __future__ import print_function

from systems.component_base import ComponentBase
from systems.component_base import RigComponentBase


class TestComponent(ComponentBase):
    u"""用于验证 ComponentBase 生命周期顺序的最小测试类。"""

    def __init__(self):
        self.calls = []

    def collect_inputs(self):
        self.calls.append(
            "collect_inputs"
        )
        return True

    def prepare_data(self):
        self.calls.append(
            "prepare_data"
        )
        return True

    def process_data(self):
        self.calls.append(
            "process_data"
        )
        return True

    def finalize_step(self):
        self.calls.append(
            "finalize_step"
        )
        return True


class TestRigComponent(RigComponentBase):
    u"""用于验证 RigComponentBase 三阶段构建顺序的最小测试类。"""

    def __init__(self):
        self.calls = []

    def collect_inputs(self):
        self.calls.append(
            "collect_inputs"
        )
        return True

    def prepare_data(self):
        self.calls.append(
            "prepare_data"
        )
        return True

    def create_joint(self):
        self.calls.append(
            "create_joint"
        )
        return True

    def create_controller(self):
        self.calls.append(
            "create_controller"
        )
        return True

    def create_connection(self):
        self.calls.append(
            "create_connection"
        )
        return True

    def finalize_step(self):
        self.calls.append(
            "finalize_step"
        )
        return True


def test_component_lifecycle():
    u"""检查 ComponentBase 是否严格执行四阶段生命周期。"""
    component = TestComponent()
    result = component.run_step()

    expected_calls = [
        "collect_inputs",
        "prepare_data",
        "process_data",
        "finalize_step",
    ]

    if result is not True:
        raise RuntimeError(
            u"ComponentBase.run_step() 没有返回 True。"
        )

    if component.calls != expected_calls:
        raise RuntimeError(
            u"ComponentBase 生命周期顺序错误：{}".format(
                component.calls
            )
        )

    return True


def test_rig_component_lifecycle():
    u"""检查 RigComponentBase 是否在 process_data 中执行标准三阶段构建。"""
    component = TestRigComponent()
    result = component.run_step()

    expected_calls = [
        "collect_inputs",
        "prepare_data",
        "create_joint",
        "create_controller",
        "create_connection",
        "finalize_step",
    ]

    if result is not True:
        raise RuntimeError(
            u"RigComponentBase.run_step() 没有返回 True。"
        )

    if component.calls != expected_calls:
        raise RuntimeError(
            u"RigComponentBase 构建顺序错误：{}".format(
                component.calls
            )
        )

    return True


def run():
    u"""执行全部 Component Base Contract Test。"""
    print("=" * 78)
    print("Muzi Toolset - Component Base Contract Test")
    print("=" * 78)

    test_component_lifecycle()
    test_rig_component_lifecycle()

    print(u"[PASS] ComponentBase / RigComponentBase 构建规范正确。")
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
