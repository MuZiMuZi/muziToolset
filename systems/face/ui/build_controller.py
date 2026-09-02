# coding=utf-8
u"""
Face Rig Step 03 Build UI Controller
====================================

在现有 Workflow Controller 之上补充 Step 03 Module Build 页面，
同时修正 UI 与当前 Face Controller Config Schema 的映射。

设计边界：
    1. Step 01 / Step 02 的稳定基础 UI 和 Workflow 逻辑保持不变；
    2. 本层补充 Teeth / Tongue Controller Size，并使用正式 Config Attribute；
    3. 本层负责 Step 03 的 Module 触发和状态反馈；
    4. Teeth Rig 业务逻辑统一位于 systems.face.modules；
    5. Step 03 暂时不自动标记完成，因为其它 Module 尚未全部接入；
    6. 后续 Module 继续按照相同 Card + Public Build API 的模式加入。
"""

from __future__ import print_function

try:
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ....ui import theme
from .. import config
from ..modules import build_teeth
from . import workflow_controller


class FaceRigWizard(workflow_controller.FaceRigWizard):
    u"""增加正式 Controller Schema 和 Step 03 Module Build 页面的 Face Rig Wizard。"""

    def __init__(self, parent=None):
        u"""
        初始化 Step 03 Build UI。

        Args:
            parent (str):
                父级 Maya 节点名称。
        """
        self.teeth_build_result = None

        super(FaceRigWizard, self).__init__(
            parent
        )

    # =========================================================================
    # Step 02 Controller Settings Extension
    # =========================================================================

    def create_step2_page(self):
        u"""
        创建原有 Step 02 页面，并补充 Teeth / Tongue Controller Size。

        Returns:
            object:
                方法执行后的结果数据。
        """
        # -------------------------------------------------------------------------
        # Step 01：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        page = super(FaceRigWizard, self).create_step2_page()
        main_layout = page.layout()

        extra_card, extra_layout = theme.make_card(
            page
        )
        extra_layout.addWidget(
            theme.make_section_title(
                u"Oral Controller Size"
            )
        )

        description = QLabel(
            u"Teeth 和 Tongue 使用独立尺寸参数；最终尺寸仍会乘以 Face Global Scale。"
        )
        description.setWordWrap(
            True
        )
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        theme.set_role(
            description,
            "muted"
        )
        extra_layout.addWidget(
            description
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

        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self.controller_size_widgets["teeth"] = self.create_size_spin_box(
            value=1.0
        )
        self.controller_size_widgets["tongue"] = self.create_size_spin_box(
            value=1.0
        )

        settings_grid.addWidget(
            QLabel(u"Teeth"),
            0,
            0
        )
        settings_grid.addWidget(
            self.controller_size_widgets["teeth"],
            0,
            1
        )
        settings_grid.addWidget(
            QLabel(u"Tongue"),
            1,
            0
        )
        settings_grid.addWidget(
            self.controller_size_widgets["tongue"],
            1,
            1
        )
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        settings_grid.setColumnStretch(
            1,
            1
        )

        extra_layout.addLayout(
            settings_grid
        )

        insert_index = main_layout.count() - 1

        if insert_index < 0:
            insert_index = 0

        main_layout.insertWidget(
            insert_index,
            extra_card
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return page

    def get_step2_controller_settings(self):
        u"""
        使用当前 config.py 正式 Attribute 名称收集完整 Controller Settings。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        settings = {}

        settings[config.face_controller_global_scale_attr] = (
            self.face_ctrl_global_scale_spin.value()
        )

        for side in config.face_controller_color_attr_names:
            attr_name = config.face_controller_color_attr_names.get(
                side
            )
            settings[attr_name] = self.controller_color_widgets[side].get_value()

        for module_name in config.face_controller_size_attr_names:
            attr_name = config.face_controller_size_attr_names.get(
                module_name
            )
            size_widget = self.controller_size_widgets.get(
                module_name
            )

            if size_widget is None:
                raise RuntimeError(
                    u"Controller Size UI 缺少 Module：{}".format(
                        module_name
                    )
                )

            settings[attr_name] = size_widget.value()

        return settings

    def load_step2_controller_settings(self):
        u"""
        使用当前正式 Config Schema 回填全部 Controller Settings。

        Returns:
            bool:
                方法执行后的结果数据。
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
                float(
                    settings.get(
                        config.face_controller_global_scale_attr,
                        1.0
                    )
                )
            )

            for side in config.face_controller_color_attr_names:
                attr_name = config.face_controller_color_attr_names.get(
                    side
                )
                default_value = config.face_controller_default_settings.get(
                    attr_name,
                    17
                )
                self.controller_color_widgets[side].set_value(
                    int(
                        settings.get(
                            attr_name,
                            default_value
                        )
                    )
                )

            for module_name in config.face_controller_size_attr_names:
                attr_name = config.face_controller_size_attr_names.get(
                    module_name
                )
                default_value = config.face_controller_default_settings.get(
                    attr_name,
                    1.0
                )
                size_widget = self.controller_size_widgets.get(
                    module_name
                )

                if size_widget is None:
                    continue

                size_widget.setValue(
                    float(
                        settings.get(
                            attr_name,
                            default_value
                        )
                    )
                )
        finally:
            self.loading_controller_settings = False

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    # =========================================================================
    # Step 03 Page
    # =========================================================================

    def create_pages(self):
        u"""
        创建原有页面，并把 Step 03 占位页替换成正式 Module Build 页面。
        """
        super(FaceRigWizard, self).create_pages()

        old_step3_page = self.step3_page
        self.step3_page = self.create_step3_page()

        self.page_stack.removeWidget(
            old_step3_page
        )
        old_step3_page.deleteLater()

        self.page_stack.insertWidget(
            2,
            self.step3_page
        )

    def create_step3_page(self):
        u"""
        创建 Step 03 Module Build 页面。

        Returns:
            object:
                方法执行后的结果数据。
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

        intro_card, intro_layout = theme.make_card(
            page
        )
        intro_layout.addWidget(
            theme.make_section_title(
                u"Step 03 · Build"
            )
        )

        intro_description = QLabel(
            u"Face Module 按模块独立构建。当前先接入 Teeth；后续 Jaw、Lip、Eye、Eyelid、Brow、Nose、Cheek、Tongue 会继续加入同一页面。"
        )
        intro_description.setWordWrap(
            True
        )
        theme.set_role(
            intro_description,
            "muted"
        )
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        intro_layout.addWidget(
            intro_description
        )

        teeth_card, teeth_layout = theme.make_card(
            page
        )
        teeth_layout.addWidget(
            theme.make_section_title(
                u"Teeth"
            )
        )

        teeth_description = QLabel(
            u"Upper / Lower Teeth 使用 Guide → Controller → Bind Joint → Rigid Skin。Gum 不在 Teeth Module 中绑定，后续由 Mouth / Jaw Deformation 处理。"
        )
        teeth_description.setWordWrap(
            True
        )
        theme.set_role(
            teeth_description,
            "muted"
        )
        teeth_layout.addWidget(
            teeth_description
        )

        teeth_action_layout = QHBoxLayout()
        teeth_action_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        teeth_action_layout.setSpacing(
            10
        )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.teeth_build_status_label = QLabel(
            u"未构建"
        )
        theme.set_role(
            self.teeth_build_status_label,
            "pill"
        )

        self.build_teeth_button = QPushButton(
            u"构建 Teeth"
        )
        theme.style_primary(
            self.build_teeth_button
        )

        teeth_action_layout.addWidget(
            self.teeth_build_status_label
        )
        teeth_action_layout.addStretch(
            1
        )
        teeth_action_layout.addWidget(
            self.build_teeth_button
        )

        teeth_layout.addLayout(
            teeth_action_layout
        )

        future_card, future_layout = theme.make_card(
            page
        )
        # -------------------------------------------------------------------------
        # Step 04：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        future_layout.addWidget(
            theme.make_section_title(
                u"Next Modules"
            )
        )

        future_label = QLabel(
            u"Jaw → Tongue → Lip → Eye / Eyelid → Brow → Nose / Cheek"
        )
        future_label.setWordWrap(
            True
        )
        theme.set_role(
            future_label,
            "muted"
        )
        future_layout.addWidget(
            future_label
        )

        main_layout.addWidget(
            intro_card
        )
        main_layout.addWidget(
            teeth_card
        )
        main_layout.addWidget(
            future_card
        )
        main_layout.addStretch(
            1
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return page

    # =========================================================================
    # Connections
    # =========================================================================

    def create_connections(self):
        u"""
        连接原有信号和 Step 03 Teeth Build 信号。
        """
        super(FaceRigWizard, self).create_connections()

        self.build_teeth_button.clicked.connect(
            self.clicked_build_teeth
        )

    # =========================================================================
    # Teeth Build
    # =========================================================================

    def clicked_build_teeth(self):
        u"""
        通过 Face System 公共 API 构建 Teeth Module。

        Returns:
            bool:
                方法执行后的结果数据。
        """
        # -------------------------------------------------------------------------
        # Step 01：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.build_teeth_button.setEnabled(
            False
        )
        self.teeth_build_status_label.setText(
            u"构建中"
        )
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"正在构建 Teeth Module"
        )

        try:
            result = build_teeth()
        except Exception as error:
            self.teeth_build_result = None
            self.teeth_build_status_label.setText(
                u"构建失败"
            )
            theme.set_role(
                self.teeth_build_status_label,
                "danger_text"
            )
            self.status_label.setText(
                u"Teeth Module 构建失败"
            )
            self.build_teeth_button.setEnabled(
                True
            )

            QMessageBox.critical(
                self,
                u"Teeth Module 构建失败",
                u"{}".format(error)
            )
            return False

        self.teeth_build_result = result
        # -------------------------------------------------------------------------
        # Step 03：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.teeth_build_status_label.setText(
            u"构建完成"
        )
        theme.set_role(
            self.teeth_build_status_label,
            "pill"
        )
        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.status_label.setText(
            u"Teeth Module 构建完成"
        )

        self.build_teeth_button.setEnabled(
            False
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True


def main():
    u"""
    创建带 Step 03 Module Build 页面的正式 Face Rig UI。

    Returns:
        object:
            方法执行后的结果数据。
    """
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
