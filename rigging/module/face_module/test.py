
import muziToolset.rigging.module.face_module.tongue as tongue
from importlib import reload



reload(tonegue)



def build_setup() :
	tonegue_m = tonegue.Tongue(joint_parent = None , control_parent = None)
	tonegue_m.build_setup()



def build_rig() :
	tonegue_m = tonegue.Tongue( joint_parent = None , control_parent = None)
	tonegue_m.build_rig()



# #
# # #
build_setup()
build_rig()