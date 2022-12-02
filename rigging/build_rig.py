# coding=utf-8

u"""
这是一个用来生成自动绑定系统的类，之前所有的类都是为这个类服务的。

继承了base_rig

目前已有的功能：

build： 根据导入的对应模块，生成绑定系统
"""

import muziToolset.rigging.base_rig as base_rig
import muziToolset.rigging.arm_rig as arm_rig
import muziToolset.rigging.foot_rig as foot_rig
import muziToolset.rigging.neck_rig as neck_rig
import muziToolset.rigging.spine_rig as spine_rig
import muziToolset.rigging.chest_rig as chest_rig
import muziToolset.rigging.leg_rig as leg_rig
import muziToolset.rigging.hand_rig as hand_rig

import maya.cmds as cmds

# 手臂的关节定向是-z

class Build_Rig(base_rig.Base_Rig):
    def __init__(self):
        super(Build_Rig, self).__init__()
        # 定义各个绑定模块的路径
        skeletonPath = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton'

        troll_model = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/model/troll_model.ma'
        biped_skeleton = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/biped_skeleton.ma'

        self.arm_rig_path = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/arm_rig.ma'
        self.hand_rig_path = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/hand_rig.ma'
        self.leg_rig_path = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/leg_rig.ma'
        self.foot_rig_path = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/foot_rig.ma'
        self.neck_rig_path = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/neck_rig.ma'
        self.spine_rig_path = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/spine_rig.ma'
        self.chest_rig_path = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/chest_rig.ma'

        self.modular_rig_path_list = [self.arm_rig_path, self.hand_rig_path, self.leg_rig_path, self.foot_rig_path, self.foot_rig_path, self.neck_rig_path, self.spine_rig_path,self.chest_rig_path]
    def import_modular (self,modular_rig_list):
        u'''
        绑定生成的预设步骤，导入对应的模型和关节结构
        '''
        # 导入模块结构
        if 'neck_rig' in modular_rig_list :
            cmds.file(self.neck_rig_path, i = True)
        if 'spine_rig' in modular_rig_list:
            cmds.file(self.spine_rig_path, i = True)
        if 'chest_rig' in modular_rig_list:
            cmds.file(self.chest_rig_path, i = True)
        if 'arm_rig' in modular_rig_list:
            cmds.file(self.arm_rig_path, i = True)
        if 'hand_rig' in modular_rig_list:
            cmds.file(self.hand_rig_path, i = True)
        if 'leg_rig' in modular_rig_list:
            cmds.file(self.leg_rig_path, i = True)
        if 'leg_rig' in modular_rig_list:
            cmds.file(self.foot_rig_path, i = True)


    def claer_modular(self):
        cmds.delete(self.group)
        for modular in self.modular_rig_list:
            if cmds.objExists(modular):
                cmds.delete(modular)
    def build_rig(self):
        u'''
        根据导入的对应模块，生成绑定系统
        '''
        if self.chest_rig:
            chest = chest_rig.Chest_Rig(bp_joints = None, joint_parent = None, control_parent = 'output_m_cog_001')
            chest.create_chest_rig()
        if self.spine_rig:
            spine = spine_rig.Spine_Rig(bp_joints = None, joint_parent = None, control_parent = None, mirror = False)
            spine.create_spine_rig()

        if self.arm_rig:
            arm = arm_rig.Arm_Rig(bp_joints = None, joint_parent = None, control_parent = 'output_l_scapula_001', mirror = cmds.getAttr(self.arm_rig + '.mirror'),
                                  ribbon =  cmds.getAttr(self.arm_rig + '.ribbonRig'),joint_number = cmds.getAttr(self.arm_rig + '.ribbonJntNumber'),
                                  space_list = ['world', 'cog', 'chest'] )
            arm.create_arm_rig()

        if self.leg_rig:
            leg = leg_rig.Leg_Rig(bp_joints = None, joint_parent = None, control_parent = None, mirror = cmds.getAttr(self.leg_rig + '.mirror'),
                                  ribbon =  cmds.getAttr(self.leg_rig + '.ribbonRig'),joint_number = cmds.getAttr(self.leg_rig + '.ribbonJntNumber'),
                                  space_list = ['world', 'cog', 'spine'])
            leg.create_leg_rig()

        if self.neck_rig:
            neck = neck_rig.Neck_Rig(bp_joints = None, joint_parent = None, control_parent = None, mirror = False)
            neck.create_neck_rig()

        if self.foot_rig:
            foot = foot_rig.Foot_Rig(bp_joints = None, joint_parent = None, control_parent = None, mirror = True)
            foot.create_footIK_rig('l')
            foot.create_footIK_rig('r')

        if self.hand_rig:
            hand = hand_rig.Hand_Rig(bp_joints = None, joint_parent = None, control_parent = None, mirror = True)
            hand.create_hand_rig()

        cmds.delete( self.spine_rig, self.arm_rig, self.leg_rig, self.neck_rig,self.foot_rig,
                    self.hand_rig)
        cmds.parent(self.chest_rig,self.joint)