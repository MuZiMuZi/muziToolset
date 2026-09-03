# coding=utf-8
u"""
Face Guide Long Path Compatibility
==================================

在正式 FaceGuide 之上补充 Long DAG Path / Maya Namespace 安全的模板 Root 识别。

背景：
    FaceBase.ensure_hierarchy() 现在会缓存真实 DAG Long Path，例如：

        |grp_md_face_master_001|grp_md_face_guide_001

    face_guide.ma 中的模板 Root 则仍然使用标准 Rig Short Name：

        grp_md_face_guide_001

    因此模板导入识别不能直接比较 Short Name 与 Long Path，而应统一比较
    去掉 DAG Path 和 Namespace 后的标准 Rig Name。

边界：
    - 不修改 Face Guide Template；
    - 不退回 Short Path 架构；
    - 不改变 Guide Build / Mirror / Validation 的其它业务逻辑；
    - 只覆盖 Template Root 解析方法。
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


__all__ = [
    "FaceGuide",
]
