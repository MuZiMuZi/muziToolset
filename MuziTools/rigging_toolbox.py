# coding=utf-8
u"""
Rigging Toolbox
===============

MuziTools 主面板。

特点：
    - ``tools`` 注册表只扫描文件，子工具点击时才真正 import；
    - 分类默认收起；
    - 工具按钮统一交给 ``window_manager`` 管理；
    - 支持开发过程中刷新工具列表；
    - 单个工具加载失败时只提示该工具，不影响整个 Toolbox。
"""

from __future__ import print_function

import traceback
from functools import partial

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QScrollArea
    from PySide2.QtWidgets import QSizePolicy
    from PySide2.QtWidgets import QToolButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QScrollArea
    from PySide6.QtWidgets import QSizePolicy
    from PySide6.QtWidgets import QToolButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget
    from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui

from . import window_manager
from .tools import get_tools_by_category
from .tools import refresh_tools


_window = None


_TOOL_DISPLAY_NAMES = {
    "rename_tool": u"重命名工具",
    "attr_tool": u"属性工具",
    "connections_tool": u"连接工具",
    "constraint_tool": u"约束工具",
    "joint_tool": u"Joint 工具",
    "joint_resamp_tool": u"关节链重采样",
    "control_shape_tool": u"控制器 Shape 图库",
    "create_ctrl_tool": u"创建控制器",
    "create_fk_ctrl_tool": u"创建 FK 控制器",
    "set_ctrl_tool": u"编辑控制器 Shape",
    "face_rig_tool": u"Face Rig Wizard",
    "rig_tool": u"Rig 工具",
    "skirt_ctrl_tool": u"裙子绑定工具",
    "face_select_key_tool": u"面部 Driven Key",
    "skin_tool": u"Skin 工具",
    "add_blendshape_tool": u"BlendShape Target",
    "invert_shape_tool": u"Invert Shape",
    "hierarchy_cleaner": u"层级清理器",
    "model_checker": u"模型检查器",
}


def get_maya_main_window():
    """获取 Maya 主窗口 QWidget。"""
    try:
        pointer = omui.MQtUtil.mainWindow()
    except Exception:
        pointer = None

    if pointer is None:
        return None

    try:
        return wrapInstance(int(pointer), QWidget)
    except Exception:
        return None


def _display_name(tool_name):
    """返回工具按钮显示名称。"""
    if tool_name in _TOOL_DISPLAY_NAMES:
        return _TOOL_DISPLAY_NAMES[tool_name]

    words = tool_name.split("_")
    display_words = []

    for word in words:
        if not word:
            continue
        display_words.append(word.title())

    return " ".join(display_words)


class CollapsibleBox(QWidget):
    """简单稳定的可折叠分类容器。"""

    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QToolButton(self)
        self.toggle_button.setText(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.setToolButtonStyle(
            Qt.ToolButtonTextBesideIcon
        )
        self.toggle_button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.content_area = QFrame(self)
        self.content_area.setFrameShape(QFrame.NoFrame)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)

        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 4, 4, 6)
        self.content_layout.setSpacing(4)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)

        self.toggle_button.toggled.connect(self.set_expanded)

    def set_expanded(self, expanded):
        """设置展开状态。"""
        if self.toggle_button.isChecked() != expanded:
            self.toggle_button.blockSignals(True)
            self.toggle_button.setChecked(expanded)
            self.toggle_button.blockSignals(False)

        if expanded:
            self.toggle_button.setArrowType(Qt.DownArrow)
            self.content_area.setMaximumHeight(16777215)
        else:
            self.toggle_button.setArrowType(Qt.RightArrow)
            self.content_area.setMaximumHeight(0)

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)


