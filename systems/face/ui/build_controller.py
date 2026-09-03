# coding=utf-8
u"""
Face Rig Step 03 Build UI Controller
====================================

在现有 Workflow Controller 之上补充 Step 03 Module Build 页面，
同时把完整 FaceRig Orchestrator 接入正式 Step 03。

设计边界：
    1. Step 01 / Step 02 的稳定基础 UI 和 Workflow 逻辑保持不变；
    2. 本层补充 Teeth / Tongue Controller Size，并使用正式 Config Attribute；
    3. 本层负责 Step 03 完整 FaceBuild 触发和状态反馈；
    4. Step 03 只调用 FaceBuild.run_step()，不直接调用具体 Face Module；
    5. 完整 Build 成功后允许进入 Step 04 Finalize；
    6. Build 失败由 FaceBuild 统一 Undo 回滚，UI 可以安全重试。
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
from ..build.face_build import FaceBuild
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
        self.face_build_result = None

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
            创建或构建完成后的 Maya / Rig 对象或 Build Result。
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
            当前查询匹配到的 Maya / Rig 数据；没有结果时按 API 约定返回空值。

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
        创建 Step 03 完整 Face Rig Build 页面。

        Returns:
            QWidget:
                完整 FaceBuild 操作页面。
        """
        # -------------------------------------------------------------------------
        # Step 01：创建 Step 03 页面和完整 Build 说明
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
            u"Step 03 现在通过 FaceBuild → FaceRig 一次构建全部正式 Face Module。UI 不再直接管理单个 Module。"
        )
        intro_description.setWordWrap(
            True
        )
        theme.set_role(
            intro_description,
            "muted"
        )
        intro_layout.addWidget(
            intro_description
        )

        # -------------------------------------------------------------------------
        # Step 02：显示正式 Module 依赖顺序，方便检查完整构建范围
        # -------------------------------------------------------------------------
        module_card, module_layout = theme.make_card(
            page
        )
        module_layout.addWidget(
            theme.make_section_title(
                u"Face Modules"
            )
        )

        module_description = QLabel(
            u"Brow → Eye → Eyelid → Nose → Cheek → Ear → Jaw → Teeth → Tongue → Lip → Mouth"
        )
        module_description.setWordWrap(
            True
        )
        theme.set_role(
            module_description,
            "muted"
        )
        module_layout.addWidget(
            module_description
        )

        dependency_description = QLabel(
            u"显式依赖：Eye → Eyelid，Jaw + Lip → Mouth。其它 Module 保持固定顺序以获得稳定场景结果。"
        )
        dependency_description.setWordWrap(
            True
        )
        theme.set_role(
            dependency_description,
            "muted"
        )
        module_layout.addWidget(
            dependency_description
        )

        # -------------------------------------------------------------------------
        # Step 03：创建完整 Build 状态和唯一正式构建按钮
        # -------------------------------------------------------------------------
        build_card, build_layout = theme.make_card(
            page
        )
        build_layout.addWidget(
            theme.make_section_title(
                u"Complete Face Rig"
            )
        )

        build_hint = QLabel(
            u"构建失败时整个 Step 03 会自动 Undo 回滚；成功后 Step 03 标记完成并进入 Finalize 流程。"
        )
        build_hint.setWordWrap(
            True
        )
        theme.set_role(
            build_hint,
            "muted"
        )
        build_layout.addWidget(
            build_hint
        )

        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        action_layout.setSpacing(
            10
        )

        self.face_build_status_label = QLabel(
            u"未构建"
        )
        theme.set_role(
            self.face_build_status_label,
            "pill"
        )

        self.build_face_button = QPushButton(
            u"构建完整 Face Rig"
        )
        theme.style_primary(
            self.build_face_button
        )

        action_layout.addWidget(
            self.face_build_status_label
        )
        action_layout.addStretch(
            1
        )
        action_layout.addWidget(
            self.build_face_button
        )
        build_layout.addLayout(
            action_layout
        )

        # -------------------------------------------------------------------------
        # Step 04：组合页面并保留底部弹性空间
        # -------------------------------------------------------------------------
        main_layout.addWidget(
            intro_card
        )
        main_layout.addWidget(
            module_card
        )
        main_layout.addWidget(
            build_card
        )
        main_layout.addStretch(
            1
        )
        return page

    # =========================================================================
    # Connections
    # =========================================================================

    def create_connections(self):
        u"""连接原有 Signal 和完整 FaceBuild 按钮信号。"""
        super(FaceRigWizard, self).create_connections()

        self.build_face_button.clicked.connect(
            self.clicked_build_face
        )

    # =========================================================================
    # Step 03 State / Navigation
    # =========================================================================

    def load_step_config_to_ui(self, step_index):
        u"""
        恢复原 Workflow Config，并在 Step 03 回填完整 FaceBuild 状态。

        Args:
            step_index (int):
                当前 UI Step 索引。

        Returns:
            bool | object:
                Config 回填结果。
        """
        result = super(FaceRigWizard, self).load_step_config_to_ui(
            step_index
        )

        if step_index == 2:
            self.load_step3_build_state()

        return result

    def load_step3_build_state(self):
        u"""
        从 Face Config 恢复 Step 03 完成状态和按钮状态。

        Returns:
            bool:
                Step 03 已完成时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        face_context = self.get_face_guide()
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        completed = False

        if face_context.config_node_exists():
            completed = face_context.is_step_completed(
                step_value=3
            )

        # -------------------------------------------------------------------------
        # Step 03：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if completed:
            self.completed_step_indexes.add(
                2
            )
            self.face_build_status_label.setText(
                u"构建完成"
            )
            theme.set_role(
                self.face_build_status_label,
                "pill"
            )
            self.build_face_button.setEnabled(
                False
            )
        else:
            self.completed_step_indexes.discard(
                2
            )
            self.face_build_status_label.setText(
                u"未构建"
            )
            theme.set_role(
                self.face_build_status_label,
                "pill"
            )
            self.build_face_button.setEnabled(
                True
            )

        # -------------------------------------------------------------------------
        # Step 04：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self.update_navigation_buttons()
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return completed

    def update_navigation_buttons(self):
        u"""扩展底部导航：Step 03 完成后允许进入 Finalize。"""
        super(FaceRigWizard, self).update_navigation_buttons()

        if self.current_step_index != 2:
            return

        completed = 2 in self.completed_step_indexes

        if not completed:
            face_context = self.get_face_guide()

            if face_context.config_node_exists():
                completed = face_context.is_step_completed(
                    step_value=3
                )

        self.next_button.setEnabled(
            bool(completed)
        )

        if completed:
            self.next_button.setText(
                u"进入 Finalize"
            )

    def clicked_next_button(self):
        u"""
        提交原有 Step；Step 03 完成后进入 Step 04 Finalize。

        Returns:
            object | None:
                原 Step 返回结果；Step 03 成功切换页面时返回 None。
        """
        if self.current_step_index != 2:
            return super(FaceRigWizard, self).clicked_next_button()

        face_context = self.get_face_guide()

        if not face_context.config_node_exists():
            return

        if not face_context.is_step_completed(
                step_value=3
        ):
            return

        self.completed_step_indexes.add(
            2
        )
        self.set_current_step(
            3
        )

    # =========================================================================
    # Complete Face Build
    # =========================================================================

    def clicked_build_face(self):
        u"""
        通过 FaceBuild.run_step() 一次构建完整 Face Rig。

        Returns:
            bool:
                Step 03 完整构建成功时返回 True，否则返回 False。
        """
        # -------------------------------------------------------------------------
        # Step 01：进入构建状态并阻止重复点击
        # -------------------------------------------------------------------------
        self.build_face_button.setEnabled(
            False
        )
        self.face_build_status_label.setText(
            u"构建中"
        )
        theme.set_role(
            self.face_build_status_label,
            "pill"
        )
        self.status_label.setText(
            u"正在构建完整 Face Rig"
        )

        # -------------------------------------------------------------------------
        # Step 02：只调用正式 Workflow Step；失败时 FaceBuild 会自动整体 Undo
        # -------------------------------------------------------------------------
        face_build = FaceBuild()

        try:
            face_build.run_step()
        except Exception as error:
            self.face_build_result = None
            self.face_build_status_label.setText(
                u"构建失败"
            )
            theme.set_role(
                self.face_build_status_label,
                "danger_text"
            )
            self.status_label.setText(
                u"Face Build 失败 · 场景已尝试回滚"
            )
            self.build_face_button.setEnabled(
                True
            )

            QMessageBox.critical(
                self,
                u"Face Build 失败",
                u"{}".format(error)
            )
            self.update_navigation_buttons()
            return False

        # -------------------------------------------------------------------------
        # Step 03：保存公开结果并同步 Step 03 UI 完成状态
        # -------------------------------------------------------------------------
        self.face_build_result = face_build.build_result
        self.completed_step_indexes.add(
            2
        )
        self.invalidate_ui_steps_after(
            2
        )

        self.face_build_status_label.setText(
            u"构建完成"
        )
        theme.set_role(
            self.face_build_status_label,
            "pill"
        )
        self.build_face_button.setEnabled(
            False
        )

        # -------------------------------------------------------------------------
        # Step 04：刷新 Workflow / Channel Box，并允许进入 Finalize
        # -------------------------------------------------------------------------
        module_count = len(
            self.face_build_result
        )
        self.status_label.setText(
            u"完整 Face Rig 构建完成 · {} Modules".format(
                module_count
            )
        )
        self.apply_config_channel_box_display()
        self.update_step_buttons()
        self.update_navigation_buttons()
        return True


def main():
    u"""
    创建带 Step 03 Module Build 页面的正式 Face Rig UI。

    Returns:
        object:
        当前工具入口创建并显示的窗口或执行结果。
    """
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
