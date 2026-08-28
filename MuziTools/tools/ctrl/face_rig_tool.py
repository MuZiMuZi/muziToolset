#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""
Maya 简单 UI 面板
=================

功能：
    1. 获取 Maya 场景中当前选择的物体
    2. 把选择结果显示到输入框中
    3. 在脚本编辑器中打印选择结果
    4. 清空输入框或关闭窗口

兼容：
    Maya 2020～2024：PySide2
    Maya 2025+：PySide6

使用方法：
    1. 把这个文件放到 Maya scripts 目录中
    2. 在 Maya Python 脚本编辑器中运行：

       import simple_ui_panel
       simple_ui_panel.main()
"""


# =============================================================================
# 导入模块
# =============================================================================
try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QGroupBox
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QWidget
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QGroupBox
    from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui


# 保存窗口实例，避免窗口被 Python 垃圾回收后自动关闭
simple_ui_panel_window = None


# =============================================================================
# 获取 Maya 主窗口
# =============================================================================
def get_maya_main_window():
    u"""获取 Maya 主窗口的 QWidget 对象。"""
    maya_main_window_ptr = omui.MQtUtil.mainWindow()

    if maya_main_window_ptr is None:
        return None

    maya_main_window = wrapInstance(
        int(maya_main_window_ptr),
        QWidget
    )
    return maya_main_window


# =============================================================================
# 简单 UI 面板
# =============================================================================
class Simple_UI_Panel(QWidget):
    u"""Maya 简单工具面板。"""

    WINDOW_OBJECT_NAME = "Simple_UI_Panel_Window"

    def __init__(self, parent=None):
        u"""初始化工具窗口。"""
        if parent is None:
            parent = get_maya_main_window()

        super(Simple_UI_Panel, self).__init__(parent)

        self.setObjectName(self.WINDOW_OBJECT_NAME)
        self.setWindowTitle(u"简单工具面板")
        self.setWindowFlags(Qt.Window)
        self.setMinimumWidth(360)
        self.resize(400, 180)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()


    # =========================================================================
    # 创建 UI 部件
    # =========================================================================
    def create_widgets(self):
        u"""创建界面中使用的标签、输入框和按钮。"""
        self.title_label = QLabel(u"-------------- 简单工具面板 --------------")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            u"color: rgb(169, 255, 175); font-weight: bold;"
        )

        self.selection_groupBox = QGroupBox(u"场景选择")

        self.selection_label = QLabel(u"当前物体：")

        self.selection_lineEdit = QLineEdit()
        self.selection_lineEdit.setPlaceholderText(u"请在 Maya 中选择一个或多个物体")
        self.selection_lineEdit.setReadOnly(True)

        self.load_selection_btn = QPushButton(u"获取选择")
        self.print_selection_btn = QPushButton(u"打印选择")
        self.clear_btn = QPushButton(u"清空")
        self.close_btn = QPushButton(u"关闭")


    # =========================================================================
    # 创建布局
    # =========================================================================
    def create_layouts(self):
        u"""创建界面布局并排列所有部件。"""

        self.selection_input_layout = QHBoxLayout()
        self.selection_input_layout.addWidget(self.selection_label)
        self.selection_input_layout.addWidget(self.selection_lineEdit)
        self.selection_input_layout.addWidget(self.load_selection_btn)

        self.selection_button_layout = QHBoxLayout()
        self.selection_button_layout.addWidget(self.print_selection_btn)
        self.selection_button_layout.addWidget(self.clear_btn)

        self.selection_group_layout = QVBoxLayout(self.selection_groupBox)
        self.selection_group_layout.addLayout(self.selection_input_layout)
        self.selection_group_layout.addLayout(self.selection_button_layout)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.close_btn)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.selection_groupBox)
        self.main_layout.addLayout(self.bottom_layout)


    # =========================================================================
    # 创建信号连接
    # =========================================================================
    def create_connections(self):
        u"""把按钮的 clicked 信号连接到对应的方法。"""
        self.load_selection_btn.clicked.connect(
            self.clicked_load_selection_btn
        )
        self.print_selection_btn.clicked.connect(
            self.clicked_print_selection_btn
        )
        self.clear_btn.clicked.connect(
            self.clicked_clear_btn
        )
        self.close_btn.clicked.connect(
            self.clicked_close_btn
        )


    # =========================================================================
    # 获取场景选择
    # =========================================================================
    def get_selected_objects(self):
        u"""返回 Maya 场景中当前选择的物体列表。"""
        selected_objects = cmds.ls(
            selection=True,
            long=True
        )

        if selected_objects is None:
            selected_objects = []

        return selected_objects


    # =========================================================================
    # 获取选择按钮
    # =========================================================================
    def clicked_load_selection_btn(self):
        u"""点击“获取选择”按钮时，把选择结果显示到输入框。"""
        selected_objects = self.get_selected_objects()

        if not selected_objects:
            self.selection_lineEdit.clear()
            cmds.warning(u"【简单工具面板】请先选择物体。")
            return

        object_name_list = []

        for selected_object in selected_objects:
            short_name = selected_object.split("|")[-1]
            object_name_list.append(short_name)

        selection_text = ", ".join(object_name_list)
        self.selection_lineEdit.setText(selection_text)

        cmds.warning(
            u"【简单工具面板】已读取 {} 个物体。".format(
                len(selected_objects)
            )
        )










# =============================================================================
# 显示窗口
# =============================================================================
def main():
    u"""关闭旧窗口并显示一个新的简单工具面板。"""
    global simple_ui_panel_window

    if simple_ui_panel_window is not None:
        try:
            simple_ui_panel_window.close()
            simple_ui_panel_window.deleteLater()
        except RuntimeError:
            pass

    simple_ui_panel_window = Simple_UI_Panel()
    simple_ui_panel_window.show()
    simple_ui_panel_window.raise_()
    simple_ui_panel_window.activateWindow()

    return simple_ui_panel_window


# =============================================================================
# 直接运行脚本时自动打开窗口
# =============================================================================
if __name__ == "__main__":
    main()
