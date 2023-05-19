# coding=utf,8
'''
眼皮的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base , bone
from ...chain import chain , chainFK
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils



class EyeLid(bone.Bone) :
	
	
	
	def __init__(self , side , name ,joint_number = 7 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		#定位用的曲线
		self.skin_curve = 'crv_{}_{}{}Skin_001'.format(self._side , self._name , self._rtype)
		
		self.shape = 'cube'
		self._rtype = 'EyeLid'
		self.radius = 0.05
		self.joint_number = joint_number
		self.curve_jnt_list = list()
	
	
	
	def create_namespace(self) :
		u"""
		创建名称规范整理
		"""
		super().create_namespace()
		# 整理与控制器有关的曲线的名称规范层级结构
		self.curve = 'crv_{}_{}{}_001'.format(self._side , self._name , self._rtype)
		for index in range(7) :
			self.curve_jnt_list.append('jnt_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , index + 1))
		self.curve_jnt_grp = 'grp_{}_{}{}Jnts_001'.format(self._side , self._name , self._rtype)
		self.curve_nodes_grp = 'grp_{}_{}{}RigNodes_001'.format(self._side , self._name , self._rtype)
		
		# 整理与蒙皮关节有关的曲线名称规范层级结构
		self.skin_curve = 'crv_{}_{}{}Skin_001'.format(self._side , self._name , self._rtype)
		self.skin_jnt_grp = 'grp_{}_{}{}SkinJnts_001'.format(self._side , self._name , self._rtype)
		
		# 整理眼睛的关节和向上方向的参考向量的名称规范层级结构
		self.eye_jnt = 'jnt_{}_Eye_001'.format(self._side)
		self.eye_up_loc = 'loc_{}_EyeUp_001'.format(self._side)
		self.eye_up_zero = 'zero_{}_EyeUp_001'.format(self._side)
	
	
	
	def build_curve(self) :
		u"""
		根据选择的模型点创建用于定位的曲线
		"""
		
		# 根据skin_curve来制作curve，用于制作控制器的控制
		self.curve = cmds.duplicate(self.skin_curve , name = self.curve)[0]
		cmds.setAttr(self.skin_curve + '.visibility' , 0)
		# 重建self.curve用来控制曲线
		self.curve = \
			cmds.rebuildCurve(self.curve , ch = 1 , rpo = 1 , rt = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 , kt = 0 ,
			                  s = 4 , d = 3 , tol = 0.01)[0]
		
		# 在曲线上创建关节用来蒙皮曲线创建控制器的约束
		cmds.select(self.curve)
		jnt_list = jointUtils.Joint.create_joints_on_curve(is_parent = False)['jnt_list']
		# 重命名蒙皮关节和层级结构的名称
		for index , jnt in enumerate(jnt_list) :
			cmds.rename(jnt , self.curve_jnt_list[index])
		self.curve_jnt_grp = cmds.rename('grp_{}Jnts'.format(self.curve) , self.curve_jnt_grp)
		self.curve_nodes_grp = cmds.rename('grp_{}RigNodes'.format(self.curve) , self.curve_nodes_grp)
		# 蒙皮曲线
		cmds.skinCluster(self.curve_jnt_list , self.curve)
		
		# 控制器曲线对蒙皮曲线做wire变形，让控制器曲线控制蒙皮曲线,注意如果是两条曲线做wire变形器的话，被控制的曲线需要给个w参数
		wire_node = cmds.wire(self.skin_curve , w = self.curve , gw = False , en = 1.000000 , ce = 0.000000 ,
		                      li = 0.000000)[0]
		cmds.setAttr(wire_node + '.dropoffDistance[0]' , 200)
	
	
	
	def create_joint(self) :
		u'''
		创建眼皮的权重关节在曲线上
		'''
		# 将控制器的关节进行隐藏
		cmds.setAttr(self.curve_jnt_grp + '.visibility' , 0)
		# 判断向上的目标物体是否存在，如果不存在的话则创建
		if cmds.objExists(self.eye_up_loc) :
			pass
		else :
			self.eye_up_zero = cmds.createNode('transform' , name = self.eye_up_zero)
			self.eye_up_loc = cmds.spaceLocator(name = self.eye_up_loc)[0]
			cmds.parent(self.eye_up_loc , self.eye_up_zero)
			cmds.matchTransform(self.eye_up_zero , self.eye_jnt)
			cmds.setAttr(self.eye_up_loc + '.translateY' , 5)
		# 创建眼皮的权重关节在曲线上
		pipelineUtils.Pipeline.create_eyelid_joints_on_curve(self.skin_curve , self.eye_jnt , self.eye_up_loc)
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
	
	
	
	def add_constraint(self) :
		super().add_constraint()
		
		# 控制器之间需要添加约束
		# ctrl_list =
		# [0,3,6]
		# [0,2,3]
		# [0,1,2]
		# [3,4,6]
		# [4,5,6]
		
		# 首端控制器和末端控制器约束中间的控制器,在列表里是[0,3,6]
		cmds.parentConstraint(self.output_list[0] , self.output_list[6] , self.driven_list[3] , mo = True)
		
		# 约束中间的控制器[0,2,3]，两侧的控制器约束中间的控制器
		cmds.parentConstraint(self.output_list[0] , self.output_list[3] , self.driven_list[2] , mo = True)
		
		# 约束中间的控制器[0,1,2]，两侧的控制器约束中间的控制器
		cmds.parentConstraint(self.output_list[0] , self.output_list[2] , self.driven_list[1] , mo = True)
		
		# 约束中间的控制器[3,4,6]，两侧的控制器约束中间的控制器
		cmds.parentConstraint(self.output_list[3] , self.output_list[6] , self.driven_list[4] , mo = True)
		
		# 约束中间的控制器[4,5,6]，两侧的控制器约束中间的控制器
		cmds.parentConstraint(self.output_list[4] , self.output_list[6] , self.driven_list[5])
		
		# 第二个控制器和第六个控制器是为了调整小的形态，默认是隐藏的,连接他们的可见性到中间的控制器上
		cmds.addAttr(self.ctrl_list[3] , attributeType = 'bool' , longName = 'LidSubCtrlVis' , keyable = 1 ,
		             defaultValue = 0)
		
		# 连接可见性
		cmds.connectAttr(self.ctrl_list[3] + '.LidSubCtrlVis' , self.ctrl_list[1] + '.visibility')
		cmds.connectAttr(self.ctrl_list[3] + '.LidSubCtrlVis' , self.ctrl_list[5] + '.visibility')
	
	
	
	
	
	
	def build_setup(self) :
		"""
		创建定位曲线,生成准备
		"""
		self.create_namespace()
	
	
	
	def build_rig(self) :
		self.create_namespace()
		self.create_joint()
		self.create_ctrl()
		self.add_constraint()
		self.add_connect()
