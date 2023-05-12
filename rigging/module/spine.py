from ..base import base
from ..chain import chainIK

class Spine(chainIK.ChainIK):
	
	
	
	def __init__(self , side , name , joint_number , direction , length = 10 , is_stretch = 1 , joint_parent = None ,
	             control_parent = None) :
		super().__init__(side , name , joint_number , direction , length , is_stretch , joint_parent , control_parent)
		self._rtype = 'Spine'