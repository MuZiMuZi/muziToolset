# coding=utf-8
# 导入所有需要的模块
from importlib import reload

import maya.cmds as cmds
from PySide2.QtWidgets import *

from ..setup import bone_ui
from ... import config
from ....bind.module.base import bone


reload (bone)
reload (bone_ui)


class Bone_Widget (bone_ui.Ui_MainWindow , QMainWindow) :


    # rigtype_bone = ['bone']

    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        # 针对多个关节点的绑定模块，
        # 组件需要的参数有[side,name,jnt_number,jnt_parent,ctrl_parent]
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        super ().__init__ (parent , *args , **kwargs)
        # 调用父类的ui方法，来运行ui
        self.setupUi (self)

        # 默认情况下删除按钮为隐藏状态
        self.delete_btn.setVisible (False)
        self.init_base ()

        # 给定一个用来采集信息收集的变量,判断是否已经采集了所有组件的参数信息并返回，当参数信息没有采集完毕的时候不进行下一步
        self.is_info_base = False

        self.add_connect ()


    # 初始化需要输入的参数
    def init_base (self) :
        # 初始化参数
        for side in config.Side :
            self.side_cbox.addItem (side.value)


    # 用来添加连接的槽函数
    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        self.create_btn.clicked.connect (self.clicked_create_btn)
        # self.base_widget.delete_btn.clicked.connect (self.delete_setup)


    # 连接创建按钮的槽函数，当按下创建按钮函数的时候会做以下操作
    def clicked_create_btn (self) :
        """
        连接创建按钮的槽函数，当按下创建按钮函数的时候会做以下操作
        1.将获取已经给定的组件的属性
        2.判断组件需要给定数值的组件参数是否存在，如果都符合要求的话，则开始进行生成绑定
         # 如果参数已经全部收集完毕符合可以创建绑定的条件的时候，则开始生成绑定
            # 1.将创建按钮变成不可操作的模式，防止误触
            self.create_btn.setVisible (False)
            # 2.将删除按钮从隐藏状态下显示出来，用于删除不需要的绑定
            self.delete_btn.setVisible (True)
            # 3，将获取组件的属性用来创建用于关节定位的bp关节
            # 创建用来定位的bp关节
        """

        # 获取填写的组件的参数信息
        # 获取组件的属性
        self.parse_base ()

        # 判断组件需要给定数值的组件参数是否存在，如果都符合要求的话，则进行下一步
        self.is_info_base = self.check_parameters ()

        # 判断self.is_info_base的值是否存在，当这个值不存在的时候，说明参数收集还未完成，不进行下一步
        if not self.is_info_base :
            return
        else :
            # 如果参数已经全部收集完毕符合可以创建绑定的条件的时候，则开始进行下一步
            # 1.将创建按钮变成不可操作的模式，防止误触
            self.create_btn.setVisible (False)
            # 2.将删除按钮从隐藏状态下显示出来，用于删除不需要的绑定
            self.delete_btn.setVisible (True)
            # 3，将获取组件的属性用来创建用于关节定位的bp关节
            # 创建用来定位的bp关节
            self.build_setup ()


    # 分析base_widget中的输入并将其作为参数返回
    def parse_base (self , *args) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        self.name = self.name_edit.text ()
        self.side = self.side_cbox.currentText ()
        self.jnt_number = self.jnt_number_sbox.value ()
        self.jnt_parent = self.jnt_parent_edit.text ()
        self.ctrl_parent = self.ctrl_parent_edit.text ()

        # 组件需要给定数值的输入，
        self.base_parameters = [self.side , self.jnt_number]


    # 判断组件需要给定数值的组件参数是否存在或者是否符合要求，如果都符合要求的话，则进行下一步
    def check_parameters (self) :
        self.is_info_base = True  # 变量用于判断所有参数是否都符合要求

        for parameter in self.base_parameters :
            # 判断组件需要给定数值的组件参数是否存在
            if not parameter :
                cmds.warning ("{}_{}_{}_{:03d}组件还未给定所有需要的参数，请重新设置".format (self.side , self.name ,
                                                                                             self.module_edit.text () ,
                                                                                             int (
                                                                                                 self.index_edit.text ())))
                self.is_info_base = False
                raise ValueError ("{}_{}_{}_{:03d}组件还未给定所有需要的参数，请重新设置".format (self.side , self.name ,
                                                                                                 self.module_edit.text () ,
                                                                                                 int (
                                                                                                     self.index_edit.text ())))

        return self.is_info_base


        # 根据给定的参数信息，生成绑定准备，创建用来定位的bp关节


    def build_setup (self) :
        # 创建实例化的对象
        self.module = bone.Bone (self.side , self.name , self.jnt_number , self.jnt_parent , self.ctrl_parent)
        self.module.build_setup ()


    # 根据base_widget和extra_widget返回的参数,创建绑定系统
    def build_rig (self) :
        # 删除已经创建好的绑定系统
        self.module.build_rig ()


    # 删除已经创建好的绑定系统
    def delete_rig (self) :
        self.module.delete_rig ()


def main () :
    return Bone_Widget ()
