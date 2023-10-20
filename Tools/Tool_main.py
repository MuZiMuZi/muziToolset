from __future__ import unicode_literals , print_function
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from importlib import reload
from ..core import pipelineUtils
from . import config , Names_Tool_main , Joint_Tool_main , Rig_Tool_main , test_main
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
class TemplateWindow (QMainWindow) :

    def __init__ (self , parent = pipelineUtils.Pipeline.get_maya_main_window ()) :
        super (TemplateWindow , self).__init__ (parent)

        # 设置标题
        self.setWindowTitle ("muzi_Tools")
        # 设置宽高
        self.setMinimumSize (500 , 600)

        # 添加ui布局
        self.add_actions ()
        self.add_menubar ()
        self.add_layouts ()


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
        self.main_widget.addTab (Joint_Tool_main.main () , '关节')
        self.main_widget.addTab (Rig_Tool_main.main () , '绑定')
        self.main_widget.addTab (control_widget.main() , '控制器')
        self.main_widget.addTab (Names_Tool_main.main () , '命名')
        # self.main_widget.addTab (self.attr_tool_tab , '属性')
        # self.main_widget.addTab (self.constraint_tool_tab , '约束')
        self.main_widget.addTab (nodes_widget.main () , '节点')
        self.main_widget.addTab (snap_widget.main () , '吸附')

        self.setCentralWidget (self.main_widget)


    # 信号与槽链接


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = TemplateWindow ()  # 创建实例
    window.show ()  # 显示窗口
