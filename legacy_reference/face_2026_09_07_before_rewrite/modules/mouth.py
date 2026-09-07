# coding=utf-8
u"""
Mouth Module
============

嘴部关系与特殊效果模块。

依赖：
    JawModule
    LipModule

职责：
    - 创建 Mouth Main Ctrl；
    - Mouth Main 跟随 Jaw；
    - 左右 Mouth Corner 跟随 Mouth Main；
    - 使用正式 Matrix Zip Lip Builder 创建拉链嘴。
"""

from __future__ import print_function

from ....core import scene_utils
from ....core import snap_utils
from ....core import transform_utils
from ... import ctrl_base
from .. import config
from ..build.lip.zip_builder import build_zip_lip
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class MouthModule(FaceModuleBase):
    u"""组织 Jaw / Lip / Mouth Corner 的关系并创建 Zip Lip。"""

    def __init__(self):
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

        """

        super(MouthModule, self).__init__(
            side="md",
            part="mouth",
            index=1
        )
        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_size = 1.0
        self.controller_radius = 1.0
        self.lip_jnt_count = 8

        self.lip_guide_dict = None
        self.upper_lip_jnts = []
        self.lower_lip_jnts = []
        self.left_corner_ctrl = None
        self.right_corner_ctrl = None
        self.jaw_ctrl = None
        self.jaw_output = None
        self.mouth_main_ctrl_dict = None
        self.mouth_follow_dict = None
        self.corner_follow_dict_list = []
        self.zip_lip_dict = None

    def load_setup(self):
        u"""

                读取 Mouth 设置，并确认 JawModule / LipModule 的关键节点已存在。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.validate_setup_config(
            require_mouth_jnt_number=True
        )
        self.ensure_hierarchy()

        controller_settings = self.face_guide.load_controller_settings()
        # -------------------------------------------------------------------------
        # Step 02：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
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
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.lip_jnt_count = max(
            5,
            int(round(float(self.mouth_jnt_number) / 2.0))
        )

        jaw_ctrl_name = self.create_name(
            type="ctrl",
            side="md",
            part="jaw",
            function="bind",
            index=1
        )
        jaw_output_name = self.create_name(
            type="output",
            side="md",
            part="jaw",
            function="bind",
            index=1
        )

        # -------------------------------------------------------------------------
        # Step 04：解析 Jaw / Lip Module 已创建的真实 Namespace / DAG 节点
        # -------------------------------------------------------------------------
        left_corner_ctrl_name = self.create_name(
            type="ctrl",
            side="lf",
            part="mouth_corner",
            function="bind",
            index=1
        )
        right_corner_ctrl_name = self.create_name(
            type="ctrl",
            side="rt",
            part="mouth_corner",
            function="bind",
            index=1
        )

        self.jaw_ctrl = self._resolve_scene_node(
            jaw_ctrl_name,
            label=u"Mouth Jaw Ctrl Dependency",
            node_type="transform"
        )
        self.jaw_output = self._resolve_scene_node(
            jaw_output_name,
            label=u"Mouth Jaw Output Dependency",
            node_type="transform"
        )
        self.left_corner_ctrl = self._resolve_scene_node(
            left_corner_ctrl_name,
            label=u"Mouth Left Corner Ctrl Dependency",
            node_type="transform"
        )
        self.right_corner_ctrl = self._resolve_scene_node(
            right_corner_ctrl_name,
            label=u"Mouth Right Corner Ctrl Dependency",
            node_type="transform"
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def load_guide(self):
        u"""

                读取 Mouth Corner 与 Upper / Lower Lip Guide。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

        """
        self.lip_guide_dict = self.face_guide.get_lip_guides(
            required=True
        )
        return self.lip_guide_dict

    def create_jnt(self):
        u"""

                解析并注册 LipModule 已创建的 Upper / Lower Deform Jnt。

                Returns:
                    list:
                        按当前 API 约定顺序返回的结果列表。

        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.upper_lip_jnts = []
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.lower_lip_jnts = []

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        index = 0
        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        while index < self.lip_jnt_count:
            item_index = index + 1
            upper_lip_jnt = self.create_name(
                type="jnt",
                side="md",
                part="upper_lip_deform",
                function="bind",
                index=item_index
            )
            lower_lip_jnt = self.create_name(
                type="jnt",
                side="md",
                part="lower_lip_deform",
                function="bind",
                index=item_index
            )
            upper_lip_jnt = self._resolve_scene_node(
                upper_lip_jnt,
                label=u"Upper Lip Deform Jnt",
                node_type="joint"
            )
            lower_lip_jnt = self._resolve_scene_node(
                lower_lip_jnt,
                label=u"Lower Lip Deform Jnt",
                node_type="joint"
            )
            self.upper_lip_jnts.append(upper_lip_jnt)
            self.lower_lip_jnts.append(lower_lip_jnt)
            index += 1

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return [
            self.upper_lip_jnts,
            self.lower_lip_jnts,
        ]

    def create_ctrl(self):
        u"""

                在嘴部中心创建 Mouth Main Controller。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        upper_guides = self.lip_guide_dict["upper"]
        lower_guides = self.lip_guide_dict["lower"]
        upper_center_guide = upper_guides[int(len(upper_guides) / 2)]
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        lower_center_guide = lower_guides[int(len(lower_guides) / 2)]

        mouth_main_ctrl_name = self.create_name(
            type="ctrl",
            side="md",
            part="mouth",
            function="main",
            index=1
        )
        self.mouth_main_ctrl_dict = ctrl_base.create_ctrl(
            name=mouth_main_ctrl_name,
            shape="circle",
            radius=self.controller_radius * 1.25,
            color=17,
            axis="Z+",
            target_node=upper_center_guide,
            parent_node=self.face_ctrl_grp,
            create_sub_ctrl=False,
            add_to_set=True,
            ctrl_set=config.face_ctrl_set
        )

        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        upper_position = snap_utils.get_item_world_position(
            upper_center_guide
        )
        lower_position = snap_utils.get_item_world_position(
            lower_center_guide
        )
        mouth_position = []
        # -------------------------------------------------------------------------
        # Step 04：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        axis_index = 0

        while axis_index < 3:
            mouth_position.append(
                (upper_position[axis_index] + lower_position[axis_index]) * 0.5
            )
            axis_index += 1

        transform_utils.set_world_translation(
            self.mouth_main_ctrl_dict["top_grp"],
            mouth_position
        )
        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return self.mouth_main_ctrl_dict

    def _get_existing_ctrl_dict(self, ctrl_name):
        u"""根据 CtrlBase 确定性层级恢复 create_follow() 所需的最小 Ctrl Dict。"""
        ctrl_leaf_name = str(ctrl_name).rsplit("|", 1)[-1]
        ctrl_canonical_name = ctrl_leaf_name.rsplit(":", 1)[-1]
        hierarchy_names = ctrl_base.get_ctrl_hierarchy_names(
            ctrl_canonical_name
        )
        ctrl_node = self._resolve_scene_node(
            ctrl_name,
            label=u"Mouth Existing Ctrl",
            node_type="transform"
        )
        zero_grp = self._resolve_scene_node(
            hierarchy_names["zero"],
            label=u"Mouth Existing Ctrl Zero",
            node_type="transform"
        )
        driven_grp = self._resolve_scene_node(
            hierarchy_names["driven"],
            label=u"Mouth Existing Ctrl Driven",
            node_type="transform"
        )

        return {
            "ctrl_node": ctrl_node,
            "grp_dict": {
                "zero": zero_grp,
                "driven": driven_grp,
            },
        }

    def create_connect(self):
        u"""

                创建 Jaw -> Mouth Main 与 Mouth Main -> Corner 的 Follow。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

        """
        self.mouth_follow_dict = ctrl_base.create_follow(
            driver_node=self.jaw_output,
            ctrl_dict=self.mouth_main_ctrl_dict,
            weight=0.5,
            attr_name="jaw_follow",
            maintain_offset=True
        )

        self.corner_follow_dict_list = []
        corner_ctrl_list = [
            self.left_corner_ctrl,
            self.right_corner_ctrl,
        ]

        for corner_ctrl in corner_ctrl_list:
            corner_ctrl_dict = self._get_existing_ctrl_dict(
                corner_ctrl
            )
            corner_follow_dict = ctrl_base.create_follow(
                driver_node=self.mouth_main_ctrl_dict["output_node"],
                ctrl_dict=corner_ctrl_dict,
                weight=0.5,
                attr_name="mouth_follow",
                maintain_offset=True
            )
            self.corner_follow_dict_list.append(
                corner_follow_dict
            )

        return {
            "mouth_follow": self.mouth_follow_dict,
            "corner_follow": self.corner_follow_dict_list,
        }

    def create_deform(self):
        u"""

                调用正式 Matrix Zip Lip Builder 创建上下嘴唇闭合系统。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        self.zip_lip_dict = build_zip_lip(
            upper_jnts=self.upper_lip_jnts,
            lower_jnts=self.lower_lip_jnts,
            left_zip_control=self.left_corner_ctrl,
            right_zip_control=self.right_corner_ctrl,
            jaw_control=self.jaw_ctrl,
            zip_height=0.5,
            falloff=3,
            utility_parent=self.face_rig_nodes_grp
        )
        return self.zip_lip_dict

    def create_finalize(self):
        u"""

                验证 Mouth Main / Zip Lip 关键输出。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        scene_utils.validate_node(
            self.mouth_main_ctrl_dict["ctrl_node"],
            label=u"Mouth Main Ctrl"
        )

        if not self.zip_lip_dict:
            raise RuntimeError(u"Mouth Zip Lip 没有完成构建。")

        # -------------------------------------------------------------------------
        # Step 01：Zip Lip Builder 可能重新组织 Jnt DAG，先刷新真实 Long Path
        # -------------------------------------------------------------------------
        resolved_upper_lip_jnts = []

        for upper_lip_jnt in self.upper_lip_jnts:
            resolved_upper_lip_jnt = self._resolve_scene_node(
                upper_lip_jnt,
                label=u"Upper Lip Jnt",
                node_type="joint"
            )
            resolved_upper_lip_jnts.append(
                resolved_upper_lip_jnt
            )

        resolved_lower_lip_jnts = []

        for lower_lip_jnt in self.lower_lip_jnts:
            resolved_lower_lip_jnt = self._resolve_scene_node(
                lower_lip_jnt,
                label=u"Lower Lip Jnt",
                node_type="joint"
            )
            resolved_lower_lip_jnts.append(
                resolved_lower_lip_jnt
            )

        self.upper_lip_jnts = resolved_upper_lip_jnts
        self.lower_lip_jnts = resolved_lower_lip_jnts

        # -------------------------------------------------------------------------
        # Step 02：使用刷新后的 Scene Node 验证最终 Mouth / Zip Lip 输出
        # -------------------------------------------------------------------------
        for upper_lip_jnt in self.upper_lip_jnts:
            scene_utils.validate_node(
                upper_lip_jnt,
                label=u"Upper Lip Jnt"
            )

        for lower_lip_jnt in self.lower_lip_jnts:
            scene_utils.validate_node(
                lower_lip_jnt,
                label=u"Lower Lip Jnt"
            )

        self.module_dict["mouth_main_ctrl_dict"] = self.mouth_main_ctrl_dict
        self.module_dict["upper_lip_jnts"] = self.upper_lip_jnts
        self.module_dict["lower_lip_jnts"] = self.lower_lip_jnts
        self.module_dict["zip_lip_dict"] = self.zip_lip_dict
        self.module_dict["built"] = True
        return True


def build_mouth():
    u"""

        构建 Mouth Module 并返回统一 Module Dict。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    mouth_module = MouthModule()
    mouth_module_dict = mouth_module.create_build()
    return mouth_module_dict


__all__ = [
    "MouthModule",
    "build_mouth",
]
