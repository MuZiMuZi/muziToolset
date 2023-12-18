# coding=utf,8
'''
嘴巴的绑定系统创建
'''
from importlib import reload

import maya.cmds as cmds

from . import mouthLip
from ...module.base import base
from ....core import controlUtils , pipelineUtils


reload (mouthLip)
reload (base)


class Mouth (base.Base) :


    def __init__ (self , side , name , joint_number = 7 , joint_parent = None , control_parent = None) :
        super ().__init__ (side , name , joint_number , joint_parent , control_parent)

        self.rtype = 'Mouth'
        # 生成上部分的嘴唇
        self.mouth_lip_upper = mouthLip.MouthLip (side = self.side , name = 'upper' , joint_number = 10,
                                                  joint_parent = None ,
                                                  control_parent = None)

        # 生成下部分的嘴唇
        self.mouth_lip_lower = mouthLip.MouthLip (side = self.side , name = 'lower' , joint_number = 10 ,
                                                  joint_parent = None ,
                                                  control_parent = None)


    def create_namespace (self) :
        super ().create_namespace ()
        self.mouth_lip_upper.create_namespace ()
        self.mouth_lip_lower.create_namespace ()
        ## 创建嘴内侧和嘴外侧的控制器
        self.inn_ctrl = 'ctrl_{}_{}{}Inn_001'.format (self.side , self.name , self.rtype)
        self.out_ctrl = 'ctrl_{}_{}{}Out_001'.format (self.side , self.name , self.rtype)


    def create_bpjnt (self) :
        # 创建上下嘴唇的控制器曲线
        self.mouth_lip_upper.build_curve ()
        self.mouth_lip_lower.build_curve ()


    def create_joint (self) :
        # 创建上下嘴唇的曲线
        self.mouth_lip_upper.create_joint ()
        self.mouth_lip_lower.create_joint ()


    def create_ctrl (self) :
        # 创建整体的控制器层级组
        self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.control_parent)
        # 创建上下嘴唇的控制器
        self.mouth_lip_upper.create_ctrl ()
        self.mouth_lip_lower.create_ctrl ()

        # 创建嘴内侧与嘴外侧的控制器

        self.inn_ctrl = controlUtils.Control.create_ctrl (self.inn_ctrl , shape = 'ball' , axis = 'X+' , radius = 1,
                                                          pos = self.mouth_lip_upper.zero_list [0] ,
                                                          parent = self.ctrl_grp)
        self.out_ctrl = controlUtils.Control.create_ctrl (self.out_ctrl , shape = 'ball' , axis = 'X+' , radius = 1 ,
                                                          pos = self.mouth_lip_upper.zero_list [-1] ,
                                                          parent = self.ctrl_grp)

        # 整理控制器的层级结构
        cmds.parent (self.mouth_lip_upper.ctrl_grp , self.mouth_lip_lower.ctrl_grp , self.ctrl_grp)


    def add_constraint (self) :
        # 创建上下嘴唇的约束
        self.mouth_lip_upper.add_constraint ()
        self.mouth_lip_lower.add_constraint ()

        # # 嘴角内侧控制器对上下嘴唇的内侧控制器做约束
        cmds.parentConstraint (self.inn_ctrl.replace ('ctrl' , 'output') , self.mouth_lip_upper.driven_list [0] ,
                               mo = True)
        cmds.parentConstraint (self.inn_ctrl.replace ('ctrl' , 'output') , self.mouth_lip_lower.driven_list [0] ,
                               mo = True)

        # # 隐藏上下嘴唇的内侧控制器
        cmds.setAttr(self.mouth_lip_upper.zero_list[0] + '.visibility' , 0)
        cmds.setAttr(self.mouth_lip_lower.zero_list[0] + '.visibility' , 0)
        # 嘴角外侧控制器对上下嘴唇的外侧控制器做约束
        cmds.parentConstraint (self.out_ctrl.replace ('ctrl' , 'output') , self.mouth_lip_upper.driven_list [-1] ,
                               mo = True)
        cmds.parentConstraint (self.out_ctrl.replace ('ctrl' , 'output') , self.mouth_lip_lower.driven_list [-1] ,
                               mo = True)
        # # 隐藏上下嘴唇的外侧控制器
        cmds.setAttr(self.mouth_lip_upper.zero_list[-1] + '.visibility' , 0)
        cmds.setAttr(self.mouth_lip_lower.zero_list[-1] + '.visibility' , 0)
        #
        # 添加拉链嘴的绑定效果
        self.add_zip_lip ()


    def add_zip_lip (self) :
        u"""
        添加拉链嘴的绑定
        """
        lip_ctrls = [self.inn_ctrl , self.out_ctrl]
        jaw_ctrl = self.inn_ctrl
        upper_jnts = self.mouth_lip_upper.skin_jnt_list
        lower_jnts = self.mouth_lip_lower.skin_jnt_list

        self.zip_lip_dict = pipelineUtils.Pipeline.create_zip_lip (lip_ctrls , jaw_ctrl , upper_jnts , lower_jnts ,
                                                                   zip_height = 0.5 ,
                                                                   falloff = 3)
        cmds.parent (self.zip_lip_dict ['node_grp'] , self.node_grp)


if __name__ == '__main__' :
    def build_setup () :
        mouth_m = mouth.Mouth (side = 'm' , name = '' , joint_number = 2 , joint_parent = None ,
                               control_parent = None)
        mouth_m.build_setup ()


    def build_rig () :
        mouth_m = mouth.Mouth (side = 'm' , name = '' , joint_number = 2 , joint_parent = None ,
                               control_parent = None)
        mouth_m.build_rig ()


    #
    build_setup ()
    build_rig ()
