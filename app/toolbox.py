# coding=utf-8
u"""
Muzi Rigging Toolbox
====================

大型 Maya Rigging Toolset 的主应用窗口。

主窗口只负责：
    1. 分类浏览工具；
    2. 搜索当前分类中的工具；
    3. 区分 UI 工具和直接执行工具；
    4. 懒加载并启动工具；
    5. 统一管理子工具窗口；
    6. 刷新工具注册表。

具体绑定算法不放在这个文件中。
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
    from PySide2.QtWidgets import QLineEdit
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
    from PySide6.QtWidgets import QLineEdit
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

from .. import config
from ..ui import theme
from ..tools import get_tools_by_category
from ..tools import refresh_tools
from . import window_manager


_window = None

TOOL_MODE_UI = "ui"
TOOL_MODE_ACTION = "action"


tool_display_names = {
    "rename_tool": u"重命名工具",
    "attr_tool": u"属性工具",
    "connections_tool": u"连接工具",
    "constraint_tool": u"约束工具",
    "snap_tool": u"快速吸附",
    "jnt_tool": u"Jnt 工具",
    "jnt_resamp_tool": u"关节链重采样",
    "control_shape_tool": u"控制器 Shape 图库",
    "create_ctrl_tool": u"创建控制器",
    "create_fk_ctrl_tool": u"创建 FK 控制器",
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


tool_descriptions = {
    "rename_tool": u"批量命名、替换、前后缀与层级重命名。",
    "attr_tool": u"属性编辑、Channel Box 排序、锁定与隐藏。",
    "connections_tool": u"Transform、自定义属性与已有连接管理。",
    "constraint_tool": u"常用约束创建、查询和删除。",
    "snap_tool": u"按当前选择立即执行位置、旋转和矩阵吸附。",
    "jnt_tool": u"Jnt 创建、显示、镜像与常用骨骼操作。",
    "jnt_resamp_tool": u"在关节区间安全插入并重新分布 Jnt。",
    "control_shape_tool": u"浏览、替换、缩放、旋转与管理 Controller Shape。",
    "create_ctrl_tool": u"创建标准控制器层级、颜色、轴向与输出结构。",
    "create_fk_ctrl_tool": u"按当前选择顺序立即创建 FK Controller 链。",
    "face_rig_tool": u"完整 Face Rig 系统入口。",
    "rig_tool": u"FK、IK、PV、层级、约束等常用绑定操作。",
    "skirt_ctrl_tool": u"裙子定位曲线、Blueprint、Bind Jnt 与 FK 创建。",
    "face_select_key_tool": u"快速建立面部 Driven Key 驱动关系。",
    "skin_tool": u"SkinCluster、复制权重、权重文件与影响骨骼管理。",
    "add_blendshape_tool": u"BlendShape Target 查询、复制与管理。",
    "invert_shape_tool": u"基于 Maya invertShape 的修型反算工具。",
    "hierarchy_cleaner": u"安全清理层级、空组与可清理历史。",
    "model_checker": u"模型拓扑、命名、Transform 与历史检查。",
}


category_descriptions = {
    u"基础工具": u"命名、属性、连接、约束、吸附等通用 Maya 操作。",
    u"骨骼工具": u"Jnt 创建、编辑、镜像与关节链处理。",
    u"控制器工具": u"Controller 创建、Shape 图库与 FK Controller。",
    u"绑定工具": u"Rig、IK / FK、PV 与专项绑定工具。",
    u"面部工具": u"Face Rig 入口与 Driven Key 面部驱动。",
    u"蒙皮工具": u"SkinCluster、权重复制与权重文件管理。",
    u"BlendShape 工具": u"BlendShape Target 与修型反算。",
    u"检查与清理": u"模型检查、层级检查与安全场景清理。",
}


category_short_names = {
    u"基础工具": "BASIC",
    u"骨骼工具": __MUZI_MAYA_JNT_PROTECTED_00000__,
    u"控制器工具": "CONTROL",
    u"绑定工具": "RIG",
    u"面部工具": "FACE",
    u"蒙皮工具": "SKIN",
    u"BlendShape 工具": "SHAPE",
    u"检查与清理": "CLEAN",
}


def get_maya_main_window():
    u"""
    返回 Maya 主窗口 QWidget。

    Returns:
        QWidget | None:
        Maya 主窗口；无法获取时返回 None。
    """
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


def get_tool_display_name(tool_name):
    u"""
    返回工具显示名称。

    Args:
        tool_name (str):
            Tool Registry 中的工具模块名称。

    Returns:
        str:
        用于界面展示的工具名称。
    """
    if tool_name in tool_display_names:
        return tool_display_names[tool_name]

    words = tool_name.split("_")
    display_words = []

    for word in words:
        if not word:
            continue

        display_words.append(word.title())

    return " ".join(display_words)


def get_tool_description(tool_name):
    u"""
    返回工具说明。

    Args:
        tool_name (str):
            Tool Registry 中的工具模块名称。

    Returns:
        str:
        工具卡片使用的一行功能说明。
    """
    if tool_name in tool_descriptions:
        return tool_descriptions[tool_name]

    return u"运行 {} 模块。".format(tool_name)


def get_tool_mode(tool_function):
    u"""
    返回工具运行模式。

    Tool Registry 会把 `tool_mode` 写到懒加载 Runner 上。
    未声明时统一按照 UI 工具处理，保证旧工具继续可用。

    Args:
        tool_function (callable):
            Tool Registry 创建的懒加载 Runner。

    Returns:
        str:
        `ui` 或 `action`。
    """
    tool_mode = getattr(
        tool_function,
        "tool_mode",
        TOOL_MODE_UI
    )

    if tool_mode == TOOL_MODE_ACTION:
        return TOOL_MODE_ACTION

    return TOOL_MODE_UI


def get_tool_mode_display_name(tool_mode):
    u"""
    返回工具模式的中文显示名称。

    Args:
        tool_mode (str):
            Tool Registry 声明的运行模式。

    Returns:
        str:
        `界面工具` 或 `直接执行`。
    """
    if tool_mode == TOOL_MODE_ACTION:
        return u"直接执行"

    return u"界面工具"


class ToolCard(QFrame):
    """主工具箱右侧使用的单个工具卡片。"""

    def __init__(
        self,
        category_name,
        tool_name,
        tool_function,
        run_callback,
        parent=None
    ):
        u"""
        创建工具卡片。

        Args:
            category_name (str):
                当前工具所属分类。
            tool_name (str):
                工具模块名称。
            tool_function (callable):
                Tool Registry 的懒加载 Runner。
            run_callback (callable):
                用户点击卡片按钮时调用的主窗口回调。
            parent (QWidget | None):
                Qt 父对象。
        """
        # -------------------------------------------------------------------------
        # Step 01：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        super(ToolCard, self).__init__(parent)

        self.category_name = category_name
        self.tool_name = tool_name
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.tool_function = tool_function
        self.run_callback = run_callback

        self.display_name = get_tool_display_name(tool_name)
        self.description = get_tool_description(tool_name)
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.tool_mode = get_tool_mode(tool_function)
        self.search_visible = True

        theme.set_role(self, "card")
        self.setMinimumHeight(142)
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.create_widgets()
        self.create_layouts()
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.create_connections()

    def create_widgets(self):
        u"""
        创建工具卡片控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        short_name = category_short_names.get(
            self.category_name,
            "TOOL"
        )

        self.category_label = QLabel(short_name)
        theme.set_role(self.category_label, "pill")

        mode_text = "UI"

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if self.tool_mode == TOOL_MODE_ACTION:
            mode_text = "ACTION"

        self.mode_label = QLabel(mode_text)
        theme.set_role(self.mode_label, "pill")

        self.title_label = theme.make_section_title(
            self.display_name
        )

        self.description_label = QLabel(self.description)
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.description_label.setWordWrap(True)
        theme.set_role(self.description_label, "muted")

        self.module_label = QLabel(
            u"{}.py".format(self.tool_name)
        )
        theme.set_role(self.module_label, "muted")

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        button_text = u"打开"

        if self.tool_mode == TOOL_MODE_ACTION:
            button_text = u"执行"

        self.action_button = QPushButton(button_text)
        self.action_button.setMinimumWidth(76)
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.style_primary(self.action_button)

    def create_layouts(self):
        u"""
        创建工具卡片布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(7)

        top_layout = QHBoxLayout()
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(6)
        top_layout.addWidget(self.category_label)
        top_layout.addWidget(self.mode_label)
        top_layout.addStretch(1)

        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.description_label)
        main_layout.addStretch(1)

        bottom_layout = QHBoxLayout()
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.module_label)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.action_button)

        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addLayout(bottom_layout)

    def create_connections(self):
        u"""
        连接工具卡片信号。
        """
        tool_key = "{}/{}".format(
            self.category_name,
            self.tool_name
        )

        callback = partial(
            self.run_callback,
            tool_key,
            self.tool_function,
            self.tool_mode
        )

        self.action_button.clicked.connect(callback)

    def matches_search(self, search_text):
        u"""
        判断工具是否匹配搜索关键字。

        Args:
            search_text (str):
                当前分类搜索框中的文本。

        Returns:
            bool:
            是否显示当前卡片。
        """
        search_text = search_text.strip().lower()

        if not search_text:
            return True

        mode_search_text = get_tool_mode_display_name(
            self.tool_mode
        )

        values = [
            self.tool_name,
            self.display_name,
            self.description,
            self.category_name,
            self.tool_mode,
            mode_search_text,
        ]

        if self.tool_mode == TOOL_MODE_ACTION:
            values.append(u"执行")
        else:
            values.append(u"打开")

        for value in values:
            if search_text in value.lower():
                return True

        return False


class ToolSection(QWidget):
    """分类页面中的一组同类型工具。"""

    def __init__(
        self,
        title,
        description,
        parent=None
    ):
        u"""
        创建一个工具分区。

        Args:
            title (str):
                分区标题。
            description (str):
                分区说明。
            parent (QWidget | None):
                Qt 父对象。
        """
        # -------------------------------------------------------------------------
        # Step 01：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        super(ToolSection, self).__init__(parent)

        self.cards = []

        self.title_label = theme.make_section_title(title)
        self.description_label = QLabel(description)
        self.description_label.setWordWrap(True)
        theme.set_role(self.description_label, "muted")

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.count_label = QLabel()
        theme.set_role(self.count_label, "accent")

        self.card_widget = QWidget(self)
        self.card_layout = QGridLayout(self.card_widget)
        self.card_layout.setContentsMargins(0, 0, 6, 0)
        self.card_layout.setHorizontalSpacing(12)
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.card_layout.setVerticalSpacing(12)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(self.title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.count_label)

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(8)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.description_label)
        # -------------------------------------------------------------------------
        # Step 05：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        main_layout.addWidget(self.card_widget)

    def add_card(self, card):
        u"""
        把一张工具卡片加入当前分区。

        Args:
            card (ToolCard):
                要加入的卡片。
        """
        self.cards.append(card)

        card_index = len(self.cards) - 1
        row = card_index // 2
        column = card_index % 2

        self.card_layout.addWidget(
            card,
            row,
            column
        )

        self.card_layout.setColumnStretch(0, 1)
        self.card_layout.setColumnStretch(1, 1)

    def update_visibility(self):
        u"""
        根据搜索结果刷新分区可见性和数量。

        Returns:
            tuple[int, int]:
            当前可见数量和分区总数量。
        """
        total_count = len(self.cards)
        visible_count = 0

        for card in self.cards:
            if card.search_visible:
                visible_count += 1

        if visible_count == total_count:
            count_text = u"{} 个".format(total_count)
        else:
            count_text = u"{} / {} 个".format(
                visible_count,
                total_count
            )

        self.count_label.setText(count_text)
        self.setVisible(visible_count > 0)

        return visible_count, total_count


class CategoryPage(QWidget):
    """右侧的单个工具分类页面。"""

    def __init__(
        self,
        category_name,
        tools_dict,
        run_callback,
        parent=None
    ):
        u"""
        创建一个分类页面。

        Args:
            category_name (str):
                分类显示名称。
            tools_dict (dict):
                工具名到懒加载 Runner 的字典。
            run_callback (callable):
                卡片执行回调。
            parent (QWidget | None):
                Qt 父对象。
        """
        super(CategoryPage, self).__init__(parent)

        self.category_name = category_name
        self.tools_dict = tools_dict
        self.run_callback = run_callback
        self.tool_cards = []

        self.create_widgets()
        self.create_layouts()
        self.create_cards()

    def create_widgets(self):
        u"""
        创建分类页面控件。
        """
        self.title_label = theme.make_title(
            self.category_name
        )

        description = category_descriptions.get(
            self.category_name,
            u"Muzi Rigging 工具分类。"
        )

        self.subtitle_label = theme.make_subtitle(
            description
        )

        self.count_label = QLabel()
        theme.set_role(self.count_label, "accent")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.scroll_content = QWidget()

        self.ui_section = ToolSection(
            u"界面工具",
            u"点击「打开」进入独立工具界面，可继续调整参数和执行多步操作。",
            self.scroll_content
        )

        self.action_section = ToolSection(
            u"直接执行",
            u"点击「执行」立即使用当前 Maya 选择或场景状态运行一次操作。",
            self.scroll_content
        )

        self.scroll_area.setWidget(self.scroll_content)

    def create_layouts(self):
        u"""
        创建分类页面布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(3)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.subtitle_label)

        header_layout.addLayout(title_layout, 1)
        header_layout.addWidget(
            self.count_label,
            0,
            Qt.AlignTop | Qt.AlignRight
        )

        scroll_layout = QVBoxLayout(self.scroll_content)
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(22)
        scroll_layout.addWidget(self.ui_section)
        scroll_layout.addWidget(self.action_section)
        scroll_layout.addStretch(1)

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 22, 24, 22)
        main_layout.setSpacing(18)
        main_layout.addLayout(header_layout)
        # -------------------------------------------------------------------------
        # Step 05：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        main_layout.addWidget(self.scroll_area, 1)

    def create_cards(self):
        u"""
        创建当前分类中的工具卡片，并按照运行模式分组。
        """
        tool_names = []

        for tool_name in self.tools_dict:
            tool_names.append(tool_name)

        tool_names.sort()

        for tool_name in tool_names:
            tool_function = self.tools_dict[tool_name]

            card = ToolCard(
                self.category_name,
                tool_name,
                tool_function,
                self.run_callback,
                self.scroll_content
            )

            self.tool_cards.append(card)

            if card.tool_mode == TOOL_MODE_ACTION:
                self.action_section.add_card(card)
            else:
                self.ui_section.add_card(card)

        self.update_count_label()

    def update_count_label(self):
        u"""
        更新当前分类的工具数量。

        这里不再使用 QWidget.isVisible() 统计，因为页面尚未切换到前台时，
        Qt 会让子控件的 effective visible 状态为 False，导致初次显示错误地
        出现“0 个工具”。改为统计卡片自己的 search_visible 状态。
        """
        visible_ui_count, total_ui_count = (
            self.ui_section.update_visibility()
        )
        visible_action_count, total_action_count = (
            self.action_section.update_visibility()
        )

        visible_count = (
            visible_ui_count
            + visible_action_count
        )
        total_count = (
            total_ui_count
            + total_action_count
        )

        if visible_count == total_count:
            count_text = (
                u"{} 个工具 · 界面 {} · 执行 {}"
            ).format(
                total_count,
                total_ui_count,
                total_action_count
            )
        else:
            count_text = (
                u"{} / {} 个工具 · 界面 {} · 执行 {}"
            ).format(
                visible_count,
                total_count,
                visible_ui_count,
                visible_action_count
            )

        self.count_label.setText(count_text)

    def filter_tools(self, search_text):
        u"""
        按照关键字过滤当前分类的工具卡片。

        Args:
            search_text (str):
                当前分类搜索文本。
        """
        for card in self.tool_cards:
            visible = card.matches_search(search_text)
            card.search_visible = visible
            card.setVisible(visible)

        self.update_count_label()

    def get_tool_counts(self):
        u"""
        返回当前分类的工具数量。

        Returns:
            dict:
            `total`、`ui`、`action` 三类数量。
        """
        ui_count = len(self.ui_section.cards)
        action_count = len(self.action_section.cards)

        return {
            "total": ui_count + action_count,
            "ui": ui_count,
            "action": action_count,
        }


