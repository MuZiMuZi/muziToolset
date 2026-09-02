# coding=utf-8
u"""
Rename Utils
============

Maya 节点命名 / 批量重命名底层模块。

职责：
    1. DAG Short Name 与外部 Maya Name Token 整理；
    2. Selection / Hierarchy Rename 范围整理；
    3. Prefix / Suffix / Search Replace；
    4. Auto Number / Pattern Rename；
    5. 单节点安全 Rename。

边界：
    - Rig 五段式名称语义由 systems.rig_base.RigBase 负责；
    - 节点是否存在、Long DAG Path 是否唯一由 scene_utils.py 负责；
    - DAG Parent / Child / Descendant 查询由 hierarchy_utils.py 负责；
    - 本模块不包含 PySide UI。
"""

from __future__ import print_function

import re

import maya.cmds as cmds

from . import hierarchy_utils
from . import scene_utils


# =============================================================================
# Query / Sanitize
# =============================================================================

def get_short_name(node):
    u"""返回 Maya DAG Short Name；None / 空值统一返回空字符串。"""
    if node is None:
        return ""

    node = str(node).strip()

    if not node:
        return ""

    if "|" in node:
        return node.rsplit(
            "|",
            1
        )[-1]

    return node


def get_sanitized_short_name(
        node,
        namespace_separator="_"
):
    u"""返回去掉 DAG Path，并安全替换 Namespace 的 Short Name。"""
    short_name = get_short_name(
        node
    )

    return short_name.replace(
        ":",
        namespace_separator
    )


def get_name_token(
        node,
        fallback="new"
):
    u"""
    把任意外部 Maya 名称整理成适合作为新名称组成部分的 Token。

    这个 API 面向用户选择、外部场景节点等不受 Rig Naming 完全控制的数据。
    内部 Rig Naming 不应该先调用本方法做重复 Normalize。
    """
    token = get_sanitized_short_name(
        node,
        namespace_separator="_"
    )
    token = token.strip().lower()
    token = token.replace(
        " ",
        "_"
    )
    token = token.replace(
        "-",
        "_"
    )

    while "__" in token:
        token = token.replace(
            "__",
            "_"
        )

    token = token.strip(
        "_"
    )

    if token:
        return token

    return fallback


# =============================================================================
# Selection / Sort
# =============================================================================

def get_selected_objects(show_warning=True):
    u"""返回当前 Maya Selection 的 Long DAG Path。"""
    selected_objects = cmds.ls(
        selection=True,
        long=True
    )

    if selected_objects is None:
        selected_objects = []

    if not selected_objects and show_warning:
        cmds.warning(
            u"请先选择物体。"
        )

    return selected_objects


def sort_objects_child_first(objects):
    u"""对 DAG 节点去重，并按层级深度从深到浅排序。"""
    result = []

    for node in objects:
        if node in result:
            continue

        result.append(
            node
        )

    result.sort(
        key=hierarchy_utils.get_dag_depth,
        reverse=True
    )

    return result


def get_objects_by_scope(scope_name):
    u"""根据 Rename Tool 的范围名称返回目标 Transform。"""
    if scope_name == u"选中物体":
        return get_selected_objects()

    if scope_name == u"选中层级":
        selected_objects = get_selected_objects()

        if not selected_objects:
            return []

        hierarchy_objects = []

        for selected_object in selected_objects:
            descendants = hierarchy_utils.get_descendants(
                selected_object,
                node_type="transform",
                full_path=True
            )

            for descendant in descendants:
                if descendant in hierarchy_objects:
                    continue

                hierarchy_objects.append(
                    descendant
                )

            if selected_object not in hierarchy_objects:
                hierarchy_objects.append(
                    selected_object
                )

        return sort_objects_child_first(
            hierarchy_objects
        )

    all_objects = cmds.ls(
        transforms=True,
        long=True
    )

    if all_objects is None:
        all_objects = []

    return sort_objects_child_first(
        all_objects
    )


# =============================================================================
# Single Rename
# =============================================================================

def rename_node(node, new_name):
    u"""安全重命名单个 Maya 节点；名称没有变化时不调用 cmds.rename。"""
    if not node:
        return None

    if not cmds.objExists(node):
        return None

    if not new_name:
        return None

    current_name = get_short_name(
        node
    )

    if current_name == new_name:
        return node

    try:
        return cmds.rename(
            node,
            new_name
        )
    except RuntimeError as error:
        cmds.warning(
            str(error)
        )
        return None


# =============================================================================
# Prefix / Suffix
# =============================================================================

@scene_utils.undo_chunk
def add_prefix(prefix):
    u"""给当前 Selection 批量添加 Prefix。"""
    if not prefix:
        cmds.warning(
            u"请输入前缀。"
        )
        return 0

    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    for selected_object in selected_objects:
        current_name = get_short_name(
            selected_object
        )

        result = rename_node(
            selected_object,
            prefix + current_name
        )

        if result is not None:
            renamed_count += 1

    return renamed_count


