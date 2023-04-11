# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals, print_function

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtWidgets import *
    from PySide import __version__
    from shiboken import wrapInstance

import os
import pymel.core as pm
import maya.cmds as cmds
import muziToolset.res.ui.backGround as backGround

import muziToolset.core.controlUtils as controlUtils

reload(controlUtils)

class ShapeWidget(QListWidget):
    def __init__(self):
        QListWidget.__init__(self)
        self.init_ui()

    def init_ui(self):
        self.update_shapes()
        # 设置无法拖拽模式
        self.setMovement(self.Static)
        #设置选择模式
        self.setSelectionMode(self.ExtendedSelection)

        # 创建控制器形状页面布局
        self.setViewMode(self.IconMode)
        self.setIconSize(QSize(100,100))
        self.setResizeMode(self.Adjust)

        self.itemClicked.connect(self.clicked)

        # 创建控制器形状右键页面布局
        self.menu = QMenu(self)
        self.menu.addAction('上传控制器',self.update_control)
        self.menu.addAction('删除控制器',self.delete_control)

    def contextMenuEvent(self, event):
        QListWidget.contextMenuEvent(self,event)
        self.menu.exec_(event.globalPos())

    def update_shapes(self):
        # 删除视图里的所有项目和选择
        self.clear()
        # 找到图片放置的路径并导入选择框中
        data_dir = os.path.abspath(__file__ + "/../../../image")
        for file_name in os.listdir(data_dir):
            name,ext = os.path.splitext(file_name)
            if ext != '.jpg':
                continue
            jpg_file = os.path.join(data_dir,file_name)
            # QIcon可以从给定的像素图集中生成更小、更大、活动和禁用的像素图。Qt 小部件使用此类像素图来显示代表特定操作的图标
            icon = QIcon(jpg_file)
            QListWidgetItem(icon,name,self)

    @staticmethod
    def clicked(item):
        pm.undoInfo(openChunk = 1)
        s = item.text()
        selected = controlUtils.Control.selected()
        if selected:
            controlUtils.Control.set_selected(s=s, r = controlUtils.Control.get_soft_radius())
        else:
            controlUtils.Control(n=s, s=s, r= controlUtils.Control.get_soft_radius())
        pm.undoInfo(closeChunk = 1)
    def update_control(self):
        pm.undoInfo(openChunk=1)
        for control in controlUtils.Control.selected():
            control.upload()
        self.update_shapes()
        pm.undoInfo(closeChunk=1)

    def delete_control(self):
        pm.undoInfo(openChunk=1)
        shapes = []
        for item in self.selectedItems():
            shapes.append(item.text())
        controlUtils.Control.delete_shapes(*shapes)
        self.update_shapes()
        pm.undoInfo(closeChunk=1)

class ColorWidget(QListWidget):
    def __init__(self):
        QListWidget.__init__(self)
        self.init_ui()

    def init_ui(self):
        # 设置无法拖拽模式
        self.setMovement(self.Static)
        self.resize(500, 500)
        # 创建控制器颜色页面布局
        self.setViewMode(self.IconMode)
        self.setIconSize(QSize(100,100))
        self.setResizeMode(self.Adjust)


        # 预设颜色画布的数值
        index_rgb_map = [
            [0.5, 0.5, 0.5],
            [0, 0, 0],
            [0.247, 0.247, 0.247],
            [0.498, 0.498, 0.498],
            [0.608, 0, 0.157],
            [0, 0.16, 0.376],
            [0, 0, 1],
            [0, 0.275, 0.094],
            [0.149, 0, 0.263],
            [0.78, 0, 0.78],
            [0.537, 0.278, 0.2],
            [0.243, 0.133, 0.121],
            [0.6, 0.145, 0],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0.2549, 0.6],
            [1, 1, 1],
            [1, 1, 0],
            [0.388, 0.863, 1],
            [0.263, 1, 0.639],
            [1, 0.686, 0.686],
            [0.89, 0.674, 0.474],
            [1, 1, 0.388],
            [0, 0.6, 0.329],
            [0.627, 0.411, 0.188],
            [0.619, 0.627, 0.188],
            [0.408, 0.631, 0.188],
            [0.188, 0.631, 0.365],
            [0.188, 0.627, 0.627],
            [0.188, 0.403, 0.627],
            [0.434, 0.188, 0.627],
            [0.627, 0.188, 0.411],
        ]
        # 添加颜色画布
        for i,rgb in enumerate(index_rgb_map):
            pix = QPixmap(70,70)
            pix.fill(QColor.fromRgbF(*rgb))
            item = QListWidgetItem(QIcon(pix),'',self)
            item.setSizeHint(QSize(72,72))

        # 连接信号
        self.itemClicked.connect(self.clicked)

    def clicked(self,item):
        pm.undoInfo(openChunk=1)
        index = self.indexFromItem(item)
        c = index.row()
        controlUtils.Control.set_selected(c = c)
        pm.undoInfo(closeChunk=1)

