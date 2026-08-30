# coding=utf-8
u"""Face Rig 全局配置。"""

from ...core import name_utils


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
# Face 默认设置
# ============================================================

face_center_axis = "X"


# ============================================================
# 创建层级时使用的列表
# ============================================================

# 这里只保存名称，不在配置文件中创建 Maya 节点。
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
