# coding=utf-8

u"""
这是一个用来编写chest（胸部）绑定的类，之后的绑定都会在这个类的基础上逐级继承下去
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


import ikfk_rig


chest_bp_joints = ['bpjnt_l_shoulder_001', 'bpjnt_l_elbow_001',' bpjnt_l_wrist_001']

class Chest_Rig(ikfk_rig.IKFK_Rig):
    def __init__(self, bp_joints = None , joint_parent = None, control_parent = None):
        super(Chest_Rig, self).__init__(bp_joints = bp_joints, joint_parent=joint_parent,control_parent = control_parent)
        # self.chest_bp_joints = self.get_modular_bp_joints(self.chest_rig)
        # self.bp_joints = self.chest_bp_joints
        self.bp_clavicle_jnt = ['bpjnt_l_clavicle_001']
        self.bp_scapula_jnt = 'bpjnt_l_scapula_001'
        self.bp_shrug_jnt = 'bpjnt_l_shrug_001'


    def create_chest_rig(self):
        self.create_ikfk_chain_rig()
        if self.ribbon  == True:
            self.create_ribbon_Rig(self.ikfk_chain,self.control_parent, self.joint_number)
            self.create_ribbon_Rig(self.ikfk_chain_mirror, self.control_parent_mirror, self.joint_number)

    def chest_rig(self):
        # 创建锁骨的控制器
        clavicle_ctrl = self.bp_clavicle_jnt.replace('bpjnt_','ctrl_')
        clavicle_ctrl_obj = controlUtils.Control.create_ctrl(clavicle_ctrl, shape = 'clavicle', radius = 13, axis = 'Z+',
                                                            pos = self.bp_clavicle_jnt, parent = None)
        # 创建肩胛骨的控制器
        shrug_ctrl = self.bp_scapula_jnt.replace('bpjnt_', 'ctrl_')
        scapula_ctrl_obj = controlUtils.Control.create_ctrl(shrug_ctrl,
                                                         shape = 'Cube', radius = 6, axis = 'Z+',
                                                         pos = self.bp_scapula_jnt, parent = None)

        # 创建肩膀耸肩的控制器
        shrug_ctrl = self.bp_shrug_jnt.replace('bpjnt_', 'ctrl_')
        shrug_ctrl_obj = controlUtils.Control.create_ctrl(shrug_ctrl,
                                                         shape = 'shrug', radius = 6, axis = 'X+',
                                                         pos = None, parent = None)

        cmds.matchTransform(shrug_ctrl.replace('ctrl_','zero_'),self.bp_shrug_jnt,position = True)








