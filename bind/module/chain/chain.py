import maya.cmds as cmds

from ....core import jointUtils , pipelineUtils
from ..base import base
from importlib import reload
reload(jointUtils)


class Chain(base.Base) :
	
	
	
	def __init__(self , side , name , joint_number , length = 10 , joint_parent = None , control_parent = None) :
		base.Base.__init__(self , side , name , joint_number , joint_parent , control_parent)
		'''
		length：关节的总长度
		
		'''
		self._rtype = 'Chain'
		
		self.length = length
		self.interval = None
		self.direction = None
		self.curve = None
		

	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		for bpjnt in self.bpjnt_list :
			self.bpjnt = cmds.createNode('joint' , name = bpjnt , parent = self.joint_parent)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.bpjnt
			# 调整距离
			pipelineUtils.Pipeline.move(obj = self.bpjnt , pos = self.direction)
		# 进行关节定向
		jointUtils.Joint.joint_orientation(self.bpjnt_list)
	
	
	
	def create_joint(self) :
		'''
		根据定位的bp关节创建关节
		'''
		# 根据bp关节创建新的关节
		for bpjnt in self.bpjnt_list :
			for attr in ['.translate' , '.rotate' , '.scale'] :
				# 判断bp关节上有没有连接的属性，如果有的话则断掉
				plug = cmds.listConnections(bpjnt + attr , s = True , d = False , p = True)
				if plug :
					cmds.disconnectAttr(plug[0] , bpjnt + attr)
		
		for bpjnt , jnt in zip(self.bpjnt_list , self.jnt_list) :
			# 判断场景里是否已经存在对应的关节，重建的情况
			if cmds.objExists(jnt) :
				# 删除过去的关节后，并重新创建关节
				cmds.delete(jnt)
			# 场景里没有存在对应的关节，第一次创建绑定的情况
			self.jnt = cmds.createNode('joint' , name = jnt , parent = self.joint_parent)
			cmds.matchTransform(jnt , bpjnt)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.jnt
			
		# 隐藏bp的定位关节
		cmds.setAttr(self.bpjnt_list[0] + '.visibility' , 0)
		
		# 进行关节定向
		jointUtils.Joint.joint_orientation(self.jnt_list)