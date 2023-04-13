import muziToolset.rigging.mateHumanRigging.matehuman_ikfk_rig as matehuman_ikfk_rig
import muziToolset.rigging.mateHumanRigging.matehuman_hand_rig as matehuman_hand_rig
from importlib import reload



reload(matehuman_hand_rig)
joint_parent = None
control_parent = None
space_list = None
side = 'l'

master = matehuman_hand_rig.Hand_Rig(joint_parent , control_parent , side)

master.create_hand_rig()