# coding=utf-8
u"""Face Rig 全局配置。"""

from __future__ import print_function

import os

from ... import config as package_config
from ...core import name_utils


# ============================================================
# 命名规范
# ============================================================
#
# Maya 节点：
#     [类型]_[方向]_[部位]_[功能]_[序号]
#
# Config Attribute：
#     [类型]_[方向]_[部位]_[功能]
#
# 例如：
#     grp_md_face_master_001
#     ctrl_lf_eye_main_001
#     ctrl_md_face_color
#     ctrl_md_brow_size
#
# 方向统一：
#     lf = left
#     rt = right
#     md = middle / center
# ============================================================


# ------------------------------------------------------------
# Face 基础命名字段
# ------------------------------------------------------------

face_side = "md"
face_part = "face"


def create_config_attr_name(
        node_type,
        side,
        part,
        function
):
    u"""使用正式命名规范创建不带序号的 Config Attribute 名称。"""
    node_name = name_utils.Name.create_name(
        node_type=node_type,
        side=side,
        part=part,
        function=function,
        index=1
    )

    return node_name.rsplit(
        "_",
        1
    )[0]


# ============================================================
# Face Rig 层级名称
# ============================================================

face_master_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="master",
    index=1
)

face_guide_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="guide",
    index=1
)

face_ctrl_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="ctrl",
    index=1
)

face_jnt_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="jnt",
    index=1
)

face_rig_nodes_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="rig_nodes",
    index=1
)

face_pos_driver_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="pos_driver",
    index=1
)


# ============================================================
# Face 模型层级
# ============================================================

face_model_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="model",
    index=1
)

face_tweak_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="tweak",
    index=1
)

face_stretch_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="stretch",
    index=1
)

face_deform_grp = name_utils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="deform",
    index=1
)


# ============================================================
# Set
# ============================================================

face_ctrl_set = name_utils.Name.create_name(
    node_type="set",
    side=face_side,
    part=face_part,
    function="ctrl",
    index=1
)


# ============================================================
# Face 配置 Network Node
# ============================================================

config_node = name_utils.Name.create_name(
    node_type="network",
    side=face_side,
    part=face_part,
    function="config",
    index=1
)


# ============================================================
# Face Guide
# ============================================================

face_guide_template_file_name = "face_guide.ma"
face_guide_template_path = os.path.join(
    package_config.resources_dir,
    "face",
    face_guide_template_file_name
)

face_guide_move_ctrl = name_utils.Name.create_name(
    node_type="ctrl",
    side=face_side,
    part=face_part,
    function="move",
    index=1
)

face_guide_version = "1.0"


# ============================================================
# Face Controller Config Attribute
# ============================================================

face_controller_global_scale_attr = create_config_attr_name(
    node_type="ctrl",
    side="md",
    part="face",
    function="global_scale"
)

face_controller_color_attr_names = {
    "lf": create_config_attr_name(
        node_type="ctrl",
        side="lf",
        part="face",
        function="color"
    ),
    "rt": create_config_attr_name(
        node_type="ctrl",
        side="rt",
        part="face",
        function="color"
    ),
    "md": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="face",
        function="color"
    ),
}

face_controller_size_attr_names = {
    "brow": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="brow",
        function="size"
    ),
    "eye": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="eye",
        function="size"
    ),
    "eyelid": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="eyelid",
        function="size"
    ),
    "nose": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="nose",
        function="size"
    ),
    "cheek": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="cheek",
        function="size"
    ),
    "lip": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="lip",
        function="size"
    ),
    "jaw": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="jaw",
        function="size"
    ),
    "teeth": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="teeth",
        function="size"
    ),
    "tongue": create_config_attr_name(
        node_type="ctrl",
        side="md",
        part="tongue",
        function="size"
    ),
}


# ============================================================
# Face Controller 默认设置
# ============================================================

