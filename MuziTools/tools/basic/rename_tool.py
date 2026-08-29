# coding=utf-8
u"""
批量重命名工具
==============

功能：
    1. 添加前缀
    2. 添加后缀
    3. 查找并替换名称
    4. 按选择 / 层级 / 全场景范围处理
    5. 自动数字编号
    6. 自动字母编号
    7. 使用 * 作为编号占位符进行模式重命名

说明：
    - Maya 2023 / maya.cmds。
    - 这个工具使用 Maya 原生 cmds.window，不依赖 PySide。
    - 所有批量重命名都放入一个 Undo Chunk，方便一次 Ctrl+Z 撤销。
"""

from __future__ import print_function

import re

import maya.cmds as cmds


window_name = "MuziRenameToolWindow"

prefix_field = "MuziRenamePrefixField"
suffix_field = "MuziRenameSuffixField"
search_field = "MuziRenameSearchField"
replace_field = "MuziRenameReplaceField"
scope_radio = "MuziRenameScopeRadio"
start_number_field = "MuziRenameStartNumberField"
padding_field = "MuziRenamePaddingField"
number_type_menu = "MuziRenameNumberTypeMenu"
base_name_field = "MuziRenameBaseNameField"
pattern_field = "MuziRenamePatternField"


# -----------------------------------------------------------------------------
# 通用函数
# -----------------------------------------------------------------------------


def get_short_name(node):
    """从完整 DAG 路径中取得最后一级名称。"""

    if "|" in node:
        return node.rsplit("|", 1)[-1]

    return node


def get_selected_objects():
    """获取当前选择物体。"""

    selected_objects = cmds.ls(
        selection=True,
        long=True
    )

    if selected_objects is None:
        selected_objects = []

    if not selected_objects:
        cmds.warning(u"请先选择物体。")

    return selected_objects


def sort_objects_child_first(objects):
    """
    把 DAG 层级更深的物体放在前面。

    批量修改父子层级名称时，如果先重命名父节点，子节点的完整路径会改变，
    后续保存的旧路径就会失效。因此需要先处理最深层的子节点。
    """

    result = []

    for node in objects:
        if node in result:
            continue

        result.append(node)

    # 不使用列表推导式，直接用简单冒泡逻辑按 DAG 深度排序。
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


def get_objects_by_scope():
    """根据界面中的范围设置返回需要重命名的 Transform。"""

    scope_index = cmds.radioButtonGrp(
        scope_radio,
        query=True,
        select=True
    )

    # 选中物体。
    if scope_index == 1:
        return get_selected_objects()

    # 选中层级。
    if scope_index == 2:
        selected_objects = get_selected_objects()

        if not selected_objects:
            return []

        hierarchy_objects = []

        descendants = cmds.listRelatives(
            selected_objects,
            allDescendents=True,
            type="transform",
            fullPath=True
        )

        if descendants is None:
            descendants = []

        for descendant in descendants:
            if descendant not in hierarchy_objects:
                hierarchy_objects.append(descendant)

        for selected_object in selected_objects:
            if selected_object not in hierarchy_objects:
                hierarchy_objects.append(selected_object)

        return sort_objects_child_first(hierarchy_objects)

    # 全部 Transform。
    all_objects = cmds.ls(
        transforms=True,
        long=True
    )

    if all_objects is None:
        all_objects = []

    return sort_objects_child_first(all_objects)


def rename_node(node, new_name):
    """只有名称发生变化时才执行 cmds.rename。"""

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


# -----------------------------------------------------------------------------
# 前缀 / 后缀
# -----------------------------------------------------------------------------


def add_prefix(*args):
    """给当前选择物体添加前缀。"""

    prefix = cmds.textField(
        prefix_field,
        query=True,
        text=True
    )

    if not prefix:
        cmds.warning(u"请输入前缀。")
        return

    selected_objects = get_selected_objects()

    if not selected_objects:
        return

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRenameAddPrefix"
    )

    try:
        for selected_object in selected_objects:
            current_name = get_short_name(selected_object)
            new_name = prefix + current_name
            rename_node(selected_object, new_name)
    finally:
        cmds.undoInfo(closeChunk=True)


