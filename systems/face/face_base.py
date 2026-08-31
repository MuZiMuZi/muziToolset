# coding=utf-8
u"""
Face Base
=========

所有 Face Rig Component 共用的业务上下文。

FaceBase 只负责：
    - Face 标准层级；
    - Face Setup 公共数据；
    - Face Workflow Step 状态；
    - FaceConfig 访问；
    - RigComponentBase 生命周期继承。

Maya Node 的基础操作直接使用 PyMEL，不再经过通用 Wrapper。
"""

from __future__ import print_function

import pymel.core as pm

from ..component_base import RigComponentBase
from . import config as face_settings
from .face_config import FaceConfig


class FaceBase(RigComponentBase):
    u"""所有 Face Rig Component 共用的基础类。"""

    def __init__(self):
        self.step_value = None

        self.side = face_settings.FACE_SIDE
        self.center_axis = face_settings.CENTER_AXIS

        self.config = FaceConfig()

        self.master_group = None
        self.model_group = None
        self.guide_group = None
        self.control_group = None
        self.joint_group = None
        self.rig_nodes_group = None
        self.position_driver_group = None

        self.tweak_group = None
        self.stretch_group = None
        self.deform_group = None

        self.head_model = None
        self.left_eye_model = None
        self.right_eye_model = None
        self.upper_teeth_model = None
        self.lower_teeth_model = None
        self.tongue_model = None
        self.gum_model = None
        self.mouth_joint_count = None

    @staticmethod
    def _ensure_transform_group(
            name,
            parent=None
    ):
        u"""创建或复用一个 Face 标准 Transform Group。"""
        if pm.objExists(name):
            group = pm.PyNode(name)

            if group.nodeType() != "transform":
                raise RuntimeError(
                    u"Face Group 名称已被非 Transform 节点占用：{}".format(name)
                )
        else:
            group = pm.createNode(
                "transform",
                name=name
            )

        if parent is not None:
            current_parent = group.getParent()

            if current_parent != parent:
                group.setParent(parent)

        return group

    def ensure_hierarchy(self):
        u"""确保 Face Rig 标准层级存在，并缓存对应 PyNode。"""
        self.master_group = self._ensure_transform_group(
            face_settings.MASTER_GROUP_NAME
        )
        self.model_group = self._ensure_transform_group(
            face_settings.MODEL_GROUP_NAME,
            self.master_group
        )
        self.guide_group = self._ensure_transform_group(
            face_settings.GUIDE_GROUP_NAME,
            self.master_group
        )
        self.control_group = self._ensure_transform_group(
            face_settings.CONTROL_GROUP_NAME,
            self.master_group
        )
        self.joint_group = self._ensure_transform_group(
            face_settings.JOINT_GROUP_NAME,
            self.master_group
        )
        self.rig_nodes_group = self._ensure_transform_group(
            face_settings.RIG_NODES_GROUP_NAME,
            self.master_group
        )
        self.position_driver_group = self._ensure_transform_group(
            face_settings.POSITION_DRIVER_GROUP_NAME,
            self.master_group
        )
        self.tweak_group = self._ensure_transform_group(
            face_settings.TWEAK_GROUP_NAME,
            self.model_group
        )
        self.stretch_group = self._ensure_transform_group(
            face_settings.STRETCH_GROUP_NAME,
            self.model_group
        )
        self.deform_group = self._ensure_transform_group(
            face_settings.DEFORM_GROUP_NAME,
            self.model_group
        )

        return {
            "master": self.master_group,
            "model": self.model_group,
            "guide": self.guide_group,
            "control": self.control_group,
            "joint": self.joint_group,
            "rig_nodes": self.rig_nodes_group,
            "position_driver": self.position_driver_group,
            "tweak": self.tweak_group,
            "stretch": self.stretch_group,
            "deform": self.deform_group,
        }

    def refresh_hierarchy(self):
        group_map = {
            "master_group": face_settings.MASTER_GROUP_NAME,
            "model_group": face_settings.MODEL_GROUP_NAME,
            "guide_group": face_settings.GUIDE_GROUP_NAME,
            "control_group": face_settings.CONTROL_GROUP_NAME,
            "joint_group": face_settings.JOINT_GROUP_NAME,
            "rig_nodes_group": face_settings.RIG_NODES_GROUP_NAME,
            "position_driver_group": face_settings.POSITION_DRIVER_GROUP_NAME,
            "tweak_group": face_settings.TWEAK_GROUP_NAME,
            "stretch_group": face_settings.STRETCH_GROUP_NAME,
            "deform_group": face_settings.DEFORM_GROUP_NAME,
        }

        for property_name in group_map:
            node_name = group_map[property_name]
            node = None

            if pm.objExists(node_name):
                node = pm.PyNode(node_name)

            setattr(
                self,
                property_name,
                node
            )

        return True

    def load_setup_data(self):
        u"""从 FaceConfig 读取 Step 01 数据，并缓存为 PyNode。"""
        setup_data = self.config.load_setup()

        self.head_model = setup_data.get("face_head_model")
        self.left_eye_model = setup_data.get("face_lf_eye_model")
        self.right_eye_model = setup_data.get("face_rt_eye_model")
        self.upper_teeth_model = setup_data.get("upper_teeth_model")
        self.lower_teeth_model = setup_data.get("lower_teeth_model")
        self.tongue_model = setup_data.get("face_tongue_model")
        self.gum_model = setup_data.get("face_gum_model")
        self.mouth_joint_count = setup_data.get("mouth_joint_count")

        return {
            "head_model": self.head_model,
            "left_eye_model": self.left_eye_model,
            "right_eye_model": self.right_eye_model,
            "upper_teeth_model": self.upper_teeth_model,
            "lower_teeth_model": self.lower_teeth_model,
            "tongue_model": self.tongue_model,
            "gum_model": self.gum_model,
            "mouth_joint_count": self.mouth_joint_count,
        }

    @staticmethod
    def validate_model(
            model,
            label=u"Model"
    ):
        u"""检查输入必须是带 Mesh Shape 的 Transform PyNode。"""
        if model is None:
            raise RuntimeError(
                u"{} 不能为空。".format(label)
            )

        if isinstance(model, str):
            if not pm.objExists(model):
                raise RuntimeError(
                    u"{} 不存在：{}".format(label, model)
                )

            model = pm.PyNode(model)

        if model.nodeType() == "mesh":
            model = model.getParent()

        if model.nodeType() != "transform":
            raise TypeError(
                u"{} 必须是 Transform：{}".format(label, model)
            )

        mesh_shapes = []

        for shape in model.getShapes(noIntermediate=True):
            if shape.nodeType() == "mesh":
                mesh_shapes.append(shape)

        if not mesh_shapes:
            raise TypeError(
                u"{} 没有有效 Mesh Shape：{}".format(label, model)
            )

        return model

    def validate_setup_data(
            self,
            require_mouth_joint_count=True
    ):
        if not self.config.exists():
            raise RuntimeError(
                u"没有找到 Face Config，请先完成 Face Setup。"
            )

        self.load_setup_data()

        self.head_model = self.validate_model(
            self.head_model,
            u"Face Head Model"
        )

        optional_models = [
            (u"Left Eye Model", "left_eye_model"),
            (u"Right Eye Model", "right_eye_model"),
            (u"Upper Teeth Model", "upper_teeth_model"),
            (u"Lower Teeth Model", "lower_teeth_model"),
            (u"Tongue Model", "tongue_model"),
            (u"Gum Model", "gum_model"),
        ]

        for label, property_name in optional_models:
            model = getattr(self, property_name)

            if model is None:
                continue

            model = self.validate_model(
                model,
                label
            )
            setattr(
                self,
                property_name,
                model
            )

        if require_mouth_joint_count:
            if self.mouth_joint_count is None:
                raise RuntimeError(
                    u"没有读取到 Mouth Joint Count，请先完成 Face Setup。"
                )

        return True

    def set_step_completed(
            self,
            completed=True,
            step_value=None
    ):
        if step_value is None:
            step_value = self.step_value

        if step_value is None:
            raise RuntimeError(
                u"当前 Face Component 没有设置 step_value。"
            )

        return self.config.set_step_completed(
            step_value,
            completed
        )

    def is_step_completed(self, step_value):
        return self.config.is_step_completed(step_value)

    def get_step_status(self):
        return self.config.get_step_status()

    def invalidate_later_steps(self, step_value=None):
        if step_value is None:
            step_value = self.step_value

        if step_value is None:
            raise RuntimeError(
                u"当前 Face Component 没有设置 step_value。"
            )

        return self.config.invalidate_steps_after(step_value)

    def get_current_step(self):
        return self.config.get_current_step()

    def set_current_step(self, step_value):
        return self.config.set_current_step(step_value)

    def apply_step_visibility(self, step_value):
        u"""应用 Face Step Group Visibility。"""
        if step_value not in face_settings.STEP_VISIBILITY_RULES:
            raise ValueError(
                u"不支持的 Face Step：{}".format(step_value)
            )

        self.ensure_hierarchy()

        group_map = {
            "model": self.model_group,
            "guide": self.guide_group,
            "control": self.control_group,
            "joint": self.joint_group,
            "rig_nodes": self.rig_nodes_group,
            "position_driver": self.position_driver_group,
        }
        rules = face_settings.STEP_VISIBILITY_RULES[step_value]

        for group_key in rules:
            group = group_map[group_key]

            if group is None:
                continue

            group.visibility.set(
                bool(rules[group_key])
            )

        return True


__all__ = [
    "FaceBase",
]
