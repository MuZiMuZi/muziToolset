# coding=utf-8
# 导入所有需要的模块

from importlib import reload

from PySide2.QtWidgets import *

from . import bone_widget
from ..setup import base_ui
from ....bind.module.base import base


reload (bone_widget)
reload (base)
reload (base_ui)


class Base_Widget (base_ui.Ui_MainWindow , bone_widget.Bone_Widget , QMainWindow) :


    def __init__ (self , parent = None , *args , **kwargs) :
        super ().__init__ (parent , *args , **kwargs)
        self.jnt_number = 1


    # 分析组件里额外的输入内容输入并将其作为参数返回
    def parse_extra (self) :
        '''
        分析组件里额外的输入内容输入并将其作为参数返回
        '''
        # 组件需要给定数值的输入，
        self.base_parameters = [self.side]


    # 创建实例化的对象,然后生成对应的bp定位关节
    def build_setup (self) :
        # 创建实例化的对象
        self.module = base.Base (self.side , self.name , self.jnt_number,self.jnt_parent , self.ctrl_parent)
        self.module.build_setup ()


    # 根据base_widget和extra_widget返回的参数,创建绑定系统
    def build_rig (self) :
        # 删除已经创建好的绑定系统
        self.module.build_rig ()


    # 删除已经创建好的绑定系统
    def delete_rig (self) :
        self.module.delete_rig ()


def main () :
    return Base_Widget ()
