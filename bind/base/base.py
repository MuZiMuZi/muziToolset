from importlib import reload

from . import bone



reload(bone)



class Base(bone.Bone) :
	u"""
	基础的关节和控制器绑定
	"""
	
	
	
	def __init__(self , side , name , joint_number , joint_parent = None , control_parent = None) :
		bone.Bone.__init__(self , side , name , joint_number , joint_parent , control_parent)
		self._rtype = 'Base'
