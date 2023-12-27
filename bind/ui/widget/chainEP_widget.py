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
from bind.ui import chainEP_ui
from . import chain_widget
from importlib import reload


reload (chain_widget)
reload (chainEP_ui)


class ChainEP_Widget (chainEP_ui.Ui_MainWindow , chain_widget.Chain_Widget, QMainWindow) :


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
        super ().parse_base ()


    def build_setup (self) :
        # 读取输入信息
        self.parse_base ()
        #
        # # 生成定位关节系统
        # self.setup = base.Base (self.side , self.name , self.joint_number , self.joint_parent , self.control_parent)
        # self.setup.build_setup ()


def main () :
    return ChainEP_Widget ()
