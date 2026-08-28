#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模型检查工具
功能：检查模型中的常见问题，如非流形几何体、薄片面、重名、法线方向等
分类：clean
"""

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui


def get_maya_main_window():
    """获取 Maya 主窗口，作为工具箱的父窗口"""
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), QWidget)
    return None


# =============================================================================
#  检查功能函数
# =============================================================================
def check_nonmanifold_geometry(meshes=None):
    """
    检查非流形几何体
    返回：问题列表 [{"mesh": "名称", "type": "非流形几何体", "details": "..."}]
    """
    if meshes is None:
        meshes = cmds.ls(type="mesh", long=True)
    else:
        meshes = [meshes] if isinstance(meshes, str) else meshes

    issues = []
    for m in meshes:
        if not cmds.objExists(m):
            continue
        try:
            nonmanifold_verts = cmds.polyInfo(m, nonManifoldVertices=True) or []
            nonmanifold_edges = cmds.polyInfo(m, nonManifoldEdges=True) or []
            if nonmanifold_verts or nonmanifold_edges:
                transform = cmds.listRelatives(m, parent=True, fullPath=True)[0]
                issues.append({
                    "mesh": transform,
                    "type": "非流形几何体",
                    "details": f"顶点:{len(nonmanifold_verts)} 边:{len(nonmanifold_edges)}"
                })
        except:
            pass
    return issues


def check_lamina_faces(meshes=None):
    """
    检查薄片面（lamina faces）
    """
    if meshes is None:
        meshes = cmds.ls(type="mesh", long=True)
    else:
        meshes = [meshes] if isinstance(meshes, str) else meshes

    issues = []
    for m in meshes:
        if not cmds.objExists(m):
            continue
        try:
            lamina = cmds.polyInfo(m, laminaFaces=True) or []
            if lamina:
                transform = cmds.listRelatives(m, parent=True, fullPath=True)[0]
                issues.append({
                    "mesh": transform,
                    "type": "薄片面",
                    "details": f"数量: {len(lamina)}"
                })
        except:
            pass
    return issues


def check_duplicate_names():
    """
    检查重名节点（短名称相同但长路径不同）
    """
    all_nodes = cmds.ls(dag=True, long=True)
    name_map = {}

    for node in all_nodes:
        short_name = node.split("|")[-1]
        if short_name in name_map:
            name_map[short_name].append(node)
        else:
            name_map[short_name] = [node]

    issues = []
    for short_name, nodes in name_map.items():
        if len(nodes) > 1 and short_name not in ["front", "persp", "side", "top"]:
            issues.append({
                "mesh": short_name,
                "type": "重名",
                "details": f"出现 {len(nodes)} 次"
            })
    return issues


def check_construction_history(meshes=None):
    """
    检查是否有遗留的构造历史
    """
    if meshes is None:
        meshes = cmds.ls(type="mesh", long=True)
    else:
        meshes = [meshes] if isinstance(meshes, str) else meshes

    issues = []
    for m in meshes:
        if not cmds.objExists(m):
            continue
        try:
            history = cmds.listHistory(m) or []
            # 过滤掉 shape 和 transform 本身
            real_history = [h for h in history if cmds.nodeType(h) not in ["mesh", "transform"]]
            if real_history:
                transform = cmds.listRelatives(m, parent=True, fullPath=True)[0]
                issues.append({
                    "mesh": transform,
                    "type": "遗留构造历史",
                    "details": f"{len(real_history)} 个历史节点"
                })
        except:
            pass
    return issues


def check_transformations(nodes=None):
    """
    检查变换是否归零（T/R 不为零，S 不为1）
    """
    if nodes is None:
        nodes = cmds.ls(type="transform", long=True)

    issues = []
    for node in nodes:
        short_name = node.split("|")[-1]
        if short_name in ["front", "persp", "side", "top"]:
            continue
        try:
            t = cmds.getAttr(f"{node}.translate")[0]
            r = cmds.getAttr(f"{node}.rotate")[0]
            s = cmds.getAttr(f"{node}.scale")[0]

            if (any(abs(v) > 0.001 for v in t) or
                any(abs(v) > 0.001 for v in r) or
                any(abs(v - 1.0) > 0.001 for v in s)):
                issues.append({
                    "mesh": node,
                    "type": "变换未归零",
                    "details": f"T:{[round(x,3) for x in t]} R:{[round(x,3) for x in r]} S:{[round(x,3) for x in s]}"
                })
        except:
            pass
    return issues


def check_locked_normals(meshes=None):
    """
    检查法线是否被锁定
    """
    if meshes is None:
        meshes = cmds.ls(type="mesh", long=True)
    else:
        meshes = [meshes] if isinstance(meshes, str) else meshes

    issues = []
    for m in meshes:
        if not cmds.objExists(m):
            continue
        try:
            # 检查是否有锁定的法线
            vertices = cmds.ls(f"{m}.vtx[*]", flatten=True)
            locked_count = 0
            for vtx in vertices[:100]:  # 采样检查，避免太慢
                locked = cmds.polyNormalPerVertex(vtx, query=True, freezeNormal=True)
                if locked and locked[0]:
                    locked_count += 1
            if locked_count > 0:
                transform = cmds.listRelatives(m, parent=True, fullPath=True)[0]
                issues.append({
                    "mesh": transform,
                    "type": "法线被锁定",
                    "details": f"约 {locked_count} 个顶点法线锁定"
                })
        except:
            pass
    return issues


# =============================================================================
#  UI 类
# =============================================================================
class Model_Checker_UI(QDialog):
    """
    模型检查工具界面
    """

    def __init__(self, parent=None):
        if parent is None:
            parent = get_maya_main_window()
        super(Model_Checker_UI, self).__init__(parent)

        self.setWindowTitle("模型检查工具")
        self.setMinimumWidth(460)
        self.setMinimumHeight(520)

        self.issues = []

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """创建 UI 部件"""
        self.title_label = QLabel("模型检查工具")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: rgb(169, 255, 175);")
        self.title_label.setAlignment(Qt.AlignCenter)

        # 检查选项
        self.chk_nonmanifold = QCheckBox("非流形几何体")
        self.chk_nonmanifold.setChecked(True)

        self.chk_lamina = QCheckBox("薄片面 (Lamina)")
        self.chk_lamina.setChecked(True)

        self.chk_duplicate = QCheckBox("重名节点")
        self.chk_duplicate.setChecked(True)

        self.chk_history = QCheckBox("遗留构造历史")
        self.chk_history.setChecked(True)

        self.chk_transform = QCheckBox("变换未归零")
        self.chk_transform.setChecked(True)

        self.chk_normals = QCheckBox("法线被锁定")
        self.chk_normals.setChecked(True)

        # 仅检查选中
        self.chk_selected_only = QCheckBox("仅检查选中对象")
        self.chk_selected_only.setChecked(False)

        # 按钮
        self.btn_check = QPushButton("开始检查")
        self.btn_check.setMinimumHeight(36)
        self.btn_check.setStyleSheet("""
            QPushButton {
                background-color: rgb(60, 100, 140);
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgb(80, 140, 180);
            }
        """)

        self.btn_select_issues = QPushButton("选中问题对象")
        self.btn_select_issues.setEnabled(False)

        self.btn_fix_selected = QPushButton("修复选中项")
        self.btn_fix_selected.setEnabled(False)

        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["对象", "问题类型", "详情"])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.result_table.setAlternatingRowColors(True)

        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)

    def create_layouts(self):
        """组装布局"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        main_layout.addWidget(self.title_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: rgb(100, 100, 100);")
        main_layout.addWidget(line)

        # 选项网格
        options_layout = QGridLayout()
        options_layout.setSpacing(6)
        options_layout.addWidget(self.chk_nonmanifold, 0, 0)
        options_layout.addWidget(self.chk_lamina, 0, 1)
        options_layout.addWidget(self.chk_duplicate, 1, 0)
        options_layout.addWidget(self.chk_history, 1, 1)
        options_layout.addWidget(self.chk_transform, 2, 0)
        options_layout.addWidget(self.chk_normals, 2, 1)
        main_layout.addLayout(options_layout)

        main_layout.addWidget(self.chk_selected_only)

        # 按钮行
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_check)
        btn_layout.addWidget(self.btn_select_issues)
        btn_layout.addWidget(self.btn_fix_selected)
        main_layout.addLayout(btn_layout)

        main_layout.addWidget(self.result_table)
        main_layout.addWidget(self.status_label)

    def create_connections(self):
        """连接信号"""
        self.btn_check.clicked.connect(self.on_check)
        self.btn_select_issues.clicked.connect(self.on_select_issues)
        self.btn_fix_selected.clicked.connect(self.on_fix_selected)
        self.result_table.itemSelectionChanged.connect(self.on_selection_changed)

    def on_check(self):
        """执行检查"""
        self.result_table.setRowCount(0)
        self.issues = []

        # 获取目标
        if self.chk_selected_only.isChecked():
            selected = cmds.ls(selection=True, long=True)
            if not selected:
                self.status_label.setText("<span style='color: rgb(255, 100, 100);'>请先选择对象</span>")
                return

            meshes = []
            transforms = selected
            for s in selected:
                shapes = cmds.listRelatives(s, shapes=True, fullPath=True) or []
                meshes.extend([sh for sh in shapes if cmds.nodeType(sh) == "mesh"])
        else:
            meshes = None
            transforms = None

        all_issues = []

        if self.chk_nonmanifold.isChecked():
            all_issues.extend(check_nonmanifold_geometry(meshes))

        if self.chk_lamina.isChecked():
            all_issues.extend(check_lamina_faces(meshes))

        if self.chk_duplicate.isChecked():
            all_issues.extend(check_duplicate_names())

        if self.chk_history.isChecked():
            all_issues.extend(check_construction_history(meshes))

        if self.chk_transform.isChecked():
            all_issues.extend(check_transformations(transforms))

        if self.chk_normals.isChecked():
            all_issues.extend(check_locked_normals(meshes))

        # 填充表格
        self.result_table.setRowCount(len(all_issues))
        for i, issue in enumerate(all_issues):
            self.result_table.setItem(i, 0, QTableWidgetItem(issue["mesh"]))
            self.result_table.setItem(i, 1, QTableWidgetItem(issue["type"]))
            self.result_table.setItem(i, 2, QTableWidgetItem(issue["details"]))

        self.issues = all_issues

        if all_issues:
            self.status_label.setText(
                f"<span style='color: rgb(255, 150, 100);'>发现 {len(all_issues)} 个问题</span>"
            )
            self.btn_select_issues.setEnabled(True)
        else:
            self.status_label.setText(
                "<span style='color: rgb(169, 255, 175);'>检查通过，未发现明显问题</span>"
            )
            self.btn_select_issues.setEnabled(False)
            self.btn_fix_selected.setEnabled(False)

        self.result_table.resizeColumnsToContents()

    def on_selection_changed(self):
        """表格选择变化"""
        has_selection = len(self.result_table.selectedItems()) > 0
        self.btn_fix_selected.setEnabled(has_selection)

    def on_select_issues(self):
        """选中所有问题对象"""
        if not self.issues:
            return

        objects = list(set([issue["mesh"] for issue in self.issues]))
        try:
            cmds.select(objects, replace=True)
            self.status_label.setText(f"已选中 {len(objects)} 个问题对象")
        except Exception as e:
            cmds.warning(f"选择失败: {str(e)}")

    def on_fix_selected(self):
        """修复选中的问题"""
        selected_rows = set()
        for item in self.result_table.selectedItems():
            selected_rows.add(item.row())

        fixed_count = 0
        for row in selected_rows:
            if row >= len(self.issues):
                continue

            issue = self.issues[row]
            mesh = issue["mesh"]
            issue_type = issue["type"]

            try:
                if issue_type == "遗留构造历史":
                    cmds.delete(mesh, constructionHistory=True)
                    fixed_count += 1
                elif issue_type == "变换未归零":
                    cmds.makeIdentity(mesh, apply=True, t=1, r=1, s=1, n=0, pn=1)
                    fixed_count += 1
                elif issue_type == "法线被锁定":
                    cmds.polyNormalPerVertex(mesh, unFreezeNormal=True)
                    fixed_count += 1
                elif issue_type == "薄片面":
                    cmds.delete(mesh, constructionHistory=True)
                    cmds.polyClean(mesh, lamina=True)
                    fixed_count += 1
            except Exception as e:
                cmds.warning(f"修复 {mesh} 失败: {str(e)}")

        if fixed_count > 0:
            self.status_label.setText(
                f"<span style='color: rgb(169, 255, 175);'>已修复 {fixed_count} 项，请重新检查</span>"
            )
            self.on_check()
        else:
            self.status_label.setText("选中项无法自动修复或无需修复")


def main():
    """显示模型检查工具窗口"""
    global model_checker_window

    try:
        model_checker_window.close()
        model_checker_window.deleteLater()
    except:
        pass

    model_checker_window = Model_Checker_UI()
    model_checker_window.show()
    model_checker_window.raise_()
    model_checker_window.activateWindow()
    return model_checker_window