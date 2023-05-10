from ..base import base
import maya.cmds as cmds
from ...core import pipelineUtils
from ...core import vectorUtils
import math

from importlib import reload
reload(vectorUtils)
class Chain(base.Base) :
	
	
	
	def __init__(self , side , name , index , length = 10 , joint_parent = None , control_parent = None) :
		base.Base.__init__(self , side , name , index , joint_parent , control_parent)
		'''
		length：关节的总长度
		
		'''
		self._rtype = 'chain'
		self._name = name + self._rtype
		
		
		self.length = length
		self.interval =None
		self.direction = None
		self.curve = None
	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		for bpjnt in self.bpjnt_list :
			self.bpjnt = cmds.createNode('joint' , name = bpjnt,parent = self.joint_parent)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.bpjnt
			# 调整距离
			pipelineUtils.Pipeline.move(obj = self.bpjnt , pos = self.direction)
	
	
	
	def create_joint(self) :
		'''
		根据定位的bp关节创建关节
		'''
		for bpjnt,jnt in [self.bpjnt_list,self.jnt_list] :
			self.jnt = cmds.createNode('joint' , name = jnt , parent = self.joint_parent)
			cmds.matchTransform(self.jnt, bpjnt)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.jnt
		
		# 删除bp的定位关节
		cmds.delete(self.bpjnt_list[0])
