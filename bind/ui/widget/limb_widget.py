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

from . import base_widget
from ..setup import limb_ui
from importlib import reload


reload (limb_ui)
reload (base_widget)


class Limb_Widget (limb_ui.Ui_MainWindow , base_widget.Base_Widget , QMainWindow) :


    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        super ().__init__ (parent , *args , **kwargs)


    def init_base (self) :
        # 继承base_widget.Base_Widget的init_base方法
        super ().init_base ()


    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        super ().add_connect ()


    def parse_base (self , *args) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        self.name = self.name_edit.text ()
        self.side = self.side_cbox.currentText ()
        self.jnt_parent = self.jnt_parent_edit.text ()
        self.ctrl_parent = self.ctrl_parent_edit.text ()


    def build_setup (self) :
        # 读取输入信息
        self.parse_base ()
        #
        # # 生成定位关节系统
        # self.setup = base.Base (self.side , self.name , self.jnt_number , self.jnt_parent , self.ctrl_parent)
        # self.setup.build_setup ()


def main () :
    return Chain_Widget ()


def main () :
    return Limb_Widget ()
