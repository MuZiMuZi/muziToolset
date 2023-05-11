import muziToolset.rigging.chain.limbIK as limbIK
from importlib import reload



reload(limbIK)



def build_setup() :
	custom = limbIK.LimbIK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
	                       is_stretch = 1 ,
	                       limbtype = 'arm' ,
	                       joint_parent = None ,
	                       control_parent = None)
	custom.build_setup()



def build_rig() :
	custom = limbIK.LimbIK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
	                       limbtype = 'arm' ,
	                       joint_parent = None ,
	                       control_parent = None)
	custom.build_rig()



build_setup()
build_rig()
