# coding=utf-8
u"""Face Rig 全局配置。"""

from __future__ import print_function

import os

from ... import config as package_config
from ..rig_base import RigBase


# ============================================================
# 命名规范
# ============================================================
#
# Maya 节点：
#     [类型]_[方向]_[部位]_[功能]_[序号]
#
# part 可以包含下划线，function 必须是单一 Token。
#
# Config Attribute：
#     去掉 Maya 节点标准名称最后的序号。
#
# 例如：
#     grp_md_face_master_001
#     grp_md_face_rig_nodes_001
#     ctrl_lf_eye_main_001
#     ctrl_md_face_global_scale
#
# 方向统一：
#     lf = left
#     rt = right
#     md = middle / center
# ============================================================


face_side = "md"
face_part = "face"

# Face System 自己也是一个明确的 Rig Object。
# Config 中绝大多数固定名称直接继承这个 Identity。
face_rig = RigBase(
    side=face_side,
    part=face_part,
    index=1
)


def create_config_attr_name(
        type,
        side,
        part,
        function
):
    u"""使用统一 Rig Naming 创建不带序号的 Config Attribute 名称。"""
    rig_object = RigBase(
        side=side,
        part=part,
        index=1
    )
    node_name = rig_object.create_name(
        type=type,
        function=function
    )

    return node_name.rsplit(
        "_",
        1
    )[0]


# ============================================================
# Face Rig 层级名称
# ============================================================

face_master_grp = face_rig.create_name(
    type="grp",
    function="master"
)

face_guide_grp = face_rig.create_name(
    type="grp",
    function="guide"
)

face_ctrl_grp = face_rig.create_name(
    type="grp",
    function="ctrl"
)

face_jnt_grp = face_rig.create_name(
    type="grp",
    function="jnt"
)

face_rig_nodes_grp = face_rig.create_name(
    type="grp",
    part="face_rig",
    function="nodes"
)

face_pos_driver_grp = face_rig.create_name(
    type="grp",
    part="face_pos",
    function="driver"
)


# ============================================================
# Face 模型层级
# ============================================================

face_model_grp = face_rig.create_name(
    type="grp",
    function="model"
)

face_tweak_grp = face_rig.create_name(
    type="grp",
    function="tweak"
)

face_stretch_grp = face_rig.create_name(
    type="grp",
    function="stretch"
)

face_deform_grp = face_rig.create_name(
    type="grp",
    function="deform"
)


# ============================================================
# Set
# ============================================================

face_ctrl_set = face_rig.create_name(
    type="set",
    function="ctrl"
)


# ============================================================
# Face 配置 Network Node
# ============================================================

config_node = face_rig.create_name(
    type="network",
    function="config"
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

face_guide_move_ctrl = face_rig.create_name(
    type="ctrl",
    function="move"
)

face_guide_version = "1.0"


# ============================================================
# Face Controller Config Attribute
# ============================================================

face_controller_global_scale_attr = create_config_attr_name(
    type="ctrl",
    side="md",
    part="face_global",
    function="scale"
)

face_controller_color_attr_names = {
    "lf": create_config_attr_name(
        type="ctrl",
        side="lf",
        part="face",
        function="color"
    ),
    "rt": create_config_attr_name(
        type="ctrl",
        side="rt",
        part="face",
        function="color"
    ),
    "md": create_config_attr_name(
        type="ctrl",
        side="md",
        part="face",
        function="color"
    ),
}

face_controller_size_attr_names = {
    "brow": create_config_attr_name(
        type="ctrl",
        side="md",
        part="brow",
        function="size"
    ),
    "eye": create_config_attr_name(
        type="ctrl",
        side="md",
        part="eye",
        function="size"
    ),
    "eyelid": create_config_attr_name(
        type="ctrl",
        side="md",
        part="eyelid",
        function="size"
    ),
    "nose": create_config_attr_name(
        type="ctrl",
        side="md",
        part="nose",
        function="size"
    ),
    "cheek": create_config_attr_name(
        type="ctrl",
        side="md",
        part="cheek",
        function="size"
    ),
    "lip": create_config_attr_name(
        type="ctrl",
        side="md",
        part="lip",
        function="size"
    ),
    "jaw": create_config_attr_name(
        type="ctrl",
        side="md",
        part="jaw",
        function="size"
    ),
    "teeth": create_config_attr_name(
        type="ctrl",
        side="md",
        part="teeth",
        function="size"
    ),
    "tongue": create_config_attr_name(
        type="ctrl",
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
