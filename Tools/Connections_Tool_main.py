import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils , qtUtils , controlUtils , snapUtils , connectionUtils
from importlib import reload

import maya.cmds as cmds


class Connections_Tool (QWidget) :
    """
这是一个用来写属性连接工具的类
"""


    def __init__ (self , parent = None) :
        super (Connections_Tool , self).__init__ (parent)
        self.win_name = 'Connections_Tool'
        self.win_title = 'Connections_Tool(连接工具)'
        self.create_widgets ()
        self.create_layouts ()
        self.add_connnect ()


    def create_widgets (self) :
        """
        创建连接的部件
        """
        #创建默认属性连接的部件
        self.connect_default_connection_label = QLabel('---------------连接默认属性连接---------------')
        self.connect_default_connection_label.setStyleSheet (u"color: rgb(169, 255, 175);")
        self.translate_attr_cheekbox = QCheckBox('Translate')
        self.rotate_attr_cheekbox = QCheckBox ('Rotate')
        self.scale_attr_cheekbox = QCheckBox ('Scale')
        self.matrix_attr_cheekbox = QCheckBox ('Matrix')
        self.reset_attr_btn = QPushButton(QIcon (icon_dir + '/reset.png') ,'Reset(重置)')

        self.connect_default_connection_btn = QPushButton(QIcon(icon_dir + '/connect.png'),'create_connection(创建连接)')
        self.delete_default_connection_btn = QPushButton (QIcon (icon_dir + '/disconnect.png') ,'delete_connection(删除连接)')

        #创建自定义属性连接的部件
        self.connect_custom_connection_label = QLabel ('---------------连接自定义属性连接---------------')
        self.connect_custom_connection_label.setStyleSheet (u"color: rgb(85, 255, 255);")
        self.driver_attr_label = QLabel('Driver(驱动者):---')
        self.driver_attr_line = QLineEdit()
        self.pick_driver_attr_btn = QPushButton(QIcon (icon_dir + '/select.png') ,'pick(拾取)')

        self.driven_attr_label = QLabel ('Driven(被驱动者):')
        self.driven_attr_line = QLineEdit ()
        self.pick_driven_attr_btn = QPushButton (QIcon (icon_dir + '/select.png') ,'pick(拾取)')

        self.connect_custom_connection_btn = QPushButton (QIcon (icon_dir + '/connect.png') ,'create_connection(创建连接)')
        self.delete_custom_connection_btn = QPushButton (QIcon (icon_dir + '/disconnect.png') ,'delete_connection(删除连接)')

        
        #创建复制属性连接的部件
        self.copy_delete_connection_label = QLabel ('---------------复制/删除属性连接---------------')
        self.copy_delete_connection_label.setStyleSheet (u"color: rgb(170, 255, 128);")
        self.copy_connection_btn = QPushButton (QIcon (icon_dir + '/copy.png') ,'copy_Driven_connection(复制连接)')
        self.delete_connection_btn = QPushButton (QIcon (icon_dir + '/delete.png') ,'delete_Driven_connection(删除连接)')


    def create_layouts (self) :
        ##创建默认属性连接的的布局
        self.connect_default_connection_layout = QVBoxLayout()
        #创建默认属性的布局
        self.default_attr_layout = QHBoxLayout()
        self.default_attr_layout.addWidget(self.translate_attr_cheekbox)
        self.default_attr_layout.addWidget (self.rotate_attr_cheekbox)
        self.default_attr_layout.addWidget (self.scale_attr_cheekbox)
        self.default_attr_layout.addWidget (self.matrix_attr_cheekbox)
        self.default_attr_layout.addWidget(self.reset_attr_btn)

        #创建操作默认属性链接的布局
        self.operate_default_connection_layout = QHBoxLayout ()
        self.operate_default_connection_layout.addWidget(self.connect_default_connection_btn)
        self.operate_default_connection_layout.addWidget (self.delete_default_connection_btn)

        #将default_attr_layout和operate_default_connection_layout，添加到connect_default_connection_layout里
        self.connect_default_connection_layout.addLayout(self.default_attr_layout)
        self.connect_default_connection_layout.addLayout (self.operate_default_connection_layout)

        ##创建自定义属性连接的布局
        self.connect_custom_connection_layout = QVBoxLayout()

        #创建驱动者的属性连接布局
        self.driver_attr_layout = QHBoxLayout()
        self.driver_attr_layout.addWidget(self.driver_attr_label)
        self.driver_attr_layout.addWidget (self.driver_attr_line)
        self.driver_attr_layout.addWidget (self.pick_driver_attr_btn)

        # 创建驱动者的属性连接布局
        self.driven_attr_layout = QHBoxLayout ()
        self.driven_attr_layout.addWidget (self.driven_attr_label)
        self.driven_attr_layout.addWidget (self.driven_attr_line)
        self.driven_attr_layout.addWidget (self.pick_driven_attr_btn)

        #创建操作自定义属性连接按钮的布局
        self.operate_custom_connection_layout = QHBoxLayout()
        self.operate_custom_connection_layout.addWidget(self.connect_custom_connection_btn)
        self.operate_custom_connection_layout.addWidget (self.delete_custom_connection_btn)

        #将驱动者的属性布局和被驱动者的属性布局添加到自定义属性连接布局
        self.connect_custom_connection_layout.addLayout(self.driver_attr_layout)
        self.connect_custom_connection_layout.addLayout(self.driven_attr_layout)
        self.connect_custom_connection_layout.addLayout(self.operate_custom_connection_layout)

        #创建复制属性连接的页面布局
        self.copy_delete_connection_layout = QHBoxLayout()
        self.copy_delete_connection_layout.addWidget(self.copy_connection_btn)
        self.copy_delete_connection_layout.addWidget (self.delete_connection_btn)

        # 创建main_layout的布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addWidget(self.connect_default_connection_label)
        self.main_layout.addLayout(self.connect_default_connection_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.connect_custom_connection_label)
        self.main_layout.addLayout(self.connect_custom_connection_layout)
        self.main_layout.addStretch ()
        self.main_layout.addWidget(self.copy_delete_connection_label)
        self.main_layout.addLayout(self.copy_delete_connection_layout)
        self.main_layout.addStretch ()


    def add_connnect (self) :
        self.matrix_attr_cheekbox.stateChanged.connect(self.stateChanged_matrix_attr_cheekbox)
        self.reset_attr_btn.clicked.connect(self.clicked_reset_attr_btn)


    def stateChanged_matrix_attr_cheekbox(self):
        """
        当matrix_attr_cheekbox按钮被选中的时候，则将位移,旋转，缩放的属性选项全部取消
        """
        matrix_check_value = self.matrix_attr_cheekbox.isChecked()
        if matrix_check_value:
            self.translate_attr_cheekbox.setChecked (False)
            self.rotate_attr_cheekbox.setChecked (False)
            self.scale_attr_cheekbox.setChecked (False)

    def clicked_reset_attr_btn(self):
        """
        当reset_attr_btn按钮被按下的时候，则将位移,旋转，缩放，矩阵的属性选项全部取消
        """
        self.translate_attr_cheekbox.setChecked (False)
        self.rotate_attr_cheekbox.setChecked (False)
        self.scale_attr_cheekbox.setChecked (False)
        self.matrix_attr_cheekbox.setChecked(False)

def main () :
    return Connections_Tool ()


if __name__ == "__main__" :
    app = QApplication (sys.argv)
    mainwindow = Connections_Tool ()
    mainwindow.show ()
    sys.exit (app.exec_ ())
