# coding=utf-8
u"""
Model Checker
=============

Maya 2023 / PySide2 模型检查工具。

检查项：
    - Non-Manifold Vertex / Edge；
    - Lamina Face；
    - DAG 重名；
    - 建模历史（过滤 Skin / BlendShape 等正常 Rig Deformer）；
    - Mesh Transform 未冻结；
    - 锁定法线。

检查逻辑和修复逻辑分离。只有相对安全的项目允许自动修复，拓扑问题不会
直接“猜着修”，避免检查器把生产模型越修越坏。
"""

from __future__ import print_function

import re

import maya.cmds as cmds

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAbstractItemView
from PySide2.QtWidgets import QCheckBox
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QFrame
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QTableWidget
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtWidgets import QVBoxLayout

from ....core import qtUtils


_window = None

_DEFAULT_CAMERAS = {
    "persp",
    "top",
    "front",
    "side",
}

_DEFORMER_TYPES = {
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
    "sculpt",
}

_HISTORY_IGNORE_TYPES = {
    "mesh",
    "transform",
    "groupId",
    "groupParts",
    "objectSet",
    "shadingEngine",
    "tweak",
}


def _short_name(node):
    return node.split("|")[-1]


def _mesh_shapes_from_nodes(nodes=None):
    """把 Transform / Mesh 输入统一转成非 intermediate Mesh Shape。"""
    if nodes is None:
        return cmds.ls(
            type="mesh",
            long=True,
            noIntermediate=True
        ) or []

    if isinstance(nodes, str):
        nodes = [nodes]

    result = []

    for node in nodes:
        if not node or not cmds.objExists(node):
            continue

        node_type = cmds.nodeType(node)

        if node_type == "mesh":
            if not cmds.getAttr(node + ".intermediateObject"):
                matches = cmds.ls(node, long=True) or [node]
                mesh = matches[0]
                if mesh not in result:
                    result.append(mesh)
            continue

        if node_type not in ("transform", "joint"):
            continue

        shapes = cmds.listRelatives(
            node,
            shapes=True,
            noIntermediate=True,
            fullPath=True,
            type="mesh"
        ) or []

        for shape in shapes:
            if shape not in result:
                result.append(shape)

    return result


def _mesh_transform(mesh_shape):
    parents = cmds.listRelatives(
        mesh_shape,
        parent=True,
        fullPath=True
    ) or []

    if parents:
        return parents[0]

    return mesh_shape


def _mesh_transforms(meshes):
    result = []

    for mesh in meshes:
        transform = _mesh_transform(mesh)
        if transform not in result:
            result.append(transform)

    return result


def _is_referenced(node):
    try:
        return cmds.referenceQuery(node, isNodeReferenced=True)
    except Exception:
        return False


def _history_node_types(mesh):
    history = cmds.listHistory(
        mesh,
        pruneDagObjects=True
    ) or []

    result = []

    for node in history:
        try:
            node_type = cmds.nodeType(node)
        except Exception:
            continue

        if node_type in _HISTORY_IGNORE_TYPES:
            continue

        result.append((node, node_type))

    return result


def _modeling_history(mesh):
    """返回非 Deformer 的建模历史节点。"""
    result = []

    for node, node_type in _history_node_types(mesh):
        if node_type in _DEFORMER_TYPES:
            continue

        if cmds.objectType(node, isAType="geometryFilter"):
            continue

        result.append((node, node_type))

    return result


def _has_deformer_history(mesh):
    for node, node_type in _history_node_types(mesh):
        if node_type in _DEFORMER_TYPES:
            return True

        try:
            if cmds.objectType(node, isAType="geometryFilter"):
                return True
        except Exception:
            pass

    return False


def check_nonmanifold_geometry(meshes=None):
    meshes = _mesh_shapes_from_nodes(meshes)
    issues = []

    for mesh in meshes:
        try:
            vertices = cmds.polyInfo(
                mesh,
                nonManifoldVertices=True
            ) or []
            edges = cmds.polyInfo(
                mesh,
                nonManifoldEdges=True
            ) or []
        except Exception:
            continue

        if not vertices and not edges:
            continue

        issues.append({
            "node": _mesh_transform(mesh),
            "type": u"非流形几何体",
            "details": u"顶点 {} / 边 {}".format(
                len(vertices),
                len(edges)
            ),
            "fixable": False,
        })

    return issues


