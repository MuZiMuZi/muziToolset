# coding=utf-8
u"""
Step 02 - Face Guide
====================

Face Guide Manager。

职责：
    1. 组织 Step 02 生命周期；
    2. 管理 Guide Template 的公开入口；
    3. 提供稳定的 Guide 节点查询接口；
    4. 从 guide_data 读取固定 Template Contract；
    5. “下一步”时检查 face_guide.ma 中全部 Locator 是否仍然存在；
    6. 保存 Guide 和 Controller Settings 到统一 Face Config；
    7. Step 02 完成后把 Face Workflow 当前进度推进到 Step 03。

重要边界：
    - 固定节点名称 / Guide 顺序 / 默认参数放在 guide_data.py；
    - Template Import / Repair 放在 guide_template.py；
    - 左右 Mirror / Undo 放在 guide_mirror.py；
    - FaceGuide 只负责 Step 02 的调度、查询、Validation 和 Config。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import rename_utils
from ....core import transform_utils
from .. import face_base
from . import guide_data
from . import guide_template


class FaceGuide(face_base.FaceBase):
    u"""Face Rig Step 02 - Guide 管理器。"""

    guide_template_file_name = guide_data.guide_template_file_name
    guide_move_ctrl_name = guide_data.guide_move_ctrl_name
    guide_version = guide_data.guide_version

    def __init__(self):
        u"""初始化 Face Guide Step。"""
        super(FaceGuide, self).__init__()

        self.step_value = 2
        self.guide_root = None
        self.guide_move_ctrl = None
        self.validation_result = None

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
                u"Face Guide 尚未完整加载，请使用“重新导入模板”修复后再继续。"
            )

        return True

    def prepare_data(self):
        u"""确保 Face Hierarchy 和 Config 可用于保存 Step 02。"""
        # 确保 Face Rig 基础层级存在，避免 Guide 保存到不完整层级。
        self.ensure_hierarchy()

        # 创建或复用 Workflow / Step Config 分隔结构，旧场景也会按新 Schema 整理显示。
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
        # 保存 Guide Root / Move Ctrl / Version，作为后续 Build 的稳定输入。
        self.save_guide_config()

        # 正式记录 Step 02 已完成。
        self.set_step_completed(
            completed=True
        )

        # Guide 重新提交后，旧的 Step 03 / 04 结果必须失效。
        self.invalidate_later_steps()

        # Step 02 完成后，下一次打开 Face Rig 应直接回到 Step 03 Build。
        self.set_current_step_value(
            3
        )

        # 最后重新整理 Config Attribute 顺序，确保 Step 02 数据集中显示。
        self.organize_config_attributes()
        return True

    # =========================================================================
    # Setup / Template
    # =========================================================================

    def validate_setup(self):
        u"""检查 Step 02 所依赖的 Step 01 公共数据。"""
        return self.validate_setup_config(
            require_mouth_jnt_number=True
        )

    def get_guide_template_path(self):
        u"""返回 face_guide.ma 的规范绝对路径。"""
        return guide_data.get_guide_template_path()

    def validate_guide_template_file(self):
        u"""检查 Face Guide 模板文件是否存在。"""
        return guide_data.validate_guide_template_file()

    def build_guide(self):
        u"""导入或复用可编辑的 Face Guide Template。"""
        return guide_template.build_guide(
            self
        )

    def reset_guide(self):
        u"""恢复一份完全干净的 Face Guide Template。"""
        return guide_template.reset_template(
            self
        )

    def reimport_guide(self):
        u"""重新导入模板，同时保留当前仍存在 Locator 的位置。"""
        return guide_template.reimport_template_preserve_guide(
            self
        )

    # =========================================================================
    # DAG Helper
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

    def get_node_under_parent(
            self,
            parent,
            short_name
    ):
        u"""获取指定 Parent 下的直接子 Transform。"""
        if not short_name:
            return None

        if parent:
            if not cmds.objExists(parent):
                return None

            children = cmds.listRelatives(
                parent,
                children=True,
                type="transform",
                fullPath=True
            )

            if children is None:
                children = []

            for child in children:
                child_short_name = rename_utils.get_short_name(
                    child
                )

                if child_short_name == short_name:
                    return child

            return None

        matches = cmds.ls(
            short_name,
            type="transform",
            long=True
        )

        if matches is None:
            matches = []

        if len(matches) == 1:
            return matches[0]

        return None

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

    # =========================================================================
    # Guide State / Query
    # =========================================================================

    def refresh_guide_handles(self):
        u"""刷新当前场景中的 Guide Root 和 Face Move Ctrl 引用。"""
        self.guide_root = None
        self.guide_move_ctrl = None

        if not cmds.objExists(self.face_guide_grp):
            return False

        self.guide_root = self.face_guide_grp
        move_ctrl = self.get_node_under_parent(
            self.face_guide_grp,
            self.guide_move_ctrl_name
        )

        if move_ctrl:
            self.guide_move_ctrl = move_ctrl

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

        descendants = cmds.listRelatives(
            self.face_guide_grp,
            allDescendents=True,
            type="transform",
            fullPath=True
        )

        if descendants is None:
            descendants = []

        for node in descendants:
            node_short_name = rename_utils.get_short_name(
                node
            )

            if node_short_name != short_name:
                continue

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

        descendants = cmds.listRelatives(
            self.face_guide_grp,
            allDescendents=True,
            type="transform",
            fullPath=True
        )

        if descendants is None:
            descendants = []

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

        locators.sort()
        return locators

    def get_guides_from_names(
            self,
            guide_names,
            required=True
    ):
        u"""按固定名称顺序解析 Guide Transform。"""
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
            include_tokens=None,
            exclude_tokens=None,
            required=False
    ):
        u"""从 Guide Template Contract 中解析某个 Face 部位。"""
        guide_names = guide_data.get_part_guide_names(
            part=part,
            side=side,
            include_tokens=include_tokens,
            exclude_tokens=exclude_tokens
        )

        return self.get_guides_from_names(
            guide_names,
            required=required
        )

    def get_guide_positions(self, guides):
        u"""按输入顺序返回多个 Guide 的世界坐标。"""
        positions = []

        if not guides:
            return positions

        for guide in guides:
            position = transform_utils.get_world_translation(
                guide
            )
            positions.append(
                position
            )

        return positions

    # =========================================================================
    # Face Part Query
    # =========================================================================

    def get_lip_guides(self, required=True):
        u"""返回上下嘴唇和嘴角的固定有序 Guide。"""
        return {
            "upper": self.get_guides_from_names(
                guide_data.lip_guide_names["upper"],
                required=required
            ),
            "lower": self.get_guides_from_names(
                guide_data.lip_guide_names["lower"],
                required=required
            ),
            "corners": self.get_guides_from_names(
                guide_data.lip_guide_names["corners"],
                required=required
            ),
        }

    def get_eyelid_guides(
            self,
            side,
            required=True
    ):
        u"""返回某一侧 Upper / Lower Eyelid 的固定有序 Guide。"""
        guide_names = guide_data.get_eyelid_guide_names(
            side
        )

        return {
            "upper": self.get_guides_from_names(
                guide_names["upper"],
                required=required
            ),
            "lower": self.get_guides_from_names(
                guide_names["lower"],
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
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Eye side 必须是 lf 或 rt。"
            )

        return {
            "eye_ball": self.get_guide_node(
                "loc_{}_eye_ball_guide_001".format(side),
                required=required
            ),
            "eye_iris": self.get_guide_node(
                "loc_{}_eye_iris_guide_001".format(side),
                required=required
            ),
        }

    def get_eye_bag_guides(self, side):
        u"""返回某一侧 Eye Bag Guide。"""
        return self.get_part_guides(
            part="eye_bag",
            side=side
        )

    def get_nose_guides(self):
        u"""返回全部 Nose Guide。"""
        return self.get_part_guides(
            part="nose"
        )

    def get_jaw_guides(self):
        u"""返回全部 Jaw Guide。"""
        return self.get_part_guides(
            part="jaw"
        )

    def get_teeth_guides(self):
        u"""返回全部 Teeth Guide。"""
        return self.get_part_guides(
            part="teeth"
        )

    def get_tongue_guides(self):
        u"""返回全部 Tongue Guide。"""
        return self.get_part_guides(
            part="tongue"
        )

    def get_ear_guides(self, side=None):
        u"""返回 Ear Guide。"""
        return self.get_part_guides(
            part="ear",
            side=side
        )

    def get_zygoma_guides(self, side=None):
        u"""返回 Zygoma Guide。"""
        return self.get_part_guides(
            part="zygoma",
            side=side
        )

    # =========================================================================
    # Validation
    # =========================================================================

    def validate_guides(self):
        u"""
        检查 Step 02 Guide 是否完整。

        核心规则：face_guide.ma 中定义的每一个 Locator 都必须仍然存在，
        任意 Locator 被误删都会阻止进入 Step 03。
        """
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

        if not self.guide_exists():
            result["errors"].append(
                u"Face Guide 模板尚未完整加载，缺少 {}。".format(
                    self.guide_move_ctrl_name
                )
            )

        locators = self.get_guide_locators()
        result["guide_count"] = len(locators)

        expected_names = guide_data.get_template_locator_names()
        result["template_guide_count"] = len(expected_names)

        current_names = []
        name_counts = {}

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
            count = name_counts.get(
                short_name
            )

            if count <= 1:
                continue

            result["errors"].append(
                u"Guide 短名称重复: {} x {}".format(
                    short_name,
                    count
                )
            )

        for current_name in current_names:
            if current_name in expected_names:
                continue

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
    # Config - Guide
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

    # =========================================================================
    # Config - Controller Settings
    # =========================================================================

    def load_controller_settings(self):
        u"""从 Face Config 读取 Controller Settings。"""
        settings = guide_data.get_default_controller_settings()

        if not self.config_node_exists():
            return settings

        attr_names = []

        for attr_name in guide_data.default_controller_settings:
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

            if saved_value is None:
                continue

            settings[attr_name] = saved_value

        return settings

    def save_controller_settings(self, settings):
        u"""把 Step 02 Controller Settings 保存到统一 Face Config。"""
        guide_data.validate_controller_settings(
            settings
        )

        values = {}

        for attr_name in guide_data.default_controller_settings:
            values[attr_name] = settings.get(
                attr_name
            )

        return self.set_config_values(
            attrs_dict=values,
            attr_types=guide_data.controller_setting_attr_types,
            lock=False,
            hide=True
        )


__all__ = [
    "FaceGuide",
]
