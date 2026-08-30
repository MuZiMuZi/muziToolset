# coding=utf-8
u"""
Face Rig UI
===========

Face Rig 的分步构建界面。

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
from .face_guide import FaceGuide
from .face_setup import FaceSetup


class FaceRigWizard(QWidget):
    u"""Face Rig 分步构建窗口。"""

    def __init__(self, parent=None):
        u"""
        初始化 Face Rig UI。

        Args:
            parent (QWidget | None):
                Qt 父窗口。
        """
        super(FaceRigWizard, self).__init__(parent)

        self.current_step_index = 0
        self.completed_step_indexes = set()
        self.step_buttons = []

        self.face_setup = None
        self.face_guide = None

        # 嘴唇 Joint 数量始终以 4 为一个档位。
        # Slider 内部只保存档位，真正的 Joint 数量由档位 * 4 得到。
        self.mouth_joint_step = 4
        self.mouth_joint_minimum = 4
        self.mouth_joint_maximum = 128
        self.mouth_joint_default = 40

        self.setWindowTitle(u"Face Rig")
        self.setMinimumWidth(680)
        self.resize(760, 720)

        self.create_widgets()
        self.create_pages()
        self.create_layouts()
        self.create_connections()

        theme.style_window(self)
        self.restore_step_state()

    # =========================================================================
    # UI
    # =========================================================================

    def create_widgets(self):
        u"""创建公共控件。"""
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
        u"""创建四个步骤页面。"""
        self.step1_page = self.create_step1_page()
        self.step2_page = self.create_step2_page()
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
        u"""创建 Face Setup 页面。"""
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

    def create_step2_page(self):
        u"""创建正式的 Face Guide 页面。"""
        page = QWidget()

        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        # ---------------------------------------------------------------------
        # Guide 状态
        # ---------------------------------------------------------------------
        status_card, status_layout = theme.make_card(page)
        status_layout.addWidget(
            theme.make_section_title(u"Face Guide 状态")
        )

        status_description = QLabel(
            u"Step 02 使用 resources/face/face_guide.ma 作为 Guide 模板。"
            u"Build 负责导入或复用模板；调整完成后再执行 Finalize。"
        )
        status_description.setWordWrap(True)
        theme.set_role(status_description, "muted")

        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 0, 0, 0)
        status_row.setSpacing(8)

        self.guide_state_label = QLabel(u"未加载")
        theme.set_role(self.guide_state_label, "pill")

        self.guide_count_label = QLabel(u"Locator: 0")
        theme.set_role(self.guide_count_label, "pill")

        self.refresh_guide_button = QPushButton(u"刷新状态")
        theme.style_ghost(self.refresh_guide_button)

        status_row.addWidget(self.guide_state_label)
        status_row.addWidget(self.guide_count_label)
        status_row.addStretch(1)
        status_row.addWidget(self.refresh_guide_button)

        self.guide_details_label = QLabel(u"Guide 尚未加载")
        self.guide_details_label.setWordWrap(True)
        theme.set_role(self.guide_details_label, "muted")

        status_layout.addWidget(status_description)
        status_layout.addLayout(status_row)
        status_layout.addWidget(self.guide_details_label)

        # ---------------------------------------------------------------------
        # Template Build
        # ---------------------------------------------------------------------
        template_card, template_layout = theme.make_card(page)
        template_layout.addWidget(
            theme.make_section_title(u"Guide Template")
        )

        template_description = QLabel(
            u"Build Face Guide 会验证 Step 01、确保 Face 层级、导入或复用 Guide 模板，"
            u"并把 Guide Root / Move Ctrl / Version 保存到 Config。"
        )
        template_description.setWordWrap(True)
        theme.set_role(template_description, "muted")

        template_button_layout = QHBoxLayout()
        template_button_layout.setContentsMargins(0, 0, 0, 0)
        template_button_layout.setSpacing(8)

        self.build_step2_button = QPushButton(u"Build Face Guide")
        theme.style_primary(self.build_step2_button)

        self.reset_guide_button = QPushButton(u"Reset Guide")
        theme.style_ghost(self.reset_guide_button)

        template_button_layout.addWidget(self.build_step2_button, 1)
        template_button_layout.addWidget(self.reset_guide_button)

        template_layout.addWidget(template_description)
        template_layout.addLayout(template_button_layout)

        # ---------------------------------------------------------------------
        # Validation / Symmetry
        # ---------------------------------------------------------------------
        validation_card, validation_layout = theme.make_card(page)
        validation_layout.addWidget(
            theme.make_section_title(u"Guide Validation")
        )

        validation_description = QLabel(
            u"Repair Symmetry 用于修复 LF → RT 的 Guide 节点、Parent 和连接。"
            u"Validate 会检查必要 Guide、重复命名以及左右镜像完整性。"
        )
        validation_description.setWordWrap(True)
        theme.set_role(validation_description, "muted")

        validation_button_layout = QHBoxLayout()
        validation_button_layout.setContentsMargins(0, 0, 0, 0)
        validation_button_layout.setSpacing(8)

        self.repair_symmetry_button = QPushButton(u"Repair Symmetry")
        theme.style_ghost(self.repair_symmetry_button)

        self.validate_guide_button = QPushButton(u"Validate Guide")
        theme.style_ghost(self.validate_guide_button)

        validation_button_layout.addWidget(self.repair_symmetry_button)
        validation_button_layout.addWidget(self.validate_guide_button)
        validation_button_layout.addStretch(1)

        self.guide_validation_label = QLabel(
            u"尚未执行 Guide Validation"
        )
        self.guide_validation_label.setWordWrap(True)
        theme.set_role(self.guide_validation_label, "muted")

        validation_layout.addWidget(validation_description)
        validation_layout.addLayout(validation_button_layout)
        validation_layout.addWidget(self.guide_validation_label)

        # ---------------------------------------------------------------------
        # Finalize
        # ---------------------------------------------------------------------
        finalize_card, finalize_layout = theme.make_card(page)
        finalize_layout.addWidget(
            theme.make_section_title(u"Step 02 Finalize")
        )

        finalize_description = QLabel(
            u"Finalize 不创建正式 Rig。它只确认 Guide 可以交给后续 Builder，"
            u"保存当前 Guide Config，并把 Step 02 标记为完成。"
        )
        finalize_description.setWordWrap(True)
        theme.set_role(finalize_description, "muted")

        self.finalize_step2_button = QPushButton(u"Finalize Face Guide")
        theme.style_primary(self.finalize_step2_button)

        finalize_layout.addWidget(finalize_description)
        finalize_layout.addWidget(self.finalize_step2_button)

        main_layout.addWidget(status_card)
        main_layout.addWidget(template_card)
        main_layout.addWidget(validation_card)
        main_layout.addWidget(finalize_card)
        main_layout.addStretch(1)

        return page

    def style_mouth_joint_slider(self):
        u"""设置嘴唇 Joint Slider 的进度条式视觉。"""
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
        u"""创建尚未完成的系统步骤页面。"""
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
        u"""创建 UI 主布局。"""
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
        u"""连接 UI 信号。"""
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

        self.refresh_guide_button.clicked.connect(
            self.refresh_guide_state
        )
        self.build_step2_button.clicked.connect(
            self.build_step2
        )
        self.reset_guide_button.clicked.connect(
            self.reset_step2_guide
        )
        self.repair_symmetry_button.clicked.connect(
            self.repair_step2_symmetry
        )
        self.validate_guide_button.clicked.connect(
            self.validate_step2_guides
        )
        self.finalize_step2_button.clicked.connect(
            self.finalize_step2
        )

    # =========================================================================
    # Step State
    # =========================================================================

    def get_face_guide(self, refresh=False):
        u"""返回当前 UI 使用的 FaceGuide 实例。"""
        if refresh:
            self.face_guide = None

        if self.face_guide is None:
            self.face_guide = FaceGuide()

        return self.face_guide

    def restore_step_state(self):
        u"""
        从 Face Config 恢复已经完成的 Step，并进入第一个未完成步骤。

        新场景没有 Config 时保持在 Step 01。
        """
        self.completed_step_indexes.clear()

        face_guide = self.get_face_guide(
            refresh=True
        )

        if not face_guide.config_node_exists():
            self.set_current_step(0)
            self.refresh_guide_state()
            return

        try:
            step_status = face_guide.get_step_status(
                last_step=4
            )
        except Exception:
            self.set_current_step(0)
            self.refresh_guide_state()
            return

        current_step_index = 0
        found_incomplete_step = False

        step_value = 1

        while step_value <= 4:
            completed = bool(
                step_status.get(
                    step_value,
                    False
                )
            )

            if completed:
                self.completed_step_indexes.add(
                    step_value - 1
                )
                step_value += 1
                continue

            current_step_index = step_value - 1
            found_incomplete_step = True
            break

        if not found_incomplete_step:
            current_step_index = 3

        self.set_current_step(
            current_step_index
        )
        self.refresh_guide_state()

    def invalidate_ui_steps_after(self, step_index):
        u"""把指定 UI Step 之后的本地完成状态清除。"""
        next_step_index = step_index + 1

        while next_step_index < len(self.step_buttons):
            self.completed_step_indexes.discard(
                next_step_index
            )
            next_step_index += 1

        self.update_step_buttons()
        self.update_navigation_buttons()

    def set_current_step(self, step_index):
        u"""切换当前步骤。"""
        if step_index < 0:
            return

        if step_index >= self.page_stack.count():
            return

        self.current_step_index = step_index
        self.page_stack.setCurrentIndex(step_index)

        if step_index == 1:
            self.refresh_guide_state()

        self.update_step_buttons()
        self.update_navigation_buttons()

    def update_step_buttons(self):
        u"""更新顶部步骤按钮状态。"""
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
        u"""更新底部导航按钮。"""
        self.previous_button.setEnabled(
            self.current_step_index > 0
        )

        if self.current_step_index == 0:
            self.next_button.setText(
                u"Build 并进入下一步"
            )
            self.next_button.setEnabled(True)
            return

        if self.current_step_index == 1:
            if 1 in self.completed_step_indexes:
                self.next_button.setText(
                    u"进入下一步"
                )
                self.next_button.setEnabled(True)
                return

            face_guide = self.get_face_guide()
            guide_exists = face_guide.guide_exists()

            self.next_button.setText(
                u"Finalize 并进入下一步"
            )
            self.next_button.setEnabled(
                bool(guide_exists)
            )
            return

        # Step 03～04 尚未正式接入。
        self.next_button.setText(u"该步骤尚未实现")
        self.next_button.setEnabled(False)

    def clicked_step_button(self):
        u"""允许返回已经完成的步骤。"""
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
        u"""返回上一个页面，不重新 Build。"""
        previous_index = self.current_step_index - 1

        if previous_index < 0:
            return

        self.set_current_step(previous_index)

    def clicked_next_button(self):
        u"""执行当前已经接入的 Step。"""
        if self.current_step_index == 0:
            build_result = self.build_step1()

            if not build_result:
                return

            self.set_current_step(1)
            return

        if self.current_step_index == 1:
            if 1 not in self.completed_step_indexes:
                finalize_result = self.finalize_step2()

                if not finalize_result:
                    return

            self.set_current_step(2)
            return

    # =========================================================================
    # Step 01
    # =========================================================================

    def update_mouth_joint_value(self, slider_value):
        u"""根据 Slider 档位实时更新嘴唇 Joint 数量显示。"""
        mouth_joint_number = slider_value * self.mouth_joint_step

        self.mouth_joint_value_label.setText(
            u"{}".format(mouth_joint_number)
        )

    def get_mouth_joint_number(self):
        u"""返回当前 Slider 对应的真实嘴唇 Joint 数量。"""
        slider_value = self.mouth_joint_slider.value()
        mouth_joint_number = slider_value * self.mouth_joint_step
        return mouth_joint_number

    def build_step1(self):
        u"""从 UI 收集参数并执行 FaceSetup.build()。"""
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
        self.invalidate_ui_steps_after(0)

        # Step 01 重新 Build 后，重新创建 FaceGuide，
        # 让它读取刚刚写入 Config 的最新 Setup 数据。
        self.get_face_guide(
            refresh=True
        )

        self.status_label.setText(
            u"Face Setup Build 完成：{} | Mouth Joint {}".format(
                face_setup.config_node,
                face_setup.mouth_jnt_number
            )
        )

        self.refresh_guide_state()

        return True

    # =========================================================================
    # Step 02
    # =========================================================================

    def refresh_guide_state(self):
        u"""刷新 Step 02 Guide 的场景状态显示。"""
        if not hasattr(self, "guide_state_label"):
            return False

        face_guide = self.get_face_guide()

        try:
            guide_exists = face_guide.guide_exists()
        except Exception:
            guide_exists = False

        if not guide_exists:
            self.completed_step_indexes.discard(1)
            self.completed_step_indexes.discard(2)
            self.completed_step_indexes.discard(3)

            self.guide_state_label.setText(
                u"未加载"
            )
            self.guide_count_label.setText(
                u"Locator: 0"
            )
            self.guide_details_label.setText(
                u"Guide 尚未加载。请先完成 Step 01，然后执行 Build Face Guide。"
            )

            self.build_step2_button.setEnabled(True)
            self.reset_guide_button.setEnabled(False)
            self.repair_symmetry_button.setEnabled(False)
            self.validate_guide_button.setEnabled(False)
            self.finalize_step2_button.setEnabled(False)

            self.update_navigation_buttons()
            return False

        guide_count = len(
            face_guide.get_guide_locators()
        )

        step_completed = False

        if face_guide.config_node_exists():
            try:
                step_completed = face_guide.is_step_completed(
                    step_value=2
                )
            except Exception:
                step_completed = False

        if step_completed:
            self.guide_state_label.setText(
                u"已 Finalize"
            )
            self.completed_step_indexes.add(1)
        else:
            self.completed_step_indexes.discard(1)
            self.completed_step_indexes.discard(2)
            self.completed_step_indexes.discard(3)

            self.guide_state_label.setText(
                u"已加载"
            )

        self.guide_count_label.setText(
            u"Locator: {}".format(
                guide_count
            )
        )

        guide_root = face_guide.guide_root
        guide_move_ctrl = face_guide.guide_move_ctrl

        self.guide_details_label.setText(
            u"Root: {}\nMove Ctrl: {}\nGuide Version: {}".format(
                guide_root,
                guide_move_ctrl,
                face_guide.guide_version
            )
        )

        self.build_step2_button.setEnabled(True)
        self.reset_guide_button.setEnabled(True)
        self.repair_symmetry_button.setEnabled(True)
        self.validate_guide_button.setEnabled(True)
        self.finalize_step2_button.setEnabled(True)

        self.update_step_buttons()
        self.update_navigation_buttons()

        return True

    def build_step2(self):
        u"""执行 FaceGuide.build()，导入或复用 Guide Template。"""
        face_guide = self.get_face_guide(
            refresh=True
        )

        try:
            result = face_guide.build()
        except Exception as error:
            self.status_label.setText(
                u"Face Guide Build 失败"
            )

            QMessageBox.critical(
                self,
                u"Face Guide Build 失败",
                u"{}".format(error)
            )
            self.refresh_guide_state()
            return False

        # FaceGuide.build() 明确让 Step 02 保持未完成，
        # 因此 UI 本地状态也同步清除 Step 02 以及之后的状态。
        self.completed_step_indexes.discard(1)
        self.invalidate_ui_steps_after(1)

        imported = False

        if isinstance(result, dict):
            imported = bool(
                result.get(
                    "imported",
                    False
                )
            )

        if imported:
            self.status_label.setText(
                u"Face Guide 模板导入完成"
            )
        else:
            self.status_label.setText(
                u"Face Guide 已存在，复用当前 Guide"
            )

        self.guide_validation_label.setText(
            u"Guide 已加载，请贴合模型后执行 Validate / Finalize。"
        )

        self.refresh_guide_state()
        return True

    def get_messagebox_standard_buttons(self):
        u"""返回兼容 PySide2 / PySide6 的 QMessageBox Yes / No。"""
        try:
            yes_button = QMessageBox.StandardButton.Yes
            no_button = QMessageBox.StandardButton.No
        except AttributeError:
            yes_button = QMessageBox.Yes
            no_button = QMessageBox.No

        return yes_button, no_button

    def reset_step2_guide(self):
        u"""删除当前 Guide 内容并重新导入原始模板。"""
        yes_button, no_button = self.get_messagebox_standard_buttons()

        reply = QMessageBox.question(
            self,
            u"Reset Face Guide",
            u"Reset 会删除当前 Face Guide 的手动调整，并重新导入原始模板。\n\n是否继续？",
            yes_button | no_button,
            no_button
        )

        if reply != yes_button:
            return False

        face_guide = self.get_face_guide(
            refresh=True
        )

        try:
            face_guide.validate_setup()
            face_guide.reset_guide()
        except Exception as error:
            self.status_label.setText(
                u"Face Guide Reset 失败"
            )

            QMessageBox.critical(
                self,
                u"Face Guide Reset 失败",
                u"{}".format(error)
            )
            self.refresh_guide_state()
            return False

        self.completed_step_indexes.discard(1)
        self.invalidate_ui_steps_after(1)

        self.guide_validation_label.setText(
            u"Guide 已重置，请重新贴合模型。"
        )
        self.status_label.setText(
            u"Face Guide Reset 完成"
        )

        self.refresh_guide_state()
        return True

    def repair_step2_symmetry(self):
        u"""执行 FaceGuide.repair_symmetry() 并重新校验 Guide。"""
        face_guide = self.get_face_guide()

        try:
            face_guide.validate_setup()

            if not face_guide.guide_exists():
                raise RuntimeError(
                    u"Face Guide 尚未加载。"
                )

            repair_result = face_guide.repair_symmetry()

            # Repair 会修改 Guide 层级 / 连接。
            # 已经 Finalize 的 Step 02 需要重新确认。
            face_guide.set_step_completed(
                completed=False
            )
            face_guide.invalidate_later_steps()

            validation = face_guide.validate_guides(
                check_symmetry=True
            )
        except Exception as error:
            self.status_label.setText(
                u"Repair Symmetry 失败"
            )

            QMessageBox.critical(
                self,
                u"Repair Symmetry 失败",
                u"{}".format(error)
            )
            return False

        self.completed_step_indexes.discard(1)
        self.invalidate_ui_steps_after(1)

        repair_count = 0

        if isinstance(repair_result, dict):
            repair_items = repair_result.get(
                "repairs",
                []
            )
            repair_count = len(repair_items)

        self.show_guide_validation(
            validation
        )

        self.status_label.setText(
            u"Repair Symmetry 完成：处理 {} 组 Guide".format(
                repair_count
            )
        )

        self.refresh_guide_state()
        return True

    def validate_step2_guides(self):
        u"""执行 FaceGuide.validate_guides()。"""
        face_guide = self.get_face_guide()

        try:
            face_guide.validate_setup()
            validation = face_guide.validate_guides(
                check_symmetry=True
            )
        except Exception as error:
            self.status_label.setText(
                u"Face Guide Validation 失败"
            )

            QMessageBox.critical(
                self,
                u"Face Guide Validation 失败",
                u"{}".format(error)
            )
            return False

        self.show_guide_validation(
            validation
        )

        if validation["valid"]:
            self.status_label.setText(
                u"Face Guide Validation 通过"
            )
            return True

        self.status_label.setText(
            u"Face Guide Validation 未通过"
        )
        return False

    def format_guide_validation(self, validation):
        u"""把 FaceGuide.validate_guides() 的结果转换成 UI 文本。"""
        if not isinstance(validation, dict):
            return u"没有可显示的 Validation 结果。"

        guide_count = validation.get(
            "guide_count",
            0
        )
        valid = bool(
            validation.get(
                "valid",
                False
            )
        )

        lines = []

        if valid:
            lines.append(
                u"Validation 通过 · Locator {}".format(
                    guide_count
                )
            )
        else:
            lines.append(
                u"Validation 未通过 · Locator {}".format(
                    guide_count
                )
            )

        errors = validation.get(
            "errors",
            []
        )

        for error in errors:
            lines.append(
                u"- {}".format(
                    error
                )
            )

        warnings = validation.get(
            "warnings",
            []
        )

        for warning in warnings:
            lines.append(
                u"Warning: {}".format(
                    warning
                )
            )

        return u"\n".join(lines)

    def show_guide_validation(self, validation):
        u"""把 Guide Validation 结果显示到 Step 02 页面。"""
        text = self.format_guide_validation(
            validation
        )

        self.guide_validation_label.setText(
            text
        )

    def finalize_step2(self):
        u"""执行 FaceGuide.finalize() 并把 Step 02 标记为完成。"""
        face_guide = self.get_face_guide()

        try:
            validation = face_guide.finalize(
                check_symmetry=True
            )
        except Exception as error:
            # Finalize 失败时再读取一次结构化 Validation，
            # 让页面上可以直接看到全部问题。
            try:
                validation = face_guide.validate_guides(
                    check_symmetry=True
                )
                self.show_guide_validation(
                    validation
                )
            except Exception:
                pass

            self.status_label.setText(
                u"Face Guide Finalize 失败"
            )

            QMessageBox.critical(
                self,
                u"Face Guide Finalize 失败",
                u"{}".format(error)
            )
            self.refresh_guide_state()
            return False

        self.completed_step_indexes.add(1)
        self.invalidate_ui_steps_after(1)

        self.show_guide_validation(
            validation
        )

        self.status_label.setText(
            u"Face Guide Finalize 完成：{} 个 Locator".format(
                validation.get(
                    "guide_count",
                    0
                )
            )
        )

        self.refresh_guide_state()
        return True


def main():
    u"""创建 Face Rig UI 并返回 QWidget。"""
    window = FaceRigWizard()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
