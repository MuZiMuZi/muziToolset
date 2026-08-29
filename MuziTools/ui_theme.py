# coding=utf-8
u"""
Muzi Silicon UI Theme
=====================

MuziTools 自己的 Maya / PySide2 视觉系统。

设计方向参考现代 Silicon / Fluent 类桌面 UI 的视觉语言：
    - 深色分层背景；
    - 柔和紫色 Accent；
    - 大圆角卡片；
    - 低对比边框；
    - 清晰的标题 / 正文 / 辅助文字层级；
    - 控件 Hover / Press / Checked 状态统一；
    - 紧凑但不拥挤，适合 Maya 工具窗口。

注意：
    本文件不依赖 PyQt-SiliconUI，也没有复制其控件实现。
    目的是保持 Maya 2023 / PySide2 可直接运行，并方便整个 MuziTools
    使用一套可维护的 Theme Token。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget


# =============================================================================
# Theme Tokens
# =============================================================================
BACKGROUND = "#17151B"
BACKGROUND_ALT = "#1D1A22"
SURFACE = "#211E27"
SURFACE_ALT = "#29242F"
SURFACE_HOVER = "#332C3A"
SURFACE_PRESSED = "#3B3244"

BORDER = "#3A3341"
BORDER_SOFT = "#302A36"
BORDER_FOCUS = "#B57AC8"

TEXT = "#F0ECF3"
TEXT_SECONDARY = "#C9C2CE"
TEXT_MUTED = "#958E9D"
TEXT_DISABLED = "#69636F"

ACCENT = "#B57AC8"
ACCENT_HOVER = "#C98CDC"
ACCENT_PRESSED = "#9661AA"
ACCENT_SOFT = "#3B2942"
ACCENT_SOFT_HOVER = "#493051"

SECONDARY_ACCENT = "#8370D8"
SUCCESS = "#71B98A"
WARNING = "#D39A67"
DANGER = "#D56F7F"
INFO = "#6FA7D8"

RADIUS_SMALL = 6
RADIUS = 10
RADIUS_LARGE = 14


# =============================================================================
# Global Style Sheet
# =============================================================================
def _build_style_sheet():
    """生成完整 QSS。"""
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

QWidget[muziSurface="true"] {
    background-color: %(surface)s;
    border: 1px solid %(border_soft)s;
    border-radius: %(radius_large)dpx;
}

QWidget[muziCard="true"],
QFrame[muziCard="true"] {
    background-color: %(surface)s;
    border: 1px solid %(border)s;
    border-radius: %(radius_large)dpx;
}

QWidget[muziSubCard="true"],
QFrame[muziSubCard="true"] {
    background-color: %(surface_alt)s;
    border: 1px solid %(border_soft)s;
    border-radius: %(radius)dpx;
}

/* -------------------------------------------------------------------------
   Text hierarchy
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
    color: %(text_secondary)s;
    font-size: 12px;
}

QLabel[muziSectionTitle="true"] {
    color: %(text)s;
    font-size: 13px;
    font-weight: 600;
}

QLabel[muziMuted="true"] {
    color: %(text_muted)s;
}

QLabel[muziAccent="true"] {
    color: %(accent)s;
    font-weight: 600;
}

/* -------------------------------------------------------------------------
   Buttons
   ------------------------------------------------------------------------- */
QPushButton,
QToolButton {
    min-height: 30px;
    padding: 0px 12px;
    background-color: %(surface_alt)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius_small)dpx;
}

QPushButton:hover,
QToolButton:hover {
    background-color: %(surface_hover)s;
    border-color: #4D4356;
}

QPushButton:pressed,
QToolButton:pressed {
    background-color: %(surface_pressed)s;
    border-color: %(accent_pressed)s;
}

QPushButton:checked,
QToolButton:checked {
    background-color: %(accent_soft)s;
    border-color: %(accent)s;
    color: %(text)s;
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
    color: #1A131D;
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
    color: #FFFFFF;
}

QPushButton[muziDanger="true"] {
    background-color: #3A242A;
    border-color: #5A3039;
    color: #F0B1BB;
}

QPushButton[muziDanger="true"]:hover {
    background-color: #4A2931;
    border-color: %(danger)s;
}

QPushButton[muziGhost="true"],
QToolButton[muziGhost="true"] {
    background-color: transparent;
    border-color: transparent;
    color: %(text_secondary)s;
}

QPushButton[muziGhost="true"]:hover,
QToolButton[muziGhost="true"]:hover {
    background-color: %(surface_alt)s;
    border-color: %(border_soft)s;
    color: %(text)s;
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
    background-color: %(background_alt)s;
    color: %(text)s;
    border: 1px solid %(border)s;
    border-radius: %(radius_small)dpx;
}

QTextEdit,
QPlainTextEdit {
    padding: 8px;
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
    border-color: #514758;
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
    background-color: #211C25;
}

QLineEdit:read-only,
QTextEdit:read-only,
QPlainTextEdit:read-only {
    color: %(text_muted)s;
    background-color: #1B181F;
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
    selection-background-color: %(accent_soft_hover)s;
    selection-color: %(text)s;
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
    background-color: %(background_alt)s;
    border: 1px solid #5B5361;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: %(accent)s;
    border: 1px solid %(accent)s;
    border-radius: 4px;
}

QRadioButton::indicator:unchecked {
    background-color: %(background_alt)s;
    border: 1px solid #5B5361;
    border-radius: 8px;
}

QRadioButton::indicator:checked {
    background-color: %(accent)s;
    border: 4px solid %(background_alt)s;
    border-radius: 8px;
}

/* -------------------------------------------------------------------------
   Group / Tab / Splitter
   ------------------------------------------------------------------------- */
QGroupBox {
    margin-top: 12px;
    padding: 12px 10px 10px 10px;
    background-color: %(surface)s;
    color: %(text)s;
    border: 1px solid %(border)s;
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
    border: 1px solid %(border)s;
    border-radius: %(radius)dpx;
    background-color: %(surface)s;
    top: -1px;
}

QTabBar::tab {
    min-height: 28px;
    padding: 0px 12px;
    margin-right: 4px;
    background-color: transparent;
    color: %(text_muted)s;
    border: none;
    border-bottom: 2px solid transparent;
}

QTabBar::tab:hover {
    color: %(text)s;
    background-color: %(surface_alt)s;
}

QTabBar::tab:selected {
    color: %(text)s;
    border-bottom: 2px solid %(accent)s;
}

QSplitter::handle {
    background-color: %(border_soft)s;
}

/* -------------------------------------------------------------------------
   Views / Tables
   ------------------------------------------------------------------------- */
QListWidget,
QTreeWidget,
QTableWidget,
QTableView,
QTreeView,
QListView {
    background-color: %(background_alt)s;
    alternate-background-color: #201C24;
    color: %(text_secondary)s;
    border: 1px solid %(border)s;
    border-radius: %(radius)dpx;
    outline: none;
    gridline-color: %(border_soft)s;
}

QListWidget::item,
QTreeWidget::item,
QListView::item,
QTreeView::item {
    min-height: 26px;
    padding: 3px 7px;
    border-radius: 5px;
}

QListWidget::item:hover,
QTreeWidget::item:hover,
QListView::item:hover,
QTreeView::item:hover {
    background-color: %(surface_alt)s;
    color: %(text)s;
}

QListWidget::item:selected,
QTreeWidget::item:selected,
QListView::item:selected,
QTreeView::item:selected,
QTableWidget::item:selected,
QTableView::item:selected {
    background-color: %(accent_soft)s;
    color: %(text)s;
}

QHeaderView::section {
    min-height: 28px;
    padding: 0px 8px;
    background-color: %(surface_alt)s;
    color: %(text_secondary)s;
    border: none;
    border-right: 1px solid %(border_soft)s;
    border-bottom: 1px solid %(border)s;
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
    background-color: #625A68;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: %(accent)s;
}

QScrollBar:horizontal {
    height: 8px;
    margin: 2px;
    background: transparent;
}

QScrollBar::handle:horizontal {
    min-width: 30px;
    background-color: #625A68;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: %(accent)s;
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
    background-color: %(surface_alt)s;
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
    background-color: %(text)s;
    border: 3px solid %(accent)s;
    border-radius: 7px;
}

QProgressBar {
    min-height: 8px;
    max-height: 8px;
    background-color: %(surface_alt)s;
    border: none;
    border-radius: 4px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background-color: %(accent)s;
    border-radius: 4px;
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
    background-color: #3B3441;
    color: %(text)s;
    border: 1px solid #514758;
    border-radius: 6px;
}

/* -------------------------------------------------------------------------
   Misc
   ------------------------------------------------------------------------- */
QFrame[frameShape="4"],
QFrame[frameShape="5"] {
    color: %(border_soft)s;
}
""" % {
        "background": BACKGROUND,
        "background_alt": BACKGROUND_ALT,
        "surface": SURFACE,
        "surface_alt": SURFACE_ALT,
        "surface_hover": SURFACE_HOVER,
        "surface_pressed": SURFACE_PRESSED,
        "border": BORDER,
        "border_soft": BORDER_SOFT,
        "border_focus": BORDER_FOCUS,
        "text": TEXT,
        "text_secondary": TEXT_SECONDARY,
        "text_muted": TEXT_MUTED,
        "text_disabled": TEXT_DISABLED,
        "accent": ACCENT,
        "accent_hover": ACCENT_HOVER,
        "accent_pressed": ACCENT_PRESSED,
        "accent_soft": ACCENT_SOFT,
        "accent_soft_hover": ACCENT_SOFT_HOVER,
        "danger": DANGER,
        "radius_small": RADIUS_SMALL,
        "radius": RADIUS,
        "radius_large": RADIUS_LARGE,
    }


