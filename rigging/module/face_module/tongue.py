# coding=utf-8
'''
舌头的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base
from ...chain import chain , chainFK
from ....core import controlUtils , jointUtils , pipelineUtils



class Tongue(chainFK.ChainFK) :
	
	
	
	def __init__(self , side = 'm' , name = '' , joint_number = 5 , direction = [-1 , 0 , 0] , length = 10 ,
	             joint_parent = None ,
	             control_parent = None) :
		super().__init__(side , name , joint_number , direction , length , joint_parent , control_parent)
		self._rtype = 'Tongue'
		self.radius = 0.35
	
	
	
	def create_bpjnt(self) :
		# 获得tongue_bpjnt 的路径
		self.tongue_bpjnt_path = os.path.abspath(__file__ + "/../tongue_bpjnt.ma")
		# 导入关节
		cmds.file(self.tongue_bpjnt_path , i = True , rnn = True)
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		# 添加一键控制舌头的弯曲功能
		self.tongue_curl()
	
	
	
	def tongue_curl(self) :
		u"""
		添加一键控制舌头的弯曲功能
		"""
		cmds.addAttr(self.ctrl_list[0] , ln = 'TongueCurl' , dv = 0 , min = -10 , max = 10 , k = 1)
		# 添加一键控制舌头的弯曲功能
		for connect in self.connect_list[1 :-1] :
			mult_node = cmds.createNode('multDoubleLinear' , name = connect.replace('connect' , 'mult'))
			cmds.setAttr(mult_node + '.input1' , 10)
			cmds.connectAttr(self.ctrl_list[0] + '.TongueCurl' , mult_node + '.input2')
			cmds.connectAttr(mult_node + '.output' , connect + '.rotateY')



if __name__ == '__main__' :
	def build_setup() :
		tongue_m = tongue.Tongue(joint_parent = None , control_parent = None)
		tongue_m.build_setup()
	
	
	
	def build_rig() :
		tongue_m = tongue.Tongue(joint_parent = None , control_parent = None)
		tongue_m.build_rig()
	
	
	
	# #
	# # #
	build_setup()
	build_rig()