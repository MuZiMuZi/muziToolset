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
from ..core import pipelineUtils , qtUtils

from . import config , Names_Tool_main , Joint_Tool_main , Rig_Tool_main , Constraint_Tool_main , \
    Connections_Tool_main , Attr_Tool_main
import muziToolset.res.ui.control_modular.control_widget as control_widget
import muziToolset.res.ui.nodes_modular.nodes_widget as nodes_widget
import muziToolset.res.ui.snap_modular.snap_widget as snap_widget


reload (config)
reload (Names_Tool_main)
reload (Joint_Tool_main)
reload (Rig_Tool_main)
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

        # 恢复窗口大小和位置
        settings = QSettings ()
        geometry = settings.value ("geometry")
        windowState = settings.value ("windowState")

        if geometry is not None :
            self.restoreGeometry (geometry)

        if windowState is not None :
            self.restoreState (windowState)

        # 设置qt样式表
        style_file = './simplicity.qss'
        style_sheet = qtUtils.QSSLoader.read_qss_file (config.qss_dir + style_file)
        self.setStyleSheet (style_sheet)


    # 创建标签
    def add_actions (self) :
        self.close_action = QAction ("Close" , self)

        self.help_documents_action = QAction ("About" , self)

        # 主题设置的action
        self.manjaroMix_action = QAction ('manjaroMix' , self)
        self.amoled_action = QAction ('amoled' , self)

        self.shared_action = QAction ('shared' , self)
        self.black_action = QAction ('black' , self)
        self.lightblack_action = QAction ('lightblack' , self)
        self.simplicity_action = QAction ('simplicity' , self)
        self.evilworks_action = QAction ('evilworks' , self)


        self.theme_Actions = [self.manjaroMix_action , self.amoled_action  , self.shared_action , self.black_action , self.lightblack_action,
                              self.simplicity_action,self.evilworks_action]


    def add_actions_connect (self) :
        """连接actions的信号"""
        self.theme_menu.hovered.connect (self.on_menu_hovered)


    def on_menu_hovered (self , action) :
        """
        连接主题菜单的槽函数，在鼠标悬浮上空时发射该信号，获取悬浮位置的action的名称然后更新主题设置
        """
        # 用于处理悬停信号的插槽
        if isinstance (action , QAction) :
            action_text = action.text ()
            self.setStyleSheet (qtUtils.QSSLoader.read_qss_file (config.qss_dir + './{}.qss'.format (action_text)))


    def add_menubar (self) :
        # 创建window栏的菜单
        self.window_menu = QMenu ("Window")
        self.window_menu.addAction (self.close_action)

        # 创建help栏的菜单
        self.help_menu = QMenu ("Help")
        self.help_menu.addAction (self.help_documents_action)

        # 创建theme栏的菜单
        self.theme_menu = QMenu ("Theme")
        self.theme_menu.addActions (self.theme_Actions)

        # 添加各个菜单到窗口
        self.menu_bar = self.menuBar ()
        self.menu_bar.addMenu (self.window_menu)
        self.menu_bar.addMenu (self.help_menu)
        self.menu_bar.addMenu (self.theme_menu)

        # 连接信号
        self.add_actions_connect ()


    # 创建布局
    def add_layouts (self) :
        # 设置标签布局
        self.main_widget = QTabWidget ()
        # self.main_widget.setTabShape (QTabWidget.Triangular)

        # 创建对应的页面标签
        self.main_widget.addTab (Rig_Tool_main.main () , 'Rig')
        self.main_widget.addTab (Attr_Tool_main.main () , 'Attr')
        self.main_widget.addTab (Constraint_Tool_main.main () , 'Constraint')
        self.main_widget.addTab (Joint_Tool_main.main () , 'Joint')
        self.main_widget.addTab (control_widget.main () , 'Control')
        self.main_widget.addTab (Names_Tool_main.main () , 'Names')
        self.main_widget.addTab (Connections_Tool_main.main () , 'Connections')

        self.setCentralWidget (self.main_widget)


    def closeEvent (self , event) :
        # 关闭窗口时保存窗口大小和位置,重写了closeEvent方法
        settings = QSettings ()
        settings.setValue ("geometry" , self.saveGeometry ())
        settings.setValue ("windowState" , self.saveState ())
        super ().closeEvent (event)


if __name__ == "__main__" :

    try :
        window.close ()  # 关闭窗口
        window.deleteLater ()  # 删除窗口
    except :
        pass
    window = Tool_main_Window ()  # 创建实例
    window.show ()  # 显示窗口
