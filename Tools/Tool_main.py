from __future__ import unicode_literals , print_function

import json
import os.path
import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from importlib import reload
from ..core import pipelineUtils
from . import config , Names_Tool_main , Joint_Tool_main , Rig_Tool_main , test_main , Constraint_Tool_main , \
    Connections_Tool_main , Attr_Tool_main
import muziToolset.res.ui.control_modular.control_widget as control_widget
import muziToolset.res.ui.nodes_modular.nodes_widget as nodes_widget
import muziToolset.res.ui.snap_modular.snap_widget as snap_widget


reload (Names_Tool_main)
reload (Joint_Tool_main)
reload (Rig_Tool_main)
reload (test_main)
reload (control_widget)
reload (nodes_widget)
reload (snap_widget)
reload (Constraint_Tool_main)
reload (Connections_Tool_main)
reload (Attr_Tool_main)


class Tool_main_Window (QMainWindow) :

    def __init__ (self , parent = pipelineUtils.Pipeline.get_maya_main_window ()) :
        super (Tool_main_Window , self).__init__ (parent)

        # 设置标题
        self.setWindowTitle ("muzi_Tools")
        # 设置宽高
        self.setMinimumSize (500 , 600)
        # 添加ui布局
        self.add_actions ()
        self.add_menubar ()
        self.add_layouts ()

        self.geometry = None


    # 创建标签
    def add_actions (self) :
        self.close_action = QAction ("关闭" , self)

        self.help_documents_action = QAction ("帮助文档" , self)


    # 创建小部件
    def add_menubar (self) :
        # 创建window栏的菜单
        self.window_menu = QMenu ("Window")
        self.window_menu.addAction (self.close_action)

        # 创建help栏的菜单
        self.help_menu = QMenu ("Help")
        self.help_menu.addAction (self.help_documents_action)

        # 添加help栏的菜单
        self.menu_bar = self.menuBar ()
        self.menu_bar.addMenu (self.window_menu)
        self.menu_bar.addMenu (self.help_menu)


    # 创建布局
    def add_layouts (self) :
        # 设置标签布局
        self.main_widget = QTabWidget ()
        self.main_widget.setTabShape (QTabWidget.Triangular)

        # 创建对应的页面标签
        self.main_widget.addTab (Attr_Tool_main.main () , '属性')
        self.main_widget.addTab (Constraint_Tool_main.main () , '约束')

        self.main_widget.addTab (Joint_Tool_main.main () , '关节')
        self.main_widget.addTab (Rig_Tool_main.main () , '绑定')
        self.main_widget.addTab (control_widget.main () , '控制器')
        self.main_widget.addTab (Names_Tool_main.main () , '命名')
        self.main_widget.addTab (Connections_Tool_main.main () , '连接')


        self.setCentralWidget (self.main_widget)


    # 信号与槽链接


    def closeEvent (self , event) :
        # 防止出现qt被删除的情况报错，如果对象被删除，则代码不执行
        if isinstance (self , Tool_main_Window) :
            # 在对话框关闭的时候存储对话框位置信息和大小
            self.geometry = self.saveGeometry ()


    def showEvent (self , event) :
        # 在对话框显示的时候读取对话框的位置信息和大小
        if self.geometry :
            self.restoreGeometry (self.geometry)


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Tool_main_Window ()  # 创建实例
    window.show ()  # 显示窗口
