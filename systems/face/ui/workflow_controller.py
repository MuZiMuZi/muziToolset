# coding=utf-8
u"""
Face Rig Workflow UI Controller
===============================

在 FaceRigWizard 视图之上统一处理 Config -> UI 恢复和 Step Scene Visibility。

职责：
    1. 进入或回退 Step 时，从 Scene Config 恢复对应 UI；
    2. Step 01 恢复模型引用和 Mouth Joint Number；
    3. Step 02 恢复并实时持久化 Controller Settings；
    4. 当前 UI Step 切换时应用 Face Workflow Scene Visibility；
    5. 不复制 Face Setup / Guide 的业务构建算法。

设计原则：
    - Scene Config 是可恢复 UI 参数的唯一持久化来源；
    - UI 临时查看某个旧 Step 不修改正式 Workflow Progress；
    - 修改 Step 02 参数会保存 Config，并把 Step 02 标记为 Dirty；
    - Guide Locator 的位置由 Maya Scene 自身保存，不重复序列化到 UI Config。
"""

from __future__ import print_function

from .. import workflow
from . import face_rig_ui


class FaceRigWizard(face_rig_ui.FaceRigWizard):
    u"""带 Config 恢复和 Scene Visibility 管理的正式 Face Rig Wizard。"""

    # =========================================================================
    # Step Navigation / Restore
    # =========================================================================

    def set_current_step(
            self,
            step_index
    ):
        u"""
        切换 UI Step，并恢复该 Step 的 Config 数据与场景显示状态。

        正式 Workflow Progress 仍由 FaceBase 保存，本方法只控制当前查看页面。
        """
        result = super(FaceRigWizard, self).set_current_step(
            step_index
        )

        self.load_step_config_to_ui(
            step_index
        )
        self.apply_step_scene_visibility(
            step_index
        )

        return result

    def load_step_config_to_ui(
            self,
            step_index
    ):
        u"""根据 Step Index 把 Scene Config 中已保存的数据回填到 UI。"""
        if step_index == 0:
            return self.load_step1_config_to_ui()

        if step_index == 1:
            return self.load_step2_config_to_ui()

        # Step 03 / 04 目前还是 Placeholder。
        # 后续正式加入 Build / Finalize 参数时继续在这里接入对应 Loader。
        return True

    def load_step1_config_to_ui(self):
        u"""从 Face Config 恢复 Step 01 模型引用和 Mouth Joint Number。"""
        face_context = self.get_face_guide()

        if not face_context.config_node_exists():
            return False

        setup_data = face_context.get_setup_data(
            refresh=True
        )

        picker_data = [
            (self.face_head_picker, "face_head_model"),
            (self.face_lf_eye_picker, "face_lf_eye_model"),
            (self.face_rt_eye_picker, "face_rt_eye_model"),
            (self.upper_teech_picker, "upper_teech_model"),
            (self.lower_teech_picker, "lower_teech_model"),
            (self.face_tongue_picker, "face_tongue_model"),
            (self.face_gum_picker, "face_gum_model"),
        ]

        for picker_item in picker_data:
            picker = picker_item[0]
            attr_name = picker_item[1]
            value = setup_data.get(
                attr_name
            )

            if value:
                picker.set_value(
                    value
                )
            else:
                picker.clear()

        mouth_jnt_number = setup_data.get(
            "mouth_jnt_number"
        )

        if mouth_jnt_number is not None:
            slider_value = int(
                round(
                    float(mouth_jnt_number) / self.mouth_joint_step
                )
            )
            self.mouth_joint_slider.setValue(
                slider_value
            )

        return True

    def load_step2_config_to_ui(self):
        u"""从 Face Config 恢复 Step 02 Controller Settings。"""
        face_context = self.get_face_guide()

        if not face_context.config_node_exists():
            return False

        return self.load_step2_controller_settings()

    # =========================================================================
    # Step 02 Persistence
    # =========================================================================

    def enter_step2(self):
        u"""
        进入 Step 02 后加载 Guide，并确保 Controller Settings 已持久化到 Config。

        即使用户从未修改默认值，Scene Config 也会拥有完整的 Step 02 参数。
        """
        result = super(FaceRigWizard, self).enter_step2()

        if not result:
            return False

        face_context = self.get_face_guide()

        if not face_context.config_node_exists():
            return True

        settings = self.get_step2_controller_settings()
        face_context.save_controller_settings(
            settings
        )
        face_context.ensure_config_layout()
        face_context.organize_config_attributes()
        return True

    def controller_settings_changed(
            self,
            value=None
    ):
        u"""
        Controller Settings 修改后立即保存到 Scene Config，并把 Step 02 标记 Dirty。

        参数持久化和 Step Finalize 分开：
            - 修改参数立即保存；
            - 点击“下一步”仍负责 Guide Validation 和 Step Completed。
        """
        if self.loading_controller_settings:
            return

        face_context = self.get_face_guide()
        settings = self.get_step2_controller_settings()

        try:
            face_context.save_controller_settings(
                settings
            )
            face_context.ensure_config_layout()
            face_context.organize_config_attributes()
        except Exception as error:
            self.status_label.setText(
                u"Controller Settings 保存失败：{}".format(
                    error
                )
            )
            return

        self.mark_step2_dirty()
        self.status_label.setText(
            u"Controller Settings 已保存到 Scene Config，Step 02 需要重新提交"
        )

    # =========================================================================
    # Scene Visibility
    # =========================================================================

    def apply_step_scene_visibility(
            self,
            step_index
    ):
        u"""让当前查看 Step 自动控制 Face 顶层功能组 Visibility。"""
        if step_index < 0:
            return False

        step_value = step_index + 1
        face_context = self.get_face_guide()

        try:
            workflow.apply_step_scene_visibility(
                face_context,
                step_value
            )
        except Exception:
            # Visibility 属于工作流显示辅助，不应该阻止用户打开 Face Rig。
            return False

        return True


def main():
    u"""创建正式 Face Rig Workflow Wizard。"""
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
