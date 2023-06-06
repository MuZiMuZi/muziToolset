import muziToolset.bind.module.face_module.brow as brow
from importlib import reload



reload(brow)



def build_setup() :
	brow_m = brow.Brow(side = 'm' , joint_parent = None , control_parent = None)
	brow_m.build_setup()



def build_rig() :
	brow_m = brow.Brow(side = 'm' , joint_parent = None , control_parent = None)
	brow_m.build_rig()


build_setup()
# build_rig()