def add_suffix(*args):
    """给当前选择物体添加后缀。"""

    suffix = cmds.textField(
        suffix_field,
        query=True,
        text=True
    )

    if not suffix:
        cmds.warning(u"请输入后缀。")
        return

    selected_objects = get_selected_objects()

    if not selected_objects:
        return

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRenameAddSuffix"
    )

    try:
        for selected_object in selected_objects:
            current_name = get_short_name(selected_object)
            new_name = current_name + suffix
            rename_node(selected_object, new_name)
    finally:
        cmds.undoInfo(closeChunk=True)


# -----------------------------------------------------------------------------
# 查找替换
# -----------------------------------------------------------------------------


def search_replace(*args):
    """在指定范围内查找并替换节点名称。"""

    search_text = cmds.textField(
        search_field,
        query=True,
        text=True
    )
    replace_text = cmds.textField(
        replace_field,
        query=True,
        text=True
    )

    if not search_text:
        cmds.warning(u"请输入需要查找的内容。")
        return

    target_objects = get_objects_by_scope()

    if not target_objects:
        cmds.warning(u"没有可操作的对象。")
        return

    cmds.undoInfo(
        openChunk=True,
        chunkName="MuziRenameSearchReplace"
    )

    try:
        for target_object in target_objects:
            if not cmds.objExists(target_object):
                continue

            current_name = get_short_name(target_object)
            new_name = current_name.replace(
                search_text,
                replace_text
            )

            rename_node(
                target_object,
                new_name
            )
    finally:
        cmds.undoInfo(closeChunk=True)


# -----------------------------------------------------------------------------
# 自动编号
# -----------------------------------------------------------------------------


def number_to_alpha(number, uppercase=True):
    """
    把从 0 开始的整数转换成字母编号。

    Examples:
        0  -> A
        25 -> Z
        26 -> AA
    """

    if number < 0:
        raise ValueError(u"字母编号不能小于 0。")

    character_list = []
    character_base = ord("A")

    while True:
        number, remainder = divmod(number, 26)
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
    """根据编号类型生成最终编号字符串。"""

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


def auto_number(*args):
    """按照当前选择顺序批量添加数字或字母编号。"""

    base_name = cmds.textField(
        base_name_field,
        query=True,
        text=True
    )
    start_number = cmds.intField(
        start_number_field,
        query=True,
        value=True
    )
    padding = cmds.intField(
        padding_field,
        query=True,
        value=True
    )
    number_type = cmds.optionMenu(
        number_type_menu,
        query=True,
        value=True
    )

    selected_objects = get_selected_objects()

    if not selected_objects:
        return

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

            current_name = get_short_name(selected_object)
            final_base_name = base_name

            if not final_base_name:
                final_base_name = current_name

            new_name = "{}_{}".format(
                final_base_name,
                number_string
            )

            rename_node(
                selected_object,
                new_name
            )

            index += 1
    finally:
        cmds.undoInfo(closeChunk=True)


# -----------------------------------------------------------------------------
# 模式重命名
# -----------------------------------------------------------------------------


