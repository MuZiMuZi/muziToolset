# coding=utf-8
u"""绑定库局部主题：暖灰白底、工业墨色文字和酸橙高亮。"""

import os


# -----------------------------------------------------------------------------
# Modular Rig Library local stylesheet
# -----------------------------------------------------------------------------
# 视觉原则：
#     1. 大面积暖白留白，避免传统 DCC 深色面板的压迫感；
#     2. 酸橙色只用于当前步骤、当前选择、主操作和成功状态；
#     3. 面板依靠细线、字号和间距建立层级，减少厚重卡片；
#     4. 保持 Maya / PySide2 与 PySide6 可用，不依赖额外字体文件。
stylesheet = """
QWidget#ModularRigWindow {
    background: #f4f4ef;
    color: #232a27;
}

QWidget {
    font-family: "Segoe UI", "Microsoft YaHei UI", "Noto Sans CJK SC";
    font-size: 12px;
}

QLabel {
    color: #252d29;
    background: transparent;
}

QLabel[role="title"] {
    font-family: "Georgia";
    font-size: 32px;
    font-weight: bold;
    color: #202622;
}

QLabel[role="subtitle"] {
    color: #7d847d;
    font-size: 10px;
    letter-spacing: 1px;
}

QLabel[role="panelTitle"] {
    font-family: "Georgia";
    font-size: 17px;
    font-weight: bold;
    color: #252c28;
}

QLabel[role="moduleTitle"] {
    font-family: "Georgia";
    font-size: 22px;
    font-weight: bold;
    color: #222925;
}

QLabel[role="muted"] {
    color: #858b84;
    font-size: 11px;
}

QLabel[role="badge"] {
    color: #3e4b26;
    background: #eef5cf;
    border: 1px solid #dbe7a8;
    border-radius: 2px;
    padding: 4px 8px;
}

QLabel[role="status"] {
    color: #303831;
    font-size: 14px;
}

QFrame#HeaderFrame {
    background: #fafaf6;
    border: none;
    border-bottom: 1px solid #d9dcd5;
}

QFrame[role="panel"] {
    background: #fbfbf7;
    border: 1px solid #daddd6;
    border-radius: 2px;
}

QFrame#ModuleBanner {
    background: #f1f5dc;
    border: none;
    border-left: 4px solid #d4ed49;
}

QTabWidget#LibraryTabs::pane {
    border: none;
    background: transparent;
    top: -1px;
}

QTabBar::tab {
    background: transparent;
    color: #858a84;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 8px 10px 7px 10px;
    min-width: 82px;
}

QTabBar::tab:selected {
    color: #222a25;
    border-bottom: 2px solid #cfe844;
    font-weight: bold;
}

QTabBar::tab:hover:!selected {
    color: #566057;
    background: #f3f5e9;
}

QLineEdit,
QComboBox,
QDoubleSpinBox,
QSpinBox,
QPlainTextEdit {
    background: #ffffff;
    color: #29312d;
    border: 1px solid #d8dcd5;
    border-radius: 2px;
    padding: 5px 8px;
    min-height: 20px;
    selection-background-color: #dff173;
    selection-color: #232a25;
}

QLineEdit:hover,
QComboBox:hover,
QDoubleSpinBox:hover,
QSpinBox:hover,
QPlainTextEdit:hover {
    border-color: #c3c9be;
}

QLineEdit:focus,
QComboBox:focus,
QDoubleSpinBox:focus,
QSpinBox:focus,
QPlainTextEdit:focus {
    border: 1px solid #9caf40;
    background: #fffffd;
}

QLineEdit:disabled,
QComboBox:disabled,
QPlainTextEdit:disabled,
QDoubleSpinBox:disabled,
QSpinBox:disabled {
    background: #f0f1ed;
    color: #969b95;
    border-color: #e1e3de;
}

QComboBox::drop-down {
    width: 22px;
    border: none;
}

QComboBox::down-arrow {
    image: url("__ICON_DIR__/arrow_down.svg");
    width: 14px;
    height: 14px;
}

QSpinBox::up-button,
QDoubleSpinBox::up-button {
    width: 20px;
    border: none;
    subcontrol-origin: border;
    subcontrol-position: top right;
}

QSpinBox::down-button,
QDoubleSpinBox::down-button {
    width: 20px;
    border: none;
    subcontrol-origin: border;
    subcontrol-position: bottom right;
}

QSpinBox::up-arrow,
QDoubleSpinBox::up-arrow {
    image: url("__ICON_DIR__/arrow_up.svg");
    width: 11px;
    height: 11px;
}

QSpinBox::down-arrow,
QDoubleSpinBox::down-arrow {
    image: url("__ICON_DIR__/arrow_down.svg");
    width: 11px;
    height: 11px;
}

QComboBox QAbstractItemView {
    background: #fbfbf7;
    color: #29312d;
    border: 1px solid #d6dad2;
    selection-background-color: #e9f4b0;
    selection-color: #232b25;
}

QListWidget,
QTreeWidget {
    background: transparent;
    border: none;
    outline: none;
    color: #2b332f;
    alternate-background-color: #f8f8f3;
}

QListWidget::item {
    padding: 9px 7px;
    border-bottom: 1px solid #eceee8;
    border-radius: 1px;
}

QTreeWidget::item {
    min-height: 33px;
    border-bottom: 1px solid #eef0ea;
    padding-right: 4px;
}

QListWidget::item:selected,
QTreeWidget::item:selected {
    background: #e5f49d;
    color: #222a24;
}

QListWidget::item:hover,
QTreeWidget::item:hover {
    background: #f0f4df;
}

QHeaderView::section {
    background: #f3f4ef;
    color: #7d847d;
    border: none;
    border-bottom: 1px solid #e1e3dd;
    padding: 7px 4px;
}

QPushButton,
QToolButton {
    background: #fafbf7;
    border: 1px solid #d7dcd2;
    border-radius: 2px;
    padding: 6px 11px;
    min-height: 20px;
    color: #333c36;
}

QPushButton:hover,
QToolButton:hover {
    background: #f0f5dc;
    border-color: #b6c881;
}

QPushButton:pressed,
QToolButton:pressed {
    background: #e1edb6;
    border-color: #a8bb70;
}

QPushButton:focus,
QToolButton:focus {
    border-color: #879c35;
}

QPushButton#WorkflowStep {
    min-height: 78px;
    max-height: 78px;
    padding: 0;
    border: none;
    background: transparent;
}

QPushButton:disabled,
QToolButton:disabled {
    background: #f0f1ed;
    color: #a3a8a2;
    border-color: #e3e5e0;
}

QPushButton[role="primary"] {
    background: #d7ef49;
    color: #20271f;
    border: 1px solid #c7df3e;
    border-radius: 2px;
    font-size: 17px;
    font-weight: bold;
    padding: 13px 25px;
}

QPushButton[role="primary"]:hover {
    background: #e0f56b;
    border-color: #c5dc43;
}

QPushButton[role="primary"]:pressed {
    background: #c9e23f;
}

QPushButton[role="primary"]:disabled {
    background: #e8ebdc;
    border-color: #dfe3d5;
    color: #a0a78f;
}

QToolButton[role="section"] {
    background: #f1f2ed;
    border: none;
    border-bottom: 1px solid #e0e3dc;
    border-radius: 0;
    text-align: left;
    font-family: "Georgia";
    font-size: 13px;
    font-weight: bold;
    padding: 6px 7px;
    color: #303732;
}

QToolButton[role="section"]:hover {
    background: #eef3dc;
}

QCheckBox {
    color: #384139;
    spacing: 8px;
    background: transparent;
}

QCheckBox::indicator {
    width: 15px;
    height: 15px;
}

QCheckBox::indicator:unchecked {
    border: 1px solid #b9c0b5;
    background: #ffffff;
    border-radius: 2px;
}

QCheckBox::indicator:checked {
    background: #d2eb49;
    border: 1px solid #9fb337;
    border-radius: 2px;
}

QCheckBox:disabled {
    color: #929890;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollArea > QWidget > QWidget {
    background: #fbfbf7;
}

QSplitter::handle {
    background: #e9ece4;
}

QSplitter::handle:hover {
    background: #dce3c9;
}

QScrollBar:vertical {
    background: #f5f6f1;
    width: 7px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #c7cec0;
    min-height: 25px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #aeb8a5;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QToolTip {
    background: #2d342f;
    color: #f7f8f2;
    border: none;
    padding: 6px;
}

QMenu {
    background: #fbfbf7;
    color: #2d3530;
    border: 1px solid #cfd4ca;
    padding: 5px;
}

QMenu::item {
    padding: 7px 24px 7px 10px;
    border-radius: 1px;
}

QMenu::item:selected {
    background: #e2f282;
    color: #253020;
}

QMenu::item:disabled {
    color: #9ca29b;
    background: transparent;
}
"""


stylesheet = stylesheet.replace(
    "__ICON_DIR__",
    os.path.join(os.path.dirname(__file__), "icons").replace("\\", "/")
)