class RiggingToolbox(QWidget):
    """木子大型绑定工具集主窗口。"""

    def __init__(self, parent=None):
        u"""
        创建木子绑定工具集主窗口。

        Args:
            parent (QWidget | None):
                Qt 父对象；默认使用 Maya 主窗口。
        """
        if parent is None:
            parent = get_maya_main_window()

        super(RiggingToolbox, self).__init__(parent)

        self.setWindowTitle(u"木子绑定工具集")
        self.setWindowFlags(Qt.Window)
        self.setMinimumSize(780, 560)
        self.resize(980, 720)

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

        theme.style_window(self)
        self.rebuild_tools(refresh_registry=False)

    def create_widgets(self):
        u"""
        创建主工具箱控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.sidebar = QFrame()
        theme.set_role(self.sidebar, "sidebar")
        self.sidebar.setFixedWidth(190)

        self.brand_label = theme.make_title(u"MUZI")
        self.brand_subtitle_label = theme.make_subtitle(
            u"Rigging Toolset"
        )

        self.version_label = QLabel(
            u"v{} · Maya 2023+".format(config.version)
        )
        theme.set_role(self.version_label, "muted")

        self.nav_title_label = QLabel(u"工具分类")
        theme.set_role(self.nav_title_label, "muted")

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.navigation_widget = QWidget()
        self.navigation_layout = QVBoxLayout(
            self.navigation_widget
        )
        self.navigation_layout.setContentsMargins(0, 0, 0, 0)
        self.navigation_layout.setSpacing(3)

        self.refresh_button = QToolButton()
        self.refresh_button.setText(u"刷新工具")
        theme.style_ghost(self.refresh_button)

        self.close_subtools_button = QToolButton()
        self.close_subtools_button.setText(u"关闭子工具")
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.style_ghost(self.close_subtools_button)

        self.content_frame = QFrame()
        theme.set_role(self.content_frame, "surface")

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(
            u"搜索当前分类中的工具..."
        )
        self.search_edit.setClearButtonEnabled(True)
        theme.style_search(self.search_edit)

        self.page_stack = QStackedWidget()

        self.status_label = QLabel(u"准备就绪")
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(self.status_label, "muted")

        self.empty_page = QWidget()
        self.empty_title_label = theme.make_title(
            u"没有发现工具"
        )
        self.empty_message_label = theme.make_subtitle(
            u"请检查 tools/<category>/*.py，并确认工具文件提供 main()。"
        )

        empty_layout = QVBoxLayout(self.empty_page)
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
        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        empty_layout.addStretch(1)

    def create_layouts(self):
        u"""
        创建左侧导航和右侧内容布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(16, 22, 16, 16)
        sidebar_layout.setSpacing(8)

        sidebar_layout.addWidget(self.brand_label)
        sidebar_layout.addWidget(self.brand_subtitle_label)
        sidebar_layout.addWidget(self.version_label)
        sidebar_layout.addSpacing(22)
        sidebar_layout.addWidget(self.nav_title_label)
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        sidebar_layout.addWidget(self.navigation_widget)
        sidebar_layout.addStretch(1)
        sidebar_layout.addWidget(self.refresh_button)
        sidebar_layout.addWidget(self.close_subtools_button)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar_layout.addStretch(1)
        top_bar_layout.addWidget(self.search_edit, 0)

        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.search_edit.setMinimumWidth(280)
        self.search_edit.setMaximumWidth(420)

        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 14, 0, 10)
        content_layout.setSpacing(8)
        content_layout.addLayout(top_bar_layout)
        content_layout.addWidget(self.page_stack, 1)

        status_layout = QHBoxLayout()
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        status_layout.setContentsMargins(24, 0, 24, 0)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch(1)

        content_layout.addLayout(status_layout)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.sidebar)
        # -------------------------------------------------------------------------
        # Step 05：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        main_layout.addWidget(self.content_frame, 1)

    def create_connections(self):
        u"""
        连接主窗口信号。
        """
        self.refresh_button.clicked.connect(
            self.refresh_tool_registry
        )
        self.close_subtools_button.clicked.connect(
            self.close_all_subtools
        )
        self.search_edit.textChanged.connect(
            self.filter_current_page
        )

    def clear_navigation(self):
        u"""
        清理旧分类按钮。
        """
        while self.navigation_layout.count():
            item = self.navigation_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self.category_buttons = {}

    def clear_pages(self):
        u"""
        清理旧分类页面。
        """
        while self.page_stack.count():
            widget = self.page_stack.widget(0)
            self.page_stack.removeWidget(widget)
            widget.deleteLater()

        self.category_pages = {}

    def rebuild_tools(self, refresh_registry=False):
        u"""
        重新构建左侧分类和右侧页面。

        Args:
            refresh_registry (bool):
                是否重新扫描 Tool Registry。
        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if refresh_registry:
            self.tools_by_category = refresh_tools()
        else:
            self.tools_by_category = get_tools_by_category()

        self.search_edit.clear()
        self.clear_navigation()
        # -------------------------------------------------------------------------
        # Step 02：清理当前阶段不再需要的数据或场景状态
        # -------------------------------------------------------------------------
        self.clear_pages()

        if not self.tools_by_category:
            self.page_stack.addWidget(self.empty_page)
            self.page_stack.setCurrentWidget(self.empty_page)
            self.status_label.setText(u"没有发现可用工具")
            return

        category_names = []

        for category_name in self.tools_by_category:
            category_names.append(category_name)

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        first_category = None

        for category_name in category_names:
            tools_dict = self.tools_by_category[category_name]

            nav_button = QPushButton(category_name)
            nav_button.setCheckable(True)
            theme.style_navigation(nav_button)

            callback = partial(
                self.select_category,
                category_name
            )
            nav_button.clicked.connect(callback)

            self.navigation_layout.addWidget(nav_button)
            self.category_buttons[category_name] = nav_button

            page = CategoryPage(
                category_name,
                tools_dict,
                self.run_tool,
                self.page_stack
            )
            self.page_stack.addWidget(page)
            self.category_pages[category_name] = page

            if first_category is None:
                first_category = category_name

        self.navigation_layout.addStretch(1)

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if first_category is not None:
            self.select_category(first_category)

        total_tool_count = 0

        for category_name in self.tools_by_category:
            category_tools = self.tools_by_category[category_name]
            total_tool_count += len(category_tools)

        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"已发现 {} 个工具分类，共 {} 个工具".format(
                len(category_names),
                total_tool_count
            )
        )

    def select_category(self, category_name):
        u"""
        切换当前工具分类。

        Args:
            category_name (str):
                要显示的分类名称。
        """
        if category_name not in self.category_pages:
            return

        self.current_category = category_name

        for button_category in self.category_buttons:
            button = self.category_buttons[button_category]
            active = button_category == category_name

            button.setChecked(active)
            theme.style_navigation(
                button,
                active=active
            )

        page = self.category_pages[category_name]
        self.page_stack.setCurrentWidget(page)

        self.search_edit.clear()

        counts = page.get_tool_counts()

        self.status_label.setText(
            u"{} · {} 个工具（界面 {} / 执行 {}）".format(
                category_descriptions.get(
                    category_name,
                    category_name
                ),
                counts["total"],
                counts["ui"],
                counts["action"]
            )
        )

    def filter_current_page(self, search_text):
        u"""
        过滤当前分类的工具卡片。

        Args:
            search_text (str):
                当前搜索文本。
        """
        if self.current_category is None:
            return

        page = self.category_pages.get(
            self.current_category
        )

        if page is None:
            return

        page.filter_tools(search_text)

    def run_tool(
        self,
        tool_key,
        tool_function,
        tool_mode=TOOL_MODE_UI
    ):
        u"""
        打开 UI 工具或直接执行命令型工具。

        Args:
            tool_key (str):
                Tool Registry 中唯一识别工具的 Key。
            tool_function (callable):
                Tool Registry 的懒加载 Runner。
            tool_mode (str):
                `ui` 表示打开界面，`action` 表示立即执行。

        Returns:
            object | None:
            工具 main() 的返回值。
        """
        if tool_mode == TOOL_MODE_ACTION:
            return self.execute_action_tool(
                tool_key,
                tool_function
            )

        return self.open_ui_tool(
            tool_key,
            tool_function
        )

    def open_ui_tool(self, tool_key, tool_function):
        u"""
        通过 Window Manager 打开一个 UI 工具。

        Args:
            tool_key (str):
                工具唯一 Key。
            tool_function (callable):
                Tool Registry 的懒加载 Runner。

        Returns:
            object | None:
            工具窗口或 main() 返回值。
        """
        self.status_label.setText(
            u"正在打开 {}...".format(tool_key)
        )

        try:
            result = window_manager.show_tool(
                tool_key,
                tool_function
            )
        except Exception as error:
            traceback.print_exc()

            self.status_label.setText(
                u"打开失败：{}".format(tool_key)
            )

            QMessageBox.critical(
                self,
                u"工具启动失败",
                u"无法打开：{}\n\n{}".format(
                    tool_key,
                    error
                )
            )
            return None

        self.status_label.setText(
            u"已打开：{}".format(tool_key)
        )
        return result

    def execute_action_tool(self, tool_key, tool_function):
        u"""
        直接执行一个没有独立 UI 的工具。

        Args:
            tool_key (str):
                工具唯一 Key。
            tool_function (callable):
                Tool Registry 的懒加载 Runner。

        Returns:
            object | None:
            工具 main() 返回值。
        """
        self.status_label.setText(
            u"正在执行 {}...".format(tool_key)
        )

        try:
            result = tool_function()
        except Exception as error:
            traceback.print_exc()

            self.status_label.setText(
                u"执行失败：{}".format(tool_key)
            )

            QMessageBox.critical(
                self,
                u"工具执行失败",
                u"无法执行：{}\n\n{}".format(
                    tool_key,
                    error
                )
            )
            return None

        self.status_label.setText(
            u"执行完成：{}".format(tool_key)
        )
        return result

    def refresh_tool_registry(self):
        u"""
        重新扫描工具目录并刷新界面。
        """
        try:
            self.rebuild_tools(refresh_registry=True)
        except Exception as error:
            traceback.print_exc()

            QMessageBox.critical(
                self,
                u"刷新失败",
                u"重新扫描工具目录失败：\n{}".format(error)
            )

    def close_all_subtools(self):
        u"""
        关闭所有由主工具箱管理的 UI 子工具。
        """
        window_manager.close_all_tools()
        self.status_label.setText(u"已关闭全部子工具")


def main():
    u"""
    创建或恢复主工具箱。

    Returns:
        RiggingToolbox:
        主工具箱实例。
    """
    global _window

    if _window is not None:
        try:
            _window.showNormal()
            _window.raise_()
            _window.activateWindow()
            return _window
        except Exception:
            _window = None

    _window = RiggingToolbox()
    _window.show()
    _window.raise_()
    _window.activateWindow()
    return _window


if __name__ == "__main__":
    main()
