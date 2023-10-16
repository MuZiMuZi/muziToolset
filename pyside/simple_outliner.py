# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
class SimpleOutliner (QtWidgets.QDialog) :
    """
    创建一个类似maya大纲视图的弹窗页面
    """

    def __init__ (self , parent = get_maya_window ()) :
        super (Dialog , self).__init__ (parent)
        self.window_title = 'Simple_Outliner'
        self.setWindowTitle(self.window_title)
        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        """创建需要的小部件"""
        self.refresh_btn = QtWidgets.QPushButton('Refresh')


    def create_layouts (self) :
        """创建需要的布局"""
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addLayout(button_layout)


    def create_connections (self) :
        """连接需要的部件和对应的信号"""
        self.refresh_btn.clicked.connect(self.refresh_tree_widget)

    def refresh_tree_widget(self):
        print('TODO :  refresh_tree_widget')