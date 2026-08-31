# coding=utf-8
u"""
Face Config
===========

Face Rig 的持久化数据对象。

FaceConfig 只负责本 Face System 的 Network Node 数据：
    - Setup 模型引用；
    - Workflow Step 状态；
    - Guide 引用和版本；
    - Controller Settings。

它直接使用 PyMEL，不再经过通用 Attr / Config Wrapper。
"""

from __future__ import print_function

import pymel.core as pm

from . import config


class FaceConfig(object):
    u"""一个 Face Rig 的 Scene Config 数据对象。"""

    def __init__(self, node_name=None):
        self.node_name = node_name or config.config_node_name
        self.node = None
        self.refresh()

    def refresh(self):
        u"""重新解析 Scene 中的 Config PyNode。"""
        self.node = None

        if pm.objExists(self.node_name):
            node = pm.PyNode(
                self.node_name
            )

            if node.nodeType() != "network":
                raise RuntimeError(
                    u"Face Config 名称已被非 Network 节点占用：{}".format(
                        self.node_name
                    )
                )

            self.node = node

        return self.node

    def exists(self):
        return self.refresh() is not None

    def ensure(self):
        node = self.refresh()

        if node is not None:
            return node

        self.node = pm.createNode(
            "network",
            name=self.node_name
        )
        return self.node

    def delete(self):
        node = self.refresh()

        if node is None:
            return False

        pm.delete(node)
        self.node = None
        return True

    def has_attribute(self, attribute_name):
        node = self.refresh()

        if node is None:
            return False

        return node.hasAttr(attribute_name)

    def _ensure_attribute(
            self,
            attribute_name,
            attribute_type
    ):
        node = self.ensure()

        if node.hasAttr(attribute_name):
            return node.attr(attribute_name)

        if attribute_type == "string":
            node.addAttr(
                attribute_name,
                dataType="string"
            )
        else:
            node.addAttr(
                attribute_name,
                attributeType=attribute_type
            )

        return node.attr(attribute_name)

    def _ensure_message_attribute(self, attribute_name):
        return self._ensure_attribute(
            attribute_name,
            "message"
        )

    def get_node(self, attribute_name):
        u"""读取一个 Message Attribute 保存的 PyNode。"""
        if not self.has_attribute(attribute_name):
            return None

        plug = self.node.attr(attribute_name)
        inputs = plug.inputs()

        if not inputs:
            return None

        return inputs[0]

    def set_node(
            self,
            attribute_name,
            scene_node
    ):
        u"""把一个 Maya Node 通过 Message Connection 保存到 Config。"""
        plug = self._ensure_message_attribute(
            attribute_name
        )

        input_plugs = plug.inputs(plugs=True)

        for input_plug in input_plugs:
            pm.disconnectAttr(
                input_plug,
                plug
            )

        if scene_node is None:
            return None

        if isinstance(scene_node, str):
            if not pm.objExists(scene_node):
                raise RuntimeError(
                    u"需要保存到 Face Config 的节点不存在：{}".format(
                        scene_node
                    )
                )

            scene_node = pm.PyNode(scene_node)

        scene_node.message.connect(
            plug,
            force=True
        )
        return scene_node

    def get_nodes(self, attribute_names):
        result = {}

        for attribute_name in attribute_names:
            result[attribute_name] = self.get_node(attribute_name)

        return result

    def set_nodes(self, values):
        result = {}

        for attribute_name in values:
            result[attribute_name] = self.set_node(
                attribute_name,
                values[attribute_name]
            )

        return result

    def get_value(
            self,
            attribute_name,
            default=None
    ):
        if not self.has_attribute(attribute_name):
            return default

        return self.node.attr(attribute_name).get()

    def set_value(
            self,
            attribute_name,
            value,
            attribute_type="double"
    ):
        plug = self._ensure_attribute(
            attribute_name,
            attribute_type
        )

        if plug.isLocked():
            plug.unlock()

        plug.set(value)
        return value

    def get_values(self, attribute_names):
        result = {}

        for attribute_name in attribute_names:
            result[attribute_name] = self.get_value(attribute_name)

        return result

    def set_values(
            self,
            values,
            attribute_types=None
    ):
        if attribute_types is None:
            attribute_types = {}

        result = {}

        for attribute_name in values:
            attribute_type = attribute_types.get(
                attribute_name,
                "double"
            )
            result[attribute_name] = self.set_value(
                attribute_name,
                values[attribute_name],
                attribute_type
            )

        return result

    def save_setup(
            self,
            head_model,
            left_eye_model=None,
            right_eye_model=None,
            upper_teeth_model=None,
            lower_teeth_model=None,
            tongue_model=None,
            gum_model=None,
            mouth_joint_count=32
    ):
        node_values = {
            "face_head_model": head_model,
            "face_lf_eye_model": left_eye_model,
            "face_rt_eye_model": right_eye_model,
            "upper_teeth_model": upper_teeth_model,
            "lower_teeth_model": lower_teeth_model,
            "face_tongue_model": tongue_model,
            "face_gum_model": gum_model,
        }

        self.set_nodes(node_values)
        self.set_value(
            "mouth_joint_count",
            int(mouth_joint_count),
            "long"
        )
        return self.load_setup()

    def load_setup(self):
        result = self.get_nodes(
            config.setup_node_attributes
        )
        result["mouth_joint_count"] = self.get_value(
            "mouth_joint_count"
        )
        return result

    @staticmethod
    def _step_completed_attribute(step_value):
        attribute_name = config.step_completed_attributes.get(step_value)

        if attribute_name is None:
            raise ValueError(
                u"不支持的 Face Step：{}".format(step_value)
            )

        return attribute_name

    def get_current_step(self):
        value = self.get_value(
            config.current_step_attribute,
            1
        )

        if value is None:
            return 1

        value = int(value)

        if value < 1:
            return 1
        if value > config.last_step:
            return config.last_step
        return value

    def set_current_step(self, step_value):
        if not isinstance(step_value, int):
            raise TypeError(u"Face Step 必须是整数。")

        if step_value < 1 or step_value > config.last_step:
            raise ValueError(
                u"Face Step 必须在 1～{}。".format(config.last_step)
            )

        return self.set_value(
            config.current_step_attribute,
            step_value,
            "long"
        )

    def is_step_completed(self, step_value):
        attribute_name = self._step_completed_attribute(step_value)
        return bool(
            self.get_value(
                attribute_name,
                False
            )
        )

    def set_step_completed(
            self,
            step_value,
            completed=True
    ):
        attribute_name = self._step_completed_attribute(step_value)
        return self.set_value(
            attribute_name,
            bool(completed),
            "bool"
        )

    def get_step_status(self):
        result = {}
        step_value = 1

        while step_value <= config.last_step:
            result[step_value] = self.is_step_completed(step_value)
            step_value += 1

        return result

    def invalidate_steps_after(self, step_value):
        current_step = step_value + 1

        while current_step <= config.last_step:
            self.set_step_completed(
                current_step,
                False
            )
            current_step += 1

        return True

    def save_guide(
            self,
            guide_root,
            move_control,
            guide_version
    ):
        self.set_node(
            config.guide_root_attribute,
            guide_root
        )
        self.set_node(
            config.guide_move_control_attribute,
            move_control
        )
        self.set_value(
            config.guide_version_attribute,
            str(guide_version),
            "string"
        )
        return self.load_guide()

    def load_guide(self):
        return {
            "guide_root": self.get_node(config.guide_root_attribute),
            "move_control": self.get_node(config.guide_move_control_attribute),
            "guide_version": self.get_value(config.guide_version_attribute),
        }

    def clear_guide(self):
        self.set_node(
            config.guide_root_attribute,
            None
        )
        self.set_node(
            config.guide_move_control_attribute,
            None
        )
        return True

    def save_controller_settings(self, settings):
        for attribute_name in settings:
            attribute_type = config.controller_setting_types.get(
                attribute_name,
                "double"
            )
            self.set_value(
                attribute_name,
                settings[attribute_name],
                attribute_type
            )

        return self.load_controller_settings()

    def load_controller_settings(self):
        result = {}

        for attribute_name in config.controller_default_settings:
            default_value = config.controller_default_settings[attribute_name]
            result[attribute_name] = self.get_value(
                attribute_name,
                default_value
            )

        return result


__all__ = [
    "FaceConfig",
]
