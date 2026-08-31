# coding=utf-8
u"""
Face Rig Workflow Controller
============================

FaceRigView 与 PyMEL Face System 之间的业务控制层。
"""

from __future__ import print_function

import maya.OpenMayaUI as omui
import pymel.core as pm

try:
    from PySide2.QtWidgets import QMessageBox
    from PySide2.QtWidgets import QWidget
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtWidgets import QWidget
    from shiboken6 import wrapInstance

from .. import config
from ..build import FaceBuild
from ..face_base import FaceBase
from ..face_config import FaceConfig
from ..finalize import FaceFinalize
from ..guide import FaceGuide
from ..setup import FaceSetup
from .face_rig_ui import FaceRigView


def maya_main_window():
    main_window_pointer = omui.MQtUtil.mainWindow()
    if main_window_pointer is None:
        return None
    return wrapInstance(int(main_window_pointer), QWidget)


class FaceRigWindow(FaceRigView):
    u"""Face Rig 正式 Workflow Window。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = maya_main_window()
        super(FaceRigWindow, self).__init__(parent)
        self.mirror_snapshot = None
        self.connect_signals()
        self.load_scene_data()

    def connect_signals(self):
        for picker_key in self.node_pickers:
            picker = self.node_pickers[picker_key]
            picker.pick_button.clicked.connect(
                self.create_picker_callback(picker_key)
            )
        self.reload_button.clicked.connect(self.load_scene_data)
        self.run_setup_button.clicked.connect(self.run_setup)
        self.build_guide_button.clicked.connect(self.build_guide)
        self.reimport_guide_button.clicked.connect(self.reimport_guide)
        self.mirror_left_to_right_button.clicked.connect(self.mirror_left_to_right)
        self.mirror_right_to_left_button.clicked.connect(self.mirror_right_to_left)
        self.undo_mirror_button.clicked.connect(self.undo_last_mirror)
        self.validate_guide_button.clicked.connect(self.validate_guide)
        self.save_controller_settings_button.clicked.connect(
            self.save_controller_settings
        )
        self.complete_guide_button.clicked.connect(self.complete_guide)
        self.run_build_button.clicked.connect(self.run_build)
        self.finalize_button.clicked.connect(self.finalize_face)
        self.tabs.currentChanged.connect(self.on_step_changed)

    def create_picker_callback(self, picker_key):
        def callback():
            self.pick_selected_node(picker_key)
        return callback

    def show_error(self, title, error):
        QMessageBox.critical(self, title, str(error))
        self.set_status(u"Error: {}".format(error))

    @staticmethod
    def node_display_name(node):
        if node is None:
            return None
        try:
            return node.longName()
        except Exception:
            return str(node)

    def pick_selected_node(self, picker_key):
        selection = pm.selected()
        if not selection:
            self.set_status(u"请选择一个 Maya 节点。")
            return False

        node = selection[0]
        if node.nodeType() not in ["transform", "joint"]:
            parent = node.getParent()
            if parent is not None:
                node = parent

        self.node_pickers[picker_key].set_value(self.node_display_name(node))
        self.set_status(u"Picked: {}".format(node))
        return True

    def load_default_controller_settings(self):
        self.controller_global_scale_spin.setValue(
            float(config.controller_default_settings[
                config.controller_global_scale_attribute
            ])
        )
        for side in config.controller_color_attributes:
            attribute_name = config.controller_color_attributes[side]
            self.controller_color_widgets[side].setValue(
                int(config.controller_default_settings[attribute_name])
            )
        for module_name in config.controller_size_attributes:
            attribute_name = config.controller_size_attributes[module_name]
            self.controller_size_widgets[module_name].setValue(
                float(config.controller_default_settings[attribute_name])
            )

    def apply_controller_settings(self, settings):
        global_scale = settings.get(config.controller_global_scale_attribute)
        if global_scale is not None:
            self.controller_global_scale_spin.setValue(float(global_scale))
        for side in config.controller_color_attributes:
            attribute_name = config.controller_color_attributes[side]
            value = settings.get(attribute_name)
            if value is not None:
                self.controller_color_widgets[side].setValue(int(value))
        for module_name in config.controller_size_attributes:
            attribute_name = config.controller_size_attributes[module_name]
            value = settings.get(attribute_name)
            if value is not None:
                self.controller_size_widgets[module_name].setValue(float(value))

    def update_step_labels(self, step_status):
        labels = [
            u"Step 01  Setup",
            u"Step 02  Guide",
            u"Step 03  Build",
            u"Step 04  Finalize",
        ]
        index = 0
        while index < len(labels):
            step_value = index + 1
            label = labels[index]
            if step_status.get(step_value, False):
                label += u"  ✓"
            self.tabs.setTabText(index, label)
            index += 1

    def load_scene_data(self):
        face_config = FaceConfig()
        self.load_default_controller_settings()

        if not face_config.exists():
            self.set_status(u"Face Config 尚未创建。")
            self.update_step_labels({})
            return False

        setup_data = face_config.load_setup()
        picker_map = {
            "head_model": "face_head_model",
            "left_eye_model": "face_lf_eye_model",
            "right_eye_model": "face_rt_eye_model",
            "upper_teeth_model": "upper_teeth_model",
            "lower_teeth_model": "lower_teeth_model",
            "tongue_model": "face_tongue_model",
            "gum_model": "face_gum_model",
        }
        for picker_key in picker_map:
            node = setup_data.get(picker_map[picker_key])
            picker = self.node_pickers[picker_key]
            if node is None:
                picker.clear()
            else:
                picker.set_value(self.node_display_name(node))

        mouth_joint_count = setup_data.get("mouth_joint_count")
        if mouth_joint_count is not None:
            self.mouth_joint_count_spin.setValue(int(mouth_joint_count))

        self.apply_controller_settings(face_config.load_controller_settings())
        self.update_step_labels(face_config.get_step_status())
        tab_index = face_config.get_current_step() - 1
        if tab_index < 0 or tab_index >= self.tabs.count():
            tab_index = 0
        self.tabs.blockSignals(True)
        self.tabs.setCurrentIndex(tab_index)
        self.tabs.blockSignals(False)
        self.set_status(u"Scene Config Reloaded")
        return True

    def run_setup(self):
        try:
            setup = FaceSetup(
                head_model=self.node_pickers["head_model"].value(),
                left_eye_model=self.node_pickers["left_eye_model"].value(),
                right_eye_model=self.node_pickers["right_eye_model"].value(),
                upper_teeth_model=self.node_pickers["upper_teeth_model"].value(),
                lower_teeth_model=self.node_pickers["lower_teeth_model"].value(),
                tongue_model=self.node_pickers["tongue_model"].value(),
                gum_model=self.node_pickers["gum_model"].value(),
                mouth_joint_count=self.mouth_joint_count_spin.value()
            )
            setup.run_step()
        except Exception as error:
            self.show_error(u"Face Setup", error)
            return False
        self.load_scene_data()
        self.set_status(u"Face Setup Completed")
        return True

    def build_guide(self):
        try:
            FaceGuide().build_guide()
        except Exception as error:
            self.show_error(u"Build Face Guide", error)
            return False
        self.set_status(u"Face Guide Built")
        return True

    def reimport_guide(self):
        try:
            result = FaceGuide().reimport_guide()
        except Exception as error:
            self.show_error(u"Reimport Face Guide", error)
            return False
        self.set_status(
            u"Guide Reimported, Restored: {}".format(result["restored_count"])
        )
        return True

    def mirror_left_to_right(self):
        return self.mirror_guides("lf", "rt")

    def mirror_right_to_left(self):
        return self.mirror_guides("rt", "lf")

    def mirror_guides(self, source_side, target_side):
        try:
            result = FaceGuide().mirror_guides(source_side, target_side)
            self.mirror_snapshot = result["snapshot"]
        except Exception as error:
            self.show_error(u"Mirror Face Guide", error)
            return False
        self.set_status(
            u"Mirrored {} → {}, Count: {}".format(
                source_side,
                target_side,
                result["count"]
            )
        )
        return True

    def undo_last_mirror(self):
        if self.mirror_snapshot is None:
            self.set_status(u"没有可恢复的 Mirror Snapshot。")
            return False
        try:
            result = FaceGuide().undo_mirror(self.mirror_snapshot)
        except Exception as error:
            self.show_error(u"Undo Face Guide Mirror", error)
            return False
        self.mirror_snapshot = None
        self.set_status(
            u"Mirror Restored, Count: {}".format(result["restored_count"])
        )
        return True

    def validate_guide(self):
        try:
            result = FaceGuide().validate_guides()
        except Exception as error:
            self.show_error(u"Validate Face Guide", error)
            return False

        if result["valid"]:
            QMessageBox.information(
                self,
                u"Face Guide",
                u"Guide Validation Passed.\nGuide Count: {}".format(
                    result["guide_count"]
                )
            )
            self.set_status(u"Guide Validation Passed")
            return True

        message = u"Guide Validation Failed"
        for error in result["errors"]:
            message += u"\n- {}".format(error)
        self.show_error(u"Face Guide", message)
        return False

    def collect_controller_settings(self):
        settings = {
            config.controller_global_scale_attribute:
                self.controller_global_scale_spin.value()
        }
        for side in config.controller_color_attributes:
            attribute_name = config.controller_color_attributes[side]
            settings[attribute_name] = self.controller_color_widgets[side].value()
        for module_name in config.controller_size_attributes:
            attribute_name = config.controller_size_attributes[module_name]
            settings[attribute_name] = self.controller_size_widgets[module_name].value()
        return settings

    def save_controller_settings(self):
        try:
            FaceGuide().save_controller_settings(self.collect_controller_settings())
        except Exception as error:
            self.show_error(u"Controller Settings", error)
            return False
        self.set_status(u"Controller Settings Saved")
        return True

    def complete_guide(self):
        try:
            guide = FaceGuide()
            guide.save_controller_settings(self.collect_controller_settings())
            guide.run_step()
        except Exception as error:
            self.show_error(u"Complete Face Guide", error)
            return False
        self.load_scene_data()
        self.set_status(u"Face Guide Completed")
        return True

    def run_build(self):
        try:
            FaceBuild().run_step()
        except Exception as error:
            self.show_error(u"Build Face Rig", error)
            return False
        self.load_scene_data()
        self.set_status(u"Face Build Completed")
        return True

    def finalize_face(self):
        try:
            FaceFinalize().run_step()
        except Exception as error:
            self.show_error(u"Finalize Face Rig", error)
            return False
        self.load_scene_data()
        self.set_status(u"Face Rig Finalized")
        return True

    def on_step_changed(self, tab_index):
        face_config = FaceConfig()
        if not face_config.exists():
            return False
        try:
            FaceBase().apply_step_visibility(tab_index + 1)
        except Exception as error:
            self.set_status(u"Visibility Error: {}".format(error))
            return False
        return True


__all__ = [
    "FaceRigWindow",
    "maya_main_window",
]
