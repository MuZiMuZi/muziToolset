# coding=utf-8
u"""
Rename Utils
============

Maya 节点批量重命名底层模块。

本模块不包含 PySide UI。
"""

from __future__ import print_function

import re

import maya.cmds as cmds


def get_short_name(node):
    """返回 DAG 节点短名称。"""
    if "|" in node:
        return node.rsplit("|", 1)[-1]

    return node


def get_selected_objects(show_warning=True):
    """返回当前 Maya 选择。"""
    selected_objects = cmds.ls(
        selection=True,
        long=True
    )

    if selected_objects is None:
        selected_objects = []

    if not selected_objects and show_warning:
        cmds.warning(u"请先选择物体。")

    return selected_objects


def sort_objects_child_first(objects):
    """按 DAG 深度从深到浅排序。"""
    result = []

    for node in objects:
        if node not in result:
            result.append(node)

    item_count = len(result)
    outer_index = 0

    while outer_index < item_count:
        inner_index = 0

        while inner_index < item_count - 1:
            current_depth = result[inner_index].count("|")
            next_depth = result[inner_index + 1].count("|")

            if current_depth < next_depth:
                temporary_node = result[inner_index]
                result[inner_index] = result[inner_index + 1]
                result[inner_index + 1] = temporary_node

            inner_index += 1

        outer_index += 1

    return result


def get_objects_by_scope(scope_name):
    """根据中文范围名称返回需要处理的 Transform。"""
    if scope_name == u"选中物体":
        return get_selected_objects()

    if scope_name == u"选中层级":
        selected_objects = get_selected_objects()

        if not selected_objects:
            return []

        hierarchy_objects = []

        for selected_object in selected_objects:
            descendants = cmds.listRelatives(
                selected_object,
                allDescendents=True,
                type="transform",
                fullPath=True
            )

            if descendants is None:
                descendants = []

            for descendant in descendants:
                if descendant not in hierarchy_objects:
                    hierarchy_objects.append(descendant)

            if selected_object not in hierarchy_objects:
                hierarchy_objects.append(selected_object)

        return sort_objects_child_first(hierarchy_objects)

    all_objects = cmds.ls(
        transforms=True,
        long=True
    )

    if all_objects is None:
        all_objects = []

    return sort_objects_child_first(all_objects)


def rename_node(node, new_name):
    """只有名称变化时才执行 Maya rename。"""
    if not cmds.objExists(node):
        return None

    current_name = get_short_name(node)

    if current_name == new_name:
        return node

    try:
        return cmds.rename(
            node,
            new_name
        )
    except RuntimeError as error:
        cmds.warning(str(error))
        return None


def add_prefix(prefix):
    """给当前选择添加前缀。"""
    if not prefix:
        cmds.warning(u"请输入前缀。")
        return 0

    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRenameAddPrefix"
    )

    try:
        for selected_object in selected_objects:
            current_name = get_short_name(selected_object)
            result = rename_node(
                selected_object,
                prefix + current_name
            )

            if result is not None:
                renamed_count += 1
    finally:
        cmds.undoInfo(closeChunk=True)

    return renamed_count


def add_suffix(suffix):
    """给当前选择添加后缀。"""
    if not suffix:
        cmds.warning(u"请输入后缀。")
        return 0

    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRenameAddSuffix"
    )

    try:
        for selected_object in selected_objects:
            current_name = get_short_name(selected_object)
            result = rename_node(
                selected_object,
                current_name + suffix
            )

            if result is not None:
                renamed_count += 1
    finally:
        cmds.undoInfo(closeChunk=True)

    return renamed_count


def search_replace(search_text, replace_text, scope_name):
    """按指定范围查找替换节点名称。"""
    if not search_text:
        cmds.warning(u"请输入需要查找的内容。")
        return 0

    target_objects = get_objects_by_scope(scope_name)

    if not target_objects:
        cmds.warning(u"没有可操作的对象。")
        return 0

    renamed_count = 0

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRenameSearchReplace"
    )

    try:
        for target_object in target_objects:
            if not cmds.objExists(target_object):
                continue

            current_name = get_short_name(target_object)

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
    finally:
        cmds.undoInfo(closeChunk=True)

    return renamed_count


def number_to_alpha(number, uppercase=True):
    """把从 0 开始的整数转换成 A-Z / AA-ZZ。"""
    if number < 0:
        raise ValueError(u"字母编号不能小于 0。")

    character_list = []
    character_base = ord("A")

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
    result = "".join(character_list)

    if uppercase:
        return result

    return result.lower()


def get_number_string(number, padding, number_type):
    """根据编号类型返回数字或字母字符串。"""
    if number_type == u"数字":
        number_string = str(number)

        if padding > 0:
            number_string = number_string.zfill(padding)

        return number_string

    alpha_number = number - 1

    if alpha_number < 0:
        return None

    uppercase = True

    if number_type == u"小写字母":
        uppercase = False

    alpha_string = number_to_alpha(
        alpha_number,
        uppercase=uppercase
    )

    if padding <= len(alpha_string):
        return alpha_string

    fill_character = "A"

    if not uppercase:
        fill_character = "a"

    return alpha_string.rjust(
        padding,
        fill_character
    )


def auto_number(
        base_name,
        start_number=1,
        padding=3,
        number_type=u"数字"
):
    """按照当前选择顺序自动编号。"""
    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRenameAutoNumber"
    )

    try:
        index = 0

        for selected_object in selected_objects:
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
                index += 1
                continue

            final_base_name = base_name

            if not final_base_name:
                final_base_name = get_short_name(selected_object)

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

            index += 1
    finally:
        cmds.undoInfo(closeChunk=True)

    return renamed_count


def build_pattern_name(pattern, number):
    """根据 * 占位块生成名称。"""
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
        padding = len(star_block)
        number_string = str(number).zfill(padding)
        new_name += number_string
        new_name += pattern_parts[block_index + 1]
        block_index += 1

    return new_name


def pattern_rename(pattern):
    """按照 * 编号占位规则重命名当前选择。"""
    if not pattern:
        cmds.warning(u"请输入重命名模式。")
        return 0

    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRenamePattern"
    )

    try:
        number = 1

        for selected_object in selected_objects:
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

            number += 1
    finally:
        cmds.undoInfo(closeChunk=True)

    return renamed_count


__all__ = [
    "get_short_name",
    "get_selected_objects",
    "get_objects_by_scope",
    "add_prefix",
    "add_suffix",
    "search_replace",
    "auto_number",
    "pattern_rename",
    "build_pattern_name",
]
