# coding=utf-8
u"""
Step 02 - Face Guide
====================

Face Guide Manager。

职责：
    1. 读取 Step 01 保存的公共 Face Setup 数据；
    2. 管理 resources/face/face_guide.ma 模板的导入 / 删除 / 重置；
    3. 提供统一的 Guide Locator 查询和世界坐标读取接口；
    4. 按 Face 部位整理 Guide 数据，供后续 Builder 使用；
    5. 检查 Guide 完整性和左右镜像连接；
    6. 在镜像结构损坏时提供 Repair Symmetry；
    7. Finalize Step 02，并把 Guide 状态保存到 Face Config。

重要边界：
    - Locator 颜色、初始层级、左右节点和默认连接属于 face_guide.ma 模板；
    - FaceGuide 正常 Build 不重新创建模板已经存在的右侧 Guide；
    - Lip / Brow / Eyelid Curve 和 Joint 不在这里创建；
    - 后续 Builder 只消费 FaceGuide 输出的有序 Guide 数据。

兼容：
    旧的 mirror_left_guide() / mirror_left_guides() API 继续保留，
    但现在它们属于 Repair Symmetry 能力，而不是正常 Build 流程。
"""

from __future__ import print_function

import os

import maya.cmds as cmds

from ... import config as package_config
from ...core import file_utils
from ...core import scene_utils
from . import face_base


