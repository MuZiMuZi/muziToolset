# coding=utf-8
u"""
Hierarchy Cleaner
=================

Maya 2023 / PySide2 场景层级清理工具。

安全原则：
    1. 默认只处理当前选择，避免误伤整个 Rig 场景；
    2. 空组删除会递归执行，直到没有新的空父组；
    3. Delete History / Freeze 会跳过明显的绑定、动画和约束节点；
    4. 全场景模式执行前需要再次确认；
    5. 所有修改包装在一个 Maya Undo Chunk 中。
"""

from __future__ import print_function

import maya.cmds as cmds

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QCheckBox
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QFrame
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QMessageBox
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout

from ....core import qtUtils


_window = None

_DEFAULT_CAMERAS = {
    "persp",
    "top",
    "front",
    "side",
}

_RIG_HISTORY_TYPES = {
    "skinCluster",
    "blendShape",
    "cluster",
    "wire",
    "ffd",
    "lattice",
    "nonLinear",
    "deltaMush",
    "tension",
    "wrap",
    "proximityWrap",
}

_CONSTRAINT_TYPES = {
    "parentConstraint",
    "pointConstraint",
    "orientConstraint",
    "scaleConstraint",
    "aimConstraint",
    "poleVectorConstraint",
}


def _short_name(node):
    return node.split("|")[-1]


def _is_default_camera(node):
    return _short_name(node) in _DEFAULT_CAMERAS


def _is_referenced(node):
    try:
        return cmds.referenceQuery(node, isNodeReferenced=True)
    except Exception:
        return False


def _existing_nodes(nodes):
    result = []

    if not nodes:
        return result

    for node in nodes:
        if not node:
            continue

        if not cmds.objExists(node):
            continue

        matches = cmds.ls(node, long=True) or [node]
        resolved = matches[0]

        if resolved not in result:
            result.append(resolved)

    return result


def _all_transform_nodes():
    return cmds.ls(type="transform", long=True) or []


def _has_incoming_animation(node):
    anim_curve_types = [
        "animCurveTA",
        "animCurveTL",
        "animCurveTT",
        "animCurveTU",
    ]

    for anim_type in anim_curve_types:
        connections = cmds.listConnections(
            node,
            source=True,
            destination=False,
            type=anim_type
        ) or []

        if connections:
            return True

    return False


def _has_constraint(node):
    connections = cmds.listConnections(
        node,
        source=True,
        destination=False
    ) or []

    for connection in connections:
        try:
            node_type = cmds.nodeType(connection)
        except Exception:
            continue

        if node_type in _CONSTRAINT_TYPES:
            return True

    return False


def _has_rig_history(node):
    history = cmds.listHistory(node, pruneDagObjects=True) or []

    for history_node in history:
        try:
            node_type = cmds.nodeType(history_node)
        except Exception:
            continue

        if node_type in _RIG_HISTORY_TYPES:
            return True

    return False


def _can_modify_transform(node):
    if not cmds.objExists(node):
        return False

    if _is_default_camera(node):
        return False

    if _is_referenced(node):
        return False

    node_type = cmds.nodeType(node)
    if node_type != "transform":
        return False

    return True


def delete_empty_groups(nodes=None):
    """
    递归删除空 Transform Group。

    Args:
        nodes(list/None):
            None 时检查整个场景；传列表时只检查列表及其父层级。

    Returns:
        int: 删除数量。
    """
    if nodes is None:
        candidates = _all_transform_nodes()
    else:
        candidates = _existing_nodes(nodes)

        parent_candidates = []
        for node in list(candidates):
            current = node

            while current:
                parents = cmds.listRelatives(
                    current,
                    parent=True,
                    fullPath=True
                ) or []

                if not parents:
                    break

                current = parents[0]
                if current not in parent_candidates:
                    parent_candidates.append(current)

        for parent in parent_candidates:
            if parent not in candidates:
                candidates.append(parent)

    deleted_count = 0
    changed = True

    while changed:
        changed = False

        current_candidates = []
        for node in candidates:
            if cmds.objExists(node):
                current_candidates.append(node)

        current_candidates.sort(
            key=lambda item: item.count("|"),
            reverse=True
        )

        for node in current_candidates:
            if not _can_modify_transform(node):
                continue

            shapes = cmds.listRelatives(
                node,
                shapes=True,
                fullPath=True
            ) or []

            children = cmds.listRelatives(
                node,
                children=True,
                fullPath=True
            ) or []

            if shapes or children:
                continue

            try:
                cmds.delete(node)
                deleted_count += 1
                changed = True
            except Exception as error:
                cmds.warning(
                    u"无法删除空组 {}：{}".format(
                        node,
                        error
                    )
                )

    return deleted_count


