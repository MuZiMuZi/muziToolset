# coding=utf-8
u"""
MuziTools UI Theme
==================

Maya 2023 / PySide2 统一视觉系统。

模块职责：
    1. 统一维护 MuziTools 的颜色、圆角和基础视觉常量；
    2. 统一生成全局 Qt Style Sheet；
    3. 提供常用 Label / Card / Button 的样式辅助函数；
    4. 通过 Qt Dynamic Property 管理控件的视觉角色。

模块边界：
    - 本模块只负责视觉样式，不处理 Maya Scene 数据；
    - 不在具体 Tool 中重复维护整套 QSS；
    - 不负责窗口生命周期，窗口显示和引用由 ui.window_utils / app.window_manager 负责；
    - PySide2 用于 Maya 2020-2024，PySide6 作为 Maya 2025+ 兼容入口。

设计方向：
    - 使用柔和背景、轻量边框、浮层式卡片和明确内容层级；
    - 主操作清晰，次级操作可见但不过度抢占注意力；
    - 保留 MuziTools 自己的品牌和 Maya 工作流；
    - 所有正式 UI 优先复用本 Theme。
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
# Theme Constants
# =============================================================================

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
    u"""生成 MuziTools 全局 QSS 字符串。"""
    # -------------------------------------------------------------------------
    # Step 01：整理并返回当前函数的最终结果
    # -------------------------------------------------------------------------
    return u"""
