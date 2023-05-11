import muziToolset.rigging.chain.chainIKFK as chainIKFK
from importlib import reload



reload(chainIKFK)



def x() :
	custom = chainIKFK.ChainIKFK(side = 'l' , name = 'zz' , index = 5 , direction = [1,0,0] ,joint_parent = None , control_parent = None)
	custom.build_setup()



def y() :
	custom = chainIKFK.ChainIKFK(side = 'l' , name = 'zz' , index = 5 , direction = [1 , 0 , 0],
	joint_parent = None , control_parent = None)
	custom.build_rig()



x()
y()

