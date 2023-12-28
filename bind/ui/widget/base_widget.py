# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals , print_function


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
from importlib import reload
import os
from ... import config
from ..setup import base_ui

from ....bind.module.base import base
from ....core import qtUtils


reload (base)
reload (base_ui)


class Base_Widget (base_ui.Ui_MainWindow , QMainWindow) :


    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        super ().__init__ (parent , *args , **kwargs)
        # 调用父类的ui方法，来运行ui
        self.setupUi (self)

        # 默认情况下删除按钮为隐藏状态
        self.delete_btn.setVisible (False)
        self.name = None
        self.side = None
        self.jnt_number = None
        self.jnt_parent = None
        self.ctrl_parent = None
        self.init_base ()
        self.add_connect ()
        # self.create_widget ()
        # self.create_layout ()


    def init_base (self) :
        # 初始化参数
        for side in config.Side :
            self.side_cbox.addItem (side.value)


    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        self.create_btn.clicked.connect (self.clicked_create_btn)
        # self.base_widget.delete_btn.clicked.connect (self.delete_setup)


    def clicked_create_btn (self) :
        """
        连接创建按钮的槽函数，当按下创建按钮函数的时候会做以下操作
        1，将创建按钮变成不可操作的模式，防止误触
        2.将删除按钮从隐藏状态下显示出来，用于删除不需要的绑定
        3，将获取组件的属性用来创建用于关节定位的bp关节
        4.获取组件的属性来修改custom_widget里item的名称
        """
        # 1.将创建按钮变成不可操作的模式，防止误触
        self.create_btn.setVisible (False)
        # 2.将删除按钮从隐藏状态下显示出来，用于删除不需要的绑定
        self.delete_btn.setVisible (True)
        # Todo
        # 3，将获取组件的属性用来创建用于关节定位的bp关节
        # 获取组件的属性
        self.parse_base ()
        # 创建用来定位的bp关节
        self.build_setup ()



    def parse_base (self , *args) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        self.name = self.name_edit.text ()
        self.side = self.side_cbox.currentText ()
        self.jnt_number = self.jnt_number_sbox.value ()
        self.jnt_parent = self.jnt_parent_edit.text ()
        self.ctrl_parent = self.ctrl_parent_edit.text ()


    def build_setup (self) :
        # # 生成定位关节系统
        self.setup = base.Base (self.side , self.name , self.jnt_number , self.jnt_parent , self.ctrl_parent)
        self.setup.build_setup ()


    # 根据base_widget和extra_widget返回的参数,创建绑定系统
    def build_rig (self) :
        # 删除已经创建好的绑定系统
        self.rig = base.Base (self.side , self.name , self.jnt_number , self.jnt_parent , self.ctrl_parent)
        self.rig.build_rig ()


def main () :
    return Base_Widget ()


class Setting_Widget (QMainWindow) :

    def __init__ (self , name , *args , **kwargs) :
        """Override"""
        super (Setting_Widget , self).__init__ (*args , **kwargs)
        self.base_ui = '{}.ui'.format (name)
        self.create_base_widget ()


    # 初始化作为QWidget对象的extra_widget属性,用于设置绑定组件的特殊属性，比如(长度，朝向，拉伸，IK启用，FK启用,twist启用)等属性
    # （Length, orientation, stretch, IK enabled, FK enabled, twist enabled）
    def create_base_widget (self) :
        # 初始化作为QWidget对象的extra_widget属性,用于设置绑定组件的特殊属性，比如(长度，朝向，拉伸，IK启用，FK启用,twist启用)等属性
        # （Length, orientation, stretch, IK enabled, FK enabled, twist enabled）
        self.base_widget = QWidget ()
        self.ui_path = os.path.join (config.ui_dir , self.base_ui)
        # Use the custom loadUi function
        self.ui = qtUtils.load_ui (self.ui_path)
        for side in config.Side :
            self.ui.side_cbox.addItem (side.value)


    # 分析base_widget中的输入并将其作为参数返回
    def parse_base_widget (self) :
        """ 分析base_widget中的输入并将其作为参数返回
        获取Side (side) , name,jnt_number,jnt_parent,ctrl_parent
        """
        side = self.base_widget.side_cbox.currentText ()
        name = self.base_widget.name_edit.text ()
        jnt_number = self.base_widget.jnt_number_sbox.currentText ()
        jnt_parent = self.base_widget.jnt_parent_edit.text ()
        ctrl_parent = self.base_widget.ctrl_parent_edit.text ()

        return [Side (side) , name , jnt_number , jnt_parent , ctrl_parent]


    ## 根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备
    def build_setup (self , side , name , jnt_number , jnt_parent , ctrl_parent) :
        """根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备"""
        # 分析base_widget中的输入并将其作为参数返回
        side , name , jnt_number , jnt_parent , ctrl_parent = self.parse_base_widget ()
        # 根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备
        self.obj = Base (side , name , jnt_number , jnt_parent , ctrl_parent)
        self.obj.build_setup ()


    # 根据base_widget和extra_widget返回的参数,创建绑定系统
    def build_rig (self) :
        """
        根据生成的bp定位关节，创建绑定系统
        """
        side , name , jnt_number , jnt_parent , ctrl_parent = self.parse_base_widget ()
        # 根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备
        self.obj = Base (side , name , jnt_number , jnt_parent , ctrl_parent)
        self.obj.build_rig ()


    # 删除已经创建好的绑定系统
    def delete_rig (self) :
        side , name , jnt_number , jnt_parent , ctrl_parent = self.parse_base_widget ()
        # 删除已经创建好的绑定系统
        self.obj = Base (side , name , jnt_number , jnt_parent , ctrl_parent)
        self.obj.delete_rig ()
