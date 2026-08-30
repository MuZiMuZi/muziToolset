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
# Face Guide Locator 颜色
# ============================================================
#
# 规则：
#     1. 同一个面部部位的 lf / rt / md Guide 使用同一种颜色；
#     2. 不同部位使用不同颜色，方便在 Viewport 和 Outliner 中快速识别；
#     3. 颜色值使用 Maya RGB Override 的 0.0 ~ 1.0 范围；
#     4. 匹配时按照列表从上到下执行，所以更具体的名称放在前面。
#
# Locator 名称示例：
#     loc_lf_eye_ball_guide_001
#     loc_lf_eye_iris_guide_001
#     loc_lf_upper_lid_guide_001
#     loc_lf_upper_eye_bag_guide_001
# ============================================================

guide_locator_color_rules = [
    ("eye_bag", (0.95, 0.18, 0.68)),       # 洋红：眼袋
    ("eye_iris", (0.00, 0.95, 0.72)),      # 青绿：虹膜
    ("eye_ball", (0.00, 0.72, 1.00)),      # 天蓝：眼球
    ("_lid_", (0.52, 0.30, 1.00)),         # 紫色：眼皮
    ("_jaw_", (1.00, 0.42, 0.05)),         # 橙色：下颌
    ("_brow_", (1.00, 0.76, 0.05)),        # 金黄：眉毛
    ("_teeth_", (0.95, 0.95, 0.70)),       # 象牙：牙齿
    ("mouth_corner", (1.00, 0.08, 0.18)),  # 红色：嘴角，归属嘴唇
    ("_lip_", (1.00, 0.08, 0.18)),         # 红色：嘴唇
    ("_tongue_", (1.00, 0.32, 0.52)),      # 玫红：舌头
    ("_zygoma_", (0.00, 0.90, 0.62)),      # 薄荷绿：颧骨
    ("_nose_", (0.30, 0.92, 0.12)),        # 黄绿：鼻子
    ("_muzzle_", (0.30, 0.92, 0.12)),      # 黄绿：口鼻区，归属鼻子
    ("_ear_", (0.18, 0.42, 1.00)),         # 蓝色：耳朵
]


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
