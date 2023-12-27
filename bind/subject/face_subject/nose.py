# coding=utf-8
'''
鼻子的绑定系统创建
'''
import os

import maya.cmds as cmds

from .... core import controlUtils , jointUtils , pipelineUtils
from ...module.base import base

from importlib import reload


reload (base)

class Nose(base.Base) :
	
	
	
	def __init__(self , side = 'm' , name = '' , jnt_number = 2 , jnt_parent = None , control_parent = None) :
		super().__init__(side , name , jnt_number , jnt_parent , control_parent)
		self.shape = 'cube'
		self.rtype = 'Nose'
		self.radius = 0.2
		
		self.side_bpjnt_list = list()
		self.side_jnt_list = list()
	
	
	
	def create_namespace(self) :
		# 创建用于定位的四边的鼻子关节
		self.bottom_bpjnt = 'bpjnt_m_Nose{}_001'.format('Bottom')
		self.front_bpjnt = 'bpjnt_m_Nose{}_001'.format('Front')
		for side in ['l' , 'r'] :
			self.side_bpjnt_list.append('bpjnt_{}_NoseSide_001'.format(side))
		self.side_bpjnt_list.append(self.bottom_bpjnt)
		self.side_bpjnt_list.append(self.front_bpjnt)
		
		for bpjnt in self.side_bpjnt_list :
			self.side_jnt_list.append(bpjnt.replace('bpjnt' , 'jnt'))
		super ().create_namespace ()
	
	
	
	def create_bpjnt(self) :
		# 获得nose_bpjnt 的路径
		self.nose_bpjnt_path = os.path.abspath(__file__ + "/../../../bpjnt/nose_bpjnt.ma")
		# 导入关节
		cmds.file(self.nose_bpjnt_path , i = True , rnn = True)
	
	
	
	def create_joint(self) :
		'''
		根据定位的bp关节创建关节
		'''
		# 根据bp关节创建新的关节
		parent = self.jnt_parent
		for bpjnt , jnt in zip(self.bpjnt_list , self.jnt_list) :
			jnt = cmds.createNode('joint' , name = jnt , parent = parent)
			cmds.matchTransform(jnt , bpjnt)
			parent = jnt
		# 创建botton关节和front关节，side关节
		for bpjnt in self.side_bpjnt_list :
			jnt = cmds.createNode('joint' , name = bpjnt.replace('bpjnt' , 'jnt') , parent = self.jnt_list[-1])
			cmds.matchTransform(jnt , bpjnt)
		# 进行关节定向
		jointUtils.Joint.joint_orientation(self.jnt_list)
		cmds.joint(self.jnt_list[-1] , zeroScaleOrient = 1 , children = 1 , e = 1 , orientJoint = 'none')
		# 定向四边的关节，无子关节，关节定向为世界方向
		for jnt in self.side_jnt_list :
			cmds.makeIdentity(jnt , apply = True , translate = 1 , rotate = 1 , scale = 1 , normal = 0 ,
			                  preserveNormals = 1)
			cmds.joint(jnt , zeroScaleOrient = 1 , children = 1 , e = 1 , orientJoint = 'none')
		# 删除定位的bp关节
		cmds.delete(self.bpjnt_list[0])
	
	
	
	def create_ctrl(self) :
		u"""
		创建控制器
		"""
		self.set_shape(self.shape)
		# 创建整体的控制器层级组
		self.ctrl_grp = cmds.createNode('transform' , name = self.ctrl_grp , parent = self.control_parent)
		parent = self.ctrl_grp
		for ctrl , jnt in zip(self.ctrl_list , self.jnt_list) :
			self.ctrl = controlUtils.Control.create_ctrl(ctrl , shape = self.shape ,
			                                             radius = self.radius ,
			                                             axis = 'X+' , pos = jnt ,
			                                             parent = parent)
			parent = self.ctrl.replace('ctrl' , 'output')
		# 创建四边的控制器
		for jnt in self.side_jnt_list :
			ctrl = controlUtils.Control.create_ctrl(jnt.replace('jnt' , 'ctrl') , shape = 'ball' ,
			                                        radius = self.radius ,
			                                        axis = 'X+' , pos = jnt ,
			                                        parent = self.ctrl_list[-1])
		# 左边的控制器上层的组scaleY需要给个-1值对称
		cmds.setAttr(self.side_jnt_list[1].replace('jnt' , 'offset') + '.scaleY' , -1)
	
	
	
	def add_constraint(self) :
		super().add_constraint()
		# side控制器与对应的关节组做约束
		for bpjnt in self.side_bpjnt_list :
			output_ctrl = bpjnt.replace('bpjnt' , 'output')
			jnt = bpjnt.replace('bpjnt' , 'jnt')
			pipelineUtils.Pipeline.create_constraint(output_ctrl , jnt ,
			                                         point_value = False ,
			                                         orient_value = False , parent_value = True,scale_value =
			                                         True ,
			                                         mo_value = True)



if __name__ == "__main__" :
	def build_setup() :
		nose_m = nose.Nose(jnt_parent = None , control_parent = None)
		nose_m.build_setup()
	
	
	
	def build_rig() :
		nose_m = nose.Nose(jnt_parent = None , control_parent = None)
		nose_m.build_rig()
	
	
	
	# #
	# # #
	build_setup()
	build_rig()
