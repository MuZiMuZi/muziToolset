import muziToolset.bind.module.face_module.ear as ear
from importlib import reload



reload(ear)



def build_setup() :
	ear_l = ear.Ear(side = 'l' , joint_parent = None , control_parent = None)
	ear_l.build_setup()
	
	ear_r = ear.Ear(side = 'r' , joint_parent = None , control_parent = None)
	ear_r.build_setup()



def build_rig() :
	ear_l = ear.Ear(side = 'l' , joint_parent = None , control_parent = None)
	ear_l.build_rig()
	
	ear_r = ear.Ear(side = 'r' , joint_parent = None , control_parent = None)
	ear_r.build_rig()



# build_setup()
build_rig()
