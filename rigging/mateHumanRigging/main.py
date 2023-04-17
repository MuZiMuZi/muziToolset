import muziToolset.rigging.mateHumanRigging.matehuman_ikfk_rig as matehuman_ikfk_rig
import muziToolset.rigging.mateHumanRigging.matehuman_hand_rig as matehuman_hand_rig
import muziToolset.rigging.mateHumanRigging.matehuman_arm_rig as matehuman_arm_rig
import muziToolset.rigging.mateHumanRigging.matehuman_leg_rig as matehuman_leg_rig
import muziToolset.rigging.mateHumanRigging.matehuman_foot_rig as matehuman_foot_rig
import muziToolset.rigging.mateHumanRigging.matehuman_spine_rig as matehuman_spine_rig
import muziToolset.rigging.mateHumanRigging.matehuman_neck_rig as matehuman_neck_rig
from . import matehuman_base_rig
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


class MateHuman_Rig(matehuman_base_rig.Base_Rig):
	
	
	def __init__(self) :
		super().__init__()
		self.create_rig()
		self.create_offset_ctrl()
	def create_rig(self):
		m_spine = matehuman_spine_rig.Spine_Rig(space_list , stretch = True)
		
		m_spine.create_spine_rig()
		
		m_neck = matehuman_neck_rig.Neck_Rig( space_list)
		
		m_neck.create_neck_rig()
		
		for side in ['l','r']:
			arm = matehuman_arm_rig.Arm_rig(side , space_list = None , stretch = True)
			arm.create_arm_rig()
			
			leg = matehuman_leg_rig.Leg_rig(side , space_list = None , stretch = True)
			leg.create_leg_rig()

