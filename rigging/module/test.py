import muziToolset.rigging.module.foot as foot
from importlib import reload



reload(foot)
def build_setup():
    foot_l = foot.Foot(side = 'l' , name  = 'zz', joint_parent = None , control_parent = None)
    foot_l.build_setup()
def build_rig():
    foot_l = foot.Foot(side = 'l' , name = 'zz' , joint_parent = None , control_parent = None)
    foot_l.build_rig()

#
#
build_setup()
build_rig()