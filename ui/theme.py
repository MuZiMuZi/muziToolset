# coding=utf-8
u"""
MuziTools UI Theme
==================

Maya 2023 / PySide2 统一视觉系统。

当前设计方向参考网易云音乐电脑版的桌面端布局语言：
    - 浅灰色应用背景；
    - 白色主内容区域和卡片；
    - 左侧固定导航栏；
    - 红色作为唯一主要强调色；
    - 大量留白和轻量分割线；
    - 搜索框、导航、按钮都采用柔和圆角；
    - Hover 变化轻，不做厚重阴影；
    - 保持 Maya 工具窗口需要的紧凑信息密度。

说明：
    这里只参考布局和视觉语言，不复制网易云音乐的品牌素材、Logo 或图标。
    所有控件仍然使用 PySide2 / PySide6 原生组件，保证 Maya 中稳定运行。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QVBoxLayout
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QVBoxLayout


# =============================================================================
# Theme Tokens
# =============================================================================
background = "#F5F5F7"
background_alt = "#F0F1F3"
sidebar_background = "#F7F7F9"
surface = "#FFFFFF"
surface_alt = "#FAFAFB"
surface_hover = "#F3F3F5"
surface_pressed = "#ECECEF"

border = "#E4E5E8"
border_soft = "#ECEDEF"
border_focus = "#EC4141"

text = "#1F2024"
text_secondary = "#55575F"
text_muted = "#8A8D96"
text_disabled = "#B8BBC2"

accent = "#EC4141"
accent_hover = "#F05252"
accent_pressed = "#D93636"
accent_soft = "#FFF0F0"
accent_soft_hover = "#FFE4E4"

success = "#31A66A"
warning = "#D58A2D"
danger = "#D94C4C"
info = "#4D87D8"

radius_small = 6
radius = 9
radius_large = 12


# =============================================================================
# Global Style Sheet
# =============================================================================
def _build_style_sheet():
    """生成 MuziTools 全局 QSS。"""

    return u"""
/* -------------------------------------------------------------------------
   Base
   ------------------------------------------------------------------------- */
QWidget {
    background-color: %(background)s;
    color: %(text)s;
    font-family: "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei";
    font-size: 12px;
    selection-background-color: %(accent)s;
    selection-color: #FFFFFF;
}

QWidget[muziSurface="true"],
QFrame[muziSurface="true"] {
    background-color: %(surface)s;
    border: 1px solid %(border_soft)s;
    border-radius: %(radius_large)dpx;
}

QWidget[muziSidebar="true"],
QFrame[muziSidebar="true"] {
    background-color: %(sidebar_background)s;
    border: none;
    border-right: 1px solid %(border)s;
}

QWidget[muziCard="true"],
QFrame[muziCard="true"] {
    background-color: %(surface)s;
    border: 1px solid %(border_soft)s;
    border-radius: %(radius_large)dpx;
}

QWidget[muziSubCard="true"],
QFrame[muziSubCard="true"] {
    background-color: %(surface_alt)s;
    border: 1px solid %(border_soft)s;
    border-radius: %(radius)dpx;
}

/* -------------------------------------------------------------------------
   Text
   ------------------------------------------------------------------------- */
QLabel {
    background: transparent;
    border: none;
    color: %(text_secondary)s;
}

QLabel[muziTitle="true"] {
    color: %(text)s;
    font-size: 20px;
    font-weight: 700;
}

QLabel[muziSubtitle="true"] {
    color: %(text_muted)s;
    font-size: 12px;
}

QLabel[muziSectionTitle="true"] {
    color: %(text)s;
    font-size: 14px;
    font-weight: 600;
}

QLabel[muziMuted="true"] {
    color: %(text_muted)s;
}

QLabel[muziAccent="true"] {
    color: %(accent)s;
    font-weight: 600;
}

QLabel[muziPill="true"] {
    padding: 3px 8px;
    background-color: %(accent_soft)s;
    color: %(accent)s;
    border: 1px solid #FFDADA;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
}

/* -------------------------------------------------------------------------
   Push Buttons
   ------------------------------------------------------------------------- */
QPushButton,
QToolButton {
    min-height: 30px;
    padding: 0px 12px;
    background-color: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius_small)dpx;
}

QPushButton:hover,
QToolButton:hover {
    background-color: %(surface_hover)s;
    border-color: #D6D8DC;
}

