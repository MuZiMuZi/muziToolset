# coding=utf-8
u"""
MuziTools UI Theme
==================

Maya 2023 / PySide2 统一视觉系统。

设计方向：
    - 参考 Arc Browser 的 clean / calm / sidebar-first 信息组织；
    - 使用柔和背景、轻量边框、浮层式卡片和明确内容层级；
    - 主操作清晰，次级操作可见但不过度抢占注意力；
    - 保留 MuziTools 自己的品牌和 Maya 工作流，不复制 Arc Logo、图标或品牌资产；
    - 所有正式 UI 优先复用本 Theme，不在 Tool 中重复维护整套 QSS。
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

# Arc-inspired 默认主题：柔和冷灰 + 淡紫色强调。
background = "#F2F1F6"
background_alt = "#ECEBF1"
sidebar_background = "#E9E7F0"
surface = "#FBFAFD"
surface_alt = "#F6F5F9"
surface_hover = "#EEEAF7"
surface_pressed = "#E5E0F1"

border = "#DCD9E4"
border_soft = "#E7E4EC"
border_focus = "#6D68D9"

text = "#242229"
text_secondary = "#55515D"
text_muted = "#8D8897"
text_disabled = "#B7B2BF"

accent = "#6D68D9"
accent_hover = "#5F5BC5"
accent_pressed = "#514DB1"
accent_soft = "#ECEAFA"
accent_soft_hover = "#E2DFF7"

success = "#3B966B"
warning = "#B7792D"
danger = "#C94E59"
info = "#4F78C7"

radius_small = 8
radius = 12
radius_large = 16


# =============================================================================
# Global Style Sheet
# =============================================================================

def _build_style_sheet():
    u"""生成 MuziTools 全局 QSS。"""
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
    border-right: 1px solid %(border_soft)s;
}

QWidget[muziCard="true"],
QFrame[muziCard="true"] {
    background-color: %(surface)s;
    border: 1px solid %(border_soft)s;
    border-radius: %(radius_large)dpx;
}

QWidget[muziCard="true"]:hover,
QFrame[muziCard="true"]:hover {
    border-color: %(border)s;
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
    font-size: 13px;
    font-weight: 650;
}

QLabel[muziMuted="true"] {
    color: %(text_muted)s;
}

QLabel[muziAccent="true"] {
    color: %(accent)s;
    font-weight: 600;
}

QLabel[muziPill="true"] {
    padding: 4px 9px;
    background-color: %(accent_soft)s;
    color: %(accent)s;
    border: 1px solid #DAD6F3;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
}

QLabel[muziSuccess="true"] {
    color: %(success)s;
    font-weight: 600;
}

QLabel[muziWarning="true"] {
    color: %(warning)s;
    font-weight: 600;
}

QLabel[muziDangerText="true"] {
    color: %(danger)s;
    font-weight: 600;
}

/* -------------------------------------------------------------------------
   Push Buttons
   ------------------------------------------------------------------------- */
QPushButton,
QToolButton {
    min-height: 32px;
    padding: 0px 13px;
    background-color: %(surface_alt)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius_small)dpx;
}

QPushButton:hover,
QToolButton:hover {
    background-color: %(surface_hover)s;
    border-color: #CBC6D6;
}

QPushButton:pressed,
QToolButton:pressed {
    background-color: %(surface_pressed)s;
    border-color: #BEB8CA;
}

QPushButton:checked,
QToolButton:checked {
    background-color: %(accent_soft)s;
    border-color: #CFC9EE;
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

QPushButton[muziSecondary="true"],
QToolButton[muziSecondary="true"] {
    background-color: %(surface)s;
    color: %(text)s;
    border: 1px solid #CCC7D5;
    font-weight: 600;
}

QPushButton[muziSecondary="true"]:hover,
QToolButton[muziSecondary="true"]:hover {
    background-color: %(accent_soft)s;
    color: %(accent)s;
    border-color: #C4BEE7;
}

QPushButton[muziDanger="true"] {
    background-color: #FFF1F2;
    border-color: #F3CCD0;
    color: %(danger)s;
}

QPushButton[muziDanger="true"]:hover {
    background-color: #FFE7EA;
    border-color: #EFB8BE;
}

QPushButton[muziGhost="true"],
QToolButton[muziGhost="true"] {
    background-color: transparent;
    border: 1px solid transparent;
    color: %(text_secondary)s;
}

QPushButton[muziGhost="true"]:hover,
QToolButton[muziGhost="true"]:hover {
    background-color: rgba(255, 255, 255, 0.44);
    border-color: %(border_soft)s;
    color: %(text)s;
}

QPushButton[muziNav="true"] {
    min-height: 34px;
    padding-left: 13px;
    padding-right: 12px;
    text-align: left;
    background-color: transparent;
    border: 1px solid transparent;
    color: %(text_secondary)s;
    border-radius: 10px;
}

QPushButton[muziNav="true"]:hover {
    background-color: rgba(255, 255, 255, 0.42);
    border-color: rgba(255, 255, 255, 0.28);
    color: %(text)s;
}

QPushButton[muziNav="true"]:checked,
QPushButton[muziNavActive="true"] {
    background-color: rgba(255, 255, 255, 0.70);
    color: %(text)s;
    border: 1px solid rgba(255, 255, 255, 0.78);
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
    min-height: 32px;
    padding: 0px 10px;
    background-color: rgba(255, 255, 255, 0.78);
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius_small)dpx;
}

QTextEdit,
QPlainTextEdit {
    padding: 9px;
}

QLineEdit[muziSearch="true"] {
    min-height: 34px;
    padding-left: 14px;
    padding-right: 14px;
    background-color: rgba(255, 255, 255, 0.62);
    border: 1px solid rgba(255, 255, 255, 0.72);
    border-radius: 17px;
}

QLineEdit[muziSearch="true"]:hover {
    background-color: rgba(255, 255, 255, 0.78);
    border-color: %(border)s;
}

QLineEdit[muziSearch="true"]:focus {
    background-color: %(surface)s;
    border: 1px solid %(border_focus)s;
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
    border-color: #CBC6D5;
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

QCheckBox::indicator,
QRadioButton::indicator {
    width: 15px;
    height: 15px;
}

QCheckBox::indicator:unchecked {
    background-color: %(surface)s;
    border: 1px solid #C8C3D0;
    border-radius: 5px;
}

QCheckBox::indicator:checked {
    background-color: %(accent)s;
    border: 1px solid %(accent)s;
    border-radius: 5px;
}

QRadioButton::indicator:unchecked {
    background-color: %(surface)s;
    border: 1px solid #C8C3D0;
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
    min-height: 29px;
    padding: 4px 8px;
    border-radius: 7px;
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
    min-height: 29px;
    padding: 0px 8px;
    background-color: %(surface_alt)s;
    color: %(text_secondary)s;
    border: none;
    border-right: 1px solid %(border_soft)s;
    border-bottom: 1px solid %(border_soft)s;
    font-weight: 600;
}

/* -------------------------------------------------------------------------
   Scroll Area / Scroll Bar
   ------------------------------------------------------------------------- */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollBar:vertical {
    width: 9px;
    margin: 2px;
    background: transparent;
}

QScrollBar::handle:vertical {
    min-height: 30px;
    background-color: #C7C2CE;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #AAA4B3;
}

QScrollBar:horizontal {
    height: 9px;
    margin: 2px;
    background: transparent;
}

QScrollBar::handle:horizontal {
    min-width: 30px;
    background-color: #C7C2CE;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #AAA4B3;
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
    height: 6px;
    background-color: #DCD8E2;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background-color: %(accent)s;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 16px;
    height: 16px;
    margin: -5px 0px;
    background-color: #FFFFFF;
    border: 2px solid %(accent)s;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background-color: %(accent_soft)s;
    border-color: %(accent_hover)s;
}

QProgressBar {
    min-height: 6px;
    max-height: 6px;
    background-color: #DDD9E3;
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
    padding: 7px;
    background-color: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius)dpx;
}

QMenu::item {
    min-height: 27px;
    padding: 2px 24px 2px 10px;
    border-radius: 7px;
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
    padding: 7px 10px;
    background-color: #2E2B33;
    color: #FFFFFF;
    border: none;
    border-radius: 7px;
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
        "success": success,
        "warning": warning,
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
    u"""动态属性变化后重新刷新 QSS。"""
    if widget is None:
        return

    style = widget.style()

    if style is None:
        return

    style.unpolish(widget)
    style.polish(widget)
    widget.update()


def set_role(widget, role, enabled=True):
    u"""给 QWidget 设置 MuziTools 视觉角色。"""
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
        "success": "muziSuccess",
        "warning": "muziWarning",
        "danger_text": "muziDangerText",
        "primary": "muziPrimary",
        "secondary": "muziSecondary",
        "danger": "muziDanger",
        "ghost": "muziGhost",
        "nav": "muziNav",
        "nav_active": "muziNavActive",
        "search": "muziSearch",
    }.get(role)

    if property_name is None:
        return widget

    widget.setProperty(
        property_name,
        bool(enabled)
    )
    repolish(
        widget
    )
    return widget


def apply_theme(widget):
    u"""把统一主题应用到一个窗口。"""
    if widget is None:
        return None

    try:
        widget.setStyleSheet(
            style_sheet
        )
    except Exception:
        return widget

    return widget


def make_title(text_value, parent=None):
    u"""创建主标题 Label。"""
    label = QLabel(
        text_value,
        parent
    )
    set_role(
        label,
        "title"
    )
    return label


def make_subtitle(text_value, parent=None):
    u"""创建自动换行的次级说明 Label。"""
    label = QLabel(
        text_value,
        parent
    )
    set_role(
        label,
        "subtitle"
    )
    label.setWordWrap(
        True
    )
    return label


def make_section_title(text_value, parent=None):
    u"""创建 Section 标题 Label。"""
    label = QLabel(
        text_value,
        parent
    )
    set_role(
        label,
        "section_title"
    )
    return label


def make_card(
        parent=None,
        margins=(16, 14, 16, 14),
        spacing=8
):
    u"""创建标准浮层内容卡片。"""
    card = QFrame(
        parent
    )
    set_role(
        card,
        "card"
    )

    layout = QVBoxLayout(
        card
    )
    layout.setContentsMargins(
        margins[0],
        margins[1],
        margins[2],
        margins[3]
    )
    layout.setSpacing(
        spacing
    )

    return card, layout


def make_sub_card(
        parent=None,
        margins=(12, 10, 12, 10),
        spacing=6
):
    u"""创建次级柔和内容卡片。"""
    card = QFrame(
        parent
    )
    set_role(
        card,
        "sub_card"
    )

    layout = QVBoxLayout(
        card
    )
    layout.setContentsMargins(
        margins[0],
        margins[1],
        margins[2],
        margins[3]
    )
    layout.setSpacing(
        spacing
    )

    return card, layout


def style_primary(button):
    u"""设置主要操作按钮。"""
    return set_role(
        button,
        "primary"
    )


def style_secondary(button):
    u"""设置清晰但不过度强调的次级操作按钮。"""
    return set_role(
        button,
        "secondary"
    )


def style_danger(button):
    u"""设置危险操作按钮。"""
    return set_role(
        button,
        "danger"
    )


def style_ghost(button):
    u"""设置弱强调 Ghost Button。"""
    return set_role(
        button,
        "ghost"
    )


def style_navigation(button, active=False):
    u"""设置 Sidebar / Step Navigation Button。"""
    set_role(
        button,
        "nav"
    )
    set_role(
        button,
        "nav_active",
        active
    )
    return button


def style_search(line_edit):
    u"""设置轻量搜索输入框。"""
    return set_role(
        line_edit,
        "search"
    )


def style_window(
        widget,
        title=None,
        minimum_width=None
):
    u"""统一设置窗口标题、最小宽度和主题。"""
    if widget is None:
        return None

    if title:
        widget.setWindowTitle(
            title
        )

    if minimum_width is not None:
        widget.setMinimumWidth(
            minimum_width
        )

    apply_theme(
        widget
    )

    try:
        widget.setAttribute(
            Qt.WA_StyledBackground,
            True
        )
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
    "style_secondary",
    "style_danger",
    "style_ghost",
    "style_navigation",
    "style_search",
    "style_window",
]
