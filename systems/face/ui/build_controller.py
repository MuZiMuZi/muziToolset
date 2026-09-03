# coding=utf-8
u"""
Face Rig Step 03 Build UI Controller
====================================

Step 03 负责两件事情：
    1. 通过 FaceBuild 一次构建完整 Face Rig；
    2. 在 Controller 创建后继续实时调整 Controller Shape 的尺寸和颜色。

设计边界：
    - Step 02 只负责 Guide 编辑、镜像、修复与完整性提交；
    - Controller Settings 的正式 UI 只显示在 Step 03；
    - Settings 继续保存到现有 Face Config Schema，避免产生第二套数据源；
    - 已构建 Controller 的实时调整只修改 Shape，不修改 Transform / Zero / Guide；
    - Global Scale / Module Size 使用比例更新，不重复累积尺寸误差；
    - Build 失败仍由 FaceBuild 统一 Undo 回滚。
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
from ....ui.widgets import MayaIndexColorSlider
from .. import config
from .. import controller_appearance
from ..build.face_build import FaceBuild
from . import workflow_controller


class FaceRigWizard(workflow_controller.FaceRigWizard):
    u"""Step 03 Build + Controller Appearance 的正式 Face Rig Wizard。"""

    def __init__(self, parent=None):
        u"""
        初始化 Step 03 Build UI。

        Args:
            parent (QWidget | None):
                当前窗口使用的 Qt Parent；未提供时使用 None。
        """
        self.face_build_result = None

        super(FaceRigWizard, self).__init__(
            parent
        )

    # =========================================================================
    # Step 02 UI
    # =========================================================================

    def create_step2_page(self):
        u"""
        创建 Guide 页面，并隐藏旧 Controller Settings Card。

        Workflow Controller 仍负责创建这些旧控件，是为了保持当前继承链和 Config
        恢复逻辑兼容；正式显示与交互控件会在 Step 03 重新创建并替换引用。

        Returns:
            QWidget:
                已创建并隐藏旧 Controller Settings Card 的 Step 02 页面。
        """
        page = super(FaceRigWizard, self).create_step2_page()

        old_global_scale_spin = getattr(
            self,
            "face_ctrl_global_scale_spin",
            None
        )

        if old_global_scale_spin is not None:
            controller_card = old_global_scale_spin.parentWidget()

            if controller_card is not None:
                controller_card.setVisible(
                    False
                )

        return page

    # =========================================================================
    # Controller Settings Data
    # =========================================================================

    def get_step2_controller_settings(self):
        u"""
        从当前 Step 03 UI 收集正式 Controller Settings。

        Returns:
            dict:
                当前 Global Scale、Side Color 与各 Module Size 的设置字典。
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
        使用正式 Config Schema 回填 Step 03 Controller Settings。

        Returns:
            bool:
                Controller Settings 成功回填到 Step 03 UI 时返回 True。
        """
        face_context = self.get_face_guide()
        settings = face_context.load_controller_settings()

        self.loading_controller_settings = True

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

        return True

    # =========================================================================
    # Step 03 Page
    # =========================================================================

    def create_pages(self):
        u"""创建原有页面，并把 Step 03 占位页替换成正式 Build 页面。"""
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
        创建 Step 03 完整 Face Rig Build + Controller Settings 页面。

        Returns:
            QWidget:
                包含 Build 与 Controller Appearance 控件的 Step 03 页面。
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
        # Build Overview
        # ---------------------------------------------------------------------
        intro_card, intro_layout = theme.make_card(
            page
        )
        intro_layout.addWidget(
            theme.make_section_title(
                u"Step 03 · Build"
            )
        )

        intro_description = QLabel(
            u"先构建完整 Face Rig；构建完成后可直接在本页实时调整 Controller Size 和 Color，不需要重新 Build。"
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
        intro_layout.addWidget(
            module_description
        )

        # ---------------------------------------------------------------------
        # Complete Build
        # ---------------------------------------------------------------------
        build_card, build_layout = theme.make_card(
            page
        )
        build_layout.addWidget(
            theme.make_section_title(
                u"Complete Face Rig"
            )
        )

        build_hint = QLabel(
            u"构建失败时整个 Step 03 会自动 Undo 回滚。Controller Settings 会在构建前保存，并作为创建时的初始外观参数。"
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

        # ---------------------------------------------------------------------
        # Controller Appearance
        # ---------------------------------------------------------------------
        controller_card, controller_layout = theme.make_card(
            page
        )
        controller_layout.addWidget(
            theme.make_section_title(
                u"Controller Appearance"
            )
        )

        controller_description = QLabel(
            u"Global Scale 影响整套 Face Controller；Module Size 只影响对应部位；Side Color 按 LF / RT / MD 实时更新。这里只修改 Shape，不会改变 Guide 对齐位置。"
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

        # Step 03 的控件成为唯一正式引用。这样 create_connections() 只会连接这里。
        self.controller_size_widgets = {}
        self.controller_color_widgets = {}

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

        module_labels = {
            "brow": u"Brow",
            "eye": u"Eye",
            "eyelid": u"Eyelid",
            "nose": u"Nose",
            "cheek": u"Cheek",
            "lip": u"Lip",
            "jaw": u"Jaw",
            "teeth": u"Teeth",
            "tongue": u"Tongue",
        }

        row = 2

        for module_name in config.face_controller_module_order:
            size_spin = self.create_size_spin_box(
                value=1.0
            )
            self.controller_size_widgets[module_name] = size_spin

            settings_grid.addWidget(
                QLabel(
                    module_labels.get(
                        module_name,
                        module_name.title()
                    )
                ),
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

        live_hint = QLabel(
            u"未构建时：修改参数只保存到 Scene Config；构建完成后：修改参数会同时保存并立即更新当前 Controller Shape。"
        )
        live_hint.setWordWrap(
            True
        )
        theme.set_role(
            live_hint,
            "muted"
        )
        controller_layout.addWidget(
            live_hint
        )

        main_layout.addWidget(
            intro_card
        )
        main_layout.addWidget(
            build_card
        )
        main_layout.addWidget(
            controller_card
        )
        main_layout.addStretch(
            1
        )

        return page

    # =========================================================================
    # Connections / Channel Box
    # =========================================================================

    def create_connections(self):
        u"""连接 Workflow Signal、Step 03 Settings 和完整 FaceBuild 按钮。"""
        super(FaceRigWizard, self).create_connections()

        self.build_face_button.clicked.connect(
            self.clicked_build_face
        )

    @staticmethod
    def get_channel_box_step_attributes(
            face_context,
            step_value
    ):
        u"""
        把 Controller Settings 的 Channel Box 展示职责迁移到 Step 03。

        Args:
            face_context (FaceGuide):
                当前 Face Workflow 的 Config / Guide 上下文。
            step_value (int):
                需要查询 Channel Box 属性的 Workflow Step 值。

        Returns:
            list[str]:
                当前 Step 应在 Channel Box 中展示的 Config 属性名称。
        """
        if step_value == 1:
            return list(
                face_context.setup_value_attr_names
            )

        if step_value == 3:
            attr_names = []

            for attr_name in config.face_controller_default_settings:
                attr_names.append(
                    attr_name
                )

            return attr_names

        return []

    # =========================================================================
    # Step 03 Settings Live Update
    # =========================================================================

    def controller_settings_changed(
            self,
            value=None
    ):
        u"""
        保存 Step 03 Controller Settings；Rig 已构建时立即更新 Controller Shape。

        这里不再调用 mark_step2_dirty()。Controller 外观属于 Step 03 的可编辑结果，
        调整尺寸或颜色不会使已经完成的 Guide / Build 结构失效。

        Args:
            value (object):
                Qt Value Changed Signal 传入的新值；业务逻辑统一从 UI 重新读取完整设置。

        Returns:
            None:
                本方法直接更新 Scene Config、Controller Shape 与 UI 状态。
        """
        if self.loading_controller_settings:
            return

        face_context = self.get_face_guide()

        if not face_context.config_node_exists():
            return

        previous_settings = face_context.load_controller_settings()
        new_settings = self.get_step2_controller_settings()

        build_completed = face_context.is_step_completed(
            step_value=3
        )

        apply_result = {
            "changed_ctrl_count": 0,
            "scaled_ctrl_count": 0,
            "colored_ctrl_count": 0,
        }

        try:
            if build_completed:
                apply_result = controller_appearance.apply_controller_settings(
                    previous_settings,
                    new_settings
                )

            face_context.save_controller_settings(
                new_settings
            )
            face_context.ensure_config_layout()
            face_context.organize_config_attributes()
            self.apply_config_channel_box_display(
                face_context
            )
        except Exception as error:
            self.status_label.setText(
                u"Controller Appearance 更新失败：{}".format(
                    error
                )
            )
            return

        if build_completed:
            self.status_label.setText(
                u"Controller Appearance 已实时更新 · {} Ctrl".format(
                    apply_result.get(
                        "changed_ctrl_count",
                        0
                    )
                )
            )
        else:
            self.status_label.setText(
                u"Controller Settings 已保存 · 构建时将使用当前参数"
            )

    # =========================================================================
    # Step 03 State / Navigation
    # =========================================================================

    def load_step_config_to_ui(self, step_index):
        u"""
        恢复 Workflow Config，并在 Step 03 回填 Settings 和 Build 状态。

        Args:
            step_index (int):
                当前需要恢复配置的零基 Workflow 页面索引。

        Returns:
            object:
                父级 Workflow Controller 恢复对应 Step 配置后的结果。
        """
        result = super(FaceRigWizard, self).load_step_config_to_ui(
            step_index
        )

        if step_index == 2:
            self.load_step2_controller_settings()
            self.load_step3_build_state()

        return result

    def load_step3_build_state(self):
        u"""
        从 Face Config 恢复 Step 03 完成状态和按钮状态。

        Returns:
            bool:
                Face Config 已标记 Step 03 完成时返回 True，否则返回 False。
        """
        face_context = self.get_face_guide()
        completed = False

        if face_context.config_node_exists():
            completed = face_context.is_step_completed(
                step_value=3
            )

        if completed:
            self.completed_step_indexes.add(
                2
            )
            self.face_build_status_label.setText(
                u"构建完成 · 可实时调整外观"
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

        self.update_navigation_buttons()
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
            object:
                非 Step 03 时返回父级导航结果；Step 03 内部导航完成时返回 None。
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
                Face Rig 构建成功时返回 True；参数保存或 Build 失败时返回 False。
        """
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

        face_context = self.get_face_guide()

        try:
            # 确保 Build 使用当前 Step 03 UI 中刚刚设置的参数。
            face_context.save_controller_settings(
                self.get_step2_controller_settings()
            )
        except Exception as error:
            self.face_build_status_label.setText(
                u"参数保存失败"
            )
            self.build_face_button.setEnabled(
                True
            )
            QMessageBox.critical(
                self,
                u"Controller Settings 保存失败",
                u"{}".format(error)
            )
            return False

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

        self.face_build_result = face_build.build_result
        self.completed_step_indexes.add(
            2
        )
        self.invalidate_ui_steps_after(
            2
        )

        self.face_build_status_label.setText(
            u"构建完成 · 可实时调整外观"
        )
        theme.set_role(
            self.face_build_status_label,
            "pill"
        )
        self.build_face_button.setEnabled(
            False
        )

        module_count = len(
            self.face_build_result
        )
        self.status_label.setText(
            u"完整 Face Rig 构建完成 · {} Modules · Controller Appearance 已开启实时调整".format(
                module_count
            )
        )
        self.apply_config_channel_box_display()
        self.update_step_buttons()
        self.update_navigation_buttons()
        return True


def main():
    u"""
    创建带 Step 03 Build / Live Controller Settings 的正式 Face Rig UI。

    Returns:
        FaceRigWizard:
            新创建的 Step 03 Face Rig Wizard 实例。
    """
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
