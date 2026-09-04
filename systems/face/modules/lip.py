# coding=utf-8
u"""
Lip Module
==========

Upper / Lower Lip 曲线绑定模块。

数据流：
    Lip Guide
        -> Detail Ctrl
            -> Curve Driver Jnt
                -> Control / Skin / Aim / Up Curves
                    -> Curve Attachment
                        -> Deform Jnt

Controller 数量由 Guide 决定；最终 Deform Joint 密度由 Step01 的 mouth_jnt_number 决定。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import curve_utils
from ....core import jnt_utils
from ....core import matrix_utils
from ....core import rename_utils
from ....core import scene_utils
from ... import ctrl_base
from .. import config
from ..build.curve_attachment import attach_joints_to_curves
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class LipModule(FaceModuleBase):
    u"""构建 Upper / Lower Lip Detail Ctrl、曲线和 Deform Joint。"""

    regions = ["upper", "lower"]

    def __init__(self):
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

        """

        super(LipModule, self).__init__(
            side="md",
            part="lip",
            index=1
        )
        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_size = 1.0
        self.controller_radius = 1.0
        self.lip_jnt_count = 8
        self.lip_guide_dict = None
        self.guide_driver_jnt_dict = {}
        self.lip_ctrl_dict = {}
        self.lip_region_dict = {}
        self.matrix_nodes = []

    def load_setup(self):
        u"""

                读取 Lip Controller 设置与 Mouth Joint 数量。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    ValueError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        # -------------------------------------------------------------------------
        # Step 01：确认 Face Setup 已完成，并读取统一 Controller Settings
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=True
        )
        self.ensure_hierarchy()

        controller_settings = self.face_guide.load_controller_settings()
        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )
        self.controller_size = controller_settings.get(
            config.face_controller_size_attr_names["lip"],
            1.0
        )
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        # -------------------------------------------------------------------------
        # Step 02：把 Step01 的 Mouth Joint 数量转换成单侧 Upper / Lower 采样密度
        # -------------------------------------------------------------------------
        if self.controller_radius <= 0.0:
            raise ValueError(u"Lip Controller Radius 必须大于 0。")

        mouth_jnt_number = int(self.mouth_jnt_number)
        if mouth_jnt_number < 6:
            raise ValueError(u"mouth_jnt_number 至少需要 6。")

        self.lip_jnt_count = max(
            5,
            int(round(float(mouth_jnt_number) / 2.0))
        )

        # -------------------------------------------------------------------------
        # Step 03：清空本次 Build 的运行时结果
        # -------------------------------------------------------------------------
        self.guide_driver_jnt_dict = {}
        self.lip_ctrl_dict = {}
        self.lip_region_dict = {}
        self.matrix_nodes = []
        return True

    def load_guide(self):
        u"""

                读取固定顺序 Upper / Lower Lip 与共享 Mouth Corner Guide。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

        """
        self.lip_guide_dict = self.face_guide.get_lip_guides(
            required=True
        )
        return self.lip_guide_dict

    def _get_unique_guides(self):
        u"""返回 Upper + Lower Guide 去重后的稳定列表。"""
        unique_guides = []

        for region in self.regions:
            for guide in self.lip_guide_dict[region]:
                if guide in unique_guides:
                    continue
                unique_guides.append(guide)

        return unique_guides

    def create_jnt(self):
        u"""

                创建 Curve Driver Jnt、四条曲线和最终 Deform Jnt Attachment。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        unique_guides = self._get_unique_guides()

        # -------------------------------------------------------------------------
        # Step 01：每个唯一 Lip / Mouth Corner Guide 创建一个 Curve Driver Joint
        # -------------------------------------------------------------------------
        for guide in unique_guides:
            guide_data = self.parse_name(
                rename_utils.get_short_name(guide)
            )
            lip_driver_jnt_name = self.create_name(
                type="jnt",
                side=guide_data["side"],
                part=guide_data["part"],
                function="driver",
                index=guide_data["index"]
            )
            scene_utils.ensure_nodes_available(
                lip_driver_jnt_name,
                label=u"Lip Curve Driver Joint"
            )
            lip_driver_jnt = jnt_utils.Joint.create_at_object(
                obj=guide,
                name=lip_driver_jnt_name,
                parent=self.face_jnt_grp,
                match_rotation=True,
                radius=self.controller_radius * 0.12
            )
            self.guide_driver_jnt_dict[guide] = lip_driver_jnt

        # -------------------------------------------------------------------------
        # Step 02：为 Upper / Lower 分别建立 Control、Skin、Aim、Up 四条曲线
        # -------------------------------------------------------------------------
        for region in self.regions:
            region_guides = self.lip_guide_dict[region]
            control_curve_name = self.create_name(
                type="crv",
                side="md",
                part="{}_lip".format(region),
                function="control",
                index=1
            )
            skin_curve_name = self.create_name(
                type="crv",
                side="md",
                part="{}_lip".format(region),
                function="skin",
                index=1
            )
            aim_curve_name = self.create_name(
                type="crv",
                side="md",
                part="{}_lip".format(region),
                function="aim",
                index=1
            )
            up_curve_name = self.create_name(
                type="crv",
                side="md",
                part="{}_lip".format(region),
                function="up",
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
            aim_curve = cmds.duplicate(
                control_curve,
                name=aim_curve_name
            )[0]
            up_curve = cmds.duplicate(
                control_curve,
                name=up_curve_name
            )[0]

            cmds.move(
                0.0,
                0.0,
                self.controller_radius,
                aim_curve,
                relative=True,
                worldSpace=True
            )
            cmds.move(
                0.0,
                self.controller_radius,
                0.0,
                up_curve,
                relative=True,
                worldSpace=True
            )

            control_curve = cmds.parent(
                control_curve,
                self.face_rig_nodes_grp
            )[0]
            skin_curve = cmds.parent(
                skin_curve,
                self.face_rig_nodes_grp
            )[0]
            aim_curve = cmds.parent(
                aim_curve,
                self.face_rig_nodes_grp
            )[0]
            up_curve = cmds.parent(
                up_curve,
                self.face_rig_nodes_grp
            )[0]

            # ---------------------------------------------------------------------
            # Step 03：按真实弧长均匀采样 Skin Curve，创建最终 Lip Deform Joint
            # ---------------------------------------------------------------------
            sample_dict = curve_utils.sample_curve_by_length(
                skin_curve,
                self.lip_jnt_count,
                world_space=True
            )
            sample_points = sample_dict["points"]
            deform_jnts = []
            sample_index = 0

            while sample_index < len(sample_points):
                item_index = sample_index + 1
                lip_deform_jnt_name = self.create_name(
                    type="jnt",
                    side="md",
                    part="{}_lip_deform".format(region),
                    function="bind",
                    index=item_index
                )
                lip_deform_jnt = jnt_utils.Joint.create(
                    name=lip_deform_jnt_name,
                    position=sample_points[sample_index],
                    parent=self.face_jnt_grp,
                    radius=self.controller_radius * 0.1
                )
                deform_jnts.append(lip_deform_jnt)
                sample_index += 1

            # ---------------------------------------------------------------------
            # Step 04：把 Deform Joint 接入 Skin / Aim / Up Curve Attachment 网络
            # ---------------------------------------------------------------------
            attachment_dict = attach_joints_to_curves(
                joints=deform_jnts,
                drive_curve=skin_curve,
                aim_curve=aim_curve,
                up_curve=up_curve,
                side="md",
                region=region,
                feature="lip",
                parent_group=self.face_rig_nodes_grp,
                preserve_joint_offset=False
            )

            self.lip_region_dict[region] = {
                "control_curve": control_curve,
                "skin_curve": skin_curve,
                "aim_curve": aim_curve,
                "up_curve": up_curve,
                "deform_jnts": deform_jnts,
                "attachment_dict": attachment_dict,
                "curve_skin_nodes": [],
            }

        return self.lip_region_dict

    def create_ctrl(self):
        u"""

                每个唯一 Lip / Mouth Corner Guide 创建一个 Detail Controller。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        controller_settings = self.face_guide.load_controller_settings()
        unique_guides = self._get_unique_guides()

        # -------------------------------------------------------------------------
        # Step 01：按 Guide 自身 side 创建独立 Lip Detail Controller
        # -------------------------------------------------------------------------
        for guide in unique_guides:
            guide_data = self.parse_name(
                rename_utils.get_short_name(guide)
            )
            side = guide_data["side"]
            lip_ctrl_name = self.create_name(
                type="ctrl",
                side=side,
                part=guide_data["part"],
                function="bind",
                index=guide_data["index"]
            )
            controller_color = controller_settings.get(
                config.face_controller_color_attr_names[side],
                17 if side == "md" else (6 if side == "lf" else 13)
            )
            lip_ctrl_dict = ctrl_base.create_ctrl(
                name=lip_ctrl_name,
                shape="cube",
                radius=self.controller_radius * 0.35,
                color=controller_color,
                axis="X+",
                target_node=guide,
                parent_node=self.face_ctrl_grp,
                create_sub_ctrl=False,
                add_to_set=True,
                ctrl_set=config.face_ctrl_set
            )
            self.lip_ctrl_dict[guide] = lip_ctrl_dict

        return self.lip_ctrl_dict

    def create_connect(self):
        u"""

                Lip Detail Ctrl Output 一一驱动 Curve Driver Joint。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        self.matrix_nodes = []

        # -------------------------------------------------------------------------
        # Step 01：Controller Output 与对应 Guide Driver Joint 建立 Matrix 驱动
        # -------------------------------------------------------------------------
        for guide in self._get_unique_guides():
            guide_data = self.parse_name(
                rename_utils.get_short_name(guide)
            )
            lip_matrix_name = self.create_name(
                type="mult",
                side=guide_data["side"],
                part=guide_data["part"],
                function="parent",
                index=guide_data["index"]
            )
            lip_matrix_node = matrix_utils.create_parent_matrix_constraint(
                driver=self.lip_ctrl_dict[guide]["output_node"],
                driven=self.guide_driver_jnt_dict[guide],
                maintain_offset=False,
                name=lip_matrix_name
            )
            self.matrix_nodes.append(lip_matrix_node)

        return self.matrix_nodes

    def create_deform(self):
        u"""

                用 Guide Driver Joint 同步驱动 Control / Skin / Aim / Up 四条曲线。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：按 Upper / Lower 收集对应 Guide Driver Joint
        # -------------------------------------------------------------------------
        for region in self.regions:
            region_data = self.lip_region_dict[region]
            influence_jnts = []

            for guide in self.lip_guide_dict[region]:
                influence_jnts.append(
                    self.guide_driver_jnt_dict[guide]
                )

            # ---------------------------------------------------------------------
            # Step 02：同一组 Driver Joint 分别 Skin 四条功能曲线，保持同步空间关系
            # ---------------------------------------------------------------------
            curve_skin_nodes = []
            curve_roles = [
                "control_curve",
                "skin_curve",
                "aim_curve",
                "up_curve",
            ]

            for curve_role in curve_roles:
                curve_skin_name = self.create_name(
                    type="skin",
                    side="md",
                    part="{}_lip_{}".format(region, curve_role.replace("_curve", "")),
                    function="bind",
                    index=1
                )
                skin_result = cmds.skinCluster(
                    influence_jnts,
                    region_data[curve_role],
                    name=curve_skin_name,
                    toSelectedBones=True,
                    bindMethod=0,
                    skinMethod=0,
                    normalizeWeights=1
                )
                curve_skin_nodes.append(
                    skin_result[0]
                )
                cmds.setAttr(
                    region_data[curve_role] + ".visibility",
                    0
                )

            region_data["curve_skin_nodes"] = curve_skin_nodes

        return self.lip_region_dict

    def create_finalize(self):
        u"""

                验证 Lip Ctrl、Curve、Attachment 和 Deform Joint。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        # -------------------------------------------------------------------------
        # Step 01：验证全部 Detail Controller
        # -------------------------------------------------------------------------
        for lip_ctrl_dict in self.lip_ctrl_dict.values():
            scene_utils.validate_node(
                lip_ctrl_dict["ctrl_node"],
                label=u"Lip Ctrl"
            )

        # -------------------------------------------------------------------------
        # Step 02：验证 Upper / Lower 曲线和最终 Deform Joint
        # -------------------------------------------------------------------------
        for region in self.regions:
            region_data = self.lip_region_dict[region]
            for curve_role in ["control_curve", "skin_curve", "aim_curve", "up_curve"]:
                scene_utils.validate_node(
                    region_data[curve_role],
                    label=u"Lip Curve"
                )

            resolved_deform_jnts = []

            for lip_deform_jnt in region_data["deform_jnts"]:
                resolved_deform_jnt = self._resolve_scene_node(
                    lip_deform_jnt,
                    label=u"Lip Deform Joint",
                    node_type="joint"
                )
                resolved_deform_jnts.append(
                    resolved_deform_jnt
                )

            region_data["deform_jnts"] = resolved_deform_jnts

        # -------------------------------------------------------------------------
        # Step 03：整理统一 Module 输出
        # -------------------------------------------------------------------------
        self.module_dict["guide_dict"] = self.lip_guide_dict
        self.module_dict["driver_jnts"] = self.guide_driver_jnt_dict
        self.module_dict["ctrl_dict"] = self.lip_ctrl_dict
        self.module_dict["regions"] = self.lip_region_dict
        self.module_dict["matrix_nodes"] = self.matrix_nodes
        self.module_dict["built"] = True
        return True


def build_lip():
    u"""

        构建 Lip Module 并返回统一 Module Dict。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    lip_module = LipModule()
    lip_module_dict = lip_module.create_build()
    return lip_module_dict


__all__ = [
    "LipModule",
    "build_lip",
]
