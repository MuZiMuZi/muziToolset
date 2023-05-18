
import muziToolset.rigging.module.face_module.eyeLid as eyeLid
from importlib import reload



reload(eyeLid)



def build_setup() :
	eye_lid = eyeLid.EyeLid(side = 'l' , name = 'upper' , joint_number = 7 , joint_parent = None , control_parent = None)
	eye_lid.build_setup()



def build_curve() :
	eye_lid = eyeLid.EyeLid(side = 'l' , name = 'upper' , joint_number = 7 , joint_parent = None , control_parent =
	None)
	eye_lid.build_setup()
	eye_lid.build_curve()

def build_rig() :
	eye_lid = eyeLid.EyeLid(side = 'l' , name = 'upper' , joint_number = 7 , joint_parent = None , control_parent =
	None)
	eye_lid.build_rig()




# build_setup()
build_curve()
build_rig()