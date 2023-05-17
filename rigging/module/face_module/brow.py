# coding=utf-8
'''
眉毛的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base , bone
from ...chain import chain , chainFK
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils



reload(pipelineUtils)



class Brow(base.Base) :
	
	
	
	def __init__(self , side = 'm' , name = '' , joint_number = 1 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		self._rtype = 'Brow'
		
		# 创建两边的眉毛系统
		self.brow_l = base.Base(side = 'l' , name = '' , joint_number = 4 , joint_parent = None , control_parent =
		None)
		self.brow_l._rtype = 'Brow'
		self.brow_r = base.Base(side = 'r' , name = '' , joint_number = 4 , joint_parent = None , control_parent =
		None)
		self.brow_r._rtype = 'Brow'
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		# 创建两边的眉毛名称规范
		self.brow_l.create_namespace()
		self.brow_r.create_namespace()
		# 创建左边的眉毛曲线名称
		self.brow_l.bpjnt_crv = self.brow_l.bpjnt_list[0].replace('jnt' , 'crv')
		self.brow_l.aim_crv = self.brow_l.bpjnt_list[0].replace('bpjnt' , 'aimcrv')
		
		# 创建右边的眉毛曲线名称
		self.brow_r.bpjnt_crv = self.brow_r.bpjnt_list[0].replace('jnt' , 'crv')
		self.brow_r.aim_crv = self.brow_r.bpjnt_list[0].replace('bpjnt' , 'aimcrv')
	
	
	
	def create_bpjnt(self) :
		# 获得brow_bpjnt 的路径
		self.brow_bpjnt_path = os.path.abspath(__file__ + "/../brow_bpjnt.ma")
		# 导入关节
		cmds.file(self.brow_bpjnt_path , i = True , rnn = True)
	
	
	
	def create_bpcrv(self) :
		u"""
		创建用于约束关节的曲线
		"""
		
		# 创建左边的bp定位眉毛曲线
		self.brow_l.bpjnt_crv = pipelineUtils.Pipeline.create_curve_on_joints(self.brow_l.bpjnt_list ,
		                                                                      self.brow_l.bpjnt_crv , degree = 3
		                                                                      )
		# 创建右边的bp定位眉毛曲线
		self.brow_r.bpjnt_crv = pipelineUtils.Pipeline.create_curve_on_joints(self.brow_r.bpjnt_list ,
		                                                                      self.brow_r.bpjnt_crv , degree = 3
		                                                                      )
	
	
	
	def create_crv(self) :
		u"""
		创建用于目标约束的曲线
		"""
		# 创建左边的aim目标约束的眉毛曲线
		self.brow_l.aim_crv = cmds.duplicate(self.brow_l.bpjnt_crv , name = self.brow_l.aim_crv)[0]
		cmds.move(0 , 0 , 0.75 , self.brow_l.aim_crv , absolute = True)
		# 创建右边的aim目标约束的眉毛曲线
		self.brow_r.aim_crv = cmds.duplicate(self.brow_r.bpjnt_crv , name = self.brow_r.aim_crv)[0]
		cmds.move(0 , 0 , 0.75 , self.brow_r.aim_crv , absolute = True)
		
	
	
	def create_joint(self) :
		self.create_bpcrv()
		self.create_crv()
		super().create_joint()
