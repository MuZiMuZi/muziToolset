# coding=utf-8
u"""
Face Rig Step 04 Finalize UI Controller
=======================================

在 Step 03 Build UI Controller 之上补充正式 Step 04 Finalize 页面。

设计边界：
    1. Step 01 / 02 / 03 UI 和业务保持原有继承链；
    2. Step 04 只调用 FaceFinalizer.run_step()，不直接整理具体 Module；
    3. Finalize 失败由 FaceFinalizer 统一 Undo 回滚；
    4. Finalize 完成后允许重复执行“重新验收”，便于人工修改场景后重新检查；
    5. 文件 Export / Publish 暂不放入当前第一版 Step 04 页面。
"""

from __future__ import print_function

try:
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ....ui import theme
from ..finalize import FaceFinalizer
from . import build_controller


class FaceRigWizard(build_controller.FaceRigWizard):
    u"""增加正式 Step 04 Finalize 页面的 Face Rig Wizard。"""

    def __init__(self, parent=None):
        u"""初始化 Step 04 Finalize UI。"""
        self.face_finalize_result = None

        super(FaceRigWizard, self).__init__(
            parent
        )

    # =========================================================================
    # Step 04 Page
    # =========================================================================

    def create_pages(self):
        u"""创建原有页面，并把 Step 04 占位页替换成正式 Finalize 页面。"""
        super(FaceRigWizard, self).create_pages()

        old_step4_page = self.step4_page
        self.step4_page = self.create_step4_page()

        self.page_stack.removeWidget(
            old_step4_page
        )
        old_step4_page.deleteLater()

        self.page_stack.insertWidget(
            3,
            self.step4_page
        )

    def create_step4_page(self):
        u"""
        创建 Step 04 Finalize 页面。

        Returns:
            QWidget:
                Finalize 操作页面。
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
        # Step 01：说明 Finalize 的边界
        # ---------------------------------------------------------------------
        intro_card, intro_layout = theme.make_card(
            page
        )
        intro_layout.addWidget(
            theme.make_section_title(
                u"Step 04 · Finalize"
            )
        )

        intro_description = QLabel(
            u"Finalize 不再创建绑定节点，只对 Step 03 的最终结果做验收和场景整理。"
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

        # ---------------------------------------------------------------------
        # Step 02：显示本阶段的正式检查内容
        # ---------------------------------------------------------------------
        validation_card, validation_layout = theme.make_card(
            page
        )
        validation_layout.addWidget(
            theme.make_section_title(
                u"Final Validation"
            )
        )

        validation_description = QLabel(
            u"验收内容：Step01/02/03 状态 → Face Hierarchy → Controller → Controller Set → Final Visibility。"
        )
        validation_description.setWordWrap(
            True
        )
        theme.set_role(
            validation_description,
            "muted"
        )
        validation_layout.addWidget(
            validation_description
        )

        visibility_description = QLabel(
            u"完成后：Model / Controller 显示；Guide / Joint / Rig Nodes / Position Driver 隐藏。"
        )
        visibility_description.setWordWrap(
            True
        )
        theme.set_role(
            visibility_description,
            "muted"
        )
        validation_layout.addWidget(
            visibility_description
        )

        # ---------------------------------------------------------------------
        # Step 03：创建 Finalize 状态和执行按钮
        # ---------------------------------------------------------------------
        action_card, action_card_layout = theme.make_card(
            page
        )
        action_card_layout.addWidget(
            theme.make_section_title(
                u"Complete Face Rig"
            )
        )

        action_hint = QLabel(
            u"Finalize 可重复执行。若之后人工修改了 Set 或显示状态，可再次点击重新验收。"
        )
        action_hint.setWordWrap(
            True
        )
        theme.set_role(
            action_hint,
            "muted"
        )
        action_card_layout.addWidget(
            action_hint
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

        self.face_finalize_status_label = QLabel(
            u"等待验收"
        )
        theme.set_role(
            self.face_finalize_status_label,
            "pill"
        )

        self.finalize_face_button = QPushButton(
            u"执行 Finalize"
        )
        theme.style_primary(
            self.finalize_face_button
        )

        action_layout.addWidget(
            self.face_finalize_status_label
        )
        action_layout.addStretch(
            1
        )
        action_layout.addWidget(
            self.finalize_face_button
        )
        action_card_layout.addLayout(
            action_layout
        )

        # ---------------------------------------------------------------------
        # Step 04：组合页面
        # ---------------------------------------------------------------------
        main_layout.addWidget(
            intro_card
        )
        main_layout.addWidget(
            validation_card
        )
        main_layout.addWidget(
            action_card
        )
        main_layout.addStretch(
            1
        )
        return page

    # =========================================================================
    # Connections
    # =========================================================================

    def create_connections(self):
        u"""连接原有 Signal 和 Step 04 Finalize 按钮信号。"""
        super(FaceRigWizard, self).create_connections()

        self.finalize_face_button.clicked.connect(
            self.clicked_finalize_face
        )

    # =========================================================================
    # Step 04 State / Navigation
    # =========================================================================

    def load_step_config_to_ui(self, step_index):
        u"""恢复原 Workflow Config，并在 Step 04 回填 Finalize 状态。"""
        result = super(FaceRigWizard, self).load_step_config_to_ui(
            step_index
        )

        if step_index == 3:
            self.load_step4_finalize_state()

        return result

    def load_step4_finalize_state(self):
        u"""
        从 Face Config 恢复 Step 04 完成状态。

        Returns:
            bool:
                Step 04 已完成时返回 True。
        """
        face_context = self.get_face_guide()
        step3_completed = False
        step4_completed = False

        if face_context.config_node_exists():
            step3_completed = face_context.is_step_completed(
                step_value=3
            )
            step4_completed = face_context.is_step_completed(
                step_value=4
            )

        if step4_completed:
            self.completed_step_indexes.add(
                3
            )
            self.face_finalize_status_label.setText(
                u"验收完成"
            )
            theme.set_role(
                self.face_finalize_status_label,
                "pill"
            )
            self.finalize_face_button.setText(
                u"重新验收 Finalize"
            )
            self.finalize_face_button.setEnabled(
                True
            )
        else:
            self.completed_step_indexes.discard(
                3
            )
            self.face_finalize_status_label.setText(
                u"等待验收"
            )
            theme.set_role(
                self.face_finalize_status_label,
                "pill"
            )
            self.finalize_face_button.setText(
                u"执行 Finalize"
            )
            self.finalize_face_button.setEnabled(
                bool(step3_completed)
            )

        self.update_navigation_buttons()
        return step4_completed

    def update_navigation_buttons(self):
        u"""扩展底部导航：Step 04 不再存在下一阶段。"""
        super(FaceRigWizard, self).update_navigation_buttons()

        if self.current_step_index != 3:
            return

        face_context = self.get_face_guide()
        completed = False

        if face_context.config_node_exists():
            completed = face_context.is_step_completed(
                step_value=4
            )

        if completed:
            self.next_button.setText(
                u"Face Rig 完成"
            )
        else:
            self.next_button.setText(
                u"等待 Finalize"
            )

        self.next_button.setEnabled(
            False
        )

    # =========================================================================
    # Finalize
    # =========================================================================

    def clicked_finalize_face(self):
        u"""
        通过 FaceFinalizer.run_step() 执行完整 Step 04。

        Returns:
            bool:
                Finalize 成功时返回 True，否则返回 False。
        """
        self.finalize_face_button.setEnabled(
            False
        )
        self.face_finalize_status_label.setText(
            u"验收中"
        )
        theme.set_role(
            self.face_finalize_status_label,
            "pill"
        )
        self.status_label.setText(
            u"正在执行 Face Finalize"
        )

        finalizer = FaceFinalizer()

        try:
            finalizer.run_step()
        except Exception as error:
            self.face_finalize_result = None
            self.face_finalize_status_label.setText(
                u"验收失败"
            )
            theme.set_role(
                self.face_finalize_status_label,
                "danger_text"
            )
            self.status_label.setText(
                u"Face Finalize 失败 · 场景已尝试回滚"
            )
            self.finalize_face_button.setText(
                u"重新执行 Finalize"
            )
            self.finalize_face_button.setEnabled(
                True
            )

            QMessageBox.critical(
                self,
                u"Face Finalize 失败",
                u"{}".format(error)
            )
            self.update_navigation_buttons()
            return False

        self.face_finalize_result = finalizer.validation_result
        self.completed_step_indexes.add(
            3
        )

        self.face_finalize_status_label.setText(
            u"验收完成"
        )
        theme.set_role(
            self.face_finalize_status_label,
            "pill"
        )
        self.finalize_face_button.setText(
            u"重新验收 Finalize"
        )
        self.finalize_face_button.setEnabled(
            True
        )

        controller_count = self.face_finalize_result.get(
            "controller_count",
            0
        )
        self.status_label.setText(
            u"Face Rig Finalize 完成 · {} Controllers".format(
                controller_count
            )
        )

        self.apply_config_channel_box_display()
        self.update_step_buttons()
        self.update_navigation_buttons()
        return True


def main():
    u"""创建带 Step 04 Finalize 页面的正式 Face Rig UI。"""
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
