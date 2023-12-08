# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals , print_function


try :
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import QUiLoader
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
from . import bone
from ....bind import config
reload (bone)
reload(config)


class BaseItem (bone.RigItem) :

    def __init__ (self , name = 'base') :
        """Override"""
        super (BaseItem , self).__init__ (name)
        self.base_ui = 'base.ui'
        self.create_base_widget ()


    # 初始化作为QWidget对象的extra_widget属性,用于设置绑定组件的特殊属性，比如(长度，朝向，拉伸，IK启用，FK启用,twist启用)等属性
    # （Length, orientation, stretch, IK enabled, FK enabled, twist enabled）
    def create_base_widget (self) :
        # 初始化作为QWidget对象的extra_widget属性,用于设置绑定组件的特殊属性，比如(长度，朝向，拉伸，IK启用，FK启用,twist启用)等属性
        # （Length, orientation, stretch, IK enabled, FK enabled, twist enabled）
        self.base_widget = QWidget ()
        self.ui_path = os.path.join (config.ui_dir , self.base_ui)
        print(self.ui_path)
        # Use the custom loadUi function
        self.ui = QUiLoader ().load (self.ui_path)
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


class Base (bone.Bone) :
    u"""
    基础的关节和控制器绑定，继承于bone
    """


    def __init__ (self , side , name , joint_number , joint_parent = None , control_parent = None) :
        bone.Bone.__init__ (self , side , name , joint_number , joint_parent , control_parent)
        self.rtype = 'Base'
