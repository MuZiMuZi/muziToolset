import muziToolset.rigging.mateHumanRigging.matehuman_arm_rig as matehuman_arm_rig
from importlib import reload



reload(ikfk_rig)
reload(matehuman_arm_rig)
#
# drv_jnts = ['upperarm_l_drv' , 'lowerarm_l_drv' , 'hand_l_drv']
# drv_jnts = ['spine_01_drv' , 'spine_02_drv' , 'spine_03_drv','spine_04_drv','spine_05_drv']

joint_parent = None
control_parent = None
space_list = None
stretch = True

drv_jnts = ['upperarm_l_drv' , 'lowerarm_l_drv' , 'hand_l_drv']
l_arm = matehuman_arm_rig.Arm_rig(drv_jnts , joint_parent , control_parent, space_list, stretch,side='l')
