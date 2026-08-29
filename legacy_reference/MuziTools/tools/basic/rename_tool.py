# coding=utf-8
u"""
批量重命名工具
==============

功能：
    1. 添加前缀 / 后缀；
    2. 查找并替换名称；
    3. 按选择 / 层级 / 全场景范围处理；
    4. 数字 / 大写字母 / 小写字母自动编号；
    5. 使用 * 作为编号占位符进行模式重命名。

场景操作统一使用 maya.cmds，UI 使用 Maya 2023 的 PySide2。
"""

from __future__ import print_function

import re

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QComboBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QScrollArea
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QComboBox
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QScrollArea
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ... import ui_theme


# -----------------------------------------------------------------------------
# Maya 节点工具
# -----------------------------------------------------------------------------


def get_short_name(node):
    """从完整 DAG 路径中取得最后一级名称。"""
    if "|" in node:
        return node.rsplit("|", 1)[-1]

    return node


def get_selected_objects(show_warning=True):
    """获取当前选择物体。"""
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
    """
    按 DAG 深度从深到浅排序。

    重命名层级时先处理子节点，避免父节点改名后子节点旧完整路径失效。
    """
    result = []

    for node in objects:
        if node in result:
            continue

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
    """根据范围名称返回需要处理的 Transform。"""
    if scope_name == u"选中物体":
        return get_selected_objects()

    if scope_name == u"选中层级":
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
# 重命名逻辑
# -----------------------------------------------------------------------------


def add_prefix_to_selection(prefix):
    """给当前选择物体添加前缀。"""
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
            new_name = prefix + current_name
            result = rename_node(
                selected_object,
                new_name
            )

            if result is not None:
                renamed_count += 1
    finally:
        cmds.undoInfo(closeChunk=True)

    return renamed_count


def add_suffix_to_selection(suffix):
    """给当前选择物体添加后缀。"""
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
            new_name = current_name + suffix
            result = rename_node(
                selected_object,
                new_name
            )

            if result is not None:
                renamed_count += 1
    finally:
        cmds.undoInfo(closeChunk=True)

    return renamed_count


def search_replace_names(search_text, replace_text, scope_name):
    """在指定范围内查找并替换名称。"""
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
    """把从 0 开始的整数转换成 A-Z / AA-ZZ 字母编号。"""
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


def auto_number_selection(
        base_name,
        start_number,
        padding,
        number_type
):
    """按照当前选择顺序批量数字 / 字母编号。"""
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

            current_name = get_short_name(selected_object)
            final_base_name = base_name

            if not final_base_name:
                final_base_name = current_name

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


def pattern_rename_selection(pattern):
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


# -----------------------------------------------------------------------------
# PySide UI
# -----------------------------------------------------------------------------