face_controller_default_settings = {
    face_controller_global_scale_attr: 1.0,
    face_controller_color_attr_names["lf"]: 6,
    face_controller_color_attr_names["rt"]: 13,
    face_controller_color_attr_names["md"]: 17,
    face_controller_size_attr_names["brow"]: 1.0,
    face_controller_size_attr_names["eye"]: 1.0,
    face_controller_size_attr_names["eyelid"]: 1.0,
    face_controller_size_attr_names["nose"]: 1.0,
    face_controller_size_attr_names["cheek"]: 1.0,
    face_controller_size_attr_names["lip"]: 1.0,
    face_controller_size_attr_names["jaw"]: 1.0,
    face_controller_size_attr_names["teeth"]: 1.0,
    face_controller_size_attr_names["tongue"]: 1.0,
}

face_controller_setting_attr_types = {
    face_controller_global_scale_attr: "double",
    face_controller_color_attr_names["lf"]: "long",
    face_controller_color_attr_names["rt"]: "long",
    face_controller_color_attr_names["md"]: "long",
    face_controller_size_attr_names["brow"]: "double",
    face_controller_size_attr_names["eye"]: "double",
    face_controller_size_attr_names["eyelid"]: "double",
    face_controller_size_attr_names["nose"]: "double",
    face_controller_size_attr_names["cheek"]: "double",
    face_controller_size_attr_names["lip"]: "double",
    face_controller_size_attr_names["jaw"]: "double",
    face_controller_size_attr_names["teeth"]: "double",
    face_controller_size_attr_names["tongue"]: "double",
}

face_controller_module_order = [
    "brow",
    "eye",
    "eyelid",
    "nose",
    "cheek",
    "lip",
    "jaw",
    "teeth",
    "tongue",
]

face_step_02_config_attr_names = [
    "face_guide_root",
    "face_guide_move_ctrl",
    "face_guide_version",
    face_controller_global_scale_attr,
    face_controller_color_attr_names["lf"],
    face_controller_color_attr_names["rt"],
    face_controller_color_attr_names["md"],
    face_controller_size_attr_names["brow"],
    face_controller_size_attr_names["eye"],
    face_controller_size_attr_names["eyelid"],
    face_controller_size_attr_names["nose"],
    face_controller_size_attr_names["cheek"],
    face_controller_size_attr_names["lip"],
    face_controller_size_attr_names["jaw"],
    face_controller_size_attr_names["teeth"],
    face_controller_size_attr_names["tongue"],
    "step_02_completed",
]


# ============================================================
# Face Workflow 显示规则
# ============================================================

face_step_visibility_rules = {
    1: {
        "face_model_grp": True,
        "face_guide_grp": False,
        "face_ctrl_grp": False,
        "face_jnt_grp": False,
        "face_rig_nodes_grp": False,
        "face_pos_driver_grp": False,
    },
    2: {
        "face_model_grp": True,
        "face_guide_grp": True,
        "face_ctrl_grp": False,
        "face_jnt_grp": False,
        "face_rig_nodes_grp": False,
        "face_pos_driver_grp": False,
    },
    3: {
        "face_model_grp": True,
        "face_guide_grp": False,
        "face_ctrl_grp": True,
        "face_jnt_grp": True,
        "face_rig_nodes_grp": False,
        "face_pos_driver_grp": False,
    },
    4: {
        "face_model_grp": True,
        "face_guide_grp": False,
        "face_ctrl_grp": True,
        "face_jnt_grp": False,
        "face_rig_nodes_grp": False,
        "face_pos_driver_grp": False,
    },
}

face_step_model_display_rules = {
    1: "setup_sources",
    2: "setup_sources",
    3: "preserve",
    4: "preserve",
}


# ============================================================
# Face 默认设置
# ============================================================

face_center_axis = "X"


# ============================================================
# 创建层级时使用的列表
# ============================================================

type_grp_list = [
    face_guide_grp,
    face_ctrl_grp,
    face_jnt_grp,
    face_rig_nodes_grp,
    face_pos_driver_grp,
]

model_grp_list = [
    face_tweak_grp,
    face_stretch_grp,
    face_deform_grp,
]
