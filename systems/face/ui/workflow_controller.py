# coding=utf-8
u"""
Face Rig Workflow UI Controller
===============================

在 FaceRigWizard 视图之上处理 Config -> UI 恢复和 Step Scene Visibility。

职责：
    1. 进入或回退 Step 时，从 Scene Config 恢复对应 UI；
    2. Step 01 恢复模型引用和 Mouth Joint Number；
    3. Step 02 恢复并实时持久化 Controller Settings；
    4. 当前 UI Step 切换时直接应用 config.py 定义的场景显示规则；
    5. 让中间 Step 内容区域可滚动，底部操作栏始终保持可见；
    6. 不复制 Face Setup / Guide 的业务构建算法。
"""

from __future__ import print_function

import maya.cmds as cmds

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QScrollArea
except ImportError:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QScrollArea

from .. import config
from . import face_rig_ui


class FaceRigWizard(face_rig_ui.FaceRigWizard):
    u"""带 Config 恢复、滚动内容区和 Scene Visibility 管理的正式 Face Rig Wizard。"""

    def __init__(self, parent=None):
        u"""初始化正式 Face Rig Workflow UI。"""
        super(FaceRigWizard, self).__init__(
            parent
        )

        # Base UI 原来只限制宽度，较长 Step 会把窗口高度撑出屏幕。
        # 正式 Workflow 允许窗口自由缩放，超出的 Step 内容交给 ScrollArea。
        self.setMinimumSize(
            600,
            460
        )
        self.resize(
            780,
            720
        )

    # =========================================================================
    # Main Layout
    # =========================================================================

    def create_layouts(self):
        u"""
        创建可缩放的主布局。

        顶部标题和 Step Navigation 固定；
        中间 Step 内容独立滚动；
        底部 Status / 下一步始终固定在窗口底部。
        """
        main_layout = face_rig_ui.QVBoxLayout(
            self
        )
        main_layout.setContentsMargins(
            20,
            18,
            20,
            16
        )
        main_layout.setSpacing(
            14
        )

        # ---------------------------------------------------------------------
        # 顶部固定区
        # ---------------------------------------------------------------------

        main_layout.addWidget(
            self.title_label
        )
        main_layout.addWidget(
            self.subtitle_label
        )

        step_frame = face_rig_ui.QFrame()
        face_rig_ui.theme.set_role(
            step_frame,
            "sub_card"
        )

        step_layout = face_rig_ui.QHBoxLayout(
            step_frame
        )
        step_layout.setContentsMargins(
            7,
            7,
            7,
            7
        )
        step_layout.setSpacing(
            5
        )

        for step_button in self.step_buttons:
            step_layout.addWidget(
                step_button,
                1
            )

        main_layout.addWidget(
            step_frame
        )

        # ---------------------------------------------------------------------
        # 中间可滚动 Step 内容区
        # ---------------------------------------------------------------------

        self.content_scroll_area = QScrollArea()
        self.content_scroll_area.setWidgetResizable(
            True
        )
        self.content_scroll_area.setFrameShape(
            face_rig_ui.QFrame.NoFrame
        )
        self.content_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.content_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )
        self.content_scroll_area.setWidget(
            self.page_stack
        )

        main_layout.addWidget(
            self.content_scroll_area,
            1
        )

        # ---------------------------------------------------------------------
        # 底部固定操作区
        # ---------------------------------------------------------------------

        bottom_layout = face_rig_ui.QHBoxLayout()
        bottom_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )
        bottom_layout.setSpacing(
            10
        )
        bottom_layout.addWidget(
            self.status_label,
            1
        )
        bottom_layout.addWidget(
            self.next_button
        )

        main_layout.addLayout(
            bottom_layout
        )

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

        if hasattr(
                self,
                "content_scroll_area"
        ):
            self.content_scroll_area.verticalScrollBar().setValue(
                0
            )
            self.content_scroll_area.horizontalScrollBar().setValue(
                0
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
    # Step 02 Controller Settings
    # =========================================================================

    def get_step2_controller_settings(self):
        u"""从 UI 收集当前正式命名的 Controller Settings。"""
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

            settings[attr_name] = size_widget.value()

        return settings

    def load_step2_controller_settings(self):
        u"""从 Face Config 回填当前正式 Controller Settings。"""
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
        u"""进入 Step 02 后加载 Guide，并保存当前 Controller Settings。"""
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

    def finalize_step2(self):
        u"""提交 Step 02 后整理 Config Attribute 顺序。"""
        result = super(FaceRigWizard, self).finalize_step2()

        if not result:
            return False

        face_context = self.get_face_guide()
        face_context.organize_config_attributes()
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

            model_display_rule = config.face_step_model_display_rules.get(
                step_value,
                "preserve"
            )

            if model_display_rule == "setup_sources":
                self.apply_setup_source_model_visibility(
                    face_context
                )
        except Exception:
            return False

        return True


def main():
    u"""创建正式 Face Rig Workflow Wizard。"""
    return FaceRigWizard()


__all__ = [
    "FaceRigWizard",
    "main",
]
