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



class Arm_Rig(ikfk_rig.IKFK_Rig):
    def __init__(self, bp_joints = None , joint_parent = None, control_parent = None,mirror = True,ribbon = True,joint_number = 5,space_list = None):
        super(Arm_Rig, self).__init__(bp_joints = bp_joints, joint_parent=joint_parent,control_parent = control_parent,space_list =space_list)
        self.mirror = mirror
        self.arm_bp_joints = ['bpjnt_l_shoulder_001', 'bpjnt_l_elbow_001',' bpjnt_l_wrist_001']
        self.bp_joints = self.arm_bp_joints
        self.ribbon = ribbon
        self.joint_number = joint_number
        self.clavicle_jnt = 'jnt_l_clavicle_001'
        self.scapula_jnt = 'jnt_l_scapula_001'
        self.shrug_jnt = 'jnt_l_shrug_001'
        self.clavicle_mirror = cmds.mirrorJoint(self.clavicle_jnt, mirrorYZ = True, mirrorBehavior = True,
                                                 searchReplace = ['_l_', '_r_'])



    def create_arm_rig(self):
        # 创建锁骨的控制器
        clavicle_ctrl = self.clavicle_jnt.replace('jnt_','ctrl_')
        clavicle_ctrl_obj = controlUtils.Control.create_ctrl(clavicle_ctrl, shape = 'clavicle', radius = 13, axis = 'Z+',
                                                            pos = self.clavicle_jnt, parent ='output_m_chest_001')
        # 创建肩胛骨的控制器
        scapula_ctrl = self.scapula_jnt.replace('jnt_', 'ctrl_')
        scapula_ctrl_obj = controlUtils.Control.create_ctrl(scapula_ctrl,
                                                         shape = 'Cube', radius = 6, axis = 'Z+',
                                                         pos = None, parent = clavicle_ctrl.replace('ctrl_','output_'))
        cmds.matchTransform(scapula_ctrl.replace('ctrl_', 'zero_'), self.scapula_jnt, position = True)

        # 创建肩膀耸肩的控制器
        shrug_ctrl = self.shrug_jnt.replace('jnt_', 'ctrl_')
        shrug_ctrl_obj = controlUtils.Control.create_ctrl(shrug_ctrl,
                                                         shape = 'shrug', radius = 8, axis = 'X+',
                                                         pos = None, parent ='output_m_chest_001')

        cmds.matchTransform(shrug_ctrl.replace('ctrl_','zero_'),self.shrug_jnt,position = True)

        # 创建镜像锁骨的控制器
        clavicle_ctrl_mirror = clavicle_ctrl.replace('_l_','_r_')
        clavicle_ctrl_mirror_obj = controlUtils.Control.create_ctrl(clavicle_ctrl_mirror, shape = 'clavicle', radius = 13, axis = 'Z+',
                                                            pos = self.clavicle_jnt.replace('_l_','_r_'), parent = 'output_m_chest_001')
        cmds.setAttr(clavicle_ctrl_mirror.replace('ctrl_','offset_') + '.scaleX',-1)
        cmds.setAttr(clavicle_ctrl_mirror.replace('ctrl_', 'offset_') + '.scaleY', -1)
        cmds.setAttr(clavicle_ctrl_mirror.replace('ctrl_', 'offset_') + '.scaleZ', -1)
        # 创建镜像肩胛骨的控制器
        scapula_ctrl_mirror = scapula_ctrl.replace('_l_','_r_')
        scapula_ctrl_mirror_obj = controlUtils.Control.create_ctrl(scapula_ctrl_mirror,
                                                         shape = 'Cube', radius = 6, axis = 'Z+',
                                                         pos = None, parent = clavicle_ctrl_mirror.replace('ctrl_','output_'))
        cmds.matchTransform(scapula_ctrl_mirror.replace('ctrl_', 'zero_'), self.scapula_jnt.replace('_l_','_r_'), position = True)

        # 创建镜像肩膀耸肩的控制器
        shrug_ctrl_mirror = shrug_ctrl.replace('_l_','_r_')
        shrug_ctrl_mirror_obj = controlUtils.Control.create_ctrl(shrug_ctrl_mirror,
                                                         shape = 'shrug', radius = 8, axis = 'X+',
                                                         pos = None, parent = 'output_m_chest_001')

        cmds.matchTransform(shrug_ctrl_mirror.replace('ctrl_','zero_'),self.shrug_jnt.replace('_l_','_r_'),position = True)

        # 创建约束
        ctrls = [clavicle_ctrl,scapula_ctrl,clavicle_ctrl_mirror,scapula_ctrl_mirror]
        for ctrl in ctrls:
            cmds.parentConstraint(ctrl,ctrl.replace('ctrl_','jnt_'),mo = True)

        # 创建肩膀耸肩的目标约束
        cmds.aimConstraint(shrug_ctrl, clavicle_ctrl.replace('ctrl_','driven_'), worldUpType = 2, aimVector = (1, 0, 0),
                           worldUpObject = shrug_ctrl.replace('ctrl_','zero_'), maintainOffset = True)
        cmds.aimConstraint(shrug_ctrl_mirror, clavicle_ctrl_mirror.replace('ctrl_', 'driven_'), worldUpType = 2,
                           aimVector = (-1, 0, 0),
                           worldUpObject = shrug_ctrl_mirror.replace('ctrl_', 'zero_'), maintainOffset = True)


        self.create_ikfk_chain_rig()
        if self.ribbon  == True:
            self.create_ribbon_Rig(self.ikfk_chain,self.control_parent, self.joint_parent,self.joint_number)
            self.create_ribbon_Rig(self.ikfk_chain_mirror, self.control_parent_mirror, self.joint_parent_mirror,self.joint_number)
