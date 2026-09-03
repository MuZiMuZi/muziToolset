# coding=utf-8
u"""
Tongue Module
=============

舌头 FK Chain 绑定模块。

保留旧 Tongue 的两个核心逻辑：
    - FK Joint / Controller Chain；
    - 第一根 Controller 上的 tongue_curl 一键弯曲。

新版本直接读取 Face Guide，并可把 Step01 指定的 Tongue Model 绑定到生成的 Joint Chain。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import attr_utils
from ....core import connection_utils
from ....core import joint_utils
from ....core import matrix_utils
from ....core import scene_utils
from ....core import skin_utils
from ... import ctrl_base
from .. import config
from ..guide import FaceGuide
from .face_module_base import FaceModuleBase


class TongueModule(FaceModuleBase):
    u"""构建 Tongue FK Chain、Curl Driver 和可选 SkinCluster。"""

    def __init__(self):
        u"""

                初始化当前对象，并准备运行时需要的状态和成员。

        """

        super(TongueModule, self).__init__(
            side="md",
            part="tongue",
            index=1
        )
        self.face_guide = FaceGuide()
        self.controller_global_scale = 1.0
        self.controller_size = 1.0
        self.controller_radius = 1.0
        self.controller_color = 17

        self.tongue_guides = []
        self.tongue_jnts = []
        self.tongue_ctrl_dict_list = []
        self.tongue_matrix_nodes = []
        self.tongue_curl_nodes = []
        self.tongue_skin_cluster = None

    def load_setup(self):
        u"""

                读取 Tongue Controller Settings 与 Tongue Model。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    ValueError:
                        输入数据、场景状态或操作条件不满足要求时抛出。
                    RuntimeError:
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
            config.face_controller_size_attr_names["tongue"],
            1.0
        )
        # -------------------------------------------------------------------------
        # Step 03：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        self.controller_color = controller_settings.get(
            config.face_controller_color_attr_names["md"],
            17
        )
        self.controller_radius = (
            float(self.controller_global_scale) *
            float(self.controller_size)
        )

        # -------------------------------------------------------------------------
        # Step 04：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if self.controller_radius <= 0.0:
            raise ValueError(u"Tongue Controller Radius 必须大于 0。")

        if self.face_tongue_model:
            scene_utils.validate_node(
                self.face_tongue_model,
                label=u"Tongue Model"
            )
            existing_skin = skin_utils.find_skin_cluster(
                self.face_tongue_model
            )
            if existing_skin:
                raise RuntimeError(
                    u"Tongue Model 已存在 SkinCluster：{}".format(existing_skin)
                )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return True

    def load_guide(self):
        u"""

                读取中线 Tongue Guide。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        self.tongue_guides = self.face_guide.get_part_guides(
            part="tongue",
            side="md",
            required=True
        )

        if not self.tongue_guides:
            raise RuntimeError(u"Face Guide 中没有 Tongue Guide。")

        return self.tongue_guides

    def create_jnt(self):
        u"""

                按 Tongue Guide 顺序创建 FK Joint Chain。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        self.tongue_jnts = []
        jnt_parent = self.face_jnt_grp
        index = 0

        while index < len(self.tongue_guides):
            item_index = index + 1
            tongue_jnt_name = self.create_name(
                type="jnt",
                side="md",
                part="tongue",
                function="bind",
                index=item_index
            )
            scene_utils.ensure_nodes_available(
                tongue_jnt_name,
                label=u"Tongue Joint"
            )
            tongue_jnt = joint_utils.Joint.create_at_object(
                obj=self.tongue_guides[index],
                name=tongue_jnt_name,
                parent=jnt_parent,
                match_rotation=True,
                radius=self.controller_radius * 0.22
            )
            self.tongue_jnts.append(tongue_jnt)
            jnt_parent = tongue_jnt
            index += 1

        return self.tongue_jnts

    def create_ctrl(self):
        u"""

                创建与 Tongue Joint 一一对应的 FK Controller Chain。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        self.tongue_ctrl_dict_list = []
        ctrl_parent = self.face_ctrl_grp
        index = 0

        while index < len(self.tongue_jnts):
            item_index = index + 1
            tongue_ctrl_name = self.create_name(
                type="ctrl",
                side="md",
                part="tongue",
                function="fk",
                index=item_index
            )
            tongue_ctrl_dict = ctrl_base.create_ctrl(
                name=tongue_ctrl_name,
                shape="circle",
                radius=self.controller_radius,
                color=self.controller_color,
                axis="X+",
                target_node=self.tongue_jnts[index],
                parent_node=ctrl_parent,
                create_sub_ctrl=False,
                add_to_set=True,
                ctrl_set=config.face_ctrl_set
            )
            self.tongue_ctrl_dict_list.append(tongue_ctrl_dict)
            ctrl_parent = tongue_ctrl_dict["output_node"]
            index += 1

        return self.tongue_ctrl_dict_list

    def create_connect(self):
        u"""

                Tongue FK Ctrl Output 一一驱动对应 Joint。

                Returns:
                    object:
                        创建或构建完成后的 Maya / Rig 对象或 Build Result。

        """
        self.tongue_matrix_nodes = []
        index = 0

        while index < len(self.tongue_jnts):
            item_index = index + 1
            tongue_matrix_name = self.create_name(
                type="mult",
                side="md",
                part="tongue",
                function="parent",
                index=item_index
            )
            tongue_matrix_node = matrix_utils.create_parent_matrix_constraint(
                driver=self.tongue_ctrl_dict_list[index]["output_node"],
                driven=self.tongue_jnts[index],
                maintain_offset=False,
                name=tongue_matrix_name
            )
            self.tongue_matrix_nodes.append(tongue_matrix_node)
            index += 1

        return self.tongue_matrix_nodes

    def create_deform(self):
        u"""

                创建 Tongue Curl，并对可选 Tongue Model 建立 SkinCluster。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

                Raises:
                    RuntimeError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        # -------------------------------------------------------------------------
        # Step 01：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if not self.tongue_ctrl_dict_list:
            raise RuntimeError(u"Tongue Controller 尚未创建。")

        root_ctrl = self.tongue_ctrl_dict_list[0]["ctrl_node"]
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        root_ctrl_attr = attr_utils.Attr(
            root_ctrl
        )
        tongue_curl_plug = root_ctrl_attr.add_attr(
            "tongue_curl",
            attr_type="double",
            lock=False,
            hide=False,
            default_value=0.0,
            min_value=-10.0,
            max_value=10.0,
            keyable=True,
            channel_box=True
        )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        self.tongue_curl_nodes = []
        index = 1

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        while index < len(self.tongue_ctrl_dict_list):
            if index == len(self.tongue_ctrl_dict_list) - 1:
                break

            item_index = index + 1
            tongue_curl_mult_name = self.create_name(
                type="mult",
                side="md",
                part="tongue_curl",
                function="driver",
                index=item_index
            )
            tongue_curl_mult = cmds.createNode(
                "multDoubleLinear",
                name=tongue_curl_mult_name
            )
            cmds.setAttr(
                tongue_curl_mult + ".input1",
                10.0
            )
            connection_utils.connect_plugs(
                tongue_curl_plug,
                tongue_curl_mult + ".input2",
                force=True
            )
            connection_utils.connect_plugs(
                tongue_curl_mult + ".output",
                self.tongue_ctrl_dict_list[index]["grp_dict"]["connect"] + ".rotateY",
                force=True
            )
            self.tongue_curl_nodes.append(tongue_curl_mult)
            index += 1

        if self.face_tongue_model:
            tongue_skin_name = self.create_name(
                type="skin",
                side="md",
                part="tongue",
                function="bind",
                index=1
            )
            skin_result = cmds.skinCluster(
                self.tongue_jnts,
                self.face_tongue_model,
                name=tongue_skin_name,
                toSelectedBones=True,
                bindMethod=0,
                skinMethod=0,
                normalizeWeights=1
            )
            self.tongue_skin_cluster = skin_result[0]

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return {
            "curl_nodes": self.tongue_curl_nodes,
            "skin_cluster": self.tongue_skin_cluster,
        }

    def create_finalize(self):
        u"""

                验证 Tongue FK Rig、Curl 与可选 SkinCluster。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

        """
        for tongue_jnt in self.tongue_jnts:
            scene_utils.validate_node(
                tongue_jnt,
                label=u"Tongue Joint"
            )

        for tongue_ctrl_dict in self.tongue_ctrl_dict_list:
            scene_utils.validate_node(
                tongue_ctrl_dict["ctrl_node"],
                label=u"Tongue Ctrl"
            )

        for tongue_matrix_node in self.tongue_matrix_nodes:
            scene_utils.validate_node(
                tongue_matrix_node,
                label=u"Tongue Matrix"
            )

        if self.face_tongue_model:
            scene_utils.validate_node(
                self.tongue_skin_cluster,
                label=u"Tongue SkinCluster"
            )

        self.module_dict["jnts"] = self.tongue_jnts
        self.module_dict["ctrl_dict_list"] = self.tongue_ctrl_dict_list
        self.module_dict["matrix_nodes"] = self.tongue_matrix_nodes
        self.module_dict["curl_nodes"] = self.tongue_curl_nodes
        self.module_dict["skin_cluster"] = self.tongue_skin_cluster
        self.module_dict["built"] = True
        return True


def build_tongue():
    u"""

        构建 Tongue Module 并返回统一 Module Dict。

        Returns:
            object:
                创建或构建完成后的 Maya / Rig 对象或 Build Result。

    """
    tongue_module = TongueModule()
    tongue_module_dict = tongue_module.create_build()
    return tongue_module_dict


__all__ = [
    "TongueModule",
    "build_tongue",
]
