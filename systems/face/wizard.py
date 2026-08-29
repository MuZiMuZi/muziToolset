# coding=utf-8
u"""
Face Rig Wizard
===============

新的 Face Rig 系统 UI。

设计原则：
    - UI 只收集参数和展示 Build 状态；
    - 实际 Step 逻辑由 FaceSetup / FaceGuide 等系统类负责；
    - 不在模块 import 时 reload 依赖；
    - 使用根包 ui 的统一 Theme 与通用 Widget。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QSlider
    from PySide2.QtWidgets import QStackedWidget
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSlider
    from PySide6.QtWidgets import QStackedWidget
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...ui import theme
from ...ui.widgets import MayaObjectPicker
from .face_setup import FaceSetup


class FaceRigWizard(QWidget):
    """Face Rig 分步构建窗口。"""

    def __init__(self, parent=None):
        super(FaceRigWizard, self).__init__(parent)

        self.current_step_index = 0
        self.completed_step_indexes = set()
        self.step_buttons = []
        self.face_setup = None

        # 嘴唇 Joint 数量始终以 4 为一个档位。
        # Slider 内部只保存档位，真正的 Joint 数量由档位 * 4 得到。
        self.mouth_joint_step = 4
        self.mouth_joint_minimum = 4
        self.mouth_joint_maximum = 128
        self.mouth_joint_default = 40

        self.setWindowTitle(u"Face Rig Wizard")
        self.setMinimumWidth(680)
        self.resize(760, 720)

        self.create_widgets()
        self.create_pages()
        self.create_layouts()
        self.create_connections()

        theme.style_window(self)
        self.set_current_step(0)

    # =========================================================================
    # UI
    # =========================================================================

    def create_widgets(self):
        """创建 Wizard 公共控件。"""
        self.title_label = theme.make_title(u"Face Rig")
        self.subtitle_label = theme.make_subtitle(
            u"按步骤建立面部绑定。每一个 Build Step 都由独立系统模块负责。"
        )

        step_names = [
            u"01  Setup",
            u"02  Guide",
            u"03  Build",
            u"04  Finalize",
        ]

        for step_index in range(len(step_names)):
            step_name = step_names[step_index]

            step_button = QPushButton(step_name)
            step_button.setCheckable(True)
            step_button.setProperty(
                "step_index",
                step_index
            )
            theme.style_navigation(step_button)

            self.step_buttons.append(step_button)

        self.page_stack = QStackedWidget()

        self.previous_button = QPushButton(u"上一步")
        theme.style_ghost(self.previous_button)

        self.next_button = QPushButton(u"下一步")
        theme.style_primary(self.next_button)

        self.status_label = QLabel(u"准备就绪")
        theme.set_role(self.status_label, "muted")

    def create_pages(self):
        """创建四个步骤页面。"""
        self.step1_page = self.create_step1_page()
        self.step2_page = self.create_placeholder_page(
            u"Step 02 · Face Guide",
            u"Guide 构建逻辑正在迁移到 systems/face。完成后这里会接入 FaceGuide。"
        )
        self.step3_page = self.create_placeholder_page(
            u"Step 03 · Face Build",
            u"这里将负责眉毛、眼睑、嘴唇、下颌等 Face Module 的正式 Build。"
        )
        self.step4_page = self.create_placeholder_page(
            u"Step 04 · Finalize",
            u"这里将负责 Controller Set、显示属性、清理、检查和最终发布。"
        )

        self.page_stack.addWidget(self.step1_page)
        self.page_stack.addWidget(self.step2_page)
        self.page_stack.addWidget(self.step3_page)
        self.page_stack.addWidget(self.step4_page)

    def create_step1_page(self):
        """创建 Face Setup 页面。"""
        page = QWidget()

        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        model_card, model_layout = theme.make_card(page)
        model_layout.addWidget(
            theme.make_section_title(u"模型输入")
        )

        model_description = QLabel(
            u"Head 为必填项，其它模型可以留空。拾取时使用 Maya 当前最后选择对象。"
        )
        model_description.setWordWrap(True)
        theme.set_role(model_description, "muted")
        model_layout.addWidget(model_description)

        self.face_head_picker = MayaObjectPicker(
            label_text=u"Head *",
            placeholder=u"头部主模型",
            node_types=["transform"]
        )
        self.face_lf_eye_picker = MayaObjectPicker(
            label_text=u"Left Eye",
            placeholder=u"左眼模型",
            node_types=["transform"]
        )
        self.face_rt_eye_picker = MayaObjectPicker(
            label_text=u"Right Eye",
            placeholder=u"右眼模型",
            node_types=["transform"]
        )
        self.upper_teech_picker = MayaObjectPicker(
            label_text=u"Upper Teeth",
            placeholder=u"上牙模型",
            node_types=["transform"]
        )
        self.lower_teech_picker = MayaObjectPicker(
            label_text=u"Lower Teeth",
            placeholder=u"下牙模型",
            node_types=["transform"]
        )
        self.face_tongue_picker = MayaObjectPicker(
            label_text=u"Tongue",
            placeholder=u"舌头模型",
            node_types=["transform"]
        )
        self.face_gum_picker = MayaObjectPicker(
            label_text=u"Gum",
            placeholder=u"牙龈模型",
            node_types=["transform"]
        )

        model_layout.addWidget(self.face_head_picker)
        model_layout.addWidget(self.face_lf_eye_picker)
        model_layout.addWidget(self.face_rt_eye_picker)
        model_layout.addWidget(self.upper_teech_picker)
        model_layout.addWidget(self.lower_teech_picker)
        model_layout.addWidget(self.face_tongue_picker)
        model_layout.addWidget(self.face_gum_picker)

        parameter_card, parameter_layout = theme.make_card(page)
        parameter_layout.addWidget(
            theme.make_section_title(u"构建参数")
        )

        mouth_layout = QHBoxLayout()
        mouth_layout.setContentsMargins(0, 0, 0, 0)
        mouth_layout.setSpacing(10)

        mouth_label = QLabel(u"嘴唇 Joint 数量")
        mouth_label.setMinimumWidth(120)

        self.mouth_joint_slider = QSlider(Qt.Horizontal)
        self.mouth_joint_slider.setMinimum(
            int(self.mouth_joint_minimum / self.mouth_joint_step)
        )
        self.mouth_joint_slider.setMaximum(
            int(self.mouth_joint_maximum / self.mouth_joint_step)
        )
        self.mouth_joint_slider.setSingleStep(1)
        self.mouth_joint_slider.setPageStep(2)
        self.mouth_joint_slider.setValue(
            int(self.mouth_joint_default / self.mouth_joint_step)
        )
        self.mouth_joint_slider.setMinimumWidth(280)
        self.style_mouth_joint_slider()

        self.mouth_joint_value_label = QLabel(
            u"{}".format(self.mouth_joint_default)
        )
        self.mouth_joint_value_label.setMinimumWidth(46)
        self.mouth_joint_value_label.setAlignment(Qt.AlignCenter)
        theme.set_role(
            self.mouth_joint_value_label,
            "pill"
        )

        mouth_hint = QLabel(
            u"{} ～ {}，每格 {} Joint".format(
                self.mouth_joint_minimum,
                self.mouth_joint_maximum,
                self.mouth_joint_step
            )
        )
        theme.set_role(mouth_hint, "muted")

        mouth_layout.addWidget(mouth_label)
        mouth_layout.addWidget(self.mouth_joint_slider, 1)
        mouth_layout.addWidget(self.mouth_joint_value_label)
        mouth_layout.addWidget(mouth_hint)

        parameter_layout.addLayout(mouth_layout)

        build_card, build_layout = theme.make_card(page)
        build_layout.addWidget(
            theme.make_section_title(u"Step 01 Build")
        )

        build_description = QLabel(
            u"Build 会确保 Face 基础层级、更新三个 Head 工作模型，并把当前参数写入同一个 Config Network Node。"
        )
        build_description.setWordWrap(True)
        theme.set_role(build_description, "muted")

        self.build_step1_button = QPushButton(u"Build Face Setup")
        theme.style_primary(self.build_step1_button)

        build_layout.addWidget(build_description)
        build_layout.addWidget(self.build_step1_button)

        main_layout.addWidget(model_card)
        main_layout.addWidget(parameter_card)
        main_layout.addWidget(build_card)
        main_layout.addStretch(1)

        return page

    def style_mouth_joint_slider(self):
        """设置嘴唇 Joint Slider 的进度条式视觉。"""
        self.mouth_joint_slider.setStyleSheet(
            u"""
            QSlider {
                background: transparent;
            }

            QSlider::groove:horizontal {
                height: 6px;
                background: #ECEDEF;
                border: none;
                border-radius: 3px;
            }

            QSlider::sub-page:horizontal {
                background: #EC4141;
                border: none;
                border-radius: 3px;
            }

            QSlider::add-page:horizontal {
                background: #ECEDEF;
                border: none;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                margin: -5px 0px;
                background: #FFFFFF;
                border: 2px solid #EC4141;
                border-radius: 8px;
            }

            QSlider::handle:horizontal:hover {
                background: #FFF0F0;
                border-color: #F05252;
            }

            QSlider::handle:horizontal:pressed {
                background: #FFE4E4;
                border-color: #D93636;
            }
            """
        )

    def create_placeholder_page(self, title, description):
        """创建尚未完成的系统步骤页面。"""
        page = QWidget()

        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        card, card_layout = theme.make_card(page)
        card_layout.addWidget(
            theme.make_section_title(title)
        )

        description_label = QLabel(description)
        description_label.setWordWrap(True)
        theme.set_role(description_label, "muted")

        state_label = QLabel(u"开发中")
        theme.set_role(state_label, "pill")

        card_layout.addWidget(description_label)
        card_layout.addWidget(
            state_label,
            0,
            Qt.AlignLeft
        )

        main_layout.addWidget(card)
        main_layout.addStretch(1)

        return page

    def create_layouts(self):
        """创建 Wizard 主布局。"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 16)
        main_layout.setSpacing(14)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.subtitle_label)

        step_frame = QFrame()
        theme.set_role(step_frame, "sub_card")

        step_layout = QHBoxLayout(step_frame)
        step_layout.setContentsMargins(8, 8, 8, 8)
        step_layout.setSpacing(5)

        for step_button in self.step_buttons:
            step_layout.addWidget(step_button, 1)

        main_layout.addWidget(step_frame)
        main_layout.addWidget(self.page_stack, 1)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.status_label, 1)
        bottom_layout.addWidget(self.previous_button)
        bottom_layout.addWidget(self.next_button)

        main_layout.addLayout(bottom_layout)

    def create_connections(self):
        """连接 Wizard 信号。"""
        for step_button in self.step_buttons:
            step_button.clicked.connect(
                self.clicked_step_button
            )

        self.previous_button.clicked.connect(
            self.clicked_previous_button
        )
        self.next_button.clicked.connect(
            self.clicked_next_button
        )
        self.build_step1_button.clicked.connect(
            self.build_step1
        )
        self.mouth_joint_slider.valueChanged.connect(
            self.update_mouth_joint_value
        )

    # =========================================================================
    # Step State
    # =========================================================================

    def set_current_step(self, step_index):
        """切换当前步骤。"""
        if step_index < 0:
            return

        if step_index >= self.page_stack.count():
            return

        self.current_step_index = step_index
        self.page_stack.setCurrentIndex(step_index)

        self.update_step_buttons()
        self.update_navigation_buttons()

    def update_step_buttons(self):
        """更新顶部步骤按钮状态。"""
        for step_index in range(len(self.step_buttons)):
            step_button = self.step_buttons[step_index]

            current = step_index == self.current_step_index
            completed = step_index in self.completed_step_indexes

            if current:
                step_button.setEnabled(True)
                step_button.setChecked(True)
                theme.style_navigation(
                    step_button,
                    active=True
                )
                continue

            step_button.setChecked(False)
            theme.style_navigation(
                step_button,
                active=False
            )

            if completed:
                step_button.setEnabled(True)
            else:
                step_button.setEnabled(False)

    def update_navigation_buttons(self):
        """更新底部导航按钮。"""
        self.previous_button.setEnabled(
            self.current_step_index > 0
        )

        if self.current_step_index == 0:
            self.next_button.setText(u"Build 并进入下一步")
            self.next_button.setEnabled(True)
            return

        # Step 02～04 的正式 Build 尚未迁移完成，避免误标记为完成。
        self.next_button.setText(u"该步骤尚未实现")
        self.next_button.setEnabled(False)

    def clicked_step_button(self):
        """允许返回已经完成的步骤。"""
        step_button = self.sender()

        if step_button is None:
            return

        step_index = step_button.property("step_index")

        if step_index is None:
            return

        step_index = int(step_index)

        if step_index == self.current_step_index:
            return

        if step_index not in self.completed_step_indexes:
            return

        self.set_current_step(step_index)

    def clicked_previous_button(self):
        """返回上一个页面，不重新 Build。"""
        previous_index = self.current_step_index - 1

        if previous_index < 0:
            return

        self.set_current_step(previous_index)

    def clicked_next_button(self):
        """执行当前已经实现的 Step。"""
        if self.current_step_index != 0:
            return

        build_result = self.build_step1()

        if not build_result:
            return

        self.completed_step_indexes.add(0)
        self.set_current_step(1)

    # =========================================================================
    # Step 01
    # =========================================================================

    def update_mouth_joint_value(self, slider_value):
        """根据 Slider 档位实时更新嘴唇 Joint 数量显示。"""
        mouth_joint_number = slider_value * self.mouth_joint_step

        self.mouth_joint_value_label.setText(
            u"{}".format(mouth_joint_number)
        )

    def get_mouth_joint_number(self):
        """返回当前 Slider 对应的真实嘴唇 Joint 数量。"""
        slider_value = self.mouth_joint_slider.value()
        mouth_joint_number = slider_value * self.mouth_joint_step
        return mouth_joint_number

    def build_step1(self):
        """从 UI 收集参数并执行 FaceSetup.build()。"""
        face_setup = FaceSetup(
            face_head_model=self.face_head_picker.get_value(),
            face_lf_eye_model=self.face_lf_eye_picker.get_value(),
            face_rt_eye_model=self.face_rt_eye_picker.get_value(),
            upper_teech_model=self.upper_teech_picker.get_value(),
            lower_teech_model=self.lower_teech_picker.get_value(),
            face_tongue_model=self.face_tongue_picker.get_value(),
            face_gum_model=self.face_gum_picker.get_value(),
            mouth_jnt_number=self.get_mouth_joint_number()
        )

        try:
            face_setup.build()
        except Exception as error:
            self.status_label.setText(u"Face Setup Build 失败")

            QMessageBox.critical(
                self,
                u"Face Setup Build 失败",
                u"{}".format(error)
            )
            return False

        self.face_setup = face_setup
        self.completed_step_indexes.add(0)
        self.update_step_buttons()

        self.status_label.setText(
            u"Face Setup Build 完成：{} | Mouth Joint {}".format(
                face_setup.config_node,
                face_setup.mouth_jnt_number
            )
        )

        return True


def main():
    """创建 Face Rig Wizard 并返回 QWidget。"""
    window = FaceRigWizard()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
