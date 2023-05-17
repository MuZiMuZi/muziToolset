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
	
	
	
	def __init__(self , side = '' , name = '' , joint_number = 1 , joint_parent = None , control_parent = None) :
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
		# 创建左边的眉毛曲线和曲面名称
		self.brow_l.drive_crv = self.brow_l.bpjnt_list[0].replace('bpjnt' , 'crv')
		self.brow_l.drive_suf = self.brow_l.bpjnt_list[0].replace('bpjnt' , 'suf')
		
		# 创建右边的眉毛曲线和曲面名称
		self.brow_r.drive_crv = self.brow_r.bpjnt_list[0].replace('bpjnt' , 'crv')
		self.brow_r.drive_suf = self.brow_r.bpjnt_list[0].replace('bpjnt' , 'suf')
	
	
	
	def create_bpjnt(self) :
		# 获得brow_bpjnt 的路径
		self.brow_bpjnt_path = os.path.abspath(__file__ + "/../brow_bpjnt.ma")
		# 导入关节
		cmds.file(self.brow_bpjnt_path , i = True , rnn = True)
	
	
	
	def create_suf(self) :
		u"""
		创建用于眉毛部位的曲面
		"""
		
		# 创建左边的bp定位眉毛曲线
		self.brow_l.drive_crv = pipelineUtils.Pipeline.create_curve_on_joints(self.brow_l.bpjnt_list ,
		                                                                      self.brow_l.drive_crv , degree = 3
		                                                                      )
		# 放样曲线出曲面
		# 通过两条曲线来放样制作左边眉毛的曲面
		self.brow_l.drive_suf = pipelineUtils.Pipeline.create_surface_on_curve(self.brow_l.drive_crv ,
		                                                                       self.brow_l.drive_suf , spans = 6 ,
		                                                                       offset = 0.2)
		
		# 创建右边的bp定位眉毛曲线
		self.brow_r.drive_crv = pipelineUtils.Pipeline.create_curve_on_joints(self.brow_r.bpjnt_list ,
		                                                                      self.brow_r.drive_crv , degree = 3
		                                                                      )
		# 放样曲线出曲面
		# 通过两条曲线来放样制作右边眉毛的曲面
		self.brow_r.drive_suf = pipelineUtils.Pipeline.create_surface_on_curve(self.brow_r.drive_crv ,
		                                                                       self.brow_r.drive_suf , spans = 6 ,
		                                                                       offset = 0.2)
	
	
	
	def create_joint(self) :
		self.create_suf()
		super().create_joint()
