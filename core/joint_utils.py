# coding=utf-8
u"""
Joint Utils
===========

Maya Joint 通用底层模块。

正式模块路径
------------
``muziToolset.core.joint_utils`` 是 Joint / JointCurve / JointChain 的唯一正式实现。
旧 ``jointUtils.py`` 兼容模块已经完成迁移并删除，正式代码统一使用 snake_case Import。

模块职责
--------
本模块按三个层级组织 Joint 能力：

Joint
    单个 Joint 的创建、查询、显示、方向、属性和 Maya Joint Label。

JointCurve
    Curve CV 与 Joint 的轻量桥接。Curve 的查询能力统一复用 curve_utils，不再维护第二套 Curve API。

JointChain
    多个 Joint 的父子链、模板链复制和批量定向。

主要公开 API
------------
Joint.create(...)
Joint.create_at_object(...)
Joint.create_child(...)
Joint.create_from_component(...)
Joint.create_from_selection(...)
    创建单个 / 多个 Joint。

Joint.get_parent()
Joint.get_children(...)
    查询 Joint 层级。

Joint.set_axis_visibility(...)
Joint.set_joints_axis_visibility(...)
Joint.set_selected_axis_visibility(...)
Joint.set_all_axis_visibility(...)
Joint.set_radius(...)
Joint.set_all_radius(...)
    Joint 显示设置。

Joint.orient(...)
Joint.clear_orient()
Joint.set_orient_keyable(...)
Joint.set_scale_compensate(...)
    Joint Orient 与 Segment Scale Compensate。

Joint.tag()
    根据项目命名设置 Maya Joint Label；同时兼容旧 l/r/m 和当前 lf/rt/md Side Token。

JointCurve.create_joints_on_curve_points(...)
    基于 Curve CV 世界位置创建 Joint。

JointChain.parent_joints_as_chain(...)
JointChain.create_chain(...)
JointChain.orient_chain(...)
    Joint Chain 操作。

设计原则
--------
1. Curve 查询统一复用 curve_utils；
2. Joint 模块不创建 Controller、不创建 Constraint、不包含 PySide UI；
3. Selection 驱动的方法仅作为 Tool 兼容入口；底层函数本身接受明确参数；
4. 完整 Arm / Leg / Spine / Eyelid 等绑定流程进入 systems，而不是继续扩张 Joint Utils；
5. 模块文件名与所有正式 Import 统一使用 snake_case。

依赖
----
maya.cmds
curve_utils
name_utils
"""

from __future__ import print_function

import re

import maya.cmds as cmds

from . import curve_utils
from . import name_utils


# =============================================================================
# Joint - 单 Joint 基础能力
# =============================================================================

