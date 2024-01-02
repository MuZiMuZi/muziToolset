# coding=utf-8
# 导入所有需要的模块
from importlib import reload

import maya.cmds as cmds
from PySide2.QtWidgets import *

from . import base_widget
from ..setup import limb_ui
from ... import config
from ....bind.subject.body_subject import arm,leg,spine
from ....core import pipelineUtils


reload (limb_ui)
reload (base_widget)


class Limb_Widget (limb_ui.Ui_MainWindow , base_widget.Base_Widget , QMainWindow) :
    # # 添加其他模块类型
    limb_modules = {
        'arm' : arm.Arm ,
        'leg' : leg.Leg ,
        'spine' : spine.Spine ,

    }


    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        # 针对身体四肢模块的绑定模块
        rigtype_limb = ['arm' , 'leg' , 'spine']
         # 组件需要的参数有[side,name,jnt_number,ikctrl_value,fkctrl_value,stretch_value,up_ribbon_value,down_ribbon_value,jnt_parent,ctrl_parent]
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        super ().__init__ (parent , *args , **kwargs)


    def parse_base (self) :
        super ().parse_base ()



    def build_setup (self) :
        # 根据self.module来判断是需要生成哪个模块的绑定
        if self.limb in self.limb_modules :
            limb_class = self.chain_modules [self.module]
            self.limb = limb_class (self.side , self.name , self.jnt_number , self.direction , self.length ,
                                        self.jnt_parent , self.ctrl_parent)


def main () :
    return Chain_Widget ()


def main () :
    return Limb_Widget ()
