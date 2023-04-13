import muziToolset.rigging.mateHumanRigging.ikfk_rig as ikfk_rig
from importlib import reload



reload(ikfk_rig)
drv_jnts = ['spine_01_drv' , 'spine_02_drv' , 'spine_03_drv','spine_04_drv','spine_05_drv']
joint_parent = None
control_parent = None
space_list = None

master = ikfk_rig.IK_Rig(drv_jnts , joint_parent , control_parent, space_list)

master.create_ik_chain()
master.ik_spine_rig(stretch = True)