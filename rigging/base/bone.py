# coding=utf-8
from importlib import reload
from ...core import jointUtils
from ...core import pipelineUtils
from ...core import hierarchyUtils
from ...core import controlUtils
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
	
	
	
	def __init__(self , side , name , index , joint_parent = None , control_parent = None ) :
		"""
		根据给定的变量创建关节和控制器

		:param side: 关节的边
		:param name: 关节的模块名称
		:param name: 关节的数量
		:param joint_parent: 生成的关节的父层级
		:param control_parent: 生成的控制器的父层级
		"""
		super(Bone , self).__init__()
		#创建层级结构
		hierarchyUtils.Hierarchy.create_rig_grp()
		self._side = side
		self._index = index
		
		
		#设置关节的父层级和控制器的父层级
		self.joint_parent = joint_parent
		self.control_parent = control_parent
		if not self.joint_parent :
			self.joint_parent = '_joint'
		if not self.control_parent :
			self.control_parent = '_control'
				

		
		#生成的绑定类型
		self._rtype =''
		self._name = name
	
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
		#修改关节定向
		self.joint_orientation()
		#根据bp关节创建新的关节
		self.jnt_list = []
		for i in range(self._index) :
			self.jnt_name = 'jnt_{}_{}_{:03d}'.format(self._side , self._name , i + 1)
			self.jnt = cmds.createNode('joint' , name = self.jnt_name , parent = self.joint_parent)
			self.bpjnt = self.jnt_name.replace('jnt','bpjnt')
			cmds.matchTransform(self.jnt_name,self.bpjnt)
			self.jnt_list.append(self.jnt)
			cmds.delete(self.bpjnt)
	
	

		
	def create_ctrl(self) :
		u"""
		创建控制器
		"""
		self.ctrl_list = []
		for i in range(self._index) :
			self.ctrl_name = 'ctrl_{}_{}_{:03d}'.format(self._side , self._name , i + 1)
			self.ctrl = controlUtils.Control.create_ctrl(self.ctrl_name , shape = 'circle' ,
			                                             radius = 5 ,
			                                             axis = 'X+' , pos = self.ctrl_name.replace('ctrl','jnt') , parent = self.control_parent)
			self.ctrl_list.append(self.ctrl)
	
	
	
	def add_constraint(self) :
		'''
		添加约束
		'''
		for ctrl , jnt in zip(self.ctrl_list , self.jnt_list) :
			
			pipelineUtils.Pipeline.create_constraint(ctrl.replace(' ctrl' , 'output') , jnt ,
			                                         point_value = True ,
			                                         orient_value = True, scale_value =
			                                         True ,
			                                         mo_value = True)
	
	
	
	def joint_orientation(self) :
		u'''
		对于用来定位绑定系统的bp关节自动关节定向,正常关节定向为X轴指向下一关节，末端关节定向为世界方向
		'''
		# 获取场景里所有的bp定位关节
		bp_jnts = cmds.ls('bpjnt_*',type = 'joint')
		
		# 判断关节是否具有子关节
		for bp_jnt in bp_jnts :
			cmds.makeIdentity(bp_jnt , apply = True , translate = 1 , rotate = 1 , scale = 1 , normal = 0 ,
			                  preserveNormals = 1)
			jnt_sub = cmds.listRelatives(bp_jnt , children = True , allDescendents = True , type = 'joint')
			# 如果有子关节，则关节定向为X轴指向下一关节
			if jnt_sub :
				cmds.joint(bp_jnt , zeroScaleOrient = 1 , children = 1 , e = 1 , orientJoint = 'xyz' ,
				           secondaryAxisOrient = 'xup')
			
			# 无子关节，关节定向为世界方向
			else :
				cmds.joint(bp_jnt , zeroScaleOrient = 1 , children = 1 , e = 1 , orientJoint = 'none')
		
	
	def build_setup(self) :
		"""
		创建bp的定位关节,生成准备
		"""
		self.create_bpjnt()
	
	
	
	def build_rig(self) :
		"""
		创建绑定系统
		"""
		self.create_joint()
		self.create_ctrl()
		self.add_constraint()




