# coding=utf-8
u"""
Face Rig Workflow Lifecycle UI Controller
=========================================

在完整 Setup / Guide / Build / Finalize UI 之上统一收紧 Workflow 生命周期。

正式规则：
    1. 向前进入下一 Step 只能点击底部“下一步”按钮；
    2. 顶部 Step Navigation 只能向后回退，不能用于向前跳转；
    3. Step 02 点击“下一步”时自动 Finalize Guide 并自动执行完整 Step 03 Build；
    4. Step 03 页面只显示 Controller Appearance，不再提供独立 Build 按钮；
    5. Step 03 -> Step 02 回退会删除 Step 03 / 04 生成物，但保留当前 Guide 和 Settings；
    6. Step 02 -> Step 01 回退会先保存 Guide Snapshot，再删除 Guide 和后续生成物；
    7. Step 01 再进入 Step 02 时重新导入标准模板，并自动恢复保存的 Guide Snapshot；
    8. Enter / Return 不允许触发底部“下一步”，Controller Appearance 修改不会推进 Workflow。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QGridLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QGridLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ....ui import theme
from ....ui.widgets import MayaIndexColorSlider
from .. import config
from .. import workflow_lifecycle
from ..build.face_build import FaceBuild
from . import finalize_controller


class FaceRigWizard(finalize_controller.FaceRigWizard):
    u"""应用正式回退清理、自动 Build 和 Click-only 前进规则的 Face Rig Wizard。"""

    def __init__(self, parent=None):
        u"""
        初始化最终 Workflow 生命周期 UI。

        Args:
            parent (QWidget | None):
                可选 Qt 父窗口。
        """
        super(FaceRigWizard, self).__init__(
            parent
        )

        # “下一步”只允许鼠标明确点击，不参与 Dialog Default Button / Keyboard Focus。
        self.next_button.setAutoDefault(
            False
        )
        self.next_button.setDefault(
            False
        )
        self.next_button.setFocusPolicy(
            Qt.NoFocus
        )

        if hasattr(self, "build_face_button"):
            self.build_face_button.setAutoDefault(
                False
            )
            self.build_face_button.setDefault(
                False
            )
            self.build_face_button.setFocusPolicy(
                Qt.NoFocus
            )

    # =========================================================================
    # Step 03 Appearance-only Page
    # =========================================================================

    def create_step3_page(self):
        u"""
        创建只包含 Controller Appearance 的 Step 03 页面。

        Step 03 的 Rig 已经由 Step 02 底部“下一步”自动完成，因此本页不再显示
        Complete Face Rig、Build 状态和独立构建按钮。

        Returns:
            QWidget:
                只包含 Controller Size / Color 设置的 Step 03 页面。
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

        # 父级 Build Controller 仍会连接 / 更新这两个历史控件。
        # 保留隐藏实例只用于继承兼容，不把它们加入页面布局。
        self.face_build_status_label = QLabel(
            u"自动构建"
        )
        self.face_build_status_label.setParent(
            page
        )
        self.face_build_status_label.setVisible(
            False
        )

        self.build_face_button = QPushButton(
            u"自动构建 Face Rig"
        )
        self.build_face_button.setParent(
            page
        )
        self.build_face_button.setVisible(
            False
        )

        controller_card, controller_layout = theme.make_card(
            page
        )
        controller_layout.addWidget(
            theme.make_section_title(
                u"Controller Appearance"
            )
        )

        controller_description = QLabel(
            u"Step 02 点击“下一步”后绑定已经自动创建。本页只调整 Controller Shape 的大小和颜色；不会修改 Transform、Guide、Output 或 Jnt。"
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

        global_default = config.face_controller_default_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )

        settings_grid.addWidget(
            QLabel(u"Global Scale"),
            0,
            0
        )
        self.face_ctrl_global_scale_spin = self.create_size_spin_box(
            value=global_default
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

        side_labels = {
            "lf": u"LF",
            "rt": u"RT",
            "md": u"MD",
        }
        row = 2

        for side in ["lf", "rt", "md"]:
            attr_name = config.face_controller_color_attr_names.get(
                side
            )
            default_color = config.face_controller_default_settings.get(
                attr_name,
                17
            )

            color_widget = MayaIndexColorSlider(
                value=int(default_color)
            )
            self.controller_color_widgets[side] = color_widget

            settings_grid.addWidget(
                QLabel(
                    side_labels.get(
                        side,
                        side.upper()
                    )
                ),
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
            attr_name = config.face_controller_size_attr_names.get(
                module_name
            )
            default_size = config.face_controller_default_settings.get(
                attr_name,
                1.0
            )
            size_spin = self.create_size_spin_box(
                value=default_size
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
            u"Controller Appearance 会实时保存到 Face Config。回退到 Guide 或 Setup 后再次构建，仍会沿用这里的自定义设置。"
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
            controller_card
        )
        main_layout.addStretch(
            1
        )
        return page

    # =========================================================================
    # Guide Snapshot Restore
    # =========================================================================

    def enter_step2(self):
        u"""
        进入 Step 02；Guide 被重新导入时自动恢复上一次保存的位置快照。

        Returns:
            bool:
                Guide 加载和 Snapshot 恢复成功时返回 True。
        """
        face_guide = self.get_face_guide(
            refresh=True
        )

        try:
            guide_existed = face_guide.guide_exists()
        except Exception:
            guide_existed = False

        result = super(FaceRigWizard, self).enter_step2()

        if not result:
            return False

        if guide_existed:
            return True

        face_guide = self.get_face_guide()

        try:
            restored_locators = workflow_lifecycle.restore_guide_snapshot(
                face_guide
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                u"Guide Snapshot 恢复失败",
                u"{}".format(error)
            )
            return False

        if restored_locators:
            self.refresh_step2_summary()
            self.status_label.setText(
                u"Face Guide 已重新导入 · 恢复 {} 个自定义 Locator 位置".format(
                    len(restored_locators)
                )
            )

        return True

    # =========================================================================
    # Forward Navigation - Only Bottom Next Button
    # =========================================================================

    def clicked_next_button(self):
        u"""
        唯一允许向前推进 Workflow 的正式入口。

        Returns:
            object | bool | None:
                Step 01 返回父级执行结果；Step 02 自动 Build 成功时返回 True；
                Step 03 进入 Finalize 时返回 True；其它情况返回 None / False。
        """
        # Step 01 -> Step 02：继续使用正式 FaceSetup，然后由 enter_step2() 恢复 Guide Snapshot。
        if self.current_step_index == 0:
            return super(FaceRigWizard, self).clicked_next_button()

        # Step 02 -> Step 03：提交 Guide 后立即自动创建绑定。
        if self.current_step_index == 1:
            if not self.finalize_step2():
                return False

            face_guide = self.get_face_guide()

            try:
                workflow_lifecycle.save_guide_snapshot(
                    face_guide
                )
            except Exception:
                pass

            if not self.clicked_build_face():
                face_guide.set_step_completed(
                    step_value=3,
                    completed=False
                )
                face_guide.set_current_step_value(
                    2
                )
                self.current_step_index = 1
                self.page_stack.setCurrentIndex(
                    1
                )
                self.apply_step_scene_visibility(
                    1
                )
                self.update_step_buttons()
                self.update_navigation_buttons()
                return False

            # FaceBuild 的独立 API 契约会把 Current Step 推到 04。
            # 在 Wizard 中 Step 03 仍需由用户检查外观，因此自动 Build 后明确退回 03。
            face_guide.set_current_step_value(
                3
            )
            self.set_current_step(
                2
            )
            self.status_label.setText(
                u"Face Rig 已自动构建 · Step 03 可调整 Controller Appearance"
            )
            return True

        # Step 03 -> Step 04：只有用户明确点击底部按钮时才推进。
        if self.current_step_index == 2:
            face_context = self.get_face_guide()

            if not face_context.config_node_exists():
                return False

            if not face_context.is_step_completed(
                    step_value=3
            ):
                return False

            face_context.set_current_step_value(
                4
            )
            self.completed_step_indexes.add(
                2
            )
            self.set_current_step(
                3
            )
            return True

        return None

    # =========================================================================
    # Automatic Step 03 Build
    # =========================================================================

    def clicked_build_face(self):
        u"""
        自动构建完整 Face Rig，并记录 Step 03 Scene Manifest。

        该方法保留父级方法名用于现有继承契约，但正式 UI 不再显示 Build 按钮；
        实际调用只来自 Step 02 底部“下一步”。

        Returns:
            bool:
                完整 Face Rig 构建和 Manifest 保存成功时返回 True。
        """
        self.build_face_button.setEnabled(
            False
        )
        self.face_build_status_label.setText(
            u"构建中"
        )
        self.status_label.setText(
            u"正在自动构建完整 Face Rig"
        )

        face_context = self.get_face_guide()

        try:
            face_context.save_controller_settings(
                self.get_step2_controller_settings()
            )
        except Exception as error:
            self.build_face_button.setEnabled(
                True
            )
            QMessageBox.critical(
                self,
                u"Controller Settings 保存失败",
                u"{}".format(error)
            )
            return False

        before_state = workflow_lifecycle.capture_scene_state()
        face_build = FaceBuild()

        try:
            face_build.run_step()
        except Exception as error:
            self.face_build_result = None
            self.face_build_status_label.setText(
                u"构建失败"
            )
            self.build_face_button.setEnabled(
                True
            )
            self.status_label.setText(
                u"Face Build 失败 · 场景已尝试回滚"
            )
            QMessageBox.critical(
                self,
                u"Face Build 失败",
                u"{}".format(error)
            )
            self.update_navigation_buttons()
            return False

        self.face_build_result = face_build.build_result

        manifest = workflow_lifecycle.create_scene_manifest(
            before_state
        )
        workflow_lifecycle.save_step_manifest(
            face_context,
            3,
            manifest
        )

        self.completed_step_indexes.add(
            2
        )
        self.invalidate_ui_steps_after(
            2
        )
        self.face_build_status_label.setText(
            u"构建完成"
        )
        self.build_face_button.setEnabled(
            False
        )

        # 防止 WindowActivate / Scene Reload 读取 FaceBuild 的 Current Step=04 后自动跳页。
        face_context.set_current_step_value(
            3
        )

        module_count = 0

        if self.face_build_result:
            module_count = len(
                self.face_build_result
            )

        self.status_label.setText(
            u"完整 Face Rig 自动构建完成 · {} Modules".format(
                module_count
            )
        )
        self.apply_config_channel_box_display(
            face_context
        )
        self.update_step_buttons()
        self.update_navigation_buttons()
        return True

    # =========================================================================
    # Back Navigation - Cleanup Later Steps
    # =========================================================================

    def clicked_step_button(self):
        u"""
        顶部 Step Navigation 只处理向后回退，并在切换前清理后续生成物。

        Returns:
            bool | None:
                成功回退时返回 True；无效点击或向前点击时返回 None / False。
        """
        step_button = self.sender()

        if step_button is None:
            return None

        step_index = step_button.property(
            "step_index"
        )

        if step_index is None:
            return None

        step_index = int(
            step_index
        )

        # 顶部 Navigation 永远不能向前，也不能重复进入当前 Step。
        if step_index >= self.current_step_index:
            return None

        if step_index not in self.completed_step_indexes:
            return False

        face_context = self.get_face_guide()

        try:
            # Appearance 是持久用户设置，回退前再保存一次当前 UI 值。
            if self.current_step_index >= 2:
                face_context.save_controller_settings(
                    self.get_step2_controller_settings()
                )

            workflow_lifecycle.cleanup_to_step(
                face_context,
                step_index + 1,
                face_guide=face_context
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                u"Face Workflow 回退失败",
                u"{}".format(error)
            )
            return False

        later_index = step_index + 1

        while later_index < len(self.step_buttons):
            self.completed_step_indexes.discard(
                later_index
            )
            later_index += 1

        self.set_current_step(
            step_index
        )

        if step_index == 0:
            self.status_label.setText(
                u"已回退到 Step 01 · Guide 位置快照和 Controller Settings 已保留"
            )
        elif step_index == 1:
            self.status_label.setText(
                u"已回退到 Step 02 · 后续绑定已清理，可修改 Guide 后重新构建"
            )
        elif step_index == 2:
            self.status_label.setText(
                u"已回退到 Step 03 · Step 04 结果已清理"
            )

        return True

    def update_step_buttons(self):
        u"""
        刷新顶部 Step Button，并强制所有未来 Step 保持不可点击。

        Returns:
            None:
                直接更新 UI Button 状态。
        """
        super(FaceRigWizard, self).update_step_buttons()

        for step_index in range(len(self.step_buttons)):
            if step_index <= self.current_step_index:
                continue

            self.step_buttons[step_index].setEnabled(
                False
            )

    # =========================================================================
    # Step 04 Manifest
    # =========================================================================

    def clicked_finalize_face(self):
        u"""
        执行正式 Finalize，并记录 Step 04 新建节点 Manifest。

        Returns:
            bool:
                Finalize 成功并保存 Manifest 时返回 True，否则返回 False。
        """
        before_state = workflow_lifecycle.capture_scene_state()
        result = super(FaceRigWizard, self).clicked_finalize_face()

        if not result:
            return False

        face_context = self.get_face_guide()
        manifest = workflow_lifecycle.create_scene_manifest(
            before_state
        )
        workflow_lifecycle.save_step_manifest(
            face_context,
            4,
            manifest
        )
        return True


def main():
    u"""
    创建应用正式 Workflow Lifecycle 的 Face Rig UI。

    Returns:
        FaceRigWizard:
            最终 Face Rig Wizard 实例。
    """
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
