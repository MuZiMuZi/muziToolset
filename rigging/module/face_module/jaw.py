# coding=utf-8
'''
下巴的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base
from ...chain import chain , chainFK
from ....core import controlUtils , jointUtils



class Jaw(chainFK.ChainFK) :
	
	
	
	def __init__(self , side , name = '' , joint_number = 2 , direction = [-1 , 0 , 0] ,
	             length = 5 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , direction , length , joint_parent , control_parent)
		self.shape = 'circle'
		self._rtype = 'Jaw'
		self.radius = 2
	
	
	
	def create_namespace(self) :
		super().create_namespace()
	
	
	
	def create_bpjnt(self) :
		# 获得jaw_bpjnt 的路径
		self.jaw_bpjnt_path = os.path.abspath(__file__ + "/../jaw_bpjnt.ma")
		# 导入关节
		cmds.file(self.jaw_bpjnt_path , i = True , rnn = True)



if __name__ == "__main__" :
	def build_setup() :
		jaw_m = jaw.Jaw(side = 'm' , joint_parent = None , control_parent = None)
		jaw_m.build_setup()
	
	
	
	def build_rig() :
		jaw_m = jaw.Jaw(side = 'm' , joint_parent = None , control_parent = None)
		jaw_m.build_rig()
	
	
	
	build_setup()
	build_rig()
