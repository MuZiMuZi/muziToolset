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

        # 设置各个物体的图标
        self.transform_icon = QtGui.QIcon (":transform.svg")
        self.camera_icon = QtGui.QIcon (":Camera.png")
        self.mesh_icon = QtGui.QIcon (":mesh.svg")

        # 添加部件
        self.create_actions ()
        self.create_widgets ()
        self.create_layouts ()

        # 添加连接
        self.create_connections ()


    def create_actions (self) :
        """
        创建自定义的行为
        """
        self.about_action = QtWidgets.QAction ('About' , self)

        self.display_shape_action = QtWidgets.QAction ('Shapes' , self)
        self.display_shape_action.setCheckable (True)
        self.display_shape_action.setChecked (True)


    def create_widgets (self) :
        """创建需要的小部件"""

        self.tree_widget = QtWidgets.QTreeWidget ()
        # 隐藏抬头标题
        self.tree_widget.setHeaderHidden (True)
        # 设置抬头标题的文本
        header = self.tree_widget.headerItem ()
        header.setText (0 , 'Column 0 text')

        self.refresh_btn = QtWidgets.QPushButton ('Refresh')

        # 创建自定义的右键菜单
        self.menu_bar = QtWidgets.QMenuBar ()
        self.display_menu = self.menu_bar.addMenu ('Display')
        self.display_menu.addAction (self.display_shape_action)
        self.help_menu = self.menu_bar.addMenu ('Help')
        self.help_menu.addAction (self.about_action)


    def create_layouts (self) :
        """创建需要的布局"""
        button_layout = QtWidgets.QVBoxLayout ()
        button_layout.addStretch ()
        button_layout.addWidget (self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout (self)
        main_layout.setContentsMargins (2 , 2 , 2 , 2)
        main_layout.setMenuBar (self.menu_bar)
        main_layout.setSpacing (2)
        main_layout.addWidget (self.tree_widget)
        main_layout.addLayout (button_layout)


    def create_connections (self) :
        """连接需要的部件和对应的信号"""
        # 行为进行链接
        self.about_action.triggered.connect (self.about)
        self.display_shape_action.triggered.connect (self.set_shape_nodes_visible)
        #
        # 当tree——widget里item展开或收起的时候触发信号
        self.tree_widget.itemCollapsed.connect (self.update_icon)
        self.tree_widget.itemExpanded.connect (self.update_icon)

        # 当tree——widget里item被选择的时候触发信号
        self.tree_widget.itemSelectionChanged.connect (self.select_items)
        self.refresh_btn.clicked.connect (self.refresh_tree_widget)


    def refresh_tree_widget (self) :
        """根据maya里的物品更新tree_widget"""
        # 获取maya里所有的形状节点
        self.shape_nodes = cmds.ls (shapes = True)

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
        self.update_icon (item)
        is_shape = name in self.shape_nodes
        #存储数据
        item.setData(0,QtCore.Qt.UserRole,is_shape)
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


    def update_icon (self , item) :
        """
        更新item的图标
        """
        object_type = ""

        if item.isExpanded () :  # 如果item被展开
            object_type = "transform"
        else :
            child_count = item.childCount ()
            if child_count == 0 :
                object_type = cmds.objectType (item.text (0))
            elif child_count == 1 :
                child_item = item.child (0)
                object_type = cmds.objectType (child_item.text (0))
            else :
                object_type = "transform"
        if object_type == "transform" :
            item.setIcon (0 , self.transform_icon)
        elif object_type == "camera" :
            item.setIcon (0 , self.camera_icon)
        elif object_type == "mesh" :
            item.setIcon (0 , self.mesh_icon)


    def select_items (self) :
        """
        选择了tree_widget里的item的话，maya的物体也会被选中
        """
        items = self.tree_widget.selectedItems ()
        names = []
        for item in items :
            names.append (item.text (0))

        cmds.select (names , replace = True)


    def about (self) :
        # 弹出一个对话框
        QtWidgets.QMessageBox.about (self , 'About Simple Outliner ' , 'Add About Text Here')


    def set_shape_nodes_visible (self , visible) :
        pass


window = SimpleOutliner ()
window.show ()
