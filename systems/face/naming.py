# coding=utf-8
u"""
Face Naming
===========

Face System 内部共享的 Rig Naming 组合规则。

本模块只处理 Face Builder 经常使用的一个业务约定：

    part + multi-token role
        ↓
    [type]_[side]_[part + role prefix]_[role last token]_[index]

例如：

    part = "lip"
    role = "upper_zip_offset"

得到：

    grp_md_lip_upper_zip_offset_001

边界：
    - 五段式名称对象仍由 systems.rig_base.RigBase 负责；
    - 本模块只是 Face System 内多个 Builder 的共享组合规则；
    - 不进入 Core，因为 region / feature / role 属于 Rig 业务语义。
"""

from __future__ import print_function

from ..rig_base import RigBase


def create_role_name(
        type,
        side,
        part,
        role,
        index=1
):
    u"""
    把多 Token Role 合并进 Part，并返回标准 Rig Name。

    Args:
        type (str):
            需要创建的 Rig Node Type，例如 grp、jnt、ctrl。
        side (str):
            Rig Side，正式值为 lf、rt 或 md。
        part (str):
            Face Builder 当前基础 Part。
        role (str):
            需要拆成 Part Prefix + Function 的业务 Role。
        index (int):
            Rig Name 使用的节点序号。

    Returns:
        str:
            根据当前 Face Naming 业务规则组合后的标准 Rig Name。
    """
    role_parts = role.split("_")
    function = role_parts[-1]
    final_part = part

    if len(role_parts) > 1:
        role_prefix = "_".join(
            role_parts[:-1]
        )
        final_part = "{}_{}".format(
            part,
            role_prefix
        )

    rig_name = RigBase(
        type=type,
        side=side,
        part=final_part,
        function=function,
        index=index
    )

    return rig_name.name


def create_feature_name(
        type,
        side,
        region,
        feature,
        role,
        index=1
):
    u"""
    创建 region + feature 形式的 Face Builder 标准名称。

    Args:
        type (str):
            需要创建的 Rig Node Type，例如 grp、jnt、ctrl。
        side (str):
            Rig Side，正式值为 lf、rt 或 md。
        region (str):
            Face 区域，例如 upper、lower 或 brow。
        feature (str):
            当前 Face Builder Feature，例如 lid 或 eye_bag。
        role (str):
            需要拆成 Part Prefix + Function 的业务 Role。
        index (int):
            Rig Name 使用的节点序号。

    Returns:
        str:
            根据 Region、Feature 和 Role 组合后的标准 Rig Name。
    """
    part = "{}_{}".format(
        region,
        feature
    )

    return create_role_name(
        type=type,
        side=side,
        part=part,
        role=role,
        index=index
    )


__all__ = [
    "create_role_name",
    "create_feature_name",
]
