from ..base import base
import maya.cmds as cmds
from ...core import controlUtils
from ...core import vectorUtils
from . import chain

from importlib import reload



reload(vectorUtils)
reload(chain)



class ChainFk(chain.Chain) :
	
	
	
	def __init__(self , side , name , index , direction , length = 10 , joint_parent = None , control_parent = None) :
		u"""
		用来创建fk关节链条的绑定
		length(int)：关节的总长度
		direction（list）:从根节点到顶部节点的方向例如[1,0,0]或者[0,1,0]
		"""
		chain.Chain.__init__(self , side , name , index , length , joint_parent , control_parent)
		self._rtype = 'chainFK'
		
		self.interval = length / (self._index - 1)
		self.direction = list(vectorUtils.Vector(direction).mult_interval(self.interval))
		self.shape = 'circle'
		self.axis = vectorUtils.Vector(direction).axis
	
	
	
	def create_ctrl(self) :
		self.set_shape(self.shape)
		for ctrl , jnt in zip(self.ctrl_list , self.jnt_list) :
			self.ctrl = controlUtils.Control.create_ctrl(ctrl , shape = self.shape,
			                                             radius = 5 ,
			                                             axis = self.axis , pos = jnt ,
			                                             parent = self.control_parent)
			# 指定关节的父层级为上一轮创建出来的控制器层级组
			self.control_parent = self.ctrl.replace('ctrl','output')
	
	
	
	def add_constraint(self) :
		for index , jnt in enumerate(self.jnt_list) :
			cmds.parentConstraint(self.ctrl_list[index] , jnt)
			cmds.scaleConstraint(self.ctrl_list[index] , jnt)
