# coding=utf-8
u"""Face Rig 静态配置。"""

from __future__ import print_function

import os

from ...core import naming


FACE_SIDE = "md"
FACE_PART = "face"

PACKAGE_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)
RESOURCES_ROOT = os.path.join(
    PACKAGE_ROOT,
    "resources"
)


# =============================================================================
# Face Hierarchy
# =============================================================================

MASTER_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "master"
)

MODEL_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "model"
)

GUIDE_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "guide"
)

CONTROL_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "ctrl"
)

JOINT_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "jnt"
)

RIG_NODES_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "rig_nodes"
)

POSITION_DRIVER_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "pos_driver"
)

TWEAK_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "tweak"
)

STRETCH_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "stretch"
)

DEFORM_GROUP_NAME = naming.create_name(
    "grp",
    FACE_SIDE,
    FACE_PART,
    "deform"
)

CONTROL_SET_NAME = naming.create_name(
    "set",
    FACE_SIDE,
    FACE_PART,
    "ctrl"
)

CONFIG_NODE_NAME = naming.create_name(
    "network",
    FACE_SIDE,
    FACE_PART,
    "config"
)


# =============================================================================
# Face Setup Schema
# =============================================================================

SETUP_NODE_ATTRIBUTES = [
    "face_head_model",
    "face_lf_eye_model",
    "face_rt_eye_model",
    "upper_teeth_model",
    "lower_teeth_model",
    "face_tongue_model",
    "face_gum_model",
]

SETUP_VALUE_ATTRIBUTES = {
    "mouth_joint_count": "long",
}


# =============================================================================
# Workflow Schema
# =============================================================================

LAST_STEP = 4
CURRENT_STEP_ATTRIBUTE = "face_current_step"

STEP_COMPLETED_ATTRIBUTES = {
    1: "step_01_completed",
    2: "step_02_completed",
    3: "step_03_completed",
    4: "step_04_completed",
}


# =============================================================================
# Face Guide
# =============================================================================

GUIDE_TEMPLATE_FILE_NAME = "face_guide.ma"
GUIDE_TEMPLATE_PATH = os.path.join(
    RESOURCES_ROOT,
    "face",
    GUIDE_TEMPLATE_FILE_NAME
)

GUIDE_MOVE_CONTROL_NAME = naming.create_name(
    "ctrl",
    FACE_SIDE,
    FACE_PART,
    "move"
)

GUIDE_VERSION = "1.0"

GUIDE_ROOT_ATTRIBUTE = "face_guide_root"
GUIDE_MOVE_CONTROL_ATTRIBUTE = "face_guide_move_ctrl"
GUIDE_VERSION_ATTRIBUTE = "face_guide_version"


# =============================================================================
# Controller Settings
# =============================================================================

CONTROLLER_GLOBAL_SCALE_ATTRIBUTE = naming.create_attribute_name(
    "ctrl",
    "md",
    "face",
    "global_scale"
)

CONTROLLER_COLOR_ATTRIBUTES = {
    "lf": naming.create_attribute_name(
        "ctrl",
        "lf",
        "face",
        "color"
    ),
    "rt": naming.create_attribute_name(
        "ctrl",
        "rt",
        "face",
        "color"
    ),
    "md": naming.create_attribute_name(
        "ctrl",
        "md",
        "face",
        "color"
    ),
}

CONTROLLER_SIZE_ATTRIBUTES = {}

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
    CONTROLLER_SIZE_ATTRIBUTES[module_name] = naming.create_attribute_name(
        "ctrl",
        "md",
        module_name,
        "size"
    )

CONTROLLER_DEFAULT_SETTINGS = {
    CONTROLLER_GLOBAL_SCALE_ATTRIBUTE: 1.0,
    CONTROLLER_COLOR_ATTRIBUTES["lf"]: 6,
    CONTROLLER_COLOR_ATTRIBUTES["rt"]: 13,
    CONTROLLER_COLOR_ATTRIBUTES["md"]: 17,
}

for module_name in CONTROLLER_SIZE_ATTRIBUTES:
    attribute_name = CONTROLLER_SIZE_ATTRIBUTES[module_name]
    CONTROLLER_DEFAULT_SETTINGS[attribute_name] = 1.0

CONTROLLER_SETTING_TYPES = {
    CONTROLLER_GLOBAL_SCALE_ATTRIBUTE: "double",
    CONTROLLER_COLOR_ATTRIBUTES["lf"]: "long",
    CONTROLLER_COLOR_ATTRIBUTES["rt"]: "long",
    CONTROLLER_COLOR_ATTRIBUTES["md"]: "long",
}

for module_name in CONTROLLER_SIZE_ATTRIBUTES:
    attribute_name = CONTROLLER_SIZE_ATTRIBUTES[module_name]
    CONTROLLER_SETTING_TYPES[attribute_name] = "double"


# =============================================================================
# Display
# =============================================================================

CENTER_AXIS = "X"

STEP_VISIBILITY_RULES = {
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
