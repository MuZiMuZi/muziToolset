import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils , qtUtils , controlUtils , hierarchyUtils
from importlib import reload
import maya.mel as mel
import maya.cmds as cmds


reload (jointUtils)
reload (pipelineUtils)


class Joint_Tool (QWidget) :
    """
    一个关节工具的类
    """


    def __init__ (self , parent = None) :
        super (Joint_Tool , self).__init__ (parent)
        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        """创建需要的小部件"""
        # 关节显示大小的部件
        self.joint_size_label = QLabel ("关节显示大小:")
        self.joint_size_line = QLineEdit ()
        self.joint_size_line.setText('0.50')
        self.joint_size_slider = QSlider (Qt.Horizontal)
        self.joint_size_slider.setSingleStep(0.10)
        self.joint_size_slider.setMinimum (0.01)
        self.joint_size_slider.setMaximum (10)
        self.joint_size_slider.setTickPosition(QSlider.TicksBelow)

        # 关节轴向的部件
        self.show_joint_axis_label = QLabel ('---------------关节轴向----------------')
        self.show_joint_axis_select_btn = QPushButton ('显示关节轴向(选择)')
        self.show_joint_axis_hierarchy_btn = QPushButton ('显示关节轴向(层级)')
        self.show_joint_axis_all_btn = QPushButton ('显示关节轴向(所有)')

        self.hide_joint_axis_select_btn = QPushButton ('隐藏关节轴向(选择)')
        self.hide_joint_axis_hierarchy_btn = QPushButton ('隐藏关节轴向(层级)')
        self.hide_joint_axis_all_btn = QPushButton ('隐藏关节轴向(所有)')

        self.joint_axis_buttons = [self.show_joint_axis_select_btn , self.show_joint_axis_hierarchy_btn ,
                                   self.show_joint_axis_all_btn , self.hide_joint_axis_select_btn ,
                                   self.hide_joint_axis_hierarchy_btn , self.hide_joint_axis_all_btn
                                   ]
        # 关节定向的部件
        self.joint_orient_btn = QPushButton ('确定关节方向')


    def create_layouts (self) :
        """创建需要的布局"""
        # 创建关节大小的布局
        self.joint_size_layout = QHBoxLayout ()
        self.joint_size_layout.addWidget (self.joint_size_label)
        self.joint_size_layout.addWidget (self.joint_size_line)
        self.joint_size_layout.addWidget (self.joint_size_slider)

        # 创建关节轴向的布局
        self.joint_axis_layout = QGridLayout ()
        self.create_joint_axis_layout ()

        # 创建关节方向的布局
        self.joint_orient_layout = QHBoxLayout ()
        self.joint_orient_layout.addWidget (self.joint_orient_btn)

        # 创建关节主页面的布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addLayout (self.joint_size_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.show_joint_axis_label)
        self.main_layout.addLayout (self.joint_axis_layout)
        self.main_layout.addStretch ()
        self.main_layout.addLayout (self.joint_orient_layout)
        self.main_layout.addStretch ()


    def create_joint_axis_layout (self) :
        # 添加按钮
        positions = [(i , j) for i in range (5) for j in range (3)]

        for position , button in zip (positions , self.joint_axis_buttons) :
            self.joint_axis_layout.addWidget (button , *position)


    def create_connections (self) :
        """连接需要的部件和对应的信号"""
        self.joint_size_line.textChanged.connect(self.set_joint_size)
        self.joint_size_slider.valueChanged.connect(self.set_joint_size_line)
        self.show_joint_axis_select_btn.clicked.connect (lambda : jointUtils.Joint.show_joint_axis_select ())
        self.show_joint_axis_hierarchy_btn.clicked.connect (lambda : jointUtils.Joint.show_joint_axis_hirerarchy ())
        self.show_joint_axis_all_btn.clicked.connect (lambda : jointUtils.Joint.show_joint_axis_all ())

        self.hide_joint_axis_select_btn.clicked.connect(lambda : jointUtils.Joint.hide_joint_axis_select ())
        self.hide_joint_axis_hierarchy_btn.clicked.connect (lambda : jointUtils.Joint.hide_joint_axis_hirerarchy ())
        self.hide_joint_axis_all_btn.clicked.connect (lambda : jointUtils.Joint.hide_joint_axis_all ())

        self.joint_orient_btn.clicked.connect(lambda :mel.eval("OrientJointOptions;"))
    def set_joint_size_line(self):
        joint_size_value = float(self.joint_size_slider.value())
        self.joint_size_line.setText(str(joint_size_value))

    def set_joint_size(self):
        joint_size_value = float(self.joint_size_line.text())
        self.joint_size_slider.setValue(joint_size_value)
        jointUtils.Joint.set_jointSize(joint_size_value)


def show () :
    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Joint_Tool ()  # 创建实例
    window.show ()  # 显示窗口


def main () :
    return Joint_Tool ()


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Joint_Tool ()  # 创建实例
    window.show ()  # 显示窗口
