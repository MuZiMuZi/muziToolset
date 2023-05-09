import muziToolset.rigging.chain.chainFK as chainFK
from importlib import reload



reload(chainFK)



def x() :
	custom = chainFK.ChainFk(side = 'l' , name = 'zz' , index = 5 , joint_parent = None , control_parent = None)
	custom.build_setup()



def y() :
	custom = chainFK.ChainFk(side = 'l' , name = 'zz' , index = 5 , joint_parent = None , control_parent = None)
	custom.build_rig()



x()
y()