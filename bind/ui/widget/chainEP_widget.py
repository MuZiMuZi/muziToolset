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
from ... import config
from ..setup import chainEP_ui
from . import chain_widget
from importlib import reload
from ....bind.module.chain import chainEP
import maya.cmds as cmds
from ....core import pipelineUtils


reload (chain_widget)
reload (chainEP_ui)
reload (chainEP)
reload (pipelineUtils)


class ChainEP_Widget (chainEP_ui.Ui_MainWindow , chain_widget.Chain_Widget , QMainWindow) :


    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        # 返回组件的参数
        self.length = None
        self.direction = None
        super ().__init__ (parent , *args , **kwargs)

    #初始化参数
    def init_base (self) :
        # 继承base_widget.Base_Widget的init_base方法
        # 初始化参数
        for side in config.Side :
            self.side_cbox.addItem (side.value)

    #用来添加连接的槽函数
    def add_connect (self) :
        u"""
        用来添加连接的槽函数
        """
        super ().add_connect ()
        self.curve_btn.clicked.connect (self.clicked_curve_btn)


    # 用来连接单击选择曲线按钮的槽函数
    def clicked_curve_btn (self) :
        """
        用来连接单击选择曲线按钮的槽函数，当用户点击这个曲线拾取按钮的时候拾取选择的曲线添加到self.curve_edit里
        """
        # 获取选择的物体
        selected_object = pipelineUtils.Pipeline.get_selected_type (type = 'transform')

        if not selected_object :
            cmds.warning ('请选择用来创建控制器和关节的曲线')
            return

        # 从选择的物体，找到曲线形状节点
        shapes = cmds.listRelatives (selected_object , shapes = True)

        for shape in shapes :
            if cmds.objectType (shape) == 'nurbsCurve' :
                # 设置曲线名称到文本编辑框
                self.curve_Edit.setText (selected_object)
                cmds.warning ('已将曲线 {} 设置为用来创建控制器和关节的曲线'.format (selected_object))
                return  # 如果找到曲线就结束循环

    #分析base_widget中的输入并将其作为参数返回
    def parse_base (self , *args) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        # 获取用户输入的参数并将其返回
        self.side = self.side_cbox.currentText ()
        self.name = self.name_edit.text ()
        self.jnt_number = self.jnt_number_sbox.value ()
        self.ctrl_number = self.ctrl_number_sbox.value ()
        self.curve = self.curve_Edit.text ()
        self.jnt_parent = self.jnt_parent_edit.text ()
        self.ctrl_parent = self.ctrl_parent_edit.text ()

        # 判断给定的参数是否正确,如果正确的话才进行之后的创建
        if self.ctrl_number < 2 :
            raise ValueError (u"请有足够的控制点")
            cmds.warning (u"请有足够的控制点")
        if self.ctrl_number > self.jnt_number :
            raise ValueError (u"控制器的数量请小于关节的数量")
            cmds.warning (u"控制器的数量请小于关节的数量")
        if not self.curve :
            raise ValueError (u"请给定需要创建控制器和关节的曲线")
            cmds.warning (u"请给定需要创建控制器和关节的曲线")

        # 组件需要给定数值的输入，
        self.base_parameters = [self.side , self.jnt_number, self.ctrl_number,self.curve]
        

    #创建绑定
    def build_setup (self) :
        # 创建绑定准备，生成定位关节
        self.chainEP = chainEP.ChainEP (self.side , self.name , self.jnt_number , self.ctrl_number , self.curve ,
                                      self.jnt_parent , self.ctrl_parent)
        self.chainEP.build_setup ()


    def build_rig (self) :
        # 创建完整的绑定
        self.chainEP.build_rig ()


def main () :
    return Chain_Widget ()


def main () :
    return ChainEP_Widget ()