class Joint(object):
    """单个 Maya Joint 的基础操作对象。"""

    def __init__(self, joint=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            joint (str):
                需要处理的 Maya Joint 节点名称。
        """

        self.joint = joint

        if self.joint is not None:
            self._validate_joint(self.joint)

    # -------------------------------------------------------------------------
    # Validate / Name
    # -------------------------------------------------------------------------

    @staticmethod
    def _validate_node(node):
        """检查 Maya 节点是否存在。"""
        if not node:
            raise RuntimeError(u"节点名称不能为空。")

        if not cmds.objExists(node):
            raise RuntimeError(
                u"节点不存在：{}".format(node)
            )

        return True

    @staticmethod
    def _validate_joint(joint):
        """检查节点是否是 Joint。"""
        Joint._validate_node(joint)

        node_type = cmds.nodeType(joint)

        if node_type != "joint":
            raise RuntimeError(
                u"节点不是 Joint：{} | type={}".format(
                    joint,
                    node_type
                )
            )

        return True

    @staticmethod
    def _short_name(node):
        """返回去掉 DAG Path 的节点短名称。"""
        return node.split("|")[-1]

    # -------------------------------------------------------------------------
    # Create
    # -------------------------------------------------------------------------

    @staticmethod
    def create(
            name,
            position=None,
            rotation=None,
            parent=None,
            radius=None
    ):
        u"""
        创建单个 Joint。

        步骤：
            1. 验证名称和 Parent；
            2. 创建 Joint；
            3. 应用 World Position / Rotation；
            4. 最后整理 Parent 和 Radius。

        Args:
            name (str):
                创建或查询时使用的节点名称。
            position (object):
                `position` 对应的输入数据。
            rotation (object):
                `rotation` 对应的输入数据。
            parent (str):
                父级 Maya 节点名称。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not name:
            raise RuntimeError(u"Joint 名称不能为空。")

        if cmds.objExists(name):
            raise RuntimeError(
                u"节点已经存在：{}".format(name)
            )

        if parent is not None:
            Joint._validate_node(parent)

        joint = cmds.createNode(
            "joint",
            name=name
        )

        if position is not None:
            cmds.xform(
                joint,
                worldSpace=True,
                translation=position
            )

        if rotation is not None:
            cmds.xform(
                joint,
                worldSpace=True,
                rotation=rotation
            )

        if parent is not None:
            parent_result = cmds.parent(
                joint,
                parent,
                absolute=True
            )

            if parent_result:
                joint = parent_result[0]

        if radius is not None:
            cmds.setAttr(
                joint + ".radius",
                radius
            )

        return joint

    @staticmethod
    def create_at_object(
            obj,
            name=None,
            parent=None,
            match_rotation=True,
            radius=None
    ):
        u"""
        在指定 Transform / Joint 的世界位置创建 Joint。

        Args:
            obj (object):
                `obj` 对应的输入数据。
            name (str):
                创建或查询时使用的节点名称。
            parent (str):
                父级 Maya 节点名称。
            match_rotation (bool):
                是否启用 `match_rotation` 对应的处理。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
                方法执行后的结果数据。
        """
        Joint._validate_node(obj)

        short_name = Joint._short_name(obj)

        if name is None:
            if short_name.startswith("jnt_"):
                name = "{}_child".format(short_name)
            else:
                name = "jnt_{}".format(short_name)

        # 步骤 1：读取参考对象 World Transform。
        position = cmds.xform(
            obj,
            query=True,
            worldSpace=True,
            translation=True
        )

        rotation = None

        if match_rotation:
            rotation = cmds.xform(
                obj,
                query=True,
                worldSpace=True,
                rotation=True
            )

        # 步骤 2：统一转给 create() 创建，避免重复维护创建逻辑。
        return Joint.create(
            name=name,
            position=position,
            rotation=rotation,
            parent=parent,
            radius=radius
        )

    @staticmethod
    def create_child(
            obj,
            name=None,
            radius=None
    ):
        u"""
        在指定对象位置创建一个 Child Joint，并 Parent 到该对象下。

        Args:
            obj (object):
                `obj` 对应的输入数据。
            name (str):
                创建或查询时使用的节点名称。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
                方法执行后的结果数据。
        """
        Joint._validate_node(obj)

        short_name = Joint._short_name(obj)

        if name is None:
            name = "{}_child".format(short_name)

            if not name.startswith("jnt_"):
                name = "jnt_{}".format(name)

        position = cmds.xform(
            obj,
            query=True,
            worldSpace=True,
            translation=True
        )
        rotation = cmds.xform(
            obj,
            query=True,
            worldSpace=True,
            rotation=True
        )

        return Joint.create(
            name=name,
            position=position,
            rotation=rotation,
            parent=obj,
            radius=radius
        )

    @staticmethod
    def create_from_component(
            component,
            name,
            parent=None,
            radius=None
    ):
        u"""
        在 Vertex / CV 等组件世界位置创建 Joint。

        Args:
            component (object):
                `component` 对应的输入数据。
            name (str):
                创建或查询时使用的节点名称。
            parent (str):
                父级 Maya 节点名称。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not component:
            raise RuntimeError(u"组件名称不能为空。")

        position = cmds.xform(
            component,
            query=True,
            worldSpace=True,
            translation=True
        )

        if not position:
            raise RuntimeError(
                u"无法获取组件位置：{}".format(component)
            )

        return Joint.create(
            name=name,
            position=position,
            parent=parent,
            radius=radius
        )

    @staticmethod
    def create_from_selection(
            name_prefix="jnt_snap",
            parent_chain=False,
            radius=None
    ):
        u"""
        兼容 Tool：根据当前 Selection 的对象 / 组件创建 Joint。

        ``parent_chain=True`` 时，按 Selection 顺序组成 Joint Chain。

        Args:
            name_prefix (str):
                `name_prefix` 对应的名称、标记或字符串参数。
            parent_chain (bool):
                是否启用 `parent_chain` 对应的处理。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object | list:
                方法执行后的结果数据。
        """
        selections = cmds.ls(
            selection=True,
            flatten=True,
            long=True
        ) or []

        if not selections:
            cmds.warning(u"请选择一个或以上的物体或组件。")
            return []

        joints = []
        current_parent = None

        for index in range(len(selections)):
            item = selections[index]
            joint_name = "{}_{:03d}".format(
                name_prefix,
                index + 1
            )

            if "." in item:
                joint = Joint.create_from_component(
                    component=item,
                    name=joint_name,
                    parent=current_parent,
                    radius=radius
                )
            else:
                joint = Joint.create_at_object(
                    obj=item,
                    name=joint_name,
                    parent=current_parent,
                    match_rotation=True,
                    radius=radius
                )

            joints.append(joint)

            if parent_chain:
                current_parent = joint

        return joints

    # -------------------------------------------------------------------------
    # Query
    # -------------------------------------------------------------------------

    def get_angle_z(self):
        u"""
        查询 Maya joint(angleZ=True) 数值。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return cmds.joint(
            self.joint,
            query=True,
            angleZ=True
        )

    def get_parent(self):
        u"""
        返回 Joint Parent；没有 Joint Parent 时返回 None。

        Returns:
            object | None:
                方法执行后的结果数据。
        """
        parents = cmds.listRelatives(
            self.joint,
            parent=True,
            type="joint",
            fullPath=True
        ) or []

        if not parents:
            return None

        return parents[0]

    def get_children(self, all_descendents=False):
        u"""
        返回 Child Joint；可选择是否递归全部后代。

        Args:
            all_descendents (bool):
                是否启用 `all_descendents` 对应的处理。

        Returns:
            object:
                方法执行后的结果数据。
        """
        children = cmds.listRelatives(
            self.joint,
            children=True,
            allDescendents=all_descendents,
            type="joint",
            fullPath=True
        ) or []

        return children

    # -------------------------------------------------------------------------
    # Display
    # -------------------------------------------------------------------------

    def set_axis_visibility(self, visible=True):
        u"""
        设置 Joint Local Rotation Axis 显示。

        Args:
            visible (bool):
                是否启用 `visible` 对应的处理。

        Returns:
            object:
                方法执行后的结果数据。
        """
        value = 1 if visible else 0

        cmds.setAttr(
            self.joint + ".displayLocalAxis",
            value
        )

        return self.joint

    def show_axis(self):
        u"""
        显示 Local Rotation Axis。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.set_axis_visibility(True)

    def hide_axis(self):
        u"""
        隐藏 Local Rotation Axis。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.set_axis_visibility(False)

    def set_radius(self, radius):
        u"""
        设置当前 Joint 显示半径。

        Args:
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
                方法执行后的结果数据。
        """
        cmds.setAttr(
            self.joint + ".radius",
            radius
        )
        return self.joint

    @staticmethod
    def set_joints_axis_visibility(
            joints,
            visible=True,
            include_descendents=False
    ):
        u"""
        批量设置 Joint Local Rotation Axis。

        Args:
            joints (str | list[str]):
                `joints` 对应的输入数据。
            visible (bool):
                是否启用 `visible` 对应的处理。
            include_descendents (bool):
                是否启用 `include_descendents` 对应的处理。

        Returns:
            object | list:
                方法执行后的结果数据。
        """
        if not joints:
            return []

        process_joints = []

        # 步骤 1：整理去重后的处理列表。
        for joint in joints:
            Joint._validate_joint(joint)

            if joint not in process_joints:
                process_joints.append(joint)

            if include_descendents:
                descendants = cmds.listRelatives(
                    joint,
                    allDescendents=True,
                    type="joint",
                    fullPath=True
                ) or []

                for descendant in descendants:
                    if descendant not in process_joints:
                        process_joints.append(descendant)

        # 步骤 2：统一应用显示状态。
        for joint in process_joints:
            Joint(joint).set_axis_visibility(
                visible=visible
            )

        return process_joints

    @staticmethod
    def set_selected_axis_visibility(
            visible=True,
            include_descendents=False
    ):
        u"""
        根据当前选择批量设置 Local Rotation Axis。

        Args:
            visible (bool):
                是否启用 `visible` 对应的处理。
            include_descendents (bool):
                是否启用 `include_descendents` 对应的处理。

        Returns:
            object | list:
                方法执行后的结果数据。
        """
        joints = cmds.ls(
            selection=True,
            type="joint",
            long=True
        ) or []

        if not joints:
            cmds.warning(u"请选择一个或以上的 Joint。")
            return []

        return Joint.set_joints_axis_visibility(
            joints=joints,
            visible=visible,
            include_descendents=include_descendents
        )

    @staticmethod
    def set_all_axis_visibility(visible=True):
        u"""
        设置场景全部 Joint Local Rotation Axis。

        Args:
            visible (bool):
                是否启用 `visible` 对应的处理。

        Returns:
            object:
                方法执行后的结果数据。
        """
        joints = cmds.ls(
            type="joint",
            long=True
        ) or []

        return Joint.set_joints_axis_visibility(
            joints=joints,
            visible=visible
        )

    @staticmethod
    def set_all_radius(radius):
        u"""
        设置场景全部 Joint 显示半径。

        Args:
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
                方法执行后的结果数据。
        """
        joints = cmds.ls(
            type="joint",
            long=True
        ) or []

        for joint in joints:
            cmds.setAttr(
                joint + ".radius",
                radius
            )

        return joints

    # -------------------------------------------------------------------------
    # Joint Orient
    # -------------------------------------------------------------------------

    def orient(
            self,
            orient_joint="xyz",
            secondary_axis_orient="xup"
    ):
        u"""
        对当前 Joint 做 Maya Joint Orient。

        有 Child Joint 时按照给定 Primary / Secondary Axis 定向；末端 Joint 清为 ``none``。

        Args:
            orient_joint (str):
                `orient_joint` 对应的名称、标记或字符串参数。
            secondary_axis_orient (str):
                `secondary_axis_orient` 对应的名称、标记或字符串参数。

        Returns:
            object:
                方法执行后的结果数据。
        """
        children = self.get_children(
            all_descendents=False
        )

        if children:
            cmds.joint(
                self.joint,
                edit=True,
                zeroScaleOrient=True,
                children=True,
                orientJoint=orient_joint,
                secondaryAxisOrient=secondary_axis_orient
            )
        else:
            cmds.joint(
                self.joint,
                edit=True,
                zeroScaleOrient=True,
                orientJoint="none"
            )

        return self.joint

    def clear_orient(self):
        u"""
        把 jointOrientXYZ 清零。

        Returns:
            object:
                方法执行后的结果数据。
        """
        attrs = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ",
        ]

        for attr in attrs:
            cmds.setAttr(
                "{}.{}".format(self.joint, attr),
                0
            )

        return self.joint

    def set_orient_keyable(self, keyable=True):
        u"""
        设置 jointOrientXYZ 是否 Keyable。

        Args:
            keyable (bool):
                是否启用 `keyable` 对应的处理。

        Returns:
            object:
                方法执行后的结果数据。
        """
        attrs = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ",
        ]

        for attr in attrs:
            cmds.setAttr(
                "{}.{}".format(self.joint, attr),
                keyable=keyable
            )

        return self.joint

    def show_orient(self):
        u"""
        显示 jointOrient 通道。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.set_orient_keyable(True)

    def hide_orient(self):
        u"""
        隐藏 jointOrient 的 Keyable 状态。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return self.set_orient_keyable(False)

    def set_scale_compensate(self, enabled=True):
        u"""
        设置 segmentScaleCompensate。

        Args:
            enabled (bool):
                是否启用 `enabled` 对应的处理。

        Returns:
            object:
                方法执行后的结果数据。
        """
        cmds.setAttr(
            self.joint + ".segmentScaleCompensate",
            1 if enabled else 0
        )
        return self.joint

    # -------------------------------------------------------------------------
    # Joint Label
    # -------------------------------------------------------------------------

    def tag(self):
        u"""
        根据项目命名设置 Maya Joint Label。

        支持：
            jnt_l_arm_upper_001
            jnt_r_arm_upper_001
            jnt_m_spine_001
        同时支持当前正式 Side Token：
            jnt_lf_arm_upper_001
            jnt_rt_arm_upper_001
            jnt_md_spine_001

        Returns:
            dict:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        short_name = Joint._short_name(self.joint)
        name_parts = short_name.split("_")

        if len(name_parts) < 3:
            raise RuntimeError(
                u"Joint 名称格式不正确：{}".format(short_name)
            )

        side_name = name_parts[1]

        if side_name in ["l", "lf"]:
            side_index = 1
        elif side_name in ["r", "rt"]:
            side_index = 2
        else:
            side_index = 0

        description_parts = []

        for index in range(2, len(name_parts)):
            part = name_parts[index]

            if index == len(name_parts) - 1:
                if re.match(r"^\d{3}$", part):
                    continue

            description_parts.append(part)

        description = "_".join(description_parts)

        cmds.setAttr(
            self.joint + ".side",
            side_index
        )
        cmds.setAttr(
            self.joint + ".type",
            18
        )
        cmds.setAttr(
            self.joint + ".otherType",
            description,
            type="string"
        )

        return {
            "joint": self.joint,
            "side": side_index,
            "type": 18,
            "otherType": description,
        }


# =============================================================================
# JointCurve - Curve 与 Joint 的轻量桥接
# =============================================================================

class JointCurve(object):
    """Curve CV 与 Joint 创建相关的兼容类。"""

    @staticmethod
    def get_curve_shape(curve):
        u"""
        兼容入口：底层复用 curve_utils.get_curve_shape。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return curve_utils.get_curve_shape(curve)

    @staticmethod
    def get_curve_transform(curve):
        u"""
        兼容入口：底层复用 curve_utils.get_curve_transform。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return curve_utils.get_curve_transform(curve)

    @staticmethod
    def get_curve_cvs(curve):
        u"""
        兼容入口：返回 Curve 全部 CV Component。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return curve_utils.get_curve_cvs(curve)

    @staticmethod
    def get_curve_cv_count(curve):
        u"""
        兼容入口：返回 Curve CV 数量。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return curve_utils.get_curve_cv_count(curve)

    @staticmethod
    def get_curve_cv_positions(curve):
        u"""
        兼容入口：返回 Curve CV 世界坐标。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
                方法执行后的结果数据。
        """
        return curve_utils.get_curve_cv_positions(
            curve,
            world_space=True
        )

    @staticmethod
    def _default_joint_base_name(curve):
        """根据 Curve 名称生成默认 Joint Base Name。"""
        curve_transform = JointCurve.get_curve_transform(curve)
        short_name = Joint._short_name(curve_transform)

        if short_name.startswith("crv_"):
            base_name = short_name.replace(
                "crv_",
                "jnt_",
                1
            )
        else:
            base_name = "jnt_{}".format(short_name)

        return re.sub(
            r"_\d{3}$",
            "",
            base_name
        )

    @staticmethod
    def create_joints_on_curve_points(
            curve,
            joint_base_name=None,
            parent_chain=True,
            create_group=True,
            group_name=None,
            radius=None
    ):
        u"""
        基于 Curve CV 世界位置创建 Joint。

        注意：这是“CV 对应 Joint”功能，不是按弧长均匀采样。需要等距采样时先使用
        curve_utils.sample_curve_by_length，再由上层 System 决定如何建 Joint。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。
            joint_base_name (str):
                `joint_base_name` 对应的 Maya 节点或资源名称。
            parent_chain (bool):
                是否启用 `parent_chain` 对应的处理。
            create_group (bool):
                是否启用 `create_group` 对应的处理。
            group_name (str):
                `group_name` 对应的 Maya 节点或资源名称。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            dict:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        curve_transform = JointCurve.get_curve_transform(curve)
        positions = JointCurve.get_curve_cv_positions(curve)

        if not positions:
            raise RuntimeError(
                u"Curve 没有找到 CV：{}".format(curve)
            )

        if joint_base_name is None:
            joint_base_name = JointCurve._default_joint_base_name(curve)

        # 步骤 1：可选创建统一 Joint Group。
        joint_group = None

        if create_group:
            if group_name is None:
                group_base_name = joint_base_name

                if group_base_name.startswith("jnt_"):
                    group_base_name = group_base_name.replace(
                        "jnt_",
                        "grp_",
                        1
                    )

                group_name = "{}_joints".format(group_base_name)

            if cmds.objExists(group_name):
                raise RuntimeError(
                    u"Joint Group 已经存在：{}".format(group_name)
                )

            joint_group = cmds.createNode(
                "transform",
                name=group_name
            )

        # 步骤 2：按 CV 顺序创建 Joint。
        joints = []
        current_parent = joint_group

        for index in range(len(positions)):
            joint_name = "{}_{:03d}".format(
                joint_base_name,
                index + 1
            )

            parent = joint_group

            if parent_chain:
                parent = current_parent

            joint = Joint.create(
                name=joint_name,
                position=positions[index],
                parent=parent,
                radius=radius
            )

            joints.append(joint)

            if parent_chain:
                current_parent = joint

        return {
            "curve": curve_transform,
            "jnt_list": joints,
            "jnt_grp": joint_group,
        }


