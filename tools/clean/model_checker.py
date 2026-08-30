# coding=utf-8
u"""
Model Checker
=============

模型检查 UI。

实际检查与安全修复逻辑统一维护在：
    muziToolset.core.model_check_utils

窗口生命周期：
    用户直接调用 main() 时，由 ui.window_utils 负责保存强引用并显示窗口；
    从主工具箱打开时，仍可继续交给 app.window_manager 做应用级窗口管理。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QAbstractItemView
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QTableWidget
    from PySide2.QtWidgets import QTableWidgetItem
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QAbstractItemView
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QTableWidget
    from PySide6.QtWidgets import QTableWidgetItem
    from PySide6.QtWidgets import QVBoxLayout

from ...core import model_check_utils
from ...ui import theme
from ...ui import window_utils


class ModelChecker(QDialog):
    """模型检查器窗口。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(ModelChecker, self).__init__(parent)

        self.issues = []

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Model Checker",
            minimum_width=760
        )
        self.resize(820, 650)

    # -------------------------------------------------------------------------
    # UI
    # -------------------------------------------------------------------------

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        self.title_label = theme.make_title(u"模型检查")
        self.subtitle_label = theme.make_subtitle(
            u"检查拓扑、命名、建模历史、Transform 和锁定法线。"
            u"拓扑问题只报告，不自动猜修。"
        )

        self.nonmanifold_checkbox = QCheckBox(u"非流形")
        self.nonmanifold_checkbox.setChecked(True)

        self.lamina_checkbox = QCheckBox(u"Lamina Face")
        self.lamina_checkbox.setChecked(True)

        self.duplicate_checkbox = QCheckBox(u"DAG 重名")
        self.duplicate_checkbox.setChecked(True)

        self.history_checkbox = QCheckBox(u"遗留建模历史")
        self.history_checkbox.setChecked(True)

        self.transform_checkbox = QCheckBox(u"Mesh Transform 未冻结")
        self.transform_checkbox.setChecked(True)

        self.normals_checkbox = QCheckBox(u"锁定法线")
        self.normals_checkbox.setChecked(True)

        self.selected_only_checkbox = QCheckBox(u"仅检查当前选择")
        self.selected_only_checkbox.setChecked(False)

        self.check_button = QPushButton(u"开始检查")
        theme.style_primary(self.check_button)

        self.select_issue_button = QPushButton(u"选择问题对象")
        self.select_issue_button.setEnabled(False)

        self.fix_selected_button = QPushButton(u"修复表格选中项")
        self.fix_selected_button.setEnabled(False)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels([
            u"对象",
            u"问题类型",
            u"详情",
            u"自动修复",
        ])
        self.result_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.result_table.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )
        self.result_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.result_table.setAlternatingRowColors(True)
        self.result_table.horizontalHeader().setStretchLastSection(True)

        self.status_label = QLabel(u"准备就绪")
        theme.set_role(self.status_label, "muted")

    def create_layouts(self):
        u"""
        创建 Card 布局。
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        option_card, option_layout = theme.make_card(self)
        option_layout.addWidget(
            theme.make_section_title(u"检查项目")
        )

        option_grid = QGridLayout()
        option_grid.setHorizontalSpacing(16)
        option_grid.setVerticalSpacing(8)
        option_grid.addWidget(self.nonmanifold_checkbox, 0, 0)
        option_grid.addWidget(self.lamina_checkbox, 0, 1)
        option_grid.addWidget(self.duplicate_checkbox, 1, 0)
        option_grid.addWidget(self.history_checkbox, 1, 1)
        option_grid.addWidget(self.transform_checkbox, 2, 0)
        option_grid.addWidget(self.normals_checkbox, 2, 1)
        option_layout.addLayout(option_grid)

        scope_row = QHBoxLayout()
        scope_row.setContentsMargins(0, 0, 0, 0)
        scope_row.addWidget(self.selected_only_checkbox)
        scope_row.addStretch(1)
        scope_row.addWidget(self.check_button)
        option_layout.addLayout(scope_row)

        result_card, result_layout = theme.make_card(self)

        result_header = QHBoxLayout()
        result_header.setContentsMargins(0, 0, 0, 0)
        result_header.addWidget(
            theme.make_section_title(u"检查结果")
        )
        result_header.addStretch(1)
        result_header.addWidget(self.select_issue_button)
        result_header.addWidget(self.fix_selected_button)
        result_layout.addLayout(result_header)
        result_layout.addWidget(self.result_table, 1)

        main_layout.addWidget(option_card)
        main_layout.addWidget(result_card, 1)
        main_layout.addWidget(self.status_label)

    def create_connections(self):
        u"""
        连接 UI 信号。
        """
        self.check_button.clicked.connect(
            self.run_check
        )
        self.select_issue_button.clicked.connect(
            self.select_issue_nodes
        )
        self.fix_selected_button.clicked.connect(
            self.fix_selected_issues
        )
        self.result_table.itemSelectionChanged.connect(
            self.update_action_state
        )

    # -------------------------------------------------------------------------
    # Data
    # -------------------------------------------------------------------------

    def get_scope_nodes(self):
        u"""
        返回当前检查范围。

        Returns:
            object | None:
                方法执行后的结果数据。
        """
        if not self.selected_only_checkbox.isChecked():
            return None

        nodes = cmds.ls(
            selection=True,
            long=True
        )

        if nodes is None:
            nodes = []

        return nodes

    def get_selected_issue_rows(self):
        u"""
        返回表格当前选中的唯一行号。

        Returns:
            object:
                方法执行后的结果数据。
        """
        selected_items = self.result_table.selectedItems()
        rows = []

        for item in selected_items:
            row = item.row()

            if row not in rows:
                rows.append(row)

        rows.sort()
        return rows

    def get_selected_issues(self):
        u"""
        返回表格当前选中的 Issue。

        Returns:
            object:
                方法执行后的结果数据。
        """
        issues = []
        rows = self.get_selected_issue_rows()

        for row in rows:
            if row < 0:
                continue

            if row >= len(self.issues):
                continue

            issues.append(self.issues[row])

        return issues

    # -------------------------------------------------------------------------
    # Check
    # -------------------------------------------------------------------------

    def run_check(self):
        u"""
        执行当前勾选的检查项。
        """
        nodes = self.get_scope_nodes()

        if self.selected_only_checkbox.isChecked():
            if not nodes:
                cmds.warning(u"请先选择需要检查的模型或层级。")
                return

        self.status_label.setText(u"正在检查...")

        try:
            self.issues = model_check_utils.run_checks(
                nodes=nodes,
                check_nonmanifold=self.nonmanifold_checkbox.isChecked(),
                check_lamina=self.lamina_checkbox.isChecked(),
                check_duplicates=self.duplicate_checkbox.isChecked(),
                check_history=self.history_checkbox.isChecked(),
                check_transform=self.transform_checkbox.isChecked(),
                check_normals=self.normals_checkbox.isChecked()
            )
        except Exception as error:
            cmds.warning(str(error))
            self.status_label.setText(u"检查失败")
            return

        self.populate_table()

        if self.issues:
            self.status_label.setText(
                u"发现 {} 个问题".format(len(self.issues))
            )
        else:
            self.status_label.setText(u"检查通过，没有发现问题")

    def populate_table(self):
        u"""
        把 Issue 写入结果表格。
        """
        self.result_table.setRowCount(0)
        self.result_table.setRowCount(len(self.issues))

        row = 0

        for issue in self.issues:
            node_item = QTableWidgetItem(
                issue.get("node", "")
            )
            type_item = QTableWidgetItem(
                issue.get("type", "")
            )
            details_item = QTableWidgetItem(
                issue.get("details", "")
            )

            fix_text = u"是"

            if not issue.get("fixable"):
                fix_text = u"否"

            fix_item = QTableWidgetItem(fix_text)
            fix_item.setTextAlignment(Qt.AlignCenter)

            self.result_table.setItem(row, 0, node_item)
            self.result_table.setItem(row, 1, type_item)
            self.result_table.setItem(row, 2, details_item)
            self.result_table.setItem(row, 3, fix_item)
            row += 1

        self.result_table.resizeColumnsToContents()
        self.update_action_state()

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------

    def update_action_state(self):
        u"""
        根据结果和当前选择刷新按钮状态。
        """
        has_issues = bool(self.issues)
        selected_issues = self.get_selected_issues()
        has_selected = bool(selected_issues)
        has_fixable = False

        for issue in selected_issues:
            if issue.get("fixable"):
                has_fixable = True
                break

        self.select_issue_button.setEnabled(has_issues)
        self.fix_selected_button.setEnabled(
            has_selected and has_fixable
        )

    def select_issue_nodes(self):
        u"""
        选择问题对象；有表格选择时只选择选中项。
        """
        issues = self.get_selected_issues()

        if not issues:
            issues = self.issues

        nodes = []

        for issue in issues:
            node = issue.get("node")

            if not node:
                continue

            if not cmds.objExists(node):
                continue

            if node not in nodes:
                nodes.append(node)

        if not nodes:
            cmds.warning(u"没有可选择的问题对象。")
            return

        cmds.select(
            nodes,
            replace=True
        )

    def fix_selected_issues(self):
        u"""
        修复表格中选中的可安全自动修复项。
        """
        selected_issues = self.get_selected_issues()

        if not selected_issues:
            cmds.warning(u"请先选择需要修复的表格行。")
            return

        fixable_issues = []

        for issue in selected_issues:
            if issue.get("fixable"):
                fixable_issues.append(issue)

        if not fixable_issues:
            cmds.warning(u"选中项没有允许自动修复的问题。")
            return

        fixed_count = model_check_utils.fix_issues(
            fixable_issues
        )

        self.status_label.setText(
            u"已修复 {} 项，正在重新检查...".format(fixed_count)
        )
        self.run_check()


def main():
    u"""
    显示并返回 Model Checker。

    Returns:
        object:
            方法执行后的结果数据。
    """
    return window_utils.show_window(
        "tools.clean.model_checker",
        ModelChecker
    )


__all__ = [
    "ModelChecker",
    "main",
]
