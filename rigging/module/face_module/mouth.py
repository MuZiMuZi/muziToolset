# coding=utf,8
'''
嘴巴的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base , bone
from ...chain import chain , chainFK
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils
from . import mouthLip



reload(mouthLip)



class Mouth(bone.Bone) :
	
	
	
	def __init__(self , side , name , joint_number = 7 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		
		self._rtype = 'Mouth'
		# 生成上部分的嘴唇
		self.mouth_lip_upper = mouthLip.MouthLip(side = self.side , name = 'upper' , joint_number = 7 ,
		                                         joint_parent = None ,
		                                         control_parent = None)
		
		# 生成下部分的嘴唇
		self.mouth_lip_lower = mouthLip.MouthLip(side = self.side , name = 'lower' , joint_number = 7 ,
		                                         joint_parent = None ,
		                                         control_parent = None)
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		self.mouth_lip_upper.create_namespace()
		self.mouth_lip_lower.create_namespace()
		## 创建嘴内侧和嘴外侧的控制器
		self.inn_ctrl = 'ctrl_{}_{}{}Inn_001'.format(self.side , self._name , self._rtype)
		self.out_ctrl = 'ctrl_{}_{}{}Out_001'.format(self.side , self._name , self._rtype)
	
	
	
	def create_bpjnt(self) :
		# 创建上下嘴唇的控制器曲线
		self.mouth_lip_upper.build_curve()
		self.mouth_lip_lower.build_curve()
	
	
	
	def create_joint(self) :
		# 创建上下嘴唇的曲线
		self.mouth_lip_upper.create_joint()
		self.mouth_lip_lower.create_joint()
	
	
	
	def create_ctrl(self) :
		# 创建整体的控制器层级组
		self.ctrl_grp = cmds.createNode('transform' , name = self.ctrl_grp , parent = self.control_parent)
		# 创建上下嘴唇的控制器
		self.mouth_lip_upper.create_ctrl()
		self.mouth_lip_lower.create_ctrl()
		
		# 创建嘴内侧与嘴外侧的控制器
		
		self.inn_ctrl = controlUtils.Control.create_ctrl(self.inn_ctrl , shape = 'ball' , axis = 'X+' , radius = 0.1 ,
		                                                 pos = self.mouth_lip_upper.zero_list[0] , parent = self.ctrl_grp)
		self.out_ctrl = controlUtils.Control.create_ctrl(self.out_ctrl , shape = 'ball' , axis = 'X+' , radius = 0.1 ,
		                                                 pos = self.mouth_lip_lower.zero_list[-1] , parent = self.ctrl_grp)
	
		# 整理控制器的层级结构
		cmds.parent(self.mouth_lip_upper.ctrl_grp,self.mouth_lip_lower.ctrl_grp,self.ctrl_grp)
	
	def add_constraint(self) :
		# 创建上下嘴唇的约束
		self.mouth_lip_upper.add_constraint()
		self.mouth_lip_lower.add_constraint()
		
		# 嘴角内侧控制器对上下嘴唇的内侧控制器做约束
		cmds.parentConstraint(self.inn_ctrl.replace('ctrl' , 'output') , self.mouth_lip_upper.driven_list[0])
		cmds.parentConstraint(self.inn_ctrl.replace('ctrl' , 'output') , self.mouth_lip_lower.driven_list[0])
		# 隐藏上下嘴唇的内侧控制器
		cmds.setAttr(self.mouth_lip_upper.zero_list[0] + '.v' , 0)
		cmds.setAttr(self.mouth_lip_lower.zero_list[0] + '.v' , 0)
		# 嘴角外侧控制器对上下嘴唇的外侧控制器做约束
		cmds.parentConstraint(self.out_ctrl.replace('ctrl' , 'output') , self.mouth_lip_upper.driven_list[-1])
		cmds.parentConstraint(self.out_ctrl.replace('ctrl' , 'output') , self.mouth_lip_lower.driven_list[-1])
		# 隐藏上下嘴唇的外侧控制器
		cmds.setAttr(self.mouth_lip_upper.zero_list[-1] + '.v' , 0)
		cmds.setAttr(self.mouth_lip_lower.zero_list[-1] + '.v' , 0)
