# coding=utf-8

u"""
这是一个用来编写spine（脊椎）绑定的类，之后的绑定都会在这个类的基础上逐级继承下去

目前已有的功能：

create_spine_rig：创建脊椎的控制器绑定



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
reload(ikfk_rig)

spine_bp_joints = ['bpjnt_m_spine_001', 'bpjnt_m_spine_002',' bpjnt_m_spine_003','bpjnt_m_spine_004','bpjnt_m_spine_005']
bpcrv = 'bpcrv_m_spine_001'

class Spine_Rig(ikfk_rig.IKFK_Rig):
    def __init__(self, bp_joints = None , joint_parent = None, control_parent = None,mirror = False):
        super(Spine_Rig, self).__init__(bp_joints = bp_joints, joint_parent=joint_parent,control_parent = control_parent)
        self.mirror = mirror
        self.spine_bp_joints = self.get_modular_bp_joints(self.spine_rig)
        self.bp_joints = self.spine_bp_joints
        # self.create_spine_rig()


    def create_spine_rig(self):
        self.ikfk_spine_rig()
