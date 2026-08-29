# coding=utf-8
u"""Face Rig 全局配置。"""

from ..core import nameUtils


# ============================================================
# 命名规范
# ============================================================
#
# 标准：
#     [类型]_[方向]_[部位]_[功能]_[序号]
#
# 例如：
#     grp_md_face_master_001
#     ctrl_lf_eye_main_001
#     jnt_rt_brow_bind_001
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


# ============================================================
# Face Rig 层级名称
# ============================================================

# Face 总组
face_master_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="master",
    index=1
)

# Guide 组
face_guide_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="guide",
    index=1
)

# Controller 组
face_ctrl_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="ctrl",
    index=1
)

# Joint 组
face_jnt_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="jnt",
    index=1
)

# Rig Nodes 组
face_rig_nodes_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="rig_nodes",
    index=1
)

# Pose Driver 组
face_pos_driver_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="pos_driver",
    index=1
)


# ============================================================
# Face 模型层级
# ============================================================

# 模型总组
face_model_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="model",
    index=1
)

# Tweak 模型组
face_tweak_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="tweak",
    index=1
)

# Stretch 模型组
face_stretch_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="stretch",
    index=1
)

# Deform 模型组
face_deform_grp = nameUtils.Name.create_name(
    node_type="grp",
    side=face_side,
    part=face_part,
    function="deform",
    index=1
)


# ============================================================
# Set
# ============================================================

face_ctrl_set = nameUtils.Name.create_name(
    node_type="set",
    side=face_side,
    part=face_part,
    function="ctrl",
    index=1
)


# ============================================================
# Face 配置 Network Node
# ============================================================

config_node = nameUtils.Name.create_name(
    node_type="network",
    side=face_side,
    part=face_part,
    function="config",
    index=1
)


# ============================================================
# Face 默认设置
# ============================================================

# 脸部默认镜像轴向
face_center_axis = "X"


# ============================================================
# 创建层级时使用的列表
# ============================================================

# Face Rig 类型组
# 这里只保存名称，不在这里创建节点。
type_grp_list = [
    face_guide_grp,
    face_ctrl_grp,
    face_jnt_grp,
    face_rig_nodes_grp,
    face_pos_driver_grp
]

# Face 模型层级组
model_grp_list = [
    face_tweak_grp,
    face_stretch_grp,
    face_deform_grp
]


# ============================================================
# 旧变量名兼容
# ============================================================
# 后续代码全部建议使用上面的 snake_case 新变量名。

face_rigNodes_grp = face_rig_nodes_grp
face_posDriver_grp = face_pos_driver_grp
face_tweaks_grp = face_tweak_grp
