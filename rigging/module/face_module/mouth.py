# coding=utf,8
'''
嘴巴的绑定系统创建
'''
import json
import os
from importlib import reload

import maya.cmds as cmds

from ...base import base , bone
from ...chain import chain , chainFK
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils
from . import mouthLip

reload(mouthLip)


class Mouth(bone.Bone) :
	
	
	
	def __init__(self , side , name , joint_number = 7 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		
		# 生成上部分的嘴唇
		self.mouth_lip_upper = mouthLip.MouthLip(side = self.side , name = 'upper' , joint_number = 7 , joint_parent = None ,
		                                   control_parent = None)
		
		# 生成下部分的嘴唇
		self.mouth_lip_lower = mouthLip.MouthLip(side = self.side , name = 'lower' , joint_number = 7 ,
		                                     joint_parent = None ,
		                                     control_parent = None)
		
	
	def create_namespace(self) :
		super().create_namespace()
		self.mouth_lip_upper.create_namespace()
		self.mouth_lip_lower.create_namespace()
	
	
	
	def create_bpjnt(self) :
		# 创建上下嘴唇的控制器曲线
		self.mouth_lip_upper.build_curve()
		self.mouth_lip_lower.build_curve()
	
	
	
	