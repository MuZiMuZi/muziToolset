u"""
matehumanUtils：这是一个用来对matehuman的基础功能定义的模块

目前已有的功能：
get_mateHuman_drv_jnt:定义matehuman的骨架结构,查询到对应的模块后返回对应的关节
mateHuman_decompose:拆分mateHuman的关节名称
export_face_animation:导出面部的动画在文件的路径下
export_body_animation:导出身体的动画在文件的路径下
reset_mateHuman_control:重置控制器上所有的数值.

"""

from importlib import reload

import maya.cmds as cmds

from . import pipelineUtils,fileUtils



reload(pipelineUtils)



class MateHuman() :
	
	
	
	def __init__(self , name) :
		self.name = name
		self.side = None
		self.description = None
		self.index = None
		
		self.mateHuman_decompose()
	
	
	
	@staticmethod
	def get_mateHuman_drv_jnt(description) :
		u'''
		定义matehuman的骨架结构,查询到对应的模块后返回对应的关节
		'''
		mateHuman_joint_trunk_dict = {
				'root' : 'root_drv' ,
				'pelvis' : 'pelvis_drv' ,
				'spine' : ['spine_01_drv' , 'spine_02_drv' , 'spine_03_drv' , 'spine_04_drv' ,
				           'spine_05_drv'] ,
				'neck' : ['neck_01_drv' , 'neck_02_drv' , 'head_drv'] ,
				'head ' : 'head_drv'
				}
		
		mateHuman_joint_arm_dict = {
				'clavicle_l' : 'clavicle_l_drv' ,
				'arm_l' : ['upperarm_l_drv' , 'lowerarm_l_drv' , 'hand_l_drv'] ,
				'hand_l' : 'hand_l_drv' ,
				'wrist_l' : 'wrist_l_drv' ,
				'index_finger_l' : ['index_metacarpal_l_drv' , 'index_01_l_drv' , 'index_02_l_drv' ,
				                    'index_03_l_drv'] ,
				'middle_finger_l' : ['middle_metacarpal_l_drv' , 'middle_01_l_drv' ,
				                     'middle_02_l_drv' , 'middle_03_l_drv'] ,
				'ring_finger_l' : ['ring_metacarpal_l_drv' , 'ring_01_l_drv' , 'ring_02_l_drv' ,
				                   'ring_03_l_drv'] ,
				'pinky_finger_l' : ['pinky_metacarpal_l_drv' , 'pinky_01_l_drv' , 'pinky_02_l_drv' ,
				                    'pinky_03_l_drv'] ,
				'thumb_finger_l' : ['thumb_01_l_drv' , 'thumb_02_l_drv' , 'thumb_03_l_drv'] ,
				
				'clavicle_r' : 'clavicle_r_drv' ,
				'upperarm_r' : 'upperarm_r_drv' ,
				'lowerarm_r' : 'lowerarm_r_drv' ,
				'arm_r' : ['upperarm_r_drv' , 'lowerarm_r_drv' , 'hand_r_drv'] ,
				'hand_r' : 'hand_r_drv' ,
				'wrist_r' : 'wrist_r_drv' ,
				'index_finger_r' : ['index_metacarpal_r_drv' , 'index_01_r_drv' , 'index_02_r_drv' ,
				                    'index_03_r_drv'] ,
				'middle_finger_r' : ['middle_metacarpal_r_drv' , 'middle_01_r_drv' ,
				                     'middle_02_r_drv' , 'middle_03_r_drv'] ,
				'ring_finger_r' : ['ring_metacarpal_r_drv' , 'ring_01_r_drv' , 'ring_02_r_drv' ,
				                   'ring_03_r_drv'] ,
				'pinky_finger_r' : ['pinky_metacarpal_r_drv' , 'pinky_01_r_drv' ,
				                    'pinky_02_r_drv' , 'pinky_03_r_drv'] ,
				'thumb_finger_r' : ['thumb_01_r_drv' , 'thumb_02_r_drv' , 'thumb_03_r_drv']
				}
		
		mateHuman_joint_leg_dict = {
				'leg_l' : ['thigh_l_drv' , 'calf_l_drv' , 'foot_l_drv'] ,
				'thigh_l' : 'thigh_l_drv' ,
				'calf_l' : 'calf_l_drv' ,
				'foot_l' : 'foot_l_drv' ,
				'ball_l' : 'ball_l_drv' ,
				
				'bigtoe_l' : ['bigtoe_01_l_drv' , 'bigtoe_02_l_drv'] ,
				'indextoe_l' : ['indextoe_01_l_drv' , 'indextoe_02_l_drv'] ,
				'middletoe_l' : ['middletoe_01_l_drv' , 'middletoe_02_l_drv'] ,
				'littletoe_l' : ['littletoe_01_l_drv' , 'littletoe_02_l_drv'] ,
				'ringtoe_l' : ['ringtoe_01_l_drv' , 'ringtoe_02_l_drv'] ,
				
				'leg_r' : ['thigh_r_drv' , 'calf_r_drv' , 'foot_r_drv'] ,
				'thigh_r' : 'thigh_r_drv' ,
				'calf_r' : 'calf_r_drv' ,
				'foot_r' : 'foot_r_drv' ,
				'ball_r' : 'ball_r_drv' ,
				
				'bigtoe_r' : ['bigtoe_01_r_drv' , 'bigtoe_02_r_drv'] ,
				'indextoe_r' : ['indextoe_01_r_drv' , 'indextoe_02_r_drv'] ,
				'middletoe_r' : ['middletoe_01_r_drv' , 'middletoe_02_r_drv'] ,
				'littletoe_r' : ['littletoe_01_r_drv' , 'littletoe_02_r_drv'] ,
				'ringtoe_r' : ['ringtoe_01_r_drv' , 'ringtoe_02_r_drv']
				}
		
		for mateHuman_dict in [mateHuman_joint_trunk_dict , mateHuman_joint_arm_dict , mateHuman_joint_leg_dict] :
			if description in mateHuman_dict :
				return mateHuman_dict[description]
			else :
				pass
	
	
	
	def mateHuman_decompose(self) :
		u'''
		拆分mateHuman的关节名称
		'''
		name_parts = self.name.split('_')
		self.description = name_parts[0]
		# 当len(name_parts) == 3 的时候，关节为spine_01_drv或者是clavicle_l_drv类型的关节
		if len(name_parts) == 3 :
			# 当关节为spine_01_drv类型的时候
			if self.description in ['spine' , 'neck'] :
				self.side = 'm'
				self.index = name_parts[1]
			# 当关节为clavicle_l_drv类型的关节
			else :
				self.side = name_parts[1]
				self.index = 1
		# 情况为关节为root，pelvis，head的drv关节
		elif len(name_parts) == 2 :
			self.side = 'm'
			self.index = 1
		# 情况为关节为ankle_bckOff_l_drv，ankle_bckOff_r_drv的修型关节
		elif len(name_parts) == 4 :
			self.function = name_parts[1]
			self.side = name_parts[2]
		# 情况为关节为calf_twist_02_r_drv，calf_twist_01_r_drv的修型关节，len(name_parts) == 5
		else :
			self.function = name_parts[1]
			self.index = name_parts[2]
			self.side = name_parts[3]
	
	
	
	@staticmethod
	def export_face_animation() :
		u'''
		导出面部的动画在文件的路径下
		:return:
		'''
		# 获取maya文件的路径
		scene_path = fileUtils.File.get_current_scene_path() + '_face_animation'
		
		# 选择matehuman的动画数据
		cmds.select('FacialControls')
		pipelineUtils.Pipeline.fbxExport(scene_path)
	
	
	
	@staticmethod
	def export_body_animation() :
		u'''
		导出身体的动画在文件的路径下
		:return:
		'''
		# 获取maya文件的路径
		scene_path = fileUtils.File.get_current_scene_path () + '_body_animation'
		
		# 选择matehuman的动画数据
		cmds.select('Body_joints')
		body_jnt = cmds.ls(sl = True)
		# 需要选择骨架烘焙完所有动画在导出
		# 查询当前文件的起始帧
		start_frame = int(cmds.playbackOptions(query = True , minTime = True))
		# 查询当前文件的结束帧
		end_frame = int(cmds.playbackOptions(query = True , maxTime = True))
		
		# 根据当前文件的起始帧和结束帧烘培动画
		cmds.bakeResults(body_jnt , time = (start_frame , end_frame) , simulation = True)
		pipelineUtils.Pipeline.fbxExport(scene_path)
	
	
	
	@staticmethod
	def reset_mateHuman_control() :
		u"""重置控制器上所有的数值.



		 """
		# 重置ikfk控制器
		ctrls = cmds.ls('*ctrl_*' , type = 'transform')
		attrs = ['translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ']
		scale_attrs = ['scaleX' , 'scaleY' , 'scaleZ']
		for ctrl in ctrls :
			for attr in attrs :
				lock_val = cmds.getAttr(ctrl + '.{}'.format(attr) , lock = True)
				if lock_val == 0 :
					cmds.setAttr(ctrl + '.{}'.format(attr) , 0)
				else :
					pass
			for scale_attr in scale_attrs :
				lock_val = cmds.getAttr(ctrl + '.{}'.format(scale_attr) , lock = True)
				if lock_val == 0 :
					cmds.setAttr(ctrl + '.{}'.format(scale_attr) , 1)
				else :
					pass
		# 重置ikfk切换控制器
		ctrl_ikfkblends = cmds.ls('ikfkctrl_*' , type = 'transform')
		for ctrl_ikfkblend in ctrl_ikfkblends :
			cmds.setAttr(ctrl_ikfkblend + '.IkFkBend' , 1)
		
		# 重置手指pose控制器
		ctrl_poses = cmds.ls('fkposectrl_*' , type = 'transform')
		for ctrl_pose in ctrl_poses :
			for finger in ['pinky' , 'thumb' , 'index' , 'middle' , 'ring'] :
				cmds.setAttr(ctrl_pose + '.{}Curl'.format(finger) , 0)
