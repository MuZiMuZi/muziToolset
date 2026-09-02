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
        u"""
        初始化 Maya Object Picker。

        Args:
            label_text (str):
                Object Picker 左侧显示的 Label 文本。
            placeholder (str):
                QLineEdit / Object Picker 在没有输入时显示的 Placeholder 文本。
            node_types (str | list[str] | None):
                Object Picker 允许选择的 Maya Node Type；None 表示不限制类型。
            parent (str):
                父级 Maya 节点名称。
        """
        # -------------------------------------------------------------------------
        # Step 01：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        super(MayaObjectPicker, self).__init__(parent)

        if isinstance(node_types, str):
            node_types = [node_types]

        self.node_types = node_types

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.label = QLabel(
            label_text
        )
        self.label.setMinimumWidth(82)

        self.line_edit = QLineEdit()
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.line_edit.setPlaceholderText(
            placeholder
        )
        self.line_edit.setClearButtonEnabled(True)

        self.pick_button = QPushButton(
            u"拾取"
        )
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.pick_button.setFixedWidth(64)
        theme.style_ghost(
            self.pick_button
        )

        self.create_layout()
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.create_connections()

    # =========================================================================
    # UI
    # =========================================================================

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

    # =========================================================================
    # Value
    # =========================================================================

    def get_value(self):
        u"""

                返回当前输入的 Maya DAG Short Name。

                即使用户手动粘贴 Long DAG Path，也统一通过
                core.rename_utils.get_short_name() 规范化。

                Returns:
                    object:
                    当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

        """
        value = self.line_edit.text().strip()

        return rename_utils.get_short_name(
            value
        )

    def set_value(self, value):
        u"""
        设置当前输入值，并统一显示 Short Name。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """
        short_name = rename_utils.get_short_name(
            value
        )

        self.line_edit.setText(
            short_name
        )

    def clear(self):
        u"""
        清空当前值。
        """
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

                Returns:
                    object | None:
                    当前 API 完成处理后返回的结果。

        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        selection = cmds.ls(
            selection=True,
            long=True
        )

        if selection is None:
            selection = []

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not selection:
            cmds.warning(
                u"请先在 Maya 场景中选择一个对象。"
            )
            return None

        selected_object = selection[-1]

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self._validate_unique_short_name(
                short_name
        ):
            return None

        self.set_value(
            short_name
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return short_name


__all__ = [
    "MayaObjectPicker",
]
