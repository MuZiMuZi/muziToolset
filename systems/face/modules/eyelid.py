# coding=utf-8
u"""
Eyelid Module
=============

上下眼皮绑定模块。

新结构：
    Guide
        -> Detail Ctrl
            -> Curve Driver Jnt
                -> Control Curve
                    -> Blink Blend
                        -> Skin Curve
                            -> Radial Eyelid Bind Jnt

旧 EyeLid 的 Curve / Wire / Blink / Eye Follow 思路被重新整理为无循环的
Control Curve -> Skin Curve 数据流，并复用当前 Face Eyelid Builder。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import attr_utils
from ....core import connection_utils
from ....core import curve_utils
from ....core import joint_utils
from ....core import matrix_utils
from ....core import rename_utils
from ....core import scene_utils
from ....core import transform_utils
from ... import ctrl_base
from .. import config
from ..build.eyelid.builder import build_eyelid_joints
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class EyelidModule(FaceModuleBase):
    u"""构建左右 Upper / Lower Eyelid Curve、Ctrl、Blink 与 Radial Joint。"""

    sides = ["lf", "rt"]
    regions = ["upper", "lower"]

    def __init__(self):
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

        """

        super(EyelidModule, self).__init__(
            side="md",
            part="eyelid",
            index=1
        )
        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_size = 1.0
        self.controller_radius = 1.0
        self.eyelid_side_dict = {}

    def load_setup(self):
        u"""

                读取 Eyelid 设置，并确认 EyeModule 的 Eye Joint / Aim Ctrl 已存在。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    ValueError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )
        self.ensure_hierarchy()

        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        controller_settings = self.face_guide.load_controller_settings()
        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )
        self.controller_size = controller_settings.get(
            config.face_controller_size_attr_names["eyelid"],
            1.0
        )
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(u"Eyelid Controller Radius 必须大于 0。")

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.eyelid_side_dict = {}

        for side in self.sides:
            eye_jnt_name = self.create_name(
                type="jnt",
                side=side,
                part="eye",
                function="bind",
                index=1
            )
            eye_aim_ctrl_name = self.create_name(
                type="ctrl",
                side=side,
                part="eye",
                function="aim",
                index=1
            )
            eye_output_name = self.create_name(
                type="output",
                side=side,
                part="eye",
                function="main",
                index=1
            )

            scene_utils.validate_node(
                eye_jnt_name,
                label=u"EyeModule Eye Joint"
            )
            scene_utils.validate_node(
                eye_aim_ctrl_name,
                label=u"EyeModule Aim Ctrl"
            )
            scene_utils.validate_node(
                eye_output_name,
                label=u"EyeModule Output"
            )

            self.eyelid_side_dict[side] = {
                "controller_color": controller_settings.get(
                    config.face_controller_color_attr_names[side],
                    6 if side == "lf" else 13
                ),
                "eye_jnt": eye_jnt_name,
                "eye_aim_ctrl": eye_aim_ctrl_name,
                "eye_output": eye_output_name,
                "guide_dict": None,
                "guide_jnt_dict": {},
                "ctrl_dict": {},
                "matrix_nodes": [],
                "control_curve_dict": {},
                "skin_curve_dict": {},
                "curve_skin_dict": {},
                "radial_dict": {},
                "up_object": None,
                "blink_dict": None,
            }

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def load_guide(self):
        u"""

                读取左右 Upper / Lower Eyelid 固定有序 Guide。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

        """
        for side in self.sides:
            self.eyelid_side_dict[side]["guide_dict"] = self.face_guide.get_eyelid_guides(
                side=side,
                required=True
            )
        return self.eyelid_side_dict

    def _get_unique_guides(self, side):
        u"""返回一侧 Upper + Lower 中去重且保持顺序的 Guide。"""
        guide_dict = self.eyelid_side_dict[side]["guide_dict"]
        unique_guides = []

        for region in self.regions:
            for guide in guide_dict[region]:
                if guide in unique_guides:
                    continue
                unique_guides.append(guide)

        return unique_guides

    def create_jnt(self):
        u"""

                创建 Curve Driver Jnt、Control/Skin Curve、Up Object 和 Radial Bind Jnt。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            eyelid_dict = self.eyelid_side_dict[side]
            unique_guides = self._get_unique_guides(side)
            guide_jnt_dict = {}

            index = 0
            while index < len(unique_guides):
                guide = unique_guides[index]
                guide_name_data = self.parse_name(
                    rename_utils.get_short_name(guide)
                )
                eyelid_driver_jnt_name = self.create_name(
                    type="jnt",
                    side=side,
                    part=guide_name_data["part"],
                    function="driver",
                    index=guide_name_data["index"]
                )
                scene_utils.ensure_nodes_available(
                    eyelid_driver_jnt_name,
                    label=u"Eyelid Driver Joint"
                )
                eyelid_driver_jnt = joint_utils.Joint.create_at_object(
                    obj=guide,
                    name=eyelid_driver_jnt_name,
                    parent=self.face_jnt_grp,
                    match_rotation=True,
                    radius=self.controller_radius * 0.12
                )
                guide_jnt_dict[guide] = eyelid_driver_jnt
                index += 1

            eyelid_dict["guide_jnt_dict"] = guide_jnt_dict

            up_object_name = self.create_name(
                type="loc",
                side=side,
                part="eyelid",
                function="up",
                index=1
            )
            up_object = cmds.spaceLocator(
                name=up_object_name
            )[0]
            up_position = transform_utils.get_world_translation(
                eyelid_dict["eye_jnt"]
            )
            up_position[1] += self.controller_radius * 5.0
            transform_utils.set_world_translation(
                up_object,
                up_position
            )
            up_object = cmds.parent(
                up_object,
                self.face_rig_nodes_grp
            )[0]
            cmds.setAttr(
                up_object + ".visibility",
                0
            )
            eyelid_dict["up_object"] = up_object

            for region in self.regions:
                region_guides = eyelid_dict["guide_dict"][region]
                control_curve_name = self.create_name(
                    type="crv",
                    side=side,
                    part="{}_lid".format(region),
                    function="control",
                    index=1
                )
                skin_curve_name = self.create_name(
                    type="crv",
                    side=side,
                    part="{}_lid".format(region),
                    function="skin",
                    index=1
                )

                control_curve = curve_utils.create_curve_from_nodes(
                    nodes=region_guides,
                    name=control_curve_name,
                    degree=3
                )
                skin_curve = cmds.duplicate(
                    control_curve,
                    name=skin_curve_name
                )[0]
                control_curve = cmds.parent(
                    control_curve,
                    self.face_rig_nodes_grp
                )[0]
                skin_curve = cmds.parent(
                    skin_curve,
                    self.face_rig_nodes_grp
                )[0]

                radial_dict = build_eyelid_joints(
                    curve=skin_curve,
                    eye_joint=eyelid_dict["eye_jnt"],
                    up_object=up_object,
                    side=side,
                    region=region,
                    parent_group=self.face_rig_nodes_grp,
                    joint_radius=self.controller_radius * 0.12
                )

                eyelid_dict["control_curve_dict"][region] = control_curve
                eyelid_dict["skin_curve_dict"][region] = skin_curve
                eyelid_dict["radial_dict"][region] = radial_dict

        # -------------------------------------------------------------------------
        # Step 02：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.eyelid_side_dict

    def create_ctrl(self):
        u"""

                每个唯一 Eyelid Guide 创建一个 Detail Controller。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        for side in self.sides:
            eyelid_dict = self.eyelid_side_dict[side]
            unique_guides = self._get_unique_guides(side)
            ctrl_dict = {}

            for guide in unique_guides:
                guide_name_data = self.parse_name(
                    rename_utils.get_short_name(guide)
                )
                eyelid_ctrl_name = self.create_name(
                    type="ctrl",
                    side=side,
                    part=guide_name_data["part"],
                    function="bind",
                    index=guide_name_data["index"]
                )
                eyelid_ctrl_dict = ctrl_base.create_ctrl(
                    name=eyelid_ctrl_name,
                    shape="cube",
                    radius=self.controller_radius * 0.32,
                    color=eyelid_dict["controller_color"],
                    axis="X+",
                    target_node=guide,
                    parent_node=self.face_ctrl_grp,
                    create_sub_ctrl=False,
                    add_to_set=True,
                    ctrl_set=config.face_ctrl_set
                )
                ctrl_dict[guide] = eyelid_ctrl_dict

            eyelid_dict["ctrl_dict"] = ctrl_dict

        return self.eyelid_side_dict

    def create_connect(self):
        u"""

                Detail Ctrl 驱动 Curve Driver Jnt，并让中间眼皮控制器跟随 Eye Rotation。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            eyelid_dict = self.eyelid_side_dict[side]
            unique_guides = self._get_unique_guides(side)
            matrix_nodes = []

            for guide in unique_guides:
                guide_name_data = self.parse_name(
                    rename_utils.get_short_name(guide)
                )
                eyelid_matrix_name = self.create_name(
                    type="mult",
                    side=side,
                    part=guide_name_data["part"],
                    function="parent",
                    index=guide_name_data["index"]
                )
                eyelid_matrix_node = matrix_utils.create_parent_matrix_constraint(
                    driver=eyelid_dict["ctrl_dict"][guide]["output_node"],
                    driven=eyelid_dict["guide_jnt_dict"][guide],
                    maintain_offset=False,
                    name=eyelid_matrix_name
                )
                matrix_nodes.append(eyelid_matrix_node)

            eyelid_dict["matrix_nodes"] = matrix_nodes

            for region in self.regions:
                region_guides = eyelid_dict["guide_dict"][region]
                middle_index = int(len(region_guides) / 2)
                middle_guide = region_guides[middle_index]
                ctrl_base.create_follow(
                    driver_node=eyelid_dict["eye_output"],
                    ctrl_dict=eyelid_dict["ctrl_dict"][middle_guide],
                    weight=0.35,
                    attr_name="eye_follow",
                    maintain_offset=True
                )

        # -------------------------------------------------------------------------
        # Step 02：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.eyelid_side_dict

    def create_deform(self):
        u"""

                Skin Control Curve，并建立 Blink Height / Blink 的无循环 BlendShape 网络。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            eyelid_dict = self.eyelid_side_dict[side]

            for region in self.regions:
                region_guides = eyelid_dict["guide_dict"][region]
                influence_jnts = []

                for guide in region_guides:
                    influence_jnts.append(
                        eyelid_dict["guide_jnt_dict"][guide]
                    )

                curve_skin_name = self.create_name(
                    type="skin",
                    side=side,
                    part="{}_lid_curve".format(region),
                    function="bind",
                    index=1
                )
                skin_result = cmds.skinCluster(
                    influence_jnts,
                    eyelid_dict["control_curve_dict"][region],
                    name=curve_skin_name,
                    toSelectedBones=True,
                    bindMethod=0,
                    skinMethod=0,
                    normalizeWeights=1
                )
                eyelid_dict["curve_skin_dict"][region] = skin_result[0]

            blink_curve_name = self.create_name(
                type="crv",
                side=side,
                part="eyelid",
                function="blink",
                index=1
            )
            blink_curve = cmds.duplicate(
                eyelid_dict["skin_curve_dict"]["upper"],
                name=blink_curve_name
            )[0]
            blink_curve = cmds.parent(
                blink_curve,
                self.face_rig_nodes_grp
            )[0]

            blink_mix_name = self.create_name(
                type="bs",
                side=side,
                part="eyelid",
                function="height",
                index=1
            )
            blink_mix = cmds.blendShape(
                eyelid_dict["control_curve_dict"]["upper"],
                eyelid_dict["control_curve_dict"]["lower"],
                blink_curve,
                name=blink_mix_name,
                weight=[(0, 0.5), (1, 0.5)]
            )[0]

            upper_blink_name = self.create_name(
                type="bs",
                side=side,
                part="upper_lid",
                function="blink",
                index=1
            )
            lower_blink_name = self.create_name(
                type="bs",
                side=side,
                part="lower_lid",
                function="blink",
                index=1
            )
            upper_blink_bs = cmds.blendShape(
                eyelid_dict["control_curve_dict"]["upper"],
                blink_curve,
                eyelid_dict["skin_curve_dict"]["upper"],
                name=upper_blink_name,
                weight=[(0, 1.0), (1, 0.0)]
            )[0]
            lower_blink_bs = cmds.blendShape(
                eyelid_dict["control_curve_dict"]["lower"],
                blink_curve,
                eyelid_dict["skin_curve_dict"]["lower"],
                name=lower_blink_name,
                weight=[(0, 1.0), (1, 0.0)]
            )[0]

            aim_ctrl_attr = attr_utils.Attr(
                eyelid_dict["eye_aim_ctrl"]
            )
            blink_plug = aim_ctrl_attr.add_attr(
                "blink",
                attr_type="double",
                lock=False,
                hide=False,
                default_value=0.0,
                min_value=0.0,
                max_value=1.0,
                keyable=True,
                channel_box=True
            )
            blink_height_plug = aim_ctrl_attr.add_attr(
                "blink_height",
                attr_type="double",
                lock=False,
                hide=False,
                default_value=0.5,
                min_value=0.0,
                max_value=1.0,
                keyable=True,
                channel_box=True
            )

            height_reverse_name = self.create_name(
                type="reverse",
                side=side,
                part="eyelid",
                function="height",
                index=1
            )
            blink_reverse_name = self.create_name(
                type="reverse",
                side=side,
                part="eyelid",
                function="blink",
                index=1
            )
            height_reverse = cmds.createNode(
                "reverse",
                name=height_reverse_name
            )
            blink_reverse = cmds.createNode(
                "reverse",
                name=blink_reverse_name
            )

            connection_utils.connect_plugs(
                blink_height_plug,
                blink_mix + ".weight[1]",
                force=True
            )
            connection_utils.connect_plugs(
                blink_height_plug,
                height_reverse + ".inputX",
                force=True
            )
            connection_utils.connect_plugs(
                height_reverse + ".outputX",
                blink_mix + ".weight[0]",
                force=True
            )

            connection_utils.connect_plugs(
                blink_plug,
                blink_reverse + ".inputX",
                force=True
            )

            for blink_bs in [upper_blink_bs, lower_blink_bs]:
                connection_utils.connect_plugs(
                    blink_plug,
                    blink_bs + ".weight[1]",
                    force=True
                )
                connection_utils.connect_plugs(
                    blink_reverse + ".outputX",
                    blink_bs + ".weight[0]",
                    force=True
                )

            for region in self.regions:
                cmds.setAttr(
                    eyelid_dict["control_curve_dict"][region] + ".visibility",
                    0
                )
                cmds.setAttr(
                    eyelid_dict["skin_curve_dict"][region] + ".visibility",
                    0
                )
            cmds.setAttr(
                blink_curve + ".visibility",
                0
            )

            eyelid_dict["blink_dict"] = {
                "blink_curve": blink_curve,
                "blink_mix": blink_mix,
                "upper_blendshape": upper_blink_bs,
                "lower_blendshape": lower_blink_bs,
                "height_reverse": height_reverse,
                "blink_reverse": blink_reverse,
                "blink_plug": blink_plug,
                "blink_height_plug": blink_height_plug,
            }

        # -------------------------------------------------------------------------
        # Step 02：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.eyelid_side_dict

    def create_finalize(self):
        u"""

                验证 Eyelid Curve、Ctrl、Radial Joint 与 Blink Network。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        for side in self.sides:
            eyelid_dict = self.eyelid_side_dict[side]

            for eyelid_ctrl_dict in eyelid_dict["ctrl_dict"].values():
                scene_utils.validate_node(
                    eyelid_ctrl_dict["ctrl_node"],
                    label=u"Eyelid Ctrl"
                )

            for region in self.regions:
                scene_utils.validate_node(
                    eyelid_dict["control_curve_dict"][region],
                    label=u"Eyelid Control Curve"
                )
                scene_utils.validate_node(
                    eyelid_dict["skin_curve_dict"][region],
                    label=u"Eyelid Skin Curve"
                )

                for eyelid_jnt in eyelid_dict["radial_dict"][region]["joints"]:
                    scene_utils.validate_node(
                        eyelid_jnt,
                        label=u"Eyelid Radial Joint"
                    )

            scene_utils.validate_node(
                eyelid_dict["blink_dict"]["blink_curve"],
                label=u"Eyelid Blink Curve"
            )

        self.module_dict["sides"] = self.eyelid_side_dict
        self.module_dict["built"] = True
        return True


def build_eyelid():
    u"""

        构建 Eyelid Module 并返回统一 Module Dict。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    eyelid_module = EyelidModule()
    eyelid_module_dict = eyelid_module.create_build()
    return eyelid_module_dict


__all__ = [
    "EyelidModule",
    "build_eyelid",
]
