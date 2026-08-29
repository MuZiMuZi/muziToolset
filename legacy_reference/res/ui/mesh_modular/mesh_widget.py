# coding=utf-8
u"""
这是一个完整的maya材质工具实例

目前已有的功能：

●选择一个或者多个物体，可以选择自动展示所有材质,或者手动载入并展示
●选择组，可以选择示所有子物体的材质
●选择对象自动保存在场景中
●按材质选择时，可以灵活切换添加选择与覆盖选择两种模式
●工具设置保存在工具中,关闭Maya或者重新打开文件后不会丢失
各物体上的材质按照组动态展示
●每个按钮上的labeI与材质节点名相同,且显示面数
●窗口可以浮动显示，可以吸附到侧边栏
●自动记录日志
●当材质数量改变，或者被重命名,或者模型被更改，或者shading engine
members发生改变时，可以通过手动刷新看到新的列表

"""

# 导入所有需要的模块
from __future__ import unicode_literals , print_function
from pymel.core import workspaceControl


try :
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

except ImportError :
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtWidgets import *
    from PySide import __version__
    from shiboken import wrapInstance
import maya.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import pymel.core as pm


class Selector_tool :
    """
    这个工具可以根据材质来选择模型不同的面
    """


    def __init__ (self) :
        self.winTitle = 'Select_mesh_Face'
        self.winName = 'MeshSelectTool'
        self.objects = list ()


    def init_ui (self) :
        """
        创建ui界面
        """
        # 创建一个frameLayout来获取物体的名称
        # columnWidth3设置三个部件的宽度，adjustableColumn表示第几个部件跟随着窗口缩放
        # placeholderText提示语
        with pm.frameLayout () as self.mainForm :
            with pm.menuBarLayout () as self.menuBar :
                self.add_menus ()
            self.nameField = pm.textFieldButtonGrp (
                label = 'Objects' ,
                columnWidth3 = [50 , 140 , 5] ,
                adjustableColumn = 2 ,
                editable = False ,
                buttonLabel = '<' ,
                placeholderText = 'Please select meshes in the viewport' ,
                buttonCommand = self.insert_selection
            )

            with pm.scrollLayout (childResizable = True) as self.mainScroll :
                pass

        #设置menuBar的布局吸附
        self.mainForm.attachFrom(self.menuBar.name(),'top',0)
        self.mainForm.attachFrom (self.menuBar.name () , 'left' , 0)
        self.mainForm.attachFrom (self.menuBar.name () , 'right' , 0)

        #设置nameField的布局吸附
        self.mainForm.attachFrom (self.nameField.name () , 'right' , 0)
        self.mainForm.attachFrom (self.nameField.name () , 'right' , 0)
        self.mainForm.attachFrom (self.nameField.name () , 'right' , 0)
        self.mainForm.attachFrom (self.nameField.name () , 'right' , 0)

    def add_menus (self) :
        '''
        添加菜单栏的按钮
        '''
        # 添加window栏的按钮
        with pm.menu (label = 'Window' , tearOff = True) as self.windowMenu :
            pm.menuItem (label = 'Refresh' , image = 'refresh.png' , command = lambda *a : None)
            pm.menuItem (label = 'Clear' , image = 'clearAll.png' , command = lambda *a : None)
            pm.menuItem (label = 'Collapse All' , image = 'dot.png' , command = lambda *a : None)
            pm.menuItem (label = 'Expand All' , image = 'dot.png' , command = lambda *a : None)
            pm.menuItem (label = 'Close' , image = 'closeTabButton.png' ,
                         command = lambda *a : workspaceControl (self.winTitle , edit = True , close = True))

        with pm.menu (label = 'Edit' , tearOff = True) as self.editMenu :
            # 创建分隔符
            pm.menuItem (divider = True , dividerLabel = 'Selection Mode')
            # 创建单选的互斥按钮组
            self.modeRadios = pm.radioMenuItemCollection ()
            pm.menuItem (label = 'Exclusive' , radioButton = True , command = lambda *a : None)
            pm.menuItem (label = 'Additive' , radioButton = False , command = lambda *a : None)

        with pm.menu (label = 'Help') as self.helpMenu :
            pm.menuItem (label = 'help' , image = 'help.png' ,
                         command = lambda *a : pm.showHelp ('https://help.autodesk.com/view/MAYAUL/2023/CHS/' ,
                                                            absolute = True))


    def add_buttons (self) :
        for i in range (5) :
            pm.button ()


    def validate_selection (self , *args) :
        """
        检查所选择的物体是否为模型节点
        """
        selected_objects = pm.selected (type = 'transform')
        self.objects = [n for n in selected_objects if n.getShape ()]
        if self.objects :
            return True
        else :
            return False


    def insert_selection (self , *args) :
        """
        根据所检查的结果来对物体进行操作
        """
        # 判断如果所选择的物体都不具有模型节点则返回
        if not self.validate_selection () :
            return
        for object in self.objects :
            with pm.frameLayout (
                    label = object.getShape ().name () ,
                    collapsable = True ,
                    parent = self.mainScroll) :
                self.add_buttons ()