QPushButton:pressed,
QToolButton:pressed {
    background-color: %(surface_pressed)s;
    border-color: #C8CAD0;
}

QPushButton:checked,
QToolButton:checked {
    background-color: %(accent_soft)s;
    border-color: #FFCACA;
    color: %(accent)s;
}

QPushButton:disabled,
QToolButton:disabled {
    background-color: %(background_alt)s;
    border-color: %(border_soft)s;
    color: %(text_disabled)s;
}

QPushButton[muziPrimary="true"],
QToolButton[muziPrimary="true"] {
    background-color: %(accent)s;
    color: #FFFFFF;
    border: 1px solid %(accent)s;
    font-weight: 600;
}

QPushButton[muziPrimary="true"]:hover,
QToolButton[muziPrimary="true"]:hover {
    background-color: %(accent_hover)s;
    border-color: %(accent_hover)s;
}

QPushButton[muziPrimary="true"]:pressed,
QToolButton[muziPrimary="true"]:pressed {
    background-color: %(accent_pressed)s;
    border-color: %(accent_pressed)s;
}

QPushButton[muziDanger="true"] {
    background-color: #FFF4F4;
    border-color: #FFD9D9;
    color: %(danger)s;
}

QPushButton[muziDanger="true"]:hover {
    background-color: #FFEAEA;
    border-color: #FFBEBE;
}

QPushButton[muziGhost="true"],
QToolButton[muziGhost="true"] {
    background-color: transparent;
    border-color: transparent;
    color: %(text_secondary)s;
}

QPushButton[muziGhost="true"]:hover,
QToolButton[muziGhost="true"]:hover {
    background-color: %(surface_hover)s;
    border-color: transparent;
    color: %(text)s;
}

QPushButton[muziNav="true"] {
    min-height: 34px;
    padding-left: 14px;
    padding-right: 12px;
    text-align: left;
    background-color: transparent;
    border: none;
    color: %(text_secondary)s;
    border-radius: %(radius_small)dpx;
}

QPushButton[muziNav="true"]:hover {
    background-color: #ECEDEF;
    color: %(text)s;
}

QPushButton[muziNav="true"]:checked,
QPushButton[muziNavActive="true"] {
    background-color: %(accent_soft)s;
    color: %(accent)s;
    border: none;
    font-weight: 600;
}

/* -------------------------------------------------------------------------
   Editors
   ------------------------------------------------------------------------- */
QLineEdit,
QTextEdit,
QPlainTextEdit,
QSpinBox,
QDoubleSpinBox,
QComboBox,
QDateEdit,
QTimeEdit,
QDateTimeEdit {
    min-height: 30px;
    padding: 0px 9px;
    background-color: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius_small)dpx;
}

QTextEdit,
QPlainTextEdit {
    padding: 8px;
}

QLineEdit[muziSearch="true"] {
    min-height: 32px;
    padding-left: 14px;
    padding-right: 14px;
    background-color: #F0F1F3;
    border: 1px solid #F0F1F3;
    border-radius: 16px;
}

QLineEdit[muziSearch="true"]:hover {
    background-color: #ECEDEF;
    border-color: #E4E5E8;
}

QLineEdit[muziSearch="true"]:focus {
    background-color: %(surface)s;
    border: 1px solid #FFBDBD;
}

QLineEdit:hover,
QTextEdit:hover,
QPlainTextEdit:hover,
QSpinBox:hover,
QDoubleSpinBox:hover,
QComboBox:hover,
QDateEdit:hover,
QTimeEdit:hover,
QDateTimeEdit:hover {
    border-color: #D3D5D9;
}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QSpinBox:focus,
QDoubleSpinBox:focus,
QComboBox:focus,
QDateEdit:focus,
QTimeEdit:focus,
QDateTimeEdit:focus {
    border: 1px solid %(border_focus)s;
    background-color: %(surface)s;
}

QLineEdit:read-only,
QTextEdit:read-only,
QPlainTextEdit:read-only {
    color: %(text_muted)s;
    background-color: %(surface_alt)s;
}

QComboBox::drop-down,
QSpinBox::up-button,
QSpinBox::down-button,
QDoubleSpinBox::up-button,
QDoubleSpinBox::down-button {
    border: none;
    background: transparent;
}

QComboBox QAbstractItemView {
    background-color: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius_small)dpx;
    selection-background-color: %(accent_soft)s;
    selection-color: %(accent)s;
    outline: none;
    padding: 4px;
}

