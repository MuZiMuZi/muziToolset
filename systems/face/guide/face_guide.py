# coding=utf-8
u"""
Step 02 - Face Guide
====================

Face Guide 的单文件 Step 02 实现。

职责：
    1. 组织 Step 02 生命周期；
    2. 导入 / 重新导入 Face Guide Template；
    3. 提供通用 Guide 查询；
    4. 提供 LF / RT Mirror 和单步撤销；
    5. 检查模板中的全部 Locator 是否完整；
    6. 保存 Guide 和 Controller Settings 到 Face Config；
    7. Step 02 完成后把 Workflow 推进到 Step 03。

设计原则：
    - Face 固定名称和默认参数统一放 systems.face.config；
    - 标准 Rig Name 统一继承 FaceBase -> RigBase；
    - DAG Parent / Child / Descendant 查询统一复用 hierarchy_utils；
    - 不为简单 part 查询额外创建 get_xxx_guides() 包装；
    - 只有需要固定顺序或结构化结果的查询保留专用方法；
    - Template / Mirror 都属于 FaceGuide 自己的 Step 02 行为；
    - Controller Config Attribute 只使用当前正式 Schema，不维护旧属性兼容。
"""

from __future__ import print_function

import os
import re

import maya.cmds as cmds

from ....core import connection_utils
from ....core import hierarchy_utils
from ....core import rename_utils
from ....core import scene_utils
from ....core import transform_utils
from .. import config
from .. import face_base


guide_locator_pattern = re.compile(
    r'createNode\s+transform\s+-n\s+"(loc_[^"]+_guide_\d+)"'
)


