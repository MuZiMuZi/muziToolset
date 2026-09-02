# coding=utf-8
u"""
Face Rig Step 03 Build UI Controller
====================================

在现有 Workflow Controller 之上补充 Step 03 Component Build 页面。

设计边界：
    1. Step 01 / Step 02 的稳定 UI 和 Workflow 逻辑保持不变；
    2. 本层只负责 Step 03 的 Component 触发和状态反馈；
    3. 具体 Teeth Rig 算法仍然只存在于 systems.face.build；
    4. Step 03 暂时不自动标记完成，因为 Jaw / Lip / Eye 等 Component 尚未全部接入；
    5. 后续 Component 继续按照相同 Card + Public Build API 的模式加入。
"""

from __future__ import print_function

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QHBoxLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QPushButton
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QHBoxLayout
    from PySide6.QtWidgets import QLabel
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtWidgets import QVBoxLayout
    from PySide6.QtWidgets import QWidget

from ....ui import theme
from ..build import build_teeth
from . import workflow_controller


class FaceRigWizard(workflow_controller.FaceRigWizard):
    u"""增加 Step 03 Component Build 页面后的正式 Face Rig Wizard。"""

    def __init__(self, parent=None):
        u"""初始化 Step 03 Build UI。"""
        self.teeth_build_result = None

        super(FaceRigWizard, self).__init__(
            parent
        )

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
        u"""创建 Step 03 Component Build 页面。"""
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
            u"Face Component 按模块独立构建。当前先接入 Teeth；后续 Jaw、Lip、Eye、Eyelid、Brow、Nose、Cheek、Tongue 会继续加入同一页面。"
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

        teeth_card, teeth_layout = theme.make_card(
            page
        )
        teeth_layout.addWidget(
            theme.make_section_title(
                u"Teeth"
            )
        )

        teeth_description = QLabel(
            u"Upper / Lower Teeth 使用 Guide → Controller → Bind Joint → Rigid Skin。Gum 不在 Teeth Component 中绑定，后续由 Mouth / Jaw Deformation 处理。"
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
        future_layout.addWidget(
            theme.make_section_title(
                u"Next Components"
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

        return page

    # =========================================================================
    # Connections
    # =========================================================================

    def create_connections(self):
        u"""连接原有信号和 Step 03 Teeth Build 信号。"""
        super(FaceRigWizard, self).create_connections()

        self.build_teeth_button.clicked.connect(
            self.clicked_build_teeth
        )

    # =========================================================================
    # Teeth Build
    # =========================================================================

    def clicked_build_teeth(self):
        u"""通过 Face System 公共 API 构建 Teeth Component。"""
        self.build_teeth_button.setEnabled(
            False
        )
        self.teeth_build_status_label.setText(
            u"构建中"
        )
        self.status_label.setText(
            u"正在构建 Teeth Component"
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
                u"Teeth Component 构建失败"
            )
            self.build_teeth_button.setEnabled(
                True
            )

            QMessageBox.critical(
                self,
                u"Teeth Component 构建失败",
                u"{}".format(error)
            )
            return False

        self.teeth_build_result = result
        self.teeth_build_status_label.setText(
            u"构建完成"
        )
        theme.set_role(
            self.teeth_build_status_label,
            "pill"
        )
        self.status_label.setText(
            u"Teeth Component 构建完成"
        )

        # Teeth Component 会主动阻止重复构建，因此成功后保持按钮禁用。
        self.build_teeth_button.setEnabled(
            False
        )
        return True


def main():
    u"""创建带 Step 03 Build 页面的正式 Face Rig UI。"""
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
