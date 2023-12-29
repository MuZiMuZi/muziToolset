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
from ..setup import chain_ui
from ..widget import base_widget
from ....bind.module.base import base
from ....bind.module.chain import chainFK , chainIK , chainIKFK


reload (base_widget)
reload (base)
reload (chain_ui)
reload (chainFK)
reload (chainIK)
reload (chainIKFK)


class Chain_Widget (chain_ui.Ui_MainWindow , base_widget.Base_Widget , QMainWindow) :
    # 添加其他模块类型
    chain_modules = {
        'chainFK' : chainFK.ChainFK ,
        'chainIK' : chainIK.ChainIK ,
        'chainIKFK' : chainIKFK.ChainIKFK ,

    }


    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        # 返回组件的参数
        self.length = None
        self.direction = None
        super ().__init__ (parent , *args , **kwargs)


    def init_base (self) :
        # 继承base_widget.Base_Widget的init_base方法
        super ().init_base ()
        for direciton in config.Direction :
            self.direction_cbox.addItem (str (direciton.value))


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

        # 将以上参数也添加到self.base_parameters 里，后续判断这些参数是否有值
        self.base_parameters.append (self.length , self.direction)


    def build_setup (self) :
        # 根据self.module来判断是需要生成哪个模块的绑定
        if self.module in self.chain_modules :
            module_class = self.chain_modules [self.module]
            self.setup = module_class (self.side , self.name , self.jnt_number , self.direction , self.length ,
                                       self.jnt_parent , self.ctrl_parent)

            self.setup.build_setup ()


    # 根据base_widget和extra_widget返回的参数,创建绑定系统
    def build_rig (self) :
        # 根据self.module来判断是需要生成哪个模块的绑定
        if self.module in self.chain_modules :
            module_class = self.chain_modules [self.module]
            self.rig = module_class (self.side , self.name , self.jnt_number , self.direction , self.length ,
                                     self.jnt_parent , self.ctrl_parent)
            self.rig.build_rig ()


    ## 根据self.module来判断是需要删除哪个模块的绑定
    def delete_rig (self) :
        # 根据self.module来判断是需要删除哪个模块的绑定
        if self.module in self.chain_modules :
            module_class = self.chain_modules [self.module]
            self.delete = module_class (self.side , self.name , self.jnt_number , self.direction , self.length ,
                                        self.jnt_parent , self.ctrl_parent)
            self.delete.delete_rig ()


def main () :
    return Chain_Widget ()
