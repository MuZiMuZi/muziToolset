from __future__ import unicode_literals , print_function
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from importlib import reload
from ..core import pipelineUtils
from . import config , Names_Tool_main , Joint_Tool_main , Rig_Tool_main , test_main


reload(Names_Tool_main)
reload(Joint_Tool_main)
reload(Rig_Tool_main)
reload(test_main)

class TemplateWindow (QtWidgets.QMainWindow) :

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
        self.close_action = QtWidgets.QAction ("关闭" , self)

        self.help_documents_action = QtWidgets.QAction ("帮助文档" , self)


    # 创建小部件
    def add_menubar (self) :
        # 创建window栏的菜单
        self.window_menu = QtWidgets.QMenu ("Window")
        self.window_menu.addAction (self.close_action)

        # 创建help栏的菜单
        self.help_menu = QtWidgets.QMenu ("Help")
        self.help_menu.addAction (self.help_documents_action)

        # 添加help栏的菜单
        self.menu_bar = self.menuBar ()
        self.menu_bar.addMenu (self.window_menu)
        self.menu_bar.addMenu (self.help_menu)


    # 创建布局
    def add_layouts (self) :
        # 设置标签布局
        self.main_widget = QtWidgets.QTabWidget ()
        self.main_widget.setTabShape (QTabWidget.Triangular)

        # 创建页面
        self.name_tool_tab = QtWidgets.QWidget ()
        self.joint_tool_tab = QtWidgets.QWidget ()
        self.rig_tool_tab = QtWidgets.QWidget ()
        self.control_tool_tab = QtWidgets.QWidget ()
        self.attr_tool_tab = QtWidgets.QWidget ()
        self.constraint_tool_tab = QtWidgets.QWidget ()
        self.test_tool_tab = QtWidgets.QWidget ()

        # 创建对应的页面标签
        self.main_widget.addTab (Names_Tool_main.main () , '命名')
        self.main_widget.addTab (Joint_Tool_main.main () , '关节')
        self.main_widget.addTab (Rig_Tool_main.main () , '绑定')
        self.main_widget.addTab (self.control_tool_tab , '控制器')
        self.main_widget.addTab (self.attr_tool_tab , '属性')
        self.main_widget.addTab (self.constraint_tool_tab , '约束')
        self.main_widget.addTab (test_main.show () , '测试')

        self.setCentralWidget (self.main_widget)


    # 信号与槽链接

    def name_tool_tab_ui (self) :
        layout = QtWidgets.QHBoxLayout ()
        name_tool = Names_Tool_main.Names_Tool ()
        name_tool.show ()
        # self.name_tool_tab.setlayout (layout)


    def test_tool_tab_ui (self) :
        pass


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = TemplateWindow ()  # 创建实例
    window.show ()  # 显示窗口
