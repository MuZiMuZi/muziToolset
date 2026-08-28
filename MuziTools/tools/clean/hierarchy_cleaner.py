#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
层级清理器
功能：清理场景中的空组、冻结变换、删除历史、解锁属性等
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
#  清理功能函数
# =============================================================================
def delete_empty_groups():
    """
    递归删除场景中的所有空组
    空组定义：没有子对象、没有形状节点、不是骨骼
    """
    all_transforms = cmds.ls(type="transform", long=True)
    empty_groups = []

    for tr in all_transforms:
        # 跳过默认相机
        short_name = tr.split("|")[-1]
        if short_name in ["front", "persp", "side", "top"]:
            continue

        children = cmds.listRelatives(tr, children=True, fullPath=True) or []
        shapes = cmds.listRelatives(tr, shapes=True, fullPath=True) or []

        # 无子对象且无形状节点，且不是关节
        if not children and not shapes:
            if cmds.objectType(tr) != "joint":
                empty_groups.append(tr)

    # 从深层级向上删除，避免破坏父级结构
    empty_groups.sort(key=lambda x: x.count("|"), reverse=True)

    deleted_count = 0
    for grp in empty_groups:
        try:
            if cmds.objExists(grp):
                cmds.delete(grp)
                deleted_count += 1
        except Exception as e:
            cmds.warning(f"无法删除空组 {grp}: {str(e)}")

    return deleted_count


def delete_history(nodes=None):
    """
    删除构造历史
    参数：nodes - 要处理的 transform 节点列表，None 则处理所有几何体
    """
    if nodes is None:
        nodes = cmds.ls(type="transform", long=True)

    deleted_count = 0
    for node in nodes:
        short_name = node.split("|")[-1]
        if short_name in ["front", "persp", "side", "top"]:
            continue
        try:
            if cmds.objExists(node):
                shapes = cmds.listRelatives(node, shapes=True, fullPath=True) or []
                if shapes:
                    cmds.delete(node, constructionHistory=True)
                    deleted_count += 1
        except Exception as e:
            cmds.warning(f"无法删除历史 {node}: {str(e)}")

    return deleted_count


def freeze_transformations(nodes=None):
    """
    冻结变换
    参数：nodes - 要处理的节点列表，None 则处理所有 transform
    """
    if nodes is None:
        nodes = cmds.ls(type="transform", long=True)

    frozen_count = 0
    for node in nodes:
        short_name = node.split("|")[-1]
        if short_name in ["front", "persp", "side", "top"]:
            continue
        try:
            if cmds.objExists(node):
                cmds.makeIdentity(node, apply=True, t=1, r=1, s=1, n=0, pn=1)
                frozen_count += 1
        except Exception as e:
            cmds.warning(f"无法冻结变换 {node}: {str(e)}")

    return frozen_count


def unlock_and_show_attributes(nodes=None):
    """
    解锁并显示所有关键属性
    """
    if nodes is None:
        nodes = cmds.ls(type="transform", long=True)

    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
    unlocked_count = 0

    for node in nodes:
        for attr in attrs:
            full_attr = f"{node}.{attr}"
            try:
                if cmds.attributeQuery(attr, node=node, exists=True):
                    cmds.setAttr(full_attr, lock=False)
                    cmds.setAttr(full_attr, keyable=True)
                    unlocked_count += 1
            except:
                pass

    return unlocked_count


def center_pivot(nodes=None):
    """
    将轴心点归零到对象中心
    """
    if nodes is None:
        nodes = cmds.ls(type="transform", long=True)

    centered_count = 0
    for node in nodes:
        short_name = node.split("|")[-1]
        if short_name in ["front", "persp", "side", "top"]:
            continue
        try:
            if cmds.objExists(node):
                cmds.xform(node, cp=True)
                centered_count += 1
        except:
            pass

    return centered_count


def delete_unknown_nodes():
    """删除未知节点"""
    unknown = cmds.ls(type="unknown")
    if unknown:
        try:
            cmds.delete(unknown)
            return len(unknown)
        except:
            return 0
    return 0


