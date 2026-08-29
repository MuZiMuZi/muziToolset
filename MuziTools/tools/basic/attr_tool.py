# coding=utf-8
u"""
属性工具
========

功能：
    1. 打开 Maya 添加属性窗口
    2. 打开 Maya 编辑属性窗口
    3. 打开 Maya Connection Editor
    4. 打开 Maya Channel Control
    5. 删除 Channel Box 中选中的属性
    6. 调整自定义属性在 Channel Box 中的顺序
    7. 批量设置 Translate / Rotate / Scale / Visibility 的锁定和隐藏状态

说明：
    - Maya 2023 优先使用 PySide2。
    - 场景操作统一使用 maya.cmds，不使用 pymel。
    - main() 只负责创建并返回 QWidget，由 MuziTools.window_manager 统一显示和管理窗口生命周期。
"""

from __future__ import print_function

import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...config import icon_dir
from ....core import attrUtils


class AttrTool(QWidget):
    """属性工具窗口。"""

    def __init__(self, parent=None):
        super(AttrTool, self).__init__(parent)

        self.window_name = "AttrTool"
        self.window_title = u"Attr Tool（属性工具）"

        self.setWindowTitle(self.window_title)
        self.setMinimumWidth(420)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    # -------------------------------------------------------------------------
    # 创建界面部件
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建界面中使用的所有部件。"""

        # ------------------------------------------------------------------
        # 属性编辑
        # ------------------------------------------------------------------
        self.attr_window_label = QLabel(u"---------------- 属性编辑 ----------------")
        self.attr_window_label.setStyleSheet(u"color: rgb(255, 0, 0);")

        self.add_attr_window_button = QPushButton(
            QIcon(icon_dir + "/add.png"),
            "Add Attribute"
        )
        self.add_attr_window_button.setToolTip(u"打开 Maya 添加属性窗口")

        self.edit_attr_window_button = QPushButton(
            QIcon(icon_dir + "/edit.png"),
            "Edit Attribute"
        )
        self.edit_attr_window_button.setToolTip(u"打开 Maya 编辑属性窗口")

        self.connect_attr_window_button = QPushButton(
            QIcon(icon_dir + "/connect-empty.png"),
            "Connect Attr"
        )
        self.connect_attr_window_button.setToolTip(u"打开 Maya Connection Editor")

        self.channel_control_window_button = QPushButton(
            QIcon(icon_dir + "/set.png"),
            "Channel Control"
        )
        self.channel_control_window_button.setToolTip(u"打开 Maya Channel Control")

        self.delete_attr_window_button = QPushButton(
            QIcon(icon_dir + "/delete.png"),
            "Delete Attr"
        )
        self.delete_attr_window_button.setToolTip(u"删除 Channel Box 中选中的属性")

        # ------------------------------------------------------------------
        # 属性排序
        # ------------------------------------------------------------------
        self.attr_tool_label = QLabel(u"---------------- 属性工具 ----------------")
        self.attr_tool_label.setStyleSheet(u"color: rgb(255, 170, 255);")

        self.attr_move_label = QLabel(u"选择 Channel Box 中的一个自定义属性：")

        self.attr_up_button = QPushButton(
            QIcon(icon_dir + "/arrow-upward .png"),
            "Attr Up"
        )
        self.attr_up_button.setToolTip(u"把选中的自定义属性向上移动")

        self.attr_down_button = QPushButton(
            QIcon(icon_dir + "/arrow-downward.png"),
            "Attr Down"
        )
        self.attr_down_button.setToolTip(u"把选中的自定义属性向下移动")

        # ------------------------------------------------------------------
        # 属性状态
        # ------------------------------------------------------------------
        self.attr_set_label = QLabel(u"---------------- 属性设置 ----------------")
        self.attr_set_label.setStyleSheet(u"color: rgb(170, 255, 255);")

        self.translation_set_label = QLabel("Translation:")
        self.translation_locked_checkbox = QCheckBox("Locked")
        self.translation_hidden_checkbox = QCheckBox("Hidden")

        self.rotate_set_label = QLabel("Rotate:")
        self.rotate_locked_checkbox = QCheckBox("Locked")
        self.rotate_hidden_checkbox = QCheckBox("Hidden")

        self.scale_set_label = QLabel("Scale:")
        self.scale_locked_checkbox = QCheckBox("Locked")
        self.scale_hidden_checkbox = QCheckBox("Hidden")

        self.visibility_set_label = QLabel("Visibility:")
        self.visibility_locked_checkbox = QCheckBox("Locked")
        self.visibility_hidden_checkbox = QCheckBox("Hidden")

        self.attr_set_button = QPushButton(
            QIcon(icon_dir + "/set.png"),
            "Set"
        )
        self.attr_set_button.setToolTip(u"根据当前勾选状态设置所选物体的属性")

        self.attr_reset_button = QPushButton(
            QIcon(icon_dir + "/reset.png"),
            "Reset"
        )
        self.attr_reset_button.setToolTip(u"清空当前所有 Locked / Hidden 选项")

        self.attr_checkboxes = [
            self.translation_locked_checkbox,
            self.translation_hidden_checkbox,
            self.rotate_locked_checkbox,
            self.rotate_hidden_checkbox,
            self.scale_locked_checkbox,
            self.scale_hidden_checkbox,
            self.visibility_locked_checkbox,
            self.visibility_hidden_checkbox,
        ]

    # -------------------------------------------------------------------------
    # 创建布局
    # -------------------------------------------------------------------------

    def create_layouts(self):
        """创建并组合窗口布局。"""

        # 属性编辑区域。
        self.attr_window_layout = QGridLayout()
        self.attr_window_layout.addWidget(self.add_attr_window_button, 0, 0)
        self.attr_window_layout.addWidget(self.edit_attr_window_button, 0, 1)
        self.attr_window_layout.addWidget(self.connect_attr_window_button, 0, 2)
        self.attr_window_layout.addWidget(self.channel_control_window_button, 1, 0)
        self.attr_window_layout.addWidget(self.delete_attr_window_button, 1, 1)

        # 属性排序区域。
        self.attr_move_layout = QHBoxLayout()
        self.attr_move_layout.addWidget(self.attr_move_label)
        self.attr_move_layout.addWidget(self.attr_up_button)
        self.attr_move_layout.addWidget(self.attr_down_button)

        self.attr_tool_layout = QVBoxLayout()
        self.attr_tool_layout.addLayout(self.attr_move_layout)

        # 属性状态设置区域。
        self.attr_set_layout = QVBoxLayout()
        self.create_attr_set_layout()

        # 主布局。
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.attr_window_label)
        self.main_layout.addLayout(self.attr_window_layout)
        self.main_layout.addStretch()

        self.main_layout.addWidget(self.attr_tool_label)
        self.main_layout.addLayout(self.attr_tool_layout)
        self.main_layout.addStretch()

        self.main_layout.addWidget(self.attr_set_label)
        self.main_layout.addLayout(self.attr_set_layout)
        self.main_layout.addStretch()

    def create_attr_set_layout(self):
        """创建属性锁定和隐藏设置区域。"""

        self.translation_set_layout = QHBoxLayout()
        self.translation_set_layout.addWidget(self.translation_set_label)
        self.translation_set_layout.addWidget(self.translation_locked_checkbox)
        self.translation_set_layout.addWidget(self.translation_hidden_checkbox)

        self.rotate_set_layout = QHBoxLayout()
        self.rotate_set_layout.addWidget(self.rotate_set_label)
        self.rotate_set_layout.addWidget(self.rotate_locked_checkbox)
        self.rotate_set_layout.addWidget(self.rotate_hidden_checkbox)

        self.scale_set_layout = QHBoxLayout()
        self.scale_set_layout.addWidget(self.scale_set_label)
        self.scale_set_layout.addWidget(self.scale_locked_checkbox)
        self.scale_set_layout.addWidget(self.scale_hidden_checkbox)

        self.visibility_set_layout = QHBoxLayout()
        self.visibility_set_layout.addWidget(self.visibility_set_label)
        self.visibility_set_layout.addWidget(self.visibility_locked_checkbox)
        self.visibility_set_layout.addWidget(self.visibility_hidden_checkbox)

        self.attr_operate_layout = QHBoxLayout()
        self.attr_operate_layout.addWidget(self.attr_set_button)
        self.attr_operate_layout.addWidget(self.attr_reset_button)

        self.attr_set_layout.addLayout(self.translation_set_layout)
        self.attr_set_layout.addLayout(self.rotate_set_layout)
        self.attr_set_layout.addLayout(self.scale_set_layout)
        self.attr_set_layout.addLayout(self.visibility_set_layout)
        self.attr_set_layout.addLayout(self.attr_operate_layout)

    # -------------------------------------------------------------------------
    # 信号连接
    # -------------------------------------------------------------------------

    def create_connections(self):
        """连接界面信号。"""

        self.add_attr_window_button.clicked.connect(self.open_add_attr_window)
        self.edit_attr_window_button.clicked.connect(self.open_edit_attr_window)
        self.connect_attr_window_button.clicked.connect(self.open_connection_editor)
        self.channel_control_window_button.clicked.connect(self.open_channel_control)
        self.delete_attr_window_button.clicked.connect(self.delete_selected_attr)

        self.attr_up_button.clicked.connect(self.move_attr_up)
        self.attr_down_button.clicked.connect(self.move_attr_down)

        self.attr_set_button.clicked.connect(self.clicked_attr_set_button)
        self.attr_reset_button.clicked.connect(self.clicked_attr_reset_button)

    # -------------------------------------------------------------------------
    # Maya 属性编辑窗口
    # -------------------------------------------------------------------------

    def open_add_attr_window(self):
        """打开 Maya 自带的 Add Attribute 窗口。"""
        mel.eval("dynAddAttrWin({})")

    def open_edit_attr_window(self):
        """打开 Maya 自带的 Edit Attribute 窗口。"""
        mel.eval("dynRenameAttrWin({})")

    def open_connection_editor(self):
        """打开 Maya Connection Editor。"""
        cmds.ConnectionEditor()

    def open_channel_control(self):
        """打开 Maya Channel Control。"""
        cmds.ChannelControlEditor()

    def delete_selected_attr(self):
        """删除 Maya Channel Box 中当前选中的自定义属性。"""
        mel.eval("dynDeleteAttrWin({})")

    # -------------------------------------------------------------------------
    # Channel Box 属性顺序
    # -------------------------------------------------------------------------

    def move_attr_up(self):
        """把 Channel Box 中选中的自定义属性向上移动。"""
        attrUtils.Attr.move_channelBox_attr(
            up=True,
            down=False
        )

    def move_attr_down(self):
        """把 Channel Box 中选中的自定义属性向下移动。"""
        attrUtils.Attr.move_channelBox_attr(
            up=False,
            down=True
        )

    # -------------------------------------------------------------------------
    # 属性锁定和隐藏
    # -------------------------------------------------------------------------

    def clicked_attr_set_button(self):
        """根据界面状态设置当前选择物体的 Transform 属性。"""

        selected_objects = cmds.ls(
            selection=True,
            long=True
        )

        if not selected_objects:
            cmds.warning(u"请先选择需要设置属性的物体。")
            return

        translation_lock = self.translation_locked_checkbox.isChecked()
        translation_hide = self.translation_hidden_checkbox.isChecked()

        rotate_lock = self.rotate_locked_checkbox.isChecked()
        rotate_hide = self.rotate_hidden_checkbox.isChecked()

        scale_lock = self.scale_locked_checkbox.isChecked()
        scale_hide = self.scale_hidden_checkbox.isChecked()

        visibility_lock = self.visibility_locked_checkbox.isChecked()
        visibility_hide = self.visibility_hidden_checkbox.isChecked()

        axis_list = [
            "X",
            "Y",
            "Z",
        ]

        for selected_object in selected_objects:
            attr_handler = attrUtils.Attr(selected_object)

            for axis in axis_list:
                translate_attr = "translate{}".format(axis)
                rotate_attr = "rotate{}".format(axis)
                scale_attr = "scale{}".format(axis)

                attr_handler.lock_and_hide_attr(
                    translate_attr,
                    lock=translation_lock,
                    hide=translation_hide
                )

                attr_handler.lock_and_hide_attr(
                    rotate_attr,
                    lock=rotate_lock,
                    hide=rotate_hide
                )

                attr_handler.lock_and_hide_attr(
                    scale_attr,
                    lock=scale_lock,
                    hide=scale_hide
                )

            attr_handler.lock_and_hide_attr(
                "visibility",
                lock=visibility_lock,
                hide=visibility_hide
            )

    def clicked_attr_reset_button(self):
        """清空界面中所有 Locked / Hidden 选项。"""

        for checkbox in self.attr_checkboxes:
            checkbox.setChecked(False)


# 旧类名兼容。
# 老代码如果仍然使用 Attr_Tool()，迁移期间继续可以运行。
Attr_Tool = AttrTool


def main():
    """创建属性工具并返回 QWidget，由 window_manager 负责显示。"""
    window = AttrTool()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
