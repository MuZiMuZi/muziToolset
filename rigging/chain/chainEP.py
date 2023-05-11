import maya.cmds as cmds

from . import chain
from ..base import bone,base
from ...core import vectorUtils , controlUtils,pipelineUtils
from importlib import reload
reload(pipelineUtils)
class ChainEP(base.Base):
	
	
	
	def __init__(self , side , name , index , controller_number , curve , joint_parent = None , control_parent = None) :
		super().__init__(side , name , index , joint_parent , control_parent)
		u'''给定一根曲线，根据曲线的长度来创建关节和控制器
		controller_number：生成的控制器数量
		crv_node：需要创建控制器与关节的曲线
		'''
		self._rtype = 'ChainEP'
		self.controller_number = controller_number
		self.curve = curve
		self.radius = 3
		self.set_shape('ball')
	
	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		bpjnt_list = pipelineUtils.Pipeline.create_joints_on_curve(self.curve , self.controller_number)
		for index , bpjnt in enumerate(bpjnt_list) :
			bpjnt = cmds.rename(bpjnt , self.bpjnt_list[index])
			cmds.parent(bpjnt,self.joint_parent)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = bpjnt
	
	
	
	def create_joint(self) :
		# 根据bp关节创建新的关节
		for bpjnt , jnt in zip(self.bpjnt_list , self.jnt_list) :
			jnt = cmds.createNode('joint' , name = jnt , parent = self.joint_parent)
			cmds.matchTransform(jnt , bpjnt)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = jnt
		cmds.delete(self.bpjnt_list[0])
	
	
	
	
	
	
	
	
	
	
		
	
		