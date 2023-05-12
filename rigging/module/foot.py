import maya.cmds as cmds
from ..base import base , bone
from ..chain import chain
from ...core import controlUtils , jointUtils , hierarchyUtils , vectorUtils



class Foot(chain.Chain) :
	
	
	
	def __init__(self , side , name , joint_number = 3 , length = 6 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		self.length = length
		self.parts = ['Ankle' , 'Ball' , 'Toe']
		self.rvs_bpjnt_list = list()
		self.rvs_jnt_parts = ['Tiptoe' , 'Heel' , 'Inn' , 'Out']
		
		self.value = length / joint_number
		self.radius = 3
	
	
	def create_namespace(self) :
		u"""
		创建名称规范整理
		"""
		for part in self.parts :
			self.bpjnt_list.append('bpjnt_{}_{}{}_001'.format(self._side , self._name , part))
			self.jnt_list.append('jnt_{}_{}{}_001'.format(self._side , self._name , part))
			self.zero_list.append('zero_{}_{}{}_001'.format(self._side , self._name , part))
			self.driven_list.append('driven_{}_{}{}_001'.format(self._side , self._name , part))
			self.ctrl_list.append('ctrl_{}_{}{}_001'.format(self._side , self._name , part))
			self.output_list.append('output_{}_{}{}_001'.format(self._side , self._name , part))
		self.ctrl_grp = ('grp_{}_{}{}_001'.format(self._side , self._name , self._rtype))
		# 创建用来定位旋转轴心点的关节
		for part in self.rvs_jnt_parts :
			self.rvs_bpjnt_list.append('bpjnt_{}_{}{}_001'.format(self._side , self._name , part))
		self.tiptoe_bpjnt = ('bpjnt_{}_{}Tiptoe_001'.format(self._side , self._name))
		self.heel_bpjnt = ('bpjnt_{}_{}Heel_001'.format(self._side , self._name))
		self.inn_bpjnt = ('bpjnt_{}_{}Inn_001'.format(self._side , self._name))
		self.out_bpjnt = ('bpjnt_{}_{}Out_001'.format(self._side , self._name))
	
	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		for bpjnt in self.bpjnt_list :
			self.bpjnt = cmds.createNode('joint' , name = bpjnt , parent = self.joint_parent)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.bpjnt
			# 调整距离
			cmds.setAttr(bpjnt + '.translate' , 0 , 0 , self.value)
		cmds.setAttr(self.bpjnt_list[0] + '.translate' , self.value * self.side_value , self.value , 0)
		# 创建用来定位ik旋转轴心点的关节
		for rvs_jnt in self.rvs_bpjnt_list :
			self.rvs_jnt = cmds.createNode('joint' , name = rvs_jnt)
		# 进行关节定向
		jointUtils.Joint.joint_orientation(self.rvs_bpjnt_list)
		
		# 设置定位旋转轴心点的关节的位置
		cmds.setAttr(self.tiptoe_bpjnt + '.translate' , self.value * self.side_value , 0 , self.value * 2)
		cmds.setAttr(self.heel_bpjnt + '.translate' , self.value * self.side_value , 0 , 0)
		cmds.setAttr(self.inn_bpjnt + '.translate' , 0 , 0 , self.value)
		cmds.setAttr(self.out_bpjnt + '.translate' , self.value * 2 * self.side_value , 0 , self.value)
	
	
	
	def create_joint(self) :
		super().create_joint()
		# 创建用来定位ik旋转轴心点的关节
		for rvs_bpjnt in self.rvs_bpjnt_list :
			self.jnt = cmds.createNode('joint' , name = rvs_bpjnt.replace('bpjnt' , 'jnt') , parent = self.joint_parent)
			cmds.matchTransform(self.jnt , rvs_bpjnt)
			cmds.delete(rvs_bpjnt)
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		# 创建用来定位ik旋转轴心点的控制器
		for rvs_bpjnt in self.rvs_bpjnt_list :
			rvs_ctrl = controlUtils.Control.create_ctrl(rvs_bpjnt.replace('bpjnt' , 'ctrl') , shape = 'ball' ,
			                                            radius = self.radius * 0.5,
			                                            axis = 'X+' , pos = rvs_bpjnt.replace('bpjnt' , 'jnt') ,
			                                            parent = self.ctrl_grp)
