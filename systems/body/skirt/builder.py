# coding=utf-8
u"""
Skirt Rig Builder
=================

程序化裙子绑定系统。

工作流：
    1. 创建 Up / Down 两条定位曲线；
    2. 通过 pointOnCurveInfo 驱动 Blueprint Joint；
    3. 调整定位曲线贴合裙子；
    4. 根据横向和纵向数量创建 Bind Joint Chain；
    5. 统一调用 systems.ctrl_base 创建 FK Controller。

重要边界：
    - 外部名称 Token 统一复用 core.rename_utils；
    - 三维插值统一复用 core.math_utils；
    - Curve Shape 查询统一复用 core.curve_utils；
    - Group / Child / Parent 统一复用 core.hierarchy_utils；
    - 世界位置查询统一复用 core.transform_utils；
    - Joint 创建统一复用 core.joint_utils；
    - Attribute 创建统一复用 core.attr_utils；
    - DG Plug 连接统一复用 core.connection_utils；
    - Constraint 创建统一复用 core.constraint_utils；
    - Controller 创建统一复用 systems.ctrl_base；
    - Undo Chunk 统一复用 core.scene_utils；
    - 本模块只保留 Skirt Rig Workflow。

本模块不包含 PySide UI。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import attr_utils
from ....core import connection_utils
from ....core import constraint_utils
from ....core import curve_utils
from ....core import hierarchy_utils
from ....core import joint_utils
from ....core import math_utils
from ....core import rename_utils
from ....core import scene_utils
from ....core import transform_utils
from ... import ctrl_base


class SkirtRigBuilder(object):
    """裙子绑定系统 Builder。"""

    def __init__(
            self,
            name="skirt",
            horizontal_count=8,
            vertical_count=4
    ):
        u"""
        初始化裙子绑定系统参数。

        Args:
            name (str):
                创建或查询时使用的节点名称。
            horizontal_count (int):
                当前构建、采样或查询过程使用的元素数量。
            vertical_count (int):
                当前构建、采样或查询过程使用的元素数量。
        """
        self.name = rename_utils.get_name_token(
            name,
            fallback="skirt"
        )
        self.horizontal_count = int(horizontal_count)
        self.vertical_count = int(vertical_count)
        self.validate_parameters()

    # -------------------------------------------------------------------------
    # Config
    # -------------------------------------------------------------------------

    def validate_parameters(self):
        u"""

                检查 Builder 参数。

                Returns:
                    bool:
                        当前操作成功或目标状态满足要求时返回 True，否则返回 False。

                Raises:
                    ValueError:
                        输入数据、场景状态或操作条件不满足要求时抛出。

        """
        if self.horizontal_count < 3:
            raise ValueError(
                u"裙子横向链数量不能小于 3。"
            )

        if self.vertical_count < 2:
            raise ValueError(
                u"裙子纵向关节数量不能小于 2。"
            )

        return True

    def get_names(self):
        u"""

                返回系统内所有固定节点名称。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

        """
        return {
            "name": self.name,
            "root": "grp_m_{}_001".format(self.name),
            "setup": "grp_m_{}Setup_001".format(self.name),
            "blueprint": "grp_m_{}Bpjnts_001".format(self.name),
            "controls": "grp_m_{}Ctrls_001".format(self.name),
            "joints": "grp_m_{}Jnts_001".format(self.name),
            "nodes": "grp_m_{}Nodes_001".format(self.name),
            "build": "grp_m_{}RigBuild_001".format(self.name),
            "up_curve": "crv_m_{}Up_001".format(self.name),
            "down_curve": "crv_m_{}Down_001".format(self.name),
        }

    # -------------------------------------------------------------------------
    # Hierarchy
    # -------------------------------------------------------------------------

    def ensure_root_groups(self):
        u"""

                确保裙子系统基础层级存在。

                Returns:
                    object:
                        当前 API 完成处理后返回的结果。

        """
        names = self.get_names()
        root = hierarchy_utils.ensure_group(
            names["root"]
        )

        child_group_keys = [
            "setup",
            "blueprint",
            "controls",
            "joints",
            "nodes",
        ]

        for group_key in child_group_keys:
            hierarchy_utils.ensure_group(
                names[group_key],
                parent_node=root
            )

        return names

    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------

    def _delete_setup_nodes(self, names):
        """删除旧定位和 Blueprint 节点。"""
        # -------------------------------------------------------------------------
        # Step 01：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        delete_nodes = []

        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        group_keys = [
            "setup",
            "blueprint",
        ]

        for group_key in group_keys:
            group = names[group_key]

            if not cmds.objExists(group):
                continue

            children = hierarchy_utils.get_children(
                group,
                full_path=True
            )

            for child in children:
                if child not in delete_nodes:
                    delete_nodes.append(
                        child
                    )

        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        poci_nodes = cmds.ls(
            "poci_m_{}_*".format(self.name),
            type="pointOnCurveInfo"
        )

        if poci_nodes is None:
            poci_nodes = []

        # -------------------------------------------------------------------------
        # Step 04：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        for node in poci_nodes:
            if node not in delete_nodes:
                delete_nodes.append(
                    node
                )

        # -------------------------------------------------------------------------
        # Step 05：检查当前条件与边界情况，并进入对应处理分支
        # -------------------------------------------------------------------------
        if delete_nodes:
            cmds.delete(
                delete_nodes
            )

    def _create_setup_curve(
            self,
            name,
            y_value,
            radius,
            parent
    ):
        """创建一条定位环线。"""
        curve = cmds.circle(
            name=name,
            center=(0.0, y_value, 0.0),
            normal=(0.0, 1.0, 0.0),
            radius=radius,
            degree=3,
            sections=max(self.horizontal_count, 4),
            constructionHistory=False
        )[0]

        curve = hierarchy_utils.parent(
            curve,
            parent
        )

        return curve

    def _create_curve_blueprints(
            self,
            curve,
            place,
            names
    ):
        """在定位曲线上创建实时 Blueprint Joint。"""
        # -------------------------------------------------------------------------
        # Step 01：查询并整理当前阶段需要的 Maya 场景数据
        # -------------------------------------------------------------------------
        curve_shape = curve_utils.get_curve_shape(
            curve
        )
        # -------------------------------------------------------------------------
        # Step 02：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        index = 0

        # -------------------------------------------------------------------------
        # Step 03：遍历当前数据集合，并逐项执行核心处理
        # -------------------------------------------------------------------------
        while index < self.horizontal_count:
            point_group_name = "grp_m_{}{}Point_{:03d}".format(
                self.name,
                place,
                index + 1
            )

            point_group = scene_utils.create_node(
                "transform",
                point_group_name,
                parent=names["blueprint"]
            )

            poci_name = "poci_m_{}{}_{:03d}".format(
                self.name,
                place,
                index + 1
            )
            poci = scene_utils.create_node(
                "pointOnCurveInfo",
                poci_name
            )

            connection_utils.connect_plugs(
                curve_shape + ".worldSpace[0]",
                poci + ".inputCurve",
                force=True
            )

            cmds.setAttr(
                poci + ".turnOnPercentage",
                1
            )
            cmds.setAttr(
                poci + ".parameter",
                float(index) / float(self.horizontal_count)
            )

            connection_utils.connect_plugs(
                poci + ".position",
                point_group + ".translate",
                force=True
            )

            joint_name = "bpjnt_m_{}{}_hor{:03d}_001".format(
                self.name,
                place,
                index + 1
            )

            joint_utils.Joint.create(
                name=joint_name,
                parent=point_group,
                radius=0.25
            )

            index += 1

    @scene_utils.undo_chunk
    def create_setup(self):
        u"""

                创建或重建裙子定位系统。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

        """
        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.validate_parameters()
        names = self.ensure_root_groups()
        # -------------------------------------------------------------------------
        # Step 02：应用并更新当前阶段需要的属性或状态
        # -------------------------------------------------------------------------
        self._delete_setup_nodes(
            names
        )

        up_curve = self._create_setup_curve(
            names["up_curve"],
            y_value=5.0,
            radius=2.0,
            parent=names["setup"]
        )
        # -------------------------------------------------------------------------
        # Step 03：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        down_curve = self._create_setup_curve(
            names["down_curve"],
            y_value=0.0,
            radius=3.0,
            parent=names["setup"]
        )

        self._create_curve_blueprints(
            up_curve,
            "Up",
            names
        )
        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self._create_curve_blueprints(
            down_curve,
            "Down",
            names
        )

        cmds.select(
            [up_curve, down_curve],
            replace=True
        )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return {
            "up_curve": up_curve,
            "down_curve": down_curve,
            "names": names,
        }

    def select_setup_curves(self):
        u"""

                选择当前裙子系统的两条定位曲线。

                Returns:
                    object | list:
                        按当前 API 约定顺序返回的结果列表。

        """
        names = self.get_names()
        curves = []

        curve_keys = [
            "up_curve",
            "down_curve",
        ]

        for curve_key in curve_keys:
            curve = names[curve_key]

            if cmds.objExists(curve):
                curves.append(
                    curve
                )

        if not curves:
            cmds.warning(
                u"尚未生成定位曲线。"
            )
            return []

        cmds.select(
            curves,
            replace=True
        )

        return curves

    # -------------------------------------------------------------------------
    # Build
    # -------------------------------------------------------------------------

    def _delete_previous_build(self, names):
        """删除之前生成的绑定结果。"""
        if cmds.objExists(names["build"]):
            cmds.delete(
                names["build"]
            )

        group_keys = [
            "controls",
            "joints",
        ]

        for group_key in group_keys:
            group = names[group_key]

            if not cmds.objExists(group):
                continue

            children = hierarchy_utils.get_children(
                group,
                full_path=True
            )

            if children:
                cmds.delete(
                    children
                )

    def _validate_blueprints(self, names):
        """检查所有上下 Blueprint Joint 是否存在。"""
        missing = []
        horizontal_index = 0

        while horizontal_index < self.horizontal_count:
            up_joint = "bpjnt_m_{}Up_hor{:03d}_001".format(
                self.name,
                horizontal_index + 1
            )
            down_joint = "bpjnt_m_{}Down_hor{:03d}_001".format(
                self.name,
                horizontal_index + 1
            )

            if not cmds.objExists(up_joint):
                missing.append(
                    up_joint
                )

            if not cmds.objExists(down_joint):
                missing.append(
                    down_joint
                )

            horizontal_index += 1

        if missing:
            raise RuntimeError(
                u"定位数据不完整，请先重新生成定位。"
            )

        return True

    @scene_utils.undo_chunk
    def build(self):
        u"""

                根据当前 Blueprint 创建完整裙子 FK 绑定。

                Returns:
                    dict:
                        包含本次构建、查询或处理结果的结构化字典。

        """
        # -------------------------------------------------------------------------
        # Step 01：验证并规范化当前阶段需要的输入数据
        # -------------------------------------------------------------------------
        self.validate_parameters()
        names = self.ensure_root_groups()
        self._validate_blueprints(
            names
        )
        # -------------------------------------------------------------------------
        # Step 02：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        self._delete_previous_build(
            names
        )

        build_group = scene_utils.create_node(
            "transform",
            names["build"],
            parent=names["root"]
        )

        created_controls = []
        created_joints = []
        # -------------------------------------------------------------------------
        # Step 03：准备当前阶段计算和后续处理需要的数据
        # -------------------------------------------------------------------------
        horizontal_index = 0

        while horizontal_index < self.horizontal_count:
            up_joint = "bpjnt_m_{}Up_hor{:03d}_001".format(
                self.name,
                horizontal_index + 1
            )
            down_joint = "bpjnt_m_{}Down_hor{:03d}_001".format(
                self.name,
                horizontal_index + 1
            )

            up_position = transform_utils.get_world_translation(
                up_joint
            )
            down_position = transform_utils.get_world_translation(
                down_joint
            )

            previous_joint = None
            previous_control = None
            vertical_index = 0

            while vertical_index < self.vertical_count:
                ratio = float(vertical_index) / float(
                    self.vertical_count - 1
                )

                position = math_utils.lerp_point3(
                    up_position,
                    down_position,
                    ratio
                )

                joint_name = "jnt_m_{}_hor{:03d}_ver{:03d}".format(
                    self.name,
                    horizontal_index + 1,
                    vertical_index + 1
                )

                joint_parent = names["joints"]

                if previous_joint is not None:
                    joint_parent = previous_joint

                joint = joint_utils.Joint.create(
                    name=joint_name,
                    position=position,
                    parent=joint_parent
                )

                control_name = "ctrl_m_{}_hor{:03d}_ver{:03d}".format(
                    self.name,
                    horizontal_index + 1,
                    vertical_index + 1
                )

                parent_control = names["controls"]

                if previous_control is not None:
                    parent_control = previous_control

                control_result = ctrl_base.create_ctrl(
                    name=control_name,
                    shape="circle",
                    radius=0.6,
                    axis="Y+",
                    target_node=joint,
                    parent_node=parent_control,
                    color=17,
                    create_sub_ctrl=False,
                    add_to_set=True
                )

                control = control_result["ctrl_node"]

                constraint_utils.create_constraint(
                    driver_objects=control,
                    driven_object=joint,
                    constraint_type="parentConstraint",
                    maintain_offset=False
                )

                created_controls.append(
                    control
                )
                created_joints.append(
                    joint
                )
                previous_joint = joint
                previous_control = control
                vertical_index += 1

            horizontal_index += 1

        build_attr = attr_utils.Attr(
            build_group
        )
        # -------------------------------------------------------------------------
        # Step 04：创建并配置当前阶段需要的 Maya / Rig 对象
        # -------------------------------------------------------------------------
        build_attr.add_attr(
            "horizontalCount",
            attr_type="long",
            lock=False,
            hide=True,
            default_value=self.horizontal_count
        )
        build_attr.add_attr(
            "verticalCount",
            attr_type="long",
            lock=False,
            hide=True,
            default_value=self.vertical_count
        )

        if created_controls:
            cmds.select(
                created_controls,
                replace=True
            )

        # -------------------------------------------------------------------------
        # Step 05：整理并返回当前函数的最终结果
        # -------------------------------------------------------------------------
        return {
            "group": build_group,
            "controls": created_controls,
            "joints": created_joints,
            "names": names,
        }


__all__ = [
    "SkirtRigBuilder",
]
