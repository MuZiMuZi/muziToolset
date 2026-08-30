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
    5. 统一调用 systems.controller 创建 FK Controller。

重要边界：
    - Group 创建和 Parent 统一复用 core.hierarchy_utils；
    - 世界位置查询统一复用 core.transform_utils；
    - Joint 创建统一复用 core.joint_utils；
    - DG Plug 连接统一复用 core.connection_utils；
    - Constraint 创建统一复用 core.constraint_utils；
    - Undo Chunk 统一复用 core.scene_utils；
    - 本模块只保留 Skirt Rig Workflow。

本模块不包含 PySide UI。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import connection_utils
from ....core import constraint_utils
from ....core import hierarchy_utils
from ....core import joint_utils
from ....core import scene_utils
from ....core import transform_utils
from ... import controller as controller_system


def _safe_name(text):
    """整理裙子系统名称。"""
    result = text.strip()
    result = result.replace(" ", "_")
    result = result.replace(":", "_")

    if not result:
        result = "skirt"

    return result


def _lerp(start_value, end_value, ratio):
    """三维位置线性插值。"""
    result = []
    axis_index = 0

    while axis_index < 3:
        value = start_value[axis_index] + (
            end_value[axis_index] - start_value[axis_index]
        ) * ratio
        result.append(value)
        axis_index += 1

    return result