def delete_history(nodes):
    """
    删除安全范围内的构造历史。

    已检测到 SkinCluster / BlendShape / Wire 等 Rig Deformer 时会跳过，
    防止一个“清历史”按钮直接破坏绑定。
    """
    nodes = _existing_nodes(nodes)
    deleted_count = 0
    skipped_count = 0

    for node in nodes:
        if not _can_modify_transform(node):
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        ) or []

        if not shapes:
            continue

        if _has_rig_history(node):
            skipped_count += 1
            continue

        try:
            cmds.delete(node, constructionHistory=True)
            deleted_count += 1
        except Exception as error:
            cmds.warning(
                u"无法删除历史 {}：{}".format(
                    node,
                    error
                )
            )

    return deleted_count, skipped_count


def freeze_transformations(nodes):
    """
    冻结安全范围内的 Transform。

    有动画、约束、绑定 Deformer 或引用来源的节点会跳过。
    """
    nodes = _existing_nodes(nodes)
    frozen_count = 0
    skipped_count = 0

    for node in nodes:
        if not _can_modify_transform(node):
            skipped_count += 1
            continue

        if _has_incoming_animation(node):
            skipped_count += 1
            continue

        if _has_constraint(node):
            skipped_count += 1
            continue

        if _has_rig_history(node):
            skipped_count += 1
            continue

        try:
            cmds.makeIdentity(
                node,
                apply=True,
                translate=True,
                rotate=True,
                scale=True,
                normal=False,
                preserveNormals=True
            )
            frozen_count += 1
        except Exception as error:
            cmds.warning(
                u"无法冻结变换 {}：{}".format(
                    node,
                    error
                )
            )

    return frozen_count, skipped_count


def unlock_and_show_attributes(nodes):
    """解锁并显示标准 Transform 属性。"""
    nodes = _existing_nodes(nodes)

    attrs = [
        "tx",
        "ty",
        "tz",
        "rx",
        "ry",
        "rz",
        "sx",
        "sy",
        "sz",
        "v",
    ]

    changed_count = 0

    for node in nodes:
        if _is_referenced(node):
            continue

        for attr in attrs:
            if not cmds.attributeQuery(
                    attr,
                    node=node,
                    exists=True
            ):
                continue

            plug = "{}.{}".format(node, attr)

            try:
                cmds.setAttr(plug, lock=False)
                cmds.setAttr(plug, keyable=True)
                changed_count += 1
            except Exception:
                pass

    return changed_count


def center_pivot(nodes):
    """把可编辑几何 Transform 的 Pivot 居中。"""
    nodes = _existing_nodes(nodes)
    centered_count = 0

    for node in nodes:
        if not _can_modify_transform(node):
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        ) or []

        if not shapes:
            continue

        try:
            cmds.xform(node, centerPivots=True)
            centered_count += 1
        except Exception:
            pass

    return centered_count


def delete_unknown_nodes(nodes=None):
    """删除 Unknown 节点；传入 nodes 时只处理选择范围。"""
    if nodes is None:
        unknown_nodes = cmds.ls(type="unknown", long=True) or []
    else:
        unknown_nodes = []

        for node in _existing_nodes(nodes):
            if cmds.nodeType(node) == "unknown":
                unknown_nodes.append(node)

    deleted_count = 0

    for node in unknown_nodes:
        if _is_referenced(node):
            continue

        try:
            cmds.delete(node)
            deleted_count += 1
        except Exception as error:
            cmds.warning(
                u"无法删除 Unknown 节点 {}：{}".format(
                    node,
                    error
                )
            )

    return deleted_count


