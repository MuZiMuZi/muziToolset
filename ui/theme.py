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


def _build_style_sheet():
    u"""生成 MuziTools 全局 QSS。"""
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


def repolish(widget):
    u"""
    执行 `repolish` 对应的 Maya 工具操作。

    Args:
        widget (QtWidgets.QWidget):
            需要应用 MuziTools Theme / UI 状态的 Qt Widget。
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
    执行 `set_role` 对应的 Maya 工具操作。

    Args:
        widget (QtWidgets.QWidget):
            需要应用 MuziTools Theme / UI 状态的 Qt Widget。
        role (str):
            当前 UI / Rig 元素的语义角色，用于命名、Style 或构建分类。
        enabled (bool):
            当前 UI 控件或 Rig 功能是否启用。

    Returns:
        object:
            方法执行后的结果数据。
    """

    if widget is None:
        return widget
    property_name = {
        "surface": "muziSurface", "sidebar": "muziSidebar", "card": "muziCard", "sub_card": "muziSubCard",
        "title": "muziTitle", "subtitle": "muziSubtitle", "section_title": "muziSectionTitle", "muted": "muziMuted",
        "accent": "muziAccent", "pill": "muziPill", "success": "muziSuccess", "warning": "muziWarning",
        "danger_text": "muziDangerText", "primary": "muziPrimary", "secondary": "muziSecondary", "danger": "muziDanger",
        "ghost": "muziGhost", "nav": "muziNav", "nav_active": "muziNavActive", "search": "muziSearch",
    }.get(role)
    if property_name is None:
        return widget
    widget.setProperty(property_name, bool(enabled))
    repolish(widget)
    return widget


def apply_theme(widget):
    u"""
    执行 `apply_theme` 对应的 Maya 工具操作。

    Args:
        widget (QtWidgets.QWidget):
            需要应用 MuziTools Theme / UI 状态的 Qt Widget。

    Returns:
        object | None:
            方法执行后的结果数据。
    """

    if widget is None:
        return None
    widget.setStyleSheet(style_sheet)
    return widget


def make_title(text_value, parent=None):
    u"""
    执行 `make_title` 对应的 Maya 工具操作。

    Args:
        text_value (str):
            需要显示、验证或写入 Qt 文本控件的字符串。
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
        text_value (str):
            需要显示、验证或写入 Qt 文本控件的字符串。
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
        text_value (str):
            需要显示、验证或写入 Qt 文本控件的字符串。
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
    执行 `make_card` 对应的 Maya 工具操作。

    Args:
        parent (str):
            父级 Maya 节点名称。
        margins (tuple):
            Qt Layout 的 Left / Top / Right / Bottom Contents Margins。
        spacing (int):
            Qt Layout 中相邻控件之间的间距。

    Returns:
        tuple:
            方法执行后的结果数据。
    """

    card = QFrame(parent)
    set_role(card, "card")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
    layout.setSpacing(spacing)
    return card, layout


def make_sub_card(parent=None, margins=(12, 10, 12, 10), spacing=6):
    u"""
    执行 `make_sub_card` 对应的 Maya 工具操作。

    Args:
        parent (str):
            父级 Maya 节点名称。
        margins (tuple):
            Qt Layout 的 Left / Top / Right / Bottom Contents Margins。
        spacing (int):
            Qt Layout 中相邻控件之间的间距。

    Returns:
        tuple:
            方法执行后的结果数据。
    """

    card = QFrame(parent)
    set_role(card, "sub_card")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(margins[0], margins[1], margins[2], margins[3])
    layout.setSpacing(spacing)
    return card, layout


                           u"""
                           执行 `style_primary` 对应的 Maya 工具操作。

                           Args:
                               button (QtWidgets.QPushButton):
                                   需要应用 MuziTools Button 样式或状态的 QPushButton。

                           Returns:
                               object:
                                   方法执行后的结果数据。
                           """

def style_primary(button): return set_role(button, "primary")
                             u"""
                             执行 `style_secondary` 对应的 Maya 工具操作。

                             Args:
                                 button (QtWidgets.QPushButton):
                                     需要应用 MuziTools Button 样式或状态的 QPushButton。

                             Returns:
                                 object:
                                     方法执行后的结果数据。
                             """

def style_secondary(button): return set_role(button, "secondary")
                          u"""
                          执行 `style_danger` 对应的 Maya 工具操作。

                          Args:
                              button (QtWidgets.QPushButton):
                                  需要应用 MuziTools Button 样式或状态的 QPushButton。

                          Returns:
                              object:
                                  方法执行后的结果数据。
                          """

def style_danger(button): return set_role(button, "danger")
                         u"""
                         执行 `style_ghost` 对应的 Maya 工具操作。

                         Args:
                             button (QtWidgets.QPushButton):
                                 需要应用 MuziTools Button 样式或状态的 QPushButton。

                         Returns:
                             object:
                                 方法执行后的结果数据。
                         """

def style_ghost(button): return set_role(button, "ghost")

def style_navigation(button, active=False):
    u"""
    执行 `style_navigation` 对应的 Maya 工具操作。

    Args:
        button (QtWidgets.QPushButton):
            需要应用 MuziTools Button 样式或状态的 QPushButton。
        active (bool):
            Button / UI State 当前是否处于 Active 状态。

    Returns:
        object:
            方法执行后的结果数据。
    """

    set_role(button, "nav")
    set_role(button, "nav_active", active)
    return button

                             u"""
                             执行 `style_search` 对应的 Maya 工具操作。

                             Args:
                                 line_edit (QtWidgets.QLineEdit):
                                     需要应用 MuziTools 输入框样式的 QLineEdit。

                             Returns:
                                 object:
                                     方法执行后的结果数据。
                             """

def style_search(line_edit): return set_role(line_edit, "search")

def style_window(widget, title=None, minimum_width=None):
    u"""
    执行 `style_window` 对应的 Maya 工具操作。

    Args:
        widget (QtWidgets.QWidget):
            需要应用 MuziTools Theme / UI 状态的 Qt Widget。
        title (str):
            窗口、Section、Dialog 或报告使用的标题文本。
        minimum_width (int):
            Qt Widget / Dialog 的最小宽度。

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
    "background", "background_alt", "sidebar_background", "surface", "surface_alt", "border", "text",
    "text_secondary", "text_muted", "accent", "success", "warning", "danger", "info", "style_sheet",
    "apply_theme", "repolish", "set_role", "make_title", "make_subtitle", "make_section_title", "make_card",
    "make_sub_card", "style_primary", "style_secondary", "style_danger", "style_ghost", "style_navigation",
    "style_search", "style_window",
]
