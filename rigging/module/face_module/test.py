
import muziToolset.rigging.module.face_module.jaw as jaw
from importlib import reload



reload(jaw)



def build_setup() :
	jaw_m = jaw.Jaw(side = 'm' , joint_parent = None , control_parent = None)
	jaw_m.build_setup()



def build_rig() :
	jaw_m = jaw.Jaw(side = 'm' , joint_parent = None , control_parent = None)
	jaw_m.build_rig()



#
# #
build_setup()
build_rig()