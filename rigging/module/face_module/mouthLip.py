# coding=utf,8
'''
嘴唇的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base , bone
from ...chain import chain , chainFK
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils



class MouthLip(bone.Bone) :
	
	
	
	def __init__(self , side , name , joint_number = 7 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		# 定位用的曲线
		self._name = name
		self.shape = 'cube'
		self._rtype = 'MouthLip'
		self.radius = 0.05
		self.joint_number = joint_number
		self.curve_jnt_list = list()
		self.skin_curve = 'crv_{}_{}{}Skin_001'.format(self._side , self._name , self._rtype)
		
	
	def create_namespace(self) :
		super().create_namespace()
		# 整理与控制器有关的曲线的名称规范层级结构
		self.curve = 'crv_{}_{}{}_001'.format(self._side , self._name , self._rtype)
		for index in range(7) :
			self.curve_jnt_list.append('jnt_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , index + 1))
		self.curve_jnt_grp = 'grp_{}_{}{}SkinJnts_001'.format(self._side , self._name , self._rtype)
		self.curve_nodes_grp = 'grp_{}_{}{}RigNodes_001'.format(self._side , self._name , self._rtype)
		
		# 整理与蒙皮关节有关的曲线名称规范层级结构
		self.skin_curve = 'crv_{}_{}{}Skin_001'.format(self._side , self._name , self._rtype)
		self.skin_jnt_grp = 'grp_{}_{}{}SkinJnts_001'.format(self._side , self._name , self._rtype)
		self.skin_nodes_grp = 'grp_{}_{}{}SkinRigNodes_001'.format(self._side , self._name , self._rtype)
		
		# 整理与向上参考曲线有关的曲线名称规范层级结构
		self.aim_curve = 'crv_{}_{}{}Aim_001'.format(self._side , self._name , self._rtype)
		self.aim_jnt_grp = 'grp_{}_{}{}AimJnts_001'.format(self._side , self._name , self._rtype)
		self.aim_nodes_grp = 'grp_{}_{}{}AimRigNodes_001'.format(self._side , self._name , self._rtype)
	
	
	
	def build_curve(self) :
		u"""
				根据选择的模型点创建用于定位的曲线来创建控制器曲线
		"""
		
		# 根据skin_curve来制作curve，用于制作控制器的控制
		print(self.curve)
		self.curve = cmds.duplicate(self.skin_curve , name = self.curve)[0]
		cmds.setAttr(self.skin_curve + '.visibility' , 0)
		# 重建self.curve用来控制曲线
		self.curve = \
			cmds.rebuildCurve(self.curve , ch = 1 , rpo = 1 , rt = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 , kt = 0 ,
			                  s = 4 , d = 3 , tol = 0.01)[0]
		
			



	