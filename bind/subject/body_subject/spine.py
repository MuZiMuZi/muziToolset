from ...module.chain import chainIKFK
from ...module.base import base

from importlib import reload
reload(chainIKFK)



class Spine(chainIKFK.ChainIKFK) :
	
	
	
	def __init__(self , side , name , jnt_number , direction , length = 10 , is_stretch = 1 , jnt_parent = None ,
	             control_parent = None) :
		super().__init__(side , name , jnt_number , direction , length , is_stretch , jnt_parent , control_parent)
		self._rtype = 'Spine'



if __name__ == '__main__' :
	def build_setup() :
		spine_m = spine.Spine(side = 'm' , name = 'zz' , jnt_number = 4 , direction = [0 , 1 , 0] , length = 10 ,
		                      is_stretch = 1 , jnt_parent = None ,
		                      control_parent = None)
		spine_m.build_setup()
	
	
	
	def build_rig() :
		spine_m = spine.Spine(side = 'm' , name = 'zz' , jnt_number = 4 , direction = [0 , 1 , 0] , length = 10 ,
		                      is_stretch = 1 , jnt_parent = None ,
		                      control_parent = None)
		spine_m.build_rig()
	
	
	
	build_setup()
	build_rig()
