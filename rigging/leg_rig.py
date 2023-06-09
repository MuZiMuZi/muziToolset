# coding=utf-8

u"""
这是一个用来编写Leg（腿部）绑定的类，之后的绑定都会在这个类的基础上逐级继承下去

目前已有的功能：

create_leg_rig：创建腿部的控制器绑定



"""
import ikfk_rig
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils


class Leg_Rig(ikfk_rig.IKFK_Rig) :


    def __init__(self , bp_joints = None , joint_parent = None , control_parent = None , ribbon = True ,
                 joint_number = 5 , space_list = None) :
        super(Leg_Rig , self).__init__(bp_joints = bp_joints , joint_parent = joint_parent ,
                                       control_parent = control_parent , space_list = space_list)
        self.leg_bp_joints = self.get_modular_bp_joints(self.leg_rig)
        self.bp_joints = self.leg_bp_joints
        self.ribbon = ribbon
        self.joint_number = joint_number
        self.obj = nameUtils.Name(name = self.leg_bp_joints[0])
        self.side = self.obj.side


    def create_leg_rig(self) :
        self.create_ikfk_chain_rig()
        if self.ribbon == True :
            self.create_ribbon_Rig(self.ikfk_chain , self.control_parent , self.joint_parent , self.joint_number)
