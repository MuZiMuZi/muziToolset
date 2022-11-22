# coding=utf-8

u"""
这是一个用来编写neck（脖子）绑定的类，之后的绑定都会在这个类的基础上逐级继承下去

目前已有的功能：

create_neck_rig：创建脖子的控制器绑定



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


neck_bp_joints = ['bpjnt_m_neck_001', 'bpjnt_m_neck_002',' bpjnt_m_neck_003','bpjnt_m_neck_004','bpjnt_m_neck_005']
bpcrv = 'bpcrv_m_neck_001'

class Neck_Rig(ikfk_rig.IKFK_Rig):
    def __init__(self, bp_joints = None, joint_parent = None, control_parent = None, mirror = True,space_list = None):
        super(Neck_Rig, self).__init__(bp_joints = bp_joints, joint_parent=joint_parent,control_parent = control_parent,space_list = space_list)
        self.mirror = mirror
        self.neck_bp_joints = self.get_modular_bp_joints(self.neck_rig)
        self.bp_joints = self.neck_bp_joints
        # self.create_spine_rig()


    def create_neck_rig(self):
        self.ikfk_spine_rig()
