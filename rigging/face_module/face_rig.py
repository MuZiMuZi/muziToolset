# coding=utf-8

import maya.cmds as cmds
import muziToolset.core.jointUtils as jointUtils
from  importlib import reload
import muziToolset.rigging.face_module.jaw_rig as jaw_rig
reload(jointUtils)
reload(jaw_rig)
class Face_rig(object):
	"""
	Construction of facial binding system
	"""
	
	def __init__(self):
		jointUtils.Joint.auto_bpJoint_orientation()
	def create_face_rig(self):
		jaw = jaw_rig.Jaw_Rig()
		jaw.create_jaw_rig()
		



face = Face_rig()
face.create_face_rig()
print(10)