class SkirtRigBuilder(object):
    """裙子绑定系统 Builder。"""

    def __init__(
            self,
            name="skirt",
            horizontal_count=8,
            vertical_count=4
    ):
        u"""初始化裙子绑定系统参数。"""
        self.name = _safe_name(name)
        self.horizontal_count = int(horizontal_count)
        self.vertical_count = int(vertical_count)

        # 初始化后立即验证数量参数，避免无效配置进入后续 Setup / Build。
        self.validate_parameters()

    # -------------------------------------------------------------------------
    # Config
    # -------------------------------------------------------------------------

    def validate_parameters(self):
        u"""检查 Builder 参数。"""
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
        u"""返回系统内所有固定节点名称。"""
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
        u"""确保裙子系统基础层级存在。"""
        # 生成当前 Skirt System 使用的固定节点名称。
        names = self.get_names()

        # 创建或复用裙子系统顶层 Group。
        root = hierarchy_utils.Hierarchy.create_grp(
            names["root"]
        )

        child_group_keys = [
            "setup",
            "blueprint",
            "controls",
            "joints",
            "nodes",
        ]

        # 创建或复用 Setup / Blueprint / Control / Joint / Node 子组。
        for group_key in child_group_keys:
            hierarchy_utils.Hierarchy.create_grp(
                names[group_key],
                parent=root
            )

        return names

    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------

    def _delete_setup_nodes(self, names):
        """删除旧定位和 Blueprint 节点。"""
        delete_nodes = []

        group_keys = [
            "setup",
            "blueprint",
        ]

        for group_key in group_keys:
            group = names[group_key]

            if not cmds.objExists(group):
                continue

            children = cmds.listRelatives(
                group,
                children=True,
                fullPath=True
            )

            if children is None:
                children = []

            for child in children:
                if child not in delete_nodes:
                    delete_nodes.append(child)

        poci_nodes = cmds.ls(
            "poci_m_{}_*".format(self.name),
            type="pointOnCurveInfo"
        )

        if poci_nodes is None:
            poci_nodes = []

        for node in poci_nodes:
            if node not in delete_nodes:
                delete_nodes.append(node)

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

        # 使用统一 Hierarchy API 把定位曲线整理到 Setup Group。
        hierarchy_utils.Hierarchy.parent(
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
        curve_shapes = cmds.listRelatives(
            curve,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="nurbsCurve"
        )

        if curve_shapes is None:
            curve_shapes = []

        if not curve_shapes:
            raise RuntimeError(
                u"定位曲线没有 nurbsCurve Shape：{}".format(curve)
            )

        curve_shape = curve_shapes[0]
        index = 0

        while index < self.horizontal_count:
            point_group_name = "grp_m_{}{}Point_{:03d}".format(
                self.name,
                place,
                index + 1
            )

            # 使用 Scene Core 创建 Blueprint Point Group，并直接放入 Blueprint 层级。
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

            # 创建 pointOnCurveInfo，作为定位曲线到 Blueprint Point 的实时采样节点。
            poci = scene_utils.create_node(
                "pointOnCurveInfo",
                poci_name
            )

            # 把 Curve WorldSpace 输出接入 pointOnCurveInfo 输入。
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

            # 用 pointOnCurveInfo 的 Position 实时驱动 Blueprint Point Group。
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

            # 使用统一 Joint API 在 Point Group 下创建 Blueprint Joint。
            joint_utils.Joint.create(
                name=joint_name,
                parent=point_group,
                radius=0.25
            )

            index += 1

    @scene_utils.undo_chunk
    def create_setup(self):
        u"""创建或重建裙子定位系统。"""
        # 检查横向 / 纵向数量，避免使用无效参数创建 Setup。
        self.validate_parameters()

        # 创建或复用 Skirt Rig 的基础层级，并取得本次需要的固定名称。
        names = self.ensure_root_groups()

        # 删除上一次 Setup 创建的 Curve、Blueprint 和 POCI，保证本次从干净状态开始。
        self._delete_setup_nodes(
            names
        )

        # 创建上方定位环线，作为裙子腰部采样边界。
        up_curve = self._create_setup_curve(
            names["up_curve"],
            y_value=5.0,
            radius=2.0,
            parent=names["setup"]
        )

        # 创建下方定位环线，作为裙摆采样边界。
        down_curve = self._create_setup_curve(
            names["down_curve"],
            y_value=0.0,
            radius=3.0,
            parent=names["setup"]
        )

        # 根据上方定位曲线创建实时 Up Blueprint Joint。
        self._create_curve_blueprints(
            up_curve,
            "Up",
            names
        )

        # 根据下方定位曲线创建实时 Down Blueprint Joint。
        self._create_curve_blueprints(
            down_curve,
            "Down",
            names
        )

        cmds.select(
            [up_curve, down_curve],
            replace=True
        )

        return {
            "up_curve": up_curve,
            "down_curve": down_curve,
            "names": names,
        }

    def select_setup_curves(self):
        u"""选择当前裙子系统的两条定位曲线。"""
        # 获取当前 Skirt System 的固定 Curve 名称。
        names = self.get_names()
        curves = []

        curve_keys = [
            "up_curve",
            "down_curve",
        ]

        for curve_key in curve_keys:
            curve = names[curve_key]

            if cmds.objExists(curve):
                curves.append(curve)

        if not curves:
            cmds.warning(u"尚未生成定位曲线。")
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

            children = cmds.listRelatives(
                group,
                children=True,
                fullPath=True
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
                missing.append(up_joint)

            if not cmds.objExists(down_joint):
                missing.append(down_joint)

            horizontal_index += 1

        if missing:
            raise RuntimeError(
                u"定位数据不完整，请先重新生成定位。"
            )

        return True

    @scene_utils.undo_chunk
    def build(self):
        u"""根据当前 Blueprint 创建完整裙子 FK 绑定。"""
        # 检查 Builder 数量参数，保证 Joint Chain 可以正常插值。
        self.validate_parameters()

        # 创建或复用基础层级，并取得当前 Skirt System 的全部固定名称。
        names = self.ensure_root_groups()

        # 确认所有 Up / Down Blueprint Joint 都存在，避免构建出残缺 Joint Chain。
        self._validate_blueprints(
            names
        )

        # 删除上一次生成的 Joint / Controller / Build Metadata，保证 Build 可重复执行。
        self._delete_previous_build(
            names
        )

        # 创建本次 Build 的 Metadata Group，用于保存构建参数。
        build_group = scene_utils.create_node(
            "transform",
            names["build"],
            parent=names["root"]
        )

        created_controls = []
        created_joints = []
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

            # 使用 Transform Core 读取当前纵向链的上端 Blueprint 世界位置。
            up_position = transform_utils.get_world_translation(
                up_joint
            )

            # 使用 Transform Core 读取当前纵向链的下端 Blueprint 世界位置。
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

                position = _lerp(
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

                # 使用统一 Joint API 在上下 Blueprint 之间创建当前 Bind Joint。
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

                # 使用统一 Controller System 创建当前 Joint 对应的 FK Controller。
                control_result = controller_system.create_controller(
                    name=control_name,
                    shape="circle",
                    radius=0.6,
                    axis="Y+",
                    target=joint,
                    parent=parent_control,
                    color=17,
                    create_sub_control=False,
                    create_extra_groups=True,
                    add_to_set=True
                )

                control = control_result["control"]

                # 使用统一 Constraint Core 建立 Controller 到 Joint 的 Parent Constraint。
                constraint_utils.create_constraint(
                    driver_objects=control,
                    driven_object=joint,
                    constraint_type="parentConstraint",
                    maintain_offset=False
                )

                created_controls.append(control)
                created_joints.append(joint)
                previous_joint = joint
                previous_control = control
                vertical_index += 1

            horizontal_index += 1

        cmds.addAttr(
            build_group,
            longName="horizontalCount",
            attributeType="long",
            defaultValue=self.horizontal_count
        )
        cmds.addAttr(
            build_group,
            longName="verticalCount",
            attributeType="long",
            defaultValue=self.vertical_count
        )

        if created_controls:
            cmds.select(
                created_controls,
                replace=True
            )

        return {
            "group": build_group,
            "controls": created_controls,
            "joints": created_joints,
            "names": names,
        }


__all__ = [
    "SkirtRigBuilder",
]
