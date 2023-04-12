import muziToolset.rigging.mateHumanRigging.ikfk_rig as ikfk_rig
from importlib import reload



reload(ikfk_rig)
drv_jnts = ['upperarm_l_drv' , 'lowerarm_l_drv' , 'hand_l_drv']
joint_parent = None
control_parent = None

master = ikfk_rig.FK_Rig(drv_jnts , joint_parent , control_parent)

master.create_fk_chain()
master.fk_chain_rig()