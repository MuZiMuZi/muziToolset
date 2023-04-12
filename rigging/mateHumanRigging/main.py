import muziToolset.rigging.mateHumanRigging.ikfk_rig as ikfk_rig
from importlib import reload



reload(ikfk_rig)
drv_jnts = ['upperarm_l_drv' , 'lowerarm_l_drv' , 'hand_l_drv']
joint_parent = None
control_parent = None
space_list = None

master = ikfk_rig.IK_Rig(drv_jnts , joint_parent , control_parent, space_list)

master.create_ik_chain()
master.ik_chain_rig(stretch = True)