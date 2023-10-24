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


class Constraint_Tool (QWidget) :
    """
    一个关节工具的类
    """


    def __init__ (self , parent = None) :
        super (Constraint_Tool , self).__init__ (parent)
        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        """创建需要的小部件"""
        # 吸附对象的工具
        self.match_objects_label = QLabel ("--------------吸附对象--------------")
        self.match_objects_label.setStyleSheet (u"color: rgb(255, 0, 0);")

        self.match_pos_rot_btn = QPushButton (QIcon (icon_dir + '/directions.png') ,'匹配平移和旋转')
        self.match_all_btn = QPushButton (QIcon (icon_dir + '/directions.png') ,'匹配所有变换')
        self.match_pos_btn = QPushButton (QIcon (icon_dir + '/directions.png') ,'匹配平移')
        self.match_rot_btn = QPushButton (QIcon (icon_dir + '/directions.png') ,'匹配旋转')
        self.match_scale_btn = QPushButton (QIcon (icon_dir + '/directions.png') ,'匹配缩放')
        self.match_pivot_btn = QPushButton (QIcon (icon_dir + '/directions.png') ,'匹配枢纽')

        # 创建约束的工具部件
        self.constraint_objects_label = QLabel ("--------------约束工具--------------")
        self.constraint_objects_label.setStyleSheet (u"color: rgb(255, 0, 0);")
        self.maintainOffset_checkBox = QCheckBox ('保持偏移')
        self.parent_constraint_btn = QPushButton (QIcon (':parentConstraint.png') ,'父子约束')
        self.point_constraint_btn = QPushButton (QIcon (':posConstraint.png'),'点约束')
        self.orient_constraint_btn = QPushButton (QIcon (':orientConstraint.png') ,'方向约束')
        self.scale_constraint_btn = QPushButton (QIcon (':scaleConstraint.png') ,'缩放约束')
        self.aim_constraint_btn = QPushButton (QIcon (':aimConstraint.png') ,'目标约束')
        self.pole_vector_constraint_btn = QPushButton (QIcon ('poleVectorConstraint.png') ,'极向量约束')
        self.select_constraint_btn = QPushButton (QIcon (icon_dir + '/select.png') ,'选择约束')
        self.delete_constraint_btn = QPushButton (QIcon (icon_dir + '/delete.png') ,'删除约束')

        self.constraint_btns = [self.parent_constraint_btn ,
                                self.point_constraint_btn ,
                                self.orient_constraint_btn ,
                                self.scale_constraint_btn ,
                                self.aim_constraint_btn ,
                                self.pole_vector_constraint_btn ,
                                self.select_constraint_btn ,
                                self.delete_constraint_btn ,
                                ]


    def create_layouts (self) :
        """创建需要的布局"""
        # 创建吸附对象的页面布局
        self.match_objects_layout = QVBoxLayout ()
        self.match_objects_QHlayout = QHBoxLayout ()
        self.match_objects_QHlayout.addWidget (self.match_pos_rot_btn)
        self.match_objects_QHlayout.addWidget (self.match_all_btn)
        self.match_layout = QHBoxLayout ()
        self.match_layout.addWidget (self.match_pos_btn)
        self.match_layout.addWidget (self.match_rot_btn)
        self.match_layout.addWidget (self.match_scale_btn)
        self.match_layout.addWidget (self.match_pivot_btn)
        self.match_objects_layout.addLayout (self.match_objects_QHlayout)
        self.match_objects_layout.addLayout (self.match_layout)

        # 创建约束页面的布局
        self.constraint_objects_layout = QVBoxLayout ()
        self.maintainOffset_layout = QHBoxLayout ()
        self.maintainOffset_layout.addStretch ()
        self.maintainOffset_layout.addWidget (self.maintainOffset_checkBox)
        self.maintainOffset_layout.addStretch ()
        self.constraint_layout = QGridLayout ()
        self.create_constraint_layout ()
        self.constraint_objects_layout.addLayout (self.maintainOffset_layout)
        self.constraint_objects_layout.addLayout (self.constraint_layout)

        # 创建主页面的布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addWidget (self.match_objects_label)
        self.main_layout.addLayout (self.match_objects_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget (self.constraint_objects_label)
        self.main_layout.addLayout (self.constraint_objects_layout)
        self.main_layout.addStretch ()


    def create_connections (self) :
        """连接需要的部件和对应的信号"""
        # 吸附对象部件的连接信号
        self.match_pos_rot_btn.clicked.connect (lambda : cmds.matchTransform (cmds.ls (selection = True) , pos = True ,
                                                                              rot = True , scl = False , piv = False))
        self.match_all_btn.clicked.connect (
            lambda : cmds.matchTransform (cmds.ls (selection = True) , pos = True ,
                                          rot = True , scl = True , piv = True))
        self.match_pos_btn.clicked.connect (lambda : cmds.matchTransform (cmds.ls (selection = True) , pos = True ,
                                                                          rot = False , scl = False , piv = False))
        self.match_rot_btn.clicked.connect (lambda : cmds.matchTransform (cmds.ls (selection = True) , pos = False ,
                                                                          rot = True , scl = False , piv = False))
        self.match_scale_btn.clicked.connect (lambda : cmds.matchTransform (cmds.ls (selection = True) , pos = False ,
                                                                            rot = False , scl = True , piv = False))
        self.match_pivot_btn.clicked.connect (lambda : cmds.matchTransform (cmds.ls (selection = True) , pos = False ,
                                                                            rot = False , scl = False , piv = True))


    def create_constraint_layout (self) :
        # 添加constraint_layout的按钮
        positions = [(i , j) for i in range (5) for j in range (4)]

        for position , button in zip (positions , self.constraint_btns) :
            self.constraint_layout.addWidget (button , *position)


def main () :
    return Constraint_Tool ()


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Constraint_Tool ()  # 创建实例
    window.show ()  # 显示窗口