class FaceGuide(face_base.FaceBase):
    u"""Face Rig Step 02 - Guide。"""

    guide_template_file_name = config.face_guide_template_file_name
    guide_template_path = config.face_guide_template_path
    guide_move_ctrl_name = config.face_guide_move_ctrl
    guide_version = config.face_guide_version

    mirror_sides = [
        "lf",
        "rt",
    ]

    zero_attributes = [
        "translateX",
        "translateY",
        "translateZ",
        "rotateX",
        "rotateY",
        "rotateZ",
        "scaleX",
        "scaleY",
        "scaleZ",
        "rotateOrder",
    ]

    locator_attributes = [
        "translateX",
        "translateY",
        "translateZ",
        "rotateX",
        "rotateY",
        "rotateZ",
        "scaleX",
        "scaleY",
        "scaleZ",
        "rotateOrder",
        "visibility",
    ]

    locator_shape_attributes = [
        "localPositionX",
        "localPositionY",
        "localPositionZ",
        "localScaleX",
        "localScaleY",
        "localScaleZ",
    ]

    def __init__(self):
        u"""初始化 Face Guide Step。"""
        super(FaceGuide, self).__init__()

        self.step_value = 2
        self.guide_root = None
        self.guide_move_ctrl = None
        self.validation_result = None
        self.template_locator_names = None

        if self.config_node_exists():
            self.refresh_setup_data()

        self.refresh_guide_handles()

    # =========================================================================
    # Step Lifecycle
    # =========================================================================

    def collect_inputs(self):
        u"""检查 Step 01 和当前 Guide 是否可以正式提交。"""
        self.validate_setup()
        self.refresh_guide_handles()

        if not self.guide_exists():
            raise RuntimeError(
                u"Face Guide 尚未完整加载，请重新导入模板后再继续。"
            )

        return True

    def prepare_data(self):
        u"""确保 Face Hierarchy 和 Config 可以保存 Step 02。"""
        self.ensure_hierarchy()

        self.step_config_attr_names[2] = list(
            config.face_step_02_config_attr_names
        )

        self.ensure_config_layout()
        return True

    def process_data(self):
        u"""执行完整 Guide Validation。"""
        self.validation_result = self.validate_guides()

        if self.validation_result["valid"]:
            return self.validation_result

        error_message = u"Face Guide Validation 失败："

        for error in self.validation_result["errors"]:
            error_message += u"\n- {}".format(
                error
            )

        raise RuntimeError(
            error_message
        )

    def finalize_step(self):
        u"""保存 Guide，并把 Step 02 正式标记为完成。"""
        self.save_guide_config()

        self.set_step_completed(
            completed=True
        )
        self.invalidate_later_steps()
        self.set_current_step_value(
            3
        )
        self.organize_config_attributes()
        return True

    # =========================================================================
    # Setup / Template
    # =========================================================================

    def validate_setup(self):
        u"""检查 Step 02 所依赖的 Step 01 数据。"""
        return self.validate_setup_config(
            require_mouth_jnt_number=True
        )

    def get_guide_template_path(self):
        u"""返回 Face Guide Template 路径。"""
        return os.path.normpath(
            self.guide_template_path
        )

    def validate_guide_template_file(self):
        u"""检查 Face Guide Template 文件是否存在。"""
        return scene_utils.validate_scene_file(
            self.get_guide_template_path()
        )

    def get_template_locator_names(self, refresh=False):
        u"""从 face_guide.ma 读取全部标准 Locator 名称。"""
        if self.template_locator_names is not None:
            if not refresh:
                return list(
                    self.template_locator_names
                )

        template_path = self.validate_guide_template_file()

        with open(template_path, "rb") as file_object:
            file_data = file_object.read()

        template_text = file_data.decode(
            "latin-1"
        )
        matches = guide_locator_pattern.findall(
            template_text
        )
        locator_names = []

        for locator_name in matches:
            if locator_name in locator_names:
                continue

            locator_names.append(
                locator_name
            )

        if not locator_names:
            raise RuntimeError(
                u"Face Guide 模板中没有读取到标准 Locator: {}".format(
                    template_path
                )
            )

        self.template_locator_names = locator_names
        return list(
            locator_names
        )

    def get_temporary_guide_name(self):
        u"""返回一个未被占用的临时 Guide Container 名称。"""
        return self.create_unique_name(
            type="grp",
            side="md",
            part="face_guide",
            function="container"
        )

    def get_imported_template_root(self, imported_nodes):
        u"""从本次导入的新节点中找到唯一 Face Guide Root。"""
        imported_transforms = cmds.ls(
            imported_nodes,
            type="transform",
            long=True
        )

        if imported_transforms is None:
            imported_transforms = []

        candidates = []

        for node in imported_transforms:
            parent = hierarchy_utils.get_parent(
                node
            )

            if parent:
                continue

            short_name = rename_utils.get_short_name(
                node
            )

            if short_name != self.face_guide_grp:
                continue

            candidates.append(
                node
            )

        if len(candidates) != 1:
            raise RuntimeError(
                u"无法唯一识别 Face Guide Template Root，候选数量: {}".format(
                    len(candidates)
                )
            )

        return candidates[0]

    def clear_guide_config(self):
        u"""清除 Config 中保存的 Guide Message。"""
        if not self.config_node_exists():
            return False

        self.set_config_messages(
            attrs_dict={
                "face_guide_root": None,
                "face_guide_move_ctrl": None,
            },
            force=True,
            clear_empty=True
        )
        return True

    def remove_guide_content(self):
        u"""删除 Face Guide Root 下的模板内容，但保留 Root Container。"""
        if not cmds.objExists(self.face_guide_grp):
            self.ensure_hierarchy()

        children = hierarchy_utils.get_children(
            self.face_guide_grp,
            full_path=True
        )

        for child in children:
            if not cmds.objExists(child):
                continue

            cmds.delete(
                child
            )

        self.clear_guide_config()
        self.refresh_guide_handles()
        return True

    def build_guide(self):
        u"""导入或复用可编辑的 Face Guide Template。"""
        self.validate_setup()
        self.ensure_hierarchy()
        self.ensure_config_node()

        if self.guide_exists():
            return {
                "imported": False,
                "guide_root": self.guide_root,
                "guide_move_ctrl": self.guide_move_ctrl,
                "new_nodes": [],
            }

        guide_container = scene_utils.get_long_name(
            self.face_guide_grp
        )
        container_children = hierarchy_utils.get_children(
            guide_container,
            full_path=True
        )

        if container_children:
            raise RuntimeError(
                u"Face Guide Group 中存在未知内容，无法安全导入模板: {}".format(
                    self.face_guide_grp
                )
            )

        template_path = self.validate_guide_template_file()
        temporary_name = self.get_temporary_guide_name()
        temporary_container = rename_utils.rename_node(
            guide_container,
            temporary_name
        )
        imported_nodes = []

        try:
            imported_nodes = scene_utils.import_scene(
                template_path,
                ignore_version=True
            )
            template_root = self.get_imported_template_root(
                imported_nodes
            )
            template_root = hierarchy_utils.parent(
                template_root,
                self.face_master_grp
            )

            if temporary_container:
                if cmds.objExists(temporary_container):
                    cmds.delete(
                        temporary_container
                    )
        except Exception:
            for imported_node in imported_nodes:
                if not cmds.objExists(imported_node):
                    continue

                try:
                    cmds.delete(
                        imported_node
                    )
                except Exception:
                    pass

            if temporary_container:
                if cmds.objExists(temporary_container):
                    rename_utils.rename_node(
                        temporary_container,
                        self.face_guide_grp
                    )

            raise

        self.refresh_guide_handles()

        if not self.guide_exists():
            raise RuntimeError(
                u"Face Guide 模板导入完成，但没有找到 {}。".format(
                    self.guide_move_ctrl_name
                )
            )

        self.apply_mirror(
            source_side="lf",
            target_side="rt"
        )

        self.save_guide_config()
        self.set_step_completed(
            completed=False
        )
        self.invalidate_later_steps()

        return {
            "imported": True,
            "guide_root": self.guide_root,
            "guide_move_ctrl": self.guide_move_ctrl,
            "new_nodes": imported_nodes,
        }

    def capture_guide_state(self):
        u"""记录当前仍存在的 Move Ctrl 和 Locator 世界矩阵。"""
        state = {
            "move_ctrl_matrix": None,
            "locators": {},
        }

        self.refresh_guide_handles()

        if self.guide_move_ctrl:
            if cmds.objExists(self.guide_move_ctrl):
                state["move_ctrl_matrix"] = transform_utils.get_world_matrix(
                    self.guide_move_ctrl
                )

        locators = self.get_guide_locators()

        for locator in locators:
            short_name = rename_utils.get_short_name(
                locator
            )
            state["locators"][short_name] = transform_utils.get_world_matrix(
                locator
            )

        return state

    def set_world_matrix_preserve_lock(
            self,
            node,
            matrix_values
    ):
        u"""临时解锁 Transform Channel，写入 World Matrix 后恢复 Lock。"""
        transform_attributes = [
            "translateX",
            "translateY",
            "translateZ",
            "rotateX",
            "rotateY",
            "rotateZ",
            "scaleX",
            "scaleY",
            "scaleZ",
        ]
        lock_states = {}

        for attribute in transform_attributes:
            plug = "{}.{}".format(
                node,
                attribute
            )

            if not cmds.objExists(plug):
                continue

            lock_states[attribute] = bool(
                cmds.getAttr(
                    plug,
                    lock=True
                )
            )

            if lock_states[attribute]:
                cmds.setAttr(
                    plug,
                    lock=False
                )

        try:
            transform_utils.set_world_matrix(
                node,
                matrix_values
            )
        finally:
            for attribute in lock_states:
                cmds.setAttr(
                    "{}.{}".format(node, attribute),
                    lock=lock_states[attribute]
                )

        return node

    def restore_guide_state(self, state):
        u"""恢复重新导入前仍存在的 Locator 位置。"""
        restored_locators = []
        self.refresh_guide_handles()

        move_ctrl_matrix = state.get(
            "move_ctrl_matrix"
        )

        if move_ctrl_matrix:
            if self.guide_move_ctrl:
                self.set_world_matrix_preserve_lock(
                    self.guide_move_ctrl,
                    move_ctrl_matrix
                )

        locator_states = state.get(
            "locators",
            {}
        )

        for short_name in locator_states:
            locator = self.get_guide_node(
                short_name,
                required=False
            )

            if not locator:
                continue

            self.set_world_matrix_preserve_lock(
                locator,
                locator_states[short_name]
            )
            restored_locators.append(
                locator
            )

        return restored_locators

    @scene_utils.undo_chunk
    def reimport_guide(self):
        u"""重新导入完整模板，同时保留当前仍存在 Locator 的位置。"""
        self.validate_setup()

        state = self.capture_guide_state()
        self.remove_guide_content()
        self.build_guide()
        restored_locators = self.restore_guide_state(
            state
        )

        self.set_step_completed(
            completed=False
        )
        self.invalidate_later_steps()
        self.save_guide_config()

        return {
            "restored_count": len(restored_locators),
            "template_locator_count": len(
                self.get_template_locator_names()
            ),
        }

    # =========================================================================
    # DAG / Guide Query
    # =========================================================================

    @staticmethod
    def get_locator_shapes(locator):
        u"""获取 Locator Transform 下全部有效 Locator Shape。"""
        if not locator:
            return []

        if not cmds.objExists(locator):
            return []

        shapes = cmds.listRelatives(
            locator,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="locator"
        )

        if shapes is None:
            shapes = []

        return shapes

    @staticmethod
    def set_attr_preserve_lock(
            node,
            attribute,
            value
    ):
        u"""设置 Attribute，并恢复原来的 Lock 状态。"""
        plug = "{}.{}".format(
            node,
            attribute
        )

        if not cmds.objExists(plug):
            return False

        was_locked = cmds.getAttr(
            plug,
            lock=True
        )

        if was_locked:
            cmds.setAttr(
                plug,
                lock=False
            )

        try:
            cmds.setAttr(
                plug,
                value
            )
        finally:
            if was_locked:
                cmds.setAttr(
                    plug,
                    lock=True
                )

        return True

    def refresh_guide_handles(self):
        u"""刷新当前场景中的 Guide Root 和 Face Move Ctrl。"""
        self.guide_root = None
        self.guide_move_ctrl = None

        if not cmds.objExists(self.face_guide_grp):
            return False

        self.guide_root = self.face_guide_grp
        self.guide_move_ctrl = self.get_guide_node(
            self.guide_move_ctrl_name,
            required=False
        )

        return bool(
            self.guide_move_ctrl
        )

    def guide_exists(self):
        u"""检查正式 Guide 内容是否已经加载。"""
        self.refresh_guide_handles()

        if not self.guide_root:
            return False

        if not self.guide_move_ctrl:
            return False

        return True

    def get_guide_node(
            self,
            short_name,
            required=False
    ):
        u"""在正式 Face Guide 层级中按 Short Name 查找 Transform。"""
        if not short_name:
            if required:
                raise RuntimeError(
                    u"Guide 节点名称不能为空。"
                )
            return None

        if not cmds.objExists(self.face_guide_grp):
            if required:
                raise RuntimeError(
                    u"Face Guide Group 不存在: {}".format(
                        self.face_guide_grp
                    )
                )
            return None

        candidates = []
        root_short_name = rename_utils.get_short_name(
            self.face_guide_grp
        )

        if root_short_name == short_name:
            candidates.append(
                self.face_guide_grp
            )

        descendants = hierarchy_utils.get_descendants(
            self.face_guide_grp,
            node_type="transform",
            full_path=True
        )

        for node in descendants:
            node_short_name = rename_utils.get_short_name(
                node
            )

            if node_short_name == short_name:
                candidates.append(
                    node
                )

        if len(candidates) == 1:
            return candidates[0]

        if len(candidates) > 1:
            raise RuntimeError(
                u"Face Guide 中存在多个同名节点: {}".format(
                    short_name
                )
            )

        if required:
            raise RuntimeError(
                u"没有找到 Face Guide 节点: {}".format(
                    short_name
                )
            )

        return None

    def get_guide_locators(self):
        u"""获取正式 Guide 层级中的全部 Locator Transform。"""
        if not cmds.objExists(self.face_guide_grp):
            return []

        descendants = hierarchy_utils.get_descendants(
            self.face_guide_grp,
            node_type="transform",
            full_path=True
        )
        locators = []

        for node in descendants:
            short_name = rename_utils.get_short_name(
                node
            )

            if not short_name.startswith("loc_"):
                continue

            if "_guide_" not in short_name:
                continue

            if not self.get_locator_shapes(node):
                continue

            locators.append(
                node
            )

        locators.sort(
            key=rename_utils.get_short_name
        )
        return locators

    def get_guides_from_names(
            self,
            guide_names,
            required=True
    ):
        u"""按输入名称顺序解析 Guide Transform。"""
        guides = []

        for guide_name in guide_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                guides.append(
                    guide
                )

        return guides

    def get_part_guides(
            self,
            part,
            side=None,
            required=False
    ):
        u"""按标准名称中的 Token 获取某个 Face 部位 Guide。"""
        if not part:
            raise ValueError(
                u"part 不能为空。"
            )

        part_token = "_{}_".format(
            part
        )
        side_token = None

        if side is not None:
            side_token = "_{}_".format(
                side
            )

        guides = []
        locators = self.get_guide_locators()

        for locator in locators:
            short_name = rename_utils.get_short_name(
                locator
            )

            if part_token not in short_name:
                continue

            if side_token:
                if side_token not in short_name:
                    continue

            guides.append(
                locator
            )

        guides.sort(
            key=rename_utils.get_short_name
        )

        if required:
            if not guides:
                raise RuntimeError(
                    u"没有找到 {} Guide。".format(
                        part
                    )
                )

        return guides

    def get_guide_positions(self, guides):
        u"""按输入顺序返回多个 Guide 的世界坐标。"""
        positions = []

        for guide in guides:
            positions.append(
                transform_utils.get_world_translation(
                    guide
                )
            )

        return positions

    # =========================================================================
    # Ordered Guide Query
    # =========================================================================

    def _create_guide_name(
            self,
            side,
            part,
            index=1
    ):
        u"""创建以 guide 为 function 的标准 Locator 名称。"""
        return self.create_name(
            type="loc",
            side=side,
            part=part,
            function="guide",
            index=index
        )

    def get_lip_guides(self, required=True):
        u"""返回上下嘴唇和嘴角的固定有序 Guide。"""
        upper_names = [
            self._create_guide_name("rt", "mouth_corner", 1),
            self._create_guide_name("rt", "upper_lip", 2),
            self._create_guide_name("rt", "upper_lip", 1),
            self._create_guide_name("md", "upper_lip", 1),
            self._create_guide_name("lf", "upper_lip", 1),
            self._create_guide_name("lf", "upper_lip", 2),
            self._create_guide_name("lf", "mouth_corner", 1),
        ]
        lower_names = [
            self._create_guide_name("rt", "mouth_corner", 1),
            self._create_guide_name("rt", "lower_lip", 2),
            self._create_guide_name("rt", "lower_lip", 1),
            self._create_guide_name("md", "lower_lip", 1),
            self._create_guide_name("lf", "lower_lip", 1),
            self._create_guide_name("lf", "lower_lip", 2),
            self._create_guide_name("lf", "mouth_corner", 1),
        ]
        corner_names = [
            self._create_guide_name("rt", "mouth_corner", 1),
            self._create_guide_name("lf", "mouth_corner", 1),
        ]

        return {
            "upper": self.get_guides_from_names(
                upper_names,
                required=required
            ),
            "lower": self.get_guides_from_names(
                lower_names,
                required=required
            ),
            "corners": self.get_guides_from_names(
                corner_names,
                required=required
            ),
        }

    def get_eyelid_guides(
            self,
            side,
            required=True
    ):
        u"""返回某一侧 Upper / Lower Eyelid 的固定有序 Guide。"""
        if side not in self.mirror_sides:
            raise ValueError(
                u"Eyelid side 必须是 lf 或 rt。"
            )

        inner_name = self._create_guide_name(
            side,
            "inner_lid",
            1
        )
        outer_name = self._create_guide_name(
            side,
            "outer_lid",
            1
        )
        upper_names = [
            inner_name,
            self._create_guide_name(side, "upper_lid", 1),
            self._create_guide_name(side, "upper_lid", 2),
            self._create_guide_name(side, "upper_lid", 3),
            outer_name,
        ]
        lower_names = [
            inner_name,
            self._create_guide_name(side, "lower_lid", 1),
            self._create_guide_name(side, "lower_lid", 2),
            self._create_guide_name(side, "lower_lid", 3),
            outer_name,
        ]

        return {
            "upper": self.get_guides_from_names(
                upper_names,
                required=required
            ),
            "lower": self.get_guides_from_names(
                lower_names,
                required=required
            ),
        }

    def get_brow_guides(self, side):
        u"""返回某一侧 Brow Main 和 Brow Point Guide。"""
        all_guides = self.get_part_guides(
            part="brow",
            side=side
        )
        main_guide = None
        point_guides = []

        for guide in all_guides:
            short_name = rename_utils.get_short_name(
                guide
            )

            if "_brow_main_" in short_name:
                main_guide = guide
                continue

            point_guides.append(
                guide
            )

        return {
            "main": main_guide,
            "points": point_guides,
            "all": all_guides,
        }

    def get_eye_guides(
            self,
            side,
            required=False
    ):
        u"""返回某一侧 Eye Ball / Iris Guide。"""
        if side not in self.mirror_sides:
            raise ValueError(
                u"Eye side 必须是 lf 或 rt。"
            )

        eye_ball_name = self._create_guide_name(
            side,
            "eye_ball",
            1
        )
        eye_iris_name = self._create_guide_name(
            side,
            "eye_iris",
            1
        )

        return {
            "eye_ball": self.get_guide_node(
                eye_ball_name,
                required=required
            ),
            "eye_iris": self.get_guide_node(
                eye_iris_name,
                required=required
            ),
        }

    # =========================================================================
    # Mirror
    # =========================================================================

    def validate_mirror_sides(
            self,
            source_side,
            target_side
    ):
        u"""检查 Mirror Source / Target Side。"""
        if source_side not in self.mirror_sides:
            raise ValueError(
                u"source_side 必须是 lf 或 rt。"
            )

        if target_side not in self.mirror_sides:
            raise ValueError(
                u"target_side 必须是 lf 或 rt。"
            )

        if source_side == target_side:
            raise ValueError(
                u"Mirror Source / Target Side 不能相同。"
            )

        return True

    def get_side_zero_groups(self, side):
        u"""返回指定 Side 下全部 Guide Zero Group。"""
        prefix = "zero_{}_".format(
            side
        )
        descendants = hierarchy_utils.get_descendants(
            self.face_guide_grp,
            node_type="transform",
            full_path=True
        )
        zero_groups = []

        for node in descendants:
            short_name = rename_utils.get_short_name(
                node
            )

            if short_name.startswith(prefix):
                zero_groups.append(
                    node
                )

        zero_groups.sort(
            key=hierarchy_utils.get_dag_depth
        )
        return zero_groups

    def get_side_locator(
            self,
            zero_group,
            side
    ):
        u"""返回一个 Guide Zero Group 下对应 Side 的 Locator。"""
        prefix = "loc_{}_".format(
            side
        )
        children = hierarchy_utils.get_children(
            zero_group,
            node_type="transform",
            full_path=True
        )

        for child in children:
            short_name = rename_utils.get_short_name(
                child
            )

            if short_name.startswith(prefix):
                return child

        return None

    @staticmethod
    def capture_attributes(
            node,
            attributes
    ):
        u"""记录节点指定 Attribute 的当前值。"""
        values = {}

        if not node:
            return values

        if not cmds.objExists(node):
            return values

        for attribute in attributes:
            plug = "{}.{}".format(
                node,
                attribute
            )

            if not cmds.objExists(plug):
                continue

            values[attribute] = cmds.getAttr(
                plug
            )

        return values

    def copy_attribute(
            self,
            source_node,
            target_node,
            attribute
    ):
        u"""复制一个 Attribute，并断开 Target 原输入。"""
        source_plug = "{}.{}".format(
            source_node,
            attribute
        )
        target_plug = "{}.{}".format(
            target_node,
            attribute
        )

        if not cmds.objExists(source_plug):
            return False

        if not cmds.objExists(target_plug):
            return False

        connection_utils.disconnect_input(
            target_plug
        )
        self.set_attr_preserve_lock(
            target_node,
            attribute,
            cmds.getAttr(source_plug)
        )
        return True

    def capture_side_state(self, side):
        u"""记录 Target Side 在 Mirror 前的状态。"""
        snapshot = {
            "side": side,
            "items": [],
        }
        zero_groups = self.get_side_zero_groups(
            side
        )

        for zero_group in zero_groups:
            locator = self.get_side_locator(
                zero_group,
                side
            )
            item = {
                "zero_name": rename_utils.get_short_name(zero_group),
                "zero_values": self.capture_attributes(
                    zero_group,
                    self.zero_attributes
                ),
                "locator_name": None,
                "locator_values": {},
                "locator_shape_values": {},
            }

            if locator:
                item["locator_name"] = rename_utils.get_short_name(
                    locator
                )
                item["locator_values"] = self.capture_attributes(
                    locator,
                    self.locator_attributes
                )
                locator_shapes = self.get_locator_shapes(
                    locator
                )

                if locator_shapes:
                    item["locator_shape_values"] = self.capture_attributes(
                        locator_shapes[0],
                        self.locator_shape_attributes
                    )

            snapshot["items"].append(
                item
            )

        return snapshot

    def restore_attributes(
            self,
            node,
            values
    ):
        u"""恢复 Snapshot 中保存的 Attribute。"""
        for attribute in values:
            plug = "{}.{}".format(
                node,
                attribute
            )

            if not cmds.objExists(plug):
                continue

            connection_utils.disconnect_input(
                plug
            )
            self.set_attr_preserve_lock(
                node,
                attribute,
                values[attribute]
            )

        return True

    def restore_mirror_snapshot(self, snapshot):
        u"""恢复最近一次 Mirror 前的 Target Side 状态。"""
        if not isinstance(snapshot, dict):
            raise TypeError(
                u"Mirror Snapshot 必须是 dict。"
            )

        restored_count = 0
        items = snapshot.get(
            "items",
            []
        )

        for item in items:
            zero_group = self.get_guide_node(
                item.get("zero_name"),
                required=False
            )

            if not zero_group:
                continue

            self.restore_attributes(
                zero_group,
                item.get("zero_values", {})
            )

            locator_name = item.get(
                "locator_name"
            )

            if locator_name:
                locator = self.get_guide_node(
                    locator_name,
                    required=False
                )

                if locator:
                    self.restore_attributes(
                        locator,
                        item.get("locator_values", {})
                    )
                    locator_shapes = self.get_locator_shapes(
                        locator
                    )

                    if locator_shapes:
                        self.restore_attributes(
                            locator_shapes[0],
                            item.get("locator_shape_values", {})
                        )

            restored_count += 1

        self.set_step_completed(
            completed=False
        )
        self.invalidate_later_steps()

        return {
            "restored_count": restored_count,
        }

    def mirror_zero_group(
            self,
            source_zero,
            target_zero,
            source_side
    ):
        u"""把一个 Source Guide Zero 的当前状态复制到 Target。"""
        source_parent = hierarchy_utils.get_parent(
            source_zero
        )
        is_mirror_root = True

        if source_parent:
            source_parent_name = rename_utils.get_short_name(
                source_parent
            )
            source_token = "_{}_".format(
                source_side
            )

            if source_token in source_parent_name:
                is_mirror_root = False

        if is_mirror_root:
            self.set_attr_preserve_lock(
                target_zero,
                "translateX",
                -cmds.getAttr(source_zero + ".translateX")
            )
            self.set_attr_preserve_lock(
                target_zero,
                "scaleX",
                -cmds.getAttr(source_zero + ".scaleX")
            )
            direct_attributes = [
                "translateY",
                "translateZ",
                "rotateX",
                "rotateY",
                "rotateZ",
                "scaleY",
                "scaleZ",
                "rotateOrder",
            ]

            for attribute in direct_attributes:
                self.copy_attribute(
                    source_zero,
                    target_zero,
                    attribute
                )
        else:
            for attribute in self.zero_attributes:
                self.copy_attribute(
                    source_zero,
                    target_zero,
                    attribute
                )

        return True

    def mirror_locator(
            self,
            source_locator,
            target_locator
    ):
        u"""复制 Locator Transform 和 Shape 参数。"""
        for attribute in self.locator_attributes:
            self.copy_attribute(
                source_locator,
                target_locator,
                attribute
            )

        source_shapes = self.get_locator_shapes(
            source_locator
        )
        target_shapes = self.get_locator_shapes(
            target_locator
        )

        if source_shapes and target_shapes:
            for attribute in self.locator_shape_attributes:
                self.copy_attribute(
                    source_shapes[0],
                    target_shapes[0],
                    attribute
                )

        return True

    def apply_mirror(
            self,
            source_side,
            target_side
    ):
        u"""执行 Guide Mirror，不创建 Snapshot。"""
        self.validate_mirror_sides(
            source_side,
            target_side
        )

        if not self.guide_exists():
            raise RuntimeError(
                u"Face Guide 尚未加载。"
            )

        source_zero_groups = self.get_side_zero_groups(
            source_side
        )
        mirrored_count = 0

        for source_zero in source_zero_groups:
            source_zero_name = rename_utils.get_short_name(
                source_zero
            )
            target_zero_name = self.mirror_name(
                source_zero_name
            )
            target_zero = self.get_guide_node(
                target_zero_name,
                required=True
            )

            source_locator = self.get_side_locator(
                source_zero,
                source_side
            )

            if not source_locator:
                continue

            source_locator_name = rename_utils.get_short_name(
                source_locator
            )
            target_locator_name = self.mirror_name(
                source_locator_name
            )
            target_locator = self.get_guide_node(
                target_locator_name,
                required=True
            )

            self.mirror_zero_group(
                source_zero,
                target_zero,
                source_side
            )
            self.mirror_locator(
                source_locator,
                target_locator
            )
            mirrored_count += 1

        self.set_step_completed(
            completed=False
        )
        self.invalidate_later_steps()

        return {
            "source_side": source_side,
            "target_side": target_side,
            "count": mirrored_count,
        }

    @scene_utils.undo_chunk
    def mirror_guides(
            self,
            source_side,
            target_side
    ):
        u"""记录 Target Snapshot，并执行一次可撤销 Guide Mirror。"""
        snapshot = self.capture_side_state(
            target_side
        )
        result = self.apply_mirror(
            source_side,
            target_side
        )
        result["snapshot"] = snapshot
        return result

    @scene_utils.undo_chunk
    def undo_mirror(self, snapshot):
        u"""恢复 UI 保存的最近一次 Mirror Snapshot。"""
        return self.restore_mirror_snapshot(
            snapshot
        )

    # =========================================================================
    # Validation
    # =========================================================================

    def validate_guides(self):
        u"""检查模板中的每一个 Locator 是否仍然存在。"""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "guide_count": 0,
            "template_guide_count": 0,
            "missing_guide_names": [],
            "unexpected_guide_names": [],
        }

        if not cmds.objExists(self.face_guide_grp):
            result["errors"].append(
                u"Face Guide Group 不存在: {}".format(
                    self.face_guide_grp
                )
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
            short_name = rename_utils.get_short_name(
                locator
            )
            current_names.append(
                short_name
            )

            if short_name not in name_counts:
                name_counts[short_name] = 0

            name_counts[short_name] += 1

        for expected_name in expected_names:
            if expected_name in current_names:
                continue

            result["missing_guide_names"].append(
                expected_name
            )
            result["errors"].append(
                u"缺少模板定位器: {}".format(
                    expected_name
                )
            )

        for short_name in name_counts:
            if name_counts[short_name] <= 1:
                continue

            result["errors"].append(
                u"Guide 短名称重复: {} x {}".format(
                    short_name,
                    name_counts[short_name]
                )
            )

        for current_name in current_names:
            if current_name not in expected_names:
                result["unexpected_guide_names"].append(
                    current_name
                )

        if result["unexpected_guide_names"]:
            result["warnings"].append(
                u"当前 Guide 中存在模板之外的 Locator；不会阻止下一步。"
            )

        if result["errors"]:
            result["valid"] = False

        return result

    # =========================================================================
    # Config
    # =========================================================================

    def save_guide_config(self):
        u"""保存 Step 02 Guide Root、Move Ctrl 和 Guide Version。"""
        self.refresh_guide_handles()

        if not self.guide_root:
            raise RuntimeError(
                u"没有可保存的 Face Guide Root。"
            )

        if not self.guide_move_ctrl:
            raise RuntimeError(
                u"没有可保存的 Face Guide Move Ctrl。"
            )

        self.set_config_messages(
            attrs_dict={
                "face_guide_root": self.guide_root,
                "face_guide_move_ctrl": self.guide_move_ctrl,
            },
            force=True,
            clear_empty=True
        )
        self.set_config_values(
            attrs_dict={
                "face_guide_version": self.guide_version,
            },
            attr_types={
                "face_guide_version": "string",
            },
            lock=False,
            hide=True
        )
        return True

    @staticmethod
    def get_default_controller_settings():
        u"""返回一份独立的 Face Controller 默认设置。"""
        settings = {}

        for attr_name in config.face_controller_default_settings:
            settings[attr_name] = config.face_controller_default_settings.get(
                attr_name
            )

        return settings

    @staticmethod
    def validate_controller_settings(settings):
        u"""检查当前正式 Schema 的 Step 02 Controller Settings。"""
        if not isinstance(settings, dict):
            raise TypeError(
                u"Controller Settings 必须是 dict。"
            )

        global_scale = settings.get(
            config.face_controller_global_scale_attr
        )

        if global_scale is None:
            raise ValueError(
                u"缺少 Face Controller Global Scale。"
            )

        if float(global_scale) <= 0.0:
            raise ValueError(
                u"Face Controller Global Scale 必须大于 0。"
            )

        for module_name in config.face_controller_size_attr_names:
            attr_name = config.face_controller_size_attr_names.get(
                module_name
            )
            value = settings.get(
                attr_name
            )

            if value is None:
                raise ValueError(
                    u"缺少 Controller Size: {}".format(
                        attr_name
                    )
                )

            if float(value) <= 0.0:
                raise ValueError(
                    u"Controller Size 必须大于 0: {}".format(
                        attr_name
                    )
                )

        for side in config.face_controller_color_attr_names:
            attr_name = config.face_controller_color_attr_names.get(
                side
            )
            value = settings.get(
                attr_name
            )

            if value is None:
                raise ValueError(
                    u"缺少 Controller Color: {}".format(
                        attr_name
                    )
                )

            color_index = int(
                value
            )

            if color_index < 0 or color_index > 31:
                raise ValueError(
                    u"Maya Index Color 必须在 0～31: {}".format(
                        attr_name
                    )
                )

        return True

    def load_controller_settings(self):
        u"""从 Face Config 读取当前正式 Controller Settings。"""
        settings = self.get_default_controller_settings()

        if not self.config_node_exists():
            return settings

        attr_names = []

        for attr_name in config.face_controller_default_settings:
            attr_names.append(
                attr_name
            )

        saved_values = self.config_data.get_values(
            attr_names
        )

        for attr_name in attr_names:
            saved_value = saved_values.get(
                attr_name
            )

            if saved_value is not None:
                settings[attr_name] = saved_value

        return settings

    def save_controller_settings(self, settings):
        u"""把当前正式 Controller Settings 保存到 Face Config。"""
        self.validate_controller_settings(
            settings
        )
        values = {}

        for attr_name in config.face_controller_default_settings:
            values[attr_name] = settings.get(
                attr_name
            )

        return self.set_config_values(
            attrs_dict=values,
            attr_types=config.face_controller_setting_attr_types,
            lock=False,
            hide=True
        )


__all__ = [
    "FaceGuide",
]