class RenameTool(QWidget):
    """Silicon 风格批量重命名窗口。"""

    def __init__(self, parent=None):
        super(RenameTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        ui_theme.style_window(
            self,
            title=u"重命名工具",
            minimum_width=560
        )
        self.resize(580, 680)

    def create_widgets(self):
        """创建界面控件。"""
        self.title_label = ui_theme.make_title(u"重命名工具")
        self.subtitle_label = ui_theme.make_subtitle(
            u"批量处理前后缀、查找替换、编号和命名模式。所有操作均可一次撤销。"
        )

        # 前后缀。
        self.prefix_line = QLineEdit()
        self.prefix_line.setPlaceholderText(u"例如 ctrl_")
        self.prefix_button = QPushButton(u"添加前缀")

        self.suffix_line = QLineEdit()
        self.suffix_line.setPlaceholderText(u"例如 _geo")
        self.suffix_button = QPushButton(u"添加后缀")

        # 查找替换。
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText(u"查找")
        self.replace_line = QLineEdit()
        self.replace_line.setPlaceholderText(u"替换为，可留空")

        self.scope_combo = QComboBox()
        self.scope_combo.addItem(u"选中物体")
        self.scope_combo.addItem(u"选中层级")
        self.scope_combo.addItem(u"全场景 Transform")

        self.search_replace_button = QPushButton(u"执行查找替换")
        ui_theme.style_primary(self.search_replace_button)

        # 自动编号。
        self.base_name_line = QLineEdit()
        self.base_name_line.setPlaceholderText(
            u"基础名称；留空则沿用每个对象当前名称"
        )

        self.start_number_spin = QSpinBox()
        self.start_number_spin.setMinimum(0)
        self.start_number_spin.setMaximum(999999)
        self.start_number_spin.setValue(1)

        self.padding_spin = QSpinBox()
        self.padding_spin.setMinimum(0)
        self.padding_spin.setMaximum(8)
        self.padding_spin.setValue(2)

        self.number_type_combo = QComboBox()
        self.number_type_combo.addItem(u"数字")
        self.number_type_combo.addItem(u"大写字母")
        self.number_type_combo.addItem(u"小写字母")

        self.auto_number_button = QPushButton(u"按选择顺序编号")

        # Pattern。
        self.pattern_line = QLineEdit()
        self.pattern_line.setPlaceholderText(
            u"例如 ctrl_arm_*** 或 leg**_jnt***"
        )
        self.pattern_button = QPushButton(u"模式重命名")

        self.pattern_info_label = QLabel(
            u"每一段连续的 * 都会使用当前序号，* 的数量就是补零位数。"
        )
        self.pattern_info_label.setWordWrap(True)
        ui_theme.set_role(self.pattern_info_label, "muted")

        self.status_label = QLabel(u"准备就绪")
        ui_theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        """创建 Card + Scroll 布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(10)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 6, 0)
        scroll_layout.setSpacing(10)

        # 前缀 / 后缀。
        affix_card, affix_layout = ui_theme.make_card(scroll_content)
        affix_layout.addWidget(
            ui_theme.make_section_title(u"前缀 / 后缀")
        )

        prefix_layout = QHBoxLayout()
        prefix_layout.setContentsMargins(0, 0, 0, 0)
        prefix_layout.addWidget(self.prefix_line, 1)
        prefix_layout.addWidget(self.prefix_button)
        affix_layout.addLayout(prefix_layout)

        suffix_layout = QHBoxLayout()
        suffix_layout.setContentsMargins(0, 0, 0, 0)
        suffix_layout.addWidget(self.suffix_line, 1)
        suffix_layout.addWidget(self.suffix_button)
        affix_layout.addLayout(suffix_layout)

        # 查找替换。
        replace_card, replace_layout = ui_theme.make_card(scroll_content)
        replace_layout.addWidget(
            ui_theme.make_section_title(u"查找与替换")
        )

        replace_grid = QGridLayout()
        replace_grid.setHorizontalSpacing(8)
        replace_grid.setVerticalSpacing(8)
        replace_grid.addWidget(QLabel(u"查找"), 0, 0)
        replace_grid.addWidget(self.search_line, 0, 1)
        replace_grid.addWidget(QLabel(u"替换为"), 1, 0)
        replace_grid.addWidget(self.replace_line, 1, 1)
        replace_grid.addWidget(QLabel(u"范围"), 2, 0)
        replace_grid.addWidget(self.scope_combo, 2, 1)
        replace_layout.addLayout(replace_grid)
        replace_layout.addWidget(self.search_replace_button)

        # 自动编号。
        number_card, number_layout = ui_theme.make_card(scroll_content)
        number_layout.addWidget(
            ui_theme.make_section_title(u"自动编号")
        )
        number_layout.addWidget(self.base_name_line)

        number_grid = QGridLayout()
        number_grid.setHorizontalSpacing(8)
        number_grid.setVerticalSpacing(8)
        number_grid.addWidget(QLabel(u"起始"), 0, 0)
        number_grid.addWidget(self.start_number_spin, 0, 1)
        number_grid.addWidget(QLabel(u"位数"), 0, 2)
        number_grid.addWidget(self.padding_spin, 0, 3)
        number_grid.addWidget(QLabel(u"类型"), 1, 0)
        number_grid.addWidget(self.number_type_combo, 1, 1, 1, 3)
        number_layout.addLayout(number_grid)
        number_layout.addWidget(self.auto_number_button)

        # Pattern。
        pattern_card, pattern_layout = ui_theme.make_card(scroll_content)
        pattern_layout.addWidget(
            ui_theme.make_section_title(u"模式重命名")
        )
        pattern_layout.addWidget(self.pattern_info_label)
        pattern_layout.addWidget(self.pattern_line)
        pattern_layout.addWidget(self.pattern_button)

        scroll_layout.addWidget(affix_card)
        scroll_layout.addWidget(replace_card)
        scroll_layout.addWidget(number_card)
        scroll_layout.addWidget(pattern_card)
        scroll_layout.addStretch(1)

        self.scroll_area.setWidget(scroll_content)

        main_layout.addWidget(self.scroll_area, 1)
        main_layout.addWidget(self.status_label)

    def create_connections(self):
        """连接界面信号。"""
        self.prefix_button.clicked.connect(self.apply_prefix)
        self.suffix_button.clicked.connect(self.apply_suffix)
        self.search_replace_button.clicked.connect(
            self.apply_search_replace
        )
        self.auto_number_button.clicked.connect(
            self.apply_auto_number
        )
        self.pattern_button.clicked.connect(
            self.apply_pattern
        )

    def set_status_count(self, action_name, count):
        """更新底部状态。"""
        self.status_label.setText(
            u"{}：{} 个对象".format(
                action_name,
                count
            )
        )

    def apply_prefix(self):
        count = add_prefix_to_selection(
            self.prefix_line.text()
        )
        self.set_status_count(u"已添加前缀", count)

    def apply_suffix(self):
        count = add_suffix_to_selection(
            self.suffix_line.text()
        )
        self.set_status_count(u"已添加后缀", count)

    def apply_search_replace(self):
        count = search_replace_names(
            self.search_line.text(),
            self.replace_line.text(),
            self.scope_combo.currentText()
        )
        self.set_status_count(u"已替换", count)

    def apply_auto_number(self):
        count = auto_number_selection(
            self.base_name_line.text(),
            self.start_number_spin.value(),
            self.padding_spin.value(),
            self.number_type_combo.currentText()
        )
        self.set_status_count(u"已编号", count)

    def apply_pattern(self):
        count = pattern_rename_selection(
            self.pattern_line.text()
        )
        self.set_status_count(u"已模式重命名", count)


def main():
    """创建重命名工具。"""
    window = RenameTool()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
