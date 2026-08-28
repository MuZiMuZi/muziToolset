# coding=utf-8

u"""
jointUtils
==========

Maya Joint 基础工具模块。

结构：
    Joint
        单个关节的创建、查询、显示、方向、属性和标签。

    JointCurve
        Curve CV 与 Joint 的创建功能。

    JointChain
        多个 Joint 的层级、复制链和批量定向。

已移除：
    重采样、Controller、Constraint、PySide2 UI 相关实现。

依赖：
    maya.cmds
    nameUtils
"""

import re

import maya.cmds as cmds

from . import nameUtils


# =============================================================================
# Joint
# =============================================================================

class Joint(object):
    """
    单个 Joint 节点的基础操作。
    """

    def __init__(self, joint=None):

        self.joint = joint

        if self.joint is not None:
            self._validate_joint(self.joint)


    # -------------------------------------------------------------------------
    # 检查
    # -------------------------------------------------------------------------

    @staticmethod
    def _validate_node(node):

        if not node:
            raise RuntimeError(u"节点名称不能为空。")

        if not cmds.objExists(node):
            raise RuntimeError(
                u"节点不存在：{}".format(node)
            )

        return True


    @staticmethod
    def _validate_joint(joint):

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

        return node.split("|")[-1]


    # -------------------------------------------------------------------------
    # 创建
    # -------------------------------------------------------------------------

    @staticmethod
    def create(
            name,
            position=None,
            rotation=None,
            parent=None,
            radius=None
    ):
        """
        创建单个 Joint。

        Args:
            name(str): Joint 名称。
            position(list): 世界坐标。
            rotation(list): 世界旋转。
            parent(str): 父节点。
            radius(float): Joint 显示大小。

        Returns:
            str: Joint 名称。
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
            joint = cmds.parent(
                joint,
                parent
            )[0]

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
        """
        在指定 Transform / Joint 的位置创建 Joint。
        """

        Joint._validate_node(obj)

        short_name = Joint._short_name(obj)

        if name is None:

            if short_name.startswith("jnt_"):
                name = "{}_child".format(short_name)
            else:
                name = "jnt_{}".format(short_name)

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

        joint = Joint.create(
            name=name,
            position=position,
            rotation=rotation,
            parent=parent,
            radius=radius
        )

        return joint


    @staticmethod
    def create_child(
            obj,
            name=None,
            radius=None
    ):
        """
        在指定对象下创建一个子 Joint。
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

        child_joint = Joint.create(
            name=name,
            position=position,
            rotation=rotation,
            radius=radius
        )

        child_joint = cmds.parent(
            child_joint,
            obj
        )[0]

        return child_joint


    @staticmethod
    def create_from_component(
            component,
            name,
            parent=None,
            radius=None
    ):
        """
        在 Vertex / CV 等组件位置创建 Joint。
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

        joint = Joint.create(
            name=name,
            position=position,
            parent=parent,
            radius=radius
        )

        return joint


    @staticmethod
    def create_from_selection(
            name_prefix="jnt_snap",
            parent_chain=False,
            radius=None
    ):
        """
        根据当前选择的物体或组件创建 Joint。
        """

        selections = cmds.ls(
            selection=True,
            flatten=True,
            long=True
        )

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
    # 获取
    # -------------------------------------------------------------------------

    def get_angle_z(self):

        return cmds.joint(
            self.joint,
            query=True,
            angleZ=True
        )


    def get_parent(self):

        parents = cmds.listRelatives(
            self.joint,
            parent=True,
            type="joint",
            fullPath=True
        )

        if not parents:
            return None

        return parents[0]


    def get_children(self, all_descendents=False):

        children = cmds.listRelatives(
            self.joint,
            children=True,
            allDescendents=all_descendents,
            type="joint",
            fullPath=True
        )

        if not children:
            return []

        return children


    # -------------------------------------------------------------------------
    # Local Rotation Axis / Radius
    # -------------------------------------------------------------------------

    def set_axis_visibility(self, visible=True):

        value = 0

        if visible:
            value = 1

        cmds.setAttr(
            self.joint + ".displayLocalAxis",
            value
        )

        return self.joint


    def show_axis(self):

        return self.set_axis_visibility(
            visible=True
        )


    def hide_axis(self):

        return self.set_axis_visibility(
            visible=False
        )


    def set_radius(self, radius):

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
        """
        批量设置 Joint Local Rotation Axis。
        """

        if not joints:
            return []

        process_joints = []

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
                )

                if descendants:

                    for descendant in descendants:

                        if descendant not in process_joints:
                            process_joints.append(descendant)

        for joint in process_joints:

            joint_obj = Joint(joint)

            joint_obj.set_axis_visibility(
                visible=visible
            )

        return process_joints


    @staticmethod
    def set_selected_axis_visibility(
            visible=True,
            include_descendents=False
    ):

        joints = cmds.ls(
            selection=True,
            type="joint",
            long=True
        )

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

        joints = cmds.ls(
            type="joint",
            long=True
        )

        return Joint.set_joints_axis_visibility(
            joints=joints,
            visible=visible
        )


    @staticmethod
    def set_all_radius(radius):

        joints = cmds.ls(
            type="joint",
            long=True
        )

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
        """
        有子 Joint 时进行定向；
        末端 Joint 的 orientJoint 设置为 none。
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

        attrs = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ"
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

        attrs = [
            "jointOrientX",
            "jointOrientY",
            "jointOrientZ"
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

        return self.set_orient_keyable(
            keyable=True
        )


    def hide_orient(self):

        return self.set_orient_keyable(
            keyable=False
        )


    # -------------------------------------------------------------------------
    # Segment Scale Compensate
    # -------------------------------------------------------------------------

    def set_scale_compensate(self, enabled=True):

        value = 0

        if enabled:
            value = 1

        cmds.setAttr(
            self.joint + ".segmentScaleCompensate",
            value
        )

        return self.joint


    # -------------------------------------------------------------------------
    # Joint Label
    # -------------------------------------------------------------------------

    def tag(self):
        """
        根据命名设置 Maya Joint Label。

        预期：
            jnt_l_arm_upper_001
            jnt_r_arm_upper_001
            jnt_m_spine_001
        """

        short_name = Joint._short_name(
            self.joint
        )

        name_parts = short_name.split("_")

        if len(name_parts) < 3:
            raise RuntimeError(
                u"Joint 名称格式不正确：{}".format(short_name)
            )

        side_name = name_parts[1]

        if side_name == "l":
            side_index = 1

        elif side_name == "r":
            side_index = 2

        else:
            side_index = 0

        description_parts = []

        for index in range(
            2,
            len(name_parts)
        ):

            part = name_parts[index]

            if index == len(name_parts) - 1:

                if re.match(r"^\d{3}$", part):
                    continue

            description_parts.append(part)

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

        result = {
            "joint": self.joint,
            "side": side_index,
            "type": 18,
            "otherType": description
        }

        return result


# =============================================================================
# JointCurve
# =============================================================================

class JointCurve(object):
    """
    Curve 与 Joint 相关功能。
    """

    @staticmethod
    def get_curve_shape(curve):

        Joint._validate_node(curve)

        node_type = cmds.nodeType(curve)

        if node_type == "nurbsCurve":
            return curve

        shapes = cmds.listRelatives(
            curve,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        )

        if not shapes:
            raise RuntimeError(
                u"节点没有 Shape：{}".format(curve)
            )

        for shape in shapes:

            shape_type = cmds.nodeType(shape)

            if shape_type == "nurbsCurve":
                return shape

        raise RuntimeError(
            u"节点不是 NURBS Curve：{}".format(curve)
        )


    @staticmethod
    def get_curve_transform(curve):

        curve_shape = JointCurve.get_curve_shape(
            curve
        )

        parents = cmds.listRelatives(
            curve_shape,
            parent=True,
            fullPath=True
        )

        if not parents:
            raise RuntimeError(
                u"Curve Shape 没有 Transform：{}".format(
                    curve_shape
                )
            )

        return parents[0]


    @staticmethod
    def get_curve_cvs(curve):
        """
        直接读取 cv[*]，不再使用 spans + degree 推算 CV 数量。
        """

        curve_shape = JointCurve.get_curve_shape(
            curve
        )

        cvs = cmds.ls(
            curve_shape + ".cv[*]",
            flatten=True
        )

        if not cvs:
            return []

        return cvs


    @staticmethod
    def get_curve_cv_count(curve):

        cvs = JointCurve.get_curve_cvs(
            curve
        )

        return len(cvs)


    @staticmethod
    def get_curve_cv_positions(curve):

        cvs = JointCurve.get_curve_cvs(
            curve
        )

        positions = []

        for cv in cvs:

            position = cmds.xform(
                cv,
                query=True,
                worldSpace=True,
                translation=True
            )

            positions.append(position)

        return positions


    @staticmethod
    def _default_joint_base_name(curve):

        curve_transform = JointCurve.get_curve_transform(
            curve
        )

        short_name = Joint._short_name(
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

        base_name = re.sub(
            r"_\d{3}$",
            "",
            base_name
        )

        return base_name


    @staticmethod
    def create_joints_on_curve_points(
            curve,
            joint_base_name=None,
            parent_chain=True,
            create_group=True,
            group_name=None,
            radius=None
    ):
        """
        基于 Curve CV 创建 Joint。

        Returns:
            dict:
                {
                    "curve": curve_transform,
                    "jnt_list": joints,
                    "jnt_grp": joint_group
                }
        """

        curve_transform = JointCurve.get_curve_transform(
            curve
        )

        positions = JointCurve.get_curve_cv_positions(
            curve
        )

        if not positions:
            raise RuntimeError(
                u"Curve 没有找到 CV：{}".format(curve)
            )

        if joint_base_name is None:

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

            joint_group = cmds.createNode(
                "transform",
                name=group_name
            )

        joints = []
        current_parent = joint_group

        for index in range(len(positions)):

            joint_name = "{}_{:03d}".format(
                joint_base_name,
                index + 1
            )

            if parent_chain:
                parent = current_parent
            else:
                parent = joint_group

            joint = Joint.create(
                name=joint_name,
                position=positions[index],
                parent=parent,
                radius=radius
            )

            joints.append(joint)

            if parent_chain:
                current_parent = joint

        result = {
            "curve": curve_transform,
            "jnt_list": joints,
            "jnt_grp": joint_group
        }

        return result


# =============================================================================
# JointChain
# =============================================================================

class JointChain(object):
    """
    多 Joint 的关节链功能。
    """

    @staticmethod
    def validate_joint_list(joints):

        if not joints:
            raise RuntimeError(u"Joint 列表不能为空。")

        result = []

        for joint in joints:

            Joint._validate_joint(joint)
            result.append(joint)

        return result


    @staticmethod
    def parent_joints_as_chain(joints):
        """
        按列表顺序组成 Joint Chain。
        """

        joints = JointChain.validate_joint_list(
            joints
        )

        if len(joints) <= 1:
            return joints

        for index in range(
            len(joints) - 1,
            0,
            -1
        ):

            child_joint = joints[index]
            parent_joint = joints[index - 1]

            cmds.parent(
                child_joint,
                parent_joint
            )

        return joints


    @staticmethod
    def parent_selected_as_chain():

        joints = cmds.ls(
            selection=True,
            type="joint",
            long=True
        )

        if not joints:
            cmds.warning(u"请选择一个或以上的 Joint。")
            return []

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
        """
        根据模板 Joint 创建新的 Joint Chain。
        命名继续使用项目中的 nameUtils.Name。
        """

        blueprint_joints = JointChain.validate_joint_list(
            blueprint_joints
        )

        if joint_parent is not None:
            Joint._validate_node(joint_parent)

        joints_chain = []
        current_parent = joint_parent

        for blueprint_joint in blueprint_joints:

            name_obj = nameUtils.Name(
                name=blueprint_joint
            )

            name_obj.type = "jnt"

            name_obj.type = "{}{}".format(
                suffix,
                name_obj.type
            )

            new_joint_name = name_obj.name

            if cmds.objExists(new_joint_name):
                raise RuntimeError(
                    u"Joint 已经存在：{}".format(
                        new_joint_name
                    )
                )

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

            root_blueprint_joint = blueprint_joints[0]

            cmds.setAttr(
                root_blueprint_joint + ".visibility",
                0
            )

        return joints_chain


    @staticmethod
    def orient_chain(
            joints,
            orient_joint="xyz",
            secondary_axis_orient="xup"
    ):
        """
        批量设置 Joint Chain 方向。
        不处理任何 Constraint。
        """

        joints = JointChain.validate_joint_list(
            joints
        )

        for joint in joints:

            joint_obj = Joint(joint)

            joint_obj.orient(
                orient_joint=orient_joint,
                secondary_axis_orient=secondary_axis_orient
            )

        return joints
