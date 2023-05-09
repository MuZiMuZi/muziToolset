from ..base import base
import maya.cmds as cmds
class Chain(base.Base):
	
	
	
	def __init__(self , side , name , index , joint_parent = None , control_parent = None ) :
		base.Base.__init__(self,side , name , index , joint_parent , control_parent )
		
		self._rtype = 'chain'
		self._name = name + self._rtype
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		self.bpjnt_list = []
		for i in range(self._index) :
			self.bpjnt_name = 'bpjnt_{}_{}_{:03d}'.format(self._side , self._name , i + 1)
			self.bpjnt = cmds.createNode('joint' , name = self.bpjnt_name, parent = self.joint_parent)
			self.bpjnt_list.append(self.bpjnt)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.bpjnt_name
		
	
		

	
	
	def create_joint(self) :
		'''
		根据定位的bp关节创建关节
		'''
		self.jnt_list = []
		for i in range(self._index) :
			self.jnt_name = 'jnt_{}_{}_{:03d}'.format(self._side , self._name , i + 1)
			self.jnt = cmds.createNode('joint' , name = self.jnt_name,parent = self.joint_parent)
			self.bpjnt = self.jnt_name.replace('jnt' , 'bpjnt')
			cmds.matchTransform(self.jnt_name , self.bpjnt)
			self.jnt_list.append(self.jnt)
			#指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.jnt_name
			
		#删除bp的定位关节
		cmds.delete(self.jnt_list[0].replace('jnt','bpjnt'))
	

		
		