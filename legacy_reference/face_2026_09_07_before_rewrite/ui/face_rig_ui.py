# coding=utf-8
u"""
Face Rig UI
===========

Face Rig 的四步构建界面。

设计原则：
    - UI 只负责参数收集、状态反馈和当前 Step 的必要辅助操作；
    - Step 逻辑由 systems.face.setup / guide / build / finalize 负责；
    - 进入 Step 02 自动导入或复用 face_guide.ma；
    - Step 02 只保留 Guide Repair、Mirror、Mirror Undo 和 Controller Settings；
    - 点击“下一步”时必须检查模板中的全部 Locator 都仍然存在；
    - Controller Size 使用 QDoubleSpinBox，保留 1 位小数；
    - Controller Color 使用 Maya Index Color Slider + Index + Preview；
    - 每次打开工具优先读取 Face Config 保存的 Current Face Step 自动恢复 Workflow；
    - UI 统一使用 MuziTools Arc-inspired Theme，不在本文件复制整套 QSS。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QDoubleSpinBox
    from PySide2.QtWidgets import QFrame
    from PySide2.QtWidgets import QGridLayout
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
    from PySide6.QtWidgets import QDoubleSpinBox
    from PySide6.QtWidgets import QFrame
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QSlider
    from PySide6.QtWidgets import QStackedWidget
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ....ui import theme
from ....ui.widgets import MayaIndexColorSlider
from ....ui.widgets import MayaObjectPicker
from ..guide import guide_mirror
from ..guide.face_guide import FaceGuide
from ..setup.face_setup import FaceSetup


class FaceRigWizard(QWidget):
    u"""Face Rig 四步构建窗口。"""

    def __init__(self, parent=None):
        u"""
        初始化 Face Rig UI。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """
        # -------------------------------------------------------------------------
        # Step 01：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        super(FaceRigWizard, self).__init__(parent)

        self.current_step_index = 0
        self.completed_step_indexes = set()
        self.step_buttons = []

        self.face_setup = None
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.face_guide = None
        self.last_mirror_snapshot = None

        self.loading_controller_settings = False

        self.mouth_jnt_step = 4
        self.mouth_jnt_minimum = 4
        self.mouth_jnt_maximum = 128
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.mouth_jnt_default = 40

        self.controller_size_widgets = {}
        self.controller_color_widgets = {}

        self.setWindowTitle(
            u"Face Rig"
        )
        self.setMinimumWidth(
            720
        )
        self.resize(
            820,
            760
        )

        # -------------------------------------------------------------------------
        # Step 04：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.create_widgets()
        self.create_pages()
        self.create_layouts()
        self.create_connections()

        theme.style_window(
            self
        )

        # -------------------------------------------------------------------------
        # Step 05：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        self.restore_step_state()

    # =========================================================================
    # Common UI
    # =========================================================================

    def create_widgets(self):
        u"""
        创建公共控件。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.title_label = theme.make_title(
            u"Face Rig"
        )
        self.subtitle_label = theme.make_subtitle(
            u"Setup → Guide → Build → Finalize。每一步只展示当前真正需要处理的内容。"
        )

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        step_names = [
            u"01  Setup",
            u"02  Guide",
            u"03  Build",
            u"04  Finalize",
        ]

        for step_index in range(len(step_names)):
            step_button = QPushButton(
                step_names[step_index]
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

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.status_label = QLabel(
            u"准备就绪"
        )
        theme.set_role(
            self.status_label,
            "muted"
        )

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.next_button = QPushButton(
            u"下一步"
        )
        self.next_button.setMinimumWidth(
            88
        )
        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.style_primary(
            self.next_button
        )

    def create_pages(self):
        u"""
        创建四个 Step 页面。
        """
        self.step1_page = self.create_step1_page()
        self.step2_page = self.create_step2_page()
        self.step3_page = self.create_placeholder_page(
            u"Step 03 · Build",
            u"后续 Jaw、Lip、Eye、Eyelid、Brow、Nose、Cheek Component 将统一在 Build Package 中构建。"
        )
        self.step4_page = self.create_placeholder_page(
            u"Step 04 · Finalize",
            u"最终检查、显示管理、Controller Set、清理和发布会统一放在 Finalize Package。"
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

    def create_layouts(self):
        u"""
        创建主布局。
        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        main_layout = QVBoxLayout(
            self
        )
        main_layout.setContentsMargins(
            20,
            18,
            20,
            16
        )
        main_layout.setSpacing(
            14
        )

        main_layout.addWidget(
            self.title_label
        )
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
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
            7,
            7,
            7,
            7
        )
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
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
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 05：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        main_layout.addLayout(
            bottom_layout
        )

    def create_connections(self):
        u"""
        连接 UI Signal。
        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for step_button in self.step_buttons:
            step_button.clicked.connect(
                self.clicked_step_button
            )

        self.next_button.clicked.connect(
            self.clicked_next_button
        )
        # -------------------------------------------------------------------------
        # Step 02：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        self.mouth_jnt_slider.valueChanged.connect(
            self.update_mouth_jnt_value
        )

        self.reimport_guide_button.clicked.connect(
            self.reimport_step2_guide
        )
        self.mirror_lf_to_rt_button.clicked.connect(
            self.mirror_lf_to_rt
        )
        # -------------------------------------------------------------------------
        # Step 03：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
        self.mirror_rt_to_lf_button.clicked.connect(
            self.mirror_rt_to_lf
        )
        self.undo_mirror_button.clicked.connect(
            self.undo_last_mirror
        )

        # -------------------------------------------------------------------------
        # Step 04：建立当前阶段需要的层级、连接或驱动关系
        # -------------------------------------------------------------------------
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

        # -------------------------------------------------------------------------
        # Step 05：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for module_name in self.controller_size_widgets:
            size_spin = self.controller_size_widgets.get(
                module_name
            )
            size_spin.valueChanged.connect(
                self.controller_settings_changed
            )

    # =========================================================================
    # Step 01 UI
    # =========================================================================

    def create_step1_page(self):
        u"""
        创建 Face Setup 页面。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
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

        model_card, model_layout = theme.make_card(
            page
        )
        model_layout.addWidget(
            theme.make_section_title(
                u"模型输入"
            )
        )

        model_description = QLabel(
            u"Head 为必填项，其它模型可以留空。拾取按钮使用 Maya 当前最后选择对象。"
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

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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

        pickers = [
            self.face_head_picker,
            self.face_lf_eye_picker,
            self.face_rt_eye_picker,
            self.upper_teech_picker,
            self.lower_teech_picker,
            self.face_tongue_picker,
            self.face_gum_picker,
        ]

        for picker in pickers:
            model_layout.addWidget(
                picker
            )

        parameter_card, parameter_layout = theme.make_card(
            page
        )
        parameter_layout.addWidget(
            theme.make_section_title(
                u"构建参数"
            )
        )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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
            u"嘴唇 Jnt 数量"
        )
        mouth_label.setMinimumWidth(
            120
        )

        self.mouth_jnt_slider = QSlider(
            Qt.Horizontal
        )
        self.mouth_jnt_slider.setMinimum(
            int(self.mouth_jnt_minimum / self.mouth_jnt_step)
        )
        self.mouth_jnt_slider.setMaximum(
            int(self.mouth_jnt_maximum / self.mouth_jnt_step)
        )
        self.mouth_jnt_slider.setSingleStep(
            1
        )
        self.mouth_jnt_slider.setPageStep(
            2
        )
        self.mouth_jnt_slider.setValue(
            int(self.mouth_jnt_default / self.mouth_jnt_step)
        )
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.mouth_jnt_slider.setMinimumWidth(
            300
        )

        self.mouth_jnt_value_label = QLabel(
            u"{}".format(self.mouth_jnt_default)
        )
        theme.set_role(
            self.mouth_jnt_value_label,
            "pill"
        )

        mouth_layout.addWidget(
            mouth_label
        )
        mouth_layout.addWidget(
            self.mouth_jnt_slider,
            1
        )
        mouth_layout.addWidget(
            self.mouth_jnt_value_label
        )

        parameter_layout.addLayout(
            mouth_layout
        )

        main_layout.addWidget(
            model_card
        )
        main_layout.addWidget(
            parameter_card
        )
        main_layout.addStretch(
            1
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return page

    # =========================================================================
    # Step 02 UI
    # =========================================================================

    def create_step2_page(self):
        u"""
        创建 Face Guide 编辑页面。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
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

        guide_card, guide_layout = theme.make_card(
            page
        )
        guide_layout.addWidget(
            theme.make_section_title(
                u"Face Guide"
            )
        )

        guide_description = QLabel(
            u"进入 Step 02 会自动加载 face_guide.ma。若绑定过程中误删定位器，可重新导入完整模板；现有定位器位置会被保留。"
        )
        guide_description.setWordWrap(
            True
        )
        theme.set_role(
            guide_description,
            "muted"
        )

        guide_status_layout = QHBoxLayout()
        guide_status_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        guide_status_layout.setSpacing(
            8
        )

        self.guide_summary_label = QLabel(
            u"等待加载 Face Guide"
        )
        theme.set_role(
            self.guide_summary_label,
            "pill"
        )

        self.reimport_guide_button = QPushButton(
            u"重新导入模板"
        )
        theme.style_secondary(
            self.reimport_guide_button
        )

        guide_status_layout.addWidget(
            self.guide_summary_label
        )
        guide_status_layout.addStretch(
            1
        )
        guide_status_layout.addWidget(
            self.reimport_guide_button
        )

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        guide_layout.addWidget(
            guide_description
        )
        guide_layout.addLayout(
            guide_status_layout
        )

        mirror_card, mirror_layout = theme.make_card(
            page
        )
        mirror_layout.addWidget(
            theme.make_section_title(
                u"Guide Mirror"
            )
        )

        mirror_description = QLabel(
            u"镜像只复制当前状态，不建立永久左右连接。镜像成功后可用“撤销上次镜像”快速回退，也可以直接使用 Maya Ctrl + Z。"
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
        self.undo_mirror_button = QPushButton(
            u"撤销上次镜像"
        )

        theme.style_secondary(
            self.mirror_lf_to_rt_button
        )
        theme.style_secondary(
            self.mirror_rt_to_lf_button
        )
        theme.style_ghost(
            self.undo_mirror_button
        )
        self.undo_mirror_button.setEnabled(
            False
        )

        mirror_button_layout.addWidget(
            self.mirror_lf_to_rt_button
        )
        mirror_button_layout.addWidget(
            self.mirror_rt_to_lf_button
        )
        mirror_button_layout.addWidget(
            self.undo_mirror_button
        )
        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        mirror_button_layout.addStretch(
            1
        )

        mirror_layout.addWidget(
            mirror_description
        )
        mirror_layout.addLayout(
            mirror_button_layout
        )

        controller_card, controller_layout = theme.make_card(
            page
        )
        controller_layout.addWidget(
            theme.make_section_title(
                u"Controller Settings"
            )
        )

        controller_description = QLabel(
            u"Size 默认 1.0，可按 0.1 调整；颜色默认 LF 蓝 6、RT 红 13、MD 黄 17。模块按面部从上到下排列。"
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
            16
        )
        settings_grid.setVerticalSpacing(
            10
        )

        settings_grid.addWidget(
            QLabel(u"Global Scale"),
            0,
            0
        )
        self.face_ctrl_global_scale_spin = self.create_size_spin_box(
            value=1.0
        )
        settings_grid.addWidget(
            self.face_ctrl_global_scale_spin,
            0,
            1
        )

        side_title = QLabel(
            u"Side Color"
        )
        theme.set_role(
            side_title,
            "muted"
        )
        settings_grid.addWidget(
            side_title,
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

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        row = 2

        for side_item in side_items:
            side = side_item[0]
            label_text = side_item[1]
            default_color = side_item[2]

            color_widget = MayaIndexColorSlider(
                value=default_color
            )
            self.controller_color_widgets[side] = color_widget

            settings_grid.addWidget(
                QLabel(label_text),
                row,
                0
            )
            settings_grid.addWidget(
                color_widget,
                row,
                1
            )
            row += 1

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

        module_items = [
            ("brow", u"Brow"),
            ("eye", u"Eye"),
            ("eyelid", u"Eyelid"),
            ("nose", u"Nose"),
            ("cheek", u"Cheek"),
            ("lip", u"Lip"),
            ("jaw", u"Jaw"),
        ]

        row = 2

        for module_item in module_items:
            module_name = module_item[0]
            label_text = module_item[1]
            size_spin = self.create_size_spin_box(
                value=1.0
            )

            self.controller_size_widgets[module_name] = size_spin

            settings_grid.addWidget(
                QLabel(label_text),
                row,
                2
            )
            settings_grid.addWidget(
                size_spin,
                row,
                3
            )
            row += 1

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

        step_hint = QLabel(
            u"点击下一步会先检查模板中的全部 Locator。任何一个定位器缺失都会阻止进入 Step 03。"
        )
        step_hint.setWordWrap(
            True
        )
        theme.set_role(
            step_hint,
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
            step_hint
        )
        main_layout.addStretch(
            1
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return page

    def create_size_spin_box(
            self,
            value=1.0
    ):
        u"""
        创建只保留 1 位小数的 Controller Size QDoubleSpinBox。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
        """
        spin_box = QDoubleSpinBox()
        spin_box.setDecimals(
            1
        )
        spin_box.setRange(
            0.1,
            100.0
        )
        spin_box.setSingleStep(
            0.1
        )
        spin_box.setValue(
            float(value)
        )
        spin_box.setMinimumWidth(
            100
        )
        return spin_box

    def create_placeholder_page(
            self,
            title,
            description
    ):
        u"""
        创建尚未完成的步骤页面。

        Args:
            title (str):
                窗口、Section、Dialog 或报告使用的标题文本。
            description (str):
                UI Step / Section 中展示的功能说明文本。

        Returns:
            object:
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        page = QWidget()
        layout = QVBoxLayout(
            page
        )
        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
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
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(
            description_label,
            "muted"
        )
        card_layout.addWidget(
            description_label
        )

        state_label = QLabel(
            u"开发中"
        )
        theme.set_role(
            state_label,
            "pill"
        )
        # -------------------------------------------------------------------------
        # Step 04：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        card_layout.addWidget(
            state_label,
            0,
            Qt.AlignLeft
        )

        layout.addWidget(
            card
        )
        layout.addStretch(
            1
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return page

    # =========================================================================
    # Step State
    # =========================================================================

    def get_face_guide(
            self,
            refresh=False
    ):
        u"""
        返回当前 UI 使用的 FaceGuide 实例。

        Args:
            refresh (bool):
                读取数据前是否先从 Maya Scene / Config 重新刷新缓存。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        if refresh:
            self.face_guide = None

        if self.face_guide is None:
            self.face_guide = FaceGuide()

        return self.face_guide

    def restore_step_state(self):
        u"""
        从 Face Config 恢复完成状态，并跳转到正式保存的 Current Face Step。

        旧场景没有 face_current_step 时，FaceBase 会根据 Step Completed 状态自动推导并迁移。
        """
        # -------------------------------------------------------------------------
        # Step 01：清理当前阶段不再需要的数据或场景状态
        # -------------------------------------------------------------------------
        self.completed_step_indexes.clear()
        face_guide = self.get_face_guide(
            refresh=True
        )

        # -------------------------------------------------------------------------
        # Step 02：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not face_guide.config_node_exists():
            self.set_current_step(
                0
            )
            return

        try:
            step_status = face_guide.get_step_status(
                last_step=4
            )
            current_step_value = face_guide.get_current_step_value()
        except Exception:
            self.set_current_step(
                0
            )
            return

        step_value = 1

        # -------------------------------------------------------------------------
        # Step 03：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
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

        current_step_index = current_step_value - 1

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if current_step_index < 0 or current_step_index >= self.page_stack.count():
            current_step_index = 0

        self.set_current_step(
            current_step_index
        )

        # -------------------------------------------------------------------------
        # Step 05：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"已恢复到 Step {:02d}".format(
                current_step_value
            )
        )

    def invalidate_ui_steps_after(
            self,
            step_index
    ):
        u"""
        清除指定 Step 后面的 UI 完成状态。

        Args:
            step_index (int):
                对应 Maya Array Attribute、Target、Guide 或构建元素的逻辑索引。
        """
        next_step_index = step_index + 1

        while next_step_index < len(self.step_buttons):
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
        u"""
        切换当前 UI 页面。

        这里只改变当前查看页面，不直接修改 Config 的 Workflow Progress。
        正式进度只在 Step 完成或旧 Step 被修改变脏时更新。

        Args:
            step_index (int):
                对应 Maya Array Attribute、Target、Guide 或构建元素的逻辑索引。
        """
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
        u"""
        刷新顶部 Step Navigation。
        """
        for step_index in range(len(self.step_buttons)):
            step_button = self.step_buttons[step_index]
            current = step_index == self.current_step_index
            completed = step_index in self.completed_step_indexes

            step_button.setChecked(
                current
            )
            theme.style_navigation(
                step_button,
                active=current
            )

            if current or completed:
                step_button.setEnabled(
                    True
                )
            else:
                step_button.setEnabled(
                    False
                )

    def update_navigation_buttons(self):
        u"""
        刷新底部“下一步”状态。
        """
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
                bool(guide_exists)
            )
            return

        self.next_button.setEnabled(
            False
        )

    def clicked_step_button(self):
        u"""
        通过顶部导航返回已经完成的 Step。
        """
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
        u"""
        提交当前 Step，并在成功后进入下一步。
        """
        if self.current_step_index == 0:
            if not self.build_step1():
                return

            self.set_current_step(
                1
            )
            return

        if self.current_step_index == 1:
            if not self.finalize_step2():
                return

            self.set_current_step(
                2
            )

    # =========================================================================
    # Step 01
    # =========================================================================

    def update_mouth_jnt_value(
            self,
            slider_value
    ):
        u"""
        更新嘴唇 Jnt 数量显示。

        Args:
            slider_value (int | float):
                UI Slider 当前值；回调用于同步对应 Rig / Setup 参数。
        """
        mouth_jnt_number = slider_value * self.mouth_jnt_step
        self.mouth_jnt_value_label.setText(
            u"{}".format(
                mouth_jnt_number
            )
        )

    def get_mouth_jnt_number(self):
        u"""
        返回当前嘴唇 Jnt 数量。

        Returns:
            object:
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。
        """
        return self.mouth_jnt_slider.value() * self.mouth_jnt_step

    def build_step1(self):
        u"""
        执行 FaceSetup Step。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        face_setup = FaceSetup(
            face_head_model=self.face_head_picker.get_value(),
            face_lf_eye_model=self.face_lf_eye_picker.get_value(),
            face_rt_eye_model=self.face_rt_eye_picker.get_value(),
            upper_teech_model=self.upper_teech_picker.get_value(),
            lower_teech_model=self.lower_teech_picker.get_value(),
            face_tongue_model=self.face_tongue_picker.get_value(),
            face_gum_model=self.face_gum_picker.get_value(),
            mouth_jnt_number=self.get_mouth_jnt_number()
        )

        try:
            face_setup.run_step()
        except Exception as error:
            self.status_label.setText(
                u"Face Setup 失败"
            )
            QMessageBox.critical(
                self,
                u"Face Setup 失败",
                u"{}".format(error)
            )
            return False

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.face_setup = face_setup
        self.completed_step_indexes.add(
            0
        )
        # -------------------------------------------------------------------------
        # Step 03：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.invalidate_ui_steps_after(
            0
        )
        self.get_face_guide(
            refresh=True
        )
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"Face Setup 完成"
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    # =========================================================================
    # Step 02 Enter / Status
    # =========================================================================

    def enter_step2(self):
        u"""
        进入 Step 02，自动导入或复用 Guide。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        face_guide = self.get_face_guide(
            refresh=True
        )

        # -------------------------------------------------------------------------
        # Step 02：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            if not face_guide.guide_exists():
                result = face_guide.build_guide()

                if result.get("imported", False):
                    self.status_label.setText(
                        u"Face Guide 已自动导入"
                    )
                else:
                    self.status_label.setText(
                        u"Face Guide 已恢复"
                    )

            self.load_step2_controller_settings()
            self.refresh_step2_summary()
        except Exception as error:
            self.guide_summary_label.setText(
                u"Face Guide 加载失败"
            )
            theme.set_role(
                self.guide_summary_label,
                "danger_text"
            )
            self.status_label.setText(
                u"Face Guide 自动加载失败"
            )
            QMessageBox.critical(
                self,
                u"Face Guide 自动加载失败",
                u"{}".format(error)
            )
            return False

        # -------------------------------------------------------------------------
        # Step 03：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def refresh_step2_summary(self):
        u"""
        刷新 Guide 完整性摘要。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        face_guide = self.get_face_guide()

        # -------------------------------------------------------------------------
        # Step 02：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            validation = face_guide.validate_guides()
        except Exception:
            validation = None

        if not isinstance(validation, dict):
            self.guide_summary_label.setText(
                u"Guide 状态未知"
            )
            return False

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if validation.get("valid", False):
            self.guide_summary_label.setText(
                u"Guide 完整 · {}/{} Locator · Version {}".format(
                    validation.get("guide_count", 0),
                    validation.get("template_guide_count", 0),
                    face_guide.guide_version
                )
            )
            return True

        missing_count = len(
            validation.get(
                "missing_guide_names",
                []
            )
        )
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.guide_summary_label.setText(
            u"Guide 不完整 · 缺少 {} 个 Locator".format(
                missing_count
            )
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return False

    def mark_step2_dirty(self):
        u"""
        把 Step 02 和后续 Step 标记为需要重新提交，并把 Workflow 退回 Step 02。
        """
        face_guide = self.get_face_guide()

        if face_guide.config_node_exists():
            try:
                face_guide.set_step_completed(
                    completed=False
                )
                face_guide.invalidate_later_steps()
                face_guide.set_current_step_value(
                    2
                )
            except Exception:
                pass

        self.completed_step_indexes.discard(
            1
        )
        self.invalidate_ui_steps_after(
            1
        )

    # =========================================================================
    # Step 02 Repair
    # =========================================================================

    def reimport_step2_guide(self):
        u"""
        重新导入完整模板，并保留当前仍存在 Locator 的位置。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        face_guide = self.get_face_guide()

        try:
            result = face_guide.reimport_guide()
        except Exception as error:
            self.status_label.setText(
                u"Guide 模板重新导入失败"
            )
            QMessageBox.critical(
                self,
                u"重新导入模板失败",
                u"{}".format(error)
            )
            return False

        self.last_mirror_snapshot = None
        self.undo_mirror_button.setEnabled(
            False
        )
        self.mark_step2_dirty()
        self.refresh_step2_summary()
        self.status_label.setText(
            u"模板已重新导入 · 恢复 {} 个已有 Locator · 完整模板 {} 个".format(
                result.get("restored_count", 0),
                result.get("template_locator_count", 0)
            )
        )
        return True

    # =========================================================================
    # Step 02 Mirror / Undo
    # =========================================================================

    def mirror_lf_to_rt(self):
        u"""
        LF Guide 镜像到 RT。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self.mirror_step2_guides(
            source_side="lf",
            target_side="rt"
        )

    def mirror_rt_to_lf(self):
        u"""
        RT Guide 镜像到 LF。

        Returns:
            object:
            当前 API 完成处理后返回的结果。
        """
        return self.mirror_step2_guides(
            source_side="rt",
            target_side="lf"
        )

    def mirror_step2_guides(
            self,
            source_side,
            target_side
    ):
        u"""
        执行一次 Guide Mirror，并保存 UI Undo Snapshot。

        Args:
            source_side (str):
                当前 Maya / Rig 操作使用的 `source_side` 名称或标记。
            target_side (str):
                当前 Maya / Rig 操作使用的 `target_side` 名称或标记。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
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
                u"{}".format(error)
            )
            return False

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.last_mirror_snapshot = result.get(
            "snapshot"
        )
        self.undo_mirror_button.setEnabled(
            bool(self.last_mirror_snapshot)
        )

        # -------------------------------------------------------------------------
        # Step 03：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        self.mark_step2_dirty()
        self.refresh_step2_summary()
        # -------------------------------------------------------------------------
        # Step 04：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"Guide Mirror 完成：{} → {} · {} 组".format(
                source_side,
                target_side,
                result.get("count", 0)
            )
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def undo_last_mirror(self):
        u"""
        恢复最近一次 Mirror 前的 Target Guide 状态。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        if not self.last_mirror_snapshot:
            return False

        face_guide = self.get_face_guide()

        try:
            result = guide_mirror.undo_mirror(
                face_guide,
                self.last_mirror_snapshot
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                u"撤销镜像失败",
                u"{}".format(error)
            )
            return False

        self.last_mirror_snapshot = None
        self.undo_mirror_button.setEnabled(
            False
        )
        self.mark_step2_dirty()
        self.refresh_step2_summary()
        self.status_label.setText(
            u"已撤销上次 Guide Mirror · 恢复 {} 组".format(
                result.get("restored_count", 0)
            )
        )
        return True

    # =========================================================================
    # Step 02 Controller Settings
    # =========================================================================

    def get_step2_controller_settings(self):
        u"""
        从 UI 收集完整 Controller Settings。

        Returns:
            dict:
            包含本次构建、查询或处理结果的结构化字典。
        """
        return {
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

    def load_step2_controller_settings(self):
        u"""
        从 Face Config 回填 Controller Settings。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        face_guide = self.get_face_guide()
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        settings = face_guide.load_controller_settings()

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.loading_controller_settings = True

        # -------------------------------------------------------------------------
        # Step 04：执行可能失败的操作，并统一处理异常或清理状态
        # -------------------------------------------------------------------------
        try:
            self.face_ctrl_global_scale_spin.setValue(
                float(settings.get("face_ctrl_global_scale", 1.0))
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
                self.controller_color_widgets[side].set_value(
                    int(settings.get(attr_name))
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
                self.controller_size_widgets[module_name].setValue(
                    float(settings.get(attr_name, 1.0))
                )
        finally:
            self.loading_controller_settings = False

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def controller_settings_changed(
            self,
            value=None
    ):
        u"""
        Controller Settings 修改后标记 Step 02 Dirty。

        Args:
            value (float):
                需要读取、写入或参与计算的数值。
        """
        if self.loading_controller_settings:
            return

        self.mark_step2_dirty()
        self.status_label.setText(
            u"Controller Settings 已修改，点击下一步保存"
        )

    # =========================================================================
    # Step 02 Finalize
    # =========================================================================

    def get_missing_guide_message(self, validation):
        u"""
        把缺失 Locator 列表整理成用户可读错误信息。

        Args:
            validation (object):
                当前方法执行 Maya / Rig 操作时使用的 `validation` 数据。

        Returns:
            object | str:
            当前 API 查询或处理后得到的字符串结果。
        """
        missing_names = validation.get(
            "missing_guide_names",
            []
        )

        if not missing_names:
            return u"Face Guide 未通过完整性检查。"

        message = u"检测到 {} 个模板定位器缺失，不能进入 Step 03：".format(
            len(missing_names)
        )

        for guide_name in missing_names:
            message += u"\n- {}".format(
                guide_name
            )

        message += u"\n\n请点击“重新导入模板”补回缺失定位器；现有定位器位置会被保留。"
        return message

    def finalize_step2(self):
        u"""
        完整检查 Guide，保存 Settings，并提交 Step 02。

        Returns:
            bool:
            当前操作成功或目标状态满足要求时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        face_guide = self.get_face_guide()

        try:
            validation = face_guide.validate_guides()
        except Exception as error:
            QMessageBox.critical(
                self,
                u"Face Guide 检查失败",
                u"{}".format(error)
            )
            return False

        if not validation.get("valid", False):
            self.status_label.setText(
                u"Face Guide 不完整，无法进入下一步"
            )
            QMessageBox.critical(
                self,
                u"Face Guide 不完整",
                self.get_missing_guide_message(
                    validation
                )
            )
            self.refresh_step2_summary()
            return False

        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        settings = self.get_step2_controller_settings()

        try:
            face_guide.save_controller_settings(
                settings
            )
            face_guide.run_step()
        except Exception as error:
            self.status_label.setText(
                u"Face Guide Finalize 失败"
            )
            QMessageBox.critical(
                self,
                u"Face Guide Finalize 失败",
                u"{}".format(error)
            )
            self.refresh_step2_summary()
            return False

        self.completed_step_indexes.add(
            1
        )
        # -------------------------------------------------------------------------
        # Step 03：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.invalidate_ui_steps_after(
            1
        )
        self.last_mirror_snapshot = None
        self.undo_mirror_button.setEnabled(
            False
        )
        # -------------------------------------------------------------------------
        # Step 04：执行当前阶段的核心处理
        # -------------------------------------------------------------------------
        self.refresh_step2_summary()
        self.status_label.setText(
            u"Face Guide 完成 · {} 个模板 Locator · Controller Settings 已保存".format(
                validation.get("template_guide_count", 0)
            )
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True


def main():
    u"""
    创建 Face Rig UI 并返回 QWidget。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    return FaceRigWizard()


if __name__ == "__main__":
    window = main()
    window.show()
