
import muziToolset.rigging.module.face_module.brow as brow
from importlib import reload



reload(brow)

curve_point = cmds.ls(sl = True)
cmds.polyToCurve(curve_point  , degree = 3 , conformToSmoothMeshPreview = 1)

def build_setup() :
	brow_m = brow.Brow(side = 'm' , joint_parent = None , control_parent = None)
	brow_m.build_setup()



def build_rig() :
	brow_m = brow.Brow(side = 'm' , joint_parent = None , control_parent = None)
	brow_m.build_rig()



build_setup()
build_rig()