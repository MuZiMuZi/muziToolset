# coding=utf-8
u"""
Cheek Module
============

脸颊区域绑定模块。

旧 Cheek 的 CheekBone / Nasolabial / Cheek 三组定位思想保留；
新版本直接读取 Face Guide，不再导入 cheek_bpjnt.ma，也不再依赖右侧负 Scale 镜像。

正式 Face Guide 由 FaceGuide 统一维护 CheekBone / Nasolabial / Cheek 定位；
本模块只消费结构化 Guide 数据，不再维护独立 bpjnt 或额外定位资产。
"""

from __future__ import print_function

from ....core import jnt_utils
from ....core import matrix_utils
from ....core import scene_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class CheekModule(FaceModuleBase):
    u"""根据左右脸颊 Guide 创建局部 Jnt / Ctrl / Matrix Rig。"""

    sides = ["lf", "rt"]
    regions = ["cheekbone", "nasolabial", "cheek"]

    def __init__(self):
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

        """

        super(CheekModule, self).__init__(
            side="md",
            part="cheek",
            index=1
        )
        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_size = 1.0
        self.controller_radius = 1.0
        self.cheek_side_dict = {}
        self.skipped = False
        self.skip_reason = None

    def load_setup(self):
        u"""

                读取 Face Setup 与 Cheek Controller Settings。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    ValueError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        # -------------------------------------------------------------------------
        # Step 01：验证 Face Setup，并确保正式 Face Rig 公共层级已经存在
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=False
        )
        self.ensure_hierarchy()

        # -------------------------------------------------------------------------
        # Step 02：读取 Cheek Controller 的全局缩放、部位尺寸和左右颜色
        # -------------------------------------------------------------------------
        controller_settings = self.face_guide.load_controller_settings()
        self.controller_global_scale = controller_settings.get(
            config.face_controller_global_scale_attr,
            1.0
        )
        self.controller_size = controller_settings.get(
            config.face_controller_size_attr_names["cheek"],
            1.0
        )
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        if self.controller_radius <= 0.0:
            raise ValueError(u"Cheek Controller Radius 必须大于 0。")

        # -------------------------------------------------------------------------
        # Step 03：重置本次构建状态，避免重复使用实例时残留上一次结果
        # -------------------------------------------------------------------------
        self.skipped = False
        self.skip_reason = None
        self.cheek_side_dict = {}

        for side in self.sides:
            self.cheek_side_dict[side] = {
                "controller_color": controller_settings.get(
                    config.face_controller_color_attr_names[side],
                    6 if side == "lf" else 13
                ),
                "region_dict": {},
            }

        return True

    def load_guide(self):
        u"""

                按 CheekBone / Nasolabial / Cheek 分类读取左右 Guide。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

        """
        # -------------------------------------------------------------------------
        # Step 01：通过 FaceGuide 的固定 Schema 一次性读取左右 Cheek Guide
        # -------------------------------------------------------------------------
        cheek_guide_dict = self.face_guide.get_cheek_guides(
            required=True
        )
        total_guide_count = 0

        for side in self.sides:
            region_dict = {}

            for region in self.regions:
                region_guides = cheek_guide_dict[side][region]
                region_dict[region] = {
                    "guides": list(region_guides),
                    "jnts": [],
                    "ctrl_dict_list": [],
                    "matrix_nodes": [],
                }
                total_guide_count += len(region_guides)

            self.cheek_side_dict[side]["region_dict"] = region_dict

        # -------------------------------------------------------------------------
        # Step 02：当前模板没有 Cheek Guide 时记录可选模块跳过状态，而不是终止 FaceRig
        # -------------------------------------------------------------------------
        if total_guide_count == 0:
            self.skipped = True
            self.skip_reason = (
                u"当前 Face Guide 模板没有 Cheek / CheekBone / Nasolabial 定位。"
            )

        return self.cheek_side_dict

    def create_jnt(self):
        u"""

                每个有效 Cheek Guide 创建一个独立 Bind Joint。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if self.skipped:
            return self.cheek_side_dict

        # -------------------------------------------------------------------------
        # Step 02：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            region_dict = self.cheek_side_dict[side]["region_dict"]

            for region in self.regions:
                region_data = region_dict[region]
                region_jnts = []
                index = 0

                while index < len(region_data["guides"]):
                    item_index = index + 1
                    cheek_jnt_name = self.create_name(
                        type="jnt",
                        side=side,
                        part=region,
                        function="bind",
                        index=item_index
                    )
                    scene_utils.ensure_nodes_available(
                        cheek_jnt_name,
                        label=u"Cheek Joint"
                    )
                    cheek_jnt = joint_utils.Joint.create_at_object(
                        obj=region_data["guides"][index],
                        name=cheek_jnt_name,
                        parent=self.face_jnt_grp,
                        match_rotation=True,
                        radius=self.controller_radius * 0.2
                    )
                    region_jnts.append(cheek_jnt)
                    index += 1

                region_data["jnts"] = region_jnts

        # -------------------------------------------------------------------------
        # Step 03：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.cheek_side_dict

    def create_ctrl(self):
        u"""

                为每个 Cheek Joint 创建独立 Animator Controller。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if self.skipped:
            return self.cheek_side_dict

        # -------------------------------------------------------------------------
        # Step 02：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for side in self.sides:
            side_data = self.cheek_side_dict[side]
            region_dict = side_data["region_dict"]

            for region in self.regions:
                region_data = region_dict[region]
                ctrl_dict_list = []
                index = 0

                while index < len(region_data["guides"]):
                    item_index = index + 1
                    cheek_ctrl_name = self.create_name(
                        type="ctrl",
                        side=side,
                        part=region,
                        function="bind",
                        index=item_index
                    )
                    cheek_ctrl_dict = ctrl_base.create_ctrl(
                        name=cheek_ctrl_name,
                        shape="cube",
                        radius=self.controller_radius * 0.45,
                        color=side_data["controller_color"],
                        axis="X+",
                        target_node=region_data["guides"][index],
                        parent_node=self.face_ctrl_grp,
                        create_sub_ctrl=False,
                        add_to_set=True,
                        ctrl_set=config.face_ctrl_set
                    )
                    ctrl_dict_list.append(cheek_ctrl_dict)
                    index += 1

                region_data["ctrl_dict_list"] = ctrl_dict_list

        # -------------------------------------------------------------------------
        # Step 03：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.cheek_side_dict

    def create_connect(self):
        u"""

                使用每个 Controller Output 驱动对应 Cheek Joint。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        if self.skipped:
            return self.cheek_side_dict

        for side in self.sides:
            region_dict = self.cheek_side_dict[side]["region_dict"]

            for region in self.regions:
                region_data = region_dict[region]
                matrix_nodes = []
                index = 0

                while index < len(region_data["jnts"]):
                    item_index = index + 1
                    cheek_matrix_name = self.create_name(
                        type="mult",
                        side=side,
                        part=region,
                        function="parent",
                        index=item_index
                    )
                    cheek_matrix_node = matrix_utils.create_parent_matrix_constraint(
                        driver=region_data["ctrl_dict_list"][index]["output_node"],
                        driven=region_data["jnts"][index],
                        maintain_offset=False,
                        name=cheek_matrix_name
                    )
                    matrix_nodes.append(cheek_matrix_node)
                    index += 1

                region_data["matrix_nodes"] = matrix_nodes

        return self.cheek_side_dict

    def create_deform(self):
        u"""

                Cheek 的输出 Joint 本身作为后续 Face Skin Influence。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        if self.skipped:
            return True

        return True

    def create_finalize(self):
        u"""

                验证 Cheek Jnt / Ctrl / Matrix，并整理模块公开结果。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        # -------------------------------------------------------------------------
        # Step 01：可选模块没有 Guide 时，把跳过状态作为正式结果返回
        # -------------------------------------------------------------------------
        if self.skipped:
            self.module_dict["sides"] = self.cheek_side_dict
            self.module_dict["built"] = False
            self.module_dict["skipped"] = True
            self.module_dict["reason"] = self.skip_reason
            return True

        # -------------------------------------------------------------------------
        # Step 02：逐侧验证所有已经创建的 Joint、Controller 与 Matrix Network
        # -------------------------------------------------------------------------
        for side in self.sides:
            region_dict = self.cheek_side_dict[side]["region_dict"]

            for region in self.regions:
                region_data = region_dict[region]

                for cheek_jnt in region_data["jnts"]:
                    scene_utils.validate_node(
                        cheek_jnt,
                        label=u"Cheek Joint"
                    )

                for cheek_ctrl_dict in region_data["ctrl_dict_list"]:
                    scene_utils.validate_node(
                        cheek_ctrl_dict["ctrl_node"],
                        label=u"Cheek Ctrl"
                    )

                for cheek_matrix_node in region_data["matrix_nodes"]:
                    scene_utils.validate_node(
                        cheek_matrix_node,
                        label=u"Cheek Matrix"
                    )

        # -------------------------------------------------------------------------
        # Step 03：整理稳定的公开结果，供 FaceRig 和后续 Deformer 阶段继续复用
        # -------------------------------------------------------------------------
        self.module_dict["sides"] = self.cheek_side_dict
        self.module_dict["built"] = True
        self.module_dict["skipped"] = False
        self.module_dict["reason"] = None
        return True


def build_cheek():
    u"""

        构建 Cheek Module 并返回统一 Module Dict。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    cheek_module = CheekModule()
    cheek_module_dict = cheek_module.create_build()
    return cheek_module_dict


__all__ = [
    "CheekModule",
    "build_cheek",
]
