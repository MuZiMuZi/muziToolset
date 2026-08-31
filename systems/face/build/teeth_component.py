# coding=utf-8
u"""
Teeth Component
===============

PyMEL-first 的上下牙床 Face Rig Component。
"""

from __future__ import print_function

import pymel.core as pm

from ....core import control
from ....core import name
from .. import config
from ..face_base import FaceBase
from ..guide import FaceGuide


class TeethComponent(FaceBase):
    u"""Step 03 中的 Teeth Rig Component。"""

    def __init__(self):
        super(TeethComponent, self).__init__()
        self.face_guide = FaceGuide()
        self.upper_teeth_guide = None
        self.lower_teeth_guide = None
        self.upper_teeth_joint = None
        self.lower_teeth_joint = None
        self.upper_teeth_control = None
        self.lower_teeth_control = None
        self.upper_teeth_control_data = None
        self.lower_teeth_control_data = None
        self.connection_nodes = []
        self.model_constraints = []
        self.controller_global_scale = 1.0
        self.controller_color = 17
        self.controller_size = 1.0
        self.upper_teeth_joint_name = None
        self.lower_teeth_joint_name = None
        self.upper_teeth_control_name = None
        self.lower_teeth_control_name = None

    def collect_inputs(self):
        self.validate_setup_data(require_mouth_joint_count=False)
        self.upper_teeth_guide = self.face_guide.get_guide_node(
            name.create_name("loc", "md", "upper_teeth", "guide", 1),
            required=True
        )
        self.lower_teeth_guide = self.face_guide.get_guide_node(
            name.create_name("loc", "md", "lower_teeth", "guide", 1),
            required=True
        )

        controller_settings = self.face_guide.load_controller_settings()
        self.controller_global_scale = float(
            controller_settings.get(config.controller_global_scale_attribute, 1.0)
        )
        self.controller_color = int(
            controller_settings.get(config.controller_color_attributes["md"], 17)
        )
        self.controller_size = float(
            controller_settings.get(config.controller_size_attributes["teeth"], 1.0)
        )
        return True

    def prepare_data(self):
        self.ensure_hierarchy()
        self.upper_teeth_joint_name = name.create_name(
            "jnt", "md", "upper_teeth", "bind", 1
        )
        self.lower_teeth_joint_name = name.create_name(
            "jnt", "md", "lower_teeth", "bind", 1
        )
        self.upper_teeth_control_name = name.create_name(
            "ctrl", "md", "upper_teeth", "bind", 1
        )
        self.lower_teeth_control_name = name.create_name(
            "ctrl", "md", "lower_teeth", "bind", 1
        )
        self.delete_previous_result()
        return True

    def delete_previous_result(self):
        node_names = [
            self.upper_teeth_joint_name,
            self.lower_teeth_joint_name,
            name.replace_node_type(self.upper_teeth_control_name, "zero"),
            name.replace_node_type(self.lower_teeth_control_name, "zero"),
            name.create_name("mult", "md", "upper_teeth", "control", 1),
            name.create_name("mult", "md", "lower_teeth", "control", 1),
            name.create_name("dcmp", "md", "upper_teeth", "control", 1),
            name.create_name("dcmp", "md", "lower_teeth", "control", 1),
            name.create_name("parent", "md", "upper_teeth", "model", 1),
            name.create_name("parent", "md", "lower_teeth", "model", 1),
        ]
        for node_name in node_names:
            if pm.objExists(node_name):
                pm.delete(pm.PyNode(node_name))
        return True

    def create_joint(self):
        self.upper_teeth_joint = pm.createNode(
            "joint",
            name=self.upper_teeth_joint_name,
            parent=self.joint_group
        )
        self.lower_teeth_joint = pm.createNode(
            "joint",
            name=self.lower_teeth_joint_name,
            parent=self.joint_group
        )
        self.upper_teeth_joint.setMatrix(
            self.upper_teeth_guide.getMatrix(worldSpace=True),
            worldSpace=True
        )
        self.lower_teeth_joint.setMatrix(
            self.lower_teeth_guide.getMatrix(worldSpace=True),
            worldSpace=True
        )
        self.upper_teeth_joint.radius.set(0.5)
        self.lower_teeth_joint.radius.set(0.5)
        return {
            "upper": self.upper_teeth_joint,
            "lower": self.lower_teeth_joint,
        }

    def create_controller(self):
        radius = self.controller_global_scale * self.controller_size
        self.upper_teeth_control_data = control.create_control(
            control_name=self.upper_teeth_control_name,
            radius=radius,
            axis="Y+",
            target=self.upper_teeth_joint,
            parent=self.control_group,
            color=self.controller_color,
            create_sub_control=False,
            control_set=config.control_set_name
        )
        self.lower_teeth_control_data = control.create_control(
            control_name=self.lower_teeth_control_name,
            radius=radius,
            axis="Y+",
            target=self.lower_teeth_joint,
            parent=self.control_group,
            color=self.controller_color,
            create_sub_control=False,
            control_set=config.control_set_name
        )
        self.upper_teeth_control = self.upper_teeth_control_data["control"]
        self.lower_teeth_control = self.lower_teeth_control_data["control"]
        return {
            "upper": self.upper_teeth_control_data,
            "lower": self.lower_teeth_control_data,
        }

    def connect_control_to_joint(self, control_output, joint, part):
        mult_matrix = pm.createNode(
            "multMatrix",
            name=name.create_name("mult", "md", part, "control", 1)
        )
        decompose_matrix = pm.createNode(
            "decomposeMatrix",
            name=name.create_name("dcmp", "md", part, "control", 1)
        )
        control_output.worldMatrix[0] >> mult_matrix.matrixIn[0]
        joint_parent = joint.getParent()
        if joint_parent is not None:
            joint_parent.worldInverseMatrix[0] >> mult_matrix.matrixIn[1]
        mult_matrix.matrixSum >> decompose_matrix.inputMatrix
        decompose_matrix.outputTranslate >> joint.translate
        decompose_matrix.outputRotate >> joint.rotate
        self.connection_nodes.append(mult_matrix)
        self.connection_nodes.append(decompose_matrix)
        return {
            "mult_matrix": mult_matrix,
            "decompose_matrix": decompose_matrix,
        }

    def constrain_model(self, joint, model, part):
        if model is None:
            return None
        result = pm.parentConstraint(
            joint,
            model,
            maintainOffset=True,
            name=name.create_name("parent", "md", part, "model", 1)
        )
        if isinstance(result, (list, tuple)):
            constraint = result[0]
        else:
            constraint = result
        self.model_constraints.append(constraint)
        return constraint

    def create_connection(self):
        upper_connection = self.connect_control_to_joint(
            self.upper_teeth_control_data["output"],
            self.upper_teeth_joint,
            "upper_teeth"
        )
        lower_connection = self.connect_control_to_joint(
            self.lower_teeth_control_data["output"],
            self.lower_teeth_joint,
            "lower_teeth"
        )
        upper_constraint = self.constrain_model(
            self.upper_teeth_joint,
            self.upper_teeth_model,
            "upper_teeth"
        )
        lower_constraint = self.constrain_model(
            self.lower_teeth_joint,
            self.lower_teeth_model,
            "lower_teeth"
        )
        return {
            "upper_connection": upper_connection,
            "lower_connection": lower_connection,
            "upper_model_constraint": upper_constraint,
            "lower_model_constraint": lower_constraint,
        }

    def finalize_step(self):
        required_nodes = [
            self.upper_teeth_joint,
            self.lower_teeth_joint,
            self.upper_teeth_control,
            self.lower_teeth_control,
        ]
        for node in required_nodes:
            if node is None or not pm.objExists(node):
                raise RuntimeError(u"Teeth Component 构建结果不完整：{}".format(node))
        return True


__all__ = [
    "TeethComponent",
]
