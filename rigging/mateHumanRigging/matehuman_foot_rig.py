# coding=utf-8

u"""
这是一个用来编写hand(手指)绑定的类
继承了arm_rig

目前已有的功能：
create_hand_rig: 创建手指的FK绑定控制系统

fingerCurlRig : 设置手指关节旋转的姿势。


"""
from importlib import reload
from . import matehuman_base_rig
from . import matehuman_arm_rig
from . import matehuman_ikfk_rig
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.core.matehumanUtils as matehumanUtils


reload(pipelineUtils)
reload(jointUtils)
reload(hierarchyUtils)
reload(matehumanUtils)
reload(matehuman_arm_rig)
reload(matehuman_ikfk_rig)


class Foot_Rig(matehuman_base_rig.Base_Rig) :
	
	

	def __init__(self,side) :
		super(Foot_Rig , self).__init__()
		self.side = side

		self.foot_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('foot_{}'.format(self.side))
		self.ball_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('ball_{}'.format(self.side))
		self.joint_parent = 'ikfkjnt_' + self.foot_drv
		
	
	
	def create_foot_rig(self) :
		u"""
		创建脚掌的绑定控制系统
		"""
		# 创建脚掌的FK绑定控制系统
		self.create_foot_fk_rig()
		# 创建脚掌的IK绑定控制系统
		self.create_foot_ik_rig()
		

	def create_foot_ik_rig(self):
		u'''
		创建脚掌的ik绑定控制系统
		:return:
		'''
		#创建脚掌的ik关节
		self.foot_ik_jnt = 'ikjnt_' + self.foot_drv
		self.ball_ik_chain = jointUtils.Joint.create_mateHuman_chain([self.ball_drv] , 'ikjnt_' , self.foot_ik_jnt ,
		                                                          constraint = False)[0]
		#创建singleIKhandle
		single_ikhandle_node = \
		cmds.ikHandle(name = self.ball_ik_chain.replace('ikjnt','ikhandle') , startJoint = self.foot_ik_jnt , endEffector = self.ball_ik_chain ,
		              sticky = 'sticky' , solver = 'ikSCsolver' , setupForRPsolver = True)[0]
		
		self.foot_ik_outputlocal = self.foot_ik_jnt.replace('jnt','outputLocal')
		
		cmds.parent(single_ikhandle_node, self.foot_ik_outputlocal)
		
		
		
	
	
	def create_foot_fk_rig(self) :
		u"""
				创建脚掌的FK绑定控制系统
		"""
		# 创建控制器的层级组
		self.ball_ctrl_grp = cmds.createNode('transform' , name = 'ctrlgrp_' + self.ball_drv)
		cmds.matchTransform(self.ball_ctrl_grp , self.ball_drv , position = True , rotation = True , scale = True)
		cmds.parentConstraint(self.ball_drv , self.ball_ctrl_grp , mo = True)
		cmds.parent(self.ball_ctrl_grp,self.cog_ctrl)
		
		self.ball_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.ball_drv , 'ikctrl' , shape = 'circle' ,
		                                                       radius = 8 ,
		                                                       axis = 'Y+' ,
		                                                       pos = self.ball_drv , parent = self.ball_ctrl_grp)
		self.ball_ctrl_output = self.ball_ctrl.replace('ctrl','output')

		
		# 获取脚趾各模块的drv关节
		self.bigtoe_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('bigtoe_{}'.format(self.side))
		self.indextoe_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('indextoe_{}'.format(self.side))
		self.middletoe_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('middletoe_{}'.format(self.side))
		self.littletoe_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('littletoe_{}'.format(self.side))
		self.ringtoe_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('ringtoe_{}'.format(self.side))
		
		# 创建脚趾各模块的FK关节链
		
		bigtoe_fk_system = matehuman_ikfk_rig.FK_Rig(self.bigtoe_drv , self.joint_parent , self.ball_ctrl_output ,
		                                                redius = 3)
		bigtoe_fk_system._create_fk_chain_system(constraint = True)
		
		indextoe_fk_system = matehuman_ikfk_rig.FK_Rig(self.indextoe_drv , self.joint_parent , self.ball_ctrl_output ,
		                                               redius = 3)
		indextoe_fk_system._create_fk_chain_system(constraint = True)
		
		middletoe_fk_system = matehuman_ikfk_rig.FK_Rig(self.middletoe_drv , self.joint_parent , self.ball_ctrl_output ,
		                                                 redius = 3)
		middletoe_fk_system._create_fk_chain_system(constraint = True)
		
		littletoe_fk_system = matehuman_ikfk_rig.FK_Rig(self.littletoe_drv , self.joint_parent , self.ball_ctrl_output ,
		                                               redius = 3)
		littletoe_fk_system._create_fk_chain_system(constraint = True)
		
		ringtoe_fk_system = matehuman_ikfk_rig.FK_Rig(self.ringtoe_drv , self.joint_parent , self.ball_ctrl_output ,
		                                                redius = 3)
		ringtoe_fk_system._create_fk_chain_system(constraint = True)
	
	



# example
# l_foot = Foot_Rig( 'l')
# l_foot.create_foot_rig()
