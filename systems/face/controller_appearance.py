# coding=utf-8
u"""
Face Controller Appearance
==========================

只负责在 Face Rig 已经构建后更新 Controller Shape 外观。

设计边界：
    1. 只修改 Curve Shape 的尺寸和颜色；
    2. 不修改 Controller Transform、Zero Group 或 Guide 对齐结果；
    3. 尺寸更新使用“新有效尺寸 / 旧有效尺寸”的比例，因此不会重复累积误差；
    4. Controller Settings 仍以 systems.face.config 中的正式 Config Schema 为唯一数据源；
    5. 场景中还没有 Controller 时允许安全返回，供 Step 03 构建前保存参数使用；
    6. Controller 和 Controller Set 的名称解析都忽略 Maya Namespace；
    7. Module Size 使用明确的 Part Alias 映射，兼容 cheekbone / nasolabial 等业务命名。
"""

from __future__ import print_function

import maya.cmds as cmds

from ...core import control_shape_utils
from ...core import rename_utils
from . import config


# =============================================================================
# Controller Part -> Appearance Module
# =============================================================================

# Controller 的 part 不一定和 UI 中的 Module 名完全相同。
# 例如 CheekModule 会创建 cheekbone / nasolabial / cheek 三类 Controller，
# 但 UI 只暴露一个 Cheek Size。因此这里统一把这些 Part 映射回 cheek。
CONTROLLER_MODULE_PART_ALIASES = {
    "brow": [
        "brow",
    ],
    "eye": [
        "eye",
    ],
    "eyelid": [
        "eyelid",
    ],
    "nose": [
        "nose",
    ],
    "cheek": [
        "cheek",
        "cheekbone",
        "nasolabial",
    ],
    "lip": [
        "lip",
    ],
    "jaw": [
        "jaw",
    ],
    "teeth": [
        "teeth",
    ],
    "tongue": [
        "tongue",
    ],
}


def _get_canonical_short_name(node):
    u"""返回去掉 DAG Path 和 Maya Namespace 的标准短名称。"""
    short_name = rename_utils.get_short_name(
        node
    )
    return short_name.rsplit(
        ":",
        1
    )[-1]


def _resolve_face_ctrl_set():
    u"""解析当前场景唯一的 Face Controller Set，兼容 Maya Namespace。"""
    if cmds.objExists(config.face_ctrl_set):
        return config.face_ctrl_set

    object_sets = cmds.ls(
        type="objectSet",
        long=True
    )

    if object_sets is None:
        object_sets = []

    candidates = []

    for object_set in object_sets:
        canonical_name = _get_canonical_short_name(
            object_set
        )

        if canonical_name != config.face_ctrl_set:
            continue

        candidates.append(
            object_set
        )

    if len(candidates) == 1:
        return candidates[0]

    return None


def _get_face_ctrl_nodes():
    u"""返回 Face Controller Set 中全部有效 Controller Transform。"""
    face_ctrl_set = _resolve_face_ctrl_set()

    if face_ctrl_set is None:
        return []

    members = cmds.sets(
        face_ctrl_set,
        query=True
    )

    if members is None:
        members = []

    ctrl_nodes = []

    for member in members:
        if not cmds.objExists(member):
            continue

        transforms = cmds.ls(
            member,
            type="transform",
            long=True
        )

        if transforms is None:
            transforms = []

        for transform in transforms:
            short_name = _get_canonical_short_name(
                transform
            )

            if not short_name.startswith("ctrl_"):
                continue

            if transform in ctrl_nodes:
                continue

            ctrl_nodes.append(
                transform
            )

            descendants = cmds.listRelatives(
                transform,
                allDescendents=True,
                type="transform",
                fullPath=True
            )

            if descendants is None:
                descendants = []

            for descendant in descendants:
                descendant_short_name = _get_canonical_short_name(
                    descendant
                )

                if not descendant_short_name.startswith("ctrl_"):
                    continue

                if descendant in ctrl_nodes:
                    continue

                ctrl_nodes.append(
                    descendant
                )

    return ctrl_nodes


