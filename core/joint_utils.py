# coding=utf-8
u"""
Joint Utils
===========

Maya 单个 Joint 的底层能力模块。

设计原则
--------
Joint 类只负责“一个 Joint 节点本身应该具备的能力”：

    - 创建与初始化验证；
    - 名称；
    - World Position / Rotation；
    - Joint Orient；
    - Parent / Direct Child Joint；
    - Radius / Local Rotation Axis；
    - Segment Scale Compensate；
    - 单 Joint Orient；
    - Maya Joint Label。

Joint 实例在 __init__() 时只验证一次节点存在性和节点类型。
初始化成功后，普通方法默认 self.joint 仍然是有效 Joint，
不再为每一次操作重复执行存在性和类型检查。

本模块明确不负责：

    - Selection / 全场景批处理；
    - Vertex / Edge / CV 创建 Joint；
    - Curve -> Joint；
    - Joint Chain；
    - Duplicate Chain / Orient Chain；
    - FK / IK；
    - Face / Body 等具体 Rig Component。

这些更高层能力以后通过组合 Joint API，在对应层级重新实现。
"""

from __future__ import print_function

import maya.cmds as cmds

from . import hierarchy_utils
from . import rename_utils
from . import transform_utils


class Joint(object):
    u"""单个 Maya Joint 节点的统一操作对象。"""

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

        使用 cmds.createNode() 而不是 cmds.joint()，
        避免创建结果受到当前 Maya Selection 影响。
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

        # 先建立 Parent，再写入 World Transform。
        # 这样 position / rotation 的含义始终是最终 World Space。
        if parent is not None:
            joint = hierarchy_utils.Hierarchy.parent(
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
        u"""
        在指定 Transform / Joint 的世界位置创建 Joint。

        match_rotation=True 时，同时匹配参考对象的 World Rotation。
        """
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
    # State
    # =========================================================================

    def exists(self):
        u"""主动查询当前 Joint 节点是否仍然存在于 Maya Scene。"""
        return bool(
            cmds.objExists(
                self.joint
            )
        )

    # =========================================================================
    # Name
    # =========================================================================

    def get_name(self):
        u"""返回当前 Joint 的 Short Name。"""
        return rename_utils.get_short_name(
            self.joint
        )

    def rename(self, new_name):
        u"""重命名当前 Joint，并同步更新 self.joint。"""
        if new_name is None:
            raise RuntimeError(
                u"新的 Joint 名称不能为空。"
            )

        new_name = str(new_name).strip()

        if not new_name:
            raise RuntimeError(
                u"新的 Joint 名称不能为空。"
            )

        result = rename_utils.rename_node(
            self.joint,
            new_name
        )

        if result is None:
            raise RuntimeError(
                u"Joint 重命名失败：{} -> {}".format(
                    self.joint,
                    new_name
                )
            )

        self.joint = result
        return self.joint

    # =========================================================================
    # Transform
    # =========================================================================

    def get_position(self):
        u"""返回当前 Joint 的 World Position。"""
        return transform_utils.get_world_translation(
            self.joint
        )

    def set_position(self, position):
        u"""设置当前 Joint 的 World Position。"""
        transform_utils.set_world_translation(
            self.joint,
            position
        )

        return self.joint

    def get_rotation(self):
        u"""返回当前 Joint 的 World Rotation。"""
        return transform_utils.get_world_rotation(
            self.joint
        )

    def set_rotation(self, rotation):
        u"""
        设置当前 Joint 的 World Rotation。

        注意：rotation 和 jointOrient 是两套不同的数据。
        """
        transform_utils.set_world_rotation(
            self.joint,
            rotation
        )

        return self.joint

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
    # Hierarchy
    # =========================================================================

    def get_parent(self):
        u"""
        返回直接 DAG Parent。

        Parent 可以是 Transform，也可以是 Joint。
        """
        return hierarchy_utils.Hierarchy.get_parent(
            self.joint,
            full_path=True
        )

    def get_children(self):
        u"""只返回当前 Joint 的直接 Child Joint。"""
        return hierarchy_utils.Hierarchy.get_children(
            self.joint,
            node_type="joint",
            full_path=True
        )

    def set_parent(self, parent=None):
        u"""
        设置 Parent，并保持当前 Joint 的世界姿态。

        parent=None 表示 Parent 到 World。
        """
        if parent is None:
            current_parent = self.get_parent()

            if current_parent is None:
                return self.joint

            result = cmds.parent(
                self.joint,
                world=True,
                absolute=True
            )

            if result:
                self.joint = result[0]

            return self.joint

        transform_utils.validate_transform(
            parent
        )

        self.joint = hierarchy_utils.Hierarchy.parent(
            self.joint,
            parent
        )

        return self.joint

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
        u"""
        根据直接 Child Joint 整理当前 Joint Orient。

        这里只处理当前 Joint，不递归整条 Joint Chain。
        """
        children = self.get_children()

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
        u"""
        设置 Maya Joint Label。

        side 常用值：
            0 = Center
            1 = Left
            2 = Right

        label_type=18 表示 Other。
        """
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
        u"""
        根据项目标准 Joint 名称生成 Maya Joint Label。

        示例：
            jnt_lf_arm_bind_001
            jnt_rt_arm_bind_001
            jnt_md_spine_bind_001
        """
        short_name = self.get_name()
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


__all__ = [
    "Joint",
]
