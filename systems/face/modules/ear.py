# coding=utf-8
u"""
Ear Module
==========

耳朵 FK 绑定模块。

旧 Ear 使用 ChainFK + ear_bpjnt.ma；新版本直接读取当前 FaceGuide 的 Ear Guide，
按 Guide 顺序创建 Jnt Chain 和 FK Ctrl Chain。
"""

from __future__ import print_function

from ....core import joint_utils
from ....core import matrix_utils
from ....core import scene_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class EarModule(FaceModuleBase):
    u"""构建左右 Ear FK Jnt / Ctrl Chain。"""

    sides = ["lf", "rt"]

    def __init__(self):
        super(EarModule, self).__init__(
            side="md",
            part="ear",
            index=1
        )
        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_radius = 1.0
        self.ear_side_dict = {}

    def load_setup(self):
        u"""读取 Face Setup、全局控制器比例和左右颜色。"""
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )
        self.ensure_hierarchy()

        controller_settings = self.face_guide.load_controller_settings()
        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )
        self.controller_radius = float(self.controller_global_scale) * 0.5

        if self.controller_radius <= 0.0:
            raise ValueError(u"Ear Controller Radius 必须大于 0。")

        self.ear_side_dict = {}
        for side in self.sides:
            self.ear_side_dict[side] = {
                "controller_color": controller_settings.get(
                    config.face_controller_color_attr_names[side],
                    6 if side == "lf" else 13
                ),
                "guides": [],
                "jnts": [],
                "ctrl_dict_list": [],
                "matrix_nodes": [],
            }
        return True

    def load_guide(self):
        u"""读取左右 Ear Guide，并保持 FaceGuide 返回顺序。"""
        for side in self.sides:
            ear_guides = self.face_guide.get_part_guides(
                part="ear",
                side=side,
                required=True
            )
            self.ear_side_dict[side]["guides"] = list(ear_guides)
        return self.ear_side_dict

    def create_jnt(self):
        u"""按 Guide 顺序创建 Ear Joint Chain。"""
        for side in self.sides:
            ear_dict = self.ear_side_dict[side]
            ear_jnts = []
            jnt_parent = self.face_jnt_grp
            index = 0

            while index < len(ear_dict["guides"]):
                item_index = index + 1
                ear_jnt_name = self.create_name(
                    type="jnt",
                    side=side,
                    part="ear",
                    function="bind",
                    index=item_index
                )
                scene_utils.ensure_nodes_available(
                    ear_jnt_name,
                    label=u"Ear Joint"
                )
                ear_jnt = joint_utils.Joint.create_at_object(
                    obj=ear_dict["guides"][index],
                    name=ear_jnt_name,
                    parent=jnt_parent,
                    match_rotation=True,
                    radius=self.controller_radius * 0.25
                )
                ear_jnts.append(ear_jnt)
                jnt_parent = ear_jnt
                index += 1

            ear_dict["jnts"] = ear_jnts
        return self.ear_side_dict

    def create_ctrl(self):
        u"""按 Joint 顺序创建 Ear FK Controller Chain。"""
        for side in self.sides:
            ear_dict = self.ear_side_dict[side]
            ctrl_dict_list = []
            ctrl_parent = self.face_ctrl_grp
            index = 0

            while index < len(ear_dict["jnts"]):
                item_index = index + 1
                ear_ctrl_name = self.create_name(
                    type="ctrl",
                    side=side,
                    part="ear",
                    function="fk",
                    index=item_index
                )
                ear_ctrl_dict = ctrl_base.create_ctrl(
                    name=ear_ctrl_name,
                    shape="circle",
                    radius=self.controller_radius,
                    color=ear_dict["controller_color"],
                    axis="X+",
                    target_node=ear_dict["jnts"][index],
                    parent_node=ctrl_parent,
                    create_sub_ctrl=False,
                    add_to_set=True,
                    ctrl_set=config.face_ctrl_set
                )
                ctrl_dict_list.append(ear_ctrl_dict)
                ctrl_parent = ear_ctrl_dict["output_node"]
                index += 1

            ear_dict["ctrl_dict_list"] = ctrl_dict_list
        return self.ear_side_dict

    def create_connect(self):
        u"""Ear FK Ctrl Output 一一驱动对应 Joint。"""
        for side in self.sides:
            ear_dict = self.ear_side_dict[side]
            matrix_nodes = []
            index = 0

            while index < len(ear_dict["jnts"]):
                item_index = index + 1
                ear_matrix_name = self.create_name(
                    type="mult",
                    side=side,
                    part="ear",
                    function="parent",
                    index=item_index
                )
                ear_matrix_node = matrix_utils.create_parent_matrix_constraint(
                    driver=ear_dict["ctrl_dict_list"][index]["output_node"],
                    driven=ear_dict["jnts"][index],
                    maintain_offset=False,
                    name=ear_matrix_name
                )
                matrix_nodes.append(ear_matrix_node)
                index += 1

            ear_dict["matrix_nodes"] = matrix_nodes
        return self.ear_side_dict

    def create_deform(self):
        u"""Ear 不额外创建 Deformer；输出 Joint 直接作为 Skin Influence。"""
        return True

    def create_finalize(self):
        u"""验证 Ear Joint / Controller / Matrix 输出。"""
        for side in self.sides:
            ear_dict = self.ear_side_dict[side]

            for ear_jnt in ear_dict["jnts"]:
                scene_utils.validate_node(ear_jnt, label=u"Ear Joint")

            for ear_ctrl_dict in ear_dict["ctrl_dict_list"]:
                scene_utils.validate_node(
                    ear_ctrl_dict["ctrl_node"],
                    label=u"Ear Ctrl"
                )

            for ear_matrix_node in ear_dict["matrix_nodes"]:
                scene_utils.validate_node(
                    ear_matrix_node,
                    label=u"Ear Matrix"
                )

        self.module_dict["sides"] = self.ear_side_dict
        self.module_dict["built"] = True
        return True


def build_ear():
    u"""构建 Ear Module 并返回统一 Module Dict。"""
    ear_module = EarModule()
    ear_module_dict = ear_module.create_build()
    return ear_module_dict


__all__ = [
    "EarModule",
    "build_ear",
]
