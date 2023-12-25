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
from . import base_ui
from ..widget import bone_widget
from ....bind.module.base import base
from ....core import qtUtils


reload (bone_widget)
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

        self.name = None
        self.side = None
        self.jnt_number = None
        self.jnt_parent = None
        self.control_parent = None

        # self.create_widget ()
        # self.create_layout ()


    def create_widget (self) :
        """
        初始化作为QWidget对象的base_widget属性,用于设置绑定的基础属性（例如名称，边，关节数量，关节的父对象，控制器的父对象）
        """
        # 调用父类的ui方法，来运行ui
        pass


    def create_layout (self) :
        self.main_layout = QHBoxLayout (self)
        self.main_layout.addWidget (self.base_widget)
        if self.extra_widget :
            self.main_layout.addWidget (self.extra_widget)


    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        # self.create_btn.clicked.connect (lambda :print(12))
        # self.base_widget.delete_btn.clicked.connect (self.delete_setup)


    def parse_base (self , *args) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        self.name = self.name_edit.text ()
        self.side = self.side_cbox.currentText ()
        self.jnt_number = self.jnt_number_sbox.currentText ()
        self.jnt_parent = self.jnt_parent_edit.text ()
        self.control_parent = self.control_parent_edit.text ()


    def build_setup (self) :
        # 读取输入信息
        self.parse_base ()
        #
        # # 生成定位关节系统
        # self.setup = base.Base (self.side , self.name , self.joint_number , self.joint_parent , self.control_parent)
        # self.setup.build_setup ()


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
        获取Side (side) , name,joint_number,jnt_parent,control_parent
        """
        side = self.base_widget.side_cbox.currentText ()
        name = self.base_widget.name_edit.text ()
        joint_number = self.base_widget.jnt_number_sbox.currentText ()
        jnt_parent = self.base_widget.jnt_parent_edit.text ()
        control_parent = self.base_widget.control_parent_edit.text ()

        return [Side (side) , name , joint_number , jnt_parent , control_parent]


    ## 根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备
    def build_setup (self , side , name , joint_number , jnt_parent , control_parent) :
        """根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备"""
        # 分析base_widget中的输入并将其作为参数返回
        side , name , joint_number , jnt_parent , control_parent = self.parse_base_widget ()
        # 根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备
        self.obj = Base (side , name , joint_number , jnt_parent , control_parent)
        self.obj.build_setup ()


    # 根据base_widget和extra_widget返回的参数,创建绑定系统
    def build_rig (self) :
        """
        根据生成的bp定位关节，创建绑定系统
        """
        side , name , joint_number , jnt_parent , control_parent = self.parse_base_widget ()
        # 根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备
        self.obj = Base (side , name , joint_number , jnt_parent , control_parent)
        self.obj.build_rig ()


    # 删除已经创建好的绑定系统
    def delete_rig (self) :
        side , name , joint_number , jnt_parent , control_parent = self.parse_base_widget ()
        # 删除已经创建好的绑定系统
        self.obj = Base (side , name , joint_number , jnt_parent , control_parent)
        self.obj.delete_rig ()
