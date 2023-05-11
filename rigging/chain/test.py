import muziToolset.rigging.chain.chainEP as chainEP
from importlib import reload



reload(chainEP)


def x() :
	custom = chainEP.ChainEP(side = 'l' , name = 'zz' , joint_number = 10 , ctrl_number = 5 , curve = 'curve1' ,joint_parent = None , control_parent = None)
	custom.build_setup()



def y() :
	custom = chainEP.ChainEP(side = 'l' , name = 'zz' , joint_number = 10 , ctrl_number  = 5, curve = 'curve1',
	joint_parent = None , control_parent = None)
	custom.build_rig()



x()
y()