class HierarchyCleanerUI(QDialog):
    """层级清理器窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(HierarchyCleanerUI, self).__init__(parent)
        self.setWindowTitle(u"层级清理器")
        self.setMinimumWidth(360)

        self.title_label = QLabel(u"Hierarchy Cleaner")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.delete_empty_check = QCheckBox(u"删除空组")
        self.delete_empty_check.setChecked(True)

        self.delete_history_check = QCheckBox(u"删除安全范围内构造历史")
        self.delete_history_check.setChecked(False)

        self.freeze_check = QCheckBox(u"冻结安全范围内 Transform")
        self.freeze_check.setChecked(False)

        self.unlock_check = QCheckBox(u"解锁并显示标准 Transform 属性")
        self.unlock_check.setChecked(False)

        self.center_pivot_check = QCheckBox(u"几何体 Pivot 居中")
        self.center_pivot_check.setChecked(False)

        self.delete_unknown_check = QCheckBox(u"删除 Unknown 节点")
        self.delete_unknown_check.setChecked(True)

        self.selected_only_check = QCheckBox(u"仅处理当前选择")
        self.selected_only_check.setChecked(True)

        self.execute_btn = QPushButton(u"执行清理")
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)

        self._create_layout()
        self._create_connections()

    def _create_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(7)

        main_layout.addWidget(self.title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)

        main_layout.addWidget(self.delete_empty_check)
        main_layout.addWidget(self.delete_history_check)
        main_layout.addWidget(self.freeze_check)
        main_layout.addWidget(self.unlock_check)
        main_layout.addWidget(self.center_pivot_check)
        main_layout.addWidget(self.delete_unknown_check)
        main_layout.addWidget(self.selected_only_check)
        main_layout.addWidget(self.execute_btn)
        main_layout.addWidget(self.result_label)

    def _create_connections(self):
        self.execute_btn.clicked.connect(self.execute_cleanup)

    def _scope_nodes(self):
        if self.selected_only_check.isChecked():
            return cmds.ls(selection=True, long=True) or []

        return _all_transform_nodes()

    def _confirm_whole_scene(self):
        if self.selected_only_check.isChecked():
            return True

        result = QMessageBox.warning(
            self,
            u"确认全场景清理",
            u"你关闭了“仅处理当前选择”。\n\n"
            u"本次操作将扫描整个场景。历史、冻结、解锁等操作仍会跳过明显的 Rig 节点，"
            u"但建议先保存场景。是否继续？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        return result == QMessageBox.Yes

    def execute_cleanup(self):
        if not self._confirm_whole_scene():
            return

        selected_only = self.selected_only_check.isChecked()

        if selected_only:
            nodes = cmds.ls(selection=True, long=True) or []
            if not nodes:
                self.result_label.setText(u"请先选择需要清理的对象。")
                return
        else:
            nodes = _all_transform_nodes()

        result_lines = []

        cmds.undoInfo(openChunk=True, chunkName="MuziHierarchyCleaner")
        try:
            if self.delete_empty_check.isChecked():
                empty_scope = nodes
                if not selected_only:
                    empty_scope = None

                count = delete_empty_groups(empty_scope)
                result_lines.append(u"空组：删除 {}".format(count))

            if self.delete_history_check.isChecked():
                deleted_count, skipped_count = delete_history(nodes)
                result_lines.append(
                    u"历史：处理 {} / 跳过 Rig {}".format(
                        deleted_count,
                        skipped_count
                    )
                )

            if self.freeze_check.isChecked():
                frozen_count, skipped_count = freeze_transformations(nodes)
                result_lines.append(
                    u"冻结：处理 {} / 跳过 {}".format(
                        frozen_count,
                        skipped_count
                    )
                )

            if self.unlock_check.isChecked():
                count = unlock_and_show_attributes(nodes)
                result_lines.append(u"属性：修改 {} 项".format(count))

            if self.center_pivot_check.isChecked():
                count = center_pivot(nodes)
                result_lines.append(u"Pivot：处理 {}".format(count))

            if self.delete_unknown_check.isChecked():
                unknown_scope = nodes
                if not selected_only:
                    unknown_scope = None

                count = delete_unknown_nodes(unknown_scope)
                result_lines.append(u"Unknown：删除 {}".format(count))

        except Exception as error:
            cmds.warning(str(error))
            result_lines.append(u"执行失败：{}".format(error))
        finally:
            cmds.undoInfo(closeChunk=True)

        if not result_lines:
            result_lines.append(u"没有启用任何清理选项。")

        self.result_label.setText(u"\n".join(result_lines))


# 旧类名兼容。
Hierarchy_Cleaner_UI = HierarchyCleanerUI


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = HierarchyCleanerUI()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window


if __name__ == "__main__":
    main()