@scene_utils.undo_chunk
def add_suffix(suffix):
    u"""给当前 Selection 批量添加 Suffix。"""
    if not suffix:
        cmds.warning(
            u"请输入后缀。"
        )
        return 0

    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    for selected_object in selected_objects:
        current_name = get_short_name(
            selected_object
        )

        result = rename_node(
            selected_object,
            current_name + suffix
        )

        if result is not None:
            renamed_count += 1

    return renamed_count


# =============================================================================
# Search / Replace
# =============================================================================

@scene_utils.undo_chunk
def search_replace(
        search_text,
        replace_text,
        scope_name
):
    u"""按指定范围执行普通字符串 Search / Replace。"""
    if not search_text:
        cmds.warning(
            u"请输入需要查找的内容。"
        )
        return 0

    target_objects = get_objects_by_scope(
        scope_name
    )

    if not target_objects:
        cmds.warning(
            u"没有可操作的对象。"
        )
        return 0

    renamed_count = 0

    for target_object in target_objects:
        if not cmds.objExists(target_object):
            continue

        current_name = get_short_name(
            target_object
        )

        if search_text not in current_name:
            continue

        new_name = current_name.replace(
            search_text,
            replace_text
        )

        result = rename_node(
            target_object,
            new_name
        )

        if result is not None:
            renamed_count += 1

    return renamed_count


# =============================================================================
# Number Helper
# =============================================================================

def number_to_alpha(number, uppercase=True):
    u"""把从 0 开始的整数转换成字母编号。"""
    if number < 0:
        raise ValueError(
            u"字母编号不能小于 0。"
        )

    character_list = []
    character_base = ord(
        "A"
    )

    while True:
        number, remainder = divmod(
            number,
            26
        )

        character_list.append(
            chr(character_base + remainder)
        )

        if number == 0:
            break

        number -= 1

    character_list.reverse()

    result = "".join(
        character_list
    )

    if uppercase:
        return result

    return result.lower()


def get_number_string(
        number,
        padding,
        number_type
):
    u"""根据编号类型返回数字 / 大写字母 / 小写字母字符串。"""
    if number_type == u"数字":
        number_string = str(
            number
        )

        if padding > 0:
            number_string = number_string.zfill(
                padding
            )

        return number_string

    alpha_number = number - 1

    if alpha_number < 0:
        return None

    uppercase = number_type != u"小写字母"

    alpha_string = number_to_alpha(
        alpha_number,
        uppercase=uppercase
    )

    if padding <= len(alpha_string):
        return alpha_string

    if uppercase:
        fill_character = "A"
    else:
        fill_character = "a"

    return alpha_string.rjust(
        padding,
        fill_character
    )


# =============================================================================
# Auto Number
# =============================================================================

@scene_utils.undo_chunk
def auto_number(
        base_name,
        start_number=1,
        padding=3,
        number_type=u"数字"
):
    u"""按照当前 Selection 顺序自动编号。"""
    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    for index in range(len(selected_objects)):
        selected_object = selected_objects[index]
        number = start_number + index

        number_string = get_number_string(
            number,
            padding,
            number_type
        )

        if number_string is None:
            cmds.warning(
                u"字母编号的起始数字必须大于等于 1。"
            )
            continue

        final_base_name = base_name

        if not final_base_name:
            final_base_name = get_short_name(
                selected_object
            )

        new_name = "{}_{}".format(
            final_base_name,
            number_string
        )

        result = rename_node(
            selected_object,
            new_name
        )

        if result is not None:
            renamed_count += 1

    return renamed_count


# =============================================================================
# Pattern Rename
# =============================================================================

def build_pattern_name(pattern, number):
    u"""根据 ``*`` 数字占位块生成名称。"""
    star_blocks = re.findall(
        r"\*+",
        pattern
    )

    if not star_blocks:
        return "{}{}".format(
            pattern,
            number
        )

    pattern_parts = re.split(
        r"\*+",
        pattern
    )

    new_name = pattern_parts[0]
    block_index = 0

    for star_block in star_blocks:
        padding = len(
            star_block
        )

        number_string = str(
            number
        ).zfill(
            padding
        )

        new_name += number_string
        new_name += pattern_parts[
            block_index + 1
        ]

        block_index += 1

    return new_name


@scene_utils.undo_chunk
def pattern_rename(pattern):
    u"""按照 ``*`` 数字占位规则重命名当前 Selection。"""
    if not pattern:
        cmds.warning(
            u"请输入重命名模式。"
        )
        return 0

    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    for index in range(len(selected_objects)):
        selected_object = selected_objects[index]
        number = index + 1

        new_name = build_pattern_name(
            pattern,
            number
        )

        result = rename_node(
            selected_object,
            new_name
        )

        if result is not None:
            renamed_count += 1

    return renamed_count


__all__ = [
    "get_short_name",
    "get_sanitized_short_name",
    "get_name_token",
    "get_selected_objects",
    "sort_objects_child_first",
    "get_objects_by_scope",
    "rename_node",
    "add_prefix",
    "add_suffix",
    "search_replace",
    "number_to_alpha",
    "get_number_string",
    "auto_number",
    "build_pattern_name",
    "pattern_rename",
]
