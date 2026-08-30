# coding=utf-8
u"""
Maya Object Picker
==================

可复用的 Maya 场景对象拾取控件。

界面：
    Label | LineEdit | 拾取

职责：
    - 从 Maya 当前选择读取对象；
    - 可选限制 Maya nodeType；
    - UI 统一显示 DAG Short Name；
    - Short Name 规范化和唯一性规则复用 Core；
    - 不包含任何具体 Rig Build 逻辑。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtCore import Signal
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QWidget

from ...core import rename_utils
from ...core import scene_utils
from .. import theme


class MayaObjectPicker(QWidget):
    u"""Maya 场景对象拾取行。"""

    value_changed = Signal(str)

    def __init__(
            self,
            label_text=u"对象",
            placeholder=u"选择 Maya 对象后点击拾取",
            node_types=None,
            parent=None
    ):
        u"""初始化 Maya Object Picker。"""
        super(MayaObjectPicker, self).__init__(parent)

        if isinstance(node_types, str):
            node_types = [node_types]

        self.node_types = node_types

        self.label = QLabel(
            label_text
        )
        self.label.setMinimumWidth(82)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(
            placeholder
        )
        self.line_edit.setClearButtonEnabled(True)

        self.pick_button = QPushButton(
            u"拾取"
        )
        self.pick_button.setFixedWidth(64)
        theme.style_ghost(
            self.pick_button
        )

        self.create_layout()
        self.create_connections()

    # =========================================================================
    # UI
    # =========================================================================

    def create_layout(self):
        u"""创建控件布局。"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        main_layout.addWidget(self.label)
        main_layout.addWidget(self.line_edit, 1)
        main_layout.addWidget(self.pick_button)

    def create_connections(self):
        u"""连接控件信号。"""
        self.pick_button.clicked.connect(
            self.pick_from_selection
        )

        self.line_edit.textChanged.connect(
            self.value_changed.emit
        )

    # =========================================================================
    # Value
    # =========================================================================

    def get_value(self):
        u"""
        返回当前输入的 Maya DAG Short Name。

        即使用户手动粘贴 Long DAG Path，也统一通过
        core.rename_utils.get_short_name() 规范化。
        """
        value = self.line_edit.text().strip()

        return rename_utils.get_short_name(
            value
        )

    def set_value(self, value):
        u"""设置当前输入值，并统一显示 Short Name。"""
        short_name = rename_utils.get_short_name(
            value
        )

        self.line_edit.setText(
            short_name
        )

    def clear(self):
        u"""清空当前值。"""
        self.line_edit.clear()

    # =========================================================================
    # Validation / Pick
    # =========================================================================

    def _is_allowed_node(self, node):
        u"""检查节点类型是否符合当前 Picker 限制。"""
        if not self.node_types:
            return True

        try:
            node_type = cmds.nodeType(
                node
            )
        except Exception:
            return False

        for allowed_type in self.node_types:
            if node_type == allowed_type:
                return True

        return False

    def _validate_unique_short_name(self, short_name):
        u"""
        检查 Short Name 是否可以唯一解析到场景节点。

        唯一性规则统一复用 scene_utils.get_long_name()，
        Picker 不再维护自己的 cmds.ls(long=True) 查询实现。
        """
        try:
            scene_utils.get_long_name(
                short_name
            )
        except RuntimeError as error:
            cmds.warning(
                u"节点名称无法安全使用：{} | {}".format(
                    short_name,
                    error
                )
            )
            return False

        return True

    def pick_from_selection(self):
        u"""
        读取 Maya 当前选择中的最后一个对象。

        查询阶段使用 Long DAG Path 精确获取用户选择；
        写入 UI 前统一转换为 Short Name。
        """
        selection = cmds.ls(
            selection=True,
            long=True
        )

        if selection is None:
            selection = []

        if not selection:
            cmds.warning(
                u"请先在 Maya 场景中选择一个对象。"
            )
            return None

        selected_object = selection[-1]

        if not self._is_allowed_node(
                selected_object
        ):
            allowed_text = ", ".join(
                self.node_types
            )

            cmds.warning(
                u"当前对象类型不符合要求，允许类型：{}".format(
                    allowed_text
                )
            )
            return None

        short_name = rename_utils.get_short_name(
            selected_object
        )

        if not self._validate_unique_short_name(
                short_name
        ):
            return None

        self.set_value(
            short_name
        )

        return short_name


__all__ = [
    "MayaObjectPicker",
]
