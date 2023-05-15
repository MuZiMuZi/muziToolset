# coding=utf-8

import maya.cmds as cmds
import muziToolset.core.jointUtils as jointUtils
from importlib import reload
import muziToolset.rigging.face_module.jaw_rig as jaw_rig
import muziToolset.rigging.base_rig as base_rig



reload(jointUtils)
reload(jaw_rig)



class Face_rig(base_rig.Base_Rig) :
	"""
	Construction of facial binding system
	"""
	
	
	
	def __init__(self) :
		super().__init__()
		jointUtils.Joint.auto_bpJoint_orientation()
	
	
	
	def create_face_rig(self) :
		jaw = jaw_rig.Jaw_Rig(joint_parent = self.joint , control_parent = self.control)
		jaw.create_jaw_rig()



face = Face_rig()
face.create_face_rig()
