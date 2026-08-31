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
    5. 清理已经废弃的旧 Controller Settings Attribute；
    6. 不复制 Face Setup / Guide 的业务构建算法。

设计原则：
    - Scene Config 是可恢复 UI 参数的唯一持久化来源；
    - UI 临时查看某个旧 Step 不修改正式 Workflow Progress；
    - 修改 Step 02 参数会保存 Config，并把 Step 02 标记 Dirty；
    - Guide Locator 的位置由 Maya Scene 自身保存；
    - Workflow 显示规则直接定义在 systems.face.config；
    - Controller Config Attribute 使用 [类型]_[方向]_[部位]_[功能]，不带序号。
"""

from __future__ import print_function

import maya.cmds as cmds

from .. import config
from . import face_rig_ui


class FaceRigWizard(face_rig_ui.FaceRigWizard):
    u"""带 Config 恢复和 Scene Visibility 管理的正式 Face Rig Wizard。"""

    # =========================================================================
    # Step 02 UI Extension
    # =========================================================================

    def create_step2_page(self):
        u"""创建 Step 02，并补充 Teeth / Tongue Controller Size。"""
        page = super(FaceRigWizard, self).create_step2_page()

        brow_spin = self.controller_size_widgets.get(
            "brow"
        )

        if brow_spin is None:
            return page

        controller_card = brow_spin.parentWidget()

        if controller_card is None:
            return page

        controller_layout = controller_card.layout()

        if controller_layout is None:
            return page

        settings_grid = None
        layout_index = 0

        while layout_index < controller_layout.count():
            layout_item = controller_layout.itemAt(
                layout_index
            )
            child_layout = layout_item.layout()

            if isinstance(
                    child_layout,
                    face_rig_ui.QGridLayout
            ):
                settings_grid = child_layout
                break

            layout_index += 1

        if settings_grid is None:
            return page

        module_items = [
            ("teeth", u"Teeth"),
            ("tongue", u"Tongue"),
        ]

        row = settings_grid.rowCount()

        for module_item in module_items:
            module_name = module_item[0]
            label_text = module_item[1]

            if module_name in self.controller_size_widgets:
                continue

            size_spin = self.create_size_spin_box(
                value=1.0
            )
            self.controller_size_widgets[module_name] = size_spin

            settings_grid.addWidget(
                face_rig_ui.QLabel(label_text),
                row,
                2
            )
            settings_grid.addWidget(
                size_spin,
                row,
                3
            )
            row += 1

        return page

    # =========================================================================
    # Config Schema
    # =========================================================================

    @staticmethod
    def sync_controller_config_schema(face_context):
        u"""把 FaceBase Step 02 Attribute 顺序切换到当前正式 Config Schema。"""
        if face_context is None:
            return False

        face_context.step_config_attr_names[2] = list(
            config.face_step_02_config_attr_names
        )
        return True

    @staticmethod
    def remove_legacy_controller_setting_attributes(face_context):
        u"""删除旧版 Controller Settings Attribute，不迁移旧值。"""
        if face_context is None:
            return []

        if not face_context.config_node_exists():
            return []

        removed_attrs = []

        for attr_name in config.legacy_face_controller_setting_attr_names:
            plug = "{}.{}".format(
                face_context.config_node,
                attr_name
            )

            if not cmds.objExists(plug):
                continue

            try:
                if cmds.getAttr(
                        plug,
                        lock=True
                ):
                    cmds.setAttr(
                        plug,
                        lock=False
                    )

                cmds.deleteAttr(
                    plug
                )
                removed_attrs.append(
                    attr_name
                )
            except Exception:
                continue

        return removed_attrs

    @staticmethod
    def add_validation_aliases(settings):
        u"""
        给当前 FaceGuide 旧验证逻辑补充临时字典 Alias。

        Alias 只存在于 Python dict 中，不会写入 Scene Config。
        """
        result = {}

        for attr_name in settings:
            result[attr_name] = settings.get(
                attr_name
            )

        result["face_ctrl_global_scale"] = settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )
        result["face_ctrl_color_lf"] = settings.get(
            config.face_controller_color_attr_names["lf"],
            6
        )
        result["face_ctrl_color_rt"] = settings.get(
            config.face_controller_color_attr_names["rt"],
            13
        )
        result["face_ctrl_color_md"] = settings.get(
            config.face_controller_color_attr_names["md"],
            17
        )

        return result

    def prepare_controller_config_schema(self, face_context):
        u"""应用新 Schema、删除旧属性并重新整理 Attribute 顺序。"""
        if face_context is None:
            return False

        self.sync_controller_config_schema(
            face_context
        )
        self.remove_legacy_controller_setting_attributes(
            face_context
        )

        if face_context.config_node_exists():
            face_context.ensure_config_layout()
            face_context.organize_config_attributes()

        return True

    # =========================================================================
    # Step Navigation / Restore
    # =========================================================================

    def restore_step_state(self):
        u"""恢复 Workflow 后同步当前 Controller Config Schema。"""
        result = super(FaceRigWizard, self).restore_step_state()
        face_context = self.get_face_guide()

        if not face_context.config_node_exists():
            return result

        self.prepare_controller_config_schema(
            face_context
        )

        # 新 Schema 不迁移旧值；没有保存值时直接使用 config.py 默认设置。
        settings = face_context.load_controller_settings()
        settings = self.add_validation_aliases(
            settings
        )
        face_context.save_controller_settings(
            settings
        )
        face_context.organize_config_attributes()
        return result

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

        self.prepare_controller_config_schema(
            face_context
        )
        return self.load_step2_controller_settings()

    # =========================================================================
    # Step 02 Controller Settings
    # =========================================================================

    def get_step2_controller_settings(self):
        u"""从 UI 收集使用正式命名的 Controller Settings。"""
        settings = {
            config.face_controller_global_scale_attr:
                self.face_ctrl_global_scale_spin.value(),
            config.face_controller_color_attr_names["lf"]:
                self.controller_color_widgets["lf"].get_value(),
            config.face_controller_color_attr_names["rt"]:
                self.controller_color_widgets["rt"].get_value(),
            config.face_controller_color_attr_names["md"]:
                self.controller_color_widgets["md"].get_value(),
        }

        for module_name in config.face_controller_module_order:
            size_widget = self.controller_size_widgets.get(
                module_name
            )

            if size_widget is None:
                continue

            attr_name = config.face_controller_size_attr_names.get(
                module_name
            )

            if not attr_name:
                continue

            settings[attr_name] = size_widget.value()

        return self.add_validation_aliases(
            settings
        )

    def load_step2_controller_settings(self):
        u"""从新命名的 Face Config Attribute 回填 Controller Settings。"""
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
                    attr_name
                )
                self.controller_color_widgets[side].set_value(
                    int(
                        settings.get(
                            attr_name,
                            default_value
                        )
                    )
                )

            for module_name in config.face_controller_module_order:
                size_widget = self.controller_size_widgets.get(
                    module_name
                )

                if size_widget is None:
                    continue

                attr_name = config.face_controller_size_attr_names.get(
                    module_name
                )

                if not attr_name:
                    continue

                size_widget.setValue(
                    float(
                        settings.get(
                            attr_name,
                            1.0
                        )
                    )
                )
        finally:
            self.loading_controller_settings = False

        return True

    # =========================================================================
    # Step 02 Persistence
    # =========================================================================

    def enter_step2(self):
        u"""进入 Step 02 后加载 Guide，并确保新 Controller Settings 已保存。"""
        result = super(FaceRigWizard, self).enter_step2()

        if not result:
            return False

        face_context = self.get_face_guide()

        if not face_context.config_node_exists():
            return True

        self.prepare_controller_config_schema(
            face_context
        )
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
            self.prepare_controller_config_schema(
                face_context
            )
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

    def finalize_step2(self):
        u"""提交 Step 02 后再次按新 Schema 整理 Config Attribute。"""
        result = super(FaceRigWizard, self).finalize_step2()

        if not result:
            return False

        face_context = self.get_face_guide()
        self.prepare_controller_config_schema(
            face_context
        )
        return True

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
