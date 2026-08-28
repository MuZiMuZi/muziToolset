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
reload(matehuman_base_rig)


class Hand_Rig(matehuman_base_rig.Base_Rig) :
	
	
	def __init__(self , side) :
		super(Hand_Rig,self).__init__()
		self.side = side
		if self.side == 'l' :
			self.side_value = 1
		elif self.side == 'r' :
			self.side_value = -1
		self.hand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('hand_{}'.format(self.side))
		self.wrist_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('wrist_{}'.format(self.side))
		self.jnt_parent = 'ikfkjnt_' + self.hand_drv
	
	
	def create_hand_rig(self) :
		u"""
		创建手指的绑定控制系统
		"""
		# 创建手指的FK绑定控制系统
		self.create_hand_fk_rig()
		
		# 创建手指的弯曲系统
		self.create_hand_curl_rig()
		
		# 创建手指的IK绑定控制系统
		self.create_hand_ik_rig()
	
	
	def create_hand_fk_rig(self) :
		u"""
				创建手指的FK绑定控制系统
		"""
		# 创建控制器的层级组
		self.hand_ctrl_grp = cmds.createNode('transform' , name = 'ctrlgrp_' + self.hand_drv)
		cmds.matchTransform(self.hand_ctrl_grp , self.hand_drv , position = True , rotation = True , scale = True)
		cmds.parentConstraint(self.jnt_parent , self.hand_ctrl_grp , mo = True)
		clavicle_output = 'output_' + matehumanUtils.MateHuman.get_mateHuman_drv_jnt(
				'clavicle_{}'.format(self.side))
		cmds.parent(self.hand_ctrl_grp , clavicle_output)
		
		# 获取手指各模块的drv关节
		self.thumbHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('thumb_finger_{}'.format(self.side))
		self.indexHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('index_finger_{}'.format(self.side))
		self.middleHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('middle_finger_{}'.format(self.side))
		self.ringHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('ring_finger_{}'.format(self.side))
		self.pinkyHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('pinky_finger_{}'.format(self.side))
		
		# 创建手指各模块的FK关节链
		
		thumbHand_fk_system = matehuman_ikfk_rig.FK_Rig(self.thumbHand_drv , self.jnt_parent , self.hand_ctrl_grp ,
		                                                redius = 2)
		thumbHand_fk_system._create_fk_chain_system(constraint = True)
		
		indexHand_fk_system = matehuman_ikfk_rig.FK_Rig(self.indexHand_drv , self.jnt_parent , self.hand_ctrl_grp ,
		                                                redius = 2)
		indexHand_fk_system._create_fk_chain_system(constraint = True)
		
		middleHand_fk_system = matehuman_ikfk_rig.FK_Rig(self.middleHand_drv , self.jnt_parent , self.hand_ctrl_grp ,
		                                                 redius = 2)
		middleHand_fk_system._create_fk_chain_system(constraint = True)
		
		ringHand_fk_system = matehuman_ikfk_rig.FK_Rig(self.ringHand_drv , self.jnt_parent , self.hand_ctrl_grp ,
		                                               redius = 2)
		ringHand_fk_system._create_fk_chain_system(constraint = True)
		
		pinkyHand_fk_system = matehuman_ikfk_rig.FK_Rig(self.pinkyHand_drv , self.jnt_parent , self.hand_ctrl_grp ,
		                                                redius = 2)
		pinkyHand_fk_system._create_fk_chain_system(constraint = True)
	
	
	def create_hand_ik_rig(self) :
		u"""
				创建手指的IK绑定控制系统
		"""
		# 创建手掌的ik关节
		self.hand_ik_jnt = 'ikjnt_' + self.hand_drv
		self.wirst_ik_chain = cmds.createNode('joint' , name = 'ikjnt_' + self.wrist_drv)
		cmds.matchTransform(self.wirst_ik_chain , self.hand_ik_jnt , position = True , rotation = True)
		cmds.makeIdentity(self.wirst_ik_chain , apply = True , translate = True , rotate = True , scale = True)
		cmds.parent(self.wirst_ik_chain,self.hand_ik_jnt)
		cmds.setAttr(self.wirst_ik_chain + '.translateX' , self.side_value * 10)
		
		# 创建singleIKhandle
		single_ikhandle_node = \
			cmds.ikHandle(name = self.hand_ik_jnt.replace('ikjnt' , 'ikhandle') , startJoint = self.hand_ik_jnt ,
			              endEffector = self.wirst_ik_chain ,
			              sticky = 'sticky' , solver = 'ikSCsolver' , setupForRPsolver = True)[0]
		
		self.hand_ik_outputlocal = self.hand_ik_jnt.replace('jnt' , 'Localoutput')
		
		cmds.parent(single_ikhandle_node , self.hand_ik_outputlocal)
	
	
	def create_hand_curl_rig(self) :
		u"""
		创建手指的弯曲系统，设置手指关节旋转的姿势。
		"""
		pose_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.thumbHand_drv[0] , 'fkposectrl' ,
		                                                       shape = 'pPlatonic' ,
		                                                       radius = 6 ,
		                                                       axis = 'X+' ,
		                                                       pos = self.thumbHand_drv[0] ,
		                                                       parent = self.hand_ctrl_grp)
		
		# 获取手指名称
		finger_names = ['thumb' , 'index' , 'middle' , 'ring' , 'pinky']
		
		# 获取关节节数名称
		digit_index = {'thumb' : ['01' , '02' , '03']}
		
		# 获取curl的值
		curl_mult_values = {'thumb' : [0 , -5 , -7] ,
		                    'index' : [0 , -7.5 , -10.5 , -8] ,
		                    'middle' : [0 , -7.5 , -10.5 , -8] ,
		                    'ring' : [0 , -7.5 , -10.5 , -8] ,
		                    'pinky' : [0 , -7.5 , -10.5 , -8]}
		# 获取手姿势控制的控制器
		# 循环到每个手指，并添加curl attr
		for finger in finger_names :
			cmds.addAttr(pose_ctrl , longName = finger + 'Curl' , attributeType = 'float' , keyable = True ,
			             minValue = -10 , maxValue = 10)
			curl_attr = '{}.{}Curl'.format(pose_ctrl , finger)
			
			# 获取卷曲值
			curl_values = curl_mult_values[finger]
			# 获取关节节数名称
			finger_digits = digit_index.get(finger , ['metacarpal' , '01' , '02' , '03'])
			# 循环到每个手指并连接卷曲的值
			for digit , val in zip(finger_digits , curl_values) :
				offset_name = 'fkoffset_{}_{}_{}_drv'.format(finger , digit , self.side)
				
				if val :
					# 创建乘法节点
					mult_node = cmds.createNode('multDoubleLinear' ,
					                            name = 'mult_{}_{}{}Curl_001'.format(self.side , finger ,
					                                                                 digit.title()))
					# 连接驱动的节点的属性
					cmds.connectAttr(curl_attr , mult_node + '.input1')
					# 设置卷曲值
					cmds.setAttr(mult_node + '.input2' , val)
					
					# 将输出连接到偏移组的rotateZ
					cmds.connectAttr(mult_node + '.output' , offset_name + '.rotateZ')


# example
# l_hand = Hand_Rig( 'l')
# l_hand.create_hand_rig()
