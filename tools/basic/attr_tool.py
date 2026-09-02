# coding=utf-8
u"""
Attr Tool
=========

Maya Attribute 管理工具窗口。

模块职责
--------
1. 打开 Maya 原生 Add / Edit Attribute、Connection Editor、Channel Control；
2. 处理 Channel Box 自定义属性顺序这类 UI / Selection 工作流；
3. 批量设置 Translate / Rotate / Scale / Visibility 的 Attribute 状态；
4. Attribute 底层状态统一交给 ``core.attr_utils``。

架构边界
--------
- Channel Box 与 Selection 属于 Tool；
- Attribute Lock / Keyable / Channel Box 状态属于 core.attr_utils；
- 通用 Plug Connection 属于 core.connection_utils；
- 本文件不向 Core 反向塞入 Maya UI 状态。
"""

from __future__ import print_function

import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...config import icons_dir as icon_dir
from ...core import attr_utils
from ...core import scene_utils
from ...ui import theme as ui_theme
from ...ui import window_utils


def move_selected_channel_box_attr(up=True, down=False):
    u"""
    调整 Channel Box 当前 User Defined Attribute 的顺序。

    Args:
        up (bool):
            是否把目标 Attribute 在 Channel Box 中上移。
        down (bool):
            是否把目标 Attribute 在 Channel Box 中下移。

    Returns:
        bool:
            方法执行后的结果数据。
    """
    selections = scene_utils.get_selected_nodes(
        long=True,
        flatten=True
    )

    if not selections:
        cmds.warning(u"请先选择一个对象。")
        return False

    selected_attrs = cmds.channelBox(
        "mainChannelBox",
        query=True,
        selectedMainAttributes=True
    ) or []

    if not selected_attrs:
        cmds.warning(u"请在 Channel Box 中选择一个自定义属性。")
        return False

    node = selections[0]
    selected_attr = selected_attrs[0]
    selected_plug = "{}.{}".format(
        node,
        selected_attr
    )

    if not cmds.objExists(selected_plug):
        return False

    if cmds.getAttr(selected_plug, lock=True):
        cmds.warning(
            u"{} Attribute 不可以被编辑。".format(
                selected_plug
            )
        )
        return False

    attr_list = cmds.listAttr(
        node,
        userDefined=True
    ) or []

    if selected_attr not in attr_list:
        return False

    selected_index = attr_list.index(
        selected_attr
    )

    scene_utils.open_undo_chunk(
        "MuziMoveChannelBoxAttr"
    )

    try:
        if up and selected_index > 0:
            previous_attr = attr_list[selected_index - 1]
            cmds.deleteAttr(
                "{}.{}".format(
                    node,
                    previous_attr
                )
            )
            cmds.undo()

            index = selected_index + 1
            while index < len(attr_list):
                cmds.deleteAttr(
                    "{}.{}".format(
                        node,
                        attr_list[index]
                    )
                )
                cmds.undo()
                index += 1

        if down and selected_index < len(attr_list) - 1:
            cmds.deleteAttr(selected_plug)
            cmds.undo()

            index = selected_index + 2
            while index < len(attr_list):
                cmds.deleteAttr(
                    "{}.{}".format(
                        node,
                        attr_list[index]
                    )
                )
                cmds.undo()
                index += 1
    finally:
        scene_utils.close_undo_chunk()

    return True


