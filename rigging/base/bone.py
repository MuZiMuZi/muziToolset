# coding=utf-8
from importlib import reload
from ...core import jointUtils
from ...core import pipelineUtils
import maya.cmds as cmds



reload(pipelineUtils)



class Bone(object) :
	"""
	创建定位的bp关节，然后生成对应的绑定
	创建绑定的步骤:
	1. build_bpjnt: 	创建定位的bp关节
	2. build_rig: 		根据定位的bp关节创建关节

	# Attribute:
	namer. a string generator for temporary naming
	"""
	
	
	
	def __init__(self , side , name , index , joint_parent = None , control_parent = None , point_value = True ,
	             orient_value = True , scale_value = True , mo_value = True) :
		"""
		根据给定的变量创建关节和控制器

		:param side: 关节的边
		:param name: 关节的模块名称
		:param name: 关节的数量
		:param joint_parent: 生成的关节的父层级
		:param control_parent: 生成的控制器的父层级
		"""
		super(Bone , self).__init__()
		
		self._side = side
		self._name = name
		self._index = index
		
		#设置关节的父层级和控制器的父层级
		self.joint_parent = joint_parent
		self.control_parent = control_parent
		if not self.joint_parent :
			if not cmds.objExists('_joint') :
				cmds.createNode('transform' , name = '_joint')
				self.joint_parent = '_joint'
			else :
				self.joint_parent = '_joint'
		if not self.control_parent :
			if not cmds.objExists('_control') :
				cmds.createNode('transform' , name = '_control')
				self.control_parent = '_control'
			else :
				self.control_parent = '_control'
				
		# 约束的参数设置
		self.point_value = point_value
		self.orient_value = orient_value
		self.scale_value = scale_value
		self.mo_value = mo_value
		
		self._rtype = None
	
	
	
	@property
	def name(self) :
		return self._name
	
	
	
	@property
	def side(self) :
		return self._side
	
	
	
	@property
	def type(self) :
		return self._rtype
	
	
	
	@property
	def scale(self) :
		return self._scale
	
	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		self.bpjnt_list = []
		for i in range(self._index) :
			self.bpjnt_name = 'bpjnt_{}_{}_{:03d}'.format(self._side , self._name , i + 1)
			self.bpjnt = cmds.createNode('joint' , name = self.bpjnt_name)
			self.bpjnt_list.append(self.bpjnt)
	
	
	
	def create_joint(self) :
		'''
		根据定位的bp关节创建关节
		'''
		self.jnt_list = []
		for bpjnt in self.bpjnt_list :
			self.jnt = cmds.createNode('joint' , name = bpjnt.replace('bpjnt' , 'jnt') , parent = self.joint_parent)
			cmds.delete(bpjnt)
			self.jnt_list.append(self.jnt)
	
	
	
	def create_ctrl(self) :
		u"""
		创建控制器
		"""
		self.ctrl_list = []
		for jnt in self.jnt_list :
			self.ctrl = controlUtils.Control.create_ctrl(jnt.replace('jnt' , 'ctrl') , shape = 'cube' ,
			                                             radius = 5 ,
			                                             axis = 'X+' , pos = jnt , parent = self.control_parent)
			self.ctrl_list.append(self.ctrl)
	
	
	
	def add_constraint(self) :
		'''
		添加约束
		'''
		for ctrl , jnt in zip(self.ctrl_list , self.jnt_list) :
			
			pipelineUtils.Pipeline.create_constraint(ctrl.replace(' ctrl' , 'output') , jnt ,
			                                         point_value = self.point_value ,
			                                         orient_value = self.orient_value , scale_value =
			                                         self.scale_value ,
			                                         mo_value = self.mo_value)
	
	
	
	def build_bp(self) :
		"""
		创建bp的定位关节
		"""
		self.create_bpjnt()
	
	
	
	def build_rig(self) :
		"""
		创建绑定系统
		"""
		self.create_joint()
		self.create_ctrl()
		self.add_constraint()



if __name__ == "__main__" :
	custom = bone.Bone(side = 'l' , name = 'zz' , index = 5 , joint_parent = None , control_parent = None)
	custom.build_bp()
	custom.build_rig()
