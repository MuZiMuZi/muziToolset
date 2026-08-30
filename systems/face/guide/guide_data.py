# coding=utf-8
u"""
Face Guide Data
===============

Step 02 Face Guide 的固定模板数据和构建参数定义。

设计原则：
    1. Guide Template 节点名称以 resources/face/face_guide.ma 为唯一来源；
    2. FaceGuide 不再通过场景字符串猜测“应该有哪些 Locator”；
    3. 点击“下一步”时必须检查模板中的全部 Locator 是否仍然存在；
    4. Controller 默认参数统一保存在本模块；
    5. 本模块只定义和校验数据，不创建 Maya Rig 节点。
"""

from __future__ import print_function

import os
import re

from .... import config as package_config
from ....core import file_utils


# =============================================================================
# Guide Template Contract
# =============================================================================

guide_template_file_name = "face_guide.ma"
guide_root_name = "grp_md_face_guide_001"
guide_move_ctrl_name = "ctrl_md_face_move_001"
guide_version = "1.0"

guide_locator_pattern = re.compile(
    r'createNode\s+transform\s+-n\s+"(loc_[^"]+_guide_\d+)"'
)

_template_locator_names_cache = None


def get_guide_template_path():
    u"""返回 Face Guide Template 的规范绝对路径。"""
    template_path = os.path.join(
        package_config.resources_dir,
        "face",
        guide_template_file_name
    )

    return file_utils.normalize_path(
        template_path
    )


def validate_guide_template_file():
    u"""检查 Face Guide Template 文件是否存在并返回路径。"""
    template_path = get_guide_template_path()

    if not os.path.isfile(template_path):
        raise RuntimeError(
            u"Face Guide 模板文件不存在: {}".format(
                template_path
            )
        )

    return template_path


def get_template_locator_names(refresh=False):
    u"""
    从 face_guide.ma 读取全部标准 Locator Transform 名称。

    Maya ASCII 节点名称均为 ASCII Token，因此使用 latin-1 解码可以避免模板文件
    Codeset 不同导致读取失败，同时不会改变节点名称内容。
    """
    global _template_locator_names_cache

    if _template_locator_names_cache is not None:
        if not refresh:
            return list(
                _template_locator_names_cache
            )

    template_path = validate_guide_template_file()

    with open(template_path, "rb") as file_object:
        file_data = file_object.read()

    text = file_data.decode(
        "latin-1"
    )

    locator_names = []
    matches = guide_locator_pattern.findall(
        text
    )

    for locator_name in matches:
        if locator_name in locator_names:
            continue

        locator_names.append(
            locator_name
        )

    if not locator_names:
        raise RuntimeError(
            u"Face Guide 模板中没有读取到标准 Locator: {}".format(
                template_path
            )
        )

    _template_locator_names_cache = locator_names

    return list(
        locator_names
    )


def get_part_guide_names(
        part,
        side=None,
        include_tokens=None,
        exclude_tokens=None
):
    u"""从 Template Contract 中按部位和 Side 返回固定 Guide 名称。"""
    if not part:
        raise ValueError(
            u"part 不能为空。"
        )

    valid_sides = [
        "lf",
        "rt",
        "md",
    ]

    if side is not None:
        if side not in valid_sides:
            raise ValueError(
                u"side 必须是 lf / rt / md / None。"
            )

    if include_tokens is None:
        include_tokens = []

    if exclude_tokens is None:
        exclude_tokens = []

    locator_names = get_template_locator_names()
    result = []

    for locator_name in locator_names:
        lower_name = locator_name.lower()

        if part.lower() not in lower_name:
            continue

        if side is not None:
            side_token = "_{}_".format(
                side
            )

            if side_token not in lower_name:
                continue

        include_passed = True

        for token in include_tokens:
            if token.lower() in lower_name:
                continue

            include_passed = False
            break

        if not include_passed:
            continue

        exclude_failed = False

        for token in exclude_tokens:
            if token.lower() not in lower_name:
                continue

            exclude_failed = True
            break

        if exclude_failed:
            continue

        result.append(
            locator_name
        )

    result.sort()
    return result


# =============================================================================
# Ordered Guide Data
# =============================================================================

lip_guide_names = {
    "upper": [
        "loc_rt_mouth_corner_guide_001",
        "loc_rt_upper_lip_guide_002",
        "loc_rt_upper_lip_guide_001",
        "loc_md_upper_lip_guide_001",
        "loc_lf_upper_lip_guide_001",
        "loc_lf_upper_lip_guide_002",
        "loc_lf_mouth_corner_guide_001",
    ],
    "lower": [
        "loc_rt_mouth_corner_guide_001",
        "loc_rt_lower_lip_guide_002",
        "loc_rt_lower_lip_guide_001",
        "loc_md_lower_lip_guide_001",
        "loc_lf_lower_lip_guide_001",
        "loc_lf_lower_lip_guide_002",
        "loc_lf_mouth_corner_guide_001",
    ],
    "corners": [
        "loc_rt_mouth_corner_guide_001",
        "loc_lf_mouth_corner_guide_001",
    ],
}


