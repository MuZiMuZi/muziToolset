# coding=utf-8
u"""
Nose Module
===========

鼻子绑定模块。

当前 Face Guide 的真实结构：

    muzzle
        -> nose
            -> nose_center
                -> nose_front
                -> nose_down
                -> lf / rt nose_side

因此 NoseModule 明确拆成“中轴 FK Chain + Center 下的局部分支”，不再把全部
md Guide 错误串成一条 Chain，也不再导入旧 nose_bpjnt.ma。
"""

from __future__ import print_function

from ....core import joint_utils
from ....core import matrix_utils
from ....core import scene_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class NoseModule(FaceModuleBase):
    u"""构建 Nose 中轴 FK Chain 与 Front / Down / Side 局部控制。"""

    center_parts = [
        "muzzle",
        "nose",
        "nose_center",
    ]

    local_parts = [
        ("md", "nose_front"),
        ("md", "nose_down"),
        ("lf", "nose_side"),
        ("rt", "nose_side"),
    ]

    def __init__(self):
        super(NoseModule, self).__init__(
            side="md",
            part="nose",
            index=1
        )

        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_size = 1.0
        self.controller_radius = 1.0
        self.controller_color_dict = {}

        self.center_guides = []
        self.local_guide_dict = {}
        self.center_jnts = []
        self.local_jnt_dict = {}
        self.center_ctrl_dict_list = []
        self.local_ctrl_dict = {}
        self.nose_matrix_nodes = []

    def load_setup(self):
        u"""读取 Nose Controller Settings，并准备当前 Build 缓存。"""
        # -------------------------------------------------------------------------
        # Step 01：确认 Face Setup 已完成，并确保公共层级存在
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )
        self.ensure_hierarchy()

        # -------------------------------------------------------------------------
        # Step 02：读取统一 Controller Size / Color
        # -------------------------------------------------------------------------
        controller_settings = self.face_guide.load_controller_settings()
        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )
        self.controller_size = controller_settings.get(
            config.face_controller_size_attr_names["nose"],
            1.0
        )
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(u"Nose Controller Radius 必须大于 0。")

        for side in ["md", "lf", "rt"]:
            self.controller_color_dict[side] = controller_settings.get(
                config.face_controller_color_attr_names[side],
                17 if side == "md" else (6 if side == "lf" else 13)
            )

        # -------------------------------------------------------------------------
        # Step 03：清空本次 Build 的运行时数据
        # -------------------------------------------------------------------------
        self.center_guides = []
        self.local_guide_dict = {}
        self.center_jnts = []
        self.local_jnt_dict = {}
        self.center_ctrl_dict_list = []
        self.local_ctrl_dict = {}
        self.nose_matrix_nodes = []
        return True

    def load_guide(self):
        u"""按模板语义读取 Nose 中轴和局部分支 Guide。"""
        # -------------------------------------------------------------------------
        # Step 01：按明确顺序读取 Muzzle -> Nose -> Nose Center 中轴定位
        # -------------------------------------------------------------------------
        for part in self.center_parts:
            guide_name = self.create_name(
                type="loc",
                side="md",
                part=part,
                function="guide",
                index=1
            )
            guide = self.face_guide.get_guide_node(
                guide_name,
                required=True
            )
            self.center_guides.append(
                guide
            )

        # -------------------------------------------------------------------------
        # Step 02：读取 Nose Center 下的 Front / Down / Left Side / Right Side
        # -------------------------------------------------------------------------
        for side, part in self.local_parts:
            guide_name = self.create_name(
                type="loc",
                side=side,
                part=part,
                function="guide",
                index=1
            )
            guide = self.face_guide.get_guide_node(
                guide_name,
                required=True
            )
            self.local_guide_dict[(side, part)] = guide

        return {
            "center": self.center_guides,
            "local": self.local_guide_dict,
        }

    def create_jnt(self):
        u"""创建 Nose 中轴 Joint Chain 和 Center 下的局部 Joint。"""
        # -------------------------------------------------------------------------
        # Step 01：按 Muzzle -> Nose -> Nose Center 顺序创建 FK Joint Chain
        # -------------------------------------------------------------------------
        jnt_parent = self.face_jnt_grp
        self.center_jnts = []
        index = 0

        while index < len(self.center_guides):
            part = self.center_parts[index]
            nose_jnt_name = self.create_name(
                type="jnt",
                side="md",
                part=part,
                function="bind",
                index=1
            )
            scene_utils.ensure_nodes_available(
                nose_jnt_name,
                label=u"Nose Center Joint"
            )
            nose_jnt = joint_utils.Joint.create_at_object(
                obj=self.center_guides[index],
                name=nose_jnt_name,
                parent=jnt_parent,
                match_rotation=True,
                radius=self.controller_radius * 0.2
            )
            self.center_jnts.append(
                nose_jnt
            )
            jnt_parent = nose_jnt
            index += 1

        # -------------------------------------------------------------------------
        # Step 02：Front / Down / Side Joint 都挂在 Nose Center Joint 下
        # -------------------------------------------------------------------------
        local_parent = self.center_jnts[-1]
        self.local_jnt_dict = {}

        for side, part in self.local_parts:
            nose_local_jnt_name = self.create_name(
                type="jnt",
                side=side,
                part=part,
                function="bind",
                index=1
            )
            scene_utils.ensure_nodes_available(
                nose_local_jnt_name,
                label=u"Nose Local Joint"
            )
            nose_local_jnt = joint_utils.Joint.create_at_object(
                obj=self.local_guide_dict[(side, part)],
                name=nose_local_jnt_name,
                parent=local_parent,
                match_rotation=True,
                radius=self.controller_radius * 0.16
            )
            self.local_jnt_dict[(side, part)] = nose_local_jnt

        return {
            "center": self.center_jnts,
            "local": self.local_jnt_dict,
        }

    def create_ctrl(self):
        u"""创建 Nose 中轴 FK Ctrl Chain 和局部 Ctrl。"""
        # -------------------------------------------------------------------------
        # Step 01：中轴 Ctrl 按 Muzzle -> Nose -> Nose Center 创建 FK 层级
        # -------------------------------------------------------------------------
        ctrl_parent = self.face_ctrl_grp
        self.center_ctrl_dict_list = []
        index = 0

        while index < len(self.center_guides):
            part = self.center_parts[index]
            nose_ctrl_name = self.create_name(
                type="ctrl",
                side="md",
                part=part,
                function="bind",
                index=1
            )
            nose_ctrl_dict = ctrl_base.create_ctrl(
                name=nose_ctrl_name,
                shape="cube",
                radius=self.controller_radius * 0.55,
                color=self.controller_color_dict["md"],
                axis="X+",
                target_node=self.center_guides[index],
                parent_node=ctrl_parent,
                create_sub_ctrl=False,
                add_to_set=True,
                ctrl_set=config.face_ctrl_set
            )
            self.center_ctrl_dict_list.append(
                nose_ctrl_dict
            )
            ctrl_parent = nose_ctrl_dict["output_node"]
            index += 1

        # -------------------------------------------------------------------------
        # Step 02：局部 Ctrl 都挂在 Nose Center Ctrl Output 下
        # -------------------------------------------------------------------------
        self.local_ctrl_dict = {}

        for side, part in self.local_parts:
            nose_local_ctrl_name = self.create_name(
                type="ctrl",
                side=side,
                part=part,
                function="bind",
                index=1
            )
            nose_local_ctrl_dict = ctrl_base.create_ctrl(
                name=nose_local_ctrl_name,
                shape="ball",
                radius=self.controller_radius * 0.38,
                color=self.controller_color_dict[side],
                axis="X+",
                target_node=self.local_guide_dict[(side, part)],
                parent_node=ctrl_parent,
                create_sub_ctrl=False,
                add_to_set=True,
                ctrl_set=config.face_ctrl_set
            )
            self.local_ctrl_dict[(side, part)] = nose_local_ctrl_dict

        return {
            "center": self.center_ctrl_dict_list,
            "local": self.local_ctrl_dict,
        }

    def create_connect(self):
        u"""使用所有 Nose Ctrl Output 一一驱动对应 Joint。"""
        self.nose_matrix_nodes = []

        # -------------------------------------------------------------------------
        # Step 01：建立中轴 Ctrl -> Joint Matrix 驱动
        # -------------------------------------------------------------------------
        index = 0
        while index < len(self.center_jnts):
            part = self.center_parts[index]
            nose_matrix_name = self.create_name(
                type="mult",
                side="md",
                part=part,
                function="parent",
                index=1
            )
            nose_matrix_node = matrix_utils.create_parent_matrix_constraint(
                driver=self.center_ctrl_dict_list[index]["output_node"],
                driven=self.center_jnts[index],
                maintain_offset=False,
                name=nose_matrix_name
            )
            self.nose_matrix_nodes.append(
                nose_matrix_node
            )
            index += 1

        # -------------------------------------------------------------------------
        # Step 02：建立 Front / Down / Side Ctrl -> Joint Matrix 驱动
        # -------------------------------------------------------------------------
        for side, part in self.local_parts:
            nose_matrix_name = self.create_name(
                type="mult",
                side=side,
                part=part,
                function="parent",
                index=1
            )
            nose_matrix_node = matrix_utils.create_parent_matrix_constraint(
                driver=self.local_ctrl_dict[(side, part)]["output_node"],
                driven=self.local_jnt_dict[(side, part)],
                maintain_offset=False,
                name=nose_matrix_name
            )
            self.nose_matrix_nodes.append(
                nose_matrix_node
            )

        return self.nose_matrix_nodes

    def create_deform(self):
        u"""Nose 输出 Joint 直接作为后续 Face Skin Influence。"""
        return True

    def create_finalize(self):
        u"""验证 Nose 中轴和局部分支的 Joint / Ctrl / Matrix。"""
        # -------------------------------------------------------------------------
        # Step 01：验证全部中轴 Joint / Controller
        # -------------------------------------------------------------------------
        for nose_jnt in self.center_jnts:
            scene_utils.validate_node(
                nose_jnt,
                label=u"Nose Center Joint"
            )

        for nose_ctrl_dict in self.center_ctrl_dict_list:
            scene_utils.validate_node(
                nose_ctrl_dict["ctrl_node"],
                label=u"Nose Center Ctrl"
            )

        # -------------------------------------------------------------------------
        # Step 02：验证全部局部 Joint / Controller
        # -------------------------------------------------------------------------
        for nose_local_jnt in self.local_jnt_dict.values():
            scene_utils.validate_node(
                nose_local_jnt,
                label=u"Nose Local Joint"
            )

        for nose_local_ctrl_dict in self.local_ctrl_dict.values():
            scene_utils.validate_node(
                nose_local_ctrl_dict["ctrl_node"],
                label=u"Nose Local Ctrl"
            )

        # -------------------------------------------------------------------------
        # Step 03：验证 Matrix 并整理公开输出
        # -------------------------------------------------------------------------
        for nose_matrix_node in self.nose_matrix_nodes:
            scene_utils.validate_node(
                nose_matrix_node,
                label=u"Nose Matrix"
            )

        self.module_dict["center_guides"] = self.center_guides
        self.module_dict["local_guides"] = self.local_guide_dict
        self.module_dict["center_jnts"] = self.center_jnts
        self.module_dict["local_jnts"] = self.local_jnt_dict
        self.module_dict["center_ctrl_dict_list"] = self.center_ctrl_dict_list
        self.module_dict["local_ctrl_dict"] = self.local_ctrl_dict
        self.module_dict["matrix_nodes"] = self.nose_matrix_nodes
        self.module_dict["built"] = True
        return True


def build_nose():
    u"""构建 Nose Module 并返回统一 Module Dict。"""
    nose_module = NoseModule()
    nose_module_dict = nose_module.create_build()
    return nose_module_dict


__all__ = [
    "NoseModule",
    "build_nose",
]
