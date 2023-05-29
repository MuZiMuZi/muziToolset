# coding=utf-8
'''
耳朵的绑定系统创建
'''
import os

import maya.cmds as cmds

from ...chain import chainFK



class Ear(chainFK.ChainFK) :
	
	
	
	def __init__(self , side , name = '' , joint_number = 3 , direction = [-1 , 0 , 0] ,
	             length = 5 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , direction , length , joint_parent , control_parent)
		self.shape = 'circle'
		self._rtype = 'Ear'
		self.radius = 0.5
	
	
	
	def create_namespace(self) :
		super().create_namespace()
	
	
	
	def create_bpjnt(self) :
		# 获得ear_bpjnt 的路径
		self.ear_bpjnt_path = os.path.abspath(__file__ + "/../ear_bpjnt.ma")
		# 导入关节
		cmds.file(self.ear_bpjnt_path , i = True , rnn = True)



if __name__ == "__main__" :
	def build_setup() :
		ear_l = ear.Ear(side = 'l' , joint_parent = None , control_parent = None)
		ear_l.build_setup()
	
	
	
	def build_rig() :
		ear_l = ear.Ear(side = 'l' , joint_parent = None , control_parent = None)
		ear_l.build_rig()
	
	
	
	build_setup()
	build_rig()
