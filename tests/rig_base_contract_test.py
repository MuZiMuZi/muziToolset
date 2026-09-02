# coding=utf-8
u"""
RigBase Contract Test
=====================

非 Maya 环境下验证 RigBase 的正式 Naming 契约：

    type / side / part / function / index
    name
    compose
    decompose
    parse_name
    mirror_name

绑定库内部 Naming 默认可信，不测试重复的名称格式 Normalize / Validate。
"""

from __future__ import print_function

import os
import sys


if __package__:
    from ..systems.rig_base import RigBase
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

    from muziToolset.systems.rig_base import RigBase


def run():
    u"""验证 RigBase 既能组合名称，也能从已有名称拆分属性。"""
    jaw_ctrl = RigBase(
        type="ctrl",
        side="md",
        part="jaw",
        function="bind",
        index=1
    )

    if jaw_ctrl.name != "ctrl_md_jaw_bind_001":
        print("[FAIL] RigBase.name: {}".format(jaw_ctrl.name))
        return False

    if jaw_ctrl.type != "ctrl":
        print("[FAIL] RigBase.type: {}".format(jaw_ctrl.type))
        return False

    if jaw_ctrl.side != "md":
        print("[FAIL] RigBase.side: {}".format(jaw_ctrl.side))
        return False

    if jaw_ctrl.part != "jaw":
        print("[FAIL] RigBase.part: {}".format(jaw_ctrl.part))
        return False

    if jaw_ctrl.function != "bind":
        print("[FAIL] RigBase.function: {}".format(jaw_ctrl.function))
        return False

    if jaw_ctrl.index != 1:
        print("[FAIL] RigBase.index: {}".format(jaw_ctrl.index))
        return False

    parsed_ctrl = RigBase(
        name="ctrl_lf_upper_teeth_anim_003"
    )

    expected_attributes = {
        "type": "ctrl",
        "side": "lf",
        "part": "upper_teeth",
        "function": "anim",
        "index": 3,
    }

    for attribute_name in expected_attributes:
        current_value = getattr(
            parsed_ctrl,
            attribute_name
        )

        if current_value != expected_attributes[attribute_name]:
            print(
                "[FAIL] RigBase.decompose {}: {}".format(
                    attribute_name,
                    current_value
                )
            )
            return False

    if parsed_ctrl.name != "ctrl_lf_upper_teeth_anim_003":
        print("[FAIL] RigBase.decompose name: {}".format(parsed_ctrl.name))
        return False

    name_data = RigBase.parse_name(
        "jnt_rt_brow_bind_012"
    )

    expected_name_data = {
        "type": "jnt",
        "side": "rt",
        "part": "brow",
        "function": "bind",
        "index": 12,
    }

    for field_name in expected_name_data:
        if name_data[field_name] != expected_name_data[field_name]:
            print(
                "[FAIL] RigBase.parse_name {}: {}".format(
                    field_name,
                    name_data[field_name]
                )
            )
            return False

    override_name = jaw_ctrl.create_name(
        type="jnt",
        side="lf",
        part="jaw_corner",
        function="bind",
        index=2
    )

    if override_name != "jnt_lf_jaw_corner_bind_002":
        print("[FAIL] RigBase.create_name: {}".format(override_name))
        return False

    if jaw_ctrl.name != "ctrl_md_jaw_bind_001":
        print("[FAIL] create_name() 临时覆盖修改了实例属性。")
        return False

    mirror_name = parsed_ctrl.mirror_name()

    if mirror_name != "ctrl_rt_upper_teeth_anim_003":
        print("[FAIL] RigBase.mirror_name: {}".format(mirror_name))
        return False

    if parsed_ctrl.get_opposite_side() != "rt":
        print("[FAIL] RigBase.get_opposite_side() 错误。")
        return False

    module_identity = RigBase(
        side="md",
        part="face",
        index=1
    )

    if module_identity.name is not None:
        print("[FAIL] 不完整 Naming 不应该生成节点名称。")
        return False

    retired_attributes = [
        "identity",
        "set_identity",
        "resolve_identity",
        "flip_side",
        "is_left",
        "is_right",
        "is_center",
        "_normalize_token",
        "normalize_side",
        "normalize_part",
        "normalize_node_type",
        "normalize_function",
        "validate_index",
        "validate_name",
    ]

    for attribute_name in retired_attributes:
        if hasattr(jaw_ctrl, attribute_name):
            print(
                "[FAIL] RigBase 重新出现已删除 API：{}".format(
                    attribute_name
                )
            )
            return False

    print("[PASS] RigBase Naming Object Contract 正常。")
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