class FaceGuide(face_base.FaceBase):
    u"""Face Rig Step 02 - Guide 管理器。"""

    guide_template_file_name = "face_guide.ma"
    guide_move_ctrl_name = "ctrl_md_face_move_001"
    guide_version = "1.0"

    required_guide_names = [
        "loc_md_upper_lip_guide_001",
        "loc_md_lower_lip_guide_001",
        "loc_lf_mouth_corner_guide_001",
        "loc_rt_mouth_corner_guide_001",
        "loc_lf_eye_ball_guide_001",
        "loc_rt_eye_ball_guide_001",
    ]

    def __init__(self):
        super(FaceGuide, self).__init__()

        self.step_value = 2

        self.guide_root = None
        self.guide_move_ctrl = None

        # Config 不存在时保持空值，不在构造阶段报错。
        # 真正 Build 时由 validate_setup() 做严格检查。
        if self.config_node_exists():
            self.refresh_setup_data()

        self.refresh_guide_handles()

    # =========================================================================
    # Setup
    # =========================================================================

    def validate_setup(self):
        u"""检查 Step 02 所依赖的 Step 01 公共数据。"""
        return self.validate_setup_config(
            require_mouth_jnt_number=True
        )

    # =========================================================================
    # Name / DAG Helper
    # =========================================================================

    @staticmethod
    def get_short_name(node):
        u"""返回 DAG 节点短名称。"""
        if not node:
            return ""

        return node.split("|")[-1]

    @staticmethod
    def get_dag_depth(node):
        u"""返回 DAG Path 深度，用于父节点优先排序。"""
        if not node:
            return 0

        return node.count("|")

    @staticmethod
    def get_parent(node):
        u"""返回节点的直接 Parent。"""
        if not node:
            return None

        if not cmds.objExists(node):
            return None

        parents = cmds.listRelatives(
            node,
            parent=True,
            fullPath=True
        )

        if parents is None:
            parents = []

        if not parents:
            return None

        return parents[0]

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
                child_short_name = self.get_short_name(
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

    # =========================================================================
    # Guide Template
    # =========================================================================

    def get_guide_template_path(self):
        u"""返回 face_guide.ma 的规范绝对路径。"""
        template_path = os.path.join(
            package_config.resources_dir,
            "face",
            self.guide_template_file_name
        )

        template_path = file_utils.normalize_path(
            template_path
        )

        return template_path

    def validate_guide_template_file(self):
        u"""检查 Face Guide 模板文件是否存在。"""
        template_path = self.get_guide_template_path()

        if not os.path.isfile(template_path):
            raise RuntimeError(
                u"Face Guide 模板文件不存在: {}".format(
                    template_path
                )
            )

        return template_path

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

        return bool(self.guide_move_ctrl)

    def guide_exists(self):
        u"""
        检查正式 Guide 内容是否已经加载。

        FaceBase 创建的空 grp_md_face_guide_001 不代表模板已经加载，
        因此这里额外检查 ctrl_md_face_move_001。
        """
        self.refresh_guide_handles()

        if not self.guide_root:
            return False

        if not self.guide_move_ctrl:
            return False

        return True

    def get_imported_template_root(self, imported_nodes):
        u"""
        从本次 Import 的新节点中找到模板临时 Root。

        Step 01 已经创建了正式 grp_md_face_guide_001，
        导入同名模板后 Maya 会自动重命名模板 Root。
        因此不能依赖固定的 _002 名称，而要从 returnNewNodes 中定位。
        """
        imported_transforms = cmds.ls(
            imported_nodes,
            type="transform",
            long=True
        )

        if imported_transforms is None:
            imported_transforms = []

        root_candidates = []

        for node in imported_transforms:
            parent = self.get_parent(
                node
            )

            if parent:
                continue

            short_name = self.get_short_name(
                node
            )

            if not short_name.startswith(
                    "grp_md_face_guide_"
            ):
                continue

            root_candidates.append(
                node
            )

        if len(root_candidates) != 1:
            raise RuntimeError(
                u"无法唯一识别导入的 Face Guide 模板 Root，候选数量: {}".format(
                    len(root_candidates)
                )
            )

        return root_candidates[0]

    def merge_imported_template_root(self, template_root):
        u"""
        把模板临时 Root 的内容合并到正式 Face Guide Group。

        模板和系统层级目前都使用 grp_md_face_guide_001。
        为避免 Maya 自动重命名后的 _002 泄漏到正式场景，
        Import 后只保留模板 Root 的子内容，最后删除临时 Root。
        """
        if not cmds.objExists(self.face_guide_grp):
            raise RuntimeError(
                u"正式 Face Guide Group 不存在: {}".format(
                    self.face_guide_grp
                )
            )

        children = cmds.listRelatives(
            template_root,
            children=True,
            type="transform",
            fullPath=True
        )

        if children is None:
            children = []

        if not children:
            raise RuntimeError(
                u"导入的 Face Guide 模板 Root 下没有可合并内容: {}".format(
                    template_root
                )
            )

        merged_nodes = []

        for child in children:
            parent_result = cmds.parent(
                child,
                self.face_guide_grp
            )

            if not parent_result:
                continue

            merged_nodes.append(
                parent_result[0]
            )

        if cmds.objExists(template_root):
            cmds.delete(
                template_root
            )

        return merged_nodes

    def import_guide_template(self):
        u"""
        导入 Face Guide 模板。

        正常情况下只导入一次。
        如果 Guide 已存在，则直接返回现有节点，不重复导入。
        """
        self.ensure_hierarchy()

        if self.guide_exists():
            return {
                "imported": False,
                "guide_root": self.guide_root,
                "guide_move_ctrl": self.guide_move_ctrl,
                "new_nodes": [],
            }

        template_path = self.validate_guide_template_file()

        imported_nodes = scene_utils.import_scene(
            template_path,
            ignore_version=True
        )

        template_root = self.get_imported_template_root(
            imported_nodes
        )

        merged_nodes = self.merge_imported_template_root(
            template_root
        )

        self.refresh_guide_handles()

        if not self.guide_exists():
            raise RuntimeError(
                u"Face Guide 模板导入完成，但没有找到 {}。".format(
                    self.guide_move_ctrl_name
                )
            )

        return {
            "imported": True,
            "guide_root": self.guide_root,
            "guide_move_ctrl": self.guide_move_ctrl,
            "new_nodes": merged_nodes,
        }

    def clear_guide_config(self):
        u"""清除 Config 中保存的 Guide Message 引用。"""
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

    def remove_guide(self):
        u"""
        删除正式 Face Guide Group 下的模板内容。

        注意：
            不删除 self.face_guide_grp 本身，
            因为它属于 FaceBase 的系统主层级。
        """
        if not cmds.objExists(self.face_guide_grp):
            self.refresh_guide_handles()
            return False

        children = cmds.listRelatives(
            self.face_guide_grp,
            children=True,
            type="transform",
            fullPath=True
        )

        if children is None:
            children = []

        for child in children:
            if not cmds.objExists(child):
                continue

            cmds.delete(
                child
            )

        self.clear_guide_config()
        self.refresh_guide_handles()

        if self.config_node_exists():
            self.set_step_completed(
                completed=False
            )
            self.invalidate_later_steps()

        return True

    def reset_guide(self):
        u"""删除当前 Guide 内容，并重新导入原始 face_guide.ma。"""
        self.remove_guide()

        result = self.import_guide_template()

        self.save_guide_config()

        self.set_step_completed(
            completed=False
        )
        self.invalidate_later_steps()

        return result

    # =========================================================================
    # Guide Query
    # =========================================================================

    def get_guide_node(
            self,
            short_name,
            required=False
    ):
        u"""在正式 Face Guide 层级中按短名称查找 Transform。"""
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

        root_short_name = self.get_short_name(
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
            node_short_name = self.get_short_name(
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

    def get_guide_locators(self, parent_group=None):
        u"""获取正式 Guide 层级中的全部 Locator Transform。"""
        if parent_group is None:
            parent_group = self.face_guide_grp

        if not cmds.objExists(parent_group):
            return []

        descendants = cmds.listRelatives(
            parent_group,
            allDescendents=True,
            type="transform",
            fullPath=True
        )

        if descendants is None:
            descendants = []

        locators = []

        for node in descendants:
            short_name = self.get_short_name(
                node
            )

            if not short_name.startswith("loc_"):
                continue

            if "_guide_" not in short_name:
                continue

            shapes = self.get_locator_shapes(
                node
            )

            if not shapes:
                continue

            locators.append(
                node
            )

        locators.sort()
        return locators

    def get_part_guides(
            self,
            part,
            side=None,
            include_tokens=None,
            exclude_tokens=None
    ):
        u"""
        按命名 Token 查询某一个 Face 部位的 Locator。

        part：必须出现在 Locator 名称中的部位 Token。
        side：lf / rt / md / None。
        include_tokens：额外要求名称中必须包含的 Token。
        exclude_tokens：名称中出现任意一个 Token 时排除。
        """
        if not part:
            raise ValueError(
                u"part 不能为空。"
            )

        if side is not None:
            valid_sides = [
                "lf",
                "rt",
                "md",
            ]

            if side not in valid_sides:
                raise ValueError(
                    u"side 必须是 lf / rt / md / None，当前值: {}".format(
                        side
                    )
                )

        if include_tokens is None:
            include_tokens = []

        if exclude_tokens is None:
            exclude_tokens = []

        locators = self.get_guide_locators()
        result = []

        for locator in locators:
            short_name = self.get_short_name(
                locator
            )
            lower_name = short_name.lower()

            if part.lower() not in lower_name:
                continue

            if side is not None:
                side_token = "_{}_".format(
                    side
                )

                if side_token not in lower_name:
                    continue

            include_passed = True

            for token in include_tokens:
                if token.lower() in lower_name:
                    continue

                include_passed = False
                break

            if not include_passed:
                continue

            exclude_failed = False

            for token in exclude_tokens:
                if token.lower() not in lower_name:
                    continue

                exclude_failed = True
                break

            if exclude_failed:
                continue

            result.append(
                locator
            )

        result.sort()
        return result

    def get_world_position(self, guide):
        u"""获取一个 Guide Transform 的世界坐标。"""
        if not guide:
            raise ValueError(
                u"Guide 不能为空。"
            )

        if not cmds.objExists(guide):
            raise RuntimeError(
                u"Guide 不存在: {}".format(
                    guide
                )
            )

        position = cmds.xform(
            guide,
            query=True,
            worldSpace=True,
            translation=True
        )

        return position

    def get_guide_positions(self, guides):
        u"""按输入顺序返回多个 Guide 的世界坐标。"""
        positions = []

        if not guides:
            return positions

        for guide in guides:
            position = self.get_world_position(
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
        u"""返回上下嘴唇从 RT Corner -> MD -> LF Corner 的有序 Guide。"""
        upper_names = [
            "loc_rt_mouth_corner_guide_001",
            "loc_rt_upper_lip_guide_002",
            "loc_rt_upper_lip_guide_001",
            "loc_md_upper_lip_guide_001",
            "loc_lf_upper_lip_guide_001",
            "loc_lf_upper_lip_guide_002",
            "loc_lf_mouth_corner_guide_001",
        ]

        lower_names = [
            "loc_rt_mouth_corner_guide_001",
            "loc_rt_lower_lip_guide_002",
            "loc_rt_lower_lip_guide_001",
            "loc_md_lower_lip_guide_001",
            "loc_lf_lower_lip_guide_001",
            "loc_lf_lower_lip_guide_002",
            "loc_lf_mouth_corner_guide_001",
        ]

        upper_guides = []
        lower_guides = []

        for guide_name in upper_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                upper_guides.append(
                    guide
                )

        for guide_name in lower_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                lower_guides.append(
                    guide
                )

        corners = []

        right_corner = self.get_guide_node(
            "loc_rt_mouth_corner_guide_001",
            required=required
        )
        left_corner = self.get_guide_node(
            "loc_lf_mouth_corner_guide_001",
            required=required
        )

        if right_corner:
            corners.append(
                right_corner
            )

        if left_corner:
            corners.append(
                left_corner
            )

        return {
            "upper": upper_guides,
            "lower": lower_guides,
            "corners": corners,
        }

    def get_eyelid_guides(self, side, required=True):
        u"""返回某一侧 Upper / Lower Eyelid 的有序 Guide。"""
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Eyelid side 必须是 lf 或 rt。"
            )

        inner_name = "loc_{}_inner_lid_guide_001".format(
            side
        )
        outer_name = "loc_{}_outer_lid_guide_001".format(
            side
        )

        upper_names = [
            inner_name,
            "loc_{}_upper_lid_guide_001".format(side),
            "loc_{}_upper_lid_guide_002".format(side),
            "loc_{}_upper_lid_guide_003".format(side),
            outer_name,
        ]

        lower_names = [
            inner_name,
            "loc_{}_lower_lid_guide_001".format(side),
            "loc_{}_lower_lid_guide_002".format(side),
            "loc_{}_lower_lid_guide_003".format(side),
            outer_name,
        ]

        upper_guides = []
        lower_guides = []

        for guide_name in upper_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                upper_guides.append(
                    guide
                )

        for guide_name in lower_names:
            guide = self.get_guide_node(
                guide_name,
                required=required
            )

            if guide:
                lower_guides.append(
                    guide
                )

        return {
            "upper": upper_guides,
            "lower": lower_guides,
        }

    def get_brow_guides(self, side):
        u"""返回某一侧 Brow Main 和 Brow Point Guide。"""
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Brow side 必须是 lf 或 rt。"
            )

        all_guides = self.get_part_guides(
            part="brow",
            side=side
        )

        main_guide = None
        point_guides = []

        for guide in all_guides:
            short_name = self.get_short_name(
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

    def get_eye_guides(self, side, required=False):
        u"""返回某一侧 Eye Ball / Iris Guide。"""
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Eye side 必须是 lf 或 rt。"
            )

        eye_ball = self.get_guide_node(
            "loc_{}_eye_ball_guide_001".format(side),
            required=required
        )
        eye_iris = self.get_guide_node(
            "loc_{}_eye_iris_guide_001".format(side),
            required=required
        )

        return {
            "eye_ball": eye_ball,
            "eye_iris": eye_iris,
        }

    def get_eye_bag_guides(self, side):
        u"""返回某一侧 Eye Bag Guide。"""
        if side not in ["lf", "rt"]:
            raise ValueError(
                u"Eye Bag side 必须是 lf 或 rt。"
            )

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
    # Symmetry - Name / Parent
    # =========================================================================

    @staticmethod
    def get_right_name(left_name):
        u"""把 lf 命名转换为对应 rt 命名。"""
        if "_lf_" not in left_name:
            raise ValueError(
                u"节点名称中没有 _lf_，无法生成右侧名称: {}".format(
                    left_name
                )
            )

        return left_name.replace(
            "_lf_",
            "_rt_",
            1
        )

    def get_mirror_parent(self, left_parent):
        u"""
        获取一个左侧 Parent 对应的右侧 Parent。

        MD / 公共 Group：左右共用同一个 Parent。
        LF Parent：必须找到对应的 RT Parent。
        """
        if not left_parent:
            return None

        left_parent_name = self.get_short_name(
            left_parent
        )

        if "_lf_" not in left_parent_name:
            return left_parent

        right_parent_name = self.get_right_name(
            left_parent_name
        )

        right_parent = self.get_guide_node(
            right_parent_name,
            required=False
        )

        if not right_parent:
            raise RuntimeError(
                u"找不到嵌套 Guide 对应的右侧 Parent: {} -> {}".format(
                    left_parent_name,
                    right_parent_name
                )
            )

        return right_parent

    def get_left_zero_groups(self, parent_group=None):
        u"""查找需要镜像 / 修复的 zero_lf_* Guide Group。"""
        if parent_group is None:
            parent_group = self.face_guide_grp

        if not cmds.objExists(parent_group):
            return []

        descendants = cmds.listRelatives(
            parent_group,
            allDescendents=True,
            type="transform",
            fullPath=True
        )

        if descendants is None:
            descendants = []

        left_zero_groups = []

        for node in descendants:
            short_name = self.get_short_name(
                node
            )

            if not short_name.startswith("zero_lf_"):
                continue

            left_zero_groups.append(
                node
            )

        # 父级 Guide 必须先修复，子级才可以找到正确的 RT Parent。
        left_zero_groups.sort(
            key=self.get_dag_depth
        )

        return left_zero_groups

    def get_left_locator(self, left_zero_group):
        u"""获取 zero_lf_* 下对应的 loc_lf_* Transform。"""
        children = cmds.listRelatives(
            left_zero_group,
            children=True,
            type="transform",
            fullPath=True
        )

        if children is None:
            children = []

        for child in children:
            short_name = self.get_short_name(
                child
            )

            if short_name.startswith("loc_lf_"):
                return child

        return None

    # =========================================================================
    # Symmetry - Repair Helper
    # =========================================================================

    @staticmethod
    def set_attr_preserve_lock(
            node,
            attribute,
            value
    ):
        u"""设置属性值，并恢复属性原来的 Lock 状态。"""
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

    @staticmethod
    def connect_attr_preserve_lock(
            source_attr,
            destination_attr
    ):
        u"""连接属性，并恢复目标属性原来的 Lock 状态。"""
        if not cmds.objExists(source_attr):
            return False

        if not cmds.objExists(destination_attr):
            return False

        if cmds.isConnected(
                source_attr,
                destination_attr
        ):
            return True

        was_locked = cmds.getAttr(
            destination_attr,
            lock=True
        )

        if was_locked:
            cmds.setAttr(
                destination_attr,
                lock=False
            )

        try:
            cmds.connectAttr(
                source_attr,
                destination_attr,
                force=True
            )
        finally:
            if was_locked:
                cmds.setAttr(
                    destination_attr,
                    lock=True
                )

        return True

    def create_or_update_right_zero(self, left_zero_group):
        u"""
        创建或修复对应 zero_rt_*。

        Root LF Zero 在公共 Parent 下建立一次 X 镜像空间。
        Nested LF Zero 的 Parent 已经是 RT 镜像空间，因此只复制 Local Transform。
        """
        left_zero_name = self.get_short_name(
            left_zero_group
        )
        right_zero_name = self.get_right_name(
            left_zero_name
        )

        left_parent = self.get_parent(
            left_zero_group
        )
        right_parent = self.get_mirror_parent(
            left_parent
        )

        right_zero_group = self.get_node_under_parent(
            right_parent,
            right_zero_name
        )

        if right_zero_group is None:
            right_zero_group = self.get_guide_node(
                right_zero_name,
                required=False
            )

        if right_zero_group is None:
            right_zero_group = cmds.createNode(
                "transform",
                name=right_zero_name
            )

        current_parent = self.get_parent(
            right_zero_group
        )

        if right_parent:
            if current_parent != right_parent:
                parent_result = cmds.parent(
                    right_zero_group,
                    right_parent
                )

                if parent_result:
                    right_zero_group = parent_result[0]

        rotate_order = cmds.getAttr(
            left_zero_group + ".rotateOrder"
        )

        self.set_attr_preserve_lock(
            right_zero_group,
            "rotateOrder",
            rotate_order
        )

        translate_x = cmds.getAttr(
            left_zero_group + ".translateX"
        )
        translate_y = cmds.getAttr(
            left_zero_group + ".translateY"
        )
        translate_z = cmds.getAttr(
            left_zero_group + ".translateZ"
        )

        rotate_x = cmds.getAttr(
            left_zero_group + ".rotateX"
        )
        rotate_y = cmds.getAttr(
            left_zero_group + ".rotateY"
        )
        rotate_z = cmds.getAttr(
            left_zero_group + ".rotateZ"
        )

        scale_x = cmds.getAttr(
            left_zero_group + ".scaleX"
        )
        scale_y = cmds.getAttr(
            left_zero_group + ".scaleY"
        )
        scale_z = cmds.getAttr(
            left_zero_group + ".scaleZ"
        )

        is_mirror_root = True

        if left_parent:
            left_parent_name = self.get_short_name(
                left_parent
            )

            if "_lf_" in left_parent_name:
                is_mirror_root = False

        if is_mirror_root:
            self.set_attr_preserve_lock(
                right_zero_group,
                "translateX",
                -translate_x
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "translateY",
                translate_y
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "translateZ",
                translate_z
            )

            self.set_attr_preserve_lock(
                right_zero_group,
                "rotateX",
                rotate_x
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "rotateY",
                rotate_y
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "rotateZ",
                rotate_z
            )

            self.set_attr_preserve_lock(
                right_zero_group,
                "scaleX",
                -scale_x
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "scaleY",
                scale_y
            )
            self.set_attr_preserve_lock(
                right_zero_group,
                "scaleZ",
                scale_z
            )

        else:
            local_attributes = [
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

            for attribute in local_attributes:
                value = cmds.getAttr(
                    "{}.{}".format(
                        left_zero_group,
                        attribute
                    )
                )

                self.set_attr_preserve_lock(
                    right_zero_group,
                    attribute,
                    value
                )

        return right_zero_group

    def create_or_update_right_locator(
            self,
            left_locator,
            right_zero_group
    ):
        u"""创建、复用或重新挂接对应 loc_rt_*。"""
        left_locator_name = self.get_short_name(
            left_locator
        )
        right_locator_name = self.get_right_name(
            left_locator_name
        )

        right_locator = self.get_node_under_parent(
            right_zero_group,
            right_locator_name
        )

        if right_locator is None:
            right_locator = self.get_guide_node(
                right_locator_name,
                required=False
            )

        if right_locator is None:
            right_locator = cmds.spaceLocator(
                name=right_locator_name
            )[0]

        current_parent = self.get_parent(
            right_locator
        )

        if current_parent != right_zero_group:
            parent_result = cmds.parent(
                right_locator,
                right_zero_group
            )

            if parent_result:
                right_locator = parent_result[0]

        return right_locator

    def connect_locator_transform(
            self,
            left_locator,
            right_locator
    ):
        u"""把左侧 Locator Transform 属性直接连接到右侧。"""
        attributes = [
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

        for attribute in attributes:
            source_attr = "{}.{}".format(
                left_locator,
                attribute
            )
            destination_attr = "{}.{}".format(
                right_locator,
                attribute
            )

            self.connect_attr_preserve_lock(
                source_attr,
                destination_attr
            )

        return True

    def connect_locator_shape(
            self,
            left_locator,
            right_locator
    ):
        u"""连接 Locator Shape 的 localPosition / localScale。"""
        left_shapes = self.get_locator_shapes(
            left_locator
        )
        right_shapes = self.get_locator_shapes(
            right_locator
        )

        if not left_shapes:
            return False

        if not right_shapes:
            return False

        left_shape = left_shapes[0]
        right_shape = right_shapes[0]

        shape_attributes = [
            "localPositionX",
            "localPositionY",
            "localPositionZ",
            "localScaleX",
            "localScaleY",
            "localScaleZ",
        ]

        for attribute in shape_attributes:
            source_attr = "{}.{}".format(
                left_shape,
                attribute
            )
            destination_attr = "{}.{}".format(
                right_shape,
                attribute
            )

            self.connect_attr_preserve_lock(
                source_attr,
                destination_attr
            )

        return True

    # =========================================================================
    # Symmetry - Validate / Repair
    # =========================================================================

    def validate_symmetry(self):
        u"""检查 LF -> RT Guide 节点、Parent 和 Transform 连接是否完整。"""
        result = {
            "valid": True,
            "missing_nodes": [],
            "wrong_parents": [],
            "broken_connections": [],
        }

        if not self.guide_exists():
            result["valid"] = False
            result["missing_nodes"].append(
                self.guide_move_ctrl_name
            )
            return result

        left_zero_groups = self.get_left_zero_groups(
            self.face_guide_grp
        )

        for left_zero_group in left_zero_groups:
            left_zero_name = self.get_short_name(
                left_zero_group
            )
            right_zero_name = self.get_right_name(
                left_zero_name
            )

            right_zero_group = self.get_guide_node(
                right_zero_name,
                required=False
            )

            if not right_zero_group:
                result["missing_nodes"].append(
                    right_zero_name
                )
                continue

            left_parent = self.get_parent(
                left_zero_group
            )

            try:
                expected_right_parent = self.get_mirror_parent(
                    left_parent
                )
            except RuntimeError:
                expected_right_parent = None

            actual_right_parent = self.get_parent(
                right_zero_group
            )

            if expected_right_parent:
                expected_parent_name = self.get_short_name(
                    expected_right_parent
                )
                actual_parent_name = self.get_short_name(
                    actual_right_parent
                )

                if expected_parent_name != actual_parent_name:
                    result["wrong_parents"].append(
                        "{} -> {}".format(
                            right_zero_name,
                            expected_parent_name
                        )
                    )

            left_locator = self.get_left_locator(
                left_zero_group
            )

            if not left_locator:
                continue

            left_locator_name = self.get_short_name(
                left_locator
            )
            right_locator_name = self.get_right_name(
                left_locator_name
            )

            right_locator = self.get_guide_node(
                right_locator_name,
                required=False
            )

            if not right_locator:
                result["missing_nodes"].append(
                    right_locator_name
                )
                continue

            attributes = [
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

            for attribute in attributes:
                source_attr = "{}.{}".format(
                    left_locator,
                    attribute
                )
                destination_attr = "{}.{}".format(
                    right_locator,
                    attribute
                )

                if cmds.isConnected(
                        source_attr,
                        destination_attr
                ):
                    continue

                result["broken_connections"].append(
                    "{} -> {}".format(
                        source_attr,
                        destination_attr
                    )
                )

        if result["missing_nodes"]:
            result["valid"] = False

        if result["wrong_parents"]:
            result["valid"] = False

        if result["broken_connections"]:
            result["valid"] = False

        return result

    def mirror_left_guide(
            self,
            left_zero_group
    ):
        u"""
        修复一个 zero_lf_* + loc_lf_* Guide 镜像层级。

        保留旧 API 名称用于兼容，新代码推荐通过 repair_symmetry() 批量修复。
        """
        left_locator = self.get_left_locator(
            left_zero_group
        )

        if left_locator is None:
            raise RuntimeError(
                u"没有在 {} 下找到 loc_lf_*。".format(
                    left_zero_group
                )
            )

        right_zero_group = self.create_or_update_right_zero(
            left_zero_group
        )

        right_locator = self.create_or_update_right_locator(
            left_locator,
            right_zero_group
        )

        self.connect_locator_transform(
            left_locator,
            right_locator
        )
        self.connect_locator_shape(
            left_locator,
            right_locator
        )

        return {
            "left_zero": left_zero_group,
            "left_locator": left_locator,
            "right_zero": right_zero_group,
            "right_locator": right_locator,
        }

    def mirror_left_guides(self, parent_group=None):
        u"""批量修复全部 zero_lf_* Guide；正常 build() 不主动调用。"""
        if parent_group is None:
            parent_group = self.face_guide_grp

        left_zero_groups = self.get_left_zero_groups(
            parent_group=parent_group
        )

        results = []

        for left_zero_group in left_zero_groups:
            result = self.mirror_left_guide(
                left_zero_group
            )

            results.append(
                result
            )

        return results

    def repair_symmetry(self):
        u"""修复 Guide 左右节点层级和连接，并返回修复后的检查结果。"""
        repair_results = self.mirror_left_guides(
            parent_group=self.face_guide_grp
        )

        validation = self.validate_symmetry()

        return {
            "repairs": repair_results,
            "validation": validation,
        }

    # =========================================================================
    # Validation
    # =========================================================================

    def validate_guides(self, check_symmetry=True):
        u"""
        检查 Step 02 Guide 是否可以交给后续 Builder。

        返回结构化结果，而不是遇到第一个问题就立即抛错，
        方便 Wizard 后面一次展示全部问题。
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "guide_count": 0,
            "symmetry": None,
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
                u"Face Guide 模板尚未加载，缺少 {}。".format(
                    self.guide_move_ctrl_name
                )
            )

        locators = self.get_guide_locators()
        result["guide_count"] = len(locators)

        if not locators:
            result["errors"].append(
                u"Face Guide 层级中没有找到 Locator。"
            )

        for guide_name in self.required_guide_names:
            guide = self.get_guide_node(
                guide_name,
                required=False
            )

            if guide:
                continue

            result["errors"].append(
                u"缺少必要 Guide: {}".format(
                    guide_name
                )
            )

        name_counts = {}

        for locator in locators:
            short_name = self.get_short_name(
                locator
            )

            if short_name not in name_counts:
                name_counts[short_name] = 0

            name_counts[short_name] += 1

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

        if check_symmetry:
            symmetry_result = self.validate_symmetry()
            result["symmetry"] = symmetry_result

            for missing_node in symmetry_result["missing_nodes"]:
                result["errors"].append(
                    u"左右镜像缺少节点: {}".format(
                        missing_node
                    )
                )

            for wrong_parent in symmetry_result["wrong_parents"]:
                result["errors"].append(
                    u"右侧 Guide Parent 错误: {}".format(
                        wrong_parent
                    )
                )

            for broken_connection in symmetry_result["broken_connections"]:
                result["errors"].append(
                    u"左右镜像连接断开: {}".format(
                        broken_connection
                    )
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

    # =========================================================================
    # Build / Finalize
    # =========================================================================

    def build(self):
        u"""
        创建或恢复可供绑定师编辑的 Face Guide。

        Build 只负责：
            1. 验证 Step 01；
            2. 确保 Face 主层级；
            3. 导入 / 复用 face_guide.ma；
            4. 保存 Guide Config；
            5. Step 02 保持未完成。

        用户完成手动贴合后，再调用 finalize()。
        """
        self.validate_setup()
        self.ensure_hierarchy()
        self.ensure_config_node()

        import_result = self.import_guide_template()

        self.save_guide_config()

        self.set_step_completed(
            completed=False
        )
        self.invalidate_later_steps()

        return import_result

    def finalize(self, check_symmetry=True):
        u"""
        完成 Step 02。

        Finalize 不创建正式 Rig，只确认 Guide 数据完整并保存状态。
        """
        self.validate_setup()

        validation = self.validate_guides(
            check_symmetry=check_symmetry
        )

        if not validation["valid"]:
            error_message = u"Face Guide Validation 失败："

            for error in validation["errors"]:
                error_message += u"\n- {}".format(
                    error
                )

            raise RuntimeError(
                error_message
            )

        self.save_guide_config()

        self.set_step_completed(
            completed=True
        )
        self.invalidate_later_steps()

        return validation


__all__ = [
    "FaceGuide",
]
