# coding=utf-8
'''
下巴的绑定系统创建
'''
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.jointUtils as jointUtils
from .. import base_rig
from importlib import reload
reload(controlUtils)
reload(jointUtils)
reload(base_rig)

class Jaw_Rig(base_rig.Base_Rig):
	
	
	def __init__(self, joint_parent = None , control_parent = None) :
		super(Jaw_Rig , self).__init__()
		self.joint_parent = joint_parent
		self.control_parent = control_parent

	def create_jaw_rig(self):
		u'''
		生成下巴的绑定
		'''
		self.jaw_bpjnts = self.get_bpjnt('jaw_m')
		self.jaw_joints = jointUtils.Joint.create_chain(self.jaw_bpjnts , 'FK', self.joint_parent)
		self.jaw_ctrl = controlUtils.Control.create_ctrl(self.jaw_bpjnts[0].replace('BPjnt','ctrl') , shape = 'circle' , radius =3 , axis = 'Z-' ,
		                                                 pos = self.jaw_bpjnts[0] ,
		                                                 parent = self.control_parent)

		#约束下巴的关节
		cmds.parentConstraint(self.jaw_ctrl.replace(' ctrl','output'),self.jaw_joints[0])
