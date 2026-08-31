# coding=utf-8
u"""
Joint Utils
===========

Maya 单个 Joint 节点的专属底层能力模块。

设计原则
--------
Joint 类只负责“Joint 节点自己特有的能力”：

    - 创建 Joint；
    - Joint Orient；
    - Radius / Local Rotation Axis；
    - Segment Scale Compensate；
    - 单 Joint Orient；
    - Maya Joint Label。

通用能力不在本类重复包装：

    - 名称 / Rename        -> rename_utils
    - World Transform      -> transform_utils
    - DAG Parent / Child   -> hierarchy_utils

Joint 实例在 __init__() 时只验证一次节点存在性和节点类型。
初始化成功后，普通方法默认 self.joint 仍然是有效 Joint，
不为每一次操作重复执行存在性和类型检查。

本模块明确不负责：

    - Selection / 全场景批处理；
    - Vertex / Edge / CV 创建 Joint；
    - Curve -> Joint；
    - Joint Chain；
    - Duplicate Chain / Orient Chain；
    - FK / IK；
    - Face / Body 等具体 Rig Component。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import hierarchy_utils
from . import rename_utils
from . import transform_utils


class Joint(object):
    u"""单个 Maya Joint 节点的专属操作对象。"""

    def __init__(self, joint):
        if joint is None:
            raise RuntimeError(
                u"Joint 节点不能为空。"
            )

        joint = str(joint).strip()

        if not joint:
            raise RuntimeError(
                u"Joint 节点不能为空。"
            )

        if not cmds.objExists(joint):
            raise RuntimeError(
                u"Joint 节点不存在：{}".format(
                    joint
                )
            )

        node_type = cmds.nodeType(
            joint
        )

        if node_type != "joint":
            raise RuntimeError(
                u"节点不是 Joint：{} | type={}".format(
                    joint,
                    node_type
                )
            )

        self.joint = joint

    # =========================================================================
    # Create
    # =========================================================================

    @staticmethod
    def create(
            name,
            position=None,
            rotation=None,
            parent=None,
            radius=None
    ):
        u"""
        创建一个 Joint。

        position / rotation 都表示 World Space。
        rotation 表示普通 World Rotation，不表示 jointOrient。
        """
        if name is None:
            raise RuntimeError(
                u"Joint 名称不能为空。"
            )

        name = str(name).strip()

        if not name:
            raise RuntimeError(
                u"Joint 名称不能为空。"
            )

        if cmds.objExists(name):
            raise RuntimeError(
                u"节点已经存在：{}".format(
                    name
                )
            )

        if parent is not None:
            transform_utils.validate_transform(
                parent
            )

        joint = cmds.createNode(
            "joint",
            name=name
        )

        if parent is not None:
            joint = hierarchy_utils.parent(
                joint,
                parent
            )

        if position is not None:
            transform_utils.set_world_translation(
                joint,
                position
            )

        if rotation is not None:
            transform_utils.set_world_rotation(
                joint,
                rotation
            )

        if radius is not None:
            joint_object = Joint(
                joint
            )
            joint_object.set_radius(
                radius
            )

        return joint

    @staticmethod
    def create_at_object(
            obj,
            name,
            parent=None,
            match_rotation=True,
            radius=None
    ):
        u"""在指定 Transform / Joint 的世界位置创建 Joint。"""
        transform_utils.validate_transform(
            obj
        )

        position = transform_utils.get_world_translation(
            obj
        )
        rotation = None

        if match_rotation:
            rotation = transform_utils.get_world_rotation(
                obj
            )

        return Joint.create(
            name=name,
            position=position,
            rotation=rotation,
            parent=parent,
            radius=radius
        )

    # =========================================================================
    # Joint Orient
    # =========================================================================

    def get_joint_orient(self):
        u"""返回 [jointOrientX, jointOrientY, jointOrientZ]。"""
        attributes = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ",
        ]
        joint_orient = []

        for attribute in attributes:
            value = cmds.getAttr(
                "{}.{}".format(
                    self.joint,
                    attribute
                )
            )
            joint_orient.append(
                value
            )

        return joint_orient

    def set_joint_orient(self, joint_orient):
        u"""设置 jointOrientXYZ。"""
        if joint_orient is None:
            raise ValueError(
                u"joint_orient 必须包含 3 个数值。"
            )

        try:
            value_count = len(
                joint_orient
            )
        except TypeError:
            raise ValueError(
                u"joint_orient 必须包含 3 个数值。"
            )

        if value_count != 3:
            raise ValueError(
                u"joint_orient 必须包含 3 个数值。"
            )

        attributes = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ",
        ]

        index = 0

        while index < len(attributes):
            cmds.setAttr(
                "{}.{}".format(
                    self.joint,
                    attributes[index]
                ),
                joint_orient[index]
            )
            index += 1

        return self.joint

    def clear_joint_orient(self):
        u"""把当前 Joint 的 jointOrientXYZ 清零。"""
        return self.set_joint_orient(
            (0.0, 0.0, 0.0)
        )

    # =========================================================================
    # Display
    # =========================================================================

    def get_radius(self):
        u"""返回当前 Joint 的 radius。"""
        return cmds.getAttr(
            self.joint + ".radius"
        )

    def set_radius(self, radius):
        u"""设置当前 Joint 的 radius。"""
        try:
            radius = float(
                radius
            )
        except (TypeError, ValueError):
            raise ValueError(
                u"Joint radius 必须是数值。"
            )

        if radius < 0.0:
            raise ValueError(
                u"Joint radius 不能小于 0。"
            )

        cmds.setAttr(
            self.joint + ".radius",
            radius
        )

        return self.joint

    def show_axis(self):
        u"""显示当前 Joint 的 Local Rotation Axis。"""
        cmds.setAttr(
            self.joint + ".displayLocalAxis",
            1
        )

        return self.joint

    def hide_axis(self):
        u"""隐藏当前 Joint 的 Local Rotation Axis。"""
        cmds.setAttr(
            self.joint + ".displayLocalAxis",
            0
        )

        return self.joint

    # =========================================================================
    # Joint Property
    # =========================================================================

    def get_scale_compensate(self):
        u"""返回当前 Joint 的 segmentScaleCompensate 状态。"""
        return bool(
            cmds.getAttr(
                self.joint + ".segmentScaleCompensate"
            )
        )

    def set_scale_compensate(self, enabled=True):
        u"""设置当前 Joint 的 segmentScaleCompensate。"""
        cmds.setAttr(
            self.joint + ".segmentScaleCompensate",
            bool(enabled)
        )

        return self.joint

    # =========================================================================
    # Orient
    # =========================================================================

    def orient(
            self,
            primary_axis="xyz",
            secondary_axis="xup"
    ):
        u"""根据直接 Child Joint 整理当前 Joint Orient。"""
        children = hierarchy_utils.get_children(
            self.joint,
            node_type="joint",
            full_path=True
        )

        if not children:
            cmds.joint(
                self.joint,
                edit=True,
                orientJoint="none"
            )
            return self.joint

        cmds.joint(
            self.joint,
            edit=True,
            zeroScaleOrient=True,
            orientJoint=primary_axis,
            secondaryAxisOrient=secondary_axis
        )

        return self.joint

    # =========================================================================
    # Label
    # =========================================================================

    def set_label(
            self,
            side=0,
            label_type=18,
            other_type=""
    ):
        u"""设置 Maya Joint Label。"""
        side = int(
            side
        )
        label_type = int(
            label_type
        )

        if side not in [0, 1, 2]:
            raise ValueError(
                u"Joint Label side 只能是 0 / 1 / 2。"
            )

        if other_type is None:
            other_type = ""

        other_type = str(
            other_type
        )

        cmds.setAttr(
            self.joint + ".side",
            side
        )
        cmds.setAttr(
            self.joint + ".type",
            label_type
        )
        cmds.setAttr(
            self.joint + ".otherType",
            other_type,
            type="string"
        )

        return {
            "joint": self.joint,
            "side": side,
            "type": label_type,
            "otherType": other_type,
        }

    def tag(self):
        u"""根据项目标准 Joint 名称生成 Maya Joint Label。"""
        short_name = rename_utils.get_short_name(
            self.joint
        )
        name_parts = short_name.split(
            "_"
        )

        if len(name_parts) < 3:
            raise RuntimeError(
                u"Joint 名称格式不正确：{}".format(
                    short_name
                )
            )

        side_name = name_parts[1].lower()

        if side_name in [
                "l",
                "lf",
        ]:
            side_index = 1
        elif side_name in [
                "r",
                "rt",
        ]:
            side_index = 2
        else:
            side_index = 0

        description_parts = []
        index = 2

        while index < len(name_parts):
            part = name_parts[index]
            is_last_part = index == len(name_parts) - 1
            is_index = len(part) == 3 and part.isdigit()

            if not (is_last_part and is_index):
                description_parts.append(
                    part
                )

            index += 1

        description = "_".join(
            description_parts
        )

        return self.set_label(
            side=side_index,
            label_type=18,
            other_type=description
        )

    # =========================================================================
    # Transitional Compatibility
    # =========================================================================

    @staticmethod
    def _validate_joint(joint):
        u"""
        旧内部调用的过渡入口。

        验证逻辑仍然只有 Joint.__init__() 一份；新代码直接构造 Joint(joint)。
        """
        Joint(
            joint
        )
        return True


__all__ = [
    "Joint",
]
