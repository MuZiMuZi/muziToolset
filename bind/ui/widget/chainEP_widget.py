# coding=utf-8
# 导入所有需要的模块
from importlib import reload

import maya.cmds as cmds
from PySide2.QtWidgets import *

from . import chain_widget
from ..setup import chainEP_ui
from ....bind.module.chain import chainEP
from ....core import pipelineUtils


reload (chain_widget)
reload (chainEP_ui)
reload (chainEP)
reload (pipelineUtils)


class ChainEP_Widget (chainEP_ui.Ui_MainWindow , chain_widget.Chain_Widget , QMainWindow) :


    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        # 针对EP曲线关节链条的绑定模块，
        # 组件需要的参数有[side,name,jnt_number,ctrl_number,curve,jnt_parent,ctrl_parent]
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        # 返回组件的参数
        self.length = None
        self.direction = None
        super ().__init__ (parent , *args , **kwargs)


    # 用来添加连接的槽函数
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


    # 分析组件里额外的输入内容输入并将其作为参数返回
    def parse_extra (self) :
        '''
        分析组件里额外的输入内容输入并将其作为参数返回
        '''
        # 分析组件里额外的输入内容输入
        self.jnt_number = self.jnt_number_sbox.value ()
        self.ctrl_number = self.ctrl_number_sbox.value ()
        self.curve = self.curve_Edit.text ()

        # 将需要检查参数存在的值封装到列表中
        parameters_to_add = [self.jnt_number , self.ctrl_number , self.curve]

        # 使用 extend() 方法将列表添加到 base_parameters 中，后续通过check_parameters这个方法判断这些参数是否有值
        self.base_parameters.extend (parameters_to_add)


    # # 判断给定的参数是否正确,如果正确的话才进行之后的创建
    def check_parameters (self) :
        super ().check_parameters ()
        # 判断给定的参数是否正确,如果正确的话才进行之后的创建
        if self.ctrl_number < 2 :
            cmds.warning (u"请有足够的控制点")
            raise ValueError (u"请有足够的控制点")
        if self.ctrl_number > self.jnt_number :
            cmds.warning (u"控制器的数量请小于关节的数量")
            raise ValueError (u"控制器的数量请小于关节的数量")

        if not self.curve :
            cmds.warning (u"请给定需要创建控制器和关节的曲线")
            raise ValueError (u"请给定需要创建控制器和关节的曲线")

        self.is_info_base = True
        return self.is_info_base


    # 创建绑定的定位关节
    def build_setup (self) :
        # 创建绑定准备，生成定位关节
        self.chainEP = chainEP.ChainEP (self.side , self.name , self.jnt_number , self.ctrl_number , self.curve ,
                                        self.jnt_parent , self.ctrl_parent)
        self.chainEP.build_setup ()


    # 创建完整的绑定
    def build_rig (self) :
        # 创建完整的绑定
        self.chainEP.build_rig ()


    # 删除创建好的绑定
    def delete_rig (self) :
        # 删除绑定
        self.chainEP.delete_rig ()


def main () :
    return Chain_Widget ()


def main () :
    return ChainEP_Widget ()