STYLE_SHEET = _build_style_sheet()


# =============================================================================
# Helpers
# =============================================================================
def repolish(widget):
    """属性改变后立即刷新 QSS。"""
    if widget is None:
        return

    style = widget.style()

    if style is None:
        return

    style.unpolish(widget)
    style.polish(widget)
    widget.update()


def set_role(widget, role, enabled=True):
    """给 QWidget 设置 Muzi Theme 动态属性。"""
    if widget is None:
        return widget

    property_name = {
        "surface": "muziSurface",
        "card": "muziCard",
        "sub_card": "muziSubCard",
        "title": "muziTitle",
        "subtitle": "muziSubtitle",
        "section_title": "muziSectionTitle",
        "muted": "muziMuted",
        "accent": "muziAccent",
        "primary": "muziPrimary",
        "danger": "muziDanger",
        "ghost": "muziGhost",
    }.get(role)

    if property_name is None:
        return widget

    widget.setProperty(property_name, bool(enabled))
    repolish(widget)
    return widget


def apply_theme(widget):
    """把 Muzi Silicon Theme 应用到一个窗口及其子控件。"""
    if widget is None:
        return None

    try:
        widget.setStyleSheet(STYLE_SHEET)
    except Exception:
        return widget

    return widget


def make_title(text, parent=None):
    label = QLabel(text, parent)
    set_role(label, "title")
    return label


def make_subtitle(text, parent=None):
    label = QLabel(text, parent)
    set_role(label, "subtitle")
    label.setWordWrap(True)
    return label


def make_section_title(text, parent=None):
    label = QLabel(text, parent)
    set_role(label, "section_title")
    return label


def make_card(parent=None, margins=(14, 12, 14, 12), spacing=8):
    """
    创建一个标准 Muzi Card。

    Returns:
        tuple: (card_widget, card_layout)
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


def make_sub_card(parent=None, margins=(10, 8, 10, 8), spacing=6):
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
    return set_role(button, "primary")


def style_danger(button):
    return set_role(button, "danger")


def style_ghost(button):
    return set_role(button, "ghost")


def style_window(widget, title=None, minimum_width=None):
    """统一设置常用窗口基础外观。"""
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
    "BACKGROUND",
    "BACKGROUND_ALT",
    "SURFACE",
    "SURFACE_ALT",
    "BORDER",
    "TEXT",
    "TEXT_SECONDARY",
    "TEXT_MUTED",
    "ACCENT",
    "SUCCESS",
    "WARNING",
    "DANGER",
    "INFO",
    "STYLE_SHEET",
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
    "style_window",
]
