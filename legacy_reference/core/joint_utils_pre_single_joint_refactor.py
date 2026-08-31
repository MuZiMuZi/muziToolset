# coding=utf-8
u"""
Joint Utils
===========

Maya Joint 通用底层模块。

模块职责
--------
Joint
    单个 Joint 的创建、查询、显示、方向、属性和 Maya Joint Label。

JointCurve
    Curve CV 与 Joint 的轻量桥接。

JointChain
    多个 Joint 的父子链、模板链复制和批量定向。

设计边界
--------
- 节点存在性统一复用 scene_utils；
- DAG Short Name 统一复用 rename_utils；
- Transform 世界空间数据统一复用 transform_utils；
- 通用 Parent / Child 查询统一复用 hierarchy_utils；
- Curve 查询统一复用 curve_utils；
- 本模块只保留真正属于 Joint 的创建、显示、Orient、Label 和 Joint Chain 语义。
"""

from __future__ import print_function

import re

import maya.cmds as cmds

from . import curve_utils
from . import hierarchy_utils
from . import name_utils
from . import rename_utils
from . import scene_utils
from . import transform_utils


# =============================================================================
# Joint
# =============================================================================

class Joint(object):
    u"""单个 Maya Joint 的基础操作对象。"""

    def __init__(self, joint=None):
        u"""
        执行 `__init__` 对应的 Maya 工具操作。

        Args:
            joint (str):
                需要处理的 Maya Joint 节点名称。
        """

        self.joint = joint

        if self.joint is not None:
            # 确保构造时传入的节点确实是 Joint。
            self._validate_joint(
                self.joint
            )

    # -------------------------------------------------------------------------
    # Validate / Name - Compatibility Entrypoints
    # -------------------------------------------------------------------------

    @staticmethod
    def _validate_node(node):
        u"""
        兼容旧内部调用的节点校验入口。

        真正的节点存在性规则统一由 scene_utils.validate_node 维护。
        """
        # 使用 Scene Core 统一检查节点是否存在。
        return scene_utils.validate_node(
            node
        )

    @staticmethod
    def _validate_joint(joint):
        u"""检查节点是否存在且类型为 Joint。"""
        # 先使用 Scene Core 统一检查节点存在性。
        scene_utils.validate_node(
            joint
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

        return True

    @staticmethod
    def _short_name(node):
        u"""
        兼容旧内部调用的 Short Name 入口。

        DAG Short Name 规则统一由 rename_utils.get_short_name 维护。
        """
        # 使用 Rename Core 统一解析 DAG Short Name。
        return rename_utils.get_short_name(
            node
        )

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
        创建一个 Joint，并可设置世界姿态、Parent 与 Radius。

        Args:
            name (str):
                创建或查询时使用的节点名称。
            position (list[float] | tuple[float, float, float]):
                Joint / Transform 使用的 XYZ Position。
            rotation (list[float] | tuple[float, float, float]):
                Joint / Transform 使用的 XYZ Rotation。
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
            # 使用 Scene Core 统一验证 Parent 节点。
            scene_utils.validate_node(
                parent
            )

        # 创建真正的 Maya Joint 节点。
        joint = cmds.createNode(
            "joint",
            name=name
        )

        if position is not None:
            # 使用 Transform Core 写入 Joint 世界位置。
            transform_utils.set_world_translation(
                joint,
                position
            )

        if rotation is not None:
            # 使用 Transform Core 写入 Joint 世界旋转。
            transform_utils.set_world_rotation(
                joint,
                rotation
            )

        if parent is not None:
            # 使用 Hierarchy Core 建立 Parent，并接收可能变化的 DAG Path。
            joint = hierarchy_utils.Hierarchy.parent(
                joint,
                parent
            )

        if radius is not None:
            # Radius 属于 Joint 专属显示属性，因此保留在 Joint Core 内设置。
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
        在指定 Transform / Joint 的世界姿态创建 Joint。

        Args:
            obj (str):
                当前操作使用的 Maya DAG 节点或场景对象。
            name (str):
                创建或查询时使用的节点名称。
            parent (str):
                父级 Maya 节点名称。
            match_rotation (bool):
                根据目标 Transform 创建 Joint 时是否同时匹配目标 Rotation。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
            方法执行后的结果数据。
        """
        # 使用 Transform Core 验证参考对象。
        transform_utils.validate_transform(
            obj
        )

        # 使用统一 Short Name API 生成默认 Joint 名称。
        short_name = rename_utils.get_short_name(
            obj
        )

        if name is None:
            if short_name.startswith("jnt_"):
                name = "{}_child".format(
                    short_name
                )
            else:
                name = "jnt_{}".format(
                    short_name
                )

        # 使用 Transform Core 读取参考对象世界位置。
        position = transform_utils.get_world_translation(
            obj
        )

        rotation = None

        if match_rotation:
            # 需要匹配旋转时统一读取 World Rotation。
            rotation = transform_utils.get_world_rotation(
                obj
            )

        # 统一交给 Joint.create() 完成真正的创建流程。
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
        在指定对象世界姿态创建一个 Child Joint。

        Args:
            obj (str):
                当前操作使用的 Maya DAG 节点或场景对象。
            name (str):
                创建或查询时使用的节点名称。
            radius (float):
                创建节点或控制器使用的半径值。

        Returns:
            object:
            方法执行后的结果数据。
        """
        # 使用 Transform Core 验证 Parent / 参考对象。
        transform_utils.validate_transform(
            obj
        )

        # 使用统一 Short Name API 生成默认名称。
        short_name = rename_utils.get_short_name(
            obj
        )

        if name is None:
            name = "{}_child".format(
                short_name
            )

            if not name.startswith("jnt_"):
                name = "jnt_{}".format(
                    name
                )

        # 使用 Transform Core 读取 Parent 当前世界姿态。
        position = transform_utils.get_world_translation(
            obj
        )
        rotation = transform_utils.get_world_rotation(
            obj
        )

        # 创建 Joint，并直接挂到指定对象下。
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
        在 Vertex / CV 等 Component 世界位置创建 Joint。

        Args:
            component (str):
                用于创建 Joint 或查询位置的 Maya Component，例如 Vertex、CV 或 Edge。
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
            raise RuntimeError(
                u"组件名称不能为空。"
            )

        # Component 不是普通 DG Node，因此这里仍由 Maya xform 读取 Component Position。
        position = cmds.xform(
            component,
            query=True,
            worldSpace=True,
            translation=True
        )

        if not position:
            raise RuntimeError(
                u"无法获取组件位置：{}".format(
                    component
                )
            )

        # 统一交给 Joint.create() 完成创建和 Parent。
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
        兼容 Tool：根据当前 Selection 的对象 / Component 创建 Joint。

        这里保留 Selection 语义，因为这是明确的 Tool Compatibility API；
        真正的 Joint 创建仍统一调用参数化 API。

        Args:
            name_prefix (str):
                批量创建 Joint 时写入节点名称前部的 Prefix。
            parent_chain (bool):
                创建多个 Joint 时是否按输入顺序建立父子 Joint Chain。
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
            cmds.warning(
                u"请选择一个或以上的物体或组件。"
            )
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
                # Component 输入使用专用创建入口。
                joint = Joint.create_from_component(
                    component=item,
                    name=joint_name,
                    parent=current_parent,
                    radius=radius
                )
            else:
                # DAG 输入使用 Transform -> Joint 创建入口。
                joint = Joint.create_at_object(
                    obj=item,
                    name=joint_name,
                    parent=current_parent,
                    match_rotation=True,
                    radius=radius
                )

            joints.append(
                joint
            )

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
        返回直接 Joint Parent；上级不是 Joint 时返回 None。

        Returns:
            object | None:
            方法执行后的结果数据。
        """
        # 使用 Hierarchy Core 查询直接 Parent。
        parent = hierarchy_utils.Hierarchy.get_parent(
            self.joint,
            full_path=True
        )

        if parent is None:
            return None

        if cmds.nodeType(parent) != "joint":
            return None

        return parent

    def get_children(self, all_descendents=False):
        u"""
        返回 Child Joint；可选择递归全部后代。

        Args:
            all_descendents (bool):
                Joint 查询时是否包含当前节点以下的全部 Descendant Joint。

        Returns:
            object:
            方法执行后的结果数据。
        """
        if not all_descendents:
            # 直接 Child 查询统一交给 Hierarchy Core。
            return hierarchy_utils.Hierarchy.get_children(
                self.joint,
                node_type="joint",
                full_path=True
            )

        # 全部后代属于 Joint 专项递归查询，这里保留 Maya Joint Type Filter。
        children = cmds.listRelatives(
            self.joint,
            allDescendents=True,
            type="joint",
            fullPath=True
        ) or []

        return children

    # -------------------------------------------------------------------------
    # Display
    # -------------------------------------------------------------------------

    def set_axis_visibility(self, visible=True):
        u"""
        设置当前 Joint Local Rotation Axis 显示。

        Args:
            visible (bool):
                Joint / Guide / UI 元素是否保持可见。

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
        执行 `show_axis` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self.set_axis_visibility(
            True
        )

    def hide_axis(self):
        u"""
        执行 `hide_axis` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self.set_axis_visibility(
            False
        )

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
                需要批量处理的 Maya Joint 节点或 Joint Chain。
            visible (bool):
                Joint / Guide / UI 元素是否保持可见。
            include_descendents (bool):
                Joint 查询或显示操作是否递归包含 Descendant Joint。

        Returns:
            object | list:
            方法执行后的结果数据。
        """
        if not joints:
            return []

        process_joints = []

        for joint in joints:
            # 确保每一个输入节点都是 Joint。
            Joint._validate_joint(
                joint
            )

            if joint not in process_joints:
                process_joints.append(
                    joint
                )

            if include_descendents:
                # 通过 Joint Query API 获取全部后代，避免这里再维护一套查询规则。
                descendants = Joint(
                    joint
                ).get_children(
                    all_descendents=True
                )

                for descendant in descendants:
                    if descendant not in process_joints:
                        process_joints.append(
                            descendant
                        )

        for joint in process_joints:
            # 使用单 Joint API 统一应用显示状态。
            Joint(
                joint
            ).set_axis_visibility(
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
                Joint / Guide / UI 元素是否保持可见。
            include_descendents (bool):
                Joint 查询或显示操作是否递归包含 Descendant Joint。

        Returns:
            object | list:
            方法执行后的结果数据。
        """
        # 使用 Scene Core 查询当前选择的 Joint。
        joints = scene_utils.get_selected_nodes(
            node_type="joint",
            long=True,
            flatten=True
        )

        if not joints:
            cmds.warning(
                u"请选择一个或以上的 Joint。"
            )
            return []

        # 统一交给批量 Joint API 执行。
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
                Joint / Guide / UI 元素是否保持可见。

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
            # 使用单 Joint API 统一设置 Radius。
            Joint(
                joint
            ).set_radius(
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

        Args:
            orient_joint (str):
                当前 Rig 计算或构建使用的 Maya Joint 节点。
            secondary_axis_orient (str):
                Maya Joint Orient 使用的 Secondary Axis World Orientation，例如 `yup`、`zdown`。

        Returns:
            object:
            方法执行后的结果数据。
        """
        # 查询直接 Child Joint，用于判断当前 Joint 是否是链末端。
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
                "{}.{}".format(
                    self.joint,
                    attr
                ),
                0
            )

        return self.joint

    def set_orient_keyable(self, keyable=True):
        u"""
        设置 jointOrientXYZ 是否 Keyable。

        Args:
            keyable (bool):
                对应 Maya Attribute 是否允许 Animator Keyframe。

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
                "{}.{}".format(
                    self.joint,
                    attr
                ),
                keyable=keyable
            )

        return self.joint

    def show_orient(self):
        u"""
        执行 `show_orient` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self.set_orient_keyable(
            True
        )

    def hide_orient(self):
        u"""
        执行 `hide_orient` 对应的 Maya 工具操作。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return self.set_orient_keyable(
            False
        )

    def set_scale_compensate(self, enabled=True):
        u"""
        设置 segmentScaleCompensate。

        Args:
            enabled (bool):
                当前 UI 控件或 Rig 功能是否启用。

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

        Returns:
            dict:
            方法执行后的结果数据。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 使用统一 Short Name API 解析 Joint 名称。
        short_name = rename_utils.get_short_name(
            self.joint
        )
        name_parts = short_name.split("_")

        if len(name_parts) < 3:
            raise RuntimeError(
                u"Joint 名称格式不正确：{}".format(
                    short_name
                )
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

            description_parts.append(
                part
            )

        description = "_".join(
            description_parts
        )

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
# JointCurve
# =============================================================================

class JointCurve(object):
    u"""Curve CV 与 Joint 创建相关的兼容类。"""

    @staticmethod
    def get_curve_shape(curve):
        u"""
        执行 `get_curve_shape` 对应的 Maya 工具操作。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return curve_utils.get_curve_shape(
            curve
        )

    @staticmethod
    def get_curve_transform(curve):
        u"""
        执行 `get_curve_transform` 对应的 Maya 工具操作。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return curve_utils.get_curve_transform(
            curve
        )

    @staticmethod
    def get_curve_cvs(curve):
        u"""
        执行 `get_curve_cvs` 对应的 Maya 工具操作。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return curve_utils.get_curve_cvs(
            curve
        )

    @staticmethod
    def get_curve_cv_count(curve):
        u"""
        执行 `get_curve_cv_count` 对应的 Maya 工具操作。

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。

        Returns:
            object:
            方法执行后的结果数据。
        """

        return curve_utils.get_curve_cv_count(
            curve
        )

    @staticmethod
    def get_curve_cv_positions(curve):
        u"""
        执行 `get_curve_cv_positions` 对应的 Maya 工具操作。

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
        u"""根据 Curve 名称生成默认 Joint Base Name。"""
        # 获取正式 Curve Transform。
        curve_transform = JointCurve.get_curve_transform(
            curve
        )

        # 使用统一 Short Name API 获取名称。
        short_name = rename_utils.get_short_name(
            curve_transform
        )

        if short_name.startswith("crv_"):
            base_name = short_name.replace(
                "crv_",
                "jnt_",
                1
            )
        else:
            base_name = "jnt_{}".format(
                short_name
            )

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

        Args:
            curve (str):
                需要处理的 Maya Curve Transform 或 Shape 名称。
            joint_base_name (str):
                `joint_base_name` 对应的 Maya 节点或资源名称。
            parent_chain (bool):
                创建多个 Joint 时是否按输入顺序建立父子 Joint Chain。
            create_group (bool):
                当前 Rig / Guide / Controller 层级中的 Maya Group Transform。
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
        # 获取 Curve Transform 和 CV 世界位置。
        curve_transform = JointCurve.get_curve_transform(
            curve
        )
        positions = JointCurve.get_curve_cv_positions(
            curve
        )

        if not positions:
            raise RuntimeError(
                u"Curve 没有找到 CV：{}".format(
                    curve
                )
            )

        if joint_base_name is None:
            # 根据 Curve 名称生成默认 Joint Base Name。
            joint_base_name = JointCurve._default_joint_base_name(
                curve
            )

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

                group_name = "{}_joints".format(
                    group_base_name
                )

            if cmds.objExists(group_name):
                raise RuntimeError(
                    u"Joint Group 已经存在：{}".format(
                        group_name
                    )
                )

            # 使用 Hierarchy Core 创建 Joint Group。
            joint_group = hierarchy_utils.Hierarchy.create_grp(
                group_name
            )

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

            # 使用单 Joint API 创建当前 CV 对应 Joint。
            joint = Joint.create(
                name=joint_name,
                position=positions[index],
                parent=parent,
                radius=radius
            )

            joints.append(
                joint
            )

            if parent_chain:
                current_parent = joint

        return {
            "curve": curve_transform,
            "jnt_list": joints,
            "jnt_grp": joint_group,
        }


# =============================================================================
# JointChain
# =============================================================================

class JointChain(object):
    u"""Joint Chain 创建、Parent 与 Orient 工具。"""

    @staticmethod
    def validate_joint_list(joints):
        u"""
        验证并返回 Joint 列表。

        Args:
            joints (str | list[str]):
                需要批量处理的 Maya Joint 节点或 Joint Chain。

        Returns:
            object:
            方法执行后的结果数据。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        if not joints:
            raise RuntimeError(
                u"Joint 列表不能为空。"
            )

        result = []

        for joint in joints:
            # 确保列表中的每一个节点都是 Joint。
            Joint._validate_joint(
                joint
            )
            result.append(
                joint
            )

        return result

    @staticmethod
    def parent_joints_as_chain(joints):
        u"""
        按列表顺序组成 Joint Chain。

        Args:
            joints (str | list[str]):
                需要批量处理的 Maya Joint 节点或 Joint Chain。

        Returns:
            object:
            方法执行后的结果数据。
        """
        # 验证输入 Joint 列表。
        joints = JointChain.validate_joint_list(
            joints
        )

        if len(joints) <= 1:
            return joints

        # 从尾部开始 Parent，避免前面节点 DAG Path 改变影响后续字符串。
        for index in range(
                len(joints) - 1,
                0,
                -1
        ):
            hierarchy_utils.Hierarchy.parent(
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
        # 使用 Scene Core 查询当前选择 Joint。
        joints = scene_utils.get_selected_nodes(
            node_type="joint",
            long=True,
            flatten=True
        )

        if not joints:
            cmds.warning(
                u"请选择一个或以上的 Joint。"
            )
            return []

        # 统一交给参数化 Chain API 建立父子关系。
        return JointChain.parent_joints_as_chain(
            joints
        )

    @staticmethod
    def create_chain(
            blueprint_joints,
            suffix,
            joint_parent=None,
            hide_blueprint=True
    ):
        u"""
        根据 Blueprint Joint 创建一条新 Joint Chain。

        Args:
            blueprint_joints (str | list[str]):
                作为正式 Skeleton 构建来源的 Blueprint / Guide Joint 列表。
            suffix (str):
                添加到 Maya 节点名称尾部的 Suffix。
            joint_parent (str | None):
                新建 Joint Chain 的父 Joint / Parent Transform；None 表示保持在世界层级。
            hide_blueprint (bool):
                生成正式 Skeleton 后是否隐藏 Blueprint / Guide Joint。

        Returns:
            object:
            方法执行后的结果数据。

        Raises:
            RuntimeError:
            输入数据、场景状态或操作条件不满足要求时抛出。
        """
        # 验证 Blueprint Joint 列表。
        blueprint_joints = JointChain.validate_joint_list(
            blueprint_joints
        )

        if joint_parent is not None:
            # 使用 Scene Core 验证最终 Parent。
            scene_utils.validate_node(
                joint_parent
            )

        joints_chain = []
        current_parent = joint_parent

        for blueprint_joint in blueprint_joints:
            # 根据 Blueprint 名称生成新 Joint 名称。
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
                    u"Joint 已经存在：{}".format(
                        new_joint_name
                    )
                )

            # 使用 Transform Core 读取 Blueprint 世界位置和旋转。
            position = transform_utils.get_world_translation(
                blueprint_joint
            )
            rotation = transform_utils.get_world_rotation(
                blueprint_joint
            )

            # 创建当前正式 Joint，并组成新 Chain。
            new_joint = Joint.create(
                name=new_joint_name,
                position=position,
                rotation=rotation,
                parent=current_parent
            )

            # Freeze Transform 属于当前 Joint Chain 的构建语义，保留在这里执行。
            cmds.makeIdentity(
                new_joint,
                apply=True,
                translate=True,
                rotate=True,
                scale=True
            )

            joints_chain.append(
                new_joint
            )
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
                需要批量处理的 Maya Joint 节点或 Joint Chain。
            orient_joint (str):
                当前 Rig 计算或构建使用的 Maya Joint 节点。
            secondary_axis_orient (str):
                Maya Joint Orient 使用的 Secondary Axis World Orientation，例如 `yup`、`zdown`。

        Returns:
            object:
            方法执行后的结果数据。
        """
        # 验证输入 Joint 列表。
        joints = JointChain.validate_joint_list(
            joints
        )

        for joint in joints:
            # 使用单 Joint API 完成每个 Joint 的 Orient。
            Joint(
                joint
            ).orient(
                orient_joint=orient_joint,
                secondary_axis_orient=secondary_axis_orient
            )

        return joints


__all__ = [
    "Joint",
    "JointCurve",
    "JointChain",
]
