# coding=utf-8
u"""
Face Rig UI
===========

Face Rig Wizard 的纯 Qt View；业务逻辑由 workflow_controller.py 负责。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QDoubleSpinBox
    from PySide2.QtWidgets import QFormLayout
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QScrollArea
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QTabWidget
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QDialog
    from PySide6.QtWidgets import QDoubleSpinBox
    from PySide6.QtWidgets import QFormLayout
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QLineEdit
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QScrollArea
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QTabWidget
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget


def qt_align_center():
    if hasattr(Qt, "AlignCenter"):
        return Qt.AlignCenter
    return Qt.AlignmentFlag.AlignCenter


def qt_no_frame():
    if hasattr(QFrame, "NoFrame"):
        return QFrame.NoFrame
    return QFrame.Shape.NoFrame


align_center = qt_align_center()
no_frame = qt_no_frame()


class NodePicker(QWidget):
    u"""Maya Node 文本输入 + Pick / Clear。"""

    def __init__(self, label_text, parent=None):
        super(NodePicker, self).__init__(parent)
        self.label = QLabel(label_text)
        self.line_edit = QLineEdit()
        self.pick_button = QPushButton(u"Pick")
        self.clear_button = QPushButton(u"Clear")
        self.pick_button.setFixedWidth(58)
        self.clear_button.setFixedWidth(58)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit, 1)
        layout.addWidget(self.pick_button)
        layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear)

    def value(self):
        value = self.line_edit.text().strip()
        if not value:
            return None
        return value

    def set_value(self, value):
        if value is None:
            self.clear()
            return
        self.line_edit.setText(str(value))

    def clear(self):
        self.line_edit.clear()


class FaceRigView(QDialog):
    u"""Face Rig 四阶段 Wizard View。"""

    def __init__(self, parent=None):
        super(FaceRigView, self).__init__(parent)
        self.setWindowTitle(u"Muzi Face Rig")
        self.setMinimumSize(620, 560)
        self.resize(760, 760)
        self.node_pickers = {}
        self.controller_color_widgets = {}
        self.controller_size_widgets = {}
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.title_label = QLabel(u"Muzi Face Rig")
        self.title_label.setAlignment(align_center)
        self.status_label = QLabel(u"Ready")
        self.reload_button = QPushButton(u"Reload Scene Data")
        self.tabs = QTabWidget()
        self.setup_page = self.create_setup_page()
        self.guide_page = self.create_guide_page()
        self.build_page = self.create_build_page()
        self.finalize_page = self.create_finalize_page()
        self.tabs.addTab(self.setup_page, u"Step 01  Setup")
        self.tabs.addTab(self.guide_page, u"Step 02  Guide")
        self.tabs.addTab(self.build_page, u"Step 03  Build")
        self.tabs.addTab(self.finalize_page, u"Step 04  Finalize")

    def create_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.tabs, 1)
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.status_label, 1)
        bottom_layout.addWidget(self.reload_button)
        main_layout.addLayout(bottom_layout)

    @staticmethod
    def create_scroll_page():
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(no_frame)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        scroll_area.setWidget(content)
        page_layout.addWidget(scroll_area)
        return page, content_layout

    def create_setup_page(self):
        page, layout = self.create_scroll_page()
        picker_items = [
            ("head_model", u"Head Model"),
            ("left_eye_model", u"Left Eye"),
            ("right_eye_model", u"Right Eye"),
            ("upper_teeth_model", u"Upper Teeth"),
            ("lower_teeth_model", u"Lower Teeth"),
            ("tongue_model", u"Tongue"),
            ("gum_model", u"Gum"),
        ]
        for picker_key, label_text in picker_items:
            picker = NodePicker(label_text)
            self.node_pickers[picker_key] = picker
            layout.addWidget(picker)

        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel(u"Mouth Joint Count"))
        count_layout.addStretch(1)
        self.mouth_joint_count_spin = QSpinBox()
        self.mouth_joint_count_spin.setRange(4, 256)
        self.mouth_joint_count_spin.setSingleStep(4)
        self.mouth_joint_count_spin.setValue(32)
        count_layout.addWidget(self.mouth_joint_count_spin)
        layout.addLayout(count_layout)
        self.run_setup_button = QPushButton(u"Run Face Setup")
        layout.addWidget(self.run_setup_button)
        layout.addStretch(1)
        return page

    def create_guide_page(self):
        page, layout = self.create_scroll_page()
        button_layout = QGridLayout()
        self.build_guide_button = QPushButton(u"Build Guide")
        self.reimport_guide_button = QPushButton(u"Reimport Guide")
        self.mirror_left_to_right_button = QPushButton(u"Mirror LF → RT")
        self.mirror_right_to_left_button = QPushButton(u"Mirror RT → LF")
        self.undo_mirror_button = QPushButton(u"Undo Last Mirror")
        self.validate_guide_button = QPushButton(u"Validate Guide")
        button_layout.addWidget(self.build_guide_button, 0, 0)
        button_layout.addWidget(self.reimport_guide_button, 0, 1)
        button_layout.addWidget(self.mirror_left_to_right_button, 1, 0)
        button_layout.addWidget(self.mirror_right_to_left_button, 1, 1)
        button_layout.addWidget(self.undo_mirror_button, 2, 0)
        button_layout.addWidget(self.validate_guide_button, 2, 1)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel(u"Controller Settings"))

        settings_form = QFormLayout()
        self.controller_global_scale_spin = QDoubleSpinBox()
        self.controller_global_scale_spin.setRange(0.001, 1000.0)
        self.controller_global_scale_spin.setDecimals(3)
        self.controller_global_scale_spin.setValue(1.0)
        settings_form.addRow(u"Global Scale", self.controller_global_scale_spin)

        for side in ["lf", "rt", "md"]:
            color_spin = QSpinBox()
            color_spin.setRange(0, 31)
            self.controller_color_widgets[side] = color_spin
            settings_form.addRow(u"{} Color".format(side.upper()), color_spin)

        module_names = [
            "brow", "eye", "eyelid", "nose", "cheek",
            "lip", "jaw", "teeth", "tongue",
        ]
        for module_name in module_names:
            size_spin = QDoubleSpinBox()
            size_spin.setRange(0.001, 1000.0)
            size_spin.setDecimals(3)
            size_spin.setValue(1.0)
            self.controller_size_widgets[module_name] = size_spin
            settings_form.addRow(
                u"{} Size".format(module_name.replace("_", " ").title()),
                size_spin
            )

        layout.addLayout(settings_form)
        self.save_controller_settings_button = QPushButton(
            u"Save Controller Settings"
        )
        self.complete_guide_button = QPushButton(u"Complete Guide Step")
        layout.addWidget(self.save_controller_settings_button)
        layout.addWidget(self.complete_guide_button)
        layout.addStretch(1)
        return page

    def create_build_page(self):
        page, layout = self.create_scroll_page()
        description = QLabel(
            u"Step 03 使用 PyMEL Component 架构构建 Face Rig。\n"
            u"Teeth 已接入标准 Component；Eyelid / Curve Attachment / Zip Lip "
            u"作为可复用 Builder API。"
        )
        description.setWordWrap(True)
        self.run_build_button = QPushButton(u"Build Face Rig")
        layout.addWidget(description)
        layout.addWidget(self.run_build_button)
        layout.addStretch(1)
        return page

    def create_finalize_page(self):
        page, layout = self.create_scroll_page()
        description = QLabel(
            u"Finalize 会整理 Face Rig 最终显示状态并完成 Workflow。"
        )
        description.setWordWrap(True)
        self.finalize_button = QPushButton(u"Finalize Face Rig")
        layout.addWidget(description)
        layout.addWidget(self.finalize_button)
        layout.addStretch(1)
        return page

    def set_status(self, message):
        self.status_label.setText(str(message))


__all__ = [
    "NodePicker",
    "FaceRigView",
]
