# coding=utf-8
u"""
Face Controller Defaults
========================

集中定义当前正式 Face Rig 的 Controller Appearance 默认值。

该模块在 systems.face 包初始化时把正式默认值写入现有 config 数据结构，
因此 UI 构建、FaceBuild 和单独 Module Build 都读取同一份运行时默认配置。
已经保存在 Face Config 中的用户自定义值不会被这里覆盖。
"""

from __future__ import print_function

from . import config


CONTROLLER_DEFAULT_VALUES = {
    "global_scale": 1.0,
    "color_lf": 6,
    "color_rt": 13,
    "color_md": 17,
    "brow": 1.1,
    "eye": 1.0,
    "eyelid": 1.3,
    "nose": 0.5,
    "cheek": 1.3,
    "lip": 1.8,
    "jaw": 1.0,
    "teeth": 1.0,
    "tongue": 1.0,
}


def apply_controller_defaults():
    u"""
    把正式 Controller Appearance 默认值应用到 Face Config 运行时配置。

    Returns:
        dict:
            应用完成后的 config.face_controller_default_settings。
    """
    settings = config.face_controller_default_settings

    settings[config.face_controller_global_scale_attr] = CONTROLLER_DEFAULT_VALUES[
        "global_scale"
    ]
    settings[config.face_controller_color_attr_names["lf"]] = CONTROLLER_DEFAULT_VALUES[
        "color_lf"
    ]
    settings[config.face_controller_color_attr_names["rt"]] = CONTROLLER_DEFAULT_VALUES[
        "color_rt"
    ]
    settings[config.face_controller_color_attr_names["md"]] = CONTROLLER_DEFAULT_VALUES[
        "color_md"
    ]

    for module_name in config.face_controller_module_order:
        attr_name = config.face_controller_size_attr_names.get(
            module_name
        )

        if not attr_name:
            continue

        settings[attr_name] = CONTROLLER_DEFAULT_VALUES.get(
            module_name,
            1.0
        )

    return settings


__all__ = [
    "CONTROLLER_DEFAULT_VALUES",
    "apply_controller_defaults",
]
