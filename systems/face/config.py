# coding=utf-8
u"""Face Rig 静态配置。"""

from __future__ import print_function

import os

from ...core import name


face_side = "md"
face_part = "face"

package_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)
resources_root = os.path.join(
    package_root,
    "resources"
)


# =============================================================================
# Face Hierarchy
# =============================================================================

master_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "master"
)

model_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "model"
)

guide_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "guide"
)

control_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "ctrl"
)

joint_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "jnt"
)

rig_nodes_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "rig_nodes"
)

position_driver_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "pos_driver"
)

tweak_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "tweak"
)

stretch_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "stretch"
)

deform_group_name = name.create_name(
    "grp",
    face_side,
    face_part,
    "deform"
)

control_set_name = name.create_name(
    "set",
    face_side,
    face_part,
    "ctrl"
)

config_node_name = name.create_name(
    "network",
    face_side,
    face_part,
    "config"
)


# =============================================================================
# Face Setup Schema
# =============================================================================

setup_source_node_attributes = [
    "head_model",
    "left_eye_model",
    "right_eye_model",
    "upper_teeth_model",
    "lower_teeth_model",
    "tongue_model",
    "gum_model",
]

setup_work_node_attributes = [
    "head_tweak_model",
    "head_stretch_model",
    "head_deform_model",
]

setup_node_attributes = []

for attribute_name in setup_source_node_attributes:
    setup_node_attributes.append(
        attribute_name
    )

for attribute_name in setup_work_node_attributes:
    setup_node_attributes.append(
        attribute_name
    )

setup_value_attributes = {
    "mouth_joint_count": "long",
}


# =============================================================================
# Workflow Schema
# =============================================================================

last_step = 4
current_step_attribute = "face_current_step"

step_completed_attributes = {
    1: "step_01_completed",
    2: "step_02_completed",
    3: "step_03_completed",
    4: "step_04_completed",
}


# =============================================================================
# Face Guide
# =============================================================================

guide_template_file_name = "face_guide.ma"
guide_template_path = os.path.join(
    resources_root,
    "face",
    guide_template_file_name
)

guide_move_control_name = name.create_name(
    "ctrl",
    face_side,
    face_part,
    "move"
)

guide_version = "1.0"

guide_root_attribute = "face_guide_root"
guide_move_control_attribute = "face_guide_move_ctrl"
guide_version_attribute = "face_guide_version"


# =============================================================================
# Controller Settings
# =============================================================================

controller_global_scale_attribute = name.create_attribute_name(
    "ctrl",
    "md",
    "face",
    "global_scale"
)

controller_color_attributes = {
    "lf": name.create_attribute_name(
        "ctrl",
        "lf",
        "face",
        "color"
    ),
    "rt": name.create_attribute_name(
        "ctrl",
        "rt",
        "face",
        "color"
    ),
    "md": name.create_attribute_name(
        "ctrl",
        "md",
        "face",
        "color"
    ),
}

controller_size_attributes = {}

for module_name in [
        "brow",
        "eye",
        "eyelid",
        "nose",
        "cheek",
        "lip",
        "jaw",
        "teeth",
        "tongue",
]:
    controller_size_attributes[module_name] = name.create_attribute_name(
        "ctrl",
        "md",
        module_name,
        "size"
    )

controller_default_settings = {
    controller_global_scale_attribute: 1.0,
    controller_color_attributes["lf"]: 6,
    controller_color_attributes["rt"]: 13,
    controller_color_attributes["md"]: 17,
}

for module_name in controller_size_attributes:
    attribute_name = controller_size_attributes[module_name]
    controller_default_settings[attribute_name] = 1.0

controller_setting_types = {
    controller_global_scale_attribute: "double",
    controller_color_attributes["lf"]: "long",
    controller_color_attributes["rt"]: "long",
    controller_color_attributes["md"]: "long",
}

for module_name in controller_size_attributes:
    attribute_name = controller_size_attributes[module_name]
    controller_setting_types[attribute_name] = "double"


# =============================================================================
# Display
# =============================================================================

center_axis = "X"

step_visibility_rules = {
    1: {
        "model": True,
        "guide": False,
        "control": False,
        "joint": False,
        "rig_nodes": False,
        "position_driver": False,
    },
    2: {
        "model": True,
        "guide": True,
        "control": False,
        "joint": False,
        "rig_nodes": False,
        "position_driver": False,
    },
    3: {
        "model": True,
        "guide": False,
        "control": True,
        "joint": True,
        "rig_nodes": False,
        "position_driver": False,
    },
    4: {
        "model": True,
        "guide": False,
        "control": True,
        "joint": False,
        "rig_nodes": False,
        "position_driver": False,
    },
}
