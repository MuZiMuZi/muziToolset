from  __future__ import unicode_literals , print_function
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
from importlib import reload
from ..core import pipelineUtils
from . import config,__init__

reload(__init__)


class TemplateWindow (QtWidgets.QMainWindow) :

    def __init__ (self , parent = pipelineUtils.Pipeline.get_maya_main_window()) :
        super (TemplateWindow , self).__init__ (parent)

        # 设置标题
        self.setWindowTitle ("muzi_Tools")
        # 设置宽高
        self.setMinimumSize (300 , 500)

        self.create_actions ()
        self.create_menus ()
        self.create_widgets ()
        self.create_layouts ()



    # 创建action
    def create_actions (self) :
        self.show_settings_action = QtWidgets.QAction ("setting..." , self)
        self.show_settings_action.triggered.connect (self.show_settings_dialog)

        self.show_about_action = QtWidgets.QAction ("about" , self)
        self.show_about_action.triggered.connect (self.show_about_dialog)


    # 创建菜单
    def create_menus (self) :
        edit_menu = QtWidgets.QMenu ("Edit")
        edit_menu.addAction (self.show_settings_action)

        help_menu = QtWidgets.QMenu ("Help")
        help_menu.addAction (self.show_about_action)

        menu_bar = self.menuBar ()
        menu_bar.addMenu (edit_menu)
        menu_bar.addMenu (help_menu)


    # 创建小部件
    def create_widgets (self) :
        self.close_button = QtWidgets.QPushButton ("Close")
        self.close_button.setMinimumSize (60 , 25)
        self.apply_button = QtWidgets.QPushButton ("Apply")
        self.apply_button.setMinimumSize (60 , 25)


    # 创建布局
    def create_layouts (self) :
        self.main_widget = QtWidgets.QTabWidget ()

        self.name_tool_tab = QtWidgets.QWidget()
        self.joint_tool_tab = QtWidgets.QWidget()

        self.main_widget.addTab(self.name_tool_tab,'命名')
        self.main_widget.addTab (self.joint_tool_tab , '关节')
        self.setCentralWidget (self.main_widget)


    # 信号与槽链接

    def name_tool_tab_ui(self):
        #


    def show_settings_dialog (self) :
        print ("TODO: show_settings_dialog")


    def show_about_dialog (self) :
        print ("TODO: show_about_dialog")


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = TemplateWindow ()  # 创建实例
    window.show ()  # 显示窗口