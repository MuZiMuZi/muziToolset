# coding=utf-8

u"""
这是一个用来编写自动绑定系统的基础类，之后的绑定都会在这个类的基础上逐级继承下去

目前已有的功能：

get_modular_bp_joints：根据给定关节模块的名称来获取对应的模块组关节的名称

default_grp：创建绑定的初始层级组，并隐藏连接对应的属性

setup: 绑定生成的预设步骤，导入对应的模型和关节结构

make： 根据给定的bp_joints关节的名称来创建对应的模块组

"""
from importlib import reload
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.nameUtils as nameUtils
import pymel.core as pm



class Base_Rig(object) :
	
	
	
	def __init__(self) :
		super(Base_Rig , self).__init__()
		self.side = None
		if self.side == 'l' :
			self.side_value = 1
		elif self.side == 'r' :
			self.side_value = -1
		#定义层级架构命名
		self.define_naming_conventions()
		#创建绑定的初始层级组，并隐藏连接对应的属性
		self.rig_top_grp = 'group'
		if not cmds.objExists(self.rig_top_grp) :
			self.create_master_grp()
		
		
	
	
	def define_naming_conventions(self) :
		u'''
		定义命名规范
		:return:
		'''
		# 定义世界的层级组架构
		self.character_ctrl = 'ctrl_m_character_001'
		self.world_ctrl = 'ctrl_m_world_001'
		self.cog_ctrl = 'ctrl_m_cog_001'
		self.custom_ctrl = 'ctrl_m_custom_001'
		
		self.group = 'group'
		self.geometry = 'geometry'
		self.control = 'control'
		self.custom = 'custom'
		
		self.rigNode = 'rigNode'
		self.joint = 'joint'
		self.rigNode_Local = 'rigNode_Local'
		self.rigNode_World = 'rigNode_World'
		self.nCloth = 'nCloth'
		self.modular_rig = 'modular_rig'
		
		self.low_modle_grp = 'grp_m_low_modle_001'
		self.mid_modle_grp = 'grp_m_mid_modle_001'
		self.high_modle_grp = 'grp_m_high_modle_001'
		
		self.rig_ctrl = [self.character_ctrl , self.world_ctrl , self.cog_ctrl , self.custom_ctrl]
		self.rig_hierarchy_grp = [self.group , self.geometry , self.control , self.custom , self.rigNode , self.joint ,
		                          self.rigNode_Local , self.rigNode_World , self.nCloth ,
		                          self.modular_rig , self.low_modle_grp , self.mid_modle_grp , self.high_modle_grp]
		
		# 定义绑定模块
		
		self.arm_rig = 'arm_rig'
		self.hand_rig = 'hand_rig'
		self.leg_rig = 'leg_rig'
		self.foot_rig = 'foot_rig'
		self.neck_rig = 'neck_rig'
		self.spine_rig = 'spine_rig'
		self.chest_rig = 'chest_rig'
		self.modular_rig_list = [self.arm_rig , self.hand_rig , self.leg_rig , self.foot_rig , self.neck_rig ,
		                         self.spine_rig , self.chest_rig]
	
	
	
	def get_modular_bp_joints(self , modular) :
		u"""
		根据给定关节模块的名称来获取对应的模块组关节的名称
		"""
		modular_bp_joints = cmds.listRelatives(modular , ad = True , c = True)
		modular_bp_joints.reverse()
		return modular_bp_joints
	
	
	
	def make(self , bp_joints) :
		u"""
		根据给定的bp_joints关节的名称来创建对应的模块组
		"""
		main_obj = nameUtils.Name(name = bp_joints[0])
		main_obj.description = main_obj.description + 'RigModule'
		main_obj.type = 'grp'
		self.control_grp = cmds.group(name = main_obj.name.replace('RigModule' , 'Ctrl') , em = True ,
		                              parent = self.cog_ctrl.replace('ctrl_' , 'output_'))
		self.jnt_grp = cmds.group(name = main_obj.name.replace('RigModule' , 'Jnt') , em = True ,
		                          parent = self.joint)
		self.rigNodes_Local_grp = cmds.group(name = main_obj.name.replace('RigModule' , 'RigNodesLocal') , em = True ,
		                                     parent = self.rigNode_Local)
		self.rigNodes_World_grp = cmds.group(name = main_obj.name.replace('RigModule' , 'RigNodesWorld') , em = True ,
		                                     parent = self.rigNode_World)
		self.space_grp = cmds.group(name = main_obj.name.replace('RigModule' , 'Space') , em = True ,
		                            parent = self.control_grp)
		# 设置组的可见性
		cmds.setAttr(self.space_grp + '.visibility' , 0)
	
	
	
	@staticmethod
	def add_spaceSwitch(object , space_list) :
		u"""
		添加空间切换
		:param object: 需要添加空间切换的对象
		:param space_list(list): 添加空间切换的空间
		:return:
		"""
		
		# 在对象上添加空间切换的属性控制
		cmds.addAttr(object , longName = 'spaceSwitch' , niceName = u'空间切换' , attributeType = 'enum' ,
		             en = ":".join(space_list) , keyable = True)
		
		for space_name in space_list :
			# 创建用于空间切换的定位器
			object_obj = nameUtils.Name(name = object)
			object_obj.type = 'loc'
			object_obj.description = object_obj.description + 'Space' + space_name
			loc_node = cmds.spaceLocator(name = object_obj.name)[0]
			# 创建定位器上层的组并吸附到添加空间切换的对象的位置
			loc_zero = cmds.createNode('transform' , name = loc_node.replace('loc_' , 'zero_'))
			cmds.parent(loc_node , loc_zero)
			cmds.matchTransform(loc_zero , object , position = True , rotation = True , scale = True)
			# 定位器对添加空间切换的对象上层的组做父子约束，并且整理层级
			cmds.parentConstraint(loc_node , object.replace('ctrl_' , 'space_') , mo = False)
			cmds.parent(loc_zero , 'grp_m_{}Space_001'.format(space_name))
			# 创建用于空间切换的判断节点
			space_cond_node = cmds.createNode('condition' , name = loc_node.replace('loc_' , 'cond_'))
			cmds.setAttr(space_cond_node + '.colorIfTrueR' , 1)
			cmds.setAttr(space_cond_node + '.colorIfFalseR' , 0)
			cmds.connectAttr(object + '.spaceSwitch' , space_cond_node + '.firstTerm')
			cmds.setAttr(space_cond_node + '.secondTerm' , space_list.index(space_name))
			# 连接约束节点
			constraint_node = object.replace('ctrl_' , 'space_') + '_parentConstraint1'
			cmds.connectAttr(space_cond_node + '.outColorR' ,
			                 constraint_node + '.{}W{}'.format(loc_node , space_list.index(space_name)))
	
	
	
	def mirror_bp_joint(self) :
		u"""
		镜像关节。
		关节镜像的规律：
		首端关节平移X*-1
		关节方向x，y，z*-1

		中端及末端的关节x*-1

		:param bpjnt_list: 默认摆放定位的关节
		:return:
		"""
		import pymel.core as pm
		
		
		
		# 获取场景内所有需要镜像的绑定模块
		bpjnt_lists = pm.ls('l_*_rig')
		# 获取各个绑定模块的关节列表
		for bpjnt_list in bpjnt_lists :
			bpjnt_list_jnts = cmds.listRelatives('{}'.format(bpjnt_list) , ad = True , c = True)
			bpjnt_list_jnts.reverse()
			# 对关节列表的所有关节的位移和关节方向进行设置
			for jnt in bpjnt_list_jnts :
				if pm.objectType(jnt) == 'joint' :
					mirror_jnt = jnt.replace('_l_' , '_r_')
					cmds.setAttr(mirror_jnt + '.translateX' , cmds.getAttr(jnt + '.translateX') * -1)
					for axis in ['X' , 'Y' , 'Z'] :
						cmds.setAttr(mirror_jnt + '.jointOrient' + axis , cmds.getAttr(jnt + '.jointOrient' + axis))
			# 对关节列表的初始关节设置位移和关节方向
			mirror_start_jnt = bpjnt_list_jnts[0].replace('_l_' , '_r_')
			if pm.objectType(bpjnt_list_jnts[0]) == 'joint' :
				cmds.setAttr(mirror_start_jnt + '.jointOrient' + 'X' ,
				             cmds.getAttr(bpjnt_list_jnts[0] + '.jointOrient' + 'X') - 180)
				for axis in ['Y' , 'Z'] :
					cmds.setAttr(mirror_start_jnt + '.jointOrient' + axis ,
					             cmds.getAttr(bpjnt_list_jnts[0] + '.jointOrient' + axis) * -1)
			# 对关节列表的最后一个关节清空关节定向
			if pm.objectType(bpjnt_list_jnts[-1]) == 'joint' :
				for axis in ['X' , 'Y' , 'Z'] :
					cmds.setAttr(bpjnt_list_jnts[-1] + '.jointOrient' + axis , 0)
		
		# 单独设置锁骨关节的关节方向
		if cmds.objExists('bpjnt_l_clavicle_001') :
			bp_clavicle_jnt = 'bpjnt_l_clavicle_001'
			mirror_clavicle_jnt = bp_clavicle_jnt.replace('_l_' , '_r_')
			cmds.setAttr(mirror_clavicle_jnt + '.jointOrient' + 'X' ,
			             cmds.getAttr(bp_clavicle_jnt + '.jointOrient' + 'X') - 180)
		# 单独设置手腕关节的关节方向
		if cmds.objExists('bpjnt_l_wrist_001') :
			bp_wrist_jnt = 'bpjnt_l_wrist_001'
			mirror_wrist_jnt = bp_wrist_jnt.replace('_l_' , '_r_')
			for axis in ['X' , 'Y' , 'Z'] :
				cmds.setAttr(bp_wrist_jnt + '.jointOrient' + axis , 0)
				cmds.setAttr(mirror_wrist_jnt + '.jointOrient' + axis , 0)
	
	
	
	def create_master_grp(self) :
		u'''
		创建绑定的初始层级组，并隐藏连接对应的属性
		'''
		# 根据self.rig_hierarchy_grp 来创建对应的层级组
		for transform in self.rig_hierarchy_grp :
			cmds.createNode('transform' , name = transform)
		
		# 制作层级关系
		cmds.parent(self.geometry , self.custom , self.control , self.group)
		
		# 创建RigNode层级下的子层级组并做层级关系
		cmds.parent(self.rigNode_Local , self.rigNode_World , self.rigNode)
		cmds.parent(self.rigNode , self.joint , self.nCloth , self.modular_rig , self.custom)
		
		# 创建Modle层级下的子层级组并且做层级关系
		cmds.parent(self.low_modle_grp , self.mid_modle_grp , self.high_modle_grp , self.geometry)
		attrs_list = ['.translateX' , '.translateY' , '.translateZ' , '.rotateX' , '.rotateY' , '.rotateZ' ,
		              '.scaleX' ,
		              '.scaleY' ,
		              '.scaleZ' , '.visibility' , '.rotateOrder' , '.subCtrlVis']
		# 创建总控制器Character
		controlUtils.Control.create_ctrl(self.character_ctrl , shape = 'circle' , radius = 40 ,
		                                 axis = 'X+' ,
		                                 pos = None ,
		                                 parent = self.control)
		cmds.addAttr(self.character_ctrl , longName = 'rigScale' , niceName = u'绑定缩放' , attributeType = 'double' ,
		             defaultValue = 1 ,
		             keyable = True)
		for attr in ['.scaleX' , '.scaleY' , '.scaleZ'] :
			cmds.connectAttr(self.character_ctrl + '.rigScale' , self.character_ctrl + attr)
			cmds.setAttr(self.character_ctrl + attr , lock = True , keyable = False , channelBox = False)
		
		# 创建世界控制器
		controlUtils.Control.create_ctrl(self.world_ctrl , shape = 'local' , radius = 35 , axis = 'Z-' ,
		                                 pos = None ,
		                                 parent = self.character_ctrl.replace('ctrl_' , 'output_'))
		
		controlUtils.Control.create_ctrl(self.cog_ctrl , shape = 'circle' , radius = 20 , axis = 'X+' ,
		                                 pos = None ,
		                                 parent = self.world_ctrl.replace('ctrl_' , 'output_'))
		# 创建一个自定义的控制器，用来承载自定义的属性
		controlUtils.Control.create_ctrl(self.custom_ctrl , shape = 'cross' , radius = 3 , axis = 'X+' ,
		                                 pos = None ,
		                                 parent = self.custom)
		cmds.parentConstraint(self.character_ctrl , self.custom_ctrl , mo = True)
		cmds.scaleConstraint(self.character_ctrl , self.custom_ctrl , mo = True)
		
		# 创建自定义的控制器属性
		for attr in ['geometryVis' , 'controlsVis' , 'rigNodesVis' , 'jointsVis'] :
			if not cmds.objExists('{}.{}'.format(self.custom_ctrl , attr)) :
				cmds.addAttr(self.custom_ctrl , longName = attr , attributeType = 'bool' , defaultValue = 1 ,
				             keyable = True)
		
		# 添加精度切换的属性
		if not cmds.objExists('{}.resolution'.format(self.custom_ctrl)) :
			cmds.addAttr(self.custom_ctrl , longName = 'resolution' , attributeType = 'enum' ,
			             enumName = 'low:mid:high' ,
			             keyable = True)
			for idx , res in {0 : 'low' , 1 : 'mid' , 2 : 'high'}.items() :
				cnd_node = 'resolution_{}_conditionNode'.format(res)
				if not cmds.objExists(cnd_node) :
					cnd_node = cmds.createNode('condition' , name = cnd_node)
				cmds.connectAttr('{}.resolution'.format(self.custom_ctrl) , '{}.firstTerm'.format(cnd_node) ,
				                 force = True)
				cmds.setAttr('{}.secondTerm'.format(cnd_node) , idx)
				cmds.setAttr('{}.colorIfTrueR'.format(cnd_node) , 1)
				cmds.setAttr('{}.colorIfFalseR'.format(cnd_node) , 0)
				cmds.connectAttr('{}.outColorR'.format(cnd_node) , 'grp_m_{}_modle_001.visibility'.format(res) ,
				                 force = True)
		
		# 添加模型显示方式的属性
		if not cmds.objExists('{}.geometryDisplayType'.format(self.character_ctrl)) :
			cmds.addAttr(self.custom_ctrl , longName = 'geometryDisplayType' , attributeType = 'enum' ,
			             enumName = 'Normal:Template:Reference' ,
			             keyable = True)
		
		# 连接各个组的显示属性
		custom_ctrl_attrs = ['.geometryVis' , '.controlsVis' , '.rigNodesVis' , '.jointsVis']
		hierarchy_grp = [self.geometry , self.control , self.rigNode , self.joint]
		for attrs , grp in zip(custom_ctrl_attrs , hierarchy_grp) :
			cmds.connectAttr(self.custom_ctrl + '{}'.format(attrs) , '{}.visibility'.format(grp))
		# 连接模型的可编辑属性
		cmds.setAttr(self.geometry + '.overrideDisplayType' , 2)
		cmds.connectAttr('{}.geometryDisplayType'.format(self.custom_ctrl) , self.geometry + '.overrideEnabled' ,
		                 force = True)
		
		# 显示和隐藏属性
		for attr in attrs_list :
			cmds.setAttr(self.custom_ctrl + attr , lock = True , keyable = False , channelBox = False)
		
		# 创建用于空间切换的组
		for ctrl in self.rig_ctrl :
			ctrl_obj = nameUtils.Name(name = ctrl)
			space_grp = cmds.createNode('transform' , name = 'grp_m_{}Space_001'.format(ctrl_obj.description))
			cmds.parent(space_grp , ctrl)
			cmds.setAttr(space_grp + '.visibility' , 0)
