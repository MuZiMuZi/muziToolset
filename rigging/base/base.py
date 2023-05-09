import maya.cmds as cmds
from . import bone
from importlib import reload



reload(bone)
class Base(bone.Bone):
	u"""
	基础的关节和控制器绑定
	"""

	def __init__(self , side , name , index , joint_parent = None , control_parent = None , point_value = True ,
	             orient_value = True , scale_value = True , mo_value = True) :
		bone.Bone.__init__(self,side , name , index , joint_parent , control_parent , point_value , orient_value ,
		                 scale_value , mo_value)
		self._rtype = 'base'
		self._name = name + self._rtype
	
	
	

	

	
		
	

	
	