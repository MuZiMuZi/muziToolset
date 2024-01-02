# coding=utf-8
# 导入所有需要的模块
from importlib import reload

import maya.cmds as cmds
from PySide2.QtWidgets import *

from . import chain_widget
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
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        super ().__init__ (parent , *args , **kwargs)


    def parse_base (self) :
        super ().parse_base ()
        # 分析ikfk控制器是否创建的参数并返回
        self.ikCtrl_value = self.ikCtrl_cbox.value ()
        self.fkCtrl_value = self.fkCtrl_cbox.value ()
        # 分析是否需要拉伸的参数并返回
        self.stretch_value = self.stretch_cbox.value ()

        # 分析ribbon关节的参数并返回
        self.up_ribbon_value = self.up_ribbon_sbox.value ()
        self.down_ribbon_value = self.down_ribbon_sbox.value ()


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
