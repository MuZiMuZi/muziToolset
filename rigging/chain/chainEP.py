import maya.cmds as cmds

from . import chain
from ..base import bone,base
from ...core import vectorUtils , controlUtils,pipelineUtils
from importlib import reload
reload(pipelineUtils)
class ChainEP(base.Base):
	
	
	
	def __init__(self , side , name , joint_nuber ,ctrl_number , curve , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_nuber , joint_parent , control_parent)
		u'''给定一根曲线，根据曲线的长度来创建关节和控制器
		joint_nuber：生成的关节数量
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
			ctrl_number = self.joint_nuber
		if ctrl_number < 2 :
			raise ValueError(u"请有足够的控制点")
		
		self.guide_curve = None
		self.cvs = list()
		
		percents = pipelineUtils.Pipeline.get_percentages(ctrl_number)
		for p in percents :
			integer = int(round(p * (self.joint_nuber - 1)))
			self.cvs.append(integer)
	
	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		bpjnt_list = pipelineUtils.Pipeline.create_joints_on_curve(self.curve , self.ctrl_number)
		for joint_nuber , bpjnt in enumerate(bpjnt_list) :
			bpjnt = cmds.rename(bpjnt , self.bpjnt_list[joint_nuber])
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
	
	
	
	def add_constraint(self) :
		'''
		在关节和控制器之间添加平滑衰减约束
		'''
		for i in range(len(self.cvs) - 1) :
			head = self.cvs[i]
			tail = self.cvs[i + 1]
			for j in range(head , tail + 1) :
				gap = 1.00 / (tail - head)
				
				# 制作点约束和旋转约束
				cmds.pointConstraint(self.ctrl_list[head] , self.jnt_list[j] ,
				                     w = 1 - ((j - head) * gap) , mo = 1)
				cmds.pointConstraint(self.ctrl_list[tail] , self.jnt_list[j] ,
				                     w = (j - head) * gap , mo = 1)
				cmds.orientConstraint(self.ctrl_list[head] , self.jnt_list[j] ,
				                      w = 1 - ((j - head) * gap) , mo = 1)
				cmds.orientConstraint(self.ctrl_list[tail] , self.jnt_list[j] ,
				                      w = (j - head) * gap , mo = 1)
	
	
	
	
	
	
	
	
	
	
		
	
		