class ControlsWidget(QWidget):
    def __init__(self,parent = None):
        super(ControlsWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建控制器主页面布局
        self.main_layout  = QVBoxLayout(self)
        self.setWindowTitle(u'控制器工具')

        # 创建控制器形状页面和颜色页面布局
        self.shape_layout = ShapeWidget()
        self.color_layout = ColorWidget()

        # 创建旋转控制器按钮页面布局
        self.rotate_layout = QHBoxLayout(self)
        self.rotate_layout.addWidget(QLabel("旋转角度"))

        #创建旋转角度的输入框
        self.rotate_text = QLineEdit()

        self.rotate_button_layout = QHBoxLayout(self)
        self.rotate_rx_cb = QCheckBox("旋转x轴")

        self.rotate_ry_cb =QCheckBox("旋转y轴")
        self.rotate_rz_cb = QCheckBox("旋转z轴")

        self.rotate_button = QPushButton("旋转")
        self.rotate_button.clicked.connect(self.rotate_control)

        # 添加旋转控制器页面布局的小部件
        self.rotate_layout.addWidget(self.rotate_text)
        self.rotate_button_layout.addWidget(self.rotate_rx_cb)
        self.rotate_button_layout.addWidget(self.rotate_ry_cb)
        self.rotate_button_layout.addWidget(self.rotate_rz_cb)

        self.rotate_layout.addLayout(self.rotate_button_layout)
        self.rotate_layout.addWidget(self.rotate_button)


        # 创建控制器按钮页面布局
        self.button_layout = QHBoxLayout(self)
        self.scale_button = QPushButton("缩放(按B键调整大小)")
        self.scale_button.clicked.connect(self.scale_control)

        self.mirror_button = QPushButton("镜像")
        self.mirror_button.clicked.connect(self.mirror_control)

        self.replace_button = QPushButton("替换")
        self.replace_button.clicked.connect(self.replace_control)

        # 添加控制器按钮页面布局的小部件
        self.button_layout.addWidget(self.scale_button)
        self.button_layout.addWidget(self.mirror_button)
        self.button_layout.addWidget(self.replace_button)


        # 添加主页面布局的小部件
        self.main_layout.addWidget(self.shape_layout)
        self.main_layout.addWidget(self.color_layout)
        self.main_layout.addWidget(QLabel("-------旋转控制器形状------"))
        self.main_layout.addLayout(self.rotate_layout)
        self.main_layout.addLayout(self.button_layout)

    @staticmethod
    def scale_control():
        controlUtils.Control.set_selected(r = controlUtils.Control.get_soft_radius())

    @staticmethod
    def mirror_control():
        controlUtils.Control.mirror_selected()

    @staticmethod
    def replace_control():
        pm.undoInfo(openChunk=1)
        selected = controlUtils.Control.selected()
        target = selected.pop()
        shape = target.get_shape()
        for control in selected:
            control.set_shape(shape)
        pm.undoInfo(closeChunk=1)

    def rotate_control(self):
        pm.undoInfo(openChunk=1)
        selected = controlUtils.Control.selected()
        ro = self.rotate_text.text()
        for control in selected:
            if self.rotate_rx_cb.isChecked():
                    control.set_rotateX(rx = ro)
            elif self.rotate_ry_cb.isChecked():
                    control.set_rotateY(ry = ro)
            elif self.rotate_rz_cb.isChecked():
                    control.set_rotateZ(rz =ro)
        pm.undoInfo(closeChunk=1)

window = None

def show():
    global window
    if window is None:
        window = ControlsWidget()
    window.show()
