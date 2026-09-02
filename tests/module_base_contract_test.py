# coding=utf-8
u"""
ModuleBase Contract Test
========================

验证 ModuleBase / RigModuleBase 的统一生命周期与 Rig Identity 继承。
本测试不依赖 Maya。

支持：
    python tests/module_base_contract_test.py

也支持作为 muziToolset.tests 包内模块调用。
"""

from __future__ import print_function

import os
import sys


if __package__:
    from ..systems.module_base import ModuleBase
    from ..systems.module_base import RigModuleBase
else:
    package_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    package_parent = os.path.dirname(
        package_root
    )

    if package_parent not in sys.path:
        sys.path.insert(
            0,
            package_parent
        )

    from muziToolset.systems.module_base import ModuleBase
    from muziToolset.systems.module_base import RigModuleBase


class TestModule(ModuleBase):
    u"""记录 ModuleBase 生命周期调用顺序。"""

    def __init__(self):
        super(TestModule, self).__init__(
            side="lf",
            part="test_module",
            index=2
        )
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


class TestRigModule(RigModuleBase):
    u"""记录 RigModuleBase 的 Rig Build 调用顺序。"""

    def __init__(self):
        super(TestRigModule, self).__init__(
            side="rt",
            part="test_rig",
            index=4
        )
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


def run():
    u"""运行 Module 生命周期和 Rig Identity 契约检查。"""
    module = TestModule()

    if module.identity != {
            "side": "lf",
            "part": "test_module",
            "index": 2,
    }:
        print(
            "[FAIL] ModuleBase Identity: {}".format(
                module.identity
            )
        )
        return False

    module_name = module.create_name(
        node_type="grp",
        function="main"
    )

    if module_name != "grp_lf_test_module_main_002":
        print(
            "[FAIL] ModuleBase Identity Naming: {}".format(
                module_name
            )
        )
        return False

    module.run_step()

    expected_module_calls = [
        "collect_inputs",
        "prepare_data",
        "process_data",
        "finalize_step",
    ]

    if module.calls != expected_module_calls:
        print(
            "[FAIL] ModuleBase Lifecycle: {}".format(
                module.calls
            )
        )
        return False

    rig_module = TestRigModule()

    if rig_module.identity != {
            "side": "rt",
            "part": "test_rig",
            "index": 4,
    }:
        print(
            "[FAIL] RigModuleBase Identity: {}".format(
                rig_module.identity
            )
        )
        return False

    rig_module.run_step()

    expected_rig_calls = [
        "collect_inputs",
        "prepare_data",
        "create_joint",
        "create_controller",
        "create_connection",
        "finalize_step",
    ]

    if rig_module.calls != expected_rig_calls:
        print(
            "[FAIL] RigModuleBase Lifecycle: {}".format(
                rig_module.calls
            )
        )
        return False

    print("[PASS] ModuleBase / RigModuleBase Identity + Lifecycle Contract 正常。")
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