class AttrTool(QWidget):
    u"""Attribute 工具窗口。"""

    def __init__(self, parent=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """

        super(AttrTool, self).__init__(parent)

        self.window_title = u"属性工具"

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        ui_theme.style_window(
            self,
            title=self.window_title,
            minimum_width=520
        )
        self.resize(560, 520)

    def create_widgets(self):
        u"""
        创建界面部件。
        """
        self.title_label = ui_theme.make_title(u"属性工具")
        self.subtitle_label = ui_theme.make_subtitle(
            u"管理 Maya 属性窗口、Channel Box 顺序以及常用 Transform Attribute 状态。"
        )

        self.add_attr_window_button = QPushButton(
            QIcon(icon_dir + "/add.png"),
            u"添加属性"
        )
        self.edit_attr_window_button = QPushButton(
            QIcon(icon_dir + "/edit.png"),
            u"编辑属性"
        )
        self.connect_attr_window_button = QPushButton(
            QIcon(icon_dir + "/connect-empty.png"),
            u"连接编辑器"
        )
        self.channel_control_window_button = QPushButton(
            QIcon(icon_dir + "/set.png"),
            u"Channel Control"
        )
        self.delete_attr_window_button = QPushButton(
            QIcon(icon_dir + "/delete.png"),
            u"删除属性"
        )
        ui_theme.style_danger(self.delete_attr_window_button)

        self.attr_move_info_label = QLabel(
            u"先在 Channel Box 中选中一个自定义属性，再调整顺序。"
        )
        ui_theme.set_role(self.attr_move_info_label, "muted")

        self.attr_up_button = QPushButton(
            QIcon(icon_dir + "/arrow-upward .png"),
            u"向上移动"
        )
        self.attr_down_button = QPushButton(
            QIcon(icon_dir + "/arrow-downward.png"),
            u"向下移动"
        )

        self.translation_set_label = QLabel("Translate")
        self.rotate_set_label = QLabel("Rotate")
        self.scale_set_label = QLabel("Scale")
        self.visibility_set_label = QLabel("Visibility")

        self.lock_header_label = QLabel(u"锁定")
        self.hide_header_label = QLabel(u"隐藏")
        ui_theme.set_role(self.lock_header_label, "muted")
        ui_theme.set_role(self.hide_header_label, "muted")

        self.translation_locked_checkbox = QCheckBox()
        self.translation_hidden_checkbox = QCheckBox()
        self.rotate_locked_checkbox = QCheckBox()
        self.rotate_hidden_checkbox = QCheckBox()
        self.scale_locked_checkbox = QCheckBox()
        self.scale_hidden_checkbox = QCheckBox()
        self.visibility_locked_checkbox = QCheckBox()
        self.visibility_hidden_checkbox = QCheckBox()

        self.attr_set_button = QPushButton(
            QIcon(icon_dir + "/set.png"),
            u"应用到选择对象"
        )
        ui_theme.style_primary(self.attr_set_button)

        self.attr_reset_button = QPushButton(
            QIcon(icon_dir + "/reset.png"),
            u"重置选项"
        )
        ui_theme.style_ghost(self.attr_reset_button)

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

    def create_layouts(self):
        u"""
        创建窗口布局。
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        editor_card, editor_layout = ui_theme.make_card(self)
        editor_layout.addWidget(ui_theme.make_section_title(u"属性编辑"))

        editor_grid = QGridLayout()
        editor_grid.setHorizontalSpacing(8)
        editor_grid.setVerticalSpacing(8)
        editor_grid.addWidget(self.add_attr_window_button, 0, 0)
        editor_grid.addWidget(self.edit_attr_window_button, 0, 1)
        editor_grid.addWidget(self.connect_attr_window_button, 0, 2)
        editor_grid.addWidget(self.channel_control_window_button, 1, 0)
        editor_grid.addWidget(self.delete_attr_window_button, 1, 1)
        editor_layout.addLayout(editor_grid)

        order_card, order_layout = ui_theme.make_card(self)
        order_layout.addWidget(ui_theme.make_section_title(u"Channel Box 排序"))
        order_layout.addWidget(self.attr_move_info_label)

        order_button_layout = QHBoxLayout()
        order_button_layout.addWidget(self.attr_up_button)
        order_button_layout.addWidget(self.attr_down_button)
        order_layout.addLayout(order_button_layout)

        state_card, state_layout = ui_theme.make_card(self)
        state_layout.addWidget(ui_theme.make_section_title(u"属性状态"))

        state_grid = QGridLayout()
        state_grid.setHorizontalSpacing(18)
        state_grid.setVerticalSpacing(10)
        state_grid.addWidget(self.lock_header_label, 0, 1, Qt.AlignCenter)
        state_grid.addWidget(self.hide_header_label, 0, 2, Qt.AlignCenter)
        state_grid.addWidget(self.translation_set_label, 1, 0)
        state_grid.addWidget(self.translation_locked_checkbox, 1, 1, Qt.AlignCenter)
        state_grid.addWidget(self.translation_hidden_checkbox, 1, 2, Qt.AlignCenter)
        state_grid.addWidget(self.rotate_set_label, 2, 0)
        state_grid.addWidget(self.rotate_locked_checkbox, 2, 1, Qt.AlignCenter)
        state_grid.addWidget(self.rotate_hidden_checkbox, 2, 2, Qt.AlignCenter)
        state_grid.addWidget(self.scale_set_label, 3, 0)
        state_grid.addWidget(self.scale_locked_checkbox, 3, 1, Qt.AlignCenter)
        state_grid.addWidget(self.scale_hidden_checkbox, 3, 2, Qt.AlignCenter)
        state_grid.addWidget(self.visibility_set_label, 4, 0)
        state_grid.addWidget(self.visibility_locked_checkbox, 4, 1, Qt.AlignCenter)
        state_grid.addWidget(self.visibility_hidden_checkbox, 4, 2, Qt.AlignCenter)
        state_grid.setColumnStretch(0, 1)
        state_layout.addLayout(state_grid)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.attr_reset_button)
        action_layout.addStretch(1)
        action_layout.addWidget(self.attr_set_button)
        state_layout.addLayout(action_layout)

        main_layout.addWidget(editor_card)
        main_layout.addWidget(order_card)
        main_layout.addWidget(state_card)
        main_layout.addStretch(1)

    def create_connections(self):
        u"""
        连接界面信号。
        """
        self.add_attr_window_button.clicked.connect(self.open_add_attr_window)
        self.edit_attr_window_button.clicked.connect(self.open_edit_attr_window)
        self.connect_attr_window_button.clicked.connect(self.open_connection_editor)
        self.channel_control_window_button.clicked.connect(self.open_channel_control)
        self.delete_attr_window_button.clicked.connect(self.delete_selected_attr)
        self.attr_up_button.clicked.connect(self.move_attr_up)
        self.attr_down_button.clicked.connect(self.move_attr_down)
        self.attr_set_button.clicked.connect(self.clicked_attr_set_button)
        self.attr_reset_button.clicked.connect(self.clicked_attr_reset_button)

    @staticmethod
    def open_add_attr_window():
        u"""
        执行 `open_add_attr_window` 对应的 Maya 工具操作。
        """

        mel.eval("dynAddAttrWin({})")

    @staticmethod
    def open_edit_attr_window():
        u"""
        执行 `open_edit_attr_window` 对应的 Maya 工具操作。
        """

        mel.eval("dynRenameAttrWin({})")

    @staticmethod
    def open_connection_editor():
        u"""
        执行 `open_connection_editor` 对应的 Maya 工具操作。
        """

        cmds.ConnectionEditor()

    @staticmethod
    def open_channel_control():
        u"""
        执行 `open_channel_control` 对应的 Maya 工具操作。
        """

        cmds.ChannelControlEditor()

    @staticmethod
    def delete_selected_attr():
        u"""
        执行 `delete_selected_attr` 对应的 Maya 工具操作。
        """

        mel.eval("dynDeleteAttrWin({})")

    @staticmethod
    def move_attr_up():
        u"""
        执行 `move_attr_up` 对应的 Maya 工具操作。

        Returns:
            object:
                方法执行后的结果数据。
        """

        return move_selected_channel_box_attr(
            up=True,
            down=False
        )

    @staticmethod
    def move_attr_down():
        u"""
        执行 `move_attr_down` 对应的 Maya 工具操作。

        Returns:
            object:
                方法执行后的结果数据。
        """

        return move_selected_channel_box_attr(
            up=False,
            down=True
        )

    def clicked_attr_set_button(self):
        u"""
        把界面状态应用到当前选择对象的 Transform Channels。
        """
        selected_objects = scene_utils.get_selected_nodes(
            long=True,
            flatten=True
        )

        if not selected_objects:
            cmds.warning(u"请先选择需要设置 Attribute 的对象。")
            return

        translation_lock = self.translation_locked_checkbox.isChecked()
        translation_hide = self.translation_hidden_checkbox.isChecked()
        rotate_lock = self.rotate_locked_checkbox.isChecked()
        rotate_hide = self.rotate_hidden_checkbox.isChecked()
        scale_lock = self.scale_locked_checkbox.isChecked()
        scale_hide = self.scale_hidden_checkbox.isChecked()
        visibility_lock = self.visibility_locked_checkbox.isChecked()
        visibility_hide = self.visibility_hidden_checkbox.isChecked()

        axis_list = ["X", "Y", "Z"]

        scene_utils.open_undo_chunk("MuziAttrToolSetState")

        try:
            for selected_object in selected_objects:
                attr_handler = attr_utils.Attr(selected_object)

                for axis in axis_list:
                    translate_attr = "translate{}".format(axis)
                    rotate_attr = "rotate{}".format(axis)
                    scale_attr = "scale{}".format(axis)

                    attr_handler.set_attr_state(
                        translate_attr,
                        lock=translation_lock,
                        keyable=not translation_hide,
                        channel_box=not translation_hide
                    )
                    attr_handler.set_attr_state(
                        rotate_attr,
                        lock=rotate_lock,
                        keyable=not rotate_hide,
                        channel_box=not rotate_hide
                    )
                    attr_handler.set_attr_state(
                        scale_attr,
                        lock=scale_lock,
                        keyable=not scale_hide,
                        channel_box=not scale_hide
                    )

                attr_handler.set_attr_state(
                    "visibility",
                    lock=visibility_lock,
                    keyable=not visibility_hide,
                    channel_box=not visibility_hide
                )
        finally:
            scene_utils.close_undo_chunk()

    def clicked_attr_reset_button(self):
        u"""
        清空界面中的 Lock / Hidden 选项。
        """
        for checkbox in self.attr_checkboxes:
            checkbox.setChecked(False)


def main():
    u"""
    创建或恢复 Attr Tool，立即显示并返回 QWidget。

    Returns:
        object:
            方法执行后的结果数据。
    """
    return window_utils.show_window(
        "tools.basic.attr_tool",
        AttrTool
    )


__all__ = [
    "AttrTool",
    "main",
]
