import maya.cmds as cmds

from . import chain
from ..base import bone,base
from ...core import vectorUtils , controlUtils,pipelineUtils
from importlib import reload
reload(pipelineUtils)
class ChainEP(base.Base):
	
	
	
	def __init__(self , side , name , joint_number ,ctrl_number , curve , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		u'''给定一根曲线，根据曲线的长度来创建关节和控制器
		joint_number：生成的关节数量
		ctrl_number：生成的控制器数量
		crv_node：需要创建控制器与关节的曲线
		'''
		self._rtype = 'ChainEP'
		self.ctrl_number = ctrl_number
		self.curve = curve
		self.radius = 3
		self.set_shape('ball')
		
		#根据给定的控制器数量，获取控制对应的百分比信息
		if not ctrl_number :
			ctrl_number = self.joint_number
		if ctrl_number < 2 :
			raise ValueError(u"请有足够的控制点")
		if ctrl_number < joint_number:
			raise ValueError(u"控制器的数量请大于关节的数量")
		
		
		self.guide_curve = None
		self.cvs = list()
		
		percents = pipelineUtils.Pipeline.get_percentages(ctrl_number)
		for p in percents :
			integer = int(round(p * (self.joint_number - 1)))
			self.cvs.append(integer)
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		bpjnt_list = pipelineUtils.Pipeline.create_joints_on_curve(self.curve , self.joint_number)
		for joint_number , bpjnt in enumerate(bpjnt_list) :
			bpjnt = cmds.rename(bpjnt , self.bpjnt_list[joint_number])
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
	
	
	
	def create_ctrl(self) :
		self.set_shape(self.shape)
		for index in (self.cvs)  :
			self.ctrl = controlUtils.Control.create_ctrl(self.ctrl_list[index] , shape = self.shape ,
			                                             radius = self.radius ,
			                                             axis = 'X+' , pos = self.jnt_list[index] ,
			                                             parent = self.control_parent)
	
	
	
	def add_constraint(self) :
		'''
		在关节和控制器之间添加平滑衰减约束
		'''
		for index in self.cvs :
			#开头的关节进行约束
			if index == 0 :
				cmds.pointConstraint(self.ctrl_list[index] , self.jnt_list[index] ,
				                     mo = 1)
				cmds.orientConstraint(self.ctrl_list[index] , self.jnt_list[index] ,
				                      mo = 1)
				
			# 结尾的关节进行约束
			elif index == self.cvs[-1]:
				cmds.pointConstraint(self.ctrl_list[index] , self.jnt_list[-1] ,
				                     mo = 1)
				cmds.orientConstraint(self.ctrl_list[index] , self.jnt_list[- 1])
			# 中间的关节进行约束
			else :
				for index in range(len(self.cvs) - 1) :
					head = self.cvs[index]
					tail = self.cvs[index + 1]
					for jnt in range(head , tail + 1) :
						gap = 1.00 / (tail - head)
						
						# 设置前后两端的控制器影响关节的权重值
						cmds.pointConstraint(self.ctrl_list[head] , self.jnt_list[jnt] ,
						                     w = 1 - ((jnt - head) * gap) , mo = 1)
						cmds.pointConstraint(self.ctrl_list[tail] , self.jnt_list[jnt] ,
						                     w = (jnt - head) * gap , mo = 1)
						cmds.orientConstraint(self.ctrl_list[head] , self.jnt_list[jnt] ,
						                      w = 1 - ((jnt - head) * gap) , mo = 1)
						cmds.orientConstraint(self.ctrl_list[tail] , self.jnt_list[jnt] ,
						                      w = (jnt - head) * gap , mo = 1)
	
	
	
	
	
	
	
	
	
		
	
		