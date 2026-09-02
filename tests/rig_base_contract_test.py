# coding=utf-8
u"""
RigBase Contract Test
=====================

非 Maya 环境下验证 RigBase 的正式对象契约：

    Direct Instance Attributes
    Naming
    Parse
    Mirror
    Side Semantic
    Index Contract
    node_type Contract

支持：
    python tests/rig_base_contract_test.py

也支持作为 muziToolset.tests 包内模块调用。
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
    u"""验证 RigBase 使用直接实例属性，而不是额外 Identity 包装。"""
    rig_object = RigBase(
        side="left",
        part="upper_teeth",
        index=3
    )

    if rig_object.side != "lf":
        print("[FAIL] RigBase.side: {}".format(rig_object.side))
        return False

    if rig_object.part != "upper_teeth":
        print("[FAIL] RigBase.part: {}".format(rig_object.part))
        return False

    if rig_object.index != 3:
        print("[FAIL] RigBase.index: {}".format(rig_object.index))
        return False

    name = rig_object.create_name(
        node_type="ctrl",
        function="bind"
    )

    if name != "ctrl_lf_upper_teeth_bind_003":
        print(
            "[FAIL] RigBase.create_name: {}".format(
                name
            )
        )
        return False

    override_name = rig_object.create_name(
        node_type="jnt",
        part="lower_teeth",
        function="bind",
        index=1
    )

    if override_name != "jnt_lf_lower_teeth_bind_001":
        print(
            "[FAIL] RigBase.create_name Override: {}".format(
                override_name
            )
        )
        return False

    if rig_object.side != "lf":
        print("[FAIL] create_name() Override 修改了实例 side。")
        return False

    if rig_object.part != "upper_teeth":
        print("[FAIL] create_name() Override 修改了实例 part。")
        return False

    if rig_object.index != 3:
        print("[FAIL] create_name() Override 修改了实例 index。")
        return False

    fields = RigBase.parse_name(
        name
    )

    expected_fields = {
        "node_type": "ctrl",
        "side": "lf",
        "part": "upper_teeth",
        "function": "bind",
        "index": 3,
    }

    for field_name in expected_fields:
        if fields.get(field_name) != expected_fields[field_name]:
            print(
                "[FAIL] RigBase.parse_name {}: {}".format(
                    field_name,
                    fields.get(field_name)
                )
            )
            return False

    mirrored_name = rig_object.mirror_name(
        name
    )

    if mirrored_name != "ctrl_rt_upper_teeth_bind_003":
        print(
            "[FAIL] RigBase.mirror_name: {}".format(
                mirrored_name
            )
        )
        return False

    if rig_object.get_opposite_side() != "rt":
        print("[FAIL] RigBase.get_opposite_side() 错误。")
        return False

    if rig_object.side != "lf":
        print("[FAIL] get_opposite_side() 修改了实例 side。")
        return False

    center_object = RigBase(
        side="center",
        part="jaw",
        index=1
    )

    if center_object.side != "md":
        print("[FAIL] center Side 没有规范为 md。")
        return False

    if center_object.get_opposite_side() != "md":
        print("[FAIL] Center Opposite Side 应保持 md。")
        return False

    if not RigBase.validate_name(
            "jnt_md_jaw_bind_001"
    ):
        print("[FAIL] 标准 Rig Name 被错误判定为无效。")
        return False

    if RigBase.validate_name(
            "ctrl_md_face_global_scale"
    ):
        print("[FAIL] 缺少三位 index 的名称被错误判定为有效。")
        return False

    invalid_range_values = [
        0,
        1000,
    ]

    for invalid_index in invalid_range_values:
        try:
            RigBase(
                side="md",
                part="jaw",
                index=invalid_index
            )
        except ValueError:
            pass
        else:
            print(
                "[FAIL] RigBase 接受了越界 Index：{}".format(
                    invalid_index
                )
            )
            return False

    invalid_type_values = [
        True,
        1.5,
    ]

    for invalid_index in invalid_type_values:
        try:
            RigBase(
                side="md",
                part="jaw",
                index=invalid_index
            )
        except TypeError:
            pass
        else:
            print(
                "[FAIL] RigBase 接受了非整数 Index：{}".format(
                    invalid_index
                )
            )
            return False

    try:
        rig_object.create_name(
            node_type="parent_matrix",
            function="bind"
        )
    except ValueError:
        pass
    else:
        print("[FAIL] node_type 允许了下划线。")
        return False

    try:
        rig_object.create_name(
            node_type="ctrl",
            function="global_scale"
        )
    except ValueError:
        pass
    else:
        print("[FAIL] function 允许了下划线。")
        return False

    retired_type_kwargs = {
        "type": "ctrl",
        "function": "bind",
    }

    try:
        rig_object.create_name(
            **retired_type_kwargs
        )
    except TypeError:
        pass
    else:
        print("[FAIL] RigBase.create_name() 仍接受退休的 type= Keyword。")
        return False

    retired_attributes = [
        "name",
        "compose",
        "decompose",
        "flip",
        "identity",
        "set_identity",
        "resolve_identity",
        "flip_side",
        "is_left",
        "is_right",
        "is_center",
    ]

    for attribute_name in retired_attributes:
        if hasattr(rig_object, attribute_name):
            print(
                "[FAIL] RigBase 仍保留已精简 API：{}".format(
                    attribute_name
                )
            )
            return False

    print("[PASS] RigBase Direct Attribute + Naming Contract 正常。")
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
