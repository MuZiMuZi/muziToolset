# coding=utf,8
'''
眼皮的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base , bone
from ...chain import chain , chainFK
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils



reload(pipelineUtils)
reload(jointUtils)



class EyeLid(bone.Bone) :
	
	
	
	def __init__(self , side , name , joint_number = 5 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		
		self.shape = 'circle'
		self._rtype = 'EyeLid'
		self.radius = 0.15
		self.curve_jnt_list = list()
	
	
	
	def create_namespace(self) :
		u"""
		创建名称规范整理
		"""
		super().create_namespace()
		self.skin_curve = 'crv_{}_{}{}Skin_001'.format(self._side , self._name , self._rtype)
		self.curve = 'crv_{}_{}{}_001'.format(self._side , self._name , self._rtype)
		for index in range(7) :
			self.curve_jnt_list.append('jnt_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , index + 1))
		self.curve_jnt_grp = 'grp_{}_{}{}Jnts_001'.format(self._side , self._name , self._rtype)
	
	
	
	def build_curve(self) :
		u"""
		根据选择的模型点创建用于定位的曲线
		"""
		# 判断场景里是否已经生成过skin_curve，如果有的话则将其删除，没有的话则新创建
		
		if cmds.objExists(self.skin_curve) :
			cmds.delete(self.skin_curve)
		else :
			# 根据所选择的点创建Skin关节定位曲线
			self.skin_curve = pipelineUtils.Pipeline.create_curve_on_polyToCurve(self.skin_curve , degree = 3)[0]
		
		# 根据skin_curve来制作curve，用于制作控制器的控制
		self.curve = cmds.duplicate(self.skin_curve , name = self.curve)[0]
		cmds.setAttr(self.skin_curve + '.visibility' , 0)
		# 重建self.curve用来控制曲线
		self.curve = \
			cmds.rebuildCurve(self.curve , ch = 1 , rpo = 1 , rt = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 , kt = 0 ,
			                  s = 4 , d = 3 , tol = 0.01)[0]
		
		# 在曲线上创建关节用来蒙皮曲线创建控制器的约束
		cmds.select(self.curve)
		jnt_list = jointUtils.Joint.create_joints_on_curve(is_parent = False)['jnt_list']
		for index , jnt in enumerate(jnt_list) :
			cmds.rename(jnt , self.curve_jnt_list[index])
		self.curve_jnt_grp = cmds.rename('grp_{}Jnts'.format(self.curve) , self.curve_jnt_grp)
		cmds.skinCluster(self.curve_jnt_list , self.curve)
	
	
	
	def build_setup(self) :
		"""
		创建定位曲线,生成准备
		"""
		self.create_namespace()
	
	
	
	def build_rig(self) :
		super().build_rig()
