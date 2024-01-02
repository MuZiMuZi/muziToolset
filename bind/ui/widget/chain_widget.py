# coding=utf-8
# 导入所有需要的模块
from importlib import reload

from PySide2.QtWidgets import *

from ..setup import chain_ui
from ..widget import base_widget
from ... import config
from ....bind.module.base import base
from ....bind.module.chain import chainFK , chainIK , chainIKFK
from ....bind.subject.body_subject import finger


reload (base_widget)
reload (base)
reload (chain_ui)
reload (chainFK)
reload (chainIK)
reload (chainIKFK)
reload (finger)


class Chain_Widget (chain_ui.Ui_MainWindow , base_widget.Base_Widget , QMainWindow) :
    # 添加其他模块类型
    chain_modules = {
        'chainFK' : chainFK.ChainFK ,
        'chainIK' : chainIK.ChainIK ,
        'chainIKFK' : chainIKFK.ChainIKFK ,
        'finger' : finger.Finger

    }


    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        # 返回组件的参数
        self.length = None
        self.direction = None
        super ().__init__ (parent , *args , **kwargs)


    # 初始化参数
    def init_base (self) :
        # 继承base_widget.Base_Widget的init_base方法
        super ().init_base ()
        # 添加轴向的参数的初始化
        for direciton in config.Direction :
            self.direction_cbox.addItem (str (direciton.value))


    # 分析base_widget中的输入并将其作为参数返回
    def parse_base (self , *args) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        super ().parse_base ()
        self.length = self.length_sbox.value ()

        # 传递参数时，参数本身是一个包含字符串的元组 ('[0, 1, 0]',)，而不是一个包含数字的列表 [0, 1, 0]。因此使用eval方法将其解析成为一个列表
        self.direction = eval (self.direction_cbox.currentText ())

        # 根据self.module来判断是哪个模块的绑定
        self.module = self.module_edit.text ()

        # 将两个参数封装到列表中
        parameters_to_add = [self.length , self.direction , self.module]

        # 使用 extend() 方法将列表添加到 base_parameters 中，后续通过check_parameters这个方法判断这些参数是否有值
        self.base_parameters.extend (parameters_to_add)


    # 判断是需要生成哪个模块的绑定
    def build_setup (self) :
        # 根据self.module来判断是需要生成哪个模块的绑定
        if self.module in self.chain_modules :
            module_class = self.chain_modules [self.module]
            self.module = module_class (self.side , self.name , self.jnt_number , self.direction , self.length ,
                                        self.jnt_parent , self.ctrl_parent)

            self.module.build_setup ()


    # 根据base_widget和extra_widget返回的参数,创建绑定系统
    def build_rig (self) :
        # 创建绑定
        self.module.build_rig ()


    ## 删除绑定
    def delete_rig (self) :
        # 删除绑定
        self.module.delete_rig ()


def main () :
    return Chain_Widget ()
