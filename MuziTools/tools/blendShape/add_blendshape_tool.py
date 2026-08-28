#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Maya 添加BS工具
功能：
    1. 指定 BlendShape 节点
    2. 选择模型后一键添加为 BS 目标（重名替换）
    3. 一键复制出 BS 所有目标体为独立模型
兼容：Maya 2020+ (PySide2 / PySide6)
"""

try :
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError :
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from shiboken6 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui


def get_maya_main_window () :
    """获取 Maya 主窗口"""
    ptr = omui.MQtUtil.mainWindow ()
    if ptr is not None :
        return wrapInstance (int (ptr) , QWidget)
    return None


def get_shape (transform) :
    """获取 transform 对应的 shape 节点名（完整路径）"""
    shapes = cmds.listRelatives (transform , shapes = True , fullPath = True) or []
    if shapes :
        return shapes [0]
    return None


def get_transform (shape) :
    """获取 shape 对应的 transform 节点名（完整路径）"""
    transforms = cmds.listRelatives (shape , parent = True , fullPath = True) or []
    if transforms :
        return transforms [0]
    return None


class Add_BS_Tool (QWidget) :
    """添加BS工具"""

    def __init__ (self , parent = None) :
        if parent is None :
            parent = get_maya_main_window ()
        super (Add_BS_Tool , self).__init__ (parent)

        self.setWindowTitle ("添加BS工具")
        self.setWindowFlags (Qt.Window)
        self.setMinimumWidth (320)

        self.create_widgets ()
        self.create_layouts ()
        self.create_connections ()
        self.refresh_target_list ()


    def create_widgets (self) :
        """创建 UI 部件"""
        self.bs_label = QLabel ("--------------添加BS工具--------------")
        self.bs_label.setStyleSheet (u"color: rgb(169, 255, 175);")

        self.bs_node_label = QLabel ("BS节点:")
        self.bs_node_line = QLineEdit ()
        self.bs_node_line.setPlaceholderText ("输入BlendShape节点名或点击获取")
        self.get_bs_btn = QPushButton ("获取选中")
        self.get_bs_btn.setToolTip ("从选择的模型上自动获取BlendShape节点名")

        self.target_list_label = QLabel ("当前目标:")
        self.target_list = QListWidget ()
        self.target_list.setMaximumHeight (120)
        self.target_list.setToolTip ("显示当前BS节点下已有的目标名称")

        self.add_target_btn = QPushButton ("添加 / 替换目标")
        self.add_target_btn.setToolTip ("选择模型后点击，将模型添加为BS目标（重名则替换）")

        self.copy_targets_btn = QPushButton ("复制所有目标体")
        self.copy_targets_btn.setToolTip ("将BS中所有目标体复制为独立的模型")

        self.refresh_btn = QPushButton ("刷新列表")
        self.refresh_btn.setToolTip ("刷新当前BS节点的目标列表")


    def create_layouts (self) :
        """创建布局"""
        bs_input_layout = QHBoxLayout ()
        bs_input_layout.addWidget (self.bs_node_label)
        bs_input_layout.addWidget (self.bs_node_line)
        bs_input_layout.addWidget (self.get_bs_btn)

        self.main_layout = QVBoxLayout (self)
        self.main_layout.setSpacing (8)
        self.main_layout.setContentsMargins (12 , 12 , 12 , 12)
        self.main_layout.addWidget (self.bs_label)
        self.main_layout.addLayout (bs_input_layout)
        self.main_layout.addWidget (self.target_list_label)
        self.main_layout.addWidget (self.target_list)
        self.main_layout.addWidget (self.add_target_btn)
        self.main_layout.addWidget (self.copy_targets_btn)
        self.main_layout.addWidget (self.refresh_btn)
        self.main_layout.addStretch ()


    def create_connections (self) :
        """连接信号"""
        self.get_bs_btn.clicked.connect (self.clicked_get_bs_btn)
        self.add_target_btn.clicked.connect (self.clicked_add_target_btn)
        self.copy_targets_btn.clicked.connect (self.clicked_copy_targets_btn)
        self.refresh_btn.clicked.connect (self.refresh_target_list)
        self.bs_node_line.textChanged.connect (self.refresh_target_list)


    def get_base_mesh_shape (self , bs_node) :
        """
        获取 BlendShape 节点的 base mesh shape 节点
        """
        if not cmds.objExists (bs_node) :
            return None

        # 方式1：通过 outputGeometry 找到被影响的 shape
        outputs = cmds.listConnections (bs_node + ".outputGeometry[0]") or []
        if outputs :
            return outputs [0]

        # 方式2：通过 input[0].inputGeometry 的反向连接
        inputs = cmds.listConnections (bs_node + ".input[0].inputGeometry") or []
        if inputs :
            return inputs [0]

        # 方式3：geometry 查询返回 transform，再转 shape
        geoms = cmds.blendShape (bs_node , query = True , geometry = True)
        if geoms :
            return get_shape (geoms [0])

        return None


    def get_base_mesh_transform (self , bs_node) :
        """获取 BlendShape 节点的 base mesh transform 节点"""
        shape = self.get_base_mesh_shape (bs_node)
        if shape :
            return get_transform (shape)
        return None


    def get_existing_targets (self , bs_node) :
        """获取 BlendShape 节点已有的目标名称列表"""
        if not bs_node or not cmds.objExists (bs_node) :
            return []
        aliases = cmds.aliasAttr (bs_node , query = True) or []
        return aliases [::2] if aliases else []


    def refresh_target_list (self) :
        """刷新目标列表显示"""
        self.target_list.clear ()
        bs_node = self.bs_node_line.text ()
        targets = self.get_existing_targets (bs_node)
        for t in targets :
            self.target_list.addItem (t)
        self.target_list_label.setText ("当前目标: ({})".format (len (targets)))


    def _remove_bs_target (self , bs_node , target_alias) :
        """
        从 blendShape 节点中完全删除指定名称的 target（包括 alias）
        """
        aliases = cmds.aliasAttr (bs_node , query = True) or []
        target_names = aliases [::2]
        if target_alias not in target_names :
            return False

        idx = target_names.index (target_alias)

        # 获取旧目标的 shape 连接
        geom_attr = "{}.inputTarget[0].inputTargetGroup[{}].inputTargetItem[6000].inputGeomTarget".format (
            bs_node , idx)
        conns = cmds.listConnections (geom_attr) or []

        if conns :
            old_shape = conns [0]
            try :
                # 删除目标: (baseShapeIndex, targetIndex, targetShape, weight)
                cmds.blendShape (bs_node , edit = True , remove = True ,
                                 target = (0 , idx , old_shape , 1.0))
            except Exception as e :
                print ("[删除blendShape失败] {}".format (e))

        # 删除 alias（目标名称）
        try :
            cmds.aliasAttr (bs_node + "." + target_alias , remove = True)
        except :
            pass

        return True


    def clicked_get_bs_btn (self) :
        """从选择模型获取 BS 节点名"""
        sel = cmds.ls (selection = True , long = True)
        if not sel :
            cmds.warning ("请先选择一个带有BlendShape的模型！")
            return

        for obj in sel :
            history = cmds.listHistory (obj) or []
            bs_nodes = [n for n in history if cmds.nodeType (n) == 'blendShape']
            if bs_nodes :
                self.bs_node_line.setText (bs_nodes [0])
                self.refresh_target_list ()
                print ("[获取] BS节点: {}".format (bs_nodes [0]))
                return

        cmds.warning ("所选物体上没有找到BlendShape节点！")


    def clicked_add_target_btn (self) :
        """
        添加 / 替换 BS 目标
        target 参数格式: (baseShapeIndex, targetIndex, targetShape, weight)
        targetIndex 用 -1 表示自动分配，避免索引冲突
        """
        bs_node = self.bs_node_line.text ()
        if not bs_node :
            cmds.warning ("请先输入或获取BlendShape节点名！")
            return
        if not cmds.objExists (bs_node) :
            cmds.warning ("BlendShape节点 '{}' 不存在！".format (bs_node))
            return

        sel = cmds.ls (selection = True , long = True)
        if not sel :
            cmds.warning ("请先选择要添加为目标形状的模型！")
            return

        base_shape = self.get_base_mesh_shape (bs_node)
        if not base_shape :
            cmds.warning ("无法获取BlendShape的base mesh shape！")
            return

        cmds.undoInfo (openChunk = True , chunkName = "BlendShape_AddTarget")
        try :
            for target_transform in sel :
                target_shape = get_shape (target_transform)
                if not target_shape :
                    cmds.warning ("无法获取 {} 的 shape 节点，跳过".format (target_transform))
                    continue

                target_alias = target_transform.split ('|') [-1]

                # 重名替换：删除旧目标（包括 alias）
                current_targets = self.get_existing_targets (bs_node)
                if target_alias in current_targets :
                    self._remove_bs_target (bs_node , target_alias)
                    print ("[替换] 删除旧目标: {}".format (target_alias))

                # 添加新目标
                # (baseShapeIndex=0, targetIndex=-1自动分配, targetShape, weight=1.0)
                cmds.blendShape (bs_node , edit = True ,
                                 target = (0 , -1 , target_shape , 1.0))
                print ("[添加] {} -> {}".format (target_alias , bs_node))

            self.refresh_target_list ()

        except Exception as e :
            cmds.warning (str (e))
        finally :
            cmds.undoInfo (closeChunk = True)


    def clicked_copy_targets_btn (self) :
        """复制 BS 所有目标体为独立模型"""
        bs_node = self.bs_node_line.text ()
        if not bs_node :
            cmds.warning ("请先输入或获取BlendShape节点名！")
            return
        if not cmds.objExists (bs_node) :
            cmds.warning ("BlendShape节点 '{}' 不存在！".format (bs_node))
            return

        target_names = self.get_existing_targets (bs_node)
        if not target_names :
            cmds.warning ("当前BS节点下没有目标体！")
            return

        cmds.undoInfo (openChunk = True , chunkName = "BlendShape_CopyTargets")
        copied = []
        try :
            for idx , target_name in enumerate (target_names) :
                geom_attr = "{}.inputTarget[0].inputTargetGroup[{}].inputTargetItem[6000].inputGeomTarget".format (
                    bs_node , idx)
                conns = cmds.listConnections (geom_attr) or []
                if not conns :
                    print ("[跳过] 无法获取目标 {} 的 shape 连接".format (target_name))
                    continue

                target_shape = conns [0]
                target_transform = get_transform (target_shape)
                if not target_transform :
                    print ("[跳过] 无法获取目标 {} 的 transform".format (target_name))
                    continue

                dup = cmds.duplicate (target_transform , name = target_name) [0]
                cmds.delete (dup , constructionHistory = True)

                dup_shapes = cmds.listRelatives (dup , shapes = True , fullPath = True) or []
                for s in dup_shapes :
                    if cmds.getAttr (s + ".intermediateObject") :
                        cmds.setAttr (s + ".intermediateObject" , False)

                copied.append (dup)
                print ("[复制] {}".format (dup))

            if copied :
                cmds.select (copied , replace = True)
                print ("[完成] 共复制 {} 个目标体".format (len (copied)))
            else :
                cmds.warning ("没有成功复制任何目标体！")

        except Exception as e :
            cmds.warning (str (e))
        finally :
            cmds.undoInfo (closeChunk = True)


def main () :
    """显示添加BS工具窗口"""
    global add_bs_tool_window

    try :
        add_bs_tool_window.close ()
        add_bs_tool_window.deleteLater ()
    except :
        pass

    add_bs_tool_window = Add_BS_Tool ()
    add_bs_tool_window.show ()
    add_bs_tool_window.raise_ ()
    add_bs_tool_window.activateWindow ()
    return add_bs_tool_window


if __name__ == "__main__" :
    main ()