import muziToolset.bind.module.face_module.tongue as tongue
from importlib import reload



reload(tongue)



def build_setup() :
	tongue_m = tongue.Tongue(side = 'm' , name = '' , joint_number = 5 , direction = [-1 , 0 , 0] , length = 10 ,
	                         joint_parent = None ,
	                         control_parent = None)
	tongue_m.build_setup()



def build_rig() :
	tongue_m = tongue.Tongue(side = 'm' , name = '' , joint_number = 5 , direction = [-1 , 0 , 0] , length = 10 ,
	                         joint_parent = None ,
	                         control_parent = None)
	tongue_m.build_rig()



# build_setup()
build_rig()
