# coding=utf-8
from importlib import reload
from ...core import jointUtils, controlUtils, pipelineUtils, hierarchyUtils
import maya.cmds as cmds



reload(pipelineUtils)
reload(hierarchyUtils)



class Bone(object) :
	"""
	创建定位的bp关节，然后生成对应的绑定
	创建绑定的步骤:
	1. build_setup: 	创建定位的bp关节
	2. build_rig: 		根据定位的bp关节创建关节

	# Attribute:
	namer. a string generator for temporary naming
	"""
	
	
	
	def __init__(self , side , name , joint_number , joint_parent = None , control_parent = None) :
		"""
		根据给定的变量创建关节和控制器

		:param side: 关节的边
		:param name: 关节的模块名称
		:param joint_number: 关节的数量
		:param joint_parent: 生成的关节的父层级
		:param control_parent: 生成的控制器的父层级
		"""
		super(Bone , self).__init__()
		# 创建层级结构
		hierarchyUtils.Hierarchy.create_rig_grp()
		self._side = side
		self.joint_number = joint_number
		
		# 设置关节的父层级和控制器的父层级
		self.joint_parent = joint_parent
		self.control_parent = control_parent
		if not self.joint_parent :
			self.joint_parent = '_joint'
		if not self.control_parent :
			self.control_parent = '_control'
		
		# 生成的绑定类型
		self._rtype = ''
		self._name = name
		self.shape = 'circle'
		self.radius = 5
		
		# 根据给定的边，名称和joint_number生成列表来存储创建的名称
		self.bpjnt_list = list()
		self.jnt_list = list()
		self.ctrl_list = list()
		self.zero_list = list()
		self.driven_list = list()
		self.output_list = list()
		
		# 判断边为'l'还是'r'
		if side == 'l' :
			self.side_value = 1
		elif side == 'r' :
			self.side_value = -1
		else:
			self.side_value = 0
	
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
	
	
	
	def set_shape(self , shape) :
		u'''
		设置控制器形状
		'''
		self.shape = shape
	
	
	
	def create_namespace(self) :
		u"""
		创建名称规范整理
		"""
		for i in range(self.joint_number) :
			self.bpjnt_list.append('bpjnt_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , i + 1))
			self.jnt_list.append('jnt_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , i + 1))
			self.zero_list.append('zero_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , i + 1))
			self.driven_list.append('driven_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , i + 1))
			self.ctrl_list.append('ctrl_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , i + 1))
			self.output_list.append('output_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , i + 1))
		self.ctrl_grp = ('grp_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , i + 1))
	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		for bpjnt in self.bpjnt_list :
			self.bpjnt = cmds.createNode('joint' , name = bpjnt)
		# 进行关节定向
		jointUtils.Joint.joint_orientation(self.bpjnt_list)
	
	
	def create_joint(self) :
		'''
		根据定位的bp关节创建关节
		'''
		# 根据bp关节创建新的关节
		for bpjnt , jnt in zip(self.bpjnt_list , self.jnt_list) :
			jnt = cmds.createNode('joint' , name = jnt , parent = self.joint_parent)
			cmds.matchTransform(jnt , bpjnt)
			cmds.delete(bpjnt)
		#进行关节定向
		jointUtils.Joint.joint_orientation(self.jnt_list)
	
	
	def create_ctrl(self) :
		u"""
		创建控制器
		"""
		self.set_shape(self.shape)
		#创建整体的控制器层级组
		self.ctrl_grp = cmds.createNode('transform',name = self.ctrl_grp,parent=self.control_parent)
		
		for ctrl , jnt in zip(self.ctrl_list , self.jnt_list) :
			self.ctrl = controlUtils.Control.create_ctrl(ctrl , shape = self.shape ,
			                                             radius = self.radius ,
			                                             axis = 'X+' , pos = jnt ,
			                                             parent = self.ctrl_grp)

		
		
	
	
	
	def add_constraint(self) :
		'''
		添加约束
		'''
		for ctrl , jnt in zip(self.ctrl_list , self.jnt_list) :
			
			pipelineUtils.Pipeline.create_constraint(ctrl.replace(' ctrl' , 'output') , jnt ,
			                                         point_value = True ,
			                                         orient_value = True , scale_value =
			                                         True ,
			                                         mo_value = True)
	
	
	
		
		
	
	
	
	def build_setup(self) :
		"""
		创建bp的定位关节,生成准备
		"""
		self.create_namespace()
		self.create_bpjnt()
	
	
	
	def build_rig(self) :
		"""
		创建绑定系统
		"""
		self.create_namespace()
		self.create_joint()
		self.create_ctrl()
		self.add_constraint()
