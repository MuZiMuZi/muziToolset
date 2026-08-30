# coding=utf-8
u"""
Maya Object Picker
==================

可复用的 Maya 场景对象拾取控件。

界面：
    Label | LineEdit | 拾取

职责：
    - 显示当前对象名称；
    - 从 Maya 当前选择中读取最后一个对象；
    - 可选地限制 Maya nodeType；
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

from .. import theme


class MayaObjectPicker(QWidget):
    """Maya 场景对象拾取行。"""

    value_changed = Signal(str)

    def __init__(
        self,
        label_text=u"对象",
        placeholder=u"选择 Maya 对象后点击拾取",
        node_types=None,
        parent=None
    ):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            label_text (str):
                `label_text` 对应的名称、标记或字符串参数。
            placeholder (str):
                `placeholder` 对应的名称、标记或字符串参数。
            node_types (object):
                `node_types` 对应的输入数据。
            parent (str):
                父级 Maya 节点名称。
        """

        super(MayaObjectPicker, self).__init__(parent)

        self.node_types = node_types

        self.label = QLabel(label_text)
        self.label.setMinimumWidth(82)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.setClearButtonEnabled(True)

        self.pick_button = QPushButton(u"拾取")
        self.pick_button.setFixedWidth(64)
        theme.style_ghost(self.pick_button)

        self.create_layout()
        self.create_connections()

    def create_layout(self):
        u"""
        创建控件布局。
        """
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)

        main_layout.addWidget(self.label)
        main_layout.addWidget(self.line_edit, 1)
        main_layout.addWidget(self.pick_button)

    def create_connections(self):
        u"""
        连接控件信号。
        """
        self.pick_button.clicked.connect(
            self.pick_from_selection
        )
        self.line_edit.textChanged.connect(
            self.value_changed.emit
        )

    def get_value(self):
        u"""
        返回当前输入值。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.line_edit.text().strip()

    def set_value(self, value):
        u"""
        设置当前输入值。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """
        if value is None:
            value = ""

        self.line_edit.setText(value)

    def clear(self):
        u"""
        清空当前值。
        """
        self.line_edit.clear()

    def _is_allowed_node(self, node):
        """检查节点类型是否符合当前 Picker 限制。"""
        if not self.node_types:
            return True

        try:
            node_type = cmds.nodeType(node)
        except Exception:
            return False

        for allowed_type in self.node_types:
            if node_type == allowed_type:
                return True

        return False

    def pick_from_selection(self):
        u"""
        读取 Maya 当前选择中的最后一个对象。

        Returns:
            object | None:
                方法执行后的结果数据。
        """
        selection = cmds.ls(
            selection=True,
            long=True
        ) or []

        if not selection:
            cmds.warning(u"请先在 Maya 场景中选择一个对象。")
            return None

        selected_object = selection[-1]

        if not self._is_allowed_node(selected_object):
            allowed_text = ", ".join(self.node_types)
            cmds.warning(
                u"当前对象类型不符合要求，允许类型：{}".format(
                    allowed_text
                )
            )
            return None

        self.set_value(selected_object)
        return selected_object
