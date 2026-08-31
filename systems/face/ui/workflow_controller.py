# coding=utf-8
u"""
Face Rig Workflow UI Controller
===============================

在 FaceRigWizard 视图之上统一处理 Config -> UI 恢复和 Step Scene Visibility。

职责：
    1. 进入或回退 Step 时，从 Scene Config 恢复对应 UI；
    2. Step 01 恢复模型引用和 Mouth Joint Number；
    3. Step 02 恢复并实时持久化 Controller Settings；
    4. 当前 UI Step 切换时直接应用 config.py 定义的场景显示规则；
    5. 不复制 Face Setup / Guide 的业务构建算法。

设计原则：
    - Scene Config 是可恢复 UI 参数的唯一持久化来源；
    - UI 临时查看某个旧 Step 不修改正式 Workflow Progress；
    - 修改 Step 02 参数会保存 Config，并把 Step 02 标记 Dirty；
    - Guide Locator 的位置由 Maya Scene 自身保存；
    - Workflow 显示规则直接定义在 systems.face.config，不再额外维护 workflow.py。
"""

from __future__ import print_function

import maya.cmds as cmds

from .. import config
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
        u"""切换 UI Step，并恢复 Config 数据与场景显示状态。"""
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
        u"""把当前 Step 已保存的 Scene Config 回填到 UI。"""
        if step_index == 0:
            return self.load_step1_config_to_ui()

        if step_index == 1:
            return self.load_step2_config_to_ui()

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
        u"""进入 Step 02 后加载 Guide，并确保 Controller Settings 已保存。"""
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
        u"""Controller Settings 修改后立即保存，并把 Step 02 标记 Dirty。"""
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

    @staticmethod
    def set_node_visibility(
            node,
            visible
    ):
        u"""设置一个 Face DAG 节点 Visibility，并保留原 Lock 状态。"""
        if not node:
            return False

        if not cmds.objExists(node):
            return False

        plug = "{}.visibility".format(
            node
        )

        if not cmds.objExists(plug):
            return False

        try:
            was_locked = cmds.getAttr(
                plug,
                lock=True
            )
        except Exception:
            return False

        if was_locked:
            cmds.setAttr(
                plug,
                lock=False
            )

        try:
            cmds.setAttr(
                plug,
                bool(visible)
            )
        finally:
            if was_locked:
                cmds.setAttr(
                    plug,
                    lock=True
                )

        return True

    @staticmethod
    def get_long_node(node):
        u"""返回唯一 Long Name。"""
        if not node:
            return None

        matches = cmds.ls(
            node,
            long=True
        )

        if matches is None:
            matches = []

        if len(matches) != 1:
            return None

        return matches[0]

    def get_model_branch_under_root(
            self,
            face_context,
            node
    ):
        u"""返回一个模型在 Face Model Group 下所属的第一层分支。"""
        model_root = self.get_long_node(
            face_context.face_model_grp
        )
        current_node = self.get_long_node(
            node
        )

        if not model_root or not current_node:
            return None

        while current_node:
            parents = cmds.listRelatives(
                current_node,
                parent=True,
                fullPath=True
            )

            if parents is None:
                parents = []

            if not parents:
                return None

            parent = parents[0]

            if parent == model_root:
                return current_node

            current_node = parent

        return None

    def apply_setup_source_model_visibility(self, face_context):
        u"""Step 01 / 02 只显示 Config 中保存的原始输入模型分支。"""
        if not face_context.config_node_exists():
            return False

        setup_data = face_context.get_setup_data(
            refresh=True
        )
        source_models = []

        for attr_name in face_context.setup_message_attr_names:
            model = setup_data.get(
                attr_name
            )

            if not model:
                continue

            if not cmds.objExists(model):
                continue

            source_models.append(
                model
            )

        if not source_models:
            return False

        model_children = cmds.listRelatives(
            face_context.face_model_grp,
            children=True,
            type="transform",
            fullPath=True
        )

        if model_children is None:
            model_children = []

        visible_branches = []

        for source_model in source_models:
            branch = self.get_model_branch_under_root(
                face_context,
                source_model
            )

            if not branch:
                continue

            if branch not in visible_branches:
                visible_branches.append(
                    branch
                )

        for model_child in model_children:
            self.set_node_visibility(
                model_child,
                model_child in visible_branches
            )

        for source_model in source_models:
            self.set_node_visibility(
                source_model,
                True
            )

        return True

    def apply_step_scene_visibility(
            self,
            step_index
    ):
        u"""切换 Step 时直接应用 config.py 定义的 Face 显示规则。"""
        if step_index < 0:
            return False

        step_value = step_index + 1
        visibility_rule = config.face_step_visibility_rules.get(
            step_value
        )

        if visibility_rule is None:
            return False

        face_context = self.get_face_guide()

        try:
            # 步骤 1：切换 Face 顶层功能组。
            for group_attr_name in visibility_rule:
                group_name = getattr(
                    face_context,
                    group_attr_name,
                    None
                )
                self.set_node_visibility(
                    group_name,
                    visibility_rule[group_attr_name]
                )

            # 步骤 2：Step 01 / 02 只保留原始 Setup 模型可见。
            model_display_rule = config.face_step_model_display_rules.get(
                step_value,
                "preserve"
            )

            if model_display_rule == "setup_sources":
                self.apply_setup_source_model_visibility(
                    face_context
                )
        except Exception:
            # Visibility 只是工作流辅助，不阻止 Face Rig 打开。
            return False

        return True


def main():
    u"""创建正式 Face Rig Workflow Wizard。"""
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
