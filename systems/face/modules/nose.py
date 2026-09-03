# coding=utf-8
u"""
Nose Module
===========

鼻子绑定模块。

旧 Nose 的“中轴 Chain + Side / Front / Bottom 局部控制”思想保留。
新版本从当前 Face Guide 中自动收集 part 以 ``nose`` 开头的 Locator，不再导入
nose_bpjnt.ma。
"""

from __future__ import print_function

from ....core import joint_utils
from ....core import matrix_utils
from ....core import rename_utils
from ....core import scene_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class NoseModule(FaceModuleBase):
    u"""构建 Nose 中轴 FK Chain 与左右局部控制。"""

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
        self.nose_guide_dict = {
            "md": [],
            "lf": [],
            "rt": [],
        }
        self.nose_jnt_dict = {
            "md": [],
            "lf": [],
            "rt": [],
        }
        self.nose_ctrl_dict = {
            "md": [],
            "lf": [],
            "rt": [],
        }
        self.nose_matrix_nodes = []
        self.controller_color_dict = {}

    def load_setup(self):
        u"""读取 Nose Controller Settings 和 Face 公共层级。"""
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )
        self.ensure_hierarchy()

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

        return True

    def load_guide(self):
        u"""从全部 Face Guide 中收集 part 以 nose 开头的定位。"""
        self.nose_guide_dict = {
            "md": [],
            "lf": [],
            "rt": [],
        }
        all_guides = self.face_guide.get_guide_locators()

        for guide in all_guides:
            guide_name_data = self.parse_name(
                rename_utils.get_short_name(guide)
            )
            if not guide_name_data["part"].startswith("nose"):
                continue

            guide_side = guide_name_data["side"]
            if guide_side not in self.nose_guide_dict:
                continue

            self.nose_guide_dict[guide_side].append(guide)

        for side in self.nose_guide_dict:
            self.nose_guide_dict[side].sort(
                key=rename_utils.get_short_name
            )

        total_count = 0
        for side in self.nose_guide_dict:
            total_count += len(self.nose_guide_dict[side])

        if total_count == 0:
            raise RuntimeError(u"Face Guide 中没有找到 Nose 定位。")

        return self.nose_guide_dict

    def create_jnt(self):
        u"""中轴 Nose Guide 创建 Chain，左右 Guide 创建中轴末端的独立 Joint。"""
        self.nose_jnt_dict = {
            "md": [],
            "lf": [],
            "rt": [],
        }

        center_parent = self.face_jnt_grp
        index = 0
        while index < len(self.nose_guide_dict["md"]):
            guide = self.nose_guide_dict["md"][index]
            guide_data = self.parse_name(
                rename_utils.get_short_name(guide)
            )
            nose_jnt_name = self.create_name(
                type="jnt",
                side="md",
                part=guide_data["part"],
                function="bind",
                index=guide_data["index"]
            )
            scene_utils.ensure_nodes_available(
                nose_jnt_name,
                label=u"Nose Joint"
            )
            nose_jnt = joint_utils.Joint.create_at_object(
                obj=guide,
                name=nose_jnt_name,
                parent=center_parent,
                match_rotation=True,
                radius=self.controller_radius * 0.2
            )
            self.nose_jnt_dict["md"].append(nose_jnt)
            center_parent = nose_jnt
            index += 1

        side_parent = center_parent
        if not self.nose_jnt_dict["md"]:
            side_parent = self.face_jnt_grp

        for side in ["lf", "rt"]:
            for guide in self.nose_guide_dict[side]:
                guide_data = self.parse_name(
                    rename_utils.get_short_name(guide)
                )
                nose_jnt_name = self.create_name(
                    type="jnt",
                    side=side,
                    part=guide_data["part"],
                    function="bind",
                    index=guide_data["index"]
                )
                scene_utils.ensure_nodes_available(
                    nose_jnt_name,
                    label=u"Nose Side Joint"
                )
                nose_jnt = joint_utils.Joint.create_at_object(
                    obj=guide,
                    name=nose_jnt_name,
                    parent=side_parent,
                    match_rotation=True,
                    radius=self.controller_radius * 0.16
                )
                self.nose_jnt_dict[side].append(nose_jnt)

        return self.nose_jnt_dict

    def create_ctrl(self):
        u"""中轴建立 FK Ctrl Chain，左右局部 Ctrl 挂在中轴末端输出。"""
        self.nose_ctrl_dict = {
            "md": [],
            "lf": [],
            "rt": [],
        }

        center_ctrl_parent = self.face_ctrl_grp
        index = 0
        while index < len(self.nose_guide_dict["md"]):
            guide = self.nose_guide_dict["md"][index]
            guide_data = self.parse_name(
                rename_utils.get_short_name(guide)
            )
            nose_ctrl_name = self.create_name(
                type="ctrl",
                side="md",
                part=guide_data["part"],
                function="bind",
                index=guide_data["index"]
            )
            nose_ctrl_dict = ctrl_base.create_ctrl(
                name=nose_ctrl_name,
                shape="cube",
                radius=self.controller_radius * 0.55,
                color=self.controller_color_dict["md"],
                axis="X+",
                target_node=guide,
                parent_node=center_ctrl_parent,
                create_sub_ctrl=False,
                add_to_set=True,
                ctrl_set=config.face_ctrl_set
            )
            self.nose_ctrl_dict["md"].append(nose_ctrl_dict)
            center_ctrl_parent = nose_ctrl_dict["output_node"]
            index += 1

        side_ctrl_parent = center_ctrl_parent
        if not self.nose_ctrl_dict["md"]:
            side_ctrl_parent = self.face_ctrl_grp

        for side in ["lf", "rt"]:
            for guide in self.nose_guide_dict[side]:
                guide_data = self.parse_name(
                    rename_utils.get_short_name(guide)
                )
                nose_ctrl_name = self.create_name(
                    type="ctrl",
                    side=side,
                    part=guide_data["part"],
                    function="bind",
                    index=guide_data["index"]
                )
                nose_ctrl_dict = ctrl_base.create_ctrl(
                    name=nose_ctrl_name,
                    shape="ball",
                    radius=self.controller_radius * 0.38,
                    color=self.controller_color_dict[side],
                    axis="X+",
                    target_node=guide,
                    parent_node=side_ctrl_parent,
                    create_sub_ctrl=False,
                    add_to_set=True,
                    ctrl_set=config.face_ctrl_set
                )
                self.nose_ctrl_dict[side].append(nose_ctrl_dict)

        return self.nose_ctrl_dict

    def create_connect(self):
        u"""全部 Nose Ctrl Output 一一驱动对应 Joint。"""
        self.nose_matrix_nodes = []

        for side in ["md", "lf", "rt"]:
            index = 0
            while index < len(self.nose_jnt_dict[side]):
                nose_jnt = self.nose_jnt_dict[side][index]
                nose_ctrl_dict = self.nose_ctrl_dict[side][index]
                jnt_name_data = self.parse_name(
                    rename_utils.get_short_name(nose_jnt)
                )
                nose_matrix_name = self.create_name(
                    type="mult",
                    side=side,
                    part=jnt_name_data["part"],
                    function="parent",
                    index=jnt_name_data["index"]
                )
                nose_matrix_node = matrix_utils.create_parent_matrix_constraint(
                    driver=nose_ctrl_dict["output_node"],
                    driven=nose_jnt,
                    maintain_offset=False,
                    name=nose_matrix_name
                )
                self.nose_matrix_nodes.append(nose_matrix_node)
                index += 1

        return self.nose_matrix_nodes

    def create_deform(self):
        u"""Nose 输出 Joint 直接作为后续 Face Skin Influence。"""
        return True

    def create_finalize(self):
        u"""验证 Nose Joint / Controller / Matrix。"""
        for side in ["md", "lf", "rt"]:
            for nose_jnt in self.nose_jnt_dict[side]:
                scene_utils.validate_node(nose_jnt, label=u"Nose Joint")

            for nose_ctrl_dict in self.nose_ctrl_dict[side]:
                scene_utils.validate_node(
                    nose_ctrl_dict["ctrl_node"],
                    label=u"Nose Ctrl"
                )

        for nose_matrix_node in self.nose_matrix_nodes:
            scene_utils.validate_node(
                nose_matrix_node,
                label=u"Nose Matrix"
            )

        self.module_dict["guides"] = self.nose_guide_dict
        self.module_dict["jnts"] = self.nose_jnt_dict
        self.module_dict["ctrls"] = self.nose_ctrl_dict
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
