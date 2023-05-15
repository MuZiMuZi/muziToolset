# coding=utf-8
'''
眼睛的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base
from ...chain import chain , chainFK
from ....core import controlUtils , jointUtils



class Eye(chain.Chain) :
	
	
	
	def __init__(self , side , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
	             control_parent = None) :
		super().__init__(side , name , joint_number , length , joint_parent , control_parent)
		self.shape = 'circle'
		self._rtype = 'Eye'
		self.radius = 0.3
		
		# iris的缩放关节
		self.iris_bpjnt_list = list()
		self.iris_jnt_list = list()
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		self.aim_ctrl = ('ctrl_{}_{}{}Aim_001'.format(self._side , self._name , self._rtype))
		self.aim_loc = ('loc_{}_{}{}Aim_001'.format(self._side , self._name , self._rtype))
		self.jnt_loc = ('loc_{}_{}{}Jnt_001'.format(self._side , self._name , self._rtype))
		self.aim_crv = ('crv_{}_{}{}Aim_001'.format(self._side , self._name , self._rtype))
		for index in range(3) :
			self.iris_bpjnt_list.append(
					'bpjnt_{}_{}{}iris_{:03d}'.format(self._side , self._name , self._rtype , index + 1))
			self.iris_jnt_list.append(
					'jnt_{}_{}{}iris_{:03d}'.format(self._side , self._name , self._rtype , index + 1))
	
	
	
	def create_bpjnt(self) :
		# 获得jaw_bpjnt 的路径
		self.jaw_bpjnt_path = os.path.abspath(__file__ + "/../eye_bpjnt.ma")
		# 导入关节
		cmds.file(self.jaw_bpjnt_path , i = True , rnn = True)
	
	
	
	def create_joint(self) :
		# 创建眼球的关节
		for bpjnt , jnt in zip(self.bpjnt_list , self.jnt_list) :
			self.jnt = cmds.createNode('joint' , name = jnt , parent = self.joint_parent)
			cmds.parentConstraint(bpjnt , self.jnt , mo = False)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.jnt
		
		# 创建iris的关节
		for bpjnt , jnt in zip(self.iris_bpjnt_list , self.iris_jnt_list) :
			self.jnt = cmds.createNode('joint' , name = jnt , parent = self.joint_parent)
			cmds.parentConstraint(bpjnt , self.jnt , mo = False)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.jnt
		
		# 删除bp的定位关节
		cmds.delete(self.bpjnt_list[0])
		# 进行关节定向
		jointUtils.Joint.joint_orientation(self.jnt_list)
		jointUtils.Joint.joint_orientation(self.iris_jnt_list)
	
	
	
	def create_ctrl(self) :
		# 创建控制器总体的层级组
		self.ctrl_grp = cmds.createNode('transform' , parent = self.control_parent , name = self.ctrl_grp)
		# 创建控制器
		parent = self.ctrl_grp
		for index , ctrl in enumerate(self.ctrl_list) :
			self.ctrl = controlUtils.Control.create_ctrl(ctrl , shape = 'circle' ,
			                                             radius = self.radius ,
			                                             axis = 'X+' , pos = self.jnt_list[index] ,
			                                             parent = parent)
			parent = self.ctrl.replace('ctrl' , 'output')
			# 移动控制器的位置
			cmds.setAttr(self.zero_list[index] + '.translateX' ,
			             cmds.getAttr(self.zero_list[index] + '.translateX') + 0.25 * index)
		
		# 创建aim控制器用于做目标约束
		self.aim_ctrl = controlUtils.Control.create_ctrl(self.aim_ctrl , shape = 'shape_040' ,
		                                                 radius = self.radius ,
		                                                 axis = 'Z+' , pos = self.jnt_list[0] ,
		                                                 parent = self.ctrl_grp)
		# 移动aim控制器的位置
		self.aim_zero = self.aim_ctrl.replace('ctrl' , 'zero')
		# 移动控制器的位置
		cmds.setAttr(self.aim_zero + '.translateZ' ,
		             cmds.getAttr(self.aim_zero + '.translateZ') + 3)
		
		## 创建曲线指示器
		# 创建aim控制器的loc来记录位置
		self.aim_loc = cmds.spaceLocator(name = self.aim_loc)[0]
		cmds.matchTransform(self.aim_loc , self.aim_ctrl , position = True , rotation =
		True ,
		                    scale = True)
		cmds.parent(self.aim_loc , self.aim_ctrl)
		cmds.setAttr(self.aim_loc + '.visibility' , 0)
		# 创建jnt的loc来记录位置
		self.jnt_loc = cmds.spaceLocator(name = self.jnt_loc)[0]
		cmds.matchTransform(self.jnt_loc , self.jnt_list[0] , position = True , rotation = True , scale = True)
		cmds.parent(self.jnt_loc , self.jnt_list[0])
		cmds.setAttr(self.jnt_loc + '.visibility' , 0)
		
		# 连接loc和曲线来表示位置
		self.aim_crv = cmds.curve(degree = 1 , point = [(0.0 , 0.0 , 0.0) , (0.0 , 0.0 , 0.0)] ,
		                          name = self.aim_crv)
		aim_loc_shape = cmds.listRelatives(self.aim_loc , shapes = True)[0]
		jnt_loc_shape = cmds.listRelatives(self.jnt_loc , shapes = True)[0]
		aim_curve_shape = cmds.listRelatives(self.aim_crv , shapes = True)[0]
		
		# 连接曲线与loc
		cmds.connectAttr(aim_loc_shape + '.worldPosition[0]' , aim_curve_shape + '.controlPoints[0]')
		cmds.connectAttr(jnt_loc_shape + '.worldPosition[0]' , aim_curve_shape + '.controlPoints[1]')
		# 设置曲线的可见性
		cmds.setAttr(aim_curve_shape + '.overrideEnabled' , 1)
		cmds.setAttr(aim_curve_shape + '.overrideDisplayType' , 2)
		cmds.setAttr(self.aim_crv + '.inheritsTransform' , 0)
		cmds.parent(self.aim_crv , self.ctrl_grp)
	
	
	
	def add_constraint(self) :
		u"""
		创建约束
		"""
		super().add_constraint()
		# 创建目标约束
		self.aim_output = self.aim_ctrl.replace('ctrl' , 'output')
		cmds.aimConstraint(self.aim_output , self.ctrl_list[0] , offset = (0 , 0 , 0) , weight = 1 ,
		                   aimVector = (1 , 0 , 0) , upVector = (
					
					0 , 1 , 0) , worldUpType = "vector" , worldUpVector = (0 , 1 , 0))



if __name__ == "__main__" :
	def build_setup() :
		eye_l = eye.Eye(side = 'l' , joint_parent = None , control_parent = None)
		eye_l.build_setup()
	
	
	
	def build_rig() :
		eye_l = eye.Eye(side = 'l' , joint_parent = None , control_parent = None)
		eye_l.build_rig()
	
	
	
	#
	# #
	build_setup()
	build_rig()
