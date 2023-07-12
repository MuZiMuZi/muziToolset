from muziToolset.rigging.base import base
from importlib import reload
reload(base)

def x():
	custom = base.Base(side = 'l' , name = 'zz' , index = 5 , joint_parent = None , control_parent = None)
	custom.build_setup()
def y():
	custom = base.Base(side = 'l' , name = 'zz' , index = 5 , joint_parent = None , control_parent = None)
	custom.build_rig()

x()
y()