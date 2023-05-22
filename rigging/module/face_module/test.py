import muziToolset.rigging.module.face_module.mouth as mouth
from importlib import reload



reload(mouth)



def build_setup() :
	mouth_m = mouth.Mouth(side = 'm' , name = '' , joint_number = 2 , joint_parent = None ,
	                control_parent = None)
	mouth_m.build_setup()



def build_rig() :
	mouth_m = mouth.Eye(side = 'm' , name = '' , joint_number = 2  , joint_parent = None ,
	                control_parent = None)
	mouth_m.build_rig()



build_setup()
# build_rig()
