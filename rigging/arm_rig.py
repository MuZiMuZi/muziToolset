# coding=utf-8

u"""
这是一个用来编写arm（手臂）绑定的类，之后的绑定都会在这个类的基础上逐级继承下去
继承了ikfk_rig

目前已有的功能：

create_arm_rig：创建手臂的控制器绑定



"""

import maya.cmds as cmds
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.pipelineUtils as pipelineUtils

import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.jointUtils as jointUtils

reload(pipelineUtils)
reload(jointUtils)

import ikfk_rig


arm_bp_joints = ['bpjnt_l_shoulder_001', 'bpjnt_l_elbow_001',' bpjnt_l_wrist_001']

class Arm_Rig(ikfk_rig.IKFK_Rig):
    def __init__(self, bp_joints = None , joint_parent = None, control_parent = None,mirror = True,ribbon = True,joint_number = 5):
        super(Arm_Rig, self).__init__(bp_joints = bp_joints, joint_parent=joint_parent,control_parent = control_parent)
        self.mirror = mirror
        self.arm_bp_joints = self.get_modular_bp_joints(self.arm_rig)
        self.bp_joints = self.arm_bp_joints
        self.ribbon = ribbon
        self.joint_number = joint_number


    def create_arm_rig(self):
        self.create_ikfk_chain_rig()
        if self.ribbon  == True:
            self.ribbon_Rig(self.ikfk_chain,self.control_parent, self.joint_number)
            self.ribbon_Rig(self.ikfk_chain_mirror, self.control_parent_mirror, self.joint_number)
