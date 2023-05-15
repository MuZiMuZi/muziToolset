import muziToolset.rigging.module.leg as leg
from importlib import reload



reload(leg)
def build_setup():
    leg_l = leg.Leg(side = 'l' , name  = 'zz', joint_parent = None , control_parent = None)
    leg_l.build_setup()
def build_rig():
    leg_l = leg.Leg(side = 'l' , name = 'zz' , joint_parent = None , control_parent = None)
    leg_l.build_rig()

#
# #
build_setup()
build_rig()