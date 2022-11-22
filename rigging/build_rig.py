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



class Build_Rig(base_rig.Base_Rig):
    def __init__(self):
        super(Build_Rig, self).__init__()
        # 定义各个绑定模块的路径
        skeletonPath = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton'

        troll_model = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/model/troll_model.ma'
        biped_skeleton = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/biped_skeleton.ma'

        arm_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/arm_rig.ma'
        hand_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/hand_rig.ma'
        leg_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/leg_rig.ma'
        foot_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/foot_rig.ma'
        neck_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/neck_rig.ma'
        spine_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/spine_rig.ma'
        chest_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/chest_rig.ma'

        self.modular_rig_list = [arm_rig, hand_rig, leg_rig, foot_rig, neck_rig, spine_rig, chest_rig]
    def import_modular (self):
        u'''
        绑定生成的预设步骤，导入对应的模型和关节结构
        '''
        # 导入模块结构
        for modular in self.modular_rig_list:
            cmds.file(modular, i = True)

    def delete_modular(self):
        cmds.delete(self.chest_rig, self.spine_rig, self.arm_rig, self.leg_rig, self.neck_rig, self.foot_rig,
                    self.hand_rig)
    def build_rig(self):
        u'''
        根据导入的对应模块，生成绑定系统
        '''
        if self.chest_rig:
            chest = chest_rig.Chest_Rig(bp_joints = None, joint_parent = None, control_parent = None)
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

        self.delete_modular()
