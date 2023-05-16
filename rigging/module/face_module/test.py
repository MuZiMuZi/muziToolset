
import muziToolset.rigging.module.face_module.tongue as tongue
from importlib import reload



reload(tongue)



def build_setup() :
	tongue_m = tongue.Tongue(joint_parent = None , control_parent = None)
	tongue_m.build_setup()



def build_rig() :
	tongue_m = tongue.Tongue( joint_parent = None , control_parent = None)
	tongue_m.build_rig()



# #
# # #
build_setup()
build_rig()