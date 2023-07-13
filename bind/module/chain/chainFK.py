import maya.cmds as cmds

from ....core import controlUtils, vectorUtils
from . import chain
from importlib import reload
reload(chain)


class ChainFK(chain.Chain) :
	
	
	
	def __init__(self , side , name , joint_number , direction = [-1 , 0 , 0] , length = 10 , joint_parent = None ,
	             control_parent = None) :
		u"""
		用来创建fk关节链条的绑定
		length(int)：关节的总长度
		direction（list）:从根节点到顶部节点的方向例如[1,0,0]或者[0,1,0]
		"""
		chain.Chain.__init__(self , side , name , joint_number , length , joint_parent , control_parent)
		self._rtype = 'ChainFK'
		
		self.interval = length / (self.joint_number - 1)
		self.direction = list(vectorUtils.Vector(direction).mult_interval(self.interval))
		self.shape = 'circle'
		self.axis = vectorUtils.Vector(direction).axis
		
		self.radius = 4
	
	
	
	def create_ctrl(self) :
		# 判断场景里是否已经存在对应的控制器，重建的情况
		if cmds.objExists(self.ctrl_grp) :
			# 删除过去的控制器层级组后，并重新创建控制器
			cmds.delete(self.ctrl_grp)
			self.ctrl_grp = cmds.createNode('transform' , name = self.ctrl_grp , parent = self.control_parent)
		else :
			self.ctrl_grp = cmds.createNode('transform' , name = self.ctrl_grp , parent = self.control_parent)
			
		self.set_shape(self.shape)

		parent = self.ctrl_grp
		for ctrl , jnt in zip(self.ctrl_list , self.jnt_list) :
			self.ctrl = controlUtils.Control.create_ctrl(ctrl , shape = self.shape ,
			                                             radius = self.radius ,
			                                             axis = self.axis , pos = jnt ,
			                                             parent = parent)
			# 指定关节的父层级为上一轮创建出来的控制器层级组
			parent = ctrl.replace('ctrl' , 'output')
	
	
	
	def add_constraint(self) :
		for joint_number , jnt in enumerate(self.jnt_list) :
			cmds.parentConstraint(self.ctrl_list[joint_number] , jnt)
			cmds.scaleConstraint(self.ctrl_list[joint_number] , jnt)
