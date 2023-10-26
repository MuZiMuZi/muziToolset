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
        self.translate_attr_cheekbox = QCheckBox('Translate')
        self.rotate_attr_cheekbox = QCheckBox ('Rotate')
        self.scale_attr_cheekbox = QCheckBox ('Scale')
        self.matrix_attr_cheekbox = QCheckBox ('Matrix')

        self.connect_default_connection_btn = QPushButton('创建连接')
        self.delete_default_connection_btn = QPushButton ('删除连接')




    def create_layouts (self) :
        #创建默认属性连接的的布局
        self.connect_default_connection_layout = QVBoxLayout()
        #创建默认属性的布局
        self.default_attr_layout = QHBoxLayout()
        self.default_attr_layout.addWidget(self.translate_attr_cheekbox)
        self.default_attr_layout.addWidget (self.rotate_attr_cheekbox)
        self.default_attr_layout.addWidget (self.scale_attr_cheekbox)
        self.default_attr_layout.addWidget (self.matrix_attr_cheekbox)

        #创建操作默认属性链接的布局
        self.operate_default_connection_layout = QHBoxLayout ()
        self.operate_default_connection_layout.addWidget(self.connect_default_connection_btn)
        self.operate_default_connection_layout.addWidget (self.delete_default_connection_btn)

        #将default_attr_layout和operate_default_connection_layout，添加到connect_default_connection_layout里
        self.connect_default_connection_layout.addLayout(self.default_attr_layout)
        self.connect_default_connection_layout.addLayout (self.operate_default_connection_layout)

        # 创建main_layout的布局
        self.main_layout = QVBoxLayout (self)
        self.main_layout.addWidget(self.connect_default_connection_label)
        self.main_layout.addLayout(self.connect_default_connection_layout)
        self.main_layout.addStretch()


    def add_connnect (self) :
        pass


def main () :
    return Connections_Tool ()


if __name__ == "__main__" :
    app = QApplication (sys.argv)
    mainwindow = Connections_Tool ()
    mainwindow.show ()
    sys.exit (app.exec_ ())
