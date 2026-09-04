# coding=utf-8
u"""
Brow Module
===========

眉毛绑定模块。

旧 Brow 绑定中真正有价值的关系被保留：

    Brow Main Ctrl
        -> Detail Ctrl Follow
            -> Driver Joint
                -> Skin Surface
                    -> Follicle
                        -> Deform Joint

新版本不再导入 brow_bpjnt.ma，不再固定 7 个 Joint，也不再使用字符串 replace()
推导层级名称。Guide 数量直接来自当前 FaceGuide Template。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import attr_utils
from ....core import connection_utils
from ....core import curve_utils
from ....core import hierarchy_utils
from ....core import jnt_utils
from ....core import matrix_utils
from ....core import scene_utils
from ....core import surface_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class BrowModule(FaceModuleBase):
    u"""构建左右 Brow Main / Detail / Surface / Follicle Deform Rig。"""

    sides = [
        "lf",
        "rt",
    ]

    def __init__(self):
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

        """

        super(BrowModule, self).__init__(
            side="md",
            part="brow",
            index=1
        )

        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_size = 1.0
        self.controller_radius = 1.0
        self.brow_side_dict = {}

    # =========================================================================
    # 01. Load Setup
    # =========================================================================

    def load_setup(self):
        u"""

                读取 Face Setup / Controller Settings，并准备 Brow 构建状态。

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
            config.face_controller_size_attr_names["brow"],
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
            raise ValueError(
                u"Brow Controller Radius 必须大于 0。"
            )

        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.brow_side_dict = {}

        for side in self.sides:
            controller_color = controller_settings.get(
                config.face_controller_color_attr_names[side],
                6 if side == "lf" else 13
            )
            self.brow_side_dict[side] = {
                "side": side,
                "controller_color": controller_color,
                "main_guide": None,
                "point_guides": [],
                "driver_jnts": [],
                "deform_jnts": [],
                "main_ctrl_dict": None,
                "detail_ctrl_dict_list": [],
                "matrix_nodes": [],
                "follow_dict_list": [],
                "curve": None,
                "surface": None,
                "surface_skin": None,
                "follicle_dict_list": [],
            }

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    # =========================================================================
    # 02. Load Guide
    # =========================================================================

    def load_guide(self):
        u"""

                读取左右 Brow Main Guide 和有序 Point Guide。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        for side in self.sides:
            brow_guide_dict = self.face_guide.get_brow_guides(
                side
            )
            main_guide = brow_guide_dict["main"]
            point_guides = brow_guide_dict["points"]

            if main_guide is None:
                raise RuntimeError(
                    u"{} Brow Main Guide 不存在。".format(side)
                )

            if len(point_guides) < 2:
                raise RuntimeError(
                    u"{} Brow 至少需要两个 Point Guide。".format(side)
                )

            self.brow_side_dict[side]["main_guide"] = main_guide
            self.brow_side_dict[side]["point_guides"] = list(point_guides)

        return self.brow_side_dict

    # =========================================================================
    # 03. Create Jnt
    # =========================================================================

    def create_jnt(self):
        u"""

                按 Brow Point Guide 创建独立 Driver Joint。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            brow_dict = self.brow_side_dict[side]
            point_guides = brow_dict["point_guides"]
            driver_jnts = []

            index = 0
            while index < len(point_guides):
                item_index = index + 1
                brow_driver_jnt_name = self.create_name(
                    type="jnt",
                    side=side,
                    part="brow_driver",
                    function="bind",
                    index=item_index
                )

                scene_utils.ensure_nodes_available(
                    brow_driver_jnt_name,
                    label=u"Brow Driver Joint"
                )

                brow_driver_jnt = jnt_utils.Joint.create_at_object(
                    obj=point_guides[index],
                    name=brow_driver_jnt_name,
                    parent=self.face_jnt_grp,
                    match_rotation=True,
                    radius=self.controller_radius * 0.2
                )
                driver_jnts.append(
                    brow_driver_jnt
                )
                index += 1

            brow_dict["driver_jnts"] = driver_jnts

        # -------------------------------------------------------------------------
        # Step 02：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.brow_side_dict

    # =========================================================================
    # 04. Create Ctrl
    # =========================================================================

    def create_ctrl(self):
        u"""

                创建每侧 Brow Main Ctrl 和与 Guide 一一对应的 Detail Ctrl。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            brow_dict = self.brow_side_dict[side]

            brow_main_ctrl_name = self.create_name(
                type="ctrl",
                side=side,
                part="brow",
                function="main",
                index=1
            )
            brow_main_ctrl_dict = ctrl_base.create_ctrl(
                name=brow_main_ctrl_name,
                shape="square",
                radius=self.controller_radius * 1.5,
                color=brow_dict["controller_color"],
                axis="X+",
                target_node=brow_dict["main_guide"],
                parent_node=self.face_ctrl_grp,
                create_sub_ctrl=False,
                add_to_set=True,
                ctrl_set=config.face_ctrl_set
            )
            brow_dict["main_ctrl_dict"] = brow_main_ctrl_dict

            brow_main_attr = attr_utils.Attr(
                brow_main_ctrl_dict["ctrl_node"]
            )
            brow_ctrl_vis_plug = brow_main_attr.add_attr(
                "brow_ctrl_vis",
                attr_type="bool",
                lock=False,
                hide=False,
                default_value=1,
                keyable=True,
                channel_box=True
            )

            detail_ctrl_dict_list = []
            point_guides = brow_dict["point_guides"]
            index = 0

            while index < len(point_guides):
                item_index = index + 1
                brow_detail_ctrl_name = self.create_name(
                    type="ctrl",
                    side=side,
                    part="brow_detail",
                    function="bind",
                    index=item_index
                )
                brow_detail_ctrl_dict = ctrl_base.create_ctrl(
                    name=brow_detail_ctrl_name,
                    shape="cube",
                    radius=self.controller_radius * 0.45,
                    color=brow_dict["controller_color"],
                    axis="X+",
                    target_node=point_guides[index],
                    parent_node=self.face_ctrl_grp,
                    create_sub_ctrl=False,
                    add_to_set=True,
                    ctrl_set=config.face_ctrl_set
                )

                connection_utils.connect_plugs(
                    brow_ctrl_vis_plug,
                    brow_detail_ctrl_dict["top_grp"] + ".visibility",
                    force=True
                )

                detail_ctrl_dict_list.append(
                    brow_detail_ctrl_dict
                )
                index += 1

            brow_dict["detail_ctrl_dict_list"] = detail_ctrl_dict_list

        # -------------------------------------------------------------------------
        # Step 02：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.brow_side_dict

    # =========================================================================
    # 05. Create Connect
    # =========================================================================

    def create_connect(self):
        u"""

                建立 Detail Ctrl -> Driver Jnt，并给 Detail Ctrl 添加 Main Follow。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            brow_dict = self.brow_side_dict[side]
            detail_ctrl_dict_list = brow_dict["detail_ctrl_dict_list"]
            driver_jnts = brow_dict["driver_jnts"]
            main_output = brow_dict["main_ctrl_dict"]["output_node"]
            matrix_nodes = []
            follow_dict_list = []

            item_count = len(detail_ctrl_dict_list)
            index = 0

            while index < item_count:
                item_index = index + 1
                brow_matrix_name = self.create_name(
                    type="mult",
                    side=side,
                    part="brow_detail",
                    function="parent",
                    index=item_index
                )
                brow_matrix_node = matrix_utils.create_parent_matrix_constraint(
                    driver=detail_ctrl_dict_list[index]["output_node"],
                    driven=driver_jnts[index],
                    maintain_offset=False,
                    name=brow_matrix_name
                )
                matrix_nodes.append(
                    brow_matrix_node
                )

                if item_count == 1:
                    follow_weight = 1.0
                else:
                    normalized_index = float(index) / float(item_count - 1)
                    follow_weight = 1.0 - (abs(normalized_index - 0.5) * 0.5)

                brow_follow_dict = ctrl_base.create_follow(
                    driver_node=main_output,
                    ctrl_dict=detail_ctrl_dict_list[index],
                    weight=follow_weight,
                    attr_name="follow",
                    maintain_offset=True
                )
                follow_dict_list.append(
                    brow_follow_dict
                )
                index += 1

            brow_dict["matrix_nodes"] = matrix_nodes
            brow_dict["follow_dict_list"] = follow_dict_list

        # -------------------------------------------------------------------------
        # Step 02：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.brow_side_dict

    # =========================================================================
    # 06. Create Deform
    # =========================================================================

    def create_deform(self):
        u"""

                创建 Brow Driver Curve / Skin Surface / Follicle Deform Joints。

                Driver Joint 只负责控制 Surface；真正用于后续 Face Skin 的输出是附着在
                Follicle 下的 Deform Joint。这样保留旧 Brow Surface/Follicle 设计，但把
                Surface 与 Joint/Controller 的职责拆回当前 Core / System 边界。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            brow_dict = self.brow_side_dict[side]
            point_guides = brow_dict["point_guides"]
            driver_jnts = brow_dict["driver_jnts"]

            brow_curve_name = self.create_name(
                type="crv",
                side=side,
                part="brow",
                function="driver",
                index=1
            )
            brow_surface_name = self.create_name(
                type="suf",
                side=side,
                part="brow",
                function="driver",
                index=1
            )
            brow_skin_name = self.create_name(
                type="skin",
                side=side,
                part="brow_surface",
                function="bind",
                index=1
            )

            scene_utils.ensure_nodes_available(
                [
                    brow_curve_name,
                    brow_surface_name,
                    brow_skin_name,
                ],
                label=u"Brow Deform Node"
            )

            curve_degree = 3
            if len(point_guides) < 4:
                curve_degree = 1

            brow_curve = curve_utils.create_curve_from_nodes(
                nodes=point_guides,
                name=brow_curve_name,
                degree=curve_degree
            )
            brow_curve = hierarchy_utils.parent(
                brow_curve,
                self.face_rig_nodes_grp
            )

            brow_surface = surface_utils.create_surface_from_curve(
                curve=brow_curve,
                name=brow_surface_name,
                offset=self.controller_radius * 0.15,
                offset_axis="Y",
                degree=3
            )
            brow_surface = hierarchy_utils.parent(
                brow_surface,
                self.face_rig_nodes_grp
            )

            skin_result = cmds.skinCluster(
                driver_jnts,
                brow_surface,
                name=brow_skin_name,
                toSelectedBones=True,
                bindMethod=0,
                skinMethod=0,
                normalizeWeights=1
            )
            brow_surface_skin = skin_result[0]

            follicle_prefix = self.create_name(
                type="fol",
                side=side,
                part="brow",
                function="deform",
                index=1
            ).rsplit("_", 1)[0]

            follicle_dict_list = surface_utils.create_even_follicles(
                surface=brow_surface,
                count=len(point_guides),
                name_prefix=follicle_prefix,
                direction="V",
                fixed_parameter=0.5,
                parent=self.face_rig_nodes_grp
            )

            deform_jnts = []
            index = 0

            while index < len(follicle_dict_list):
                item_index = index + 1
                brow_deform_jnt_name = self.create_name(
                    type="jnt",
                    side=side,
                    part="brow_deform",
                    function="bind",
                    index=item_index
                )
                brow_deform_jnt = cmds.createNode(
                    "joint",
                    name=brow_deform_jnt_name,
                    parent=follicle_dict_list[index]["transform"]
                )
                cmds.setAttr(
                    brow_deform_jnt + ".translate",
                    0.0,
                    0.0,
                    0.0
                )
                cmds.setAttr(
                    brow_deform_jnt + ".rotate",
                    0.0,
                    0.0,
                    0.0
                )
                cmds.setAttr(
                    brow_deform_jnt + ".radius",
                    self.controller_radius * 0.15
                )
                deform_jnts.append(
                    brow_deform_jnt
                )
                index += 1

            cmds.setAttr(
                brow_curve + ".visibility",
                0
            )
            cmds.setAttr(
                brow_surface + ".visibility",
                0
            )

            brow_dict["curve"] = brow_curve
            brow_dict["surface"] = brow_surface
            brow_dict["surface_skin"] = brow_surface_skin
            brow_dict["follicle_dict_list"] = follicle_dict_list
            brow_dict["deform_jnts"] = deform_jnts

        # -------------------------------------------------------------------------
        # Step 02：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.brow_side_dict

    # =========================================================================
    # 07. Create Finalize
    # =========================================================================

    def create_finalize(self):
        u"""

                验证左右 Brow 模块关键输出，并整理公开 Module Dict。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        # -------------------------------------------------------------------------
        # Step 01：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            brow_dict = self.brow_side_dict[side]
            required_nodes = []
            required_nodes.append(
                brow_dict["main_ctrl_dict"]["ctrl_node"]
            )
            required_nodes.append(
                brow_dict["curve"]
            )
            required_nodes.append(
                brow_dict["surface"]
            )
            required_nodes.append(
                brow_dict["surface_skin"]
            )

            for brow_driver_jnt in brow_dict["driver_jnts"]:
                required_nodes.append(
                    brow_driver_jnt
                )

            for brow_deform_jnt in brow_dict["deform_jnts"]:
                required_nodes.append(
                    brow_deform_jnt
                )

            for node in required_nodes:
                scene_utils.validate_node(
                    node,
                    label=u"Brow Module Build Node"
                )

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.module_dict["sides"] = self.brow_side_dict
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.module_dict["built"] = True
        # -------------------------------------------------------------------------
        # Step 04：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True


def build_brow():
    u"""

        构建 Brow Module 并返回统一 Module Dict。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    brow_module = BrowModule()
    brow_module_dict = brow_module.create_build()
    return brow_module_dict


__all__ = [
    "BrowModule",
    "build_brow",
]
