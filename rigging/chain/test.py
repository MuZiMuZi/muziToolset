import muziToolset.rigging.chain.chainIKSpline as chainIKSpline
from importlib import reload



reload(chainIKSpline)



def x() :
	custom = chainIKSpline.ChainIKSpline(side = 'l' , name = 'zz' , index = 5 , direction = [1,0,0] ,joint_parent = None , control_parent = None)
	custom.build_setup()



def y() :
	custom = chainIKSpline.ChainIKSpline(side = 'l' , name = 'zz' , index = 5 , direction = [1 , 0 , 0],
	joint_parent = None , control_parent = None)
	custom.build_rig()



x()
y()