/* -------------------------------------------------------------------------
   Check / Radio
   ------------------------------------------------------------------------- */
QCheckBox,
QRadioButton {
    spacing: 7px;
    color: %(text_secondary)s;
    background: transparent;
}

QCheckBox:hover,
QRadioButton:hover {
    color: %(text)s;
}

QCheckBox::indicator,
QRadioButton::indicator {
    width: 15px;
    height: 15px;
}

QCheckBox::indicator:unchecked {
    background-color: %(surface)s;
    border: 1px solid #C8CBD0;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: %(accent)s;
    border: 1px solid %(accent)s;
    border-radius: 4px;
}

QRadioButton::indicator:unchecked {
    background-color: %(surface)s;
    border: 1px solid #C8CBD0;
    border-radius: 8px;
}

QRadioButton::indicator:checked {
    background-color: %(accent)s;
    border: 4px solid %(surface)s;
    border-radius: 8px;
}

/* -------------------------------------------------------------------------
   Group / Tab
   ------------------------------------------------------------------------- */
QGroupBox {
    margin-top: 12px;
    padding: 12px 10px 10px 10px;
    background-color: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border_soft)s;
    border-radius: %(radius_large)dpx;
    font-weight: 600;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0px 5px;
    color: %(text)s;
    background-color: %(surface)s;
}

QTabWidget::pane {
    border: 1px solid %(border_soft)s;
    border-radius: %(radius)dpx;
    background-color: %(surface)s;
    top: -1px;
}

QTabBar::tab {
    min-height: 30px;
    padding: 0px 14px;
    margin-right: 4px;
    background-color: transparent;
    color: %(text_muted)s;
    border: none;
    border-bottom: 2px solid transparent;
}

QTabBar::tab:hover {
    color: %(text)s;
}

QTabBar::tab:selected {
    color: %(text)s;
    border-bottom: 2px solid %(accent)s;
    font-weight: 600;
}

/* -------------------------------------------------------------------------
   Item Views
   ------------------------------------------------------------------------- */
QListWidget,
QTreeWidget,
QTableWidget,
QTableView,
QTreeView,
QListView {
    background-color: %(surface)s;
    alternate-background-color: %(surface_alt)s;
    color: %(text_secondary)s;
    border: 1px solid %(border_soft)s;
    border-radius: %(radius)dpx;
    outline: none;
    gridline-color: %(border_soft)s;
}

QListWidget::item,
QTreeWidget::item,
QListView::item,
QTreeView::item {
    min-height: 28px;
    padding: 4px 7px;
    border-radius: 6px;
}

QListWidget::item:hover,
QTreeWidget::item:hover,
QListView::item:hover,
QTreeView::item:hover {
    background-color: %(surface_hover)s;
    color: %(text)s;
}

QListWidget::item:selected,
QTreeWidget::item:selected,
QListView::item:selected,
QTreeView::item:selected,
QTableWidget::item:selected,
QTableView::item:selected {
    background-color: %(accent_soft)s;
    color: %(accent)s;
}

QHeaderView::section {
    min-height: 28px;
    padding: 0px 8px;
    background-color: %(surface_alt)s;
    color: %(text_secondary)s;
    border: none;
    border-right: 1px solid %(border_soft)s;
    border-bottom: 1px solid %(border_soft)s;
    font-weight: 600;
}

QTableCornerButton::section {
    background-color: %(surface_alt)s;
    border: none;
}

/* -------------------------------------------------------------------------
   Scroll Area / Scroll Bar
   ------------------------------------------------------------------------- */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    width: 8px;
    margin: 2px;
    background: transparent;
}

QScrollBar::handle:vertical {
    min-height: 30px;
    background-color: #C7C9CE;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #AEB1B7;
}

QScrollBar:horizontal {
    height: 8px;
    margin: 2px;
    background: transparent;
}

QScrollBar::handle:horizontal {
    min-width: 30px;
    background-color: #C7C9CE;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #AEB1B7;
}

QScrollBar::add-line,
QScrollBar::sub-line,
QScrollBar::add-page,
QScrollBar::sub-page {
    background: transparent;
    border: none;
}

/* -------------------------------------------------------------------------
   Slider / Progress
   ------------------------------------------------------------------------- */
