# coding=utf-8
u"""
Rename Tool
===========

批量重命名工具 UI。

模块职责
--------
1. 提供 Prefix / Suffix、Search Replace、Auto Number、Pattern Rename 界面；
2. 收集用户输入和 Maya Selection Scope；
3. 实际 Rename 行为统一调用 ``core.rename_utils``；
4. 提供可在 Maya Script Editor 中直接显示的 ``main()``。

主要公开类型 / 方法
------------------
RenameTool
    批量 Rename 主窗口。

RenameTool.add_prefix()
RenameTool.add_suffix()
RenameTool.search_replace()
RenameTool.auto_number()
RenameTool.pattern_rename()
    把 UI 参数交给 ``rename_utils``。

main()
    创建或恢复窗口，立即显示并返回 QWidget。

直接运行
--------

    from muziToolset.tools.basic import rename_tool

    window = rename_tool.main()

设计边界
--------
本文件不实现 DAG Rename 算法。Child First、Undo、编号和 Pattern 解析统一维护在
``core.rename_utils``。
"""

from __future__ import print_function

try:
    from PySide2.QtWidgets import QComboBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
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
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...core import rename_utils
from ...ui import theme
from ...ui import window_utils


class RenameTool(QWidget):
    """批量重命名工具窗口。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(RenameTool, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Rename Tool",
            minimum_width=560
        )
        self.resize(590, 590)

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(u"批量重命名")
        self.subtitle_label = theme.make_subtitle(
            u"前后缀、查找替换、自动编号和 * 模式命名。"
        )

        self.prefix_line = QLineEdit()
        self.prefix_line.setPlaceholderText(u"例如 ctrl_")
        self.add_prefix_button = QPushButton(u"添加前缀")

        self.suffix_line = QLineEdit()
        self.suffix_line.setPlaceholderText(u"例如 _bind")
        self.add_suffix_button = QPushButton(u"添加后缀")

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText(u"查找")
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.replace_line = QLineEdit()
        self.replace_line.setPlaceholderText(u"替换为")

        self.scope_combo = QComboBox()
        self.scope_combo.addItem(u"选中物体")
        self.scope_combo.addItem(u"选中层级")
        self.scope_combo.addItem(u"全场景")

        self.search_replace_button = QPushButton(u"执行查找替换")
        theme.style_primary(self.search_replace_button)

        self.base_name_line = QLineEdit()
        self.base_name_line.setPlaceholderText(
            u"基础名称；留空时使用对象原名"
        )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.start_number_spin = QSpinBox()
        self.start_number_spin.setRange(0, 999999)
        self.start_number_spin.setValue(1)

        self.padding_spin = QSpinBox()
        self.padding_spin.setRange(0, 8)
        self.padding_spin.setValue(3)

        self.number_type_combo = QComboBox()
        self.number_type_combo.addItem(u"数字")
        self.number_type_combo.addItem(u"大写字母")
        self.number_type_combo.addItem(u"小写字母")

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.auto_number_button = QPushButton(u"自动编号")
        theme.style_primary(self.auto_number_button)

        self.pattern_line = QLineEdit()
        self.pattern_line.setPlaceholderText(
            u"例如 ctrl_lf_arm_***"
        )
        self.pattern_button = QPushButton(u"模式重命名")
        theme.style_primary(self.pattern_button)

        self.pattern_info_label = QLabel(
            u"连续 * 的数量表示数字位数，例如 *** -> 001。"
        )
        theme.set_role(self.pattern_info_label, "muted")

        self.status_label = QLabel(u"准备就绪")
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        u"""
        创建 Card 布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        prefix_card, prefix_layout = theme.make_card(self)
        prefix_layout.addWidget(
            theme.make_section_title(u"前缀 / 后缀")
        )

        prefix_row = QHBoxLayout()
        prefix_row.setContentsMargins(0, 0, 0, 0)
        prefix_row.addWidget(self.prefix_line, 1)
        prefix_row.addWidget(self.add_prefix_button)
        prefix_layout.addLayout(prefix_row)

        suffix_row = QHBoxLayout()
        suffix_row.setContentsMargins(0, 0, 0, 0)
        suffix_row.addWidget(self.suffix_line, 1)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        suffix_row.addWidget(self.add_suffix_button)
        prefix_layout.addLayout(suffix_row)

        replace_card, replace_layout = theme.make_card(self)
        replace_layout.addWidget(
            theme.make_section_title(u"查找替换")
        )

        replace_grid = QGridLayout()
        replace_grid.setHorizontalSpacing(8)
        replace_grid.setVerticalSpacing(8)
        replace_grid.addWidget(QLabel(u"查找"), 0, 0)
        replace_grid.addWidget(self.search_line, 0, 1)
        replace_grid.addWidget(QLabel(u"替换"), 1, 0)
        replace_grid.addWidget(self.replace_line, 1, 1)
        replace_grid.addWidget(QLabel(u"范围"), 2, 0)
        replace_grid.addWidget(self.scope_combo, 2, 1)
        replace_grid.setColumnStretch(1, 1)
        replace_layout.addLayout(replace_grid)
        replace_layout.addWidget(self.search_replace_button)

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        number_card, number_layout = theme.make_card(self)
        number_layout.addWidget(
            theme.make_section_title(u"自动编号")
        )

        number_grid = QGridLayout()
        number_grid.setHorizontalSpacing(8)
        number_grid.setVerticalSpacing(8)
        number_grid.addWidget(QLabel(u"基础名称"), 0, 0)
        number_grid.addWidget(self.base_name_line, 0, 1, 1, 3)
        number_grid.addWidget(QLabel(u"起始"), 1, 0)
        number_grid.addWidget(self.start_number_spin, 1, 1)
        number_grid.addWidget(QLabel(u"位数"), 1, 2)
        number_grid.addWidget(self.padding_spin, 1, 3)
        number_grid.addWidget(QLabel(u"类型"), 2, 0)
        number_grid.addWidget(self.number_type_combo, 2, 1, 1, 3)
        number_grid.setColumnStretch(1, 1)
        number_grid.setColumnStretch(3, 1)
        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        number_layout.addLayout(number_grid)
        number_layout.addWidget(self.auto_number_button)

        pattern_card, pattern_layout = theme.make_card(self)
        pattern_layout.addWidget(
            theme.make_section_title(u"模式命名")
        )
        pattern_layout.addWidget(self.pattern_info_label)

        pattern_row = QHBoxLayout()
        pattern_row.setContentsMargins(0, 0, 0, 0)
        pattern_row.addWidget(self.pattern_line, 1)
        pattern_row.addWidget(self.pattern_button)
        pattern_layout.addLayout(pattern_row)

        main_layout.addWidget(prefix_card)
        main_layout.addWidget(replace_card)
        main_layout.addWidget(number_card)
        main_layout.addWidget(pattern_card)
        main_layout.addWidget(self.status_label)
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接 UI 信号。
        """
        self.add_prefix_button.clicked.connect(
            self.add_prefix
        )
        self.add_suffix_button.clicked.connect(
            self.add_suffix
        )
        self.search_replace_button.clicked.connect(
            self.search_replace
        )
        self.auto_number_button.clicked.connect(
            self.auto_number
        )
        self.pattern_button.clicked.connect(
            self.pattern_rename
        )

    def set_result_status(self, action_name, count):
        u"""
        更新执行结果状态。

        Args:
            action_name (str):
                `action_name` 对应的 Maya 节点或资源名称。
            count (int):
                需要创建、采样或处理的数量。
        """
        self.status_label.setText(
            u"{}：处理 {} 个对象".format(
                action_name,
                count
            )
        )

    def add_prefix(self):
        u"""
        读取 Prefix 输入并执行批量添加。
        """
        count = rename_utils.add_prefix(
            self.prefix_line.text().strip()
        )
        self.set_result_status(u"添加前缀", count)

    def add_suffix(self):
        u"""
        读取 Suffix 输入并执行批量添加。
        """
        count = rename_utils.add_suffix(
            self.suffix_line.text().strip()
        )
        self.set_result_status(u"添加后缀", count)

    def search_replace(self):
        u"""
        按照当前 Scope 执行 Search / Replace。
        """
        count = rename_utils.search_replace(
            search_text=self.search_line.text(),
            replace_text=self.replace_line.text(),
            scope_name=self.scope_combo.currentText()
        )
        self.set_result_status(u"查找替换", count)

    def auto_number(self):
        u"""
        按照 Selection 顺序执行自动编号。
        """
        count = rename_utils.auto_number(
            base_name=self.base_name_line.text().strip(),
            start_number=self.start_number_spin.value(),
            padding=self.padding_spin.value(),
            number_type=self.number_type_combo.currentText()
        )
        self.set_result_status(u"自动编号", count)

    def pattern_rename(self):
        u"""
        按照 * 占位规则执行 Pattern Rename。
        """
        count = rename_utils.pattern_rename(
            self.pattern_line.text().strip()
        )
        self.set_result_status(u"模式命名", count)


def main():
    u"""
    创建或恢复 Rename Tool，立即显示并返回 QWidget。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return window_utils.show_window(
        "tools.basic.rename_tool",
        RenameTool
    )


__all__ = [
    "RenameTool",
    "main",
]
