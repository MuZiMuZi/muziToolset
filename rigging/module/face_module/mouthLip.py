# coding=utf,8
'''
嘴唇的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base , bone
from ...chain import chain , chainFK
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils



reload(pipelineUtils)



class MouthLip(bone.Bone) :
	
	
	
	def __init__(self , side , name , joint_number = 7 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		# 定位用的曲线
		self._name = name
		self.shape = 'cube'
		self._rtype = 'MouthLip'
		self.radius = 0.1
		self.joint_number = joint_number
		
		self.curve_jnt_list = list()
		self.skin_jnt_list = list()
		self.skin_curve = 'crv_{}_{}{}Skin_001'.format(self._side , self._name , self._rtype)
		
		# 判断是否为下部分的嘴唇,如果为下部分的嘴唇的话，scaleY需要设置成-1，这样上下运动的时候才可匹配
		if self._name == 'lower' :
			self.Y_value = -1
		else :
			self.Y_value = 1
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		# 整理与控制器有关的曲线的名称规范层级结构
		self.curve = 'crv_{}_{}{}_001'.format(self._side , self._name , self._rtype)
		for index in range(7) :
			self.curve_jnt_list.append('jnt_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , index + 1))
		self.curve_jnt_grp = 'grp_{}_{}{}Jnts_001'.format(self._side , self._name , self._rtype)
		self.curve_nodes_grp = 'grp_{}_{}{}RigNodes_001'.format(self._side , self._name , self._rtype)
		
		# 整理与蒙皮关节有关的曲线名称规范层级结构
		# 获取蒙皮曲线的关节点数量
		self.skin_number = pipelineUtils.Pipeline.get_curve_number(self.skin_curve)
		for index in range(self.skin_number) :
			self.skin_jnt_list.append(
					'jnt_{}_{}{}Skin_{:03d}'.format(self._side , self._name , self._rtype , index + 1))
		self.skin_jnt_grp = 'grp_{}_{}{}SkinJnts_001'.format(self._side , self._name , self._rtype)
		self.skin_nodes_grp = 'grp_{}_{}{}SkinRigNodes_001'.format(self._side , self._name , self._rtype)
		
		# 整理与目标曲线有关的曲线名称规范层级结构
		self.aim_curve = 'crv_{}_{}{}Aim_001'.format(self._side , self._name , self._rtype)
		self.aim_jnt_grp = 'grp_{}_{}{}AimJnts_001'.format(self._side , self._name , self._rtype)
		self.aim_nodes_grp = 'grp_{}_{}{}AimRigNodes_001'.format(self._side , self._name , self._rtype)
		
		# 整理与向上向量曲线有关的曲线名称规范层级结构
		self.up_curve = 'crv_{}_{}{}Up_001'.format(self._side , self._name , self._rtype)
		self.up_jnt_grp = 'grp_{}_{}{}UpJnts_001'.format(self._side , self._name , self._rtype)
		self.up_nodes_grp = 'grp_{}_{}{}UpRigNodes_001'.format(self._side , self._name , self._rtype)
		
		# 整理节点的层级结构
		self.node_grp = 'grp_{}_{}{}Nodes_001'.format(self._side , self._name , self._rtype)
	
	
	
	def build_curve(self) :
		u"""
				根据选择的模型点创建用于定位的曲线来创建控制器曲线
		"""
		
		# 根据skin_curve来制作curve，用于制作控制器的控制
		self.curve = cmds.duplicate(self.skin_curve , name = self.curve)[0]
		cmds.setAttr(self.skin_curve + '.visibility' , 0)
		# 重建self.curve用来控制曲线
		self.curve = \
			cmds.rebuildCurve(self.curve , ch = 1 , rpo = 1 , rt = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 , kt = 0 ,
			                  s = 4 , d = 3 , tol = 0.01)[0]
		cmds.setAttr(self.curve + '.visibility' , 1)
		
		# 在曲线上创建关节用来蒙皮曲线创建控制器的约束
		cmds.select(self.curve)
		self.curve_jnt_dict = jointUtils.Joint.create_joints_on_curve(is_parent = False)
		curve_jnt_list = self.curve_jnt_dict['jnt_list']
		# 重命名控制器关节和层级结构的名称
		for index , jnt in enumerate(curve_jnt_list) :
			cmds.rename(jnt , self.curve_jnt_list[index])
		self.curve_jnt_grp = cmds.rename(self.curve_jnt_dict['jnt_grp'] , self.curve_jnt_grp)
		self.curve_nodes_grp = cmds.rename(self.curve_jnt_dict['node_grp'] , self.curve_nodes_grp)
		# 蒙皮曲线
		cmds.skinCluster(self.curve_jnt_list , self.curve)
		
		# 根据skin_curve来创建蒙皮关节
		cmds.select(self.skin_curve)
		self.skin_jnt_dict = jointUtils.Joint.create_joints_on_curve(is_parent = False)
		skin_jnt_list = self.skin_jnt_dict['jnt_list']
		self.skin_jnt_grp = cmds.rename(self.skin_jnt_dict['jnt_grp'] , self.skin_jnt_grp)
		self.skin_nodes_grp = cmds.rename(self.skin_jnt_dict['node_grp'] , self.skin_nodes_grp)
		for index , jnt in enumerate(skin_jnt_list) :
			cmds.rename(jnt , self.skin_jnt_list[index])
		# 控制器曲线对蒙皮曲线做wire变形，让控制器曲线控制蒙皮曲线,注意如果是两条曲线做wire变形器的话，被控制的曲线需要给个w参数
		wire_node = cmds.wire(self.skin_curve , w = self.curve , gw = False , en = 1.000000 , ce = 0.000000 ,
		                      li = 0.000000)[0]
		cmds.setAttr(wire_node + '.dropoffDistance[0]' , 200)
		cmds.setAttr(self.skin_jnt_grp + '.v' , 0)
	
	
	
	def create_joint(self) :
		u'''
		创建嘴唇的权重关节在曲线上
		'''
		# 将控制器的关节进行隐藏
		cmds.setAttr(self.curve_jnt_grp + '.visibility' , 0)
		# 根据curve来制作aim_curve，用于制作控制器的目标曲线,并且移动目标曲线的位置
		self.aim_curve = cmds.duplicate(self.curve , name = self.aim_curve)[0]
		cmds.setAttr(self.aim_curve + '.visibility' , 0)
		cmds.setAttr(self.aim_curve + '.translateZ' , lock = False)
		cmds.setAttr(self.aim_curve + '.translateZ' , cmds.getAttr(self.aim_curve + '.translateZ') + 0.1)
		
		# 根据curve来制作up_curve，用于制作控制器的向上参考曲线,并且移动向上曲线的位置
		self.up_curve = cmds.duplicate(self.curve , name = self.up_curve)[0]
		cmds.setAttr(self.up_curve + '.visibility' , 0)
		cmds.setAttr(self.up_curve + '.translateY' , lock = False)
		# 向上曲线的位置距离可以适当调整大一点，防止翻转曲线的轴向
		cmds.setAttr(self.up_curve + '.translateY' , cmds.getAttr(self.up_curve + '.translateY') + 0.8)
		# 创建三条曲线的目标约束
		con_dict = pipelineUtils.Pipeline.attach_joints_on_curve(self.skin_jnt_list , self.curve , self.aim_curve ,
		                                                         self.up_curve ,
		                                                         aim_type = 'curve')
		self.con_nodes_grp = con_dict['nodes_grp']
		self.skin_jnt_grp = con_dict['jnts_grp']
		# 整理节点的层级结构
		self.node_grp = cmds.createNode('transform' , name = self.node_grp , parent = '_node')
		cmds.parent(self.skin_nodes_grp , self.curve_nodes_grp , self.con_nodes_grp , self.node_grp)
		cmds.parent(self.skin_jnt_grp , '_joint')
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		# 设置offset组的偏移值，上下运动才可匹配
		for offset in self.offset_list :
			cmds.setAttr(offset + '.scaleY' , 1 * self.Y_value)
	
	
	
	def add_constraint(self) :
		super().add_constraint()
		# 控制器之间需要添加约束
		# ctrl_list =
		# [0,3,6]
		# [0,2,3]
		# [0,1,2]
		# [3,4,6]
		# [4,5,6]
		# 约束中间的控制器[0,2,3]，两侧的控制器约束中间的控制器
		cmds.pointConstraint(self.output_list[0] , self.output_list[3] , self.driven_list[2] , mo = True)
		
		# 约束中间的控制器[0,1,2]，两侧的控制器约束中间的控制器
		cmds.pointConstraint(self.output_list[0] , self.output_list[2] , self.driven_list[1] , mo = True)
		
		# 约束中间的控制器[3,4,6]，两侧的控制器约束中间的控制器
		cmds.pointConstraint(self.output_list[3] , self.output_list[6] , self.driven_list[4] , mo = True)
		
		# 约束中间的控制器[4,5,6]，两侧的控制器约束中间的控制器
		cmds.pointConstraint(self.output_list[4] , self.output_list[6] , self.driven_list[5])
		
		# 第二个控制器和第六个控制器是为了调整小的形态，默认是隐藏的,连接他们的可见性到中间的控制器上
		cmds.addAttr(self.ctrl_list[3] , attributeType = 'bool' , longName = 'LidSubCtrlVis' , keyable = 1 ,
		             defaultValue = 0)
		
		# 连接可见性
		cmds.connectAttr(self.ctrl_list[3] + '.LidSubCtrlVis' , self.ctrl_list[1] + '.visibility')
		cmds.connectAttr(self.ctrl_list[3] + '.LidSubCtrlVis' , self.ctrl_list[5] + '.visibility')
		
		# 设置曲线的可见性
		cmds.setAttr(self.curve + '.visibility' , 0)
		cmds.setAttr(self.skin_curve + '.visibility' , 0)
		# 设置关节的可见性
		cmds.setAttr(self.skin_jnt_grp + '.v' , 1)
		cmds.setAttr(self.curve_jnt_grp + '.v' , 0)
