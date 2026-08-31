# coding=utf-8
u"""
Face Guide
==========

Face Rig Step 02 的 PyMEL-first Guide System。

负责模板导入 / 重导、Guide 查询、左右镜像、验证和持久化。
"""

from __future__ import print_function

import os
import re

import pymel.core as pm

from ....core import name
from ....core.undo import undo_chunk
from .. import config
from ..face_base import FaceBase


guide_locator_pattern = re.compile(
    r'createNode\s+transform\s+-n\s+"(loc_[^"]+_guide_\d+)"'
)


class FaceGuide(FaceBase):
    u"""Face Rig Step 02。"""

    mirror_sides = ["lf", "rt"]

    zero_attributes = [
        "translateX", "translateY", "translateZ",
        "rotateX", "rotateY", "rotateZ",
        "scaleX", "scaleY", "scaleZ", "rotateOrder",
    ]

    locator_attributes = [
        "translateX", "translateY", "translateZ",
        "rotateX", "rotateY", "rotateZ",
        "scaleX", "scaleY", "scaleZ", "rotateOrder", "visibility",
    ]

    locator_shape_attributes = [
        "localPositionX", "localPositionY", "localPositionZ",
        "localScaleX", "localScaleY", "localScaleZ",
    ]

    def __init__(self):
        super(FaceGuide, self).__init__()
        self.step_value = 2
        self.guide_root = None
        self.guide_move_control = None
        self.validation_result = None
        self.template_locator_names = None

        if self.config.exists():
            self.load_setup_data()

        self.refresh_guide_handles()

    # -------------------------------------------------------------------------
    # Component lifecycle
    # -------------------------------------------------------------------------

    def collect_inputs(self):
        self.validate_setup_data(require_mouth_joint_count=True)
        self.refresh_guide_handles()

        if not self.guide_exists():
            raise RuntimeError(u"Face Guide 尚未完整加载。")

        return True

    def prepare_data(self):
        self.ensure_hierarchy()
        self.config.ensure()
        return True

    def process_data(self):
        self.validation_result = self.validate_guides()

        if self.validation_result["valid"]:
            return self.validation_result

        message = u"Face Guide Validation 失败："
        for error in self.validation_result["errors"]:
            message += u"\n- {}".format(error)

        raise RuntimeError(message)

    def finalize_step(self):
        self.save_guide_config()
        self.set_step_completed(True)
        self.invalidate_later_steps()
        self.set_current_step(3)
        return True

    # -------------------------------------------------------------------------
    # Template
    # -------------------------------------------------------------------------

    @staticmethod
    def get_guide_template_path():
        return os.path.normpath(config.guide_template_path)

    def validate_guide_template_file(self):
        template_path = self.get_guide_template_path()

        if not os.path.isfile(template_path):
            raise RuntimeError(
                u"Face Guide 模板文件不存在：{}".format(template_path)
            )

        return template_path

    def get_template_locator_names(self, refresh=False):
        if self.template_locator_names is not None and not refresh:
            return list(self.template_locator_names)

        template_path = self.validate_guide_template_file()

        with open(template_path, "rb") as file_object:
            template_text = file_object.read().decode("latin-1")

        locator_names = []
        matches = guide_locator_pattern.findall(template_text)

        for locator_name in matches:
            if locator_name not in locator_names:
                locator_names.append(locator_name)

        if not locator_names:
            raise RuntimeError(
                u"Face Guide 模板中没有读取到 Locator：{}".format(template_path)
            )

        self.template_locator_names = locator_names
        return list(locator_names)

    @staticmethod
    def get_temporary_guide_name():
        return name.create_unique_name(
            node_type="grp",
            side="md",
            part="face",
            function="guide_container"
        )

    @staticmethod
    def get_imported_template_root(imported_nodes):
        candidates = []

        for node in imported_nodes:
            if isinstance(node, str):
                if not pm.objExists(node):
                    continue
                node = pm.PyNode(node)

            if node.nodeType() != "transform":
                continue
            if node.getParent() is not None:
                continue
            if node.nodeName() != config.guide_group_name:
                continue

            candidates.append(node)

        if len(candidates) != 1:
            raise RuntimeError(
                u"无法唯一识别 Face Guide Template Root，候选数量：{}".format(
                    len(candidates)
                )
            )

        return candidates[0]

    def remove_guide_content(self):
        self.ensure_hierarchy()

        for child in self.guide_group.getChildren():
            pm.delete(child)

        self.config.clear_guide()
        self.refresh_guide_handles()
        return True

    def build_guide(self):
        self.validate_setup_data(require_mouth_joint_count=True)
        self.ensure_hierarchy()
        self.config.ensure()

        if self.guide_exists():
            return {
                "imported": False,
                "guide_root": self.guide_root,
                "guide_move_control": self.guide_move_control,
                "new_nodes": [],
            }

        if self.guide_group.getChildren():
            raise RuntimeError(
                u"Face Guide Group 中存在未知内容，无法安全导入模板：{}".format(
                    self.guide_group
                )
            )

        template_path = self.validate_guide_template_file()
        temporary_container = self.guide_group.rename(
            self.get_temporary_guide_name()
        )
        imported_nodes = []

        with undo_chunk("build_face_guide"):
            try:
                imported_nodes = pm.importFile(
                    template_path,
                    ignoreVersion=True,
                    returnNewNodes=True
                )
                template_root = self.get_imported_template_root(imported_nodes)
                template_root.setParent(self.master_group)

                if pm.objExists(temporary_container):
                    pm.delete(temporary_container)
            except Exception:
                for imported_node in imported_nodes:
                    if pm.objExists(imported_node):
                        try:
                            pm.delete(imported_node)
                        except Exception:
                            pass

                if pm.objExists(temporary_container):
                    temporary_container.rename(config.guide_group_name)
                raise

        self.refresh_hierarchy()
        self.refresh_guide_handles()

        if not self.guide_exists():
            raise RuntimeError(
                u"Face Guide 模板导入完成，但没有找到 Move Control：{}".format(
                    config.guide_move_control_name
                )
            )

        self.apply_mirror("lf", "rt")
        self.save_guide_config()
        self.set_step_completed(False)
        self.invalidate_later_steps()

        return {
            "imported": True,
            "guide_root": self.guide_root,
            "guide_move_control": self.guide_move_control,
            "new_nodes": imported_nodes,
        }

    def capture_guide_state(self):
        state = {
            "move_control_matrix": None,
            "locators": {},
        }
        self.refresh_guide_handles()

        if self.guide_move_control is not None:
            state["move_control_matrix"] = self.guide_move_control.getMatrix(
                worldSpace=True
            )

        for locator in self.get_guide_locators():
            state["locators"][locator.nodeName()] = locator.getMatrix(
                worldSpace=True
            )

        return state

    @staticmethod
    def set_world_matrix_preserve_lock(node, matrix_value):
        attributes = [
            "translateX", "translateY", "translateZ",
            "rotateX", "rotateY", "rotateZ",
            "scaleX", "scaleY", "scaleZ",
        ]
        lock_states = {}

        for attribute_name in attributes:
            if not node.hasAttr(attribute_name):
                continue
            plug = node.attr(attribute_name)
            lock_states[attribute_name] = plug.isLocked()
            if plug.isLocked():
                plug.unlock()

        try:
            node.setMatrix(matrix_value, worldSpace=True)
        finally:
            for attribute_name in lock_states:
                if lock_states[attribute_name]:
                    node.attr(attribute_name).lock()

        return node

    def restore_guide_state(self, state):
        restored = []
        self.refresh_guide_handles()

        matrix_value = state.get("move_control_matrix")
        if matrix_value is not None and self.guide_move_control is not None:
            self.set_world_matrix_preserve_lock(
                self.guide_move_control,
                matrix_value
            )

        locator_states = state.get("locators", {})
        for locator_name in locator_states:
            locator = self.get_guide_node(locator_name, required=False)
            if locator is None:
                continue
            self.set_world_matrix_preserve_lock(
                locator,
                locator_states[locator_name]
            )
            restored.append(locator)

        return restored

    def reimport_guide(self):
        self.validate_setup_data(require_mouth_joint_count=True)
        state = self.capture_guide_state()

        with undo_chunk("reimport_face_guide"):
            self.remove_guide_content()
            self.build_guide()
            restored = self.restore_guide_state(state)

        self.set_step_completed(False)
        self.invalidate_later_steps()
        self.save_guide_config()

        return {
            "restored_count": len(restored),
            "template_locator_count": len(self.get_template_locator_names()),
        }

    # -------------------------------------------------------------------------
    # Query
    # -------------------------------------------------------------------------

    def refresh_guide_handles(self):
        self.refresh_hierarchy()
        self.guide_root = self.guide_group
        self.guide_move_control = None

        if self.guide_group is None:
            return False

        self.guide_move_control = self.get_guide_node(
            config.guide_move_control_name,
            required=False
        )
        return self.guide_move_control is not None

    def guide_exists(self):
        self.refresh_guide_handles()
        return self.guide_root is not None and self.guide_move_control is not None

    def get_guide_node(self, short_name, required=False):
        if not short_name:
            if required:
                raise RuntimeError(u"Guide 节点名称不能为空。")
            return None

        self.refresh_hierarchy()
        if self.guide_group is None:
            if required:
                raise RuntimeError(
                    u"Face Guide Group 不存在：{}".format(config.guide_group_name)
                )
            return None

        candidates = []
        nodes = [self.guide_group]
        nodes.extend(self.guide_group.listRelatives(allDescendents=True, type="transform"))

        for node in nodes:
            if node.nodeName() == short_name:
                candidates.append(node)

        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) > 1:
            raise RuntimeError(u"Face Guide 中存在多个同名节点：{}".format(short_name))
        if required:
            raise RuntimeError(u"没有找到 Face Guide 节点：{}".format(short_name))
        return None

    @staticmethod
    def get_locator_shapes(locator):
        shapes = []
        for shape in locator.getShapes(noIntermediate=True):
            if shape.nodeType() == "locator":
                shapes.append(shape)
        return shapes

    def get_guide_locators(self):
        self.refresh_hierarchy()
        if self.guide_group is None:
            return []

        locators = []
        descendants = self.guide_group.listRelatives(
            allDescendents=True,
            type="transform"
        )

        for node in descendants:
            short_name = node.nodeName()
            if not short_name.startswith("loc_"):
                continue
            if "_guide_" not in short_name:
                continue
            if not self.get_locator_shapes(node):
                continue
            locators.append(node)

        locators.sort(key=str)
        return locators

    def get_guides_from_names(self, guide_names, required=True):
        guides = []
        for guide_name in guide_names:
            guide = self.get_guide_node(guide_name, required=required)
            if guide is not None:
                guides.append(guide)
        return guides

    def get_part_guides(self, part, side=None, required=False):
        if not part:
            raise ValueError(u"part 不能为空。")

        part_token = "_{}_".format(str(part).strip().lower())
        side_token = None

        if side is not None:
            side_token = "_{}_".format(name.normalize_side(side))

        guides = []
        for locator in self.get_guide_locators():
            short_name = locator.nodeName().lower()
            if part_token not in short_name:
                continue
            if side_token is not None and side_token not in short_name:
                continue
            guides.append(locator)

        guides.sort(key=str)

        if required and not guides:
            raise RuntimeError(u"没有找到 {} Guide。".format(part))

        return guides

    @staticmethod
    def get_guide_positions(guides):
        positions = []
        for guide in guides:
            positions.append(tuple(guide.getTranslation(space="world")))
        return positions

    def get_lip_guides(self, required=True):
        upper_names = [
            name.create_name("loc", "rt", "mouth", "corner_guide", 1),
            name.create_name("loc", "rt", "upper", "lip_guide", 2),
            name.create_name("loc", "rt", "upper", "lip_guide", 1),
            name.create_name("loc", "md", "upper", "lip_guide", 1),
            name.create_name("loc", "lf", "upper", "lip_guide", 1),
            name.create_name("loc", "lf", "upper", "lip_guide", 2),
            name.create_name("loc", "lf", "mouth", "corner_guide", 1),
        ]
        lower_names = [
            name.create_name("loc", "rt", "mouth", "corner_guide", 1),
            name.create_name("loc", "rt", "lower", "lip_guide", 2),
            name.create_name("loc", "rt", "lower", "lip_guide", 1),
            name.create_name("loc", "md", "lower", "lip_guide", 1),
            name.create_name("loc", "lf", "lower", "lip_guide", 1),
            name.create_name("loc", "lf", "lower", "lip_guide", 2),
            name.create_name("loc", "lf", "mouth", "corner_guide", 1),
        ]
        corner_names = [upper_names[0], upper_names[-1]]
        return {
            "upper": self.get_guides_from_names(upper_names, required),
            "lower": self.get_guides_from_names(lower_names, required),
            "corners": self.get_guides_from_names(corner_names, required),
        }

    def get_eyelid_guides(self, side, required=True):
        side = name.normalize_side(side)
        if side not in self.mirror_sides:
            raise ValueError(u"Eyelid side 必须是 lf 或 rt。")

        inner_name = name.create_name("loc", side, "inner", "lid_guide", 1)
        outer_name = name.create_name("loc", side, "outer", "lid_guide", 1)
        upper_names = [
            inner_name,
            name.create_name("loc", side, "upper", "lid_guide", 1),
            name.create_name("loc", side, "upper", "lid_guide", 2),
            name.create_name("loc", side, "upper", "lid_guide", 3),
            outer_name,
        ]
        lower_names = [
            inner_name,
            name.create_name("loc", side, "lower", "lid_guide", 1),
            name.create_name("loc", side, "lower", "lid_guide", 2),
            name.create_name("loc", side, "lower", "lid_guide", 3),
            outer_name,
        ]
        return {
            "upper": self.get_guides_from_names(upper_names, required),
            "lower": self.get_guides_from_names(lower_names, required),
        }

    def get_brow_guides(self, side):
        all_guides = self.get_part_guides("brow", side)
        main_guide = None
        point_guides = []

        for guide in all_guides:
            if "_brow_main_" in guide.nodeName():
                main_guide = guide
            else:
                point_guides.append(guide)

        return {
            "main": main_guide,
            "points": point_guides,
            "all": all_guides,
        }

    def get_eye_guides(self, side, required=False):
        side = name.normalize_side(side)
        if side not in self.mirror_sides:
            raise ValueError(u"Eye side 必须是 lf 或 rt。")

        return {
            "eye_ball": self.get_guide_node(
                name.create_name("loc", side, "eye", "ball_guide", 1),
                required
            ),
            "eye_iris": self.get_guide_node(
                name.create_name("loc", side, "eye", "iris_guide", 1),
                required
            ),
        }

    # -------------------------------------------------------------------------
    # Mirror
    # -------------------------------------------------------------------------

    def validate_mirror_sides(self, source_side, target_side):
        source_side = name.normalize_side(source_side)
        target_side = name.normalize_side(target_side)

        if source_side not in self.mirror_sides or target_side not in self.mirror_sides:
            raise ValueError(u"Mirror side 必须是 lf 或 rt。")
        if source_side == target_side:
            raise ValueError(u"Mirror Source / Target Side 不能相同。")

        return source_side, target_side

    def get_side_zero_groups(self, side):
        side = name.normalize_side(side)
        prefix = "zero_{}_".format(side)
        groups = []

        for node in self.guide_group.listRelatives(allDescendents=True, type="transform"):
            if node.nodeName().startswith(prefix):
                groups.append(node)

        groups.sort(key=lambda item: item.longName().count("|"))
        return groups

    @staticmethod
    def get_side_locator(zero_group, side):
        prefix = "loc_{}_".format(side)
        for child in zero_group.getChildren(type="transform"):
            if child.nodeName().startswith(prefix):
                return child
        return None

    @staticmethod
    def capture_attributes(node, attributes):
        values = {}
        if node is None:
            return values

        for attribute_name in attributes:
            if not node.hasAttr(attribute_name):
                continue
            values[attribute_name] = node.attr(attribute_name).get()
        return values

    @staticmethod
    def disconnect_input(plug):
        for input_plug in plug.inputs(plugs=True):
            pm.disconnectAttr(input_plug, plug)

    @staticmethod
    def set_attribute_preserve_lock(node, attribute_name, value):
        if not node.hasAttr(attribute_name):
            return False
        plug = node.attr(attribute_name)
        was_locked = plug.isLocked()
        if was_locked:
            plug.unlock()
        try:
            plug.set(value)
        finally:
            if was_locked:
                plug.lock()
        return True

    def copy_attribute(self, source_node, target_node, attribute_name):
        if not source_node.hasAttr(attribute_name) or not target_node.hasAttr(attribute_name):
            return False
        target_plug = target_node.attr(attribute_name)
        self.disconnect_input(target_plug)
        return self.set_attribute_preserve_lock(
            target_node,
            attribute_name,
            source_node.attr(attribute_name).get()
        )

    def capture_side_state(self, side):
        snapshot = {"side": side, "items": []}

        for zero_group in self.get_side_zero_groups(side):
            locator = self.get_side_locator(zero_group, side)
            item = {
                "zero_name": zero_group.nodeName(),
                "zero_values": self.capture_attributes(zero_group, self.zero_attributes),
                "locator_name": None,
                "locator_values": {},
                "locator_shape_values": {},
            }

            if locator is not None:
                item["locator_name"] = locator.nodeName()
                item["locator_values"] = self.capture_attributes(
                    locator,
                    self.locator_attributes
                )
                shapes = self.get_locator_shapes(locator)
                if shapes:
                    item["locator_shape_values"] = self.capture_attributes(
                        shapes[0],
                        self.locator_shape_attributes
                    )

            snapshot["items"].append(item)

        return snapshot

    def restore_attributes(self, node, values):
        for attribute_name in values:
            if not node.hasAttr(attribute_name):
                continue
            plug = node.attr(attribute_name)
            self.disconnect_input(plug)
            self.set_attribute_preserve_lock(node, attribute_name, values[attribute_name])
        return True

    def restore_mirror_snapshot(self, snapshot):
        if not isinstance(snapshot, dict):
            raise TypeError(u"Mirror Snapshot 必须是 dict。")

        restored_count = 0
        for item in snapshot.get("items", []):
            zero_group = self.get_guide_node(item.get("zero_name"), required=False)
            if zero_group is None:
                continue

            self.restore_attributes(zero_group, item.get("zero_values", {}))
            locator_name = item.get("locator_name")

            if locator_name:
                locator = self.get_guide_node(locator_name, required=False)
                if locator is not None:
                    self.restore_attributes(locator, item.get("locator_values", {}))
                    shapes = self.get_locator_shapes(locator)
                    if shapes:
                        self.restore_attributes(
                            shapes[0],
                            item.get("locator_shape_values", {})
                        )

            restored_count += 1

        self.set_step_completed(False)
        self.invalidate_later_steps()
        return {"restored_count": restored_count}

    def mirror_zero_group(self, source_zero, target_zero, source_side):
        source_parent = source_zero.getParent()
        is_mirror_root = True

        if source_parent is not None:
            if "_{}_".format(source_side) in source_parent.nodeName():
                is_mirror_root = False

        if is_mirror_root:
            self.set_attribute_preserve_lock(
                target_zero, "translateX", -source_zero.translateX.get()
            )
            self.set_attribute_preserve_lock(
                target_zero, "scaleX", -source_zero.scaleX.get()
            )
            direct_attributes = [
                "translateY", "translateZ",
                "rotateX", "rotateY", "rotateZ",
                "scaleY", "scaleZ", "rotateOrder",
            ]
            for attribute_name in direct_attributes:
                self.copy_attribute(source_zero, target_zero, attribute_name)
        else:
            for attribute_name in self.zero_attributes:
                self.copy_attribute(source_zero, target_zero, attribute_name)

        return True

    def mirror_locator(self, source_locator, target_locator):
        for attribute_name in self.locator_attributes:
            self.copy_attribute(source_locator, target_locator, attribute_name)

        source_shapes = self.get_locator_shapes(source_locator)
        target_shapes = self.get_locator_shapes(target_locator)

        if source_shapes and target_shapes:
            for attribute_name in self.locator_shape_attributes:
                self.copy_attribute(source_shapes[0], target_shapes[0], attribute_name)
        return True

    def apply_mirror(self, source_side, target_side):
        source_side, target_side = self.validate_mirror_sides(source_side, target_side)

        if not self.guide_exists():
            raise RuntimeError(u"Face Guide 尚未加载。")

        mirrored_count = 0
        for source_zero in self.get_side_zero_groups(source_side):
            target_zero = self.get_guide_node(
                name.mirror_name(source_zero.nodeName()),
                required=True
            )
            source_locator = self.get_side_locator(source_zero, source_side)
            if source_locator is None:
                continue
            target_locator = self.get_guide_node(
                name.mirror_name(source_locator.nodeName()),
                required=True
            )
            self.mirror_zero_group(source_zero, target_zero, source_side)
            self.mirror_locator(source_locator, target_locator)
            mirrored_count += 1

        self.set_step_completed(False)
        self.invalidate_later_steps()
        return {
            "source_side": source_side,
            "target_side": target_side,
            "count": mirrored_count,
        }

    def mirror_guides(self, source_side, target_side):
        with undo_chunk("mirror_face_guides"):
            snapshot = self.capture_side_state(target_side)
            result = self.apply_mirror(source_side, target_side)
            result["snapshot"] = snapshot
        return result

    def undo_mirror(self, snapshot):
        with undo_chunk("undo_face_guide_mirror"):
            return self.restore_mirror_snapshot(snapshot)

    # -------------------------------------------------------------------------
    # Validation / config
    # -------------------------------------------------------------------------

    def validate_guides(self):
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "guide_count": 0,
            "template_guide_count": 0,
            "missing_guide_names": [],
            "unexpected_guide_names": [],
        }

        self.refresh_hierarchy()
        if self.guide_group is None:
            result["errors"].append(
                u"Face Guide Group 不存在：{}".format(config.guide_group_name)
            )
            result["valid"] = False
            return result

        locators = self.get_guide_locators()
        expected_names = self.get_template_locator_names()
        current_names = []
        name_counts = {}

        result["guide_count"] = len(locators)
        result["template_guide_count"] = len(expected_names)

        for locator in locators:
            short_name = locator.nodeName()
            current_names.append(short_name)
            name_counts[short_name] = name_counts.get(short_name, 0) + 1

        for expected_name in expected_names:
            if expected_name not in current_names:
                result["missing_guide_names"].append(expected_name)
                result["errors"].append(u"缺少模板定位器：{}".format(expected_name))

        for short_name in name_counts:
            if name_counts[short_name] > 1:
                result["errors"].append(
                    u"Guide 短名称重复：{} x {}".format(
                        short_name,
                        name_counts[short_name]
                    )
                )

        for current_name in current_names:
            if current_name not in expected_names:
                result["unexpected_guide_names"].append(current_name)

        if result["unexpected_guide_names"]:
            result["warnings"].append(
                u"当前 Guide 中存在模板之外的 Locator；不会阻止下一步。"
            )
        if result["errors"]:
            result["valid"] = False
        return result

    def save_guide_config(self):
        self.refresh_guide_handles()
        if self.guide_root is None:
            raise RuntimeError(u"没有可保存的 Face Guide Root。")
        if self.guide_move_control is None:
            raise RuntimeError(u"没有可保存的 Face Guide Move Control。")

        return self.config.save_guide(
            guide_root=self.guide_root,
            move_control=self.guide_move_control,
            guide_version=config.guide_version
        )

    @staticmethod
    def get_default_controller_settings():
        settings = {}
        for attribute_name in config.controller_default_settings:
            settings[attribute_name] = config.controller_default_settings[attribute_name]
        return settings

    @staticmethod
    def validate_controller_settings(settings):
        if not isinstance(settings, dict):
            raise TypeError(u"Controller Settings 必须是 dict。")

        global_scale = settings.get(config.controller_global_scale_attribute)
        if global_scale is None or float(global_scale) <= 0.0:
            raise ValueError(u"Face Controller Global Scale 必须大于 0。")

        for module_name in config.controller_size_attributes:
            attribute_name = config.controller_size_attributes[module_name]
            value = settings.get(attribute_name)
            if value is None or float(value) <= 0.0:
                raise ValueError(u"Controller Size 必须大于 0：{}".format(attribute_name))

        for side in config.controller_color_attributes:
            attribute_name = config.controller_color_attributes[side]
            value = settings.get(attribute_name)
            if value is None:
                raise ValueError(u"缺少 Controller Color：{}".format(attribute_name))
            color_index = int(value)
            if color_index < 0 or color_index > 31:
                raise ValueError(u"Maya Index Color 必须在 0～31：{}".format(attribute_name))

        return True

    def load_controller_settings(self):
        settings = self.get_default_controller_settings()
        if not self.config.exists():
            return settings

        saved_settings = self.config.load_controller_settings()
        for attribute_name in saved_settings:
            if saved_settings[attribute_name] is not None:
                settings[attribute_name] = saved_settings[attribute_name]
        return settings

    def save_controller_settings(self, settings):
        self.validate_controller_settings(settings)
        return self.config.save_controller_settings(settings)


__all__ = [
    "FaceGuide",
]
