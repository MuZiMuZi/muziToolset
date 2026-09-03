# coding=utf-8
u"""
Eye Module
==========

眼球绑定模块。

保留旧 Eye 的三个核心功能：
    1. Eye Main Ctrl；
    2. Eye Aim Ctrl；
    3. Iris Scale。

Eyelid / Blink 已拆为独立 EyelidModule，不再由 EyeModule 内部创建。
"""

from __future__ import print_function

import math

from ....core import attr_utils
from ....core import connection_utils
from ....core import constraint_utils
from ....core import joint_utils
from ....core import matrix_utils
from ....core import scene_utils
from ....core import transform_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class EyeModule(FaceModuleBase):
    u"""构建左右 Eye Main / Aim / Iris Rig。"""

    sides = ["lf", "rt"]

    def __init__(self):
        super(EyeModule, self).__init__(
            side="md",
            part="eye",
            index=1
        )
        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_size = 1.0
        self.controller_radius = 1.0
        self.eye_side_dict = {}

    def load_setup(self):
        u"""读取 Face Setup 与 Eye Controller Settings。"""
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
            config.face_controller_size_attr_names["eye"],
            1.0
        )
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(u"Eye Controller Radius 必须大于 0。")

        self.eye_side_dict = {}
        for side in self.sides:
            self.eye_side_dict[side] = {
                "controller_color": controller_settings.get(
                    config.face_controller_color_attr_names[side],
                    6 if side == "lf" else 13
                ),
                "eye_ball_guide": None,
                "eye_iris_guide": None,
                "eye_jnt": None,
                "iris_jnt": None,
                "eye_ctrl_dict": None,
                "aim_ctrl_dict": None,
                "eye_matrix": None,
                "aim_constraint": None,
                "iris_scale_plug": None,
            }
        return True

    def load_guide(self):
        u"""读取左右 Eye Ball / Iris Guide。"""
        for side in self.sides:
            eye_guide_dict = self.face_guide.get_eye_guides(
                side=side,
                required=True
            )
            self.eye_side_dict[side]["eye_ball_guide"] = eye_guide_dict["eye_ball"]
            self.eye_side_dict[side]["eye_iris_guide"] = eye_guide_dict["eye_iris"]
        return self.eye_side_dict

    def create_jnt(self):
        u"""创建 Eye Center Joint 和 Iris Joint。"""
        for side in self.sides:
            eye_dict = self.eye_side_dict[side]
            eye_jnt_name = self.create_name(
                type="jnt",
                side=side,
                part="eye",
                function="bind",
                index=1
            )
            iris_jnt_name = self.create_name(
                type="jnt",
                side=side,
                part="eye_iris",
                function="bind",
                index=1
            )

            scene_utils.ensure_nodes_available(
                [eye_jnt_name, iris_jnt_name],
                label=u"Eye Joint"
            )

            eye_jnt = joint_utils.Joint.create_at_object(
                obj=eye_dict["eye_ball_guide"],
                name=eye_jnt_name,
                parent=self.face_jnt_grp,
                match_rotation=True,
                radius=self.controller_radius * 0.25
            )
            iris_jnt = joint_utils.Joint.create_at_object(
                obj=eye_dict["eye_iris_guide"],
                name=iris_jnt_name,
                parent=eye_jnt,
                match_rotation=True,
                radius=self.controller_radius * 0.15
            )

            eye_dict["eye_jnt"] = eye_jnt
            eye_dict["iris_jnt"] = iris_jnt
        return self.eye_side_dict

    def create_ctrl(self):
        u"""创建 Eye Main Ctrl 与 Aim Ctrl，并把 Aim 放到 Iris 朝向前方。"""
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            eye_dict = self.eye_side_dict[side]
            eye_ctrl_name = self.create_name(
                type="ctrl",
                side=side,
                part="eye",
                function="main",
                index=1
            )
            aim_ctrl_name = self.create_name(
                type="ctrl",
                side=side,
                part="eye",
                function="aim",
                index=1
            )

            eye_ctrl_dict = ctrl_base.create_ctrl(
                name=eye_ctrl_name,
                shape="circle",
                radius=self.controller_radius,
                color=eye_dict["controller_color"],
                axis="X+",
                target_node=eye_dict["eye_ball_guide"],
                parent_node=self.face_ctrl_grp,
                create_sub_ctrl=False,
                add_to_set=True,
                ctrl_set=config.face_ctrl_set
            )
            aim_ctrl_dict = ctrl_base.create_ctrl(
                name=aim_ctrl_name,
                shape="circle",
                radius=self.controller_radius * 0.65,
                color=eye_dict["controller_color"],
                axis="Z+",
                target_node=eye_dict["eye_iris_guide"],
                parent_node=self.face_ctrl_grp,
                create_sub_ctrl=False,
                add_to_set=True,
                ctrl_set=config.face_ctrl_set
            )

            eye_position = transform_utils.get_world_translation(
                eye_dict["eye_ball_guide"]
            )
            iris_position = transform_utils.get_world_translation(
                eye_dict["eye_iris_guide"]
            )

            direction = [
                iris_position[0] - eye_position[0],
                iris_position[1] - eye_position[1],
                iris_position[2] - eye_position[2],
            ]
            direction_length = math.sqrt(
                direction[0] * direction[0] +
                direction[1] * direction[1] +
                direction[2] * direction[2]
            )

            if direction_length > 0.0001:
                aim_distance = max(
                    self.controller_radius * 5.0,
                    direction_length * 3.0
                )
                aim_position = []
                axis_index = 0

                while axis_index < 3:
                    normalized_value = direction[axis_index] / direction_length
                    aim_position.append(
                        eye_position[axis_index] + normalized_value * aim_distance
                    )
                    axis_index += 1

                transform_utils.set_world_translation(
                    aim_ctrl_dict["top_grp"],
                    aim_position
                )

            eye_dict["eye_ctrl_dict"] = eye_ctrl_dict
            eye_dict["aim_ctrl_dict"] = aim_ctrl_dict

        # -------------------------------------------------------------------------
        # Step 02：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.eye_side_dict

    def create_connect(self):
        u"""Main Ctrl 驱动 Eye Joint；Aim Ctrl 驱动 Main Ctrl 的 Driven Group 朝向。"""
        for side in self.sides:
            eye_dict = self.eye_side_dict[side]
            eye_matrix_name = self.create_name(
                type="mult",
                side=side,
                part="eye",
                function="parent",
                index=1
            )
            eye_matrix = matrix_utils.create_parent_matrix_constraint(
                driver=eye_dict["eye_ctrl_dict"]["output_node"],
                driven=eye_dict["eye_jnt"],
                maintain_offset=False,
                name=eye_matrix_name
            )

            aim_constraint_name = self.create_name(
                type="cns",
                side=side,
                part="eye",
                function="aim",
                index=1
            )
            aim_constraint_list = constraint_utils.create_constraint(
                driver_objects=eye_dict["aim_ctrl_dict"]["output_node"],
                driven_object=eye_dict["eye_ctrl_dict"]["grp_dict"]["driven"],
                constraint_type="aimConstraint",
                maintain_offset=False,
                name=aim_constraint_name,
                aimVector=[1.0, 0.0, 0.0],
                upVector=[0.0, 1.0, 0.0],
                worldUpType="vector",
                worldUpVector=[0.0, 1.0, 0.0]
            )

            if not aim_constraint_list:
                raise RuntimeError(u"{} Eye Aim Constraint 创建失败。".format(side))

            eye_dict["eye_matrix"] = eye_matrix
            eye_dict["aim_constraint"] = aim_constraint_list[0]

        return self.eye_side_dict

    def create_deform(self):
        u"""在 Eye Main Ctrl 上创建 Iris Scale，并驱动 Iris Joint 的 Y/Z Scale。"""
        for side in self.sides:
            eye_dict = self.eye_side_dict[side]
            eye_ctrl = eye_dict["eye_ctrl_dict"]["ctrl_node"]
            eye_ctrl_attr = attr_utils.Attr(
                eye_ctrl
            )
            iris_scale_plug = eye_ctrl_attr.add_attr(
                "iris_scale",
                attr_type="double",
                lock=False,
                hide=False,
                default_value=1.0,
                min_value=0.1,
                max_value=2.0,
                keyable=True,
                channel_box=True
            )
            connection_utils.connect_plugs(
                iris_scale_plug,
                eye_dict["iris_jnt"] + ".scaleY",
                force=True
            )
            connection_utils.connect_plugs(
                iris_scale_plug,
                eye_dict["iris_jnt"] + ".scaleZ",
                force=True
            )
            eye_dict["iris_scale_plug"] = iris_scale_plug

        return self.eye_side_dict

    def create_finalize(self):
        u"""验证 Eye Main / Aim / Iris 的关键构建结果。"""
        for side in self.sides:
            eye_dict = self.eye_side_dict[side]
            required_nodes = [
                eye_dict["eye_jnt"],
                eye_dict["iris_jnt"],
                eye_dict["eye_ctrl_dict"]["ctrl_node"],
                eye_dict["aim_ctrl_dict"]["ctrl_node"],
                eye_dict["eye_matrix"],
                eye_dict["aim_constraint"],
            ]

            for node in required_nodes:
                scene_utils.validate_node(
                    node,
                    label=u"Eye Module Build Node"
                )

        self.module_dict["sides"] = self.eye_side_dict
        self.module_dict["built"] = True
        return True


def build_eye():
    u"""构建 Eye Module 并返回统一 Module Dict。"""
    eye_module = EyeModule()
    eye_module_dict = eye_module.create_build()
    return eye_module_dict


__all__ = [
    "EyeModule",
    "build_eye",
]
