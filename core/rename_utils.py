# coding=utf-8
u"""
Rename Utils
============

Maya 节点批量重命名底层模块。

正式模块路径
------------
``muziToolset.core.rename_utils`` 是批量 Rename 行为的正式入口。
标准 Rig 名称语义由 ``muziToolset.core.name_utils`` 负责，两者职责独立。

模块职责
--------
本模块负责面向 Tool / Selection 的批量 Rename 行为，包括 Prefix、Suffix、Search Replace、
自动编号与 Pattern Rename。

主要公开 API
------------
get_short_name(node)
    返回 DAG Short Name。

get_selected_objects(show_warning=True)
    获取当前 Maya Selection。

sort_objects_child_first(objects)
    按 DAG 深度从深到浅排序，保证层级 Rename 时 Child 先处理。

get_objects_by_scope(scope_name)
    根据“选中物体 / 选中层级 / 全部对象”整理 Rename 范围。

rename_node(node, new_name)
    安全重命名单个节点。

add_prefix(prefix)
add_suffix(suffix)
    给当前 Selection 批量添加前后缀。

search_replace(search_text, replace_text, scope_name)
    按范围执行普通字符串 Search / Replace。

number_to_alpha(number, uppercase=True)
get_number_string(number, padding, number_type)
    数字 / 字母编号辅助。

auto_number(base_name, start_number=1, padding=3, number_type=u"数字")
    根据 Selection 顺序自动编号。

build_pattern_name(pattern, number)
pattern_rename(pattern)
    使用 ``*`` 作为数字占位符执行 Pattern Rename。

和 name_utils.py 的区别
-----------------------
name_utils.py
    负责正式五段式 Rig 名称的创建、解析、镜像、唯一序号和 Name 对象。

rename_utils.py
    负责面向用户操作的批量 Rename。

两个模块名字相近，但职责不同，因此保持独立，不为了减少文件数量强行合并。

设计原则
--------
1. 层级 Rename 必须 Child First，避免 Parent Rename 后 Long Path 失效；
2. 所有批量 Rename 使用 scene_utils.undo_chunk，用户一次 Undo 即可撤销整次操作；
3. Maya 自动追加数字后缀不是正式命名策略，工具应尽量生成明确名称；
4. Selection 属于本模块的 Tool 兼容入口，真正的单节点 rename_node 接受明确参数；
5. 本模块不包含 PySide UI。
"""

from __future__ import print_function

import re

import maya.cmds as cmds

from . import scene_utils


# =============================================================================
# Query / Sort
# =============================================================================

def get_short_name(node):
    u"""
    返回 DAG 节点 Short Name。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。

    Returns:
        object:
        方法执行后的结果数据。
    """
    if "|" in node:
        return node.rsplit("|", 1)[-1]

    return node


def get_selected_objects(show_warning=True):
    u"""
    返回当前 Maya Selection 的 Long Path。

    Args:
        show_warning (bool):
            是否启用 `show_warning` 对应的处理。

    Returns:
        object:
        方法执行后的结果数据。
    """
    selected_objects = cmds.ls(
        selection=True,
        long=True
    ) or []

    if not selected_objects and show_warning:
        cmds.warning(u"请先选择物体。")

    return selected_objects


def sort_objects_child_first(objects):
    u"""
    对 DAG 节点去重，并按深度从深到浅排序。

    为什么 Child First：
        如果先 Rename Parent，原来的 Child Long Path 会立刻失效；先处理最深节点可以避免这个问题。

    Args:
        objects (str | list[str]):
            需要批量处理的 Maya 场景对象名称或对象列表。

    Returns:
        object:
        方法执行后的结果数据。
    """
    result = []

    for node in objects:
        if node not in result:
            result.append(node)

    def get_depth(node):
        return node.count("|")

    result.sort(
        key=get_depth,
        reverse=True
    )

    return result


def get_objects_by_scope(scope_name):
    u"""
    根据中文范围名称返回需要处理的 Transform。

    支持：
        选中物体
        选中层级
        其它值 -> 场景全部 Transform

    Args:
        scope_name (str):
            `scope_name` 对应的 Maya 节点或资源名称。

    Returns:
        object | list:
        方法执行后的结果数据。
    """
    # -------------------------------------------------------------------------
    # 步骤 1：仅当前 Selection。
    # -------------------------------------------------------------------------
    if scope_name == u"选中物体":
        return get_selected_objects()

    # -------------------------------------------------------------------------
    # 步骤 2：Selection + 全部 Transform 后代。
    # -------------------------------------------------------------------------
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
            ) or []

            for descendant in descendants:
                if descendant not in hierarchy_objects:
                    hierarchy_objects.append(descendant)

            if selected_object not in hierarchy_objects:
                hierarchy_objects.append(selected_object)

        return sort_objects_child_first(hierarchy_objects)

    # -------------------------------------------------------------------------
    # 步骤 3：默认处理场景全部 Transform。
    # -------------------------------------------------------------------------
    all_objects = cmds.ls(
        transforms=True,
        long=True
    ) or []

    return sort_objects_child_first(all_objects)