QSlider::groove:horizontal {
    height: 4px;
    background-color: #E5E6E9;
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background-color: %(accent)s;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    width: 14px;
    height: 14px;
    margin: -5px 0px;
    background-color: #FFFFFF;
    border: 2px solid %(accent)s;
    border-radius: 7px;
}

QProgressBar {
    min-height: 6px;
    max-height: 6px;
    background-color: #E5E6E9;
    border: none;
    border-radius: 3px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background-color: %(accent)s;
    border-radius: 3px;
}

/* -------------------------------------------------------------------------
   Menu / Tooltip
   ------------------------------------------------------------------------- */
QMenu {
    padding: 6px;
    background-color: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius)dpx;
}

QMenu::item {
    min-height: 26px;
    padding: 2px 24px 2px 10px;
    border-radius: 5px;
}

QMenu::item:selected {
    background-color: %(surface_hover)s;
}

QMenu::separator {
    height: 1px;
    margin: 5px 8px;
    background-color: %(border_soft)s;
}

QToolTip {
    padding: 6px 9px;
    background-color: #2F3136;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
}
""" % {
        "background": background,
        "background_alt": background_alt,
        "sidebar_background": sidebar_background,
        "surface": surface,
        "surface_alt": surface_alt,
        "surface_hover": surface_hover,
        "surface_pressed": surface_pressed,
        "border": border,
        "border_soft": border_soft,
        "border_focus": border_focus,
        "text": text,
        "text_secondary": text_secondary,
        "text_muted": text_muted,
        "text_disabled": text_disabled,
        "accent": accent,
        "accent_hover": accent_hover,
        "accent_pressed": accent_pressed,
        "accent_soft": accent_soft,
        "accent_soft_hover": accent_soft_hover,
        "danger": danger,
        "radius_small": radius_small,
        "radius": radius,
        "radius_large": radius_large,
    }


style_sheet = _build_style_sheet()


# =============================================================================
# Helpers
# =============================================================================
def repolish(widget):
    u"""
    动态属性变化后重新刷新 QSS。

    Args:
        widget (object):
            `widget` 对应的输入数据。
    """

    if widget is None:
        return

    style = widget.style()

    if style is None:
        return

    style.unpolish(widget)
    style.polish(widget)
    widget.update()


def set_role(widget, role, enabled=True):
    u"""
    给 QWidget 设置 MuziTools 视觉角色。

    Args:
        widget (object):
            `widget` 对应的输入数据。
        role (object):
            `role` 对应的输入数据。
        enabled (bool):
            是否启用 `enabled` 对应的处理。

    Returns:
        object:
            方法执行后的结果数据。
    """

    if widget is None:
        return widget

    property_name = {
        "surface": "muziSurface",
        "sidebar": "muziSidebar",
        "card": "muziCard",
        "sub_card": "muziSubCard",
        "title": "muziTitle",
        "subtitle": "muziSubtitle",
        "section_title": "muziSectionTitle",
        "muted": "muziMuted",
        "accent": "muziAccent",
        "pill": "muziPill",
        "primary": "muziPrimary",
        "danger": "muziDanger",
        "ghost": "muziGhost",
        "nav": "muziNav",
        "nav_active": "muziNavActive",
        "search": "muziSearch",
    }.get(role)

    if property_name is None:
        return widget

    widget.setProperty(property_name, bool(enabled))
    repolish(widget)
    return widget


def apply_theme(widget):
    u"""
    把统一主题应用到一个窗口。

    Args:
        widget (object):
            `widget` 对应的输入数据。

    Returns:
        object | None:
            方法执行后的结果数据。
    """

    if widget is None:
        return None

    try:
        widget.setStyleSheet(style_sheet)
    except Exception:
        return widget

    return widget


def make_title(text_value, parent=None):
    u"""
    执行 `make_title` 对应的 Maya 工具操作。

    Args:
        text_value (object):
            `text_value` 对应的输入数据。
        parent (str):
            父级 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """

    label = QLabel(text_value, parent)
    set_role(label, "title")
    return label


def make_subtitle(text_value, parent=None):
    u"""
    执行 `make_subtitle` 对应的 Maya 工具操作。

    Args:
        text_value (object):
            `text_value` 对应的输入数据。
        parent (str):
            父级 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """

    label = QLabel(text_value, parent)
    set_role(label, "subtitle")
    label.setWordWrap(True)
    return label


def make_section_title(text_value, parent=None):
    u"""
    执行 `make_section_title` 对应的 Maya 工具操作。

    Args:
        text_value (object):
            `text_value` 对应的输入数据。
        parent (str):
            父级 Maya 节点名称。

    Returns:
        object:
            方法执行后的结果数据。
    """

    label = QLabel(text_value, parent)
    set_role(label, "section_title")
    return label


def make_card(parent=None, margins=(16, 14, 16, 14), spacing=8):
    u"""
    创建标准白色内容卡片。

    Args:
        parent (str):
            父级 Maya 节点名称。
        margins (tuple):
            `margins` 对应的输入数据。
        spacing (int):
            `spacing` 对应的整数参数。

    Returns:
        tuple:
            方法执行后的结果数据。
    """

    card = QFrame(parent)
    set_role(card, "card")

    layout = QVBoxLayout(card)
    layout.setContentsMargins(
        margins[0],
        margins[1],
        margins[2],
        margins[3]
    )
    layout.setSpacing(spacing)

    return card, layout


def make_sub_card(parent=None, margins=(12, 10, 12, 10), spacing=6):
    u"""
    创建次级浅灰卡片。

    Args:
        parent (str):
            父级 Maya 节点名称。
        margins (tuple):
            `margins` 对应的输入数据。
        spacing (int):
            `spacing` 对应的整数参数。

    Returns:
        tuple:
            方法执行后的结果数据。
    """

    card = QFrame(parent)
    set_role(card, "sub_card")

    layout = QVBoxLayout(card)
    layout.setContentsMargins(
        margins[0],
        margins[1],
        margins[2],
        margins[3]
    )
    layout.setSpacing(spacing)

    return card, layout


def style_primary(button):
    u"""
    执行 `style_primary` 对应的 Maya 工具操作。

    Args:
        button (object):
            `button` 对应的输入数据。

    Returns:
        object:
            方法执行后的结果数据。
    """

    return set_role(button, "primary")


def style_danger(button):
    u"""
    执行 `style_danger` 对应的 Maya 工具操作。

    Args:
        button (object):
            `button` 对应的输入数据。

    Returns:
        object:
            方法执行后的结果数据。
    """

    return set_role(button, "danger")


def style_ghost(button):
    u"""
    执行 `style_ghost` 对应的 Maya 工具操作。

    Args:
        button (object):
            `button` 对应的输入数据。

    Returns:
        object:
            方法执行后的结果数据。
    """

    return set_role(button, "ghost")


def style_navigation(button, active=False):
    u"""
    执行 `style_navigation` 对应的 Maya 工具操作。

    Args:
        button (object):
            `button` 对应的输入数据。
        active (bool):
            是否启用 `active` 对应的处理。

    Returns:
        object:
            方法执行后的结果数据。
    """

    set_role(button, "nav")
    set_role(button, "nav_active", active)
    return button


def style_search(line_edit):
    u"""
    执行 `style_search` 对应的 Maya 工具操作。

    Args:
        line_edit (object):
            `line_edit` 对应的输入数据。

    Returns:
        object:
            方法执行后的结果数据。
    """

    return set_role(line_edit, "search")


def style_window(widget, title=None, minimum_width=None):
    u"""
    统一设置窗口标题、最小宽度和主题。

    Args:
        widget (object):
            `widget` 对应的输入数据。
        title (object):
            `title` 对应的输入数据。
        minimum_width (object):
            `minimum_width` 对应的输入数据。

    Returns:
        object | None:
            方法执行后的结果数据。
    """

    if widget is None:
        return None

    if title:
        widget.setWindowTitle(title)

    if minimum_width is not None:
        widget.setMinimumWidth(minimum_width)

    apply_theme(widget)

    try:
        widget.setAttribute(Qt.WA_StyledBackground, True)
    except Exception:
        pass

    return widget


__all__ = [
    "background",
    "background_alt",
    "sidebar_background",
    "surface",
    "surface_alt",
    "border",
    "text",
    "text_secondary",
    "text_muted",
    "accent",
    "success",
    "warning",
    "danger",
    "info",
    "style_sheet",
    "apply_theme",
    "repolish",
    "set_role",
    "make_title",
    "make_subtitle",
    "make_section_title",
    "make_card",
    "make_sub_card",
    "style_primary",
    "style_danger",
    "style_ghost",
    "style_navigation",
    "style_search",
    "style_window",
]
