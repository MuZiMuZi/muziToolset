# coding=utf-8
u"""
Modular Rig UI
==============

MuziTools 模块化绑定系统的主界面。

设计目标：
    1. Module Library 负责展示可以添加到当前角色的 Rig Module；
    2. Templates 负责提供常用 Module 组合预设；
    3. Settings Tree 负责展示当前角色已经使用的 Module；
    4. 右侧只显示当前 Module 的参数，不把所有绑定参数一次堆在界面上；
    5. Jnt Size / Jnt Axis 放在当前 Module 下方的高频显示设置区域；
    6. Block / Mesh / Skeleton / Control 作为构建阶段显示入口；
    7. Build 区域只负责触发 Module Build，不在 UI 内实现绑定算法；
    8. Scene / Joint Display 查询统一复用 Core，不在 UI 维护第二套 Maya 底层逻辑。

当前版本先完成正式 UI Shell 和 Maya Joint Display 联动。
各 Module 的真正 Build / Rebuild API 会随着 Module 系统重构逐步接入。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import joint_utils
from ....core import scene_utils

try:
    from PySide2.QtCore import Qt
    from PySide2.QtCore import Signal
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QComboBox
    from PySide2.QtWidgets import QDoubleSpinBox
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QListWidget
    from PySide2.QtWidgets import QListWidgetItem
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QSizePolicy
    from PySide2.QtWidgets import QSlider
    from PySide2.QtWidgets import QSplitter
    from PySide2.QtWidgets import QToolButton
    from PySide2.QtWidgets import QTreeWidget
    from PySide2.QtWidgets import QTreeWidgetItem
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtCore import Signal
    from PySide6.QtWidgets import QCheckBox
    from PySide6.QtWidgets import QComboBox
    from PySide6.QtWidgets import QDoubleSpinBox
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QListWidget
    from PySide6.QtWidgets import QListWidgetItem
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSizePolicy
    from PySide6.QtWidgets import QSlider
    from PySide6.QtWidgets import QSplitter
    from PySide6.QtWidgets import QToolButton
    from PySide6.QtWidgets import QTreeWidget
    from PySide6.QtWidgets import QTreeWidgetItem
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget


module_name_list = [
    "aim",
    "arm",
    "finger",
    "fkChain",
    "godnode",
    "head",
    "jaw",
    "leg",
    "spineFk",
    "spineIk",
]

template_name_list = [
    "arm",
    "arm_nmc",
    "arm_three_finger",
    "arm_three_finger_nmc",
    "biped",
    "biped_lightweight",
    "brow_fk",
    "brow_fk_lightweight",
    "natalie",
]

default_module_data_list = [
    {"name": "leg", "side": "L"},
    {"name": "arm", "side": "R"},
    {"name": "spineFk", "side": ""},
    {
        "name": "head",
        "side": "",
        "children": [
            {"name": "jaw", "side": ""},
            {"name": "eye_L", "side": ""},
            {"name": "eye_R", "side": ""},
            {"name": "brow", "side": ""},
            {"name": "head_end", "side": ""},
        ],
    },
    {"name": "finger", "side": "M"},
]


modular_rig_style = u"""
QWidget#ModularRigWindow {
    background-color: #F5F6F8;
    color: #1D1D1F;
    font-family: "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei";
    font-size: 12px;
}
QFrame#HeaderFrame, QFrame#PanelFrame, QFrame#BuildFrame,
QFrame#StageFrame, QFrame#QuickSettingFrame {
    background-color: #FBFCFD;
    border: 1px solid #DDE1E7;
    border-radius: 9px;
}
QLabel { color: #35363A; background: transparent; }
QLabel[uiRole="appTitle"] { color: #1D1D1F; font-size: 17px; font-weight: 600; }
QLabel[uiRole="panelTitle"] { color: #34363A; font-size: 12px; font-weight: 650; }
QLabel[uiRole="moduleTitle"] { color: #0A72E8; font-size: 14px; font-weight: 700; }
QLabel[uiRole="sectionTitle"] { color: #303236; font-weight: 650; }
QLabel[uiRole="muted"] { color: #8A8E95; }
QLineEdit, QComboBox, QDoubleSpinBox {
    min-height: 29px; padding: 0px 9px; background-color: #FFFFFF;
    color: #2C2D31; border: 1px solid #D9DDE3; border-radius: 6px;
}
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus { border: 1px solid #0A84FF; }
QComboBox::drop-down { border: none; width: 24px; }
QListWidget, QTreeWidget {
    background-color: transparent; border: none; outline: none; color: #303236;
}
QListWidget::item { min-height: 28px; padding: 2px 7px; border-radius: 5px; }
QListWidget::item:selected { background-color: #DCEEFF; color: #1268C4; }
QListWidget::item:hover { background-color: #EEF5FC; }
QTreeWidget::item { min-height: 30px; border-bottom: 1px solid #EEF0F3; }
QTreeWidget::item:selected { background-color: #DCEEFF; color: #176FCB; }
QTreeWidget::item:hover { background-color: #F0F6FC; }
QPushButton, QToolButton {
    min-height: 30px; background-color: #FFFFFF; color: #36383D;
    border: 1px solid #DCE0E5; border-radius: 7px; padding: 0px 10px;
}
QPushButton:hover, QToolButton:hover { background-color: #F2F7FD; border-color: #BFD9F4; }
QPushButton:pressed, QToolButton:pressed { background-color: #E5F1FC; }
QToolButton[uiRole="headerTool"] {
    min-width: 32px; max-width: 32px; padding: 0px; border: none;
    background: transparent; color: #45484E; font-size: 17px;
}
QToolButton[uiRole="headerTool"]:hover { background-color: #EEF2F6; }
QToolButton[uiRole="miniTool"] {
    min-width: 31px; max-width: 31px; min-height: 28px; max-height: 28px;
    padding: 0px; font-size: 15px;
}
QPushButton[uiRole="buildButton"] {
    min-height: 88px; background-color: #FFFFFF; color: #087BF1;
    border: 1px solid #D9E0E8; border-radius: 9px; font-size: 25px; font-weight: 500;
}
QPushButton[uiRole="buildButton"]:hover { background-color: #F2F8FF; border-color: #A9CDF3; }
QPushButton[uiRole="stageButton"] {
    min-height: 34px; text-align: left; padding-left: 12px; background-color: #FFFFFF;
}
QPushButton[uiRole="stageButton"]:checked {
    background-color: #DCEEFF; color: #0878EB; border-color: #A9CFF5;
}
QCheckBox#JointAxisSwitch { spacing: 0px; }
QCheckBox#JointAxisSwitch::indicator {
    width: 42px; height: 22px; border-radius: 11px;
    background-color: #D4D7DC; border: 1px solid #C8CCD2;
}
QCheckBox#JointAxisSwitch::indicator:checked {
    background-color: #0A84FF; border: 1px solid #0A84FF;
}
QSlider::groove:horizontal { height: 4px; background-color: #D6DADF; border-radius: 2px; }
QSlider::sub-page:horizontal { background-color: #0A84FF; border-radius: 2px; }
QSlider::handle:horizontal {
    width: 16px; height: 16px; margin: -6px 0px; background-color: #FFFFFF;
    border: 1px solid #AEB4BC; border-radius: 8px;
}
QSplitter::handle { background-color: transparent; }
QScrollBar:vertical { width: 8px; background: transparent; }
QScrollBar::handle:vertical { min-height: 28px; background-color: #C9CDD3; border-radius: 4px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
"""


def _set_role(widget, role):
    u"""设置当前窗口局部 QSS 使用的 UI Role。"""
    widget.setProperty("uiRole", role)
    return widget


def _make_tool_button(text_value, tool_tip=u""):
    u"""创建 Header / Toolbar 使用的轻量按钮。"""
    button = QToolButton()
    button.setText(text_value)
    button.setToolTip(tool_tip)
    _set_role(button, "headerTool")
    return button


def _make_panel_title(text_value):
    u"""创建 Panel Title Label。"""
    label = QLabel(text_value)
    _set_role(label, "panelTitle")
    return label


def _make_separator():
    u"""创建轻量水平分隔线。"""
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setFrameShadow(QFrame.Plain)
    line.setStyleSheet("color: #E4E7EB; background-color: #E4E7EB; max-height: 1px;")
    return line


class ModularRigWindow(QWidget):
    u"""MuziTools 模块化绑定系统主窗口。"""

    build_requested = Signal(str)

    def __init__(self, parent=None):
        u"""初始化 Modular Rig UI。"""
        super(ModularRigWindow, self).__init__(parent)

        self.current_module_item = None
        self.loading_module_settings = False
        self.loading_joint_display = False

        self.setObjectName("ModularRigWindow")
        self.setWindowTitle(u"Modular Rig")
        self.setMinimumSize(1040, 680)
        self.resize(1260, 780)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.setStyleSheet(modular_rig_style)

        self.populate_module_library()
        self.populate_template_library()
        self.populate_default_module_tree()
        self.restore_joint_display_settings()

    # =========================================================================
    # Create UI
    # =========================================================================

    def create_widgets(self):
        u"""创建主窗口全部控件。"""
        # ---------------------------------------------------------------------
        # Step 01：顶部 Header
        # ---------------------------------------------------------------------
        self.header_frame = QFrame()
        self.header_frame.setObjectName("HeaderFrame")

        self.brand_label = QLabel(u"M")
        self.brand_label.setFixedWidth(28)
        self.brand_label.setAlignment(Qt.AlignCenter)
        self.brand_label.setStyleSheet(
            "color: #0A84FF; font-size: 22px; font-weight: 800; background: transparent;"
        )
        self.app_title_label = QLabel(u"Modular Rig")
        _set_role(self.app_title_label, "appTitle")

        self.new_button = _make_tool_button(u"+", u"新建 Rig 配置")
        self.open_button = _make_tool_button(u"▱", u"打开 Rig 配置")
        self.save_button = _make_tool_button(u"□", u"保存 Rig 配置")
        self.undo_button = _make_tool_button(u"↶", u"撤销")
        self.redo_button = _make_tool_button(u"↷", u"重做")
        self.help_button = _make_tool_button(u"?", u"帮助")
        self.preference_button = _make_tool_button(u"⚙", u"界面 / Rig 设置")

        # ---------------------------------------------------------------------
        # Step 02：左侧 Module / Template Library
        # ---------------------------------------------------------------------
        self.left_panel = QFrame()
        self.left_panel.setObjectName("PanelFrame")
        self.left_panel.setMinimumWidth(245)
        self.module_title_label = _make_panel_title(u"MODULES")
        self.module_search = QLineEdit()
        self.module_search.setPlaceholderText(u"Search modules...")
        self.module_filter_button = QToolButton()
        self.module_filter_button.setText(u"≡")
        self.module_filter_button.setToolTip(u"Module Filter")
        _set_role(self.module_filter_button, "miniTool")
        self.module_list = QListWidget()

        self.template_title_label = _make_panel_title(u"TEMPLATES")
        self.template_search = QLineEdit()
        self.template_search.setPlaceholderText(u"Search templates...")
        self.template_filter_button = QToolButton()
        self.template_filter_button.setText(u"≡")
        self.template_filter_button.setToolTip(u"Template Filter")
        _set_role(self.template_filter_button, "miniTool")
        self.template_list = QListWidget()
        self.library_count_label = QLabel()
        _set_role(self.library_count_label, "muted")

        # ---------------------------------------------------------------------
        # Step 03：中间 Module Settings Tree
        # ---------------------------------------------------------------------
        self.center_panel = QFrame()
        self.center_panel.setObjectName("PanelFrame")
        self.center_panel.setMinimumWidth(430)
        self.settings_title_label = _make_panel_title(u"SETTINGS")

        self.add_module_button = QToolButton()
        self.add_module_button.setText(u"+")
        self.add_module_button.setToolTip(u"添加 Module")
        _set_role(self.add_module_button, "miniTool")
        self.copy_module_button = QToolButton()
        self.copy_module_button.setText(u"□")
        self.copy_module_button.setToolTip(u"复制当前 Module")
        _set_role(self.copy_module_button, "miniTool")
        self.delete_module_button = QToolButton()
        self.delete_module_button.setText(u"×")
        self.delete_module_button.setToolTip(u"删除当前 Module")
        _set_role(self.delete_module_button, "miniTool")

        self.module_tree = QTreeWidget()
        self.module_tree.setColumnCount(2)
        self.module_tree.setHeaderHidden(True)
        self.module_tree.setIndentation(20)
        self.module_tree.setRootIsDecorated(True)
        self.module_tree.setAnimated(True)
        self.module_tree.setColumnWidth(0, 330)

        # ---------------------------------------------------------------------
        # Step 04：当前 Module 高频设置
        # ---------------------------------------------------------------------
        self.quick_setting_frame = QFrame()
        self.quick_setting_frame.setObjectName("QuickSettingFrame")
        self.name_label = QLabel(u"Name")
        self.module_name_edit = QLineEdit()
        self.module_name_edit.setPlaceholderText(u"Main")

        self.jnt_size_label = QLabel(u"Jnt Size")
        self.jnt_size_slider = QSlider(Qt.Horizontal)
        self.jnt_size_slider.setMinimum(10)
        self.jnt_size_slider.setMaximum(500)
        self.jnt_size_slider.setSingleStep(5)
        self.jnt_size_slider.setPageStep(25)
        self.jnt_size_slider.setValue(100)
        self.jnt_size_spin = QDoubleSpinBox()
        self.jnt_size_spin.setRange(0.10, 5.00)
        self.jnt_size_spin.setSingleStep(0.05)
        self.jnt_size_spin.setDecimals(2)
        self.jnt_size_spin.setValue(1.00)
        self.jnt_size_spin.setFixedWidth(82)

        self.jnt_axis_label = QLabel(u"Jnt Axis")
        self.jnt_axis_switch = QCheckBox()
        self.jnt_axis_switch.setObjectName("JointAxisSwitch")
        self.jnt_axis_switch.setToolTip(u"显示 / 隐藏场景 Joint Local Axis")
        self.jnt_axis_switch.setFixedWidth(44)

        # ---------------------------------------------------------------------
        # Step 05：Build Stage
        # ---------------------------------------------------------------------
        self.stage_frame = QFrame()
        self.stage_frame.setObjectName("StageFrame")
        self.stage_button_list = []
        stage_data_list = [
            (u"◇   Block", True),
            (u"◇   Mesh", False),
            (u"♙   Skeleton", False),
            (u"✣   Control", False),
        ]

        for stage_text, checked in stage_data_list:
            stage_button = QPushButton(stage_text)
            stage_button.setCheckable(True)
            stage_button.setChecked(checked)
            _set_role(stage_button, "stageButton")
            self.stage_button_list.append(stage_button)

        # ---------------------------------------------------------------------
        # Step 06：右侧 Module Property
        # ---------------------------------------------------------------------
        self.right_panel = QFrame()
        self.right_panel.setObjectName("PanelFrame")
        self.right_panel.setMinimumWidth(350)
        self.current_module_title = QLabel(u"HEAD")
        _set_role(self.current_module_title, "moduleTitle")

        self.side_label = QLabel(u"Side")
        self.side_combo = QComboBox()
        self.side_combo.addItems([u"Center", u"Left", u"Right"])
        self.naming_preset_label = QLabel(u"Naming Preset")
        self.naming_preset_combo = QComboBox()
        self.naming_preset_combo.addItems([u"Default"])
        self.mirror_behavior_label = QLabel(u"Mirror Behavior")
        self.mirror_behavior_combo = QComboBox()
        self.mirror_behavior_combo.addItems([u"None", u"Mirror"])

        self.alignment_title = QLabel(u"Alignment")
        _set_role(self.alignment_title, "sectionTitle")
        self.world_up_label = QLabel(u"World Up")
        self.world_up_combo = QComboBox()
        self.world_up_combo.addItems([u"Y", u"X", u"Z"])
        self.aim_axis_label = QLabel(u"Aim Axis")
        self.aim_axis_combo = QComboBox()
        self.aim_axis_combo.addItems([u"Z", u"X", u"Y", u"-X", u"-Y", u"-Z"])
        self.up_axis_label = QLabel(u"Up Axis")
        self.up_axis_combo = QComboBox()
        self.up_axis_combo.addItems([u"Y", u"X", u"Z", u"-X", u"-Y", u"-Z"])

        self.joints_section_button = QPushButton(u"›   Joints")
        self.controls_section_button = QPushButton(u"›   Controls")
        self.deformation_section_button = QPushButton(u"›   Deformation")
        self.attributes_section_button = QPushButton(u"›   Attributes")
        property_section_button_list = [
            self.joints_section_button,
            self.controls_section_button,
            self.deformation_section_button,
            self.attributes_section_button,
        ]

        for section_button in property_section_button_list:
            section_button.setFlat(True)
            section_button.setStyleSheet(
                "QPushButton { text-align: left; border: none; background: transparent; "
                "padding-left: 3px; min-height: 30px; }"
                "QPushButton:hover { background-color: #F2F6FA; }"
            )

        # ---------------------------------------------------------------------
        # Step 07：Build Action
        # ---------------------------------------------------------------------
        self.build_frame = QFrame()
        self.build_frame.setObjectName("BuildFrame")
        self.guide_action_button = QToolButton()
        self.guide_action_button.setText(u"◇")
        self.guide_action_button.setToolTip(u"Guide / Block")
        self.guide_action_button.setCheckable(True)
        self.guide_action_button.setChecked(True)
        self.delete_action_button = QToolButton()
        self.delete_action_button.setText(u"⌫")
        self.delete_action_button.setToolTip(u"删除 Module Build Result")
        self.reset_action_button = QToolButton()
        self.reset_action_button.setText(u"⌂")
        self.reset_action_button.setToolTip(u"恢复 Module 默认设置")
        self.module_setting_button = QToolButton()
        self.module_setting_button.setText(u"⚙")
        self.module_setting_button.setToolTip(u"Module 高级设置")

        action_button_list = [
            self.guide_action_button,
            self.delete_action_button,
            self.reset_action_button,
            self.module_setting_button,
        ]

        for action_button in action_button_list:
            action_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            action_button.setMinimumHeight(38)

        self.build_button = QPushButton(u"◇   Build")
        _set_role(self.build_button, "buildButton")

    def create_layouts(self):
        u"""按照三栏模块化绑定设计创建主布局。"""
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(12, 6, 12, 6)
        header_layout.setSpacing(6)
        header_layout.addWidget(self.brand_label)
        header_layout.addWidget(self.app_title_label)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.new_button)
        header_layout.addSpacing(8)
        header_layout.addWidget(self.open_button)
        header_layout.addWidget(self.save_button)
        header_layout.addSpacing(8)
        header_layout.addWidget(self.undo_button)
        header_layout.addWidget(self.redo_button)
        header_layout.addStretch(1)
        header_layout.addWidget(self.help_button)
        header_layout.addWidget(self.preference_button)

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(7)
        module_search_layout = QHBoxLayout()
        module_search_layout.setContentsMargins(0, 0, 0, 0)
        module_search_layout.setSpacing(5)
        module_search_layout.addWidget(self.module_search, 1)
        module_search_layout.addWidget(self.module_filter_button)
        template_search_layout = QHBoxLayout()
        template_search_layout.setContentsMargins(0, 0, 0, 0)
        template_search_layout.setSpacing(5)
        template_search_layout.addWidget(self.template_search, 1)
        template_search_layout.addWidget(self.template_filter_button)

        left_layout.addWidget(self.module_title_label)
        left_layout.addLayout(module_search_layout)
        left_layout.addWidget(self.module_list, 1)
        left_layout.addWidget(_make_separator())
        left_layout.addWidget(self.template_title_label)
        left_layout.addLayout(template_search_layout)
        left_layout.addWidget(self.template_list, 1)
        left_layout.addWidget(self.library_count_label)

        center_layout = QVBoxLayout(self.center_panel)
        center_layout.setContentsMargins(10, 10, 10, 10)
        center_layout.setSpacing(7)
        settings_toolbar_layout = QHBoxLayout()
        settings_toolbar_layout.setContentsMargins(0, 0, 0, 0)
        settings_toolbar_layout.setSpacing(5)
        settings_toolbar_layout.addWidget(self.add_module_button)
        settings_toolbar_layout.addWidget(self.copy_module_button)
        settings_toolbar_layout.addWidget(self.delete_module_button)
        settings_toolbar_layout.addStretch(1)

        center_layout.addWidget(self.settings_title_label)
        center_layout.addWidget(_make_separator())
        center_layout.addLayout(settings_toolbar_layout)
        center_layout.addWidget(self.module_tree, 1)

        quick_setting_layout = QVBoxLayout(self.quick_setting_frame)
        quick_setting_layout.setContentsMargins(10, 8, 10, 8)
        quick_setting_layout.setSpacing(6)
        name_layout = QHBoxLayout()
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(8)
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.module_name_edit, 1)
        jnt_size_layout = QHBoxLayout()
        jnt_size_layout.setContentsMargins(0, 0, 0, 0)
        jnt_size_layout.setSpacing(8)
        jnt_size_layout.addWidget(self.jnt_size_label)
        jnt_size_layout.addWidget(self.jnt_size_slider, 1)
        jnt_size_layout.addWidget(self.jnt_size_spin)
        jnt_axis_layout = QHBoxLayout()
        jnt_axis_layout.setContentsMargins(0, 0, 0, 0)
        jnt_axis_layout.setSpacing(8)
        jnt_axis_layout.addWidget(self.jnt_axis_label)
        jnt_axis_layout.addWidget(self.jnt_axis_switch)
        jnt_axis_layout.addStretch(1)

        quick_setting_layout.addLayout(name_layout)
        quick_setting_layout.addLayout(jnt_size_layout)
        quick_setting_layout.addLayout(jnt_axis_layout)
        center_layout.addWidget(self.quick_setting_frame)

        stage_layout = QVBoxLayout(self.stage_frame)
        stage_layout.setContentsMargins(8, 7, 8, 7)
        stage_layout.setSpacing(4)

        for stage_button in self.stage_button_list:
            stage_layout.addWidget(stage_button)

        center_layout.addWidget(self.stage_frame)

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(12, 10, 12, 10)
        right_layout.setSpacing(8)
        right_layout.addWidget(self.current_module_title)
        right_layout.addSpacing(3)
        right_layout.addLayout(self.create_property_row(self.side_label, self.side_combo))
        right_layout.addLayout(self.create_property_row(self.naming_preset_label, self.naming_preset_combo))
        right_layout.addLayout(self.create_property_row(self.mirror_behavior_label, self.mirror_behavior_combo))
        right_layout.addWidget(_make_separator())
        right_layout.addWidget(self.alignment_title)
        right_layout.addLayout(self.create_property_row(self.world_up_label, self.world_up_combo))
        right_layout.addLayout(self.create_property_row(self.aim_axis_label, self.aim_axis_combo))
        right_layout.addLayout(self.create_property_row(self.up_axis_label, self.up_axis_combo))
        right_layout.addWidget(_make_separator())
        right_layout.addWidget(self.joints_section_button)
        right_layout.addWidget(self.controls_section_button)
        right_layout.addWidget(self.deformation_section_button)
        right_layout.addWidget(self.attributes_section_button)
        right_layout.addStretch(1)

        build_layout = QVBoxLayout(self.build_frame)
        build_layout.setContentsMargins(8, 8, 8, 8)
        build_layout.setSpacing(7)
        build_toolbar_layout = QHBoxLayout()
        build_toolbar_layout.setContentsMargins(0, 0, 0, 0)
        build_toolbar_layout.setSpacing(5)
        build_toolbar_layout.addWidget(self.guide_action_button)
        build_toolbar_layout.addWidget(self.delete_action_button)
        build_toolbar_layout.addWidget(self.reset_action_button)
        build_toolbar_layout.addWidget(self.module_setting_button)
        build_layout.addLayout(build_toolbar_layout)
        build_layout.addWidget(self.build_button, 1)
        right_layout.addWidget(self.build_frame)

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.addWidget(self.left_panel)
        self.main_splitter.addWidget(self.center_panel)
        self.main_splitter.addWidget(self.right_panel)
        self.main_splitter.setStretchFactor(0, 2)
        self.main_splitter.setStretchFactor(1, 4)
        self.main_splitter.setStretchFactor(2, 3)
        self.main_splitter.setSizes([260, 520, 430])

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)
        main_layout.addWidget(self.header_frame)
        main_layout.addWidget(self.main_splitter, 1)

    def create_property_row(self, label, widget):
        u"""创建右侧属性的一行 Label + Widget。"""
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(10)
        row_layout.addWidget(label)
        row_layout.addStretch(1)
        widget.setMinimumWidth(150)
        row_layout.addWidget(widget)
        return row_layout

    def create_connections(self):
        u"""连接界面 Signal。"""
        self.module_search.textChanged.connect(self.filter_module_library)
        self.template_search.textChanged.connect(self.filter_template_library)
        self.module_list.itemDoubleClicked.connect(self.add_module_from_library)
        self.template_list.itemDoubleClicked.connect(self.load_template)
        self.add_module_button.clicked.connect(self.clicked_add_module)
        self.copy_module_button.clicked.connect(self.copy_current_module)
        self.delete_module_button.clicked.connect(self.delete_current_module)
        self.module_tree.currentItemChanged.connect(self.current_module_changed)
        self.module_name_edit.editingFinished.connect(self.module_name_changed)
        self.side_combo.currentIndexChanged.connect(self.side_changed)
        self.jnt_size_slider.valueChanged.connect(self.jnt_size_slider_changed)
        self.jnt_size_spin.valueChanged.connect(self.jnt_size_spin_changed)
        self.jnt_axis_switch.toggled.connect(self.jnt_axis_changed)
        self.build_button.clicked.connect(self.clicked_build)
        self.delete_action_button.clicked.connect(self.delete_current_module)
        self.reset_action_button.clicked.connect(self.reset_current_module_settings)
        self.undo_button.clicked.connect(self.undo_maya)
        self.redo_button.clicked.connect(self.redo_maya)

    # =========================================================================
    # Library
    # =========================================================================

    def populate_module_library(self):
        u"""填充 Module Library。"""
        self.module_list.clear()

        for module_name in module_name_list:
            item = QListWidgetItem(u"◈  {}".format(module_name))
            item.setData(Qt.UserRole, module_name)
            self.module_list.addItem(item)

        if self.module_list.count() > 0:
            self.module_list.setCurrentRow(0)

        self.update_library_count()

    def populate_template_library(self):
        u"""填充 Template Library。"""
        self.template_list.clear()

        for template_name in template_name_list:
            item = QListWidgetItem(u"▦  {}".format(template_name))
            item.setData(Qt.UserRole, template_name)
            self.template_list.addItem(item)

        self.update_library_count()

    def update_library_count(self):
        u"""更新左下 Library 数量。"""
        total_count = self.module_list.count() + self.template_list.count()
        self.library_count_label.setText(u"Library: {} items".format(total_count))

    def filter_module_library(self, search_text):
        u"""按照搜索内容过滤 Module Library。"""
        search_text = search_text.strip().lower()
        row_index = 0

        while row_index < self.module_list.count():
            item = self.module_list.item(row_index)
            module_name = item.data(Qt.UserRole)

            if module_name is None:
                module_name = item.text()

            visible = True

            if search_text:
                visible = search_text in str(module_name).lower()

            item.setHidden(not visible)
            row_index += 1

    def filter_template_library(self, search_text):
        u"""按照搜索内容过滤 Template Library。"""
        search_text = search_text.strip().lower()
        row_index = 0

        while row_index < self.template_list.count():
            item = self.template_list.item(row_index)
            template_name = item.data(Qt.UserRole)

            if template_name is None:
                template_name = item.text()

            visible = True

            if search_text:
                visible = search_text in str(template_name).lower()

            item.setHidden(not visible)
            row_index += 1

    # =========================================================================
    # Module Tree
    # =========================================================================

    def populate_default_module_tree(self):
        u"""创建与 UI 设计图一致的默认 Module Tree 示例。"""
        self.module_tree.clear()

        for module_data in default_module_data_list:
            self.create_module_tree_item(module_data, parent_item=None)

        self.module_tree.expandAll()
        root_item = self.find_first_module_item("head")

        if root_item is None:
            root_item = self.module_tree.topLevelItem(0)

        if root_item is not None:
            self.module_tree.setCurrentItem(root_item)

    def create_module_tree_item(self, module_data, parent_item=None):
        u"""根据 Module Data 创建一个 Settings Tree Item。"""
        module_name = module_data.get("name", "module")
        side = module_data.get("side", "")
        item = QTreeWidgetItem()
        item.setText(0, u"◇  {}".format(module_name))
        item.setText(1, side)
        item.setData(0, Qt.UserRole, module_name)
        item.setData(1, Qt.UserRole, side)

        if parent_item is None:
            self.module_tree.addTopLevelItem(item)
        else:
            parent_item.addChild(item)

        child_data_list = module_data.get("children", [])

        for child_data in child_data_list:
            self.create_module_tree_item(child_data, parent_item=item)

        return item

    def find_first_module_item(self, module_name):
        u"""在 Settings Tree 中查找第一个同名 Module。"""
        top_index = 0

        while top_index < self.module_tree.topLevelItemCount():
            top_item = self.module_tree.topLevelItem(top_index)
            result = self.find_module_item_recursive(top_item, module_name)

            if result is not None:
                return result

            top_index += 1

        return None

    def find_module_item_recursive(self, item, module_name):
        u"""递归查找 Module Tree Item。"""
        if item is None:
            return None

        item_module_name = item.data(0, Qt.UserRole)

        if item_module_name == module_name:
            return item

        child_index = 0

        while child_index < item.childCount():
            child_item = item.child(child_index)
            result = self.find_module_item_recursive(child_item, module_name)

            if result is not None:
                return result

            child_index += 1

        return None

    def clicked_add_module(self):
        u"""点击 + 时把左侧当前 Module 添加到 Settings Tree。"""
        current_item = self.module_list.currentItem()

        if current_item is None:
            return

        self.add_module_from_library(current_item)

    def add_module_from_library(self, item):
        u"""从 Module Library 添加一个新的 Module Instance。"""
        if item is None:
            return

        module_name = item.data(Qt.UserRole)

        if not module_name:
            return

        module_data = {"name": module_name, "side": ""}
        new_item = self.create_module_tree_item(module_data, parent_item=None)
        self.module_tree.setCurrentItem(new_item)

    def copy_current_module(self):
        u"""复制当前 Module 的 UI 配置。"""
        source_item = self.module_tree.currentItem()

        if source_item is None:
            return

        module_name = source_item.data(0, Qt.UserRole)
        side = source_item.data(1, Qt.UserRole)
        module_data = {"name": module_name, "side": side}
        parent_item = source_item.parent()
        new_item = self.create_module_tree_item(module_data, parent_item=parent_item)
        self.module_tree.setCurrentItem(new_item)

    def delete_current_module(self):
        u"""从 Settings Tree 删除当前 Module UI Instance。"""
        current_item = self.module_tree.currentItem()

        if current_item is None:
            return

        parent_item = current_item.parent()

        if parent_item is None:
            item_index = self.module_tree.indexOfTopLevelItem(current_item)

            if item_index >= 0:
                self.module_tree.takeTopLevelItem(item_index)
        else:
            child_index = parent_item.indexOfChild(current_item)

            if child_index >= 0:
                parent_item.takeChild(child_index)

        self.current_module_item = None

    def current_module_changed(self, current_item, previous_item):
        u"""Settings Tree 当前 Module 变化后刷新右侧参数。"""
        if current_item is None:
            return

        self.current_module_item = current_item
        self.loading_module_settings = True
        module_name = current_item.data(0, Qt.UserRole)
        side = current_item.data(1, Qt.UserRole)

        if module_name is None:
            module_name = current_item.text(0)

        if side is None:
            side = ""

        self.module_name_edit.setText(str(module_name))
        self.current_module_title.setText(str(module_name).upper())
        side_index = 0

        if side in ["L", "LF", "Left"]:
            side_index = 1
        elif side in ["R", "RT", "Right"]:
            side_index = 2

        self.side_combo.setCurrentIndex(side_index)
        self.loading_module_settings = False

    def module_name_changed(self):
        u"""把 Name 输入框同步到当前 Module Tree Item。"""
        if self.loading_module_settings:
            return

        current_item = self.module_tree.currentItem()

        if current_item is None:
            return

        module_name = self.module_name_edit.text().strip()

        if not module_name:
            return

        current_item.setData(0, Qt.UserRole, module_name)
        current_item.setText(0, u"◇  {}".format(module_name))
        self.current_module_title.setText(module_name.upper())

    def side_changed(self, combo_index):
        u"""把 Side UI 同步到当前 Module Tree Item。"""
        if self.loading_module_settings:
            return

        current_item = self.module_tree.currentItem()

        if current_item is None:
            return

        side_value = ""

        if combo_index == 1:
            side_value = "L"
        elif combo_index == 2:
            side_value = "R"

        current_item.setData(1, Qt.UserRole, side_value)
        current_item.setText(1, side_value)

    def reset_current_module_settings(self):
        u"""恢复当前 Module UI 的基础显示参数。"""
        current_item = self.module_tree.currentItem()

        if current_item is None:
            return

        self.loading_module_settings = True
        self.side_combo.setCurrentIndex(0)
        self.naming_preset_combo.setCurrentIndex(0)
        self.mirror_behavior_combo.setCurrentIndex(0)
        self.world_up_combo.setCurrentText("Y")
        self.aim_axis_combo.setCurrentText("Z")
        self.up_axis_combo.setCurrentText("Y")
        current_item.setData(1, Qt.UserRole, "")
        current_item.setText(1, "")
        self.loading_module_settings = False

    # =========================================================================
    # Template
    # =========================================================================

    def load_template(self, item):
        u"""载入 Template UI 预设；当前版本先建立可编辑 Module Tree。"""
        if item is None:
            return

        template_name = item.data(Qt.UserRole)

        if not template_name:
            return

        self.populate_default_module_tree()
        QMessageBox.information(
            self,
            u"Template",
            u"已载入 {} 的 UI 组合预览。\n真实 Template Data 会在 Module Base 完成后接入。".format(
                template_name
            )
        )

    # =========================================================================
    # Joint Display
    # =========================================================================

    def restore_joint_display_settings(self):
        u"""从 Maya 当前场景恢复 Jnt Size / Jnt Axis 显示状态。"""
        self.loading_joint_display = True
        joint_size = 1.0

        try:
            joint_size = joint_utils.get_display_scale()
        except Exception:
            joint_size = 1.0

        joint_size = max(
            0.10,
            min(5.00, joint_size)
        )
        self.jnt_size_spin.setValue(
            joint_size
        )
        self.jnt_size_slider.setValue(
            int(round(joint_size * 100.0))
        )

        show_axis = False
        joint_list = scene_utils.get_nodes_by_type(
            "joint",
            long=True
        )

        for joint_node in joint_list:
            try:
                joint_object = joint_utils.Joint(
                    joint_node
                )
                display_axis = joint_object.is_axis_visible()
            except Exception:
                display_axis = False

            if display_axis:
                show_axis = True
                break

        self.jnt_axis_switch.setChecked(
            show_axis
        )
        self.loading_joint_display = False

    def jnt_size_slider_changed(self, slider_value):
        u"""Slider 改变时同步数值并实时修改 Maya Joint Display Scale。"""
        if self.loading_joint_display:
            return

        joint_size = float(slider_value) / 100.0
        self.loading_joint_display = True
        self.jnt_size_spin.setValue(joint_size)
        self.loading_joint_display = False
        self.set_maya_joint_size(joint_size)

    def jnt_size_spin_changed(self, joint_size):
        u"""数值框改变时同步 Slider 并修改 Maya Joint Display Scale。"""
        if self.loading_joint_display:
            return

        self.loading_joint_display = True
        self.jnt_size_slider.setValue(
            int(round(float(joint_size) * 100.0))
        )
        self.loading_joint_display = False
        self.set_maya_joint_size(joint_size)

    def set_maya_joint_size(self, joint_size):
        u"""设置 Maya 全局 Joint Display Scale。"""
        try:
            joint_utils.set_display_scale(
                joint_size
            )
        except Exception as error:
            cmds.warning(
                u"设置 Joint Display Scale 失败：{}".format(
                    error
                )
            )

    def jnt_axis_changed(self, checked):
        u"""显示或隐藏场景全部 Joint 的 Local Axis。"""
        if self.loading_joint_display:
            return

        joint_list = scene_utils.get_nodes_by_type(
            "joint",
            long=True
        )

        for joint_node in joint_list:
            try:
                joint_object = joint_utils.Joint(
                    joint_node
                )

                if checked:
                    joint_object.show_axis()
                else:
                    joint_object.hide_axis()
            except Exception as error:
                cmds.warning(
                    u"设置 Joint Axis 失败：{} | {}".format(
                        joint_node,
                        error
                    )
                )

    # =========================================================================
    # Build / Maya Action
    # =========================================================================

    def clicked_build(self):
        u"""发出当前 Module Build 请求。"""
        current_item = self.module_tree.currentItem()

        if current_item is None:
            QMessageBox.warning(
                self,
                u"Build",
                u"请先选择一个 Module。"
            )
            return

        module_name = current_item.data(0, Qt.UserRole)

        if not module_name:
            module_name = current_item.text(0)

        self.build_requested.emit(
            str(module_name)
        )
        QMessageBox.information(
            self,
            u"Module Build",
            u"{} Module 的 UI 已准备完成。\nBuild API 会在对应 Module 后端迁移完成后接入。".format(
                module_name
            )
        )

    def undo_maya(self):
        u"""调用 Maya Undo。"""
        try:
            cmds.undo()
        except Exception:
            pass

    def redo_maya(self):
        u"""调用 Maya Redo。"""
        try:
            cmds.redo()
        except Exception:
            pass


__all__ = [
    "ModularRigWindow",
]
