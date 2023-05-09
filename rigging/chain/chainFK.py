from ..base import base
import maya.cmds as cmds
from ...core import controlUtils
from . import chain



class ChainFk(chain.Chain) :
	
	
	
	def __init__(self , side , name , index , joint_parent = None , control_parent = None , point_value = True ,
	             orient_value = True , scale_value = True , mo_value = True) :
		chain.Chain.__init__(self,side , name , index , joint_parent , control_parent , point_value , orient_value ,
		                 scale_value , mo_value)
		self._rtype = 'chainFK'
		self._name = name + self._rtype
	
	
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
		
	
	