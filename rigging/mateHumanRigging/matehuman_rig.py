from importlib import reload

import maya.cmds as cmds
import muziToolset.core.matehumanUtils as matehumanUtils
import muziToolset.rigging.mateHumanRigging.matehuman_arm_rig as matehuman_arm_rig
import muziToolset.rigging.mateHumanRigging.matehuman_base_rig as matehuman_base_rig
import muziToolset.rigging.mateHumanRigging.matehuman_foot_rig as matehuman_foot_rig
import muziToolset.rigging.mateHumanRigging.matehuman_hand_rig as matehuman_hand_rig
import muziToolset.rigging.mateHumanRigging.matehuman_ikfk_rig as matehuman_ikfk_rig
import muziToolset.rigging.mateHumanRigging.matehuman_leg_rig as matehuman_leg_rig
import muziToolset.rigging.mateHumanRigging.matehuman_neck_rig as matehuman_neck_rig
import muziToolset.rigging.mateHumanRigging.matehuman_spine_rig as matehuman_spine_rig


reload(matehuman_ikfk_rig)
reload(matehuman_arm_rig)
reload(matehumanUtils)
reload(matehuman_hand_rig)
reload(matehuman_leg_rig)
reload(matehuman_foot_rig)
reload(matehuman_spine_rig)
reload(matehuman_neck_rig)
reload(matehuman_neck_rig)
reload(matehuman_base_rig)


class MateHuman_Rig(matehuman_base_rig.Base_Rig) :
	
	
	def __init__(self) :
		super(MateHuman_Rig , self).__init__()
	
	
	def create_rig(self) :
		#创建脊椎的绑定
		m_spine = matehuman_spine_rig.Spine_Rig(space_list = None , stretch = True)
		m_spine.create_spine_rig()

		# 创建脖子的绑定
		m_neck = matehuman_neck_rig.Neck_Rig(space_list = None)
		m_neck.create_neck_rig()

		# 创建四肢的绑定
		for side in ['l' , 'r'] :
			arm = matehuman_arm_rig.Arm_rig(side , space_list = None , stretch = True)
			arm.create_arm_rig()

			leg = matehuman_leg_rig.Leg_rig(side , space_list = None , stretch = True)
			leg.create_leg_rig()

		# #生成修型关节的控制器绑定
		self.create_offset_ctrl()