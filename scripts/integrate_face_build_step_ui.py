# coding=utf-8
from __future__ import print_function

from pathlib import Path


FILE_PATH = Path("systems/face/ui/build_controller.py")


def replace_section(text, start_marker, end_marker, replacement):
    start_index = text.find(start_marker)

    if start_index < 0:
        raise RuntimeError("Start marker not found: {}".format(start_marker))

    end_index = text.find(end_marker, start_index)

    if end_index < 0:
        raise RuntimeError("End marker not found: {}".format(end_marker))

    return (
        text[:start_index] +
        replacement +
        text[end_index:]
    )


def main():
    text = FILE_PATH.read_text(encoding="utf-8")

    text = text.replace(
        "同时修正 UI 与当前 Face Controller Config Schema 的映射。\n",
        "同时把完整 FaceRig Orchestrator 接入正式 Step 03。\n"
    )
    text = text.replace(
        "    3. 本层负责 Step 03 的 Module 触发和状态反馈；\n"
        "    4. Teeth Rig 业务逻辑统一位于 systems.face.modules；\n"
        "    5. Step 03 暂时不自动标记完成，因为其它 Module 尚未全部接入；\n"
        "    6. 后续 Module 继续按照相同 Card + Public Build API 的模式加入。\n",
        "    3. 本层负责 Step 03 完整 FaceBuild 触发和状态反馈；\n"
        "    4. Step 03 只调用 FaceBuild.run_step()，不直接调用具体 Face Module；\n"
        "    5. 完整 Build 成功后允许进入 Step 04 Finalize；\n"
        "    6. Build 失败由 FaceBuild 统一 Undo 回滚，UI 可以安全重试。\n"
    )
    text = text.replace(
        "from ..modules import build_teeth\n",
        "from ..build.face_build import FaceBuild\n"
    )
    text = text.replace(
        "        self.teeth_build_result = None\n",
        "        self.face_build_result = None\n"
    )

    create_step3_page = '''    def create_step3_page(self):
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

'''

    text = replace_section(
        text,
        "    def create_step3_page(self):\n",
        "    # =========================================================================\n    # Connections\n",
        create_step3_page
    )

    create_connections = '''    # =========================================================================
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
        u"""从 Face Config 恢复 Step 03 完成状态和按钮状态。"""
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
        u"""提交原有 Step；Step 03 完成后进入 Step 04 Finalize。"""
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

'''

    text = replace_section(
        text,
        "    # =========================================================================\n    # Connections\n",
        "\ndef main():\n",
        create_connections
    )

    if "build_teeth" in text:
        raise RuntimeError("Old Teeth-only Step 03 API remains in build_controller.py")

    if "teeth_build_result" in text:
        raise RuntimeError("Old teeth_build_result remains in build_controller.py")

    if "clicked_build_teeth" in text:
        raise RuntimeError("Old clicked_build_teeth remains in build_controller.py")

    if "FaceBuild" not in text:
        raise RuntimeError("FaceBuild import was not applied")

    FILE_PATH.write_text(
        text,
        encoding="utf-8",
        newline="\n"
    )


if __name__ == "__main__":
    main()
