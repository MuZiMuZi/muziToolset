# coding=utf-8
u"""
Face Rig UI
===========

Face Rig 的分步构建界面。

设计原则：
    - UI 只收集参数、展示状态和提供当前 Step 的必要辅助操作；
    - 真正的 Step 逻辑由 FaceSetup / FaceGuide 等 System 类负责；
    - 进入 Step 02 时自动导入或复用 resources/face/face_guide.ma；
    - Step 02 不暴露 Build / Reset / Refresh / Validate 等内部流程按钮；
    - Step 02 只保留 Guide Mirror 和后续 Component 使用的 Controller Settings；
    - Controller Size 使用 QSpinBox；
    - Controller Color 使用 Maya Index Color Slider + Index + 方块预览；
    - 底部只保留一个“下一步”，统一用于提交 / 重新提交当前 Step；
    - 返回旧 Step 修改参数后再次点击“下一步”，必须重新执行当前 Step，
      并让后续旧结果失效；
    - 不在模块 import 时 reload 依赖；
    - 使用根包 ui 的统一 Theme 与通用 Widget。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QSlider
    from PySide2.QtWidgets import QSpinBox
    from PySide2.QtWidgets import QStackedWidget
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSlider
    from PySide6.QtWidgets import QSpinBox
    from PySide6.QtWidgets import QStackedWidget
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ...ui import theme
from ...ui.widgets import MayaIndexColorSlider
from ...ui.widgets import MayaObjectPicker
from . import guide_mirror
from . import guide_settings
from . import guide_template
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

        # Controller Settings 从 Config 回填 UI 时不触发 Dirty State。
        self.loading_controller_settings = False

        # 嘴唇 Joint 数量始终以 4 为一个档位。
        self.mouth_joint_step = 4
        self.mouth_joint_minimum = 4
        self.mouth_joint_maximum = 128
        self.mouth_joint_default = 40

        self.controller_size_widgets = {}
        self.controller_color_widgets = {}

        self.setWindowTitle(
            u"Face Rig"
        )
        self.setMinimumWidth(
            680
        )
        self.resize(
            760,
            700
        )

        self.create_widgets()
        self.create_pages()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self
        )
        self.restore_step_state()

    # =========================================================================
    # UI
    # =========================================================================

    def create_widgets(self):
        u"""创建公共控件。"""
        self.title_label = theme.make_title(
            u"Face Rig"
        )
        self.subtitle_label = theme.make_subtitle(
            u"按步骤建立面部绑定。Step 02 会自动加载 Guide，调整完成后点击下一步提交。"
        )

        step_names = [
            u"01  Setup",
            u"02  Guide",
            u"03  Build",
            u"04  Finalize",
        ]

        for step_index in range(
                len(step_names)
        ):
            step_name = step_names[
                step_index
            ]

            step_button = QPushButton(
                step_name
            )
            step_button.setCheckable(
                True
            )
            step_button.setProperty(
                "step_index",
                step_index
            )
            theme.style_navigation(
                step_button
            )

            self.step_buttons.append(
                step_button
            )

        self.page_stack = QStackedWidget()

        self.next_button = QPushButton(
            u"下一步"
        )
        theme.style_primary(
            self.next_button
        )

        self.status_label = QLabel(
            u"准备就绪"
        )
        theme.set_role(
            self.status_label,
            "muted"
        )

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

        self.page_stack.addWidget(
            self.step1_page
        )
        self.page_stack.addWidget(
            self.step2_page
        )
        self.page_stack.addWidget(
            self.step3_page
        )
        self.page_stack.addWidget(
            self.step4_page
        )

    def create_step1_page(self):
        u"""创建 Face Setup 页面。"""
        page = QWidget()

        main_layout = QVBoxLayout(
            page
        )
        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        main_layout.setSpacing(
            12
        )

        # ---------------------------------------------------------------------
        # 模型输入
        # ---------------------------------------------------------------------
        model_card, model_layout = theme.make_card(
            page
        )
        model_layout.addWidget(
            theme.make_section_title(
                u"模型输入"
            )
        )

        model_description = QLabel(
            u"Head 为必填项，其它模型可以留空。拾取时使用 Maya 当前最后选择对象。"
        )
        model_description.setWordWrap(
            True
        )
        theme.set_role(
            model_description,
            "muted"
        )
        model_layout.addWidget(
            model_description
        )

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

        model_layout.addWidget(
            self.face_head_picker
        )
        model_layout.addWidget(
            self.face_lf_eye_picker
        )
        model_layout.addWidget(
            self.face_rt_eye_picker
        )
        model_layout.addWidget(
            self.upper_teech_picker
        )
        model_layout.addWidget(
            self.lower_teech_picker
        )
        model_layout.addWidget(
            self.face_tongue_picker
        )
        model_layout.addWidget(
            self.face_gum_picker
        )

        # ---------------------------------------------------------------------
        # 构建参数
        # ---------------------------------------------------------------------
        parameter_card, parameter_layout = theme.make_card(
            page
        )
        parameter_layout.addWidget(
            theme.make_section_title(
                u"构建参数"
            )
        )

        mouth_layout = QHBoxLayout()
        mouth_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        mouth_layout.setSpacing(
            10
        )

        mouth_label = QLabel(
            u"嘴唇 Joint 数量"
        )
        mouth_label.setMinimumWidth(
            120
        )

        self.mouth_joint_slider = QSlider(
            Qt.Horizontal
        )
        self.mouth_joint_slider.setMinimum(
            int(
                self.mouth_joint_minimum
                / self.mouth_joint_step
            )
        )
        self.mouth_joint_slider.setMaximum(
            int(
                self.mouth_joint_maximum
                / self.mouth_joint_step
            )
        )
        self.mouth_joint_slider.setSingleStep(
            1
        )
        self.mouth_joint_slider.setPageStep(
            2
        )
        self.mouth_joint_slider.setValue(
            int(
                self.mouth_joint_default
                / self.mouth_joint_step
            )
        )
        self.mouth_joint_slider.setMinimumWidth(
            280
        )
        self.style_mouth_joint_slider()

        self.mouth_joint_value_label = QLabel(
            u"{}".format(
                self.mouth_joint_default
            )
        )
        self.mouth_joint_value_label.setMinimumWidth(
            46
        )
        self.mouth_joint_value_label.setAlignment(
            Qt.AlignCenter
        )
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
        theme.set_role(
            mouth_hint,
            "muted"
        )

        mouth_layout.addWidget(
            mouth_label
        )
        mouth_layout.addWidget(
            self.mouth_joint_slider,
            1
        )
        mouth_layout.addWidget(
            self.mouth_joint_value_label
        )
        mouth_layout.addWidget(
            mouth_hint
        )

        parameter_layout.addLayout(
            mouth_layout
        )

        step_hint = QLabel(
            u"参数调整完成后点击窗口底部“下一步”。Step 01 成功后会自动进入并加载 Face Guide。"
        )
        step_hint.setWordWrap(
            True
        )
        theme.set_role(
            step_hint,
            "muted"
        )

        main_layout.addWidget(
            model_card
        )
        main_layout.addWidget(
            parameter_card
        )
        main_layout.addWidget(
            step_hint
        )
        main_layout.addStretch(
            1
        )

        return page

    def create_step2_page(self):
        u"""
        创建 Face Guide 编辑页面。

        Step 02 进入时自动导入或复用 Guide Template。
        页面只保留：
            1. Guide 编辑说明；
            2. 左右 Guide Mirror；
            3. Controller Global / Side / Module Settings。
        """
        page = QWidget()

        main_layout = QVBoxLayout(
            page
        )
        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        main_layout.setSpacing(
            12
        )

        # ---------------------------------------------------------------------
        # Guide
        # ---------------------------------------------------------------------
        guide_card, guide_layout = theme.make_card(
            page
        )
        guide_layout.addWidget(
            theme.make_section_title(
                u"Face Guide"
            )
        )

        guide_description = QLabel(
            u"进入 Step 02 时会自动导入或复用 resources/face/face_guide.ma。"
            u"请直接在 Maya 视图中调整定位器；完成后点击窗口底部“下一步”。"
        )
        guide_description.setWordWrap(
            True
        )
        theme.set_role(
            guide_description,
            "muted"
        )

        self.guide_summary_label = QLabel(
            u"等待加载 Face Guide"
        )
        self.guide_summary_label.setWordWrap(
            True
        )
        theme.set_role(
            self.guide_summary_label,
            "pill"
        )

        guide_layout.addWidget(
            guide_description
        )
        guide_layout.addWidget(
            self.guide_summary_label,
            0,
            Qt.AlignLeft
        )

        # ---------------------------------------------------------------------
        # Mirror
        # ---------------------------------------------------------------------
        mirror_card, mirror_layout = theme.make_card(
            page
        )
        mirror_layout.addWidget(
            theme.make_section_title(
                u"Guide Mirror"
            )
        )

        mirror_description = QLabel(
            u"镜像只复制当前 Guide 状态，不建立永久左右连接。镜像后 lf / rt 两侧仍可独立调整。"
        )
        mirror_description.setWordWrap(
            True
        )
        theme.set_role(
            mirror_description,
            "muted"
        )

        mirror_button_layout = QHBoxLayout()
        mirror_button_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        mirror_button_layout.setSpacing(
            8
        )

        self.mirror_lf_to_rt_button = QPushButton(
            u"LF  →  RT"
        )
        self.mirror_rt_to_lf_button = QPushButton(
            u"RT  →  LF"
        )

        theme.style_ghost(
            self.mirror_lf_to_rt_button
        )
        theme.style_ghost(
            self.mirror_rt_to_lf_button
        )

        mirror_button_layout.addWidget(
            self.mirror_lf_to_rt_button
        )
        mirror_button_layout.addWidget(
            self.mirror_rt_to_lf_button
        )
        mirror_button_layout.addStretch(
            1
        )

        mirror_layout.addWidget(
            mirror_description
        )
        mirror_layout.addLayout(
            mirror_button_layout
        )

        # ---------------------------------------------------------------------
        # Controller Settings
        # ---------------------------------------------------------------------
        controller_card, controller_layout = theme.make_card(
            page
        )
        controller_layout.addWidget(
            theme.make_section_title(
                u"Controller Settings"
            )
        )

        controller_description = QLabel(
            u"Controller Size 使用整数数字选择框，默认全部为 1。"
            u"Side Color 使用 Maya Index Color 滑条，并实时显示颜色预览。"
        )
        controller_description.setWordWrap(
            True
        )
        theme.set_role(
            controller_description,
            "muted"
        )
        controller_layout.addWidget(
            controller_description
        )

        settings_grid = QGridLayout()
        settings_grid.setContentsMargins(
            0,
            4,
            0,
            0
        )
        settings_grid.setHorizontalSpacing(
            14
        )
        settings_grid.setVerticalSpacing(
            10
        )

        # ---------------------------------------------------------------------
        # Global Size
        # ---------------------------------------------------------------------
        global_scale_label = QLabel(
            u"Global Scale"
        )
        self.face_ctrl_global_scale_spin = self.create_size_spin_box(
            value=1
        )

        settings_grid.addWidget(
            global_scale_label,
            0,
            0
        )
        settings_grid.addWidget(
            self.face_ctrl_global_scale_spin,
            0,
            1
        )

        # ---------------------------------------------------------------------
        # Side Color
        # ---------------------------------------------------------------------
        color_title = QLabel(
            u"Side Color"
        )
        theme.set_role(
            color_title,
            "muted"
        )
        settings_grid.addWidget(
            color_title,
            1,
            0,
            1,
            2
        )

        side_items = [
            ("lf", u"LF", 6),
            ("rt", u"RT", 13),
            ("md", u"MD", 17),
        ]

        row = 2

        for side_item in side_items:
            side = side_item[0]
            label_text = side_item[1]
            default_color = side_item[2]

            side_label = QLabel(
                label_text
            )
            color_widget = MayaIndexColorSlider(
                value=default_color
            )

            self.controller_color_widgets[
                side
            ] = color_widget

            settings_grid.addWidget(
                side_label,
                row,
                0
            )
            settings_grid.addWidget(
                color_widget,
                row,
                1
            )

            row += 1

        # ---------------------------------------------------------------------
        # Module Size
        # ---------------------------------------------------------------------
        module_title = QLabel(
            u"Module Size"
        )
        theme.set_role(
            module_title,
            "muted"
        )
        settings_grid.addWidget(
            module_title,
            1,
            2,
            1,
            2
        )

        # 按面部从上到下排列。
        module_items = [
            ("brow", u"Brow"),
            ("eye", u"Eye"),
            ("eyelid", u"Eyelid"),
            ("nose", u"Nose"),
            ("cheek", u"Cheek"),
            ("lip", u"Lip"),
            ("jaw", u"Jaw"),
        ]

        module_row = 2

        for module_item in module_items:
            module_name = module_item[0]
            label_text = module_item[1]

            module_label = QLabel(
                label_text
            )
            size_spin = self.create_size_spin_box(
                value=1
            )

            self.controller_size_widgets[
                module_name
            ] = size_spin

            settings_grid.addWidget(
                module_label,
                module_row,
                2
            )
            settings_grid.addWidget(
                size_spin,
                module_row,
                3
            )

            module_row += 1

        settings_grid.setColumnStretch(
            1,
            1
        )
        settings_grid.setColumnStretch(
            3,
            1
        )

        controller_layout.addLayout(
            settings_grid
        )

        next_hint = QLabel(
            u"下一步会自动检查 Guide，并把当前 Controller Settings 保存到 Face Config，再进入 Step 03。"
        )
        next_hint.setWordWrap(
            True
        )
        theme.set_role(
            next_hint,
            "muted"
        )

        main_layout.addWidget(
            guide_card
        )
        main_layout.addWidget(
            mirror_card
        )
        main_layout.addWidget(
            controller_card
        )
        main_layout.addWidget(
            next_hint
        )
        main_layout.addStretch(
            1
        )

        return page

    def create_size_spin_box(
            self,
            value=1
    ):
        u"""
        创建 Face Controller Size 使用的统一 QSpinBox。

        Args:
            value (int):
                默认大小。

        Returns:
            QSpinBox:
            数字选择框。
        """
        spin_box = QSpinBox()
        spin_box.setRange(
            1,
            100
        )
        spin_box.setSingleStep(
            1
        )
        spin_box.setValue(
            int(value)
        )
        spin_box.setMinimumWidth(
            90
        )
        return spin_box

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

    def create_placeholder_page(
            self,
            title,
            description
    ):
        u"""创建尚未完成的系统步骤页面。"""
        page = QWidget()

        main_layout = QVBoxLayout(
            page
        )
        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        main_layout.setSpacing(
            12
        )

        card, card_layout = theme.make_card(
            page
        )
        card_layout.addWidget(
            theme.make_section_title(
                title
            )
        )

        description_label = QLabel(
            description
        )
        description_label.setWordWrap(
            True
        )
        theme.set_role(
            description_label,
            "muted"
        )

        state_label = QLabel(
            u"开发中"
        )
        theme.set_role(
            state_label,
            "pill"
        )

        card_layout.addWidget(
            description_label
        )
        card_layout.addWidget(
            state_label,
            0,
            Qt.AlignLeft
        )

        main_layout.addWidget(
            card
        )
        main_layout.addStretch(
            1
        )

        return page

    def create_layouts(self):
        u"""创建 UI 主布局。"""
        main_layout = QVBoxLayout(
            self
        )
        main_layout.setContentsMargins(
            18,
            18,
            18,
            16
        )
        main_layout.setSpacing(
            14
        )

        main_layout.addWidget(
            self.title_label
        )
        main_layout.addWidget(
            self.subtitle_label
        )

        step_frame = QFrame()
        theme.set_role(
            step_frame,
            "sub_card"
        )

        step_layout = QHBoxLayout(
            step_frame
        )
        step_layout.setContentsMargins(
            8,
            8,
            8,
            8
        )
        step_layout.setSpacing(
            5
        )

        for step_button in self.step_buttons:
            step_layout.addWidget(
                step_button,
                1
            )

        main_layout.addWidget(
            step_frame
        )
        main_layout.addWidget(
            self.page_stack,
            1
        )

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        bottom_layout.setSpacing(
            10
        )

        bottom_layout.addWidget(
            self.status_label,
            1
        )
        bottom_layout.addWidget(
            self.next_button
        )

        main_layout.addLayout(
            bottom_layout
        )

    def create_connections(self):
        u"""连接 UI 信号。"""
        for step_button in self.step_buttons:
            step_button.clicked.connect(
                self.clicked_step_button
            )

        self.next_button.clicked.connect(
            self.clicked_next_button
        )

        self.mouth_joint_slider.valueChanged.connect(
            self.update_mouth_joint_value
        )

        self.mirror_lf_to_rt_button.clicked.connect(
            self.mirror_lf_to_rt
        )
        self.mirror_rt_to_lf_button.clicked.connect(
            self.mirror_rt_to_lf
        )

        self.face_ctrl_global_scale_spin.valueChanged.connect(
            self.controller_settings_changed
        )

        for side in self.controller_color_widgets:
            color_widget = self.controller_color_widgets.get(
                side
            )
            color_widget.value_changed.connect(
                self.controller_settings_changed
            )

        for module_name in self.controller_size_widgets:
            size_spin = self.controller_size_widgets.get(
                module_name
            )
            size_spin.valueChanged.connect(
                self.controller_settings_changed
            )

    # =========================================================================
    # Step State
    # =========================================================================

    def get_face_guide(
            self,
            refresh=False
    ):
        u"""返回当前 UI 使用的 FaceGuide 实例。"""
        if refresh:
            self.face_guide = None

        if self.face_guide is None:
            self.face_guide = FaceGuide()

        return self.face_guide

    def restore_step_state(self):
        u"""从 Face Config 恢复已经完成的 Step，并进入第一个未完成步骤。"""
        self.completed_step_indexes.clear()

        face_guide = self.get_face_guide(
            refresh=True
        )

        if not face_guide.config_node_exists():
            self.set_current_step(
                0
            )
            return

        try:
            step_status = face_guide.get_step_status(
                last_step=4
            )
        except Exception:
            self.set_current_step(
                0
            )
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

    def invalidate_ui_steps_after(
            self,
            step_index
    ):
        u"""把指定 UI Step 之后的本地完成状态清除。"""
        next_step_index = step_index + 1

        while next_step_index < len(
                self.step_buttons
        ):
            self.completed_step_indexes.discard(
                next_step_index
            )
            next_step_index += 1

        self.update_step_buttons()
        self.update_navigation_buttons()

    def set_current_step(
            self,
            step_index
    ):
        u"""切换当前步骤，并执行对应 Step 的进入逻辑。"""
        if step_index < 0:
            return

        if step_index >= self.page_stack.count():
            return

        self.current_step_index = step_index
        self.page_stack.setCurrentIndex(
            step_index
        )

        if step_index == 1:
            self.enter_step2()

        self.update_step_buttons()
        self.update_navigation_buttons()

    def update_step_buttons(self):
        u"""更新顶部步骤按钮状态。"""
        for step_index in range(
                len(self.step_buttons)
        ):
            step_button = self.step_buttons[
                step_index
            ]

            current = (
                step_index
                == self.current_step_index
            )
            completed = (
                step_index
                in self.completed_step_indexes
            )

            if current:
                step_button.setEnabled(
                    True
                )
                step_button.setChecked(
                    True
                )
                theme.style_navigation(
                    step_button,
                    active=True
                )
                continue

            step_button.setChecked(
                False
            )
            theme.style_navigation(
                step_button,
                active=False
            )

            if completed:
                step_button.setEnabled(
                    True
                )
            else:
                step_button.setEnabled(
                    False
                )

    def update_navigation_buttons(self):
        u"""更新底部“下一步”状态。"""
        self.next_button.setText(
            u"下一步"
        )

        if self.current_step_index == 0:
            self.next_button.setEnabled(
                True
            )
            return

        if self.current_step_index == 1:
            face_guide = self.get_face_guide()

            try:
                guide_exists = face_guide.guide_exists()
            except Exception:
                guide_exists = False

            self.next_button.setEnabled(
                bool(
                    guide_exists
                )
            )
            return

        self.next_button.setEnabled(
            False
        )

    def clicked_step_button(self):
        u"""通过顶部导航返回已经完成的步骤。"""
        step_button = self.sender()

        if step_button is None:
            return

        step_index = step_button.property(
            "step_index"
        )

        if step_index is None:
            return

        step_index = int(
            step_index
        )

        if step_index == self.current_step_index:
            return

        if step_index not in self.completed_step_indexes:
            return

        self.set_current_step(
            step_index
        )

    def clicked_next_button(self):
        u"""重新提交当前已经接入的 Step，并在成功后进入下一个步骤。"""
        if self.current_step_index == 0:
            build_result = self.build_step1()

            if not build_result:
                return

            self.set_current_step(
                1
            )
            return

        if self.current_step_index == 1:
            finalize_result = self.finalize_step2()

            if not finalize_result:
                return

            self.set_current_step(
                2
            )
            return

    # =========================================================================
    # Step 01
    # =========================================================================

    def update_mouth_joint_value(
            self,
            slider_value
    ):
        u"""根据 Slider 档位实时更新嘴唇 Joint 数量显示。"""
        mouth_joint_number = (
            slider_value
            * self.mouth_joint_step
        )

        self.mouth_joint_value_label.setText(
            u"{}".format(
                mouth_joint_number
            )
        )

    def get_mouth_joint_number(self):
        u"""返回当前 Slider 对应的真实嘴唇 Joint 数量。"""
        slider_value = self.mouth_joint_slider.value()

        mouth_joint_number = (
            slider_value
            * self.mouth_joint_step
        )

        return mouth_joint_number

    def build_step1(self):
        u"""从 UI 重新收集当前参数并执行 FaceSetup.run_step()。"""
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
            face_setup.run_step()
        except Exception as error:
            self.status_label.setText(
                u"Face Setup Build 失败"
            )

            QMessageBox.critical(
                self,
                u"Face Setup Build 失败",
                u"{}".format(
                    error
                )
            )
            return False

        self.face_setup = face_setup

        self.completed_step_indexes.add(
            0
        )
        self.invalidate_ui_steps_after(
            0
        )

        self.get_face_guide(
            refresh=True
        )

        self.status_label.setText(
            u"Face Setup 完成：{} | Mouth Joint {}".format(
                face_setup.config_node,
                face_setup.mouth_jnt_number
            )
        )

        return True

    # =========================================================================
    # Step 02 - Enter / Guide
    # =========================================================================

    def enter_step2(self):
        u"""
        进入 Step 02。

        Guide 不存在时使用正式 Guide Template Import Workflow 自动加载；
        已存在时直接复用。
        """
        face_guide = self.get_face_guide(
            refresh=True
        )

        try:
            guide_exists = face_guide.guide_exists()

            if not guide_exists:
                result = guide_template.build_guide(
                    face_guide
                )

                imported = False

                if isinstance(
                        result,
                        dict
                ):
                    imported = bool(
                        result.get(
                            "imported",
                            False
                        )
                    )

                if imported:
                    self.status_label.setText(
                        u"Face Guide 已自动导入"
                    )
                else:
                    self.status_label.setText(
                        u"Face Guide 已自动恢复"
                    )

            self.load_step2_controller_settings()
            self.refresh_step2_summary()
        except Exception as error:
            self.guide_summary_label.setText(
                u"Face Guide 加载失败"
            )
            self.status_label.setText(
                u"Face Guide 自动加载失败"
            )

            QMessageBox.critical(
                self,
                u"Face Guide 自动加载失败",
                u"{}".format(
                    error
                )
            )
            return False

        return True

    def refresh_step2_summary(self):
        u"""刷新 Step 02 简洁 Guide 状态。"""
        face_guide = self.get_face_guide()

        try:
            guide_exists = face_guide.guide_exists()
        except Exception:
            guide_exists = False

        if not guide_exists:
            self.guide_summary_label.setText(
                u"Guide 未加载"
            )
            return False

        guide_count = len(
            face_guide.get_guide_locators()
        )

        self.guide_summary_label.setText(
            u"Guide 已加载 · Locator {} · Version {}".format(
                guide_count,
                face_guide.guide_version
            )
        )

        return True

    # =========================================================================
    # Step 02 - Mirror
    # =========================================================================

    def mirror_lf_to_rt(self):
        u"""把当前 lf Guide 状态镜像复制到 rt。"""
        return self.mirror_step2_guides(
            source_side="lf",
            target_side="rt"
        )

    def mirror_rt_to_lf(self):
        u"""把当前 rt Guide 状态镜像复制到 lf。"""
        return self.mirror_step2_guides(
            source_side="rt",
            target_side="lf"
        )

    def mirror_step2_guides(
            self,
            source_side,
            target_side
    ):
        u"""执行一次 Guide Mirror，并让 Step 02 / 后续旧结果失效。"""
        face_guide = self.get_face_guide()

        try:
            result = guide_mirror.mirror_guides(
                face_guide,
                source_side=source_side,
                target_side=target_side
            )
        except Exception as error:
            self.status_label.setText(
                u"Guide Mirror 失败"
            )

            QMessageBox.critical(
                self,
                u"Guide Mirror 失败",
                u"{}".format(
                    error
                )
            )
            return False

        self.completed_step_indexes.discard(
            1
        )
        self.invalidate_ui_steps_after(
            1
        )

        self.status_label.setText(
            u"Guide Mirror 完成：{} → {} · {} 组".format(
                source_side,
                target_side,
                result.get(
                    "count",
                    0
                )
            )
        )

        self.refresh_step2_summary()

        return True

    # =========================================================================
    # Step 02 - Controller Settings
    # =========================================================================

    def get_step2_controller_settings(self):
        u"""从 Step 02 UI 收集完整 Controller Settings。"""
        settings = {
            "face_ctrl_global_scale": self.face_ctrl_global_scale_spin.value(),
            "face_ctrl_color_lf": self.controller_color_widgets["lf"].get_value(),
            "face_ctrl_color_rt": self.controller_color_widgets["rt"].get_value(),
            "face_ctrl_color_md": self.controller_color_widgets["md"].get_value(),
            "brow_ctrl_size": self.controller_size_widgets["brow"].value(),
            "eye_ctrl_size": self.controller_size_widgets["eye"].value(),
            "eyelid_ctrl_size": self.controller_size_widgets["eyelid"].value(),
            "nose_ctrl_size": self.controller_size_widgets["nose"].value(),
            "cheek_ctrl_size": self.controller_size_widgets["cheek"].value(),
            "lip_ctrl_size": self.controller_size_widgets["lip"].value(),
            "jaw_ctrl_size": self.controller_size_widgets["jaw"].value(),
        }

        return settings

    def load_step2_controller_settings(self):
        u"""从 Face Config 读取 Controller Settings 并回填 Step 02 UI。"""
        face_guide = self.get_face_guide()

        settings = guide_settings.load_controller_settings(
            face_guide
        )

        self.loading_controller_settings = True

        try:
            global_scale = settings.get(
                "face_ctrl_global_scale",
                1
            )
            self.face_ctrl_global_scale_spin.setValue(
                max(
                    1,
                    int(
                        round(
                            float(global_scale)
                        )
                    )
                )
            )

            side_attr_names = {
                "lf": "face_ctrl_color_lf",
                "rt": "face_ctrl_color_rt",
                "md": "face_ctrl_color_md",
            }

            for side in side_attr_names:
                attr_name = side_attr_names.get(
                    side
                )
                color_value = settings.get(
                    attr_name
                )

                self.controller_color_widgets[
                    side
                ].set_value(
                    int(
                        color_value
                    )
                )

            module_attr_names = {
                "brow": "brow_ctrl_size",
                "eye": "eye_ctrl_size",
                "eyelid": "eyelid_ctrl_size",
                "nose": "nose_ctrl_size",
                "cheek": "cheek_ctrl_size",
                "lip": "lip_ctrl_size",
                "jaw": "jaw_ctrl_size",
            }

            for module_name in module_attr_names:
                attr_name = module_attr_names.get(
                    module_name
                )
                size_value = settings.get(
                    attr_name,
                    1
                )

                size_value = max(
                    1,
                    int(
                        round(
                            float(size_value)
                        )
                    )
                )

                self.controller_size_widgets[
                    module_name
                ].setValue(
                    size_value
                )
        finally:
            self.loading_controller_settings = False

        return True

    def controller_settings_changed(
            self,
            value=None
    ):
        u"""标记 Step 02 Controller Settings 已修改。"""
        if self.loading_controller_settings:
            return

        face_guide = self.get_face_guide()

        if face_guide.config_node_exists():
            try:
                face_guide.set_step_completed(
                    completed=False
                )
                face_guide.invalidate_later_steps()
            except Exception:
                pass

        self.completed_step_indexes.discard(
            1
        )
        self.invalidate_ui_steps_after(
            1
        )

        self.status_label.setText(
            u"Controller Settings 已修改，点击下一步保存"
        )

    # =========================================================================
    # Step 02 - Finalize
    # =========================================================================

    def finalize_step2(self):
        u"""保存 Controller Settings，并正式提交 Face Guide Step。"""
        face_guide = self.get_face_guide()
        settings = self.get_step2_controller_settings()

        try:
            guide_settings.save_controller_settings(
                face_guide,
                settings
            )

            # 当前 Mirror 工作流允许左右独立编辑，不要求永久 LF -> RT 连接。
            face_guide.check_symmetry = False
            face_guide.run_step()

            validation = face_guide.validation_result
        except Exception as error:
            self.status_label.setText(
                u"Face Guide Finalize 失败"
            )

            QMessageBox.critical(
                self,
                u"Face Guide Finalize 失败",
                u"{}".format(
                    error
                )
            )
            self.refresh_step2_summary()
            return False

        self.completed_step_indexes.add(
            1
        )
        self.invalidate_ui_steps_after(
            1
        )

        guide_count = 0

        if isinstance(
                validation,
                dict
        ):
            guide_count = validation.get(
                "guide_count",
                0
            )

        self.status_label.setText(
            u"Face Guide 完成：{} 个 Locator · Controller Settings 已保存".format(
                guide_count
            )
        )

        self.refresh_step2_summary()

        return True


def main():
    u"""创建 Face Rig UI 并返回 QWidget。"""
    window = FaceRigWizard()
    return window


if __name__ == "__main__":
    window = main()
    window.show()