# =============================================================================
#  UI 类
# =============================================================================
class Hierarchy_Cleaner_UI(QDialog):
    """
    层级清理器界面
    """

    def __init__(self, parent=None):
        if parent is None:
            parent = get_maya_main_window()
        super(Hierarchy_Cleaner_UI, self).__init__(parent)

        self.setWindowTitle("层级清理器")
        self.setMinimumWidth(300)
        self.setMinimumHeight(400)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """创建 UI 部件"""
        self.title_label = QLabel("层级清理器")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: rgb(169, 255, 175);")
        self.title_label.setAlignment(Qt.AlignCenter)

        # 清理选项
        self.chk_delete_empty = QCheckBox("删除空组")
        self.chk_delete_empty.setChecked(True)

        self.chk_delete_history = QCheckBox("删除构造历史 (Delete History)")
        self.chk_delete_history.setChecked(True)

        self.chk_freeze = QCheckBox("冻结变换 (Freeze Transform)")
        self.chk_freeze.setChecked(True)

        self.chk_unlock = QCheckBox("解锁并显示属性")
        self.chk_unlock.setChecked(True)

        self.chk_center_pivot = QCheckBox("轴心点居中 (Center Pivot)")
        self.chk_center_pivot.setChecked(True)  # <-- 默认勾选

        self.chk_delete_unknown = QCheckBox("删除未知节点")
        self.chk_delete_unknown.setChecked(True)

        # 仅对选中对象操作
        self.chk_selected_only = QCheckBox("仅对选中对象操作")
        self.chk_selected_only.setChecked(False)

        # 执行按钮
        self.btn_execute = QPushButton("执行清理")
        self.btn_execute.setMinimumHeight(36)
        self.btn_execute.setStyleSheet("""
            QPushButton {
                background-color: rgb(60, 120, 80);
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgb(80, 160, 100);
            }
        """)

        # 结果标签
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)

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

        # 选项区域
        options_layout = QVBoxLayout()
        options_layout.setSpacing(6)
        options_layout.addWidget(self.chk_delete_empty)
        options_layout.addWidget(self.chk_delete_history)
        options_layout.addWidget(self.chk_freeze)
        options_layout.addWidget(self.chk_unlock)
        options_layout.addWidget(self.chk_center_pivot)
        options_layout.addWidget(self.chk_delete_unknown)

        main_layout.addLayout(options_layout)
        main_layout.addWidget(self.chk_selected_only)
        main_layout.addStretch()
        main_layout.addWidget(self.btn_execute)
        main_layout.addWidget(self.result_label)

    def create_connections(self):
        """连接信号"""
        self.btn_execute.clicked.connect(self.on_execute)

    def on_execute(self):
        """执行清理"""
        # 获取目标节点
        if self.chk_selected_only.isChecked():
            nodes = cmds.ls(selection=True, long=True)
            if not nodes:
                self.result_label.setText("<span style='color: rgb(255, 100, 100);'>请先选择对象</span>")
                return
        else:
            nodes = None

        results = []

        # 按合理顺序执行
        if self.chk_delete_empty.isChecked():
            count = delete_empty_groups()
            if count > 0:
                results.append(f"删除空组: {count} 个")

        if self.chk_delete_history.isChecked():
            count = delete_history(nodes)
            if count > 0:
                results.append(f"删除历史: {count} 个")

        if self.chk_freeze.isChecked():
            count = freeze_transformations(nodes)
            if count > 0:
                results.append(f"冻结变换: {count} 个")

        if self.chk_unlock.isChecked():
            count = unlock_and_show_attributes(nodes)
            if count > 0:
                results.append(f"解锁属性: {count} 项")

        if self.chk_center_pivot.isChecked():
            count = center_pivot(nodes)
            if count > 0:
                results.append(f"轴心居中: {count} 个")

        if self.chk_delete_unknown.isChecked():
            count = delete_unknown_nodes()
            if count > 0:
                results.append(f"删除未知节点: {count} 个")

        # 显示结果
        if results:
            result_text = "<br>".join(results)
            self.result_label.setText(f"<span style='color: rgb(169, 255, 175);'>{result_text}</span>")
        else:
            self.result_label.setText("<span style='color: rgb(200, 200, 200);'>无需清理或已清理完成</span>")


def main():
    """显示层级清理器窗口"""
    global hierarchy_cleaner_window

    try:
        hierarchy_cleaner_window.close()
        hierarchy_cleaner_window.deleteLater()
    except:
        pass

    hierarchy_cleaner_window = Hierarchy_Cleaner_UI()
    hierarchy_cleaner_window.show()
    hierarchy_cleaner_window.raise_()
    hierarchy_cleaner_window.activateWindow()
    return hierarchy_cleaner_window