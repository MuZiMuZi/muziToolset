# coding=utf-8
u"""
Face Guide Settings
===================

Step 02 使用的 Face Controller 构建参数。

职责：
    1. 定义 Face Controller 默认大小和 Side Color；
    2. 从 Face Config 读取 Step 02 构建参数；
    3. 把 UI 收集到的参数写入统一 Face Config；
    4. 给后续 Jaw / Lip / Eye / Brow 等 Component 提供稳定数据入口。

重要边界：
    - 本模块只管理普通配置值，不创建 Maya Controller；
    - Config Network Node 的底层 CRUD 继续由 FaceBase -> core.config_utils 负责；
    - Controller 的真实创建仍然由 systems.controller 负责；
    - UI 只负责收集参数，不直接操作 Config Attribute。
"""

from __future__ import print_function


# =============================================================================
# Default Settings
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

# 按面部从上到下排列，UI 和后续 Component 读取时保持同一顺序。
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


# =============================================================================
# Validate
# =============================================================================

def validate_controller_settings(settings):
    u"""
    检查 Step 02 Controller Settings。

    Args:
        settings (dict):
            UI 或其它 Face System 提交的 Controller 配置。

    Returns:
        bool:
        配置有效时返回 True。

    Raises:
        TypeError:
            输入不是 dict 时抛出。
        ValueError:
            Scale / Size / Color 超出允许范围时抛出。
    """
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


# =============================================================================
# Read / Write
# =============================================================================

def get_default_controller_settings():
    u"""
    返回一份独立的默认 Controller Settings。

    Returns:
        dict:
        默认配置副本。
    """
    settings = {}

    for attr_name in default_controller_settings:
        settings[attr_name] = default_controller_settings.get(
            attr_name
        )

    return settings


def load_controller_settings(face_guide):
    u"""
    从 Face Config 读取 Step 02 Controller Settings。

    Config 中缺失的旧场景属性自动回退到当前默认值。

    Args:
        face_guide (FaceGuide):
            当前 Face Guide System 实例。

    Returns:
        dict:
        完整 Controller Settings。
    """
    settings = get_default_controller_settings()

    if not face_guide.config_node_exists():
        return settings

    attr_names = []

    for attr_name in default_controller_settings:
        attr_names.append(
            attr_name
        )

    saved_values = face_guide.config_data.get_values(
        attr_names
    )

    for attr_name in attr_names:
        saved_value = saved_values.get(
            attr_name
        )

        if saved_value is None:
            continue

        settings[attr_name] = saved_value

    return settings


def save_controller_settings(
        face_guide,
        settings
):
    u"""
    把 Step 02 Controller Settings 保存到统一 Face Config。

    Args:
        face_guide (FaceGuide):
            当前 Face Guide System 实例。
        settings (dict):
            需要保存的完整 Controller Settings。

    Returns:
        dict:
        ConfigNode 批量写入结果。
    """
    # 保存前先检查配置完整性，避免半套参数进入后续 Component。
    validate_controller_settings(
        settings
    )

    values = {}

    for attr_name in default_controller_settings:
        values[attr_name] = settings.get(
            attr_name
        )

    # 使用 FaceBase 的语义化 Config API 保存普通参数。
    return face_guide.set_config_values(
        attrs_dict=values,
        attr_types=controller_setting_attr_types,
        lock=False,
        hide=True
    )


__all__ = [
    "default_controller_settings",
    "controller_setting_attr_types",
    "controller_size_attr_names",
    "controller_color_attr_names",
    "validate_controller_settings",
    "get_default_controller_settings",
    "load_controller_settings",
    "save_controller_settings",
]
