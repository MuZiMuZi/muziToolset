# coding=utf-8
u"""绑定库局部主题：暖白底、墨色文字和酸橙高亮。"""

import os

stylesheet = """
QWidget#ModularRigWindow { background: #f3f5ed; color: #26322f; }
QWidget { font-family: "Segoe UI", "Microsoft YaHei UI", "Noto Sans CJK SC"; font-size: 12px; }
QLabel { color: #293733; background: transparent; }
QLabel[role="title"] { font-family: "Georgia"; font-size: 32px; font-weight: bold; }
QLabel[role="subtitle"] { color: #7c897d; font-size: 10px; }
QLabel[role="panelTitle"] { font-family: "Georgia"; font-size: 17px; font-weight: bold; }
QLabel[role="moduleTitle"] { font-family: "Georgia"; font-size: 22px; font-weight: bold; }
QLabel[role="muted"] { color: #7d8980; font-size: 11px; }
QLabel[role="badge"] { color: #526534; background: #eef3d9; border-radius: 3px; padding: 5px 8px; }
QLabel[role="status"] { font-size: 14px; }
QFrame#HeaderFrame { background: #fafbf7; border-bottom: 1px solid #dce1d4; }
QFrame[role="panel"] { background: #fcfdf9; border: 1px solid #dce2d7; border-radius: 4px; }
QFrame#ModuleBanner { background: #f0f5df; border: 0; border-left: 3px solid #c6df4e; }
QTabWidget#LibraryTabs::pane { border: none; background: transparent; top: -1px; }
QTabBar::tab {
    background: #f2f4ed; color: #7a8678; border: 1px solid #dfe4d8;
    padding: 8px 10px; min-width: 82px;
}
QTabBar::tab:first { border-top-left-radius: 3px; border-bottom-left-radius: 3px; }
QTabBar::tab:last { border-top-right-radius: 3px; border-bottom-right-radius: 3px; }
QTabBar::tab:selected { background: #dff17f; color: #2d3c28; border-color: #c8df59; font-weight: bold; }
QTabBar::tab:hover:!selected { background: #eef3df; color: #52604d; }
QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QPlainTextEdit {
    background: #ffffff; color: #2c3b34; border: 1px solid #d8dfd4;
    border-radius: 3px; padding: 5px 8px; min-height: 20px;
    selection-background-color: #d9ed87; selection-color: #29372c;
}
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QSpinBox:focus, QPlainTextEdit:focus {
    border: 1px solid #97ae49;
}
QLineEdit:disabled, QComboBox:disabled, QPlainTextEdit:disabled {
    background: #f2f4ee; color: #8a9387;
}
QComboBox::drop-down { width: 22px; border: none; }
QComboBox::down-arrow { image: url("__ICON_DIR__/arrow_down.svg"); width: 14px; height: 14px; }
QSpinBox::up-button, QDoubleSpinBox::up-button { width: 20px; border: none; subcontrol-origin: border; subcontrol-position: top right; }
QSpinBox::down-button, QDoubleSpinBox::down-button { width: 20px; border: none; subcontrol-origin: border; subcontrol-position: bottom right; }
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow { image: url("__ICON_DIR__/arrow_up.svg"); width: 11px; height: 11px; }
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow { image: url("__ICON_DIR__/arrow_down.svg"); width: 11px; height: 11px; }
QComboBox QAbstractItemView { background: #fcfdf9; color: #29372c; selection-background-color: #e6f4b3; }
QListWidget, QTreeWidget { background: transparent; border: none; outline: none; color: #2e3c35; }
QListWidget::item { padding: 10px 7px; border-bottom: 1px solid #edf0e7; border-radius: 3px; }
QListWidget::item:selected, QTreeWidget::item:selected { background: #e8f5b3; color: #253521; }
QListWidget::item:hover, QTreeWidget::item:hover { background: #f1f6e5; }
QTreeWidget::item { min-height: 33px; border-bottom: 1px solid #f0f3eb; padding-right: 4px; }
QHeaderView::section { background: #f3f6ec; color: #7a8678; border: none; padding: 7px 4px; }
QPushButton, QToolButton {
    background: #fcfdf8; border: 1px solid #dbe2d1; border-radius: 3px;
    padding: 6px 11px; min-height: 20px; color: #354330;
}
QPushButton:hover, QToolButton:hover { background: #f0f6dc; border-color: #b5ca7e; }
QPushButton:pressed, QToolButton:pressed { background: #deedae; }
QPushButton:focus, QToolButton:focus { border-color: #8fa944; }
QPushButton#WorkflowStep { min-height: 78px; max-height: 78px; padding: 0; border: none; }
QPushButton:disabled, QToolButton:disabled { background: #f2f4ed; color: #a2ac9b; border-color: #e5e9df; }
QPushButton[role="primary"] { background: #d5ed55; border-color: #cce54c; font-size: 17px; font-weight: bold; padding: 13px 25px; }
QPushButton[role="primary"]:hover { background: #def378; }
QPushButton[role="primary"]:disabled { background: #e7ebd9; border-color: #e1e5d6; color: #a0aa8b; }
QToolButton[role="section"] { background: #f0f3eb; border: none; border-radius: 2px; text-align: left; font-family: "Georgia"; font-size: 13px; font-weight: bold; padding: 5px 6px; }
QCheckBox { color: #384631; spacing: 8px; background: transparent; }
QCheckBox::indicator { width: 15px; height: 15px; }
QCheckBox::indicator:unchecked { border: 1px solid #bac5ad; background: white; border-radius: 2px; }
QCheckBox::indicator:checked { background: #c8df4f; border: 1px solid #9fb73f; border-radius: 2px; }
QCheckBox:disabled { color: #909987; }
QScrollArea { border: none; background: transparent; }
QScrollArea > QWidget > QWidget { background: #fcfdf9; }
QSplitter::handle { background: #edf1e5; }
QScrollBar:vertical { background: #f7f9f1; width: 7px; margin: 0; }
QScrollBar::handle:vertical { background: #c6d1b7; min-height: 25px; border-radius: 3px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QToolTip { background: #303e30; color: #f7faed; border: 0; padding: 6px; }
"""

stylesheet = stylesheet.replace("__ICON_DIR__", os.path.join(os.path.dirname(__file__), "icons").replace("\\", "/"))