# =============================================================================
# Single Rename
# =============================================================================

def rename_node(node, new_name):
    u"""
    安全重命名单个 Maya 节点。

    名称没有变化时不调用 cmds.rename；失败时发出 Maya Warning 并返回 None。

    Args:
        node (str):
            需要查询或处理的 Maya 节点名称。
        new_name (str):
            `new_name` 对应的 Maya 节点或资源名称。

    Returns:
        None | object:
        方法执行后的结果数据。
    """
    if not node or not cmds.objExists(node):
        return None

    if not new_name:
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


# =============================================================================
# Prefix / Suffix
# =============================================================================

@scene_utils.undo_chunk
def add_prefix(prefix):
    u"""
    给当前 Selection 批量添加前缀，并返回成功数量。

    Args:
        prefix (object):
            `prefix` 对应的输入数据。

    Returns:
        object | int:
        方法执行后的结果数据。
    """
    if not prefix:
        cmds.warning(u"请输入前缀。")
        return 0

    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    for selected_object in selected_objects:
        current_name = get_short_name(selected_object)
        result = rename_node(
            selected_object,
            prefix + current_name
        )

        if result is not None:
            renamed_count += 1

    return renamed_count


@scene_utils.undo_chunk
def add_suffix(suffix):
    u"""
    给当前 Selection 批量添加后缀，并返回成功数量。

    Args:
        suffix (object):
            `suffix` 对应的输入数据。

    Returns:
        object | int:
        方法执行后的结果数据。
    """
    if not suffix:
        cmds.warning(u"请输入后缀。")
        return 0

    selected_objects = get_selected_objects()

    if not selected_objects:
        return 0

    renamed_count = 0

    for selected_object in selected_objects:
        current_name = get_short_name(selected_object)
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
def search_replace(search_text, replace_text, scope_name):
    u"""
    按指定范围对节点 Short Name 做普通字符串 Search / Replace。

    Args:
        search_text (object):
            `search_text` 对应的输入数据。
        replace_text (object):
            `replace_text` 对应的输入数据。
        scope_name (str):
            `scope_name` 对应的 Maya 节点或资源名称。

    Returns:
        object | int:
        方法执行后的结果数据。
    """
    if not search_text:
        cmds.warning(u"请输入需要查找的内容。")
        return 0

    target_objects = get_objects_by_scope(scope_name)

    if not target_objects:
        cmds.warning(u"没有可操作的对象。")
        return 0

    renamed_count = 0

    # Child First 的列表已经由 get_objects_by_scope 整理完成。
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

    return renamed_count


# =============================================================================
# Number Helper
# =============================================================================

def number_to_alpha(number, uppercase=True):
    u"""
    把从 0 开始的整数转换成 A-Z / AA-ZZ 字母编号。

    Args:
        number (int):
            `number` 对应的整数参数。
        uppercase (bool):
            是否启用 `uppercase` 对应的处理。

    Returns:
        object:
        方法执行后的结果数据。

    Raises:
        ValueError:
        输入数据、场景状态或操作条件不满足要求时抛出。

    Example:
        0 -> A
                                        25 -> Z
                                        26 -> AA
    """
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
    u"""
    根据编号类型返回数字 / 大写字母 / 小写字母字符串。

    Args:
        number (int):
            `number` 对应的整数参数。
        padding (object):
            `padding` 对应的输入数据。
        number_type (object):
            `number_type` 对应的输入数据。

    Returns:
        object | None:
        方法执行后的结果数据。
    """
    if number_type == u"数字":
        number_string = str(number)

        if padding > 0:
            number_string = number_string.zfill(padding)

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

    fill_character = "A" if uppercase else "a"

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
    u"""
    按照当前 Selection 顺序自动编号。

    Args:
        base_name (str):
            `base_name` 对应的 Maya 节点或资源名称。
        start_number (int):
            `start_number` 对应的整数参数。
        padding (int):
            `padding` 对应的整数参数。
        number_type (str):
            `number_type` 对应的名称、标记或字符串参数。

    Returns:
        object | int:
        方法执行后的结果数据。
    """
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
            cmds.warning(u"字母编号的起始数字必须大于等于 1。")
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

    return renamed_count


# =============================================================================
# Pattern Rename
# =============================================================================

def build_pattern_name(pattern, number):
    u"""
    根据 ``*`` 占位块生成名称。

    Args:
        pattern (str):
            用于筛选 Maya 节点名称的匹配模式。
        number (int):
            `number` 对应的整数参数。

    Returns:
        object:
        方法执行后的结果数据。

    Example:
        build_pattern_name("jnt_md_spine_bind_***", 4)
                                        -> jnt_md_spine_bind_004
    """
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


@scene_utils.undo_chunk
def pattern_rename(pattern):
    u"""
    按照 ``*`` 数字占位规则重命名当前 Selection。

    Args:
        pattern (str):
            用于筛选 Maya 节点名称的匹配模式。

    Returns:
        object | int:
        方法执行后的结果数据。
    """
    if not pattern:
        cmds.warning(u"请输入重命名模式。")
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
