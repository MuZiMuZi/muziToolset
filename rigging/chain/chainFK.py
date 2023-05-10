from ..base import base
import maya.cmds as cmds
from ...core import controlUtils
from ...core import vectorUtils
from . import chain

from importlib import reload
reload(vectorUtils)
reload(chain)


class ChainFk(chain.Chain) :
	
	
	
	def __init__(self , side , name , index , direction, length = 10 ,joint_parent = None , control_parent = None ) :
		u"""
		用来创建fk关节链条的绑定
		length：关节的总长度
		direction:从根节点到顶部节点的方向例如（1,0,0）或者（0,1,0）
		"""
		chain.Chain.__init__(self , side , name , index ,length, joint_parent , control_parent)
		self._rtype = 'chainFK'
		self._name = name + self._rtype
		
		self.interval = length / (self._index - 1)
		self.direction = list(vectorUtils.Vector(direction).mult_interval(self.interval))

	
	
	def create_ctrl(self) :
		self.ctrl_list = []
		for i in range(self._index) :
			self.ctrl_name = 'ctrl_{}_{}_{:03d}'.format(self._side , self._name , i + 1)
			self.ctrl = controlUtils.Control.create_ctrl(self.ctrl_name , shape = 'circle' ,
			                                             radius = 5 ,
			                                             axis = 'X+' , pos = self.ctrl_name.replace('ctrl' , 'jnt') ,
			                                             parent = self.control_parent)
			self.ctrl_list.append(self.ctrl)
			# 指定关节的父层级为上一轮创建出来的关节
			self.control_parent = self.ctrl_name
	
	
	
	def add_constraint(self) :
		for index,jnt in enumerate(self.jnt_list):
			cmds.parentConstraint(self.ctrl_list[index],jnt)
			cmds.scaleConstraint(self.ctrl_list[index] , jnt)
	
	