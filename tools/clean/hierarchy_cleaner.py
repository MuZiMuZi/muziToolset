# coding=utf-8
u"""
Hierarchy Cleaner
=================

场景安全清理 UI。

实际清理逻辑统一维护在：
    muziToolset.core.scene_clean_utils

窗口生命周期：
    用户直接调用 main() 时，由 ui.window_utils 负责保存强引用并显示窗口；
    从主工具箱打开时，仍可继续交给 app.window_manager 做应用级窗口管理。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout

from ...core import scene_clean_utils
from ...ui import theme
from ...ui import window_utils
from ...core import scene_utils


class HierarchyCleaner(QDialog):
    """层级清理器窗口。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(HierarchyCleaner, self).__init__(parent)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self,
            title=u"Hierarchy Cleaner",
            minimum_width=500
        )
        self.resize(530, 520)

    def create_widgets(self):
        u"""
        创建界面控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(u"层级清理")
        self.subtitle_label = theme.make_subtitle(
            u"默认只处理当前选择；高风险操作会主动跳过动画、约束和 Rig Deformer。"
        )

        self.delete_empty_checkbox = QCheckBox(u"删除空组")
        self.delete_empty_checkbox.setChecked(True)

        self.delete_history_checkbox = QCheckBox(
            u"删除安全范围内 Construction History"
        )
        self.delete_history_checkbox.setChecked(False)

        # -------------------------------------------------------------------------
        # Step 02：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.freeze_checkbox = QCheckBox(
            u"冻结安全范围内 Transform"
        )
        self.freeze_checkbox.setChecked(False)

        self.unlock_checkbox = QCheckBox(
            u"解锁并显示标准 Transform 属性"
        )
        self.unlock_checkbox.setChecked(False)

        self.center_pivot_checkbox = QCheckBox(u"几何体 Pivot 居中")
        self.center_pivot_checkbox.setChecked(False)

        # -------------------------------------------------------------------------
        # Step 03：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.delete_unknown_checkbox = QCheckBox(u"删除 Unknown 节点")
        self.delete_unknown_checkbox.setChecked(True)

        self.selected_only_checkbox = QCheckBox(u"仅处理当前选择")
        self.selected_only_checkbox.setChecked(True)

        self.safety_label = QLabel(
            u"全场景模式会扫描所有 Transform。执行前会再次确认，"
            u"但仍建议先保存 Maya 场景。"
        )
        self.safety_label.setWordWrap(True)
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(self.safety_label, "muted")

        self.execute_button = QPushButton(u"执行清理")
        theme.style_primary(self.execute_button)

        self.result_label = QLabel(u"尚未执行")
        self.result_label.setWordWrap(True)
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(self.result_label, "muted")

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

        option_card, option_layout = theme.make_card(self)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        option_layout.addWidget(
            theme.make_section_title(u"清理选项")
        )
        option_layout.addWidget(self.delete_empty_checkbox)
        option_layout.addWidget(self.delete_history_checkbox)
        option_layout.addWidget(self.freeze_checkbox)
        option_layout.addWidget(self.unlock_checkbox)
        option_layout.addWidget(self.center_pivot_checkbox)
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        option_layout.addWidget(self.delete_unknown_checkbox)

        scope_card, scope_layout = theme.make_card(self)
        scope_layout.addWidget(
            theme.make_section_title(u"执行范围")
        )
        scope_layout.addWidget(self.selected_only_checkbox)
        scope_layout.addWidget(self.safety_label)

        result_card, result_layout = theme.make_card(self)
        # -------------------------------------------------------------------------
        # Step 04：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        result_layout.addWidget(
            theme.make_section_title(u"执行结果")
        )
        result_layout.addWidget(self.result_label)

        main_layout.addWidget(option_card)
        main_layout.addWidget(scope_card)
        main_layout.addWidget(self.execute_button)
        main_layout.addWidget(result_card)
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接 UI 信号。
        """
        self.execute_button.clicked.connect(
            self.execute_cleanup
        )

    def confirm_whole_scene(self):
        u"""
        全场景模式二次确认。

        Returns:
            object | bool:
            方法执行后的结果数据。
        """
        if self.selected_only_checkbox.isChecked():
            return True

        result = QMessageBox.warning(
            self,
            u"确认全场景清理",
            u"当前将扫描整个 Maya 场景。\n\n"
            u"安全规则会跳过明显的 Rig / Animation 节点，"
            u"但仍建议先保存场景。是否继续？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        return result == QMessageBox.Yes

    def get_scope_nodes(self):
        u"""
        返回当前清理范围。

        Returns:
            object:
            方法执行后的结果数据。
        """
        if self.selected_only_checkbox.isChecked():
            nodes = cmds.ls(
                selection=True,
                long=True
            )

            if nodes is None:
                nodes = []

            return nodes

        return scene_clean_utils.all_transform_nodes()

    def format_result(self, result):
        u"""
        把 Core 返回字典格式化成 UI 文本。

        Args:
            result (object):
                上一步 Maya / Tool 操作返回的结果数据。

        Returns:
            object:
            方法执行后的结果数据。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        lines = []

        if "empty_groups" in result:
            lines.append(
                u"空组：删除 {}".format(
                    result["empty_groups"]
                )
            )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if "history" in result:
            history_result = result["history"]
            lines.append(
                u"历史：处理 {} / 跳过 {}".format(
                    history_result["processed"],
                    history_result["skipped"]
                )
            )

        if "freeze" in result:
            freeze_result = result["freeze"]
            lines.append(
                u"冻结：处理 {} / 跳过 {}".format(
                    freeze_result["processed"],
                    freeze_result["skipped"]
                )
            )

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if "attributes" in result:
            lines.append(
                u"属性：修改 {} 项".format(
                    result["attributes"]
                )
            )

        if "pivot" in result:
            lines.append(
                u"Pivot：处理 {}".format(
                    result["pivot"]
                )
            )

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if "unknown" in result:
            lines.append(
                u"Unknown：删除 {}".format(
                    result["unknown"]
                )
            )

        if not lines:
            lines.append(u"没有启用任何清理选项。")

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return u"\n".join(lines)

    def execute_cleanup(self):
        u"""
        执行当前配置的场景清理。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self.confirm_whole_scene():
            return

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        nodes = self.get_scope_nodes()
        selected_only = self.selected_only_checkbox.isChecked()

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if selected_only and not nodes:
            self.result_label.setText(u"请先选择需要清理的对象。")
            return

        scene_utils.open_undo_chunk("MuziHierarchyCleaner")

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            result = scene_clean_utils.run_cleanup(
                nodes=nodes,
                selected_only=selected_only,
                delete_empty=self.delete_empty_checkbox.isChecked(),
                delete_history_enabled=self.delete_history_checkbox.isChecked(),
                freeze_enabled=self.freeze_checkbox.isChecked(),
                unlock_enabled=self.unlock_checkbox.isChecked(),
                center_pivot_enabled=self.center_pivot_checkbox.isChecked(),
                delete_unknown_enabled=self.delete_unknown_checkbox.isChecked()
            )
        except Exception as error:
            cmds.warning(str(error))
            self.result_label.setText(
                u"执行失败：{}".format(error)
            )
            return
        finally:
            scene_utils.close_undo_chunk()

        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.result_label.setText(
            self.format_result(result)
        )


def main():
    u"""
    显示并返回 Hierarchy Cleaner。

    Returns:
        object:
        方法执行后的结果数据。
    """
    return window_utils.show_window(
        "tools.clean.hierarchy_cleaner",
        HierarchyCleaner
    )


__all__ = [
    "HierarchyCleaner",
    "main",
]
