from ..base import base
from ..chain import chainFK
import maya.cmds as cmds



class Finger(chainFK.ChainFK) :
	
	
	
	def __init__(self , side , name , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 , joint_parent = None ,
	             control_parent = None) :
		if side == 'r' :
			direction = [1 , 0 , 0]
		super().__init__(side , name , joint_number , direction , length , joint_parent , control_parent)
		
		self._rtype = 'Finger'
		self.radius = 2
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		
		# 添加手指头一键弯曲的属性
		cmds.addAttr(self.ctrl_list[0] , ln = '{}Curl'.format(self.name) , at = 'double' , dv = 0 , min = -10 ,
		             max = 10 ,
		             k = 1)
		
		self.add_curl()
	
	
	
	def add_curl(self) :
		u"""
		添加手指弯曲的效果
		"""
		for ctrl in self.ctrl_list[1 :-1] :
			mult_node = cmds.createNode('multDoubleLinear' , name = ctrl.replace('ctrl' , 'mult'))
			cmds.setAttr(mult_node + '.input2' , 9)
			cmds.connectAttr(self.ctrl_list[0] + '.{}Curl'.format(self.name) , mult_node + '.input1')
			cmds.connectAttr(mult_node + '.output' , ctrl + '.rotateZ')
