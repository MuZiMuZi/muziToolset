import muziToolset.rigging.mateHumanRigging.matehuman_arm_rig as matehuman_arm_rig
import muziToolset.rigging.mateHumanRigging.matehuman_ikfk_rig as matehuman_ikfk_rig
import muziToolset.core.matehumanUtils as matehumanUtils
from importlib import reload



reload(matehuman_ikfk_rig)
reload(matehuman_arm_rig)
reload(matehumanUtils)

mate = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('thigh_l')
print(mate)
# #
# # drv_jnts = ['upperarm_l_drv' , 'lowerarm_l_drv' , 'hand_l_drv']
# # drv_jnts = ['spine_01_drv' , 'spine_02_drv' , 'spine_03_drv','spine_04_drv','spine_05_drv']
#
# joint_parent = None
# control_parent = None
# space_list = None
# stretch = True
#
# drv_jnts = ['upperarm_l_drv' , 'lowerarm_l_drv' , 'hand_l_drv']
# l_arm = matehuman_arm_rig.Arm_rig(drv_jnts , joint_parent , control_parent, space_list, stretch,side='l')
