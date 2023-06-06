import muziToolset.bind.module.face_module.cheek as cheek
from importlib import reload



reload(cheek)



def build_setup() :
	cheek_m = cheek.Cheek(side = 'm' , name = '' , joint_number = 8 , joint_parent = None ,
	                control_parent = None)
	cheek_m.build_setup()



def build_rig() :
	cheek_m = cheek.Cheek(side = 'm' , name = '' , joint_number = 8 , joint_parent = None ,
	                control_parent = None)
	cheek_m.build_rig()



build_setup()
# build_rig()