def build_pattern_name(pattern, number):
    """
    根据 * 占位块生成名称。

    Example:
        leg**_jnt*** + 2 -> leg02_jnt002
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


def pattern_rename(*args):
    """按照 * 编号占位规则重命名当前选择。"""

    pattern = cmds.textField(
        pattern_field,
        query=True,
        text=True
    )

    if not pattern:
        cmds.warning(u"请输入重命名模式。")
        return

    selected_objects = get_selected_objects()

    if not selected_objects:
        return

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

            rename_node(
                selected_object,
                new_name
            )

            number += 1
    finally:
        cmds.undoInfo(closeChunk=True)


# -----------------------------------------------------------------------------
# 界面
# -----------------------------------------------------------------------------


def create_interface():
    """创建 Maya 原生重命名工具界面。"""

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    window = cmds.window(
        window_name,
        title=u"重命名工具",
        widthHeight=(460, 580),
        sizeable=True
    )

    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=10,
        columnAttach=("both", 10)
    )

    # ------------------------------------------------------------------
    # 前缀 / 后缀
    # ------------------------------------------------------------------
    cmds.frameLayout(
        label=u"前缀 / 后缀",
        collapsable=True,
        borderStyle="etchedIn",
        marginWidth=10,
        marginHeight=10
    )
    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=6
    )

    cmds.rowLayout(
        numberOfColumns=3,
        adjustableColumn=2
    )
    cmds.text(
        label=u"前缀：",
        width=60,
        align="right"
    )
    cmds.textField(prefix_field)
    cmds.button(
        label=u"执行",
        command=add_prefix,
        width=60
    )
    cmds.setParent("..")

    cmds.rowLayout(
        numberOfColumns=3,
        adjustableColumn=2
    )
    cmds.text(
        label=u"后缀：",
        width=60,
        align="right"
    )
    cmds.textField(suffix_field)
    cmds.button(
        label=u"执行",
        command=add_suffix,
        width=60
    )
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    # ------------------------------------------------------------------
    # 查找替换
    # ------------------------------------------------------------------
    cmds.frameLayout(
        label=u"查找与替换",
        collapsable=True,
        borderStyle="etchedIn",
        marginWidth=10,
        marginHeight=10
    )
    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=6
    )

    cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=2
    )
    cmds.text(
        label=u"查找：",
        width=70,
        align="right"
    )
    cmds.textField(search_field)
    cmds.setParent("..")

    cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=2
    )
    cmds.text(
        label=u"替换为：",
        width=70,
        align="right"
    )
    cmds.textField(replace_field)
    cmds.setParent("..")

    cmds.radioButtonGrp(
        scope_radio,
        label=u"范围：",
        numberOfRadioButtons=3,
        labelArray3=(u"选中物体", u"层级", u"全部"),
        select=1,
        columnWidth4=[70, 90, 70, 70]
    )
    cmds.button(
        label=u"执行",
        command=search_replace,
        height=28
    )
    cmds.setParent("..")
    cmds.setParent("..")

    # ------------------------------------------------------------------
    # 自动编号
    # ------------------------------------------------------------------
    cmds.frameLayout(
        label=u"自动编号",
        collapsable=True,
        borderStyle="etchedIn",
        marginWidth=10,
        marginHeight=10
    )
    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=6
    )

    cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=2
    )
    cmds.text(
        label=u"起始：",
        width=80,
        align="right"
    )
    cmds.intField(
        start_number_field,
        value=1
    )
    cmds.setParent("..")

    cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=2
    )
    cmds.text(
        label=u"补零位数：",
        width=80,
        align="right"
    )
    cmds.intField(
        padding_field,
        value=2,
        minValue=0,
        maxValue=10
    )
    cmds.setParent("..")

    cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=2
    )
    cmds.text(
        label=u"编号类型：",
        width=80,
        align="right"
    )
    cmds.optionMenu(number_type_menu)
    cmds.menuItem(label=u"数字")
    cmds.menuItem(label=u"大写字母")
    cmds.menuItem(label=u"小写字母")
    cmds.setParent("..")

    cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=2
    )
    cmds.text(
        label=u"基础名称：",
        width=80,
        align="right"
    )
    cmds.textField(
        base_name_field,
        placeholderText=u"留空则使用原名称"
    )
    cmds.setParent("..")

    cmds.button(
        label=u"执行",
        command=auto_number,
        height=28
    )
    cmds.setParent("..")
    cmds.setParent("..")

    # ------------------------------------------------------------------
    # 模式重命名
    # ------------------------------------------------------------------
    cmds.frameLayout(
        label=u"模式重命名",
        collapsable=True,
        borderStyle="etchedIn",
        marginWidth=10,
        marginHeight=10
    )
    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=6
    )

    cmds.rowLayout(
        numberOfColumns=3,
        adjustableColumn=2
    )
    cmds.text(
        label=u"模式：",
        width=70,
        align="right"
    )
    cmds.textField(
        pattern_field,
        placeholderText=u"例如 leg**_jnt*** -> leg01_jnt001"
    )
    cmds.button(
        label=u"执行",
        command=pattern_rename,
        width=60
    )
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    cmds.showWindow(window)
    return window


def main():
    """创建并显示 Maya 原生重命名工具。"""
    return create_interface()


if __name__ == "__main__":
    main()
