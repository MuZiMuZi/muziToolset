import maya.cmds as cmds
from . import bone
from importlib import reload



reload(bone)



class Base(bone.Bone) :
	u"""
	基础的关节和控制器绑定
	"""
	
	
	
	def __init__(self , side , name , index , joint_parent = None , control_parent = None ) :
		bone.Bone.__init__(self , side , name , index , joint_parent , control_parent)
		self._rtype = 'base'
		self._name = name + self._rtype