def _get_ctrl_side(ctrl_node):
    u"""从标准 Controller 名称读取 lf / rt / md。"""
    short_name = _get_canonical_short_name(
        ctrl_node
    )
    tokens = short_name.split("_")

    if len(tokens) < 3:
        return None

    side = tokens[1]

    if side not in config.face_controller_color_attr_names:
        return None

    return side


def _get_ctrl_module(ctrl_node):
    u"""根据标准 Face Controller Part 判断所属可调尺寸 Module。"""
    short_name = _get_canonical_short_name(
        ctrl_node
    )
    tokens = short_name.split("_")

    if len(tokens) < 4:
        return None

    # 去掉 ctrl / side 和最后 function + index，剩余部分只保留业务 Part Token。
    # 例如：
    #   ctrl_rt_cheekbone_bind_002 -> ["cheekbone"]
    #   ctrl_md_upper_teeth_bind_001 -> ["upper", "teeth"]
    part_tokens = tokens[2:-2]

    for module_name in config.face_controller_module_order:
        module_aliases = CONTROLLER_MODULE_PART_ALIASES.get(
            module_name
        )

        if module_aliases is None:
            module_aliases = [
                module_name,
            ]

        for module_alias in module_aliases:
            if module_alias in part_tokens:
                return module_name

    return None


def _get_setting(settings, attr_name):
    u"""读取 Controller Setting，并回退到正式默认值。"""
    default_value = config.face_controller_default_settings.get(
        attr_name
    )
    return settings.get(
        attr_name,
        default_value
    )


def _get_effective_size(settings, module_name=None):
    u"""返回 Global Scale * Module Size 的最终尺寸系数。"""
    global_scale = float(
        _get_setting(
            settings,
            config.face_controller_global_scale_attr
        )
    )

    module_scale = 1.0

    if module_name:
        attr_name = config.face_controller_size_attr_names.get(
            module_name
        )

        if attr_name:
            module_scale = float(
                _get_setting(
                    settings,
                    attr_name
                )
            )

    return global_scale * module_scale


def apply_controller_settings(
        previous_settings,
        new_settings
):
    u"""
    把新的 Face Controller Settings 实时应用到现有 Controller Shape。

    Args:
        previous_settings (dict):
            当前场景 Controller Shape 对应的旧 Config Settings。
        new_settings (dict):
            UI 即将保存的新 Config Settings。

    Returns:
        dict:
            changed_ctrl_count、scaled_ctrl_count、colored_ctrl_count。
    """
    ctrl_nodes = _get_face_ctrl_nodes()

    scaled_ctrl_count = 0
    colored_ctrl_count = 0
    changed_ctrl_nodes = []

    for ctrl_node in ctrl_nodes:
        module_name = _get_ctrl_module(
            ctrl_node
        )
        side = _get_ctrl_side(
            ctrl_node
        )

        old_effective_size = _get_effective_size(
            previous_settings,
            module_name=module_name
        )
        new_effective_size = _get_effective_size(
            new_settings,
            module_name=module_name
        )

        if old_effective_size > 0.0:
            scale_ratio = new_effective_size / old_effective_size

            if abs(scale_ratio - 1.0) > 0.000001:
                control_shape_utils.scale_shape(
                    ctrl_node,
                    scale_ratio
                )
                scaled_ctrl_count += 1

                if ctrl_node not in changed_ctrl_nodes:
                    changed_ctrl_nodes.append(
                        ctrl_node
                    )

        if side:
            color_attr_name = config.face_controller_color_attr_names.get(
                side
            )
            old_color = int(
                _get_setting(
                    previous_settings,
                    color_attr_name
                )
            )
            new_color = int(
                _get_setting(
                    new_settings,
                    color_attr_name
                )
            )

            if old_color != new_color:
                control_shape_utils.set_shape_color(
                    ctrl_node,
                    new_color
                )
                colored_ctrl_count += 1

                if ctrl_node not in changed_ctrl_nodes:
                    changed_ctrl_nodes.append(
                        ctrl_node
                    )

    return {
        "changed_ctrl_count": len(changed_ctrl_nodes),
        "scaled_ctrl_count": scaled_ctrl_count,
        "colored_ctrl_count": colored_ctrl_count,
        "ctrl_nodes": changed_ctrl_nodes,
    }


__all__ = [
    "apply_controller_settings",
]
