# coding=utf,8
'''
脸颊的绑定系统创建
'''
import os

import maya.cmds as cmds

from ...base import base



class Cheek(base.Base) :
	
	
	
	# 脸颊的绑定靠定位关节点来绑定，
	
	def __init__(self , side , name , joint_number = 8 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		
		self._rtype = ''
		self.radius = 0.1
		self.shape = 'pPlatonic'
		# 创建列表来存储命名规范
		self.bpjnt_list = list()
		self.jnt_list = list()
		self.ctrl_list = list()
		
		# 颧骨关节三个
		self.cheekbone_bpjnt_list = list()
		self.cheekbone_jnt_list = list()
		self.cheekbone_ctrl_list = list()
		
		# 法令纹关节三个
		self.nasolabial_bpjnt_list = list()
		self.nasolabial_jnt_list = list()
		self.nasolabial_ctrl_list = list()
		
		# 脸颊关节两个
		self.cheek_bpjnt_list = list()
		self.cheek_jnt_list = list()
		self.cheek_ctrl_list = list()
	
	
	
	def create_namespace(self) :
		u"""
		创建名称规范整理
		"""
		# 颧骨层级名称整理,颧骨关节三个
		for side in ['l' , 'r'] :
			for i in range(3) :
				self.cheekbone_bpjnt_list.append(
						'bpjnt_{}_{}{}CheekBone_{:03d}'.format(side , self.name , self._rtype , i + 1))
				self.cheekbone_jnt_list.append(
						'jnt_{}_{}{}CheekBone_{:03d}'.format(side , self.name , self._rtype , i + 1))
				self.cheekbone_ctrl_list.append(
						'ctrl_{}_{}{}CheekBone_{:03d}'.format(side , self.name , self._rtype , i + 1))
			# 法令纹层级名称整理，法令纹关节三个
			for i in range(3) :
				self.nasolabial_bpjnt_list.append(
						'bpjnt_{}_{}{}Nasolabial_{:03d}'.format(side , self.name , self._rtype , i + 1))
				self.nasolabial_jnt_list.append(
						'jnt_{}_{}{}Nasolabial_{:03d}'.format(side , self.name , self._rtype , i + 1))
				self.nasolabial_ctrl_list.append(
						'ctrl_{}_{}{}Nasolabial_{:03d}'.format(side , self.name , self._rtype , i + 1))
			
			# 脸颊层级名称整理，脸颊关节两个
			for i in range(2) :
				self.cheek_bpjnt_list.append(
						'bpjnt_{}_{}{}Cheek_{:03d}'.format(side , self.name , self._rtype , i + 1))
				self.cheek_jnt_list.append(
						'jnt_{}_{}{}Cheek_{:03d}'.format(side , self.name , self._rtype , i + 1))
				self.cheek_ctrl_list.append(
						'ctrl_{}_{}{}Cheek_{:03d}'.format(side , self.name , self._rtype , i + 1))
		
		# 整理所有的层级名称
		self.bpjnt_list = self.cheekbone_bpjnt_list + self.nasolabial_bpjnt_list + self.cheek_bpjnt_list
		self.jnt_list = self.cheekbone_jnt_list + self.nasolabial_jnt_list + self.cheek_jnt_list
		self.ctrl_list = self.cheekbone_ctrl_list + self.nasolabial_ctrl_list + self.cheek_ctrl_list
		self.ctrl_grp = ('grp_{}_{}{}_001'.format(self._side , self._name , self._rtype))
	
	
	
	def create_bpjnt(self) :
		# 获得cheek_bpjnt 的路径
		self.cheek_bpjnt_path = os.path.abspath(__file__ + "/../cheek_bpjnt.ma")
		# 导入关节
		cmds.file(self.cheek_bpjnt_path , i = True , rnn = True)



if __name__ == "__main__" :
	def build_setup() :
		cheek_m = cheek.Cheek(side = 'm' , name = '' , joint_number = 8 , joint_parent = None ,
		                      control_parent = None)
		cheek_m.build_setup()
	
	
	
	def build_rig() :
		cheek_m = cheek.Cheek(side = 'm' , name = '' , joint_number = 8 , joint_parent = None ,
		                      control_parent = None)
		cheek_m.build_rig()
	
	
	
	build_setup()
	build_rig()