# =============================================================================
# JointChain - 多 Joint 层级能力
# =============================================================================

class JointChain(object):
    """Joint Chain 创建、Parent 与 Orient 工具。"""

    @staticmethod
    def validate_joint_list(joints):
        u"""
        验证并返回 Joint 列表。

        Args:
            joints (str | list[str]):
                `joints` 对应的输入数据。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not joints:
            raise RuntimeError(u"Joint 列表不能为空。")

        result = []

        for joint in joints:
            Joint._validate_joint(joint)
            result.append(joint)

        return result

    @staticmethod
    def parent_joints_as_chain(joints):
        u"""
        按列表顺序组成 Joint Chain。

        Args:
            joints (str | list[str]):
                `joints` 对应的输入数据。

        Returns:
            object:
                方法执行后的结果数据。
        """
        joints = JointChain.validate_joint_list(joints)

        if len(joints) <= 1:
            return joints

        # 从尾部开始 Parent，避免前面节点 DAG Path 改变影响后续字符串。
        for index in range(
                len(joints) - 1,
                0,
                -1
        ):
            cmds.parent(
                joints[index],
                joints[index - 1]
            )

        return joints

    @staticmethod
    def parent_selected_as_chain():
        u"""
        兼容 Tool：把当前选择 Joint 按 Selection 顺序组成 Chain。

        Returns:
            object | list:
                方法执行后的结果数据。
        """
        joints = cmds.ls(
            selection=True,
            type="joint",
            long=True
        ) or []

        if not joints:
            cmds.warning(u"请选择一个或以上的 Joint。")
            return []

        return JointChain.parent_joints_as_chain(joints)

    @staticmethod
    def create_chain(
            blueprint_joints,
            suffix,
            joint_parent=None,
            hide_blueprint=True
    ):
        u"""
        根据 Blueprint Joint 创建一条新 Joint Chain。

        命名统一复用 name_utils.Name，以保持项目标准命名规则。

        Args:
            blueprint_joints (object):
                `blueprint_joints` 对应的输入数据。
            suffix (object):
                `suffix` 对应的输入数据。
            joint_parent (object):
                `joint_parent` 对应的输入数据。
            hide_blueprint (bool):
                是否启用 `hide_blueprint` 对应的处理。

        Returns:
            object:
                方法执行后的结果数据。

        Raises:
            RuntimeError:
                输入数据、场景状态或操作条件不满足要求时抛出。
        """
        blueprint_joints = JointChain.validate_joint_list(
            blueprint_joints
        )

        if joint_parent is not None:
            Joint._validate_node(joint_parent)

        joints_chain = []
        current_parent = joint_parent

        for blueprint_joint in blueprint_joints:
            # 步骤 1：根据 Blueprint 名称生成新 Joint 名称。
            name_object = name_utils.Name(
                name=blueprint_joint
            )
            name_object.type = "jnt"
            name_object.type = "{}{}".format(
                suffix,
                name_object.type
            )
            new_joint_name = name_object.name

            if cmds.objExists(new_joint_name):
                raise RuntimeError(
                    u"Joint 已经存在：{}".format(new_joint_name)
                )

            # 步骤 2：读取 Blueprint 世界姿态。
            position = cmds.xform(
                blueprint_joint,
                query=True,
                worldSpace=True,
                translation=True
            )
            rotation = cmds.xform(
                blueprint_joint,
                query=True,
                worldSpace=True,
                rotation=True
            )

            # 步骤 3：创建并组成新 Chain。
            new_joint = Joint.create(
                name=new_joint_name,
                position=position,
                rotation=rotation,
                parent=current_parent
            )

            cmds.makeIdentity(
                new_joint,
                apply=True,
                translate=True,
                rotate=True,
                scale=True
            )

            joints_chain.append(new_joint)
            current_parent = new_joint

        if hide_blueprint:
            cmds.setAttr(
                blueprint_joints[0] + ".visibility",
                0
            )

        return joints_chain

    @staticmethod
    def orient_chain(
            joints,
            orient_joint="xyz",
            secondary_axis_orient="xup"
    ):
        u"""
        按同一 Primary / Secondary Axis 批量 Orient Joint Chain。

        Args:
            joints (str | list[str]):
                `joints` 对应的输入数据。
            orient_joint (str):
                `orient_joint` 对应的名称、标记或字符串参数。
            secondary_axis_orient (str):
                `secondary_axis_orient` 对应的名称、标记或字符串参数。

        Returns:
            object:
                方法执行后的结果数据。
        """
        joints = JointChain.validate_joint_list(joints)

        for joint in joints:
            Joint(joint).orient(
                orient_joint=orient_joint,
                secondary_axis_orient=secondary_axis_orient
            )

        return joints


__all__ = [
    "Joint",
    "JointCurve",
    "JointChain",
]
