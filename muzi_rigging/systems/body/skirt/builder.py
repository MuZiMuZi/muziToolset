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

本模块不包含 PySide UI。
"""

from __future__ import print_function

import maya.cmds as cmds

from ... import controller as controller_system


def _safe_name(text):
    """整理裙子系统名称。"""
    result = text.strip()
    result = result.replace(" ", "_")
    result = result.replace(":", "_")

    if not result:
        result = "skirt"

    return result


def _ensure_group(name, parent=None):
    """确保 Transform Group 存在。"""
    if cmds.objExists(name):
        return name

    group = cmds.createNode(
        "transform",
        name=name
    )

    if parent is not None:
        cmds.parent(
            group,
            parent
        )

    return group


def _world_position(node):
    """返回节点世界空间位置。"""
    return cmds.xform(
        node,
        query=True,
        worldSpace=True,
        translation=True
    )


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
        self.name = _safe_name(name)
        self.horizontal_count = int(horizontal_count)
        self.vertical_count = int(vertical_count)

        self.validate_parameters()

    # -------------------------------------------------------------------------
    # Config
    # -------------------------------------------------------------------------

    def validate_parameters(self):
        """检查 Builder 参数。"""
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
        """返回系统内所有固定节点名称。"""
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
        """确保裙子系统基础层级存在。"""
        names = self.get_names()

        root = _ensure_group(
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
            _ensure_group(
                names[group_key],
                root
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
            cmds.delete(delete_nodes)

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

        cmds.parent(
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
            point_group = cmds.createNode(
                "transform",
                name="grp_m_{}{}Point_{:03d}".format(
                    self.name,
                    place,
                    index + 1
                ),
                parent=names["blueprint"]
            )

            poci = cmds.createNode(
                "pointOnCurveInfo",
                name="poci_m_{}{}_{:03d}".format(
                    self.name,
                    place,
                    index + 1
                )
            )

            cmds.connectAttr(
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
            cmds.connectAttr(
                poci + ".position",
                point_group + ".translate",
                force=True
            )

            joint = cmds.createNode(
                "joint",
                name="bpjnt_m_{}{}_hor{:03d}_001".format(
                    self.name,
                    place,
                    index + 1
                ),
                parent=point_group
            )
            cmds.setAttr(
                joint + ".radius",
                0.25
            )

            index += 1

    def create_setup(self):
        """创建或重建裙子定位系统。"""
        self.validate_parameters()

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziSkirtSetup"
        )

        try:
            names = self.ensure_root_groups()
            self._delete_setup_nodes(names)

            up_curve = self._create_setup_curve(
                names["up_curve"],
                y_value=5.0,
                radius=2.0,
                parent=names["setup"]
            )
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

        finally:
            cmds.undoInfo(closeChunk=True)

    def select_setup_curves(self):
        """选择当前裙子系统的两条定位曲线。"""
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
            cmds.delete(names["build"])

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
                cmds.delete(children)

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

    def build(self):
        """根据当前 Blueprint 创建完整裙子 FK 绑定。"""
        self.validate_parameters()
        names = self.ensure_root_groups()
        self._validate_blueprints(names)

        cmds.undoInfo(
            openChunk=True,
            chunkName="MuziBuildSkirtRig"
        )

        try:
            self._delete_previous_build(names)

            build_group = cmds.createNode(
                "transform",
                name=names["build"],
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

                up_position = _world_position(up_joint)
                down_position = _world_position(down_joint)

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
                    joint = cmds.createNode(
                        "joint",
                        name=joint_name
                    )
                    cmds.xform(
                        joint,
                        worldSpace=True,
                        translation=position
                    )

                    if previous_joint is None:
                        cmds.parent(
                            joint,
                            names["joints"]
                        )
                    else:
                        cmds.parent(
                            joint,
                            previous_joint
                        )

                    control_name = "ctrl_m_{}_hor{:03d}_ver{:03d}".format(
                        self.name,
                        horizontal_index + 1,
                        vertical_index + 1
                    )

                    parent_control = names["controls"]

                    if previous_control is not None:
                        parent_control = previous_control

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

                    cmds.parentConstraint(
                        control,
                        joint,
                        maintainOffset=False
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

        finally:
            cmds.undoInfo(closeChunk=True)


__all__ = [
    "SkirtRigBuilder",
]