def check_lamina_faces(meshes=None):
    meshes = _mesh_shapes_from_nodes(meshes)
    issues = []

    for mesh in meshes:
        try:
            lamina_faces = cmds.polyInfo(
                mesh,
                laminaFaces=True
            ) or []
        except Exception:
            continue

        if not lamina_faces:
            continue

        issues.append({
            "node": _mesh_transform(mesh),
            "type": u"薄片面",
            "details": u"数量 {}".format(len(lamina_faces)),
            "fixable": False,
        })

    return issues


def check_duplicate_names(nodes=None):
    """检查 DAG 短名称冲突。"""
    if nodes is None:
        dag_nodes = cmds.ls(dag=True, long=True) or []
    else:
        dag_nodes = []
        for node in nodes:
            if not cmds.objExists(node):
                continue

            matches = cmds.ls(node, long=True) or [node]
            resolved = matches[0]

            if resolved not in dag_nodes:
                dag_nodes.append(resolved)

            descendants = cmds.listRelatives(
                resolved,
                allDescendents=True,
                fullPath=True
            ) or []

            for descendant in descendants:
                if descendant not in dag_nodes:
                    dag_nodes.append(descendant)

    name_map = {}

    for node in dag_nodes:
        short_name = _short_name(node)

        if short_name in _DEFAULT_CAMERAS:
            continue

        if short_name not in name_map:
            name_map[short_name] = []

        name_map[short_name].append(node)

    issues = []

    for short_name in sorted(name_map.keys()):
        matches = name_map[short_name]

        if len(matches) <= 1:
            continue

        issues.append({
            "node": matches[0],
            "type": u"重名",
            "details": u"{} 出现 {} 次".format(
                short_name,
                len(matches)
            ),
            "fixable": False,
        })

    return issues


def check_construction_history(meshes=None):
    meshes = _mesh_shapes_from_nodes(meshes)
    issues = []

    for mesh in meshes:
        history = _modeling_history(mesh)
        if not history:
            continue

        history_types = []
        for node, node_type in history:
            if node_type not in history_types:
                history_types.append(node_type)

        issues.append({
            "node": _mesh_transform(mesh),
            "type": u"遗留建模历史",
            "details": u"{} 个节点：{}".format(
                len(history),
                ", ".join(history_types[:6])
            ),
            "fixable": True,
        })

    return issues


def check_transformations(meshes=None):
    meshes = _mesh_shapes_from_nodes(meshes)
    transforms = _mesh_transforms(meshes)
    issues = []

    for node in transforms:
        if _short_name(node) in _DEFAULT_CAMERAS:
            continue

        try:
            translate = cmds.getAttr(node + ".translate")[0]
            rotate = cmds.getAttr(node + ".rotate")[0]
            scale = cmds.getAttr(node + ".scale")[0]
        except Exception:
            continue

        translation_bad = False
        rotation_bad = False
        scale_bad = False

        for value in translate:
            if abs(value) > 0.001:
                translation_bad = True
                break

        for value in rotate:
            if abs(value) > 0.001:
                rotation_bad = True
                break

        for value in scale:
            if abs(value - 1.0) > 0.001:
                scale_bad = True
                break

        if not translation_bad and not rotation_bad and not scale_bad:
            continue

        fixable = not _has_deformer_history(node)

        issues.append({
            "node": node,
            "type": u"Mesh Transform 未冻结",
            "details": u"T {} | R {} | S {}{}".format(
                [round(value, 3) for value in translate],
                [round(value, 3) for value in rotate],
                [round(value, 3) for value in scale],
                u" | 有 Deformer，不自动 Freeze" if not fixable else ""
            ),
            "fixable": fixable,
        })

    return issues


def check_locked_normals(meshes=None, sample_limit=500):
    meshes = _mesh_shapes_from_nodes(meshes)
    issues = []

    for mesh in meshes:
        vertices = cmds.ls(
            mesh + ".vtx[*]",
            flatten=True
        ) or []

        if not vertices:
            continue

        sample_count = min(len(vertices), sample_limit)
        locked_vertex_count = 0

        index = 0
        while index < sample_count:
            vertex = vertices[index]

            try:
                locked_values = cmds.polyNormalPerVertex(
                    vertex,
                    query=True,
                    freezeNormal=True
                ) or []
            except Exception:
                locked_values = []

            is_locked = False
            for value in locked_values:
                if value:
                    is_locked = True
                    break

            if is_locked:
                locked_vertex_count += 1

            index += 1

        if locked_vertex_count <= 0:
            continue

        details = u"采样 {} 个点，发现 {} 个锁定法线点".format(
            sample_count,
            locked_vertex_count
        )

        if len(vertices) > sample_count:
            details += u"（总点数 {}）".format(len(vertices))

        issues.append({
            "node": _mesh_transform(mesh),
            "type": u"法线被锁定",
            "details": details,
            "fixable": True,
        })

    return issues


