import muziToolset.rigging.mateHumanRigging.matehuman_ikfk_rig as matehuman_ikfk_rig
import muziToolset.rigging.mateHumanRigging.matehuman_hand_rig as matehuman_hand_rig
import muziToolset.rigging.mateHumanRigging.matehuman_arm_rig as matehuman_arm_rig
import muziToolset.rigging.mateHumanRigging.matehuman_leg_rig as matehuman_leg_rig
import muziToolset.rigging.mateHumanRigging.matehuman_foot_rig as matehuman_foot_rig
import muziToolset.rigging.mateHumanRigging.matehuman_spine_rig as matehuman_spine_rig
import muziToolset.rigging.mateHumanRigging.matehuman_neck_rig as matehuman_neck_rig
import muziToolset.rigging.mateHumanRigging.matehuman_base_rig as matehuman_base_rig
import muziToolset.core.matehumanUtils as matehumanUtils
from importlib import reload


reload(matehuman_arm_rig)
reload(matehumanUtils)
reload(matehuman_hand_rig)
reload(matehuman_leg_rig)
reload(matehuman_foot_rig)
reload(matehuman_spine_rig)
reload(matehuman_neck_rig)
reload(matehuman_neck_rig)


# matehuman = MateHuman_Rig()
# matehuman.create_rig()

# matehumanUtils.MateHuman.export_face_animation()

matehumanUtils.MateHuman.export_body_animation()

