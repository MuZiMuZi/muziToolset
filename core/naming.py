# coding=utf-8
u"""
Rig Naming
==========

Muzi Toolset 的正式 Rig Naming 规则。

该模块只负责项目自己的名称语义，不包装 Maya Node。
"""

from __future__ import print_function

import re

import pymel.core as pm


SIDE_ALIASES = {
    "l": "lf",
    "left": "lf",
    "lf": "lf",
    "r": "rt",
    "right": "rt",
    "rt": "rt",
    "c": "md",
    "center": "md",
    "centre": "md",
    "m": "md",
    "mid": "md",
    "middle": "md",
    "md": "md",
}


def normalize_name_part(value, label="name"):
    u"""把名称字段整理成稳定的 snake_case 片段。"""
    if value is None:
        raise ValueError(
            u"{} 不能为空。".format(label)
        )

    value = str(value).strip().lower()
    value = value.replace("-", "_")
    value = value.replace(" ", "_")

    while "__" in value:
        value = value.replace("__", "_")

    value = value.strip("_")

    if not value:
        raise ValueError(
            u"{} 不能为空。".format(label)
        )

    if not re.match(r"^[a-z0-9_]+$", value):
        raise ValueError(
            u"{} 包含不支持的字符：{}".format(
                label,
                value
            )
        )

    return value


def normalize_side(side):
    u"""把方向统一成 lf / rt / md。"""
    key = normalize_name_part(
        side,
        "side"
    )

    result = SIDE_ALIASES.get(
        key
    )

    if result is None:
        raise ValueError(
            u"不支持的 Side：{}".format(
                side
            )
        )

    return result


def create_name(
        node_type,
        side,
        part,
        function,
        index=1
):
    u"""
    创建标准 Rig 名称。

    格式：
        [type]_[side]_[part]_[function]_[index]
    """
    node_type = normalize_name_part(
        node_type,
        "node_type"
    )
    side = normalize_side(
        side
    )
    part = normalize_name_part(
        part,
        "part"
    )
    function = normalize_name_part(
        function,
        "function"
    )

    if not isinstance(index, int):
        raise TypeError(
            u"index 必须是整数。"
        )

    if index < 1:
        raise ValueError(
            u"index 不能小于 1。"
        )

    return "{}_{}_{}_{}_{:03d}".format(
        node_type,
        side,
        part,
        function,
        index
    )


def create_attribute_name(
        node_type,
        side,
        part,
        function
):
    u"""创建不带序号的 Config Attribute 名称。"""
    node_name = create_name(
        node_type=node_type,
        side=side,
        part=part,
        function=function,
        index=1
    )

    return node_name.rsplit(
        "_",
        1
    )[0]


def create_unique_name(
        node_type,
        side,
        part,
        function,
        start_index=1
):
    u"""根据当前 Maya Scene 返回第一个未被占用的标准名称。"""
    index = start_index

    while True:
        name = create_name(
            node_type=node_type,
            side=side,
            part=part,
            function=function,
            index=index
        )

        if not pm.objExists(name):
            return name

        index += 1


__all__ = [
    "normalize_name_part",
    "normalize_side",
    "create_name",
    "create_attribute_name",
    "create_unique_name",
]