QWidget {
    background-color: %(background)s;
    color: %(text)s;
    font-family: "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei";
    font-size: 12px;
    selection-background-color: %(accent)s;
    selection-color: #FFFFFF;
}
QWidget[muziSurface="true"], QFrame[muziSurface="true"] {
    background-color: %(surface)s; border: 1px solid %(border_soft)s; border-radius: %(radius_large)dpx;
}
QWidget[muziSidebar="true"], QFrame[muziSidebar="true"] {
    background-color: %(sidebar_background)s; border: none; border-right: 1px solid %(border_soft)s;
}
QWidget[muziCard="true"], QFrame[muziCard="true"] {
    background-color: %(surface)s; border: 1px solid %(border_soft)s; border-radius: %(radius_large)dpx;
}
QWidget[muziSubCard="true"], QFrame[muziSubCard="true"] {
    background-color: %(surface_alt)s; border: 1px solid %(border_soft)s; border-radius: %(radius)dpx;
}
QLabel { background: transparent; border: none; color: %(text_secondary)s; }
QLabel[muziTitle="true"] { color: %(text)s; font-size: 20px; font-weight: 700; }
QLabel[muziSubtitle="true"] { color: %(text_muted)s; font-size: 12px; }
QLabel[muziSectionTitle="true"] { color: %(text)s; font-size: 13px; font-weight: 650; }
QLabel[muziMuted="true"] { color: %(text_muted)s; }
QLabel[muziAccent="true"] { color: %(accent)s; font-weight: 600; }
QLabel[muziPill="true"] {
    padding: 4px 9px; background-color: %(accent_soft)s; color: %(accent)s;
    border: 1px solid #DAD6F3; border-radius: 10px; font-size: 11px; font-weight: 600;
}
QLabel[muziSuccess="true"] { color: %(success)s; font-weight: 600; }
QLabel[muziWarning="true"] { color: %(warning)s; font-weight: 600; }
QLabel[muziDangerText="true"] { color: %(danger)s; font-weight: 600; }
QPushButton, QToolButton {
    min-height: 32px; padding: 0px 13px; background-color: %(surface_alt)s;
    color: %(text)s; border: 1px solid %(border)s; border-radius: %(radius_small)dpx;
}
QPushButton:hover, QToolButton:hover { background-color: %(surface_hover)s; border-color: #CBC6D6; }
QPushButton:pressed, QToolButton:pressed { background-color: %(surface_pressed)s; border-color: #BEB8CA; }
QPushButton:disabled, QToolButton:disabled { background-color: %(background_alt)s; border-color: %(border_soft)s; color: %(text_disabled)s; }
QPushButton[muziPrimary="true"], QToolButton[muziPrimary="true"] { background-color: %(accent)s; color: #FFFFFF; border: 1px solid %(accent)s; font-weight: 600; }
QPushButton[muziPrimary="true"]:hover, QToolButton[muziPrimary="true"]:hover { background-color: %(accent_hover)s; border-color: %(accent_hover)s; }
QPushButton[muziSecondary="true"], QToolButton[muziSecondary="true"] { background-color: %(surface)s; color: %(text)s; border: 1px solid #CCC7D5; font-weight: 600; }
QPushButton[muziSecondary="true"]:hover, QToolButton[muziSecondary="true"]:hover { background-color: %(accent_soft)s; color: %(accent)s; border-color: #C4BEE7; }
QPushButton[muziDanger="true"] { background-color: #FFF1F2; border-color: #F3CCD0; color: %(danger)s; }
QPushButton[muziGhost="true"], QToolButton[muziGhost="true"] { background-color: transparent; border: 1px solid transparent; color: %(text_secondary)s; }
QPushButton[muziNav="true"] { min-height: 34px; padding-left: 13px; padding-right: 12px; text-align: left; background-color: transparent; border: 1px solid transparent; color: %(text_secondary)s; border-radius: 10px; }
QPushButton[muziNav="true"]:checked, QPushButton[muziNavActive="true"] { background-color: rgba(255,255,255,0.70); color: %(text)s; border: 1px solid rgba(255,255,255,0.78); font-weight: 600; }
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QTimeEdit, QDateTimeEdit {
    min-height: 32px; padding: 0px 10px; background-color: rgba(255,255,255,0.78);
    color: %(text)s; border: 1px solid %(border)s; border-radius: %(radius_small)dpx;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus { border: 1px solid %(border_focus)s; background-color: %(surface)s; }
QComboBox::drop-down { border: none; background: transparent; }
QSpinBox, QDoubleSpinBox { padding-right: 32px; }
QSpinBox::up-button, QDoubleSpinBox::up-button {
    subcontrol-origin: border; subcontrol-position: top right; width: 26px;
    background-color: #EEEAF4; border-left: 1px solid #C9C3D2; border-bottom: 1px solid #D7D2DE;
    border-top-right-radius: %(radius_small)dpx;
}
QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border; subcontrol-position: bottom right; width: 26px;
    background-color: #EEEAF4; border-left: 1px solid #C9C3D2; border-top: 1px solid #D7D2DE;
    border-bottom-right-radius: %(radius_small)dpx;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover, QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: %(accent_soft)s; border-left-color: #AAA2C1;
}
QSpinBox::up-button:pressed, QSpinBox::down-button:pressed, QDoubleSpinBox::up-button:pressed, QDoubleSpinBox::down-button:pressed { background-color: %(accent_soft_hover)s; }
QSpinBox::up-arrow, QSpinBox::down-arrow, QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow { width: 9px; height: 9px; }
QSlider::groove:horizontal { height: 6px; background-color: #DCD8E2; border-radius: 3px; }
QSlider::sub-page:horizontal { background-color: %(accent)s; border-radius: 3px; }
QSlider::handle:horizontal { width: 16px; height: 16px; margin: -5px 0px; background-color: #FFFFFF; border: 2px solid %(accent)s; border-radius: 8px; }
QScrollBar:vertical { width: 9px; margin: 2px; background: transparent; }
QScrollBar::handle:vertical { min-height: 30px; background-color: #C7C2CE; border-radius: 4px; }
QToolTip { padding: 7px 10px; background-color: #2E2B33; color: #FFFFFF; border: none; border-radius: 7px; }
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
# Dynamic Property Helpers
# =============================================================================

def repolish(widget):
    u"""
    重新刷新一个 Qt Widget 的当前样式。

    Dynamic Property 修改后，Qt 不一定会立即重新计算 Style Sheet。
    本函数通过 unpolish / polish 让新的属性状态立即生效。

    Args:
        widget (QtWidgets.QWidget | None):
            需要刷新样式的 Qt Widget；None 时直接返回。
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
    给 Qt Widget 设置 MuziTools 语义样式角色。

    Args:
        widget (QtWidgets.QWidget | None):
            需要设置样式角色的 Qt Widget。
        role (str):
            MuziTools 角色名称，例如 ``primary``、``card``、``muted``。
        enabled (bool):
            True 时启用角色，False 时关闭角色。

    Returns:
        QtWidgets.QWidget | None:
            处理后的原 Widget；输入 None 时返回 None。
    """
    # -------------------------------------------------------------------------
    # Step 01：空 Widget 不执行任何 Qt 操作
    # -------------------------------------------------------------------------
    if widget is None:
        return widget

    # -------------------------------------------------------------------------
    # Step 02：把项目语义角色映射为 QSS 使用的 Dynamic Property
    # -------------------------------------------------------------------------
    property_map = {
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
    }
    property_name = property_map.get(
        role
    )

    # -------------------------------------------------------------------------
    # Step 03：未知角色保持原控件不变，避免写入无意义 Property
    # -------------------------------------------------------------------------
    if property_name is None:
        return widget

    # -------------------------------------------------------------------------
    # Step 04：写入 Dynamic Property，并主动刷新 Style Sheet
    # -------------------------------------------------------------------------
    widget.setProperty(
        property_name,
        bool(enabled)
    )
    repolish(
        widget
    )
    return widget


def apply_theme(widget):
    u"""
    把 MuziTools 全局 Style Sheet 应用到指定 Widget。

    Args:
        widget (QtWidgets.QWidget | None):
            需要应用全局主题的 Qt Widget。

    Returns:
        QtWidgets.QWidget | None:
            应用主题后的原 Widget；输入 None 时返回 None。
    """
    if widget is None:
        return None

    widget.setStyleSheet(
        style_sheet
    )
    return widget


# =============================================================================
# Common Widget Factory
# =============================================================================

def make_title(text_value, parent=None):
    u"""
    创建 MuziTools 一级标题 QLabel。

    Args:
        text_value (str):
            标题显示文本。
        parent (QtWidgets.QWidget | None):
            可选 Qt 父控件。

    Returns:
        QtWidgets.QLabel:
            已设置 ``title`` 角色的 QLabel。
    """
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
    u"""
    创建支持自动换行的 MuziTools 副标题 QLabel。

    Args:
        text_value (str):
            副标题显示文本。
        parent (QtWidgets.QWidget | None):
            可选 Qt 父控件。

    Returns:
        QtWidgets.QLabel:
            已设置 ``subtitle`` 角色并开启 Word Wrap 的 QLabel。
    """
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
    u"""
    创建 MuziTools Section 标题 QLabel。

    Args:
        text_value (str):
            Section 标题显示文本。
        parent (QtWidgets.QWidget | None):
            可选 Qt 父控件。

    Returns:
        QtWidgets.QLabel:
            已设置 ``section_title`` 角色的 QLabel。
    """
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
    u"""
    创建标准 MuziTools Card 和内部垂直布局。

    Args:
        parent (QtWidgets.QWidget | None):
            可选 Qt 父控件。
        margins (tuple[int, int, int, int]):
            Left / Top / Right / Bottom Contents Margins。
        spacing (int):
            Card 内相邻控件的 Layout Spacing。

    Returns:
        tuple[QtWidgets.QFrame, QtWidgets.QVBoxLayout]:
            Card QFrame 和对应的 QVBoxLayout。
    """
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
    u"""
    创建层级更轻的 MuziTools Sub Card 和内部垂直布局。

    Args:
        parent (QtWidgets.QWidget | None):
            可选 Qt 父控件。
        margins (tuple[int, int, int, int]):
            Left / Top / Right / Bottom Contents Margins。
        spacing (int):
            Sub Card 内相邻控件的 Layout Spacing。

    Returns:
        tuple[QtWidgets.QFrame, QtWidgets.QVBoxLayout]:
            Sub Card QFrame 和对应的 QVBoxLayout。
    """
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


# =============================================================================
# Button / Input Style Helpers
# =============================================================================

def style_primary(button):
    u"""
    把按钮设置为主要操作样式。

    Args:
        button (QtWidgets.QPushButton | QtWidgets.QToolButton):
            需要设置为 Primary 的按钮。

    Returns:
        QtWidgets.QWidget | None:
            处理后的原按钮。
    """
    return set_role(
        button,
        "primary"
    )


def style_secondary(button):
    u"""
    把按钮设置为次级操作样式。

    Args:
        button (QtWidgets.QPushButton | QtWidgets.QToolButton):
            需要设置为 Secondary 的按钮。

    Returns:
        QtWidgets.QWidget | None:
            处理后的原按钮。
    """
    return set_role(
        button,
        "secondary"
    )


def style_danger(button):
    u"""
    把按钮设置为危险操作样式。

    Args:
        button (QtWidgets.QPushButton):
            需要设置为 Danger 的按钮。

    Returns:
        QtWidgets.QWidget | None:
            处理后的原按钮。
    """
    return set_role(
        button,
        "danger"
    )


def style_ghost(button):
    u"""
    把按钮设置为弱化的 Ghost 样式。

    Args:
        button (QtWidgets.QPushButton | QtWidgets.QToolButton):
            需要设置为 Ghost 的按钮。

    Returns:
        QtWidgets.QWidget | None:
            处理后的原按钮。
    """
    return set_role(
        button,
        "ghost"
    )


def style_navigation(button, active=False):
    u"""
    设置侧边栏 Navigation Button 的基础和 Active 样式。

    Args:
        button (QtWidgets.QPushButton):
            需要设置为 Navigation 的按钮。
        active (bool):
            当前 Navigation Item 是否处于激活状态。

    Returns:
        QtWidgets.QPushButton | None:
            处理后的原按钮。
    """
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
    u"""
    把 QLineEdit 设置为 MuziTools Search 输入框样式。

    Args:
        line_edit (QtWidgets.QLineEdit):
            需要设置 Search 样式的输入框。

    Returns:
        QtWidgets.QWidget | None:
            处理后的原输入框。
    """
    return set_role(
        line_edit,
        "search"
    )


# =============================================================================
# Window Style
# =============================================================================

def style_window(
        widget,
        title=None,
        minimum_width=None
):
    u"""
    给 Tool Window 统一设置标题、最小宽度和 MuziTools Theme。

    Args:
        widget (QtWidgets.QWidget | None):
            需要设置统一窗口样式的 Qt Widget。
        title (str | None):
            可选 Window Title。
        minimum_width (int | None):
            可选窗口最小宽度。

    Returns:
        QtWidgets.QWidget | None:
            处理后的原 Widget；输入 None 时返回 None。
    """
    # -------------------------------------------------------------------------
    # Step 01：保护空窗口输入
    # -------------------------------------------------------------------------
    if widget is None:
        return None

    # -------------------------------------------------------------------------
    # Step 02：应用调用方明确提供的窗口基本属性
    # -------------------------------------------------------------------------
    if title:
        widget.setWindowTitle(
            title
        )

    if minimum_width is not None:
        widget.setMinimumWidth(
            minimum_width
        )

    # -------------------------------------------------------------------------
    # Step 03：应用统一 Theme，并尽量启用 Styled Background
    # -------------------------------------------------------------------------
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
