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
from ....core import controlUtils , hierarchyUtils , jointUtils



class Brow(base.Base) :
	
	
	
	def __init__(self , side = 'm' , name = '' , joint_number = 1 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		self._rtype = 'Brow'
		
		# 创建两边的眉毛系统
		self.brow_l = base.Base(side = 'l' , name = '' , joint_number = 4 , joint_parent = None , control_parent =
		None)
		self.brow_r = base.Base(side = 'r' , name = '' , joint_number = 4 , joint_parent = None , control_parent =
		None)
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		# 创建两边的眉毛名称规范
		self.brow_l.create_namespace()
		self.brow_r.create_namespace()
	
	
	
	def create_bpjnt(self) :
		# 获得brow_bpjnt 的路径
		self.brow_bpjnt_path = os.path.abspath(__file__ + "/../brow_bpjnt.ma")
		# 导入关节
		cmds.file(self.brow_bpjnt_path , i = True , rnn = True)
	
	
	
