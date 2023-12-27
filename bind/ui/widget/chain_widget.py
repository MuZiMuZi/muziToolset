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
from ... import config
from . import chain_ui
from ..widget import bone_widget
from ....bind.module.base import base


reload (bone_widget)
reload (base)
reload (chain_ui)


class Chain_Widget (chain_ui.Ui_MainWindow , QMainWindow) :


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
        self.init_base ()


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
        pass

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
    return Chain_Widget ()
