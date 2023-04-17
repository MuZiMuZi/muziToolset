# coding=utf-8
from importlib import reload

import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.matehumanUtils as matehumanUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.core.snapUtils as snapUtils

from . import matehuman_base_rig
from . import matehuman_foot_rig
from . import matehuman_hand_rig
from . import matehuman_ikfk_rig


reload(matehumanUtils)
reload(matehuman_ikfk_rig)
reload(matehuman_base_rig)
reload(matehuman_hand_rig)


class Leg_rig(matehuman_base_rig.Base_Rig) :
	
	
	def __init__(self , side , joint_parent , space_list , stretch = True) :
		super().__init__()
		self.side = side
		self.drv_jnts = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('leg_{}'.format(self.side))
		self.joint_parent = joint_parent
		self.control_parent = 'output_m_cog_001'
		self.space_list = space_list
		self.stretch = stretch
	
	
	def create_leg_rig(self) :
		u'''
		创建腿部的控制器绑定
		:return:
		'''
		# 创建腿部位的绑定
		leg_system = matehuman_ikfk_rig.IKFK_Rig(self.drv_jnts , self.joint_parent , self.control_parent ,
		                                            self.space_list , self.stretch)
		leg_system.create_ikfk_chain_rig(Y_value = -1)
		
		# 创建脚掌部位的绑定
		self.create_foot_rig()
	
	
	
	def create_foot_rig(self):
		foot_system = matehuman_foot_rig.Foot_Rig(self.side)
		foot_system.create_foot_rig()
		

# example
# l_leg = matehuman_leg_rig.Leg_rig( 'l',joint_parent , space_list = None,stretch = True)
#
# l_leg.create_leg_rig()
