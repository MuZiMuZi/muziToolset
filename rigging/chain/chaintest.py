import muziToolset.rigging.chain.limbFK as limbFK
from importlib import reload



reload(limbFK)



def build_setup() :
	custom = limbFK.LimbFK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
	                       joint_parent = None ,
	                       control_parent = None)
	custom.build_setup()



def build_rig() :
	custom = limbFK.LimbFK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
	                       joint_parent = None ,
	                       control_parent = None)
	custom.build_rig()



build_setup()
build_rig()
