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
		
		# 创建用于驱动下巴位移的偏移组
		self.offsetrot_grp = list()
	
	def create_namespace(self) :
		super().create_namespace()
		for grp in self.offset_grp
		self.offsetrot_grp = self.
	
	
	def create_bpjnt(self) :
		# 获得jaw_bpjnt 的路径
		self.jaw_bpjnt_path = os.path.abspath(__file__ + "/../jaw_bpjnt.ma")
		# 导入关节
		cmds.file(self.jaw_bpjnt_path , i = True , rnn = True)
	
	
	
	def create_jaw_open(self) :
		u"""
		下巴控制器旋转的时候同时也可以驱动下巴的位移，这样子可以在旋转的过程中直接做出吃惊等一系列夸张的效果
		原理：获得控制器offset组，ctrl，和subctrl的旋转值，将其连接给乘除节点，最后连接回给控制器的connect组
		注意点：不能够直接通过约束loc的方式来获得数值连接，这样会产生cycle的循环，
		因此需要创建三个组来分别连接对应层级的旋转值和rotate order，最后用这个创建出来的子层级组再来进行约束
		"""
		
	

if __name__ == "__main__" :
	def build_setup() :
		jaw_m = jaw.Jaw(side = 'm' , joint_parent = None , control_parent = None)
		jaw_m.build_setup()
	
	
	
	def build_rig() :
		jaw_m = jaw.Jaw(side = 'm' , joint_parent = None , control_parent = None)
		jaw_m.build_rig()
	
	
	
	build_setup()
	build_rig()
