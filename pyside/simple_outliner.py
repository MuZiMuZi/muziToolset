# coding:utf-8
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window () :
    main_window_ptr = omui.MQtUtil.mainWindow ()
    return wrapInstance (int (main_window_ptr) , QtWidgets.QWidget)


class SimpleOutliner (QtWidgets.QDialog) :
    """
    创建一个类似maya大纲视图的弹窗页面
    """


    def __init__ (self , parent = maya_main_window ()) :
        super (SimpleOutliner , self).__init__ (parent)
        self.window_title = 'Simple_Outliner'
        self.setWindowTitle (self.window_title)
        # 添加部件
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_widgets (self) :
        """创建需要的小部件"""

        self.tree_widget = QtWidgets.QTreeWidget ()
        # 隐藏抬头标题
        self.tree_widget.setHeaderHidden (True)
        # 设置抬头标题的文本
        header = self.tree_widget.headerItem ()
        header.setText (0 , 'Column 0 text')

        self.refresh_btn = QtWidgets.QPushButton ('Refresh')


    def create_layouts (self) :
        """创建需要的布局"""
        button_layout = QtWidgets.QVBoxLayout ()
        button_layout.addStretch ()
        button_layout.addWidget (self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout (self)
        main_layout.setContentsMargins (2 , 2 , 2 , 2)
        main_layout.setSpacing (2)
        main_layout.addWidget (self.tree_widget)
        main_layout.addLayout (button_layout)


    def create_connections (self) :
        """连接需要的部件和对应的信号"""
        self.refresh_btn.clicked.connect (self.refresh_tree_widget)


    def refresh_tree_widget (self) :
        """根据maya里的物品更新tree_widget"""
        # 清空tree_widget
        self.tree_widget.clear ()
        # 查询maya里所有的顶层物体，并将这些顶层物体添加到对应的tree_widget里作为item
        top_level_object_names = cmds.ls (assemblies = True)
        for name in top_level_object_names :
            item = self.create_item (name)
            self.tree_widget.addTopLevelItem (item)


    def create_item (self , name) :
        item = QtWidgets.QTreeWidgetItem ([name])
        self.add_children_item (item)

        return item


    def add_children_item (self , item) :
        """
        如果tree_widget里的item有子物体的话则需要添加子item
        """
        children = cmds.listRelatives (item.text (0) , children = True)
        if children :
            for child in children :
                child_item = self.create_item (child)
                item.addChild (child_item)


window = SimpleOutliner ()
window.show ()