def get_eyelid_guide_names(side):
    u"""返回某侧 Upper / Lower Eyelid 的固定有序名称。"""
    if side not in ["lf", "rt"]:
        raise ValueError(
            u"Eyelid side 必须是 lf 或 rt。"
        )

    inner_name = "loc_{}_inner_lid_guide_001".format(
        side
    )
    outer_name = "loc_{}_outer_lid_guide_001".format(
        side
    )

    return {
        "upper": [
            inner_name,
            "loc_{}_upper_lid_guide_001".format(side),
            "loc_{}_upper_lid_guide_002".format(side),
            "loc_{}_upper_lid_guide_003".format(side),
            outer_name,
        ],
        "lower": [
            inner_name,
            "loc_{}_lower_lid_guide_001".format(side),
            "loc_{}_lower_lid_guide_002".format(side),
            "loc_{}_lower_lid_guide_003".format(side),
            outer_name,
        ],
    }


# =============================================================================
# Controller Settings
# =============================================================================

default_controller_settings = {
    "face_ctrl_global_scale": 1.0,
    "face_ctrl_color_lf": 6,
    "face_ctrl_color_rt": 13,
    "face_ctrl_color_md": 17,
    "brow_ctrl_size": 1.0,
    "eye_ctrl_size": 1.0,
    "eyelid_ctrl_size": 1.0,
    "nose_ctrl_size": 1.0,
    "cheek_ctrl_size": 1.0,
    "lip_ctrl_size": 1.0,
    "jaw_ctrl_size": 1.0,
}

controller_setting_attr_types = {
    "face_ctrl_global_scale": "double",
    "face_ctrl_color_lf": "long",
    "face_ctrl_color_rt": "long",
    "face_ctrl_color_md": "long",
    "brow_ctrl_size": "double",
    "eye_ctrl_size": "double",
    "eyelid_ctrl_size": "double",
    "nose_ctrl_size": "double",
    "cheek_ctrl_size": "double",
    "lip_ctrl_size": "double",
    "jaw_ctrl_size": "double",
}

# UI 按面部从上到下排列。
controller_module_order = [
    "brow",
    "eye",
    "eyelid",
    "nose",
    "cheek",
    "lip",
    "jaw",
]

controller_size_attr_names = [
    "brow_ctrl_size",
    "eye_ctrl_size",
    "eyelid_ctrl_size",
    "nose_ctrl_size",
    "cheek_ctrl_size",
    "lip_ctrl_size",
    "jaw_ctrl_size",
]

controller_color_attr_names = [
    "face_ctrl_color_lf",
    "face_ctrl_color_rt",
    "face_ctrl_color_md",
]


def get_default_controller_settings():
    u"""返回独立的默认 Controller Settings。"""
    settings = {}

    for attr_name in default_controller_settings:
        settings[attr_name] = default_controller_settings.get(
            attr_name
        )

    return settings


def validate_controller_settings(settings):
    u"""检查 Step 02 Controller Settings。"""
    if not isinstance(settings, dict):
        raise TypeError(
            u"Controller Settings 必须是 dict。"
        )

    global_scale = settings.get(
        "face_ctrl_global_scale"
    )

    if global_scale is None:
        raise ValueError(
            u"缺少 face_ctrl_global_scale。"
        )

    if float(global_scale) <= 0.0:
        raise ValueError(
            u"Face Controller Global Scale 必须大于 0。"
        )

    for attr_name in controller_size_attr_names:
        value = settings.get(
            attr_name
        )

        if value is None:
            raise ValueError(
                u"缺少 Controller Size: {}".format(
                    attr_name
                )
            )

        if float(value) <= 0.0:
            raise ValueError(
                u"Controller Size 必须大于 0: {}".format(
                    attr_name
                )
            )

    for attr_name in controller_color_attr_names:
        value = settings.get(
            attr_name
        )

        if value is None:
            raise ValueError(
                u"缺少 Controller Color: {}".format(
                    attr_name
                )
            )

        color_index = int(
            value
        )

        if color_index < 0 or color_index > 31:
            raise ValueError(
                u"Maya Index Color 必须在 0～31：{} = {}".format(
                    attr_name,
                    color_index
                )
            )

    return True


__all__ = [
    "guide_template_file_name",
    "guide_root_name",
    "guide_move_ctrl_name",
    "guide_version",
    "get_guide_template_path",
    "validate_guide_template_file",
    "get_template_locator_names",
    "get_part_guide_names",
    "lip_guide_names",
    "get_eyelid_guide_names",
    "default_controller_settings",
    "controller_setting_attr_types",
    "controller_module_order",
    "controller_size_attr_names",
    "controller_color_attr_names",
    "get_default_controller_settings",
    "validate_controller_settings",
]
