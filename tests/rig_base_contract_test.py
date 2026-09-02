# coding=utf-8
u"""
RigBase Contract Test
=====================

非 Maya 环境下验证正式 Rig Naming Contract。

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
    u"""验证 RigBase 创建、解析、镜像和字段限制。"""
    name = RigBase.create_name(
        type="ctrl",
        side="left",
        part="upper_teeth",
        function="bind",
        index=3
    )

    if name != "ctrl_lf_upper_teeth_bind_003":
        print(
            "[FAIL] RigBase.create_name: {}".format(
                name
            )
        )
        return False

    fields = RigBase.parse_name(
        name
    )

    expected_fields = {
        "type": "ctrl",
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

    mirrored_name = RigBase.mirror_name(
        name
    )

    if mirrored_name != "ctrl_rt_upper_teeth_bind_003":
        print(
            "[FAIL] RigBase.mirror_name: {}".format(
                mirrored_name
            )
        )
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

    try:
        RigBase.create_name(
            type="ctrl",
            side="md",
            part="face",
            function="global_scale",
            index=1
        )
    except ValueError:
        pass
    else:
        print("[FAIL] function 允许了下划线。")
        return False

    rig_name = RigBase(
        name="jnt_lf_brow_bind_002"
    )

    if rig_name.type != "jnt":
        print("[FAIL] RigBase(name=...) 没有自动解析 type。")
        return False

    if rig_name.side != "lf":
        print("[FAIL] RigBase(name=...) 没有自动解析 side。")
        return False

    if rig_name.part != "brow":
        print("[FAIL] RigBase(name=...) 没有自动解析 part。")
        return False

    if rig_name.function != "bind":
        print("[FAIL] RigBase(name=...) 没有自动解析 function。")
        return False

    if rig_name.index != 2:
        print("[FAIL] RigBase(name=...) 没有自动解析 index。")
        return False

    rig_name.flip()

    if rig_name.name != "jnt_rt_brow_bind_002":
        print("[FAIL] RigBase.flip() 结果错误。")
        return False

    print("[PASS] RigBase Naming Contract 正常。")
    return True


if __name__ == "__main__":
    if not run():
        raise SystemExit(1)
