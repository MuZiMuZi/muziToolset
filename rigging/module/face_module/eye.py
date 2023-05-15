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
		self.radius = 0.5
		
		# iris的缩放关节
		self.iris_bpjnt_list = list()
		self.iris_jnt_list = list()
	
	
	def create_namespace(self) :
		super().create_namespace()
		self.aim_ctrl = ('ctrl_{}_{}{}Aim_001'.format(self._side , self._name , self._rtype))
		self.aim_loc = ('loc{}_{}{}Aim_001'.format(self._side , self._name , self._rtype))
		for index in range(3) :
			self.iris_bpjnt_list.append('bpjnt_{}_{}{}iris_{:03d}'.format(self._side , self._name , self._rtype , index+1))
			self.iris_jnt_list.append('jnt_{}_{}{}iris_{:03d}'.format(self._side , self._name , self._rtype , index + 1))
		
	
	
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
		             cmds.getAttr(self.aim_zero + '.translateZ') + 5)
		
		## 创建曲线指示器
		# 创建pv控制器的loc来记录位置
		midIK_pv_loc = cmds.spaceLocator(name = self.pv_loc)[0]
		cmds.matchTransform(midIK_pv_loc , self.pv_ctrl.replace('ctrl' , 'output') , position = True , rotation =
		True ,
		                    scale = True)
		cmds.parent(midIK_pv_loc , self.pv_ctrl)
		cmds.setAttr(midIK_pv_loc + '.visibility' , 0)
		# 创建pvjnt的loc来记录位置
		midIK_jnt_loc = cmds.spaceLocator(name = self.jnt_loc)[0]
		cmds.matchTransform(midIK_jnt_loc , self.jnt_list[1] , position = True , rotation = True , scale = True)
		cmds.parent(midIK_jnt_loc , self.jnt_list[1])
		cmds.setAttr(midIK_jnt_loc + '.visibility' , 0)
		
		# 连接loc和曲线来表示位置
		ikpv_curve = cmds.curve(degree = 1 , point = [(0.0 , 0.0 , 0.0) , (0.0 , 0.0 , 0.0)] ,
		                        name = self.pv_curve)
		midIK_jnt_loc_shape = cmds.listRelatives(midIK_jnt_loc , shapes = True)[0]
		midIK_pv_loc_shape = cmds.listRelatives(midIK_pv_loc , shapes = True)[0]
		ikpv_curve_shape = cmds.listRelatives(ikpv_curve , shapes = True)[0]
		
		# 连接曲线与loc
		cmds.connectAttr(midIK_jnt_loc_shape + '.worldPosition[0]' , ikpv_curve_shape + '.controlPoints[0]')
		cmds.connectAttr(midIK_pv_loc_shape + '.worldPosition[0]' , ikpv_curve_shape + '.controlPoints[1]')
		# 设置曲线的可见性
		cmds.setAttr(ikpv_curve_shape + '.overrideEnabled' , 1)
		cmds.setAttr(ikpv_curve_shape + '.overrideDisplayType' , 2)
		cmds.setAttr(ikpv_curve + '.inheritsTransform' , 0)
		cmds.parent(ikpv_curve , self.ctrl_grp)
	
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
