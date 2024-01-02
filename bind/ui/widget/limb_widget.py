# coding=utf-8
# 导入所有需要的模块
from importlib import reload

from PySide2.QtWidgets import *

from . import chain_widget
from ..setup import limb_ui
from ....bind.subject.body_subject import arm , leg , spine


reload (limb_ui)
reload (chain_widget)


class Limb_Widget (limb_ui.Ui_MainWindow , chain_widget.Chain_Widget , QMainWindow) :
    # # 添加其他模块类型
    limb_modules = {
        'arm' : arm.Arm ,
        'leg' : leg.Leg ,
        'spine' : spine.Spine ,

    }


    def __init__ (self , parent = None , *args , **kwargs) :
        '''
        # 针对身体四肢模块的绑定模块
        rigType_limb = ['arm' , 'leg' , 'spine']
         # 组件需要的参数有[side,name,jnt_number,ikctrl_value,fkctrl_value,stretch_value,up_ribbon_value,down_ribbon_value,jnt_parent,ctrl_parent]
        使用设置初始化QListWidgetItem，如名称和图标，以及初始化base、额外的widget对象和ui文件，也对应要构建的绑定组件对象

        '''
        super ().__init__ (parent , *args , **kwargs)





    # 分析组件里额外的输入内容输入并将其作为参数返回
    def parse_extra (self) :
        '''
        分析组件里额外的输入内容输入并将其作为参数返回
        '''
        #分析组件里额外的输入内容输入并将其作为参数返回
        self.length = self.length_sbox.value ()

        # 传递参数时，参数本身是一个包含字符串的元组 ('[0, 1, 0]',)，而不是一个包含数字的列表 [0, 1, 0]。因此使用eval方法将其解析成为一个列表
        self.direction = eval (self.direction_cbox.currentText ())

        # 根据self.rigType来判断是哪个模块的绑定
        self.rigType = self.rigType_edit.text ()
        
        # 获取是否设置ik控制器的值
        self.ikCtrl_value = self.ikCtrl_cbox.isChecked ()

        # 获取是否设置fk控制器的值
        self.fkCtrl_value = self.fkCtrl_cbox.isChecked ()

        # 获取是否设置拉伸的值
        self.stretch_value = self.stretch_cbox.isChecked ()

        # 获取设置上部分ribbon关节的数量
        self.up_ribbon_value = self.up_ribbon_sbox.value ()

        # 获取设置下部分ribbon关节的数量
        self.down_ribbon_value = self.down_ribbon_sbox.value ()

        # 将需要检查参数存在的值封装到列表中
        parameters_to_add = [self.length,self.direction,self.up_ribbon_value , self.down_ribbon_value]

        # 使用 extend() 方法将列表添加到 base_parameters 中，后续通过check_parameters这个方法判断这些参数是否有值
        self.base_parameters.extend (parameters_to_add)


    def build_setup (self) :
        # 根据self.rigType来判断是需要生成哪个模块的绑定
        if self.limb in self.limb_modules :
            limb_class = self.limb_modules [self.limb]
            self.limb = limb_class (self.side , self.name , self.jnt_number , self.direction , self.length ,
                                    self.jnt_parent , self.ctrl_parent)


    # 根据返回的参数,创建绑定系统
    def build_rig (self) :
        # 创建绑定
        self.limb.build_rig ()


    ## 删除绑定
    def delete_rig (self) :
        # 删除绑定
        self.limb.delete_rig ()


def main () :
    return Chain_Widget ()


def main () :
    return Limb_Widget ()
