# coding=utf-8
u"""
Face Guide Long Path Compatibility
==================================

在正式 FaceGuide 之上补充 Long DAG Path / Maya Namespace 安全的 Guide 查询。

背景：
    FaceBase.ensure_hierarchy() 现在会缓存真实 DAG Long Path，例如：

        |grp_md_face_master_001|grp_md_face_guide_001

    当 Face Rig 位于 Maya Namespace 中时，同一个节点还可能表现为：

        |muziSmoke:grp_md_face_master_001|muziSmoke:grp_md_face_guide_001

    face_guide.ma 与正式 Rig Schema 仍使用不带 Namespace 的标准名称，因此所有
    Guide 名称比较都必须先统一成去掉 DAG Path 和 Namespace 的 Canonical Name。

边界：
    - 不修改 Face Guide Template；
    - 不退回 Short Path 架构；
    - 不改变 Guide Build / Mirror / Validation 的业务规则；
    - 只覆盖依赖标准 Rig Short Name 比较的查询与校验方法。
"""

from __future__ import print_function

import maya.cmds as cmds

from ....core import hierarchy_utils
from ....core import rename_utils
from .face_guide import FaceGuide as _BaseFaceGuide


class FaceGuide(_BaseFaceGuide):
    u"""Long Path / Namespace 安全的正式 FaceGuide。"""

    @staticmethod
    def get_canonical_node_name(node):
        u"""
        返回去掉 DAG Path 和 Maya Namespace 后的标准节点名称。

        Args:
            node (str):
                Maya Node Short Name、Long Path 或带 Namespace 的名称。

        Returns:
            str:
                可用于 Rig 标准名称比较的 Canonical Short Name。
        """
        short_name = rename_utils.get_short_name(
            node
        )

        if not short_name:
            return ""

        return short_name.rsplit(
            ":",
            1
        )[-1]

    def get_imported_template_root(self, imported_nodes):
        u"""
        从本次导入的新节点中找到唯一 Face Guide Template Root。

        Root 判断规则：
            1. 必须属于本次 Import 返回的新 Transform；
            2. 必须位于 World；
            3. 去掉 DAG Path / Namespace 后必须等于当前 Face Guide 标准名称。

        Args:
            imported_nodes (list[str]):
                本次导入 face_guide.ma 后 Maya 返回的新节点列表。

        Returns:
            str:
                唯一 Template Root 的 Long DAG Path。

        Raises:
            RuntimeError:
                找不到 Root 或存在多个同名候选时抛出。
        """
        imported_transforms = cmds.ls(
            imported_nodes,
            type="transform",
            long=True
        )

        if imported_transforms is None:
            imported_transforms = []

        expected_root_name = self.get_canonical_node_name(
            self.face_guide_grp
        )
        candidates = []

        for node in imported_transforms:
            parent = hierarchy_utils.get_parent(
                node
            )

            if parent:
                continue

            canonical_name = self.get_canonical_node_name(
                node
            )

            if canonical_name != expected_root_name:
                continue

            if node in candidates:
                continue

            candidates.append(
                node
            )

        if len(candidates) != 1:
            raise RuntimeError(
                u"无法唯一识别 Face Guide Template Root，标准名称: {}，候选数量: {}".format(
                    expected_root_name,
                    len(candidates)
                )
            )

        return candidates[0]

    def get_guide_node(
            self,
            short_name,
            required=False
    ):
        u"""
        在正式 Face Guide 层级中按 Canonical Short Name 查找 Transform。

        Args:
            short_name (str):
                标准 Rig Name、带 Namespace 的 Short Name 或 Long DAG Path。
            required (bool):
                目标不存在时是否直接抛出异常。

        Returns:
            str | None:
                唯一匹配的 Guide Transform Long Path；没有匹配时返回 None。

        Raises:
            RuntimeError:
                required=True 且目标不存在，或同一 Guide 层级出现多个 Canonical
                同名 Transform 时抛出。
        """
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

        expected_name = self.get_canonical_node_name(
            short_name
        )
        candidates = []
        root_name = self.get_canonical_node_name(
            self.face_guide_grp
        )

        if root_name == expected_name:
            candidates.append(
                self.face_guide_grp
            )

        descendants = hierarchy_utils.get_descendants(
            self.face_guide_grp,
            node_type="transform",
            full_path=True
        )

        for node in descendants:
            canonical_name = self.get_canonical_node_name(
                node
            )

            if canonical_name != expected_name:
                continue

            candidates.append(
                node
            )

        if len(candidates) == 1:
            return candidates[0]

        if len(candidates) > 1:
            raise RuntimeError(
                u"Face Guide 中存在多个 Canonical 同名节点: {}".format(
                    expected_name
                )
            )

        if required:
            raise RuntimeError(
                u"没有找到 Face Guide 节点: {}".format(
                    expected_name
                )
            )

        return None

    def get_guide_locators(self):
        u"""
        获取正式 Guide 层级中的全部 Locator Transform，并忽略 Namespace 前缀。

        Returns:
            list[str]:
                按 Canonical Rig Name 排序的 Locator Transform Long Path。
        """
        if not cmds.objExists(self.face_guide_grp):
            return []

        descendants = hierarchy_utils.get_descendants(
            self.face_guide_grp,
            node_type="transform",
            full_path=True
        )
        locators = []

        for node in descendants:
            canonical_name = self.get_canonical_node_name(
                node
            )

            if not canonical_name.startswith("loc_"):
                continue

            if "_guide_" not in canonical_name:
                continue

            if not self.get_locator_shapes(node):
                continue

            locators.append(
                node
            )

        locators.sort(
            key=self.get_canonical_node_name
        )
        return locators

    def get_side_zero_groups(self, side):
        u"""
        返回指定 Side 下全部 Guide Zero Group，并忽略 Namespace 前缀。

        Args:
            side (str):
                方向标记，常用值为 lf 或 rt。

        Returns:
            list[str]:
                按 DAG 深度排序的 Guide Zero Group Long Path。
        """
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
            canonical_name = self.get_canonical_node_name(
                node
            )

            if not canonical_name.startswith(prefix):
                continue

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
        u"""
        返回一个 Guide Zero Group 下对应 Side 的 Locator，并忽略 Namespace 前缀。

        Args:
            zero_group (str):
                当前 Guide Zero Group Transform。
            side (str):
                方向标记，常用值为 lf 或 rt。

        Returns:
            str | None:
                匹配的 Locator Transform Long Path；没有匹配时返回 None。
        """
        prefix = "loc_{}_".format(
            side
        )
        children = hierarchy_utils.get_children(
            zero_group,
            node_type="transform",
            full_path=True
        )

        for child in children:
            canonical_name = self.get_canonical_node_name(
                child
            )

            if canonical_name.startswith(prefix):
                return child

        return None

    def validate_guides(self):
        u"""
        按 Canonical Rig Name 检查模板中的每一个 Locator 是否仍然存在。

        Returns:
            dict:
                Guide 完整性、缺失项、重复项与额外 Locator 的结构化结果。
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

        locators = self.get_guide_locators()
        expected_names = self.get_template_locator_names()
        current_names = []
        name_counts = {}

        result["guide_count"] = len(locators)
        result["template_guide_count"] = len(expected_names)

        for locator in locators:
            canonical_name = self.get_canonical_node_name(
                locator
            )
            current_names.append(
                canonical_name
            )

            if canonical_name not in name_counts:
                name_counts[canonical_name] = 0

            name_counts[canonical_name] += 1

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

        for canonical_name in name_counts:
            if name_counts[canonical_name] <= 1:
                continue

            result["errors"].append(
                u"Guide Canonical 名称重复: {} x {}".format(
                    canonical_name,
                    name_counts[canonical_name]
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


__all__ = [
    "FaceGuide",
]
