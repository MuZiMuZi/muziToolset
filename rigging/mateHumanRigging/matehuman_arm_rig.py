# coding=utf-8
from importlib import reload

from . import matehuman_base_rig
from . import matehuman_ikfk_rig
from . import matehuman_hand_rig
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.core.snapUtils as snapUtils
import muziToolset.core.matehumanUtils as matehumanUtils


reload(matehumanUtils)
reload(matehuman_ikfk_rig)
reload(matehuman_base_rig)
reload(matehuman_hand_rig)


class Arm_rig(matehuman_base_rig.Base_Rig) :
	
	
	def __init__(self , side , joint_parent , space_list , stretch = True) :
		super().__init__()
		self.side = side
		self.drv_jnts = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('arm_{}'.format(self.side))
		self.joint_parent = joint_parent
		self.control_parent = 'output_' + matehumanUtils.MateHuman.get_mateHuman_drv_jnt(
			'clavicle_{}'.format(self.side))
		self.space_list = space_list
		self.stretch = stretch
	
	
	def create_arm_rig(self) :
		u'''
		创建手臂的控制器绑定
		:return:
		'''
		# 创建锁骨部位的绑定
		self.create_clavicle_rig()
		# 创建手臂部位的绑定
		arm_system = matehuman_ikfk_rig.IKFK_Rig(self.drv_jnts , self.joint_parent , self.control_parent ,
		                                            self.space_list , self.stretch)
		arm_system.create_ikfk_chain_rig(Y_value = 1)
		
		# 创建手掌部位的绑定
		hand_system = matehuman_hand_rig.Hand_Rig(self.side)
		hand_system.create_hand_rig()
	
	
	def create_clavicle_rig(self) :
		# 创建锁骨的控制器
		clavicle_jnt = 'clavicle_{}_drv'.format(self.side)
		clavicle_ctrl = controlUtils.Control.create_mateHuman_ctrl(clavicle_jnt , 'ctrl' , shape = 'ball' ,
		                                                           radius = 12 ,
		                                                           axis = 'Z+' ,
		                                                           pos = clavicle_jnt , parent = None)
		clavicle_output = clavicle_ctrl.replace('ctrl' , 'output')
		# parent = 'output_m_chest_001'
		
		
		# 创建耸肩的控制器
		shrug_jnt = 'clavicle_outOff_{}_drv'.format(self.side)
		shrug_ctrl = controlUtils.Control.create_mateHuman_ctrl(shrug_jnt , 'ctrl' , shape = 'Cube' ,
		                                                        radius = 5 ,
		                                                        axis = 'Z+' ,
		                                                        pos = None , parent = clavicle_ctrl.replace(
					'ctrl' , 'output'))
		# 只吸附位移不吸附旋转
		
		cmds.matchTransform(shrug_ctrl.replace('ctrl' , 'zero') , shrug_jnt , position = True)
		shrug_output = shrug_ctrl.replace('ctrl' , 'output')
		
		# 创建肩胛骨的控制器
		scapula_jnt = 'clavicle_scapOff_{}_drv'.format(self.side)
		scapula_ctrl = controlUtils.Control.create_mateHuman_ctrl(scapula_jnt , 'ctrl' , shape = 'Cube' ,
		                                                          radius = 5 ,
		                                                          axis = 'Z+' ,
		                                                          pos = None , parent = clavicle_ctrl.replace(
					'ctrl' , 'output'))
		# 只吸附位移不吸附旋转
		
		cmds.matchTransform(scapula_ctrl.replace('ctrl' , 'zero') , scapula_jnt , position = True)
		scapula_output = scapula_ctrl.replace('ctrl' , 'output')
		
		# 创建约束
		ctrls = [clavicle_ctrl , shrug_ctrl , scapula_ctrl]
		jnts = [clavicle_jnt , shrug_jnt , scapula_jnt]
		for ctrl , jnt in zip(ctrls , jnts) :
			cmds.parentConstraint(ctrl , jnt , mo = True)
			cmds.scaleConstraint(ctrl , jnt , mo = True)



# example
# l_arm = matehuman_arm_rig.Arm_rig( 'l',joint_parent  , space_list = None,stretch = True)
#
# l_arm.create_arm_rig()
