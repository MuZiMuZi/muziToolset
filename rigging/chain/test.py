from muziToolset.rigging.chain import chain
from importlib import reload



reload(chain)



def x() :
	custom = chain.Chain(side = 'l' , name = 'zz' , index = 5 , joint_parent = None , control_parent = None)
	custom.build_setup()



def y() :
	custom = chain.Chain(side = 'l' , name = 'zz' , index = 5 , joint_parent = None , control_parent = None)
	custom.build_rig()



x()
y()