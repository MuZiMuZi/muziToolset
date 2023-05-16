
import muziToolset.rigging.module.face_module.nose as nose
from importlib import reload



reload(nose)



def build_setup() :
	nose_l = nose.Nose(joint_parent = None , control_parent = None)
	nose_l.build_setup()



def build_rig() :
	nose_l = nose.Nose( joint_parent = None , control_parent = None)
	nose_l.build_rig()



# #
# # #
build_setup()
build_rig()