def fix_issue(issue):
    """修复一个允许自动修复的问题。"""
    node = issue.get("node")
    issue_type = issue.get("type")

    if not issue.get("fixable"):
        return False

    if not node or not cmds.objExists(node):
        return False

    if _is_referenced(node):
        return False

    if issue_type == u"遗留建模历史":
        # 只删除 deformers 前后的建模历史，保留 Skin / BlendShape 等 Deformer。
        cmds.bakePartialHistory(
            node,
            prePostDeformers=True
        )
        return True

    if issue_type == u"Mesh Transform 未冻结":
        if _has_deformer_history(node):
            return False

        cmds.makeIdentity(
            node,
            apply=True,
            translate=True,
            rotate=True,
            scale=True,
            normal=False,
            preserveNormals=True
        )
        return True

    if issue_type == u"法线被锁定":
        cmds.polyNormalPerVertex(
            node,
            unFreezeNormal=True
        )
        return True

    return False


class ModelCheckerUI(QDialog):
    """模型检查器窗口。"""

    def __init__(self, parent=None):
        if parent is None:
            parent = qtUtils.get_maya_window()

        super(ModelCheckerUI, self).__init__(parent)
        self.setWindowTitle(u"模型检查工具")
        self.resize(680, 560)

        self.issues = []

        self.nonmanifold_check = QCheckBox(u"非流形")
        self.nonmanifold_check.setChecked(True)

        self.lamina_check = QCheckBox(u"Lamina Face")
        self.lamina_check.setChecked(True)

        self.duplicate_check = QCheckBox(u"DAG 重名")
        self.duplicate_check.setChecked(True)

        self.history_check = QCheckBox(u"遗留建模历史")
        self.history_check.setChecked(True)

        self.transform_check = QCheckBox(u"Mesh Transform 未冻结")
        self.transform_check.setChecked(True)

        self.normals_check = QCheckBox(u"锁定法线")
        self.normals_check.setChecked(True)

        self.selected_only_check = QCheckBox(u"仅检查当前选择")
        self.selected_only_check.setChecked(False)

        self.check_btn = QPushButton(u"开始检查")
        self.select_issues_btn = QPushButton(u"选择问题对象")
        self.fix_selected_btn = QPushButton(u"修复表格选中项")
        self.select_issues_btn.setEnabled(False)
        self.fix_selected_btn.setEnabled(False)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels([
            u"对象",
            u"问题类型",
            u"详情",
            u"自动修复",
        ])
        self.result_table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.result_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )
        self.result_table.setAlternatingRowColors(True)
        self.result_table.horizontalHeader().setStretchLastSection(True)

        self.status_label = QLabel(u"就绪")
        self.status_label.setAlignment(Qt.AlignCenter)

        self._create_layout()
        self._create_connections()

    def _create_layout(self):
        main_layout = QVBoxLayout(self)

        title_label = QLabel(u"Model Checker")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        main_layout.addWidget(separator)

        options_layout = QGridLayout()
        options_layout.addWidget(self.nonmanifold_check, 0, 0)
        options_layout.addWidget(self.lamina_check, 0, 1)
        options_layout.addWidget(self.duplicate_check, 1, 0)
        options_layout.addWidget(self.history_check, 1, 1)
        options_layout.addWidget(self.transform_check, 2, 0)
        options_layout.addWidget(self.normals_check, 2, 1)
        main_layout.addLayout(options_layout)
        main_layout.addWidget(self.selected_only_check)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.check_btn)
        button_layout.addWidget(self.select_issues_btn)
        button_layout.addWidget(self.fix_selected_btn)
        main_layout.addLayout(button_layout)

        main_layout.addWidget(self.result_table, 1)
        main_layout.addWidget(self.status_label)

    def _create_connections(self):
        self.check_btn.clicked.connect(self.run_check)
        self.select_issues_btn.clicked.connect(self.select_issue_nodes)
        self.fix_selected_btn.clicked.connect(self.fix_selected_issues)
        self.result_table.itemSelectionChanged.connect(
            self.update_fix_button
        )
        self.result_table.cellDoubleClicked.connect(
            self.select_table_row_node
        )

    def _scope(self):
        if not self.selected_only_check.isChecked():
            return None, None

        selections = cmds.ls(selection=True, long=True) or []
        if not selections:
            return [], []

        meshes = _mesh_shapes_from_nodes(selections)
        return selections, meshes

    def run_check(self):
        self.result_table.setRowCount(0)
        self.issues = []

        scope_nodes, scope_meshes = self._scope()

        if self.selected_only_check.isChecked() and not scope_nodes:
            self.status_label.setText(u"请先选择需要检查的模型。")
            return

        issues = []

        if self.nonmanifold_check.isChecked():
            issues.extend(check_nonmanifold_geometry(scope_meshes))

        if self.lamina_check.isChecked():
            issues.extend(check_lamina_faces(scope_meshes))

        if self.duplicate_check.isChecked():
            issues.extend(check_duplicate_names(scope_nodes))

        if self.history_check.isChecked():
            issues.extend(check_construction_history(scope_meshes))

        if self.transform_check.isChecked():
            issues.extend(check_transformations(scope_meshes))

        if self.normals_check.isChecked():
            issues.extend(check_locked_normals(scope_meshes))

        self.issues = issues
        self.result_table.setRowCount(len(issues))

        row = 0
        for issue in issues:
            self.result_table.setItem(
                row,
                0,
                QTableWidgetItem(issue["node"])
            )
            self.result_table.setItem(
                row,
                1,
                QTableWidgetItem(issue["type"])
            )
            self.result_table.setItem(
                row,
                2,
                QTableWidgetItem(issue["details"])
            )
            self.result_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    u"是" if issue.get("fixable") else u"否"
                )
            )
            row += 1

        self.result_table.resizeColumnsToContents()
        self.select_issues_btn.setEnabled(bool(issues))
        self.update_fix_button()

        if issues:
            self.status_label.setText(
                u"发现 {} 个问题。拓扑问题只报告，不自动猜测修复。".format(
                    len(issues)
                )
            )
        else:
            self.status_label.setText(u"检查通过，未发现所选检查项的问题。")

    def update_fix_button(self):
        selected_rows = self._selected_rows()
        has_fixable = False

        for row in selected_rows:
            if row < len(self.issues):
                if self.issues[row].get("fixable"):
                    has_fixable = True
                    break

        self.fix_selected_btn.setEnabled(has_fixable)

    def _selected_rows(self):
        rows = []

        for item in self.result_table.selectedItems():
            row = item.row()
            if row not in rows:
                rows.append(row)

        rows.sort()
        return rows

    def select_table_row_node(self, row, column):
        if row >= len(self.issues):
            return

        node = self.issues[row].get("node")
        if node and cmds.objExists(node):
            cmds.select(node, replace=True)

    def select_issue_nodes(self):
        nodes = []

        for issue in self.issues:
            node = issue.get("node")
            if node and cmds.objExists(node) and node not in nodes:
                nodes.append(node)

        if nodes:
            cmds.select(nodes, replace=True)
            self.status_label.setText(
                u"已选择 {} 个问题对象。".format(len(nodes))
            )

    def fix_selected_issues(self):
        selected_rows = self._selected_rows()
        if not selected_rows:
            return

        fixed_count = 0
        skipped_count = 0

        cmds.undoInfo(openChunk=True, chunkName="MuziModelCheckerFix")
        try:
            for row in selected_rows:
                if row >= len(self.issues):
                    continue

                issue = self.issues[row]

                try:
                    if fix_issue(issue):
                        fixed_count += 1
                    else:
                        skipped_count += 1
                except Exception as error:
                    skipped_count += 1
                    cmds.warning(
                        u"修复 {} 失败：{}".format(
                            issue.get("node"),
                            error
                        )
                    )
        finally:
            cmds.undoInfo(closeChunk=True)

        self.status_label.setText(
            u"自动修复 {} 项，跳过 {} 项。正在重新检查…".format(
                fixed_count,
                skipped_count
            )
        )
        self.run_check()


# 旧类名兼容。
Model_Checker_UI = ModelCheckerUI


def main():
    global _window

    try:
        if _window is not None:
            _window.close()
            _window.deleteLater()
    except Exception:
        pass

    _window = ModelCheckerUI()
    _window.setAttribute(Qt.WA_DeleteOnClose, False)
    _window.show()
    _window.raise_()
    _window.activateWindow()

    return _window


if __name__ == "__main__":
    main()
