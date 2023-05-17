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
		self.radius = 0.25
		self.shape = 'cube'
		self._rtype = 'Brow'
		
		# 创建两边的眉毛系统
		self.brow_l = base.Base(side = 'l' , name = '' , joint_number = 4 , joint_parent = None , control_parent =
		None)
		self.brow_l._rtype = 'Brow'
		self.brow_l.shape = 'cube'
		self.brow_l.radius = 0.25
		
		
		self.brow_r = base.Base(side = 'r' , name = '' , joint_number = 4 , joint_parent = None , control_parent =
		None)
		self.brow_r._rtype = 'Brow'
		self.brow_r.shape = 'cube'
		self.brow_r.radius = 0.25
	
	
	
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
		                                                                       offset = 0.1)
		# cmds.parent(self.brow_l.drive_suf,self.ctrl_grp)
		
		# 创建右边的bp定位眉毛曲线
		self.brow_r.drive_crv = pipelineUtils.Pipeline.create_curve_on_joints(self.brow_r.bpjnt_list ,
		                                                                      self.brow_r.drive_crv , degree = 3
		                                                                      )
		# 放样曲线出曲面
		# 通过两条曲线来放样制作右边眉毛的曲面
		self.brow_r.drive_suf = pipelineUtils.Pipeline.create_surface_on_curve(self.brow_r.drive_crv ,
		                                                                       self.brow_r.drive_suf , spans = 6 ,
		                                                                       offset = 0.1)
		# cmds.parent(self.brow_r.drive_suf , self.ctrl_grp)
	
	
	
	def create_joint(self) :
		self.create_suf()
		super().create_joint()
		
		# 创建眉毛右边的关节
		self.brow_r.create_joint()
		# 右边的关节对曲面进行蒙皮
		cmds.skinCluster(self.brow_r.jnt_list ,self.brow_r.drive_suf , tsb = True)
		
		# 创建眉毛左边的关节
		self.brow_l.create_joint()
		
		# 左边的关节对曲面进行蒙皮
		cmds.skinCluster(self.brow_l.jnt_list , self.brow_l.drive_suf , tsb = True)
		
	def create_folice(self):
		u"""
		对曲面创建毛囊，并且创建权重的关节
		"""
		pass
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		# 创建眉毛右边的控制器
		self.brow_r.create_ctrl()
		cmds.parent(self.brow_r.drive_suf , self.brow_r.ctrl_grp)
		# 创建眉毛左边的控制器
		self.brow_l.create_ctrl()
		cmds.parent(self.brow_l.drive_suf , self.brow_l.ctrl_grp)

	