class RiggingToolbox(QWidget):
    """木子绑定工具盒主窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = get_maya_main_window()

        super(RiggingToolbox, self).__init__(parent)

        self.setWindowTitle(u"木子绑定工具盒")
        self.setWindowFlags(Qt.Window)
        self.setMinimumSize(360, 500)
        self.resize(400, 650)

        try:
            self.setAttribute(Qt.WA_DeleteOnClose, False)
        except Exception:
            pass

        self.tools_by_category = {}
        self.category_boxes = {}

        self.title_label = QLabel(u"Rigging Toolbox")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.refresh_button = QPushButton(u"刷新工具")
        self.expand_button = QPushButton(u"全部展开")
        self.collapse_button = QPushButton(u"全部收起")
        self.close_subtools_button = QPushButton(u"关闭子工具")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(4)
        self.scroll_area.setWidget(self.scroll_content)

        self._create_layout()
        self._create_connections()
        self.rebuild_tool_buttons(refresh_registry=False)

    def _create_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        main_layout.addWidget(self.title_label)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.refresh_button)
        toolbar_layout.addWidget(self.expand_button)
        toolbar_layout.addWidget(self.collapse_button)
        toolbar_layout.addWidget(self.close_subtools_button)
        main_layout.addLayout(toolbar_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)
        main_layout.addWidget(self.scroll_area, 1)

    def _create_connections(self):
        self.refresh_button.clicked.connect(self.refresh_tool_registry)
        self.expand_button.clicked.connect(self.expand_all)
        self.collapse_button.clicked.connect(self.collapse_all)
        self.close_subtools_button.clicked.connect(
            window_manager.close_all_tools
        )

    def _clear_tool_layout(self):
        """删除当前分类 UI。"""
        while self.scroll_layout.count():
            layout_item = self.scroll_layout.takeAt(0)
            widget = layout_item.widget()

            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        self.category_boxes = {}

    def _create_tool_button(
            self,
            category_name,
            tool_name,
            tool_function
    ):
        button = QPushButton(_display_name(tool_name))
        button.setMinimumHeight(30)
        button.setToolTip(
            u"打开 {}.py".format(tool_name)
        )

        tool_key = "{}/{}".format(
            category_name,
            tool_name
        )

        callback = partial(
            self.run_tool,
            tool_key,
            tool_function
        )
        button.clicked.connect(callback)

        return button

    def rebuild_tool_buttons(self, refresh_registry=False):
        """根据注册表重建分类和按钮。"""
        if refresh_registry:
            self.tools_by_category = refresh_tools()
        else:
            self.tools_by_category = get_tools_by_category()

        self._clear_tool_layout()

        if not self.tools_by_category:
            empty_label = QLabel(
                u"没有发现可用工具。\n"
                u"请检查 MuziTools/tools/<category>/*.py。"
            )
            empty_label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(empty_label)
            self.scroll_layout.addStretch(1)
            return

        for category_name in self.tools_by_category:
            tools_dict = self.tools_by_category[category_name]
            category_box = CollapsibleBox(category_name)

            for tool_name in tools_dict:
                tool_function = tools_dict[tool_name]
                button = self._create_tool_button(
                    category_name,
                    tool_name,
                    tool_function
                )
                category_box.add_widget(button)

            self.category_boxes[category_name] = category_box
            self.scroll_layout.addWidget(category_box)

        self.scroll_layout.addStretch(1)

    def refresh_tool_registry(self, checked=False):
        self.rebuild_tool_buttons(refresh_registry=True)

    def expand_all(self, checked=False):
        for category_name in self.category_boxes:
            category_box = self.category_boxes[category_name]
            category_box.set_expanded(True)

    def collapse_all(self, checked=False):
        for category_name in self.category_boxes:
            category_box = self.category_boxes[category_name]
            category_box.set_expanded(False)

    def run_tool(
            self,
            tool_key,
            tool_function,
            checked=False
    ):
        """安全执行一个工具 Runner。"""
        try:
            return window_manager.show_tool(
                tool_key,
                tool_function
            )
        except Exception as error:
            print(u"\n[MuziTools] 工具打开失败：{}".format(tool_key))
            traceback.print_exc()

            QMessageBox.critical(
                self,
                u"工具打开失败",
                u"{}\n\n{}".format(
                    tool_key,
                    error
                )
            )
            return None


# 旧类名保留给 Tool_main.py，但实际实现只维护这一份。
Rigging_Toolbox = RiggingToolbox


def main():
    """显示唯一的 Rigging Toolbox 窗口。"""
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = RiggingToolbox()
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window


if __name__ == "__main__":
    main()
