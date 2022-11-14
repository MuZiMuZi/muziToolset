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
import muziToolset.rigging.leg_rig as leg_rig
import muziToolset.rigging.hand_rig as hand_rig

import maya.cmds as cmds



class Build_Rig(base_rig.Base_Rig):
    def __init__(self):
        super(Build_Rig, self).__init__()
        self.setup()
    def build(self):
        u'''
        根据导入的对应模块，生成绑定系统
        '''
        if self.arm_rig:
            arm = arm_rig.Arm_Rig(bp_joints = None, joint_parent = None, control_parent = None, mirror = cmds.getAttr(self.arm_rig + '.mirror'),
                                  ribbon =  cmds.getAttr(self.arm_rig + '.ribbonRig'),joint_number = cmds.getAttr(self.arm_rig + '.ribbonJntNumber'))
            arm.create_arm_rig()
        if self.leg_rig:
            leg = leg_rig.Leg_Rig(bp_joints = None, joint_parent = None, control_parent = None, mirror = cmds.getAttr(self.leg_rig + '.mirror'),
                                  ribbon =  cmds.getAttr(self.leg_rig + '.ribbonRig'),joint_number = cmds.getAttr(self.leg_rig + '.ribbonJntNumber'))
            leg.create_leg_rig()

        if self.spine_rig:
            spine = spine_rig.Spine_Rig(bp_joints = None, joint_parent = None, control_parent = None, mirror = False)
            spine.create_spine_rig()

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

        for modular in self.modular_rig_list:
            cmds.parent(modular, self.modular_rig)