# coding=utf-8
u"""
Maya Object Picker
==================

可复用的 Maya 场景对象拾取控件。

界面：
    Label | LineEdit | 拾取

职责：
    - 显示当前对象的短名称；
    - 从 Maya 当前选择中读取最后一个对象；
    - 可选地限制 Maya nodeType；
    - 检查短名称在当前场景中是否唯一；
    - 不包含任何具体 Rig Build 逻辑。

说明：
    Maya 的 Long DAG Path 会随着 reparent 改变。
    Rig Setup 通常会整理输入模型层级，因此 Picker 不保存类似：
        |grp_model|grp_head|model_md_head_001
    这样的完整路径，而是保存稳定的短名称：
        model_md_head_001
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
    u"""Maya 场景对象拾取行。"""

    value_changed = Signal(str)

    def __init__(
            self,
            label_text=u"对象",
            placeholder=u"选择 Maya 对象后点击拾取",
            node_types=None,
            parent=None
    ):
        u"""
        初始化 Maya Object Picker。

        Args:
            label_text (str):
                Object Picker 左侧显示的 Label 文本。
            placeholder (str):
                没有输入时显示的 Placeholder 文本。
            node_types (str | list[str] | None):
                允许选择的 Maya Node Type；None 表示不限制类型。
            parent (QWidget | None):
                Qt 父窗口。
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
    # Name
    # =========================================================================

    @staticmethod
    def get_short_name(node):
        u"""
        把 Maya Long DAG Path 转换成节点短名称。

        Examples:
            |grp_model_001|grp_md_facial_model_001|model_md_head_001
            -> model_md_head_001

        Args:
            node (str | None):
                Maya 节点名称或 DAG Path。

        Returns:
            str:
                不带 DAG 层级的节点短名称。
        """
        if node is None:
            return ""

        node = str(node).strip()

        if not node:
            return ""

        return node.split("|")[-1]

    @staticmethod
    def get_long_matches(short_name):
        u"""
        查询一个短名称在当前 Maya 场景中对应的全部 DAG Path。

        Args:
            short_name (str):
                Maya 节点短名称。

        Returns:
            list[str]:
                匹配到的 Long DAG Path。
        """
        if not short_name:
            return []

        matches = cmds.ls(
            short_name,
            long=True
        )

        if matches is None:
            matches = []

        return matches

    def is_unique_short_name(self, short_name):
        u"""
        检查短名称在当前场景中是否唯一。

        Rig 系统后续使用短名称工作，因此同名 DAG 节点必须先处理掉。

        Args:
            short_name (str):
                Maya 节点短名称。

        Returns:
            bool:
                唯一时返回 True。
        """
        matches = self.get_long_matches(
            short_name
        )

        return len(matches) == 1

    # =========================================================================
    # Value
    # =========================================================================

    def get_value(self):
        u"""
        返回当前输入的 Maya 节点短名称。

        即使用户手动粘贴 Long DAG Path，也统一返回最后一级节点名。

        Returns:
            str:
                Maya 节点短名称。
        """
        value = self.line_edit.text().strip()
        return self.get_short_name(value)

    def set_value(self, value):
        u"""
        设置当前输入值，并统一显示为短名称。

        Args:
            value (str | None):
                Maya 节点名称或 DAG Path。
        """
        short_name = self.get_short_name(
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

        Maya 查询阶段使用 Long DAG Path，保证拿到用户真正选择的节点；
        写入 UI 前转换成短名称。若短名称不唯一，则拒绝写入，避免后续
        Rig Build 操作到错误对象。

        Returns:
            str | None:
                成功时返回节点短名称，否则返回 None。
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

        if not self._is_allowed_node(selected_object):
            allowed_text = ", ".join(self.node_types)
            cmds.warning(
                u"当前对象类型不符合要求，允许类型：{}".format(
                    allowed_text
                )
            )
            return None

        short_name = self.get_short_name(
            selected_object
        )

        if not self.is_unique_short_name(short_name):
            cmds.warning(
                u"节点短名称不唯一，Face/Rig 系统不能安全使用该名称：{}。"
                u"请先把场景中的同名节点重命名。".format(
                    short_name
                )
            )
            return None

        self.set_value(
            short_name
        )

        return short_name
