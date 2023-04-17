import muziToolset.rigging.mateHumanRigging.matehuman_ikfk_rig as matehuman_ikfk_rig
import muziToolset.rigging.mateHumanRigging.matehuman_hand_rig as matehuman_hand_rig
import muziToolset.rigging.mateHumanRigging.matehuman_arm_rig as matehuman_arm_rig
import muziToolset.rigging.mateHumanRigging.matehuman_leg_rig as matehuman_leg_rig
import muziToolset.rigging.mateHumanRigging.matehuman_foot_rig as matehuman_foot_rig
import muziToolset.core.matehumanUtils as matehumanUtils
from importlib import reload


reload(matehuman_arm_rig)
reload(matehumanUtils)
reload(matehuman_hand_rig)
reload(matehuman_leg_rig)
reload(matehuman_foot_rig)

joint_parent = None
control_parent = None
space_list = None
side = 'l'

# example

l_arm = matehuman_arm_rig.Arm_rig('l' , joint_parent , space_list = None , stretch = True)
l_arm.create_arm_rig()

l_leg = matehuman_leg_rig.Leg_rig('l' , joint_parent , space_list = None , stretch = True)
l_leg.create_leg_rig()


# l_foot = matehuman_foot_rig.Foot_Rig('l')
# l_foot.create_foot_rig()
