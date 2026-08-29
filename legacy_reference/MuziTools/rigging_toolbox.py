# coding=utf-8
u"""
Rigging Toolbox
===============

MuziTools 主面板。

界面设计：
    - 左侧分类导航；
    - 右侧工具 Card 内容区；
    - 深色分层背景 + 紫色 Accent；
    - 工具模块点击时才 import，保持 Maya 启动轻量；
    - 子工具统一交给 window_manager 管理。
"""

from __future__ import print_function

import traceback
from functools import partial

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QScrollArea
    from PySide2.QtWidgets import QSizePolicy
    from PySide2.QtWidgets import QStackedWidget
    from PySide2.QtWidgets import QToolButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QScrollArea
    from PySide6.QtWidgets import QSizePolicy
    from PySide6.QtWidgets import QStackedWidget
    from PySide6.QtWidgets import QToolButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget
    from shiboken6 import wrapInstance

import maya.OpenMayaUI as omui

from . import ui_theme
from . import window_manager
from .tools import get_tools_by_category
from .tools import refresh_tools


_window = None


_TOOL_DISPLAY_NAMES = {
    "rename_tool": u"重命名工具",
    "attr_tool": u"属性工具",
    "connections_tool": u"连接工具",
    "constraint_tool": u"约束工具",
    "snap_tool": u"快速吸附",
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


_TOOL_DESCRIPTIONS = {
    "rename_tool": u"批量命名、替换、前后缀与层级重命名。",
    "attr_tool": u"属性编辑、Channel Box 排序、锁定与隐藏。",
    "connections_tool": u"Transform、自定义属性与已有连接管理。",
    "constraint_tool": u"常用约束创建、查询和删除。",
    "snap_tool": u"把最后选择对象吸附到前面对象的平均位置与旋转。",
    "joint_tool": u"Joint 创建、显示、镜像与常用骨骼操作。",
    "joint_resamp_tool": u"在关节链区间重新分布关节。",
    "control_shape_tool": u"浏览、替换、缩放、旋转与管理控制器 Shape。",
    "create_ctrl_tool": u"创建标准控制器层级、颜色与输出结构。",
    "create_fk_ctrl_tool": u"根据 Joint 链快速建立 FK 控制器。",
    "set_ctrl_tool": u"修改已有控制器 Shape。",
    "face_rig_tool": u"面部绑定流程入口。",
    "rig_tool": u"FK、IK、PV、层级、约束等常用绑定操作。",
    "skirt_ctrl_tool": u"裙子定位曲线、Blueprint、Bind Joint 与 FK 创建。",
    "face_select_key_tool": u"快速建立面部 Driven Key 驱动关系。",
    "skin_tool": u"Skin 绑定、复制权重、导入导出与影响骨骼管理。",
    "add_blendshape_tool": u"BlendShape Target 查询、复制与管理。",
    "invert_shape_tool": u"基于 Maya invertShape 的修型反算工具。",
    "hierarchy_cleaner": u"安全清理层级、空组与可清理历史。",
    "model_checker": u"模型拓扑、命名、Transform 与历史检查。",
}


_CATEGORY_DESCRIPTIONS = {
    u"基础工具": u"命名、属性、连接、约束与吸附等通用 Maya 操作。",
    u"骨骼工具": u"Joint 创建、编辑、镜像和关节链处理。",
    u"控制器工具": u"Controller 创建、Shape 图库与 FK 控制器。",
    u"绑定工具": u"身体 Rig、IK / FK、裙子等绑定模块。",
    u"面部工具": u"Face Rig 与 Driven Key 面部驱动。",
    u"蒙皮工具": u"SkinCluster、权重复制与权重文件管理。",
    u"BlendShape工具": u"BlendShape Target 与修型反算。",
    u"清理工具": u"场景层级和模型检查清理。",
}


_CATEGORY_SHORT_NAMES = {
    u"基础工具": "BASIC",
    u"骨骼工具": "JOINT",
    u"控制器工具": "CTRL",
    u"绑定工具": "RIG",
    u"面部工具": "FACE",
    u"蒙皮工具": "SKIN",
    u"BlendShape工具": "SHAPE",
    u"清理工具": "CLEAN",
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
    """返回工具显示名称。"""
    if tool_name in _TOOL_DISPLAY_NAMES:
        return _TOOL_DISPLAY_NAMES[tool_name]

    words = tool_name.split("_")
    display_words = []

    for word in words:
        if not word:
            continue

        display_words.append(word.title())

    return " ".join(display_words)


def _tool_description(tool_name):
    """返回工具说明。"""
    if tool_name in _TOOL_DESCRIPTIONS:
        return _TOOL_DESCRIPTIONS[tool_name]

    return u"打开 {} 模块。".format(tool_name)


class ToolCard(QFrame):
    """主工具箱右侧使用的工具卡片。"""

    def __init__(
            self,
            category_name,
            tool_name,
            tool_function,
            run_callback,
            parent=None
    ):
        super(ToolCard, self).__init__(parent)

        self.category_name = category_name
        self.tool_name = tool_name
        self.tool_function = tool_function
        self.run_callback = run_callback

        ui_theme.set_role(self, "card")
        self.setMinimumHeight(128)
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.category_label = QLabel(
            _CATEGORY_SHORT_NAMES.get(category_name, "TOOL")
        )
        ui_theme.set_role(self.category_label, "accent")

        self.title_label = ui_theme.make_section_title(
            _display_name(tool_name)
        )

        self.description_label = QLabel(
            _tool_description(tool_name)
        )
        self.description_label.setWordWrap(True)
        ui_theme.set_role(self.description_label, "muted")

        self.module_label = QLabel(
            u"{}.py".format(tool_name)
        )
        ui_theme.set_role(self.module_label, "muted")

        self.open_button = QPushButton(u"打开工具")
        self.open_button.setMinimumWidth(92)

        tool_key = "{}/{}".format(
            category_name,
            tool_name
        )

        callback = partial(
            self.run_callback,
            tool_key,
            tool_function
        )
        self.open_button.clicked.connect(callback)

        self.create_layouts()

    def create_layouts(self):
        """创建 Card 内部布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(6)

        main_layout.addWidget(self.category_label)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.description_label)
        main_layout.addStretch(1)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.module_label)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.open_button)

        main_layout.addLayout(bottom_layout)


class CategoryPage(QWidget):
    """右侧单个工具分类页面。"""

    def __init__(
            self,
            category_name,
            tools_dict,
            run_callback,
            parent=None
    ):
        super(CategoryPage, self).__init__(parent)

        self.category_name = category_name
        self.tools_dict = tools_dict
        self.run_callback = run_callback

        self.title_label = ui_theme.make_title(category_name)
        self.subtitle_label = ui_theme.make_subtitle(
            _CATEGORY_DESCRIPTIONS.get(
                category_name,
                u"MuziTools 工具分类。"
            )
        )

        self.count_label = QLabel(
            u"{} 个工具".format(len(tools_dict))
        )
        ui_theme.set_role(self.count_label, "accent")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()
        self.card_layout = QGridLayout(self.scroll_content)
        self.card_layout.setContentsMargins(0, 0, 6, 0)
        self.card_layout.setHorizontalSpacing(10)
        self.card_layout.setVerticalSpacing(10)
        self.scroll_area.setWidget(self.scroll_content)

        self.create_cards()
        self.create_layouts()

    def create_cards(self):
        """创建工具 Card，默认两列布局。"""
        row = 0
        column = 0

        for tool_name in self.tools_dict:
            tool_function = self.tools_dict[tool_name]

            card = ToolCard(
                self.category_name,
                tool_name,
                tool_function,
                self.run_callback,
                self.scroll_content
            )

            self.card_layout.addWidget(
                card,
                row,
                column
            )

            column += 1

            if column >= 2:
                column = 0
                row += 1

        self.card_layout.setColumnStretch(0, 1)
        self.card_layout.setColumnStretch(1, 1)
        self.card_layout.setRowStretch(row + 1, 1)

    def create_layouts(self):
        """创建分类页面布局。"""
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(3)
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)

        header_layout.addLayout(title_layout, 1)
        header_layout.addWidget(
            self.count_label,
            0,
            Qt.AlignTop | Qt.AlignRight
        )

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.scroll_area, 1)


class RiggingToolbox(QWidget):
    """木子绑定工具盒主窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = get_maya_main_window()

        super(RiggingToolbox, self).__init__(parent)

        self.setWindowTitle(u"木子绑定工具盒")
        self.setWindowFlags(Qt.Window)
        self.setMinimumSize(720, 520)
        self.resize(860, 680)

        try:
            self.setAttribute(Qt.WA_DeleteOnClose, False)
        except Exception:
            pass

        self.tools_by_category = {}
        self.category_buttons = {}
        self.category_pages = {}
        self.current_category = None

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        ui_theme.style_window(self)
        self.rebuild_tools(refresh_registry=False)

    # -------------------------------------------------------------------------
    # UI 创建
    # -------------------------------------------------------------------------

    def create_widgets(self):
        """创建主界面控件。"""
        self.brand_label = ui_theme.make_title(u"MUZI")
        self.brand_label.setAlignment(Qt.AlignLeft)

        self.brand_subtitle_label = ui_theme.make_subtitle(
            u"Rigging Toolset"
        )

        self.version_label = QLabel(u"MAYA 2023+")
        ui_theme.set_role(self.version_label, "accent")

        self.nav_title_label = QLabel(u"工具分类")
        ui_theme.set_role(self.nav_title_label, "muted")

        self.refresh_button = QToolButton()
        self.refresh_button.setText(u"刷新工具")
        ui_theme.style_ghost(self.refresh_button)

        self.close_subtools_button = QToolButton()
        self.close_subtools_button.setText(u"关闭子工具")
        ui_theme.style_ghost(self.close_subtools_button)

        self.status_label = QLabel(u"准备就绪")
        ui_theme.set_role(self.status_label, "muted")

        self.page_stack = QStackedWidget()

        self.empty_page = QWidget()
        self.empty_title_label = ui_theme.make_title(u"没有发现工具")
        self.empty_message_label = ui_theme.make_subtitle(
            u"请检查 MuziTools/tools/<category>/*.py，"
            u"并确认工具文件包含 main()。"
        )

        empty_layout = QVBoxLayout(self.empty_page)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_layout.addStretch(1)
        empty_layout.addWidget(
            self.empty_title_label,
            0,
            Qt.AlignCenter
        )
        empty_layout.addWidget(
            self.empty_message_label,
            0,
            Qt.AlignCenter
        )
        empty_layout.addStretch(1)

    def create_layouts(self):
        """创建左侧导航 + 右侧内容区布局。"""
        self.sidebar = QFrame()
        ui_theme.set_role(self.sidebar, "surface")
        self.sidebar.setFixedWidth(190)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(14, 16, 14, 14)
        sidebar_layout.setSpacing(8)

        sidebar_layout.addWidget(self.brand_label)
        sidebar_layout.addWidget(self.brand_subtitle_label)
        sidebar_layout.addWidget(self.version_label)
        sidebar_layout.addSpacing(18)
        sidebar_layout.addWidget(self.nav_title_label)

        self.nav_buttons_layout = QVBoxLayout()
        self.nav_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_buttons_layout.setSpacing(4)
        sidebar_layout.addLayout(self.nav_buttons_layout)
        sidebar_layout.addStretch(1)

        sidebar_layout.addWidget(self.refresh_button)
        sidebar_layout.addWidget(self.close_subtools_button)
        sidebar_layout.addSpacing(4)
        sidebar_layout.addWidget(self.status_label)

        self.content_frame = QFrame()
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.page_stack)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_frame, 1)

    def create_connections(self):
        """连接主界面按钮。"""
        self.refresh_button.clicked.connect(
            self.refresh_tool_registry
        )
        self.close_subtools_button.clicked.connect(
            self.close_all_subtools
        )

    # -------------------------------------------------------------------------
    # 工具页面构建
    # -------------------------------------------------------------------------

    def clear_navigation(self):
        """删除旧分类导航按钮。"""
        while self.nav_buttons_layout.count():
            layout_item = self.nav_buttons_layout.takeAt(0)
            widget = layout_item.widget()

            if widget is None:
                continue

            widget.setParent(None)
            widget.deleteLater()

        self.category_buttons = {}

    def clear_pages(self):
        """删除旧分类页面。"""
        while self.page_stack.count():
            widget = self.page_stack.widget(0)
            self.page_stack.removeWidget(widget)
            widget.setParent(None)

            if widget is not self.empty_page:
                widget.deleteLater()

        self.category_pages = {}

    def create_category_button(self, category_name, tool_count):
        """创建一个左侧分类导航按钮。"""
        text = u"{}   {}".format(
            category_name,
            tool_count
        )

        button = QToolButton()
        button.setText(text)
        button.setCheckable(True)
        button.setToolButtonStyle(Qt.ToolButtonTextOnly)
        button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        button.setMinimumHeight(36)
        ui_theme.style_ghost(button)

        callback = partial(
            self.show_category,
            category_name
        )
        button.clicked.connect(callback)

        return button

    def rebuild_tools(self, refresh_registry=False):
        """重新读取工具注册表，并重建导航和页面。"""
        previous_category = self.current_category

        if refresh_registry:
            self.tools_by_category = refresh_tools()
        else:
            self.tools_by_category = get_tools_by_category()

        self.clear_navigation()
        self.clear_pages()
        self.current_category = None

        if not self.tools_by_category:
            self.page_stack.addWidget(self.empty_page)
            self.page_stack.setCurrentWidget(self.empty_page)
            self.status_label.setText(u"0 个工具")
            return

        total_tools = 0
        first_category = None

        for category_name in self.tools_by_category:
            tools_dict = self.tools_by_category[category_name]
            tool_count = len(tools_dict)
            total_tools += tool_count

            if first_category is None:
                first_category = category_name

            nav_button = self.create_category_button(
                category_name,
                tool_count
            )
            self.category_buttons[category_name] = nav_button
            self.nav_buttons_layout.addWidget(nav_button)

            page = CategoryPage(
                category_name,
                tools_dict,
                self.run_tool,
                self.page_stack
            )
            self.category_pages[category_name] = page
            self.page_stack.addWidget(page)

        self.status_label.setText(
            u"{} 个工具".format(total_tools)
        )

        category_to_show = first_category

        if previous_category in self.category_pages:
            category_to_show = previous_category

        if category_to_show is not None:
            self.show_category(category_to_show)

    def show_category(self, category_name, checked=False):
        """切换右侧工具分类页面。"""
        if category_name not in self.category_pages:
            return

        for button_category in self.category_buttons:
            button = self.category_buttons[button_category]
            should_check = button_category == category_name

            button.blockSignals(True)
            button.setChecked(should_check)
            button.blockSignals(False)
            ui_theme.repolish(button)

        page = self.category_pages[category_name]
        self.page_stack.setCurrentWidget(page)
        self.current_category = category_name

    # -------------------------------------------------------------------------
    # 操作
    # -------------------------------------------------------------------------

    def refresh_tool_registry(self, checked=False):
        """开发过程中重新扫描 tools 目录。"""
        self.rebuild_tools(refresh_registry=True)
        self.status_label.setText(u"工具列表已刷新")

    def close_all_subtools(self, checked=False):
        """关闭全部由 Window Manager 管理的子工具。"""
        window_manager.close_all_tools()
        self.status_label.setText(u"子工具已关闭")

    def run_tool(
            self,
            tool_key,
            tool_function,
            checked=False
    ):
        """安全执行一个工具 Runner。"""
        try:
            result = window_manager.show_tool(
                tool_key,
                tool_function
            )
            self.status_label.setText(
                u"已打开 {}".format(tool_key)
            )
            return result
        except Exception as error:
            print(
                u"\n[MuziTools] 工具打开失败：{}".format(tool_key)
            )
            traceback.print_exc()

            QMessageBox.critical(
                self,
                u"工具打开失败",
                u"{}\n\n{}".format(
                    tool_key,
                    error
                )
            )

            self.status_label.setText(u"工具打开失败")
            return None


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
