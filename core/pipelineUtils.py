# coding=utf-8
u"""
这是一个用来编写流程工具的类

目前已有的功能：

clear_keys: 清除场景内所有的关键帧
add_face_tag : 将“isFace”标记添加到所选物体的属性上
remove_non_face_objs：移除没有带“isFace”标志的物体
copy_weight：复制蒙皮
rename_bs_sc：批量重命名对象的蒙皮和混合变形节点
distence_between：获取两个对象之间的距离.
reset_control：重置控制器上所有的数值.
list_operation：将两个列表的并集/差分/交集/对称_差分部分作为列表返回.
tag_joint：对选择的关节添加关节标签
batch_Constraints：选中多个物体，批量对物体进行约束
default_grp： 添加绑定的初始层级组，并隐藏连接对应的属性
create_constraints：快速创建约束	用法：先选择需要约束的物体，在选择被约束的物体
delete_constraints：删除所选择物体的所有约束节点
select_sub_objects：快速选择所选物体的所有子物体
finger_Connect：  adv重新生成后手指的驱动可能会消失，于是可以依靠这个代码重新连接
create_node：根据给定的节点类型，在给定的位置生成新的节点。
get_maya_main_window()：获取maya的主窗口
save_file_as：另存为文件
get_current_scene_path ： 获取当前文件的绝对路径
create_reference：在maya里的当前文件创建引用
create_native_script_job:创建回调函数在新场景打开的时候执行回调函数
fbxExport:所选择的物体导出成为fbx文件

"""
import math
import os
import re
from functools import partial
from functools import wraps
from importlib import reload

# noinspection PyUnresolvedReferences
from maya import OpenMaya as om
from maya import OpenMayaUI as omui
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
from PySide2 import QtWidgets
from maya import mel
from pymel.util import path
from shiboken2 import wrapInstance

from . import controlUtils
from . import hierarchyUtils
from . import qtUtils



class Pipeline(object) :
	
	
	
	def __init__(self) :
		pass
	
	
	
	@staticmethod
	def clear_keys() :
		u"""
		清除场景内所有的动画关键帧
		:return:
		"""
		animCurves = cmds.ls(type = ['animCurveTA' , 'animCurveTL' , 'animCurveTU'])
		if animCurves :
			cmds.delete(animCurves)
			cmds.warning(u"已清除场景内所有的动画关键帧")
		else :
			cmds.warning(u"场景内没有动画关键帧")
	
	
	
	@staticmethod
	def add_face_tag() :
		u"""将“isFace”标记添加到所选物体的属性上.

		"""
		
		sel_to_tag_list = cmds.ls(sl = True)
		
		for sel in sel_to_tag_list :
			if not cmds.objExists('{}.isFace'.format(sel)) :
				cmds.addAttr(sel , ln = 'isFace' , at = 'bool' , dv = 1)
				cmds.setAttr('{}.isFace'.format(sel) , keyable = False , channelBox = False)
	
	
	
	@staticmethod
	def remove_non_face_objs() :
		u"""“移除没有带face标志的物体.

		"""
		
		assemblies = cmds.ls(assemblies = True)
		
		for assembly in assemblies :
			children = cmds.listRelatives(assembly , allDescendents = True , type = 'transform')
			if children :
				for child in children :
					if not cmds.objExists('{}.isFace'.format(child)) or not cmds.getAttr('{}.isFace'.format(child)) :
						cmds.delete(child)
	
	
	
	@staticmethod
	def copy_weight() :
		u'''

		Returns:复制蒙皮

		'''
		# 获取选择
		sel = cmds.ls(selection = True)
		
		source_mesh = sel[0]
		target_meshes = sel[1 :]
		
		# 查询目标对象是否具有蒙皮信息
		for target_mesh in target_meshes :
			target_skin = mel.eval('findRelatedSkinCluster("' + target_mesh + '")')
			if target_skin :
				cmds.delete(target_skin)
		
		# 获取源对象的蒙皮信息
		source_skin = mel.eval('findRelatedSkinCluster("' + source_mesh + '")')
		
		# 获取源对象受影响的蒙皮信息
		source_joints = cmds.skinCluster(source_skin , query = True , influence = True)
		
		# 在每个目标对象中循环
		for target_mesh in target_meshes :
			# 用源关节绑定蒙皮
			target_skin = cmds.skinCluster(source_joints , target_mesh , toSelectedBones = True)[0]
			
			# 复制蒙皮权重
			cmds.copySkinWeights(sourceSkin = source_skin , destinationSkin = target_skin , noMirror = True ,
			                     surfaceAssociation = 'closestPoint' , influenceAssociation = ['label' , 'oneToOne'])
			
			# 重命名对象蒙皮
			cmds.select(sel)
			Pipeline.rename_bs_sc()
	
	
	
	@staticmethod
	def rename_bs_sc() :
		u'''
		批量重命名对象的蒙皮和混合变形节点
		'''
		geos = cmds.ls(sl = True)
		for geo in geos :
			geo_shape = cmds.listRelatives(geo , shapes = True)
			sc = cmds.listConnections(geo_shape , type = 'skinCluster')
			if sc :
				cmds.rename(sc , 'sc_{}'.format(geo))
			bs = cmds.listConnections(geo_shape , type = 'blendShape')
			if bs :
				cmds.rename(bs , 'bs_{}'.format(geo))
	
	
	
	@staticmethod
	def distence_between(node_a , node_b) :
		u'''获取两个对象之间的距离.
		node_a(str): 对象a.
		node_b(str): 对象b.

		:return
		dist(float):两个对象之间的距离.
		'''
		point_a = cmds.xform(node_a , query = True , worldSpace = True , rotatePivot = True)
		point_b = cmds.xform(node_b , query = True , worldSpace = True , rotatePivot = True)
		dist = math.sqrt(sum([pow((b - a) , 2) for b , a in zip(point_a , point_b)]))
		return dist
	
	
	
	@staticmethod
	def reset_control() :
		u"""重置控制器上所有的数值.



		 """
		ctrl_node = cmds.ls('ctrl_?_*_???')
		attrs = ['translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ']
		scale_attrs = ['scaleX' , 'scaleY' , 'scaleZ']
		for ctrl in ctrl_node :
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
		ctrl_IKFKblend = cmds.ls('ctrl_?_*IKFKBend_???')
		for IKFKblend in ctrl_IKFKblend :
			cmds.setAttr(IKFKblend + '.IkFkBend' , 1)
	
	
	
	@staticmethod
	def list_operation(list_a , list_b , operation = '|') :
		u"""将两个列表的并集/差分/交集/对称_差分部分作为列表返回.

		Args:
			list_a (list/None): 第一个列表.
			list_b (list/None): 第二个列表.
			operation (str): 运算符号为 '|', '&', '-', '^'.

		Returns:
			list: 作为列表的两个列表的并集/差分/交集/对称_差分部分.

		"""
		
		# 如果无，则将无转换为[]空列表，仅用于操作
		if not list_a :
			list_a = []
		if not list_b :
			list_b = []
		
		set_a = set(list_a)
		set_b = set(list_b)
		
		if operation == '|' :
			return list(set_a.union(set_b))
		elif operation == '&' :
			return list(set_a.intersection(set_b))
		elif operation == '-' :
			return list(set_a.difference(set_b))
		elif operation == '^' :
			return list(set_a.symmetric_difference(set_b))
	
	
	
	@staticmethod
	def tag_joint() :
		"""
		tag joint base on its name

		Args:
			jnt (str): joint name
		"""
		jnts = cmds.ls(type = 'joint')
		for jnt in jnts :
			name_parts = jnt.split('_')
			
			if name_parts[1] == 'l' :
				side_index = 1
			elif name_parts[1] == 'r' :
				side_index = 2
			else :
				side_index = 0
			
			cmds.setAttr(jnt + '.side' , side_index)
			cmds.setAttr(jnt + '.type' , 18)
			cmds.setAttr(jnt + '.otherType' , name_parts[2] + name_parts[3] , type = 'string')
	
	
	
	@staticmethod
	def batch_Constraints() :
		u"""
		选择物体，批量制作约束
		"""
		geos = cmds.ls(sl = True)
		for geo in geos :
			cmds.undoInfo(openChunk = True)  # 批量撤销的开头
			ctrl = controlUtils.Control(n = 'ctrl_' + geo , s = 'cube' , r = 1)
			ctrl_transform = '{}'.format(ctrl.transform)
			sub_ctrl = controlUtils.Control(n = 'ctrlSub_' + geo , s = 'cube' , r = 1 * 0.7)
			sub_ctrl.set_parent(ctrl.transform)
			sub_ctrl_transform = '{}'.format(sub_ctrl.transform)
			# 添加上层层级组
			offset_grp = hierarchyUtils.Hierarchy.add_extra_group(
					obj = ctrl_transform , grp_name = '{}'.format(ctrl_transform.replace('ctrl' , 'offset')) ,
					world_orient = False)
			connect_grp = hierarchyUtils.Hierarchy.add_extra_group(
					obj = offset_grp , grp_name = offset_grp.replace('offset' , 'connect') , world_orient = False)
			driven_grp = hierarchyUtils.Hierarchy.add_extra_group(
					obj = connect_grp , grp_name = connect_grp.replace('connect' , 'driven') , world_orient = False)
			zero_grp = hierarchyUtils.Hierarchy.add_extra_group(
					obj = driven_grp , grp_name = driven_grp.replace('driven' , 'zero') , world_orient = False)
			
			# 创建output层级组
			output = cmds.createNode('transform' , name = ctrl_transform.replace('ctrl_' , 'output_') ,
			                         parent = ctrl_transform)
			
			# 连接次级控制器的属性
			cmds.connectAttr(sub_ctrl.transform + '.translate' , output + '.translate')
			cmds.connectAttr(sub_ctrl.transform + '.rotate' , output + '.rotate')
			cmds.connectAttr(sub_ctrl.transform + '.scale' , output + '.scale')
			cmds.connectAttr(sub_ctrl.transform + '.rotateOrder' , output + '.rotateOrder')
			cmds.addAttr(ctrl_transform , attributeType = 'bool' , longName = 'subCtrlVis' ,
			             niceName = U'次级控制器显示' ,
			             keyable = True)
			cmds.connectAttr(ctrl_transform + '.subCtrlVis' , sub_ctrl_transform + '.visibility')
			
			cmds.matchTransform(zero_grp , geo)
			cmds.parentConstraint(sub_ctrl_transform , geo , mo = True)
			cmds.scaleConstraint(sub_ctrl_transform , geo , mo = True)
			cmds.undoInfo(openChunk = False)  # 批量撤销的开头
	
	
	
	@staticmethod
	def default_grp() :
		u'''
		添加绑定的初始层级组，并隐藏连接对应的属性
		'''
		# 创建顶层的Group组
		Group = cmds.createNode('transform' , name = 'Group')
		
		# 创建Group层级下的子层级组，并做层级关系
		Geometry = cmds.createNode('transform' , name = 'Geometry')
		Control = cmds.createNode('transform' , name = 'Control')
		Custom = cmds.createNode('transform' , name = 'Custom')
		cmds.parent(Geometry , Custom , Control , Group)
		
		# 创建RigNode层级下的子层级组并做层级关系
		RigNodes = cmds.createNode('transform' , name = 'RigNodes')
		Joints = cmds.createNode('transform' , name = 'Joints')
		RigNodes_Local = cmds.createNode('transform' , name = 'RigNodesLocal')
		RigNodes_World = cmds.createNode('transform' , name = 'RigNodesWorld')
		nCloth_geo_grp = cmds.createNode('transform' , name = 'nCloth_geo_grp')
		cmds.parent(RigNodes_Local , RigNodes_World , RigNodes)
		cmds.parent(RigNodes , Joints , nCloth_geo_grp , Custom)
		
		# 创建Modle层级下的子层级组并且做层级关系
		Low_modle_grp = cmds.createNode('transform' , name = 'grp_m_low_Modle_001')
		Mid_modle_grp = cmds.createNode('transform' , name = 'grp_m_mid_Modle_001')
		High_modle_grp = cmds.createNode('transform' , name = 'grp_m_high_Modle_001')
		cmds.parent(Low_modle_grp , Mid_modle_grp , High_modle_grp , Geometry)
		
		World_zero = [Group , Geometry , RigNodes_Local , RigNodes_World , RigNodes , Control , Joints , Custom]
		attrs_list = ['.translateX' , '.translateY' , '.translateZ' , '.rotateX' , '.rotateY' , '.rotateZ' ,
		              '.scaleX' ,
		              '.scaleY' ,
		              '.scaleZ' , '.visibility' , '.rotateOrder' , '.subCtrlVis']
		rig_top_grp = 'Group'
		if not cmds.objExists(rig_top_grp) :
			selections = cmds.ls(sl = True)
			if selections :
				rig_top_grp = selections[0]
		
		# 创建总控制器Character
		character_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_Character_001' , shape = 'circle' , radius = 10 ,
		                                                      axis = 'X+' ,
		                                                      pos = None ,
		                                                      parent = Control)
		
		# 创建世界控制器
		world_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_world_001' , shape = 'local' , radius = 8 ,
		                                                  axis = 'Z-' ,
		                                                  pos = None ,
		                                                  parent = 'ctrl_m_Character_001')
		
		cog_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_cog_001' , shape = 'circle' , radius = 3 ,
		                                                axis = 'X+' ,
		                                                pos = None ,
		                                                parent = 'output_m_world_001')
		
		# 创建一个自定义的控制器，用来承载自定义的属性
		lock_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_custom_001' , shape = 'cross' , radius = 3 ,
		                                                 axis = 'X+' ,
		                                                 pos = None ,
		                                                 parent = Custom)
		lock_ctrl = 'ctrl_m_custom_001'
		cmds.parentConstraint('ctrl_m_Character_001' , lock_ctrl , mo = True)
		cmds.scaleConstraint('ctrl_m_Character_001' , lock_ctrl , mo = True)
		
		# 创建自定义的控制器属性
		for attr in ['GeometryVis' , 'ControlsVis' , 'RigNodesVis' , 'JointsVis'] :
			if not cmds.objExists('{}.{}'.format(lock_ctrl , attr)) :
				cmds.addAttr(lock_ctrl , ln = attr , at = 'bool' , dv = 1 , keyable = True)
		
		# 添加精度切换的属性
		if not cmds.objExists('{}.Resolution'.format(lock_ctrl)) :
			cmds.addAttr(lock_ctrl , ln = 'Resolution' , at = 'enum' , en = 'low:mid:high' , keyable = True)
			for idx , res in {0 : 'low' , 1 : 'mid' , 2 : 'high'}.items() :
				cnd_node = 'resolution_{}_conditionNode'.format(res)
				if not cmds.objExists(cnd_node) :
					cnd_node = cmds.createNode('condition' , n = cnd_node)
				cmds.connectAttr('{}.Resolution'.format(lock_ctrl) , '{}.firstTerm'.format(cnd_node) , f = True)
				cmds.setAttr('{}.secondTerm'.format(cnd_node) , idx)
				cmds.setAttr('{}.colorIfTrueR'.format(cnd_node) , 1)
				cmds.setAttr('{}.colorIfFalseR'.format(cnd_node) , 0)
				cmds.connectAttr('{}.outColorR'.format(cnd_node) , 'grp_m_{}_Modle_001.visibility'.format(res) ,
				                 f = True)
		
		# 添加模型显示方式的属性
		if not cmds.objExists('{}.GeometryDisplayType'.format(lock_ctrl)) :
			cmds.addAttr(lock_ctrl , ln = 'GeometryDisplayType' , at = 'enum' , en = 'Normal:Template:Reference' ,
			             keyable = True)
		
		# 连接 GeometryVis
		cmds.connectAttr('{}.GeometryVis'.format(lock_ctrl) , '{}.visibility'.format(Geometry) , f = True)
		
		# 连接 controlsVis
		cmds.connectAttr('{}.ControlsVis'.format(lock_ctrl) , '{}.visibility'.format(Control) , f = True)
		
		# 连接 RigNodesVis
		cmds.connectAttr('{}.RigNodesVis'.format(lock_ctrl) , '{}.visibility'.format(RigNodes) , f = True)
		
		# 连接 jointsVis
		cmds.connectAttr('{}.JointsVis'.format(lock_ctrl) , '{}.visibility'.format(Joints) , f = True)
		
		# 连接模型的可编辑属性
		cmds.setAttr(Geometry + '.overrideDisplayType' , 2)
		cmds.connectAttr('{}.GeometryDisplayType'.format(lock_ctrl) , Geometry + '.overrideEnabled' , f = True)
		
		# 显示和隐藏属性
		for attr in attrs_list :
			cmds.setAttr(lock_ctrl + attr , l = True , k = False , cb = False)
		
		return {
				'Geometry' : Geometry ,
				'Control' : Control ,
				'RigNodes' : RigNodes ,
				'Joints' : Joints ,
				'RigNodes_Local' : RigNodes_Local ,
				'RigNodes_World' : RigNodes_World ,
				'nCloth_geo_grp' : nCloth_geo_grp
				}
	
	
	
	@staticmethod
	def create_constraints() :
		u"""
		快速创建约束.
		用法：先选择需要约束的物体，在选择被约束的物体
		"""
		sel = cmds.ls(sl = True)
		driver_obj = sel[-1]
		driven_obj = sel[0 :-1]
		cmds.pointConstraint(driver_obj , driven_obj , mo = True)
		cmds.orientConstraint(driver_obj , driven_obj , mo = True)
		cmds.scaleConstraint(driver_obj , driven_obj , mo = True)
	
	
	
	@staticmethod
	def delete_constraints() :
		u'''
		快速删除选择物体的约束节点
		'''
		sel = cmds.ls(sl = True)
		for obj in sel :
			const = cmds.listConnections(obj , type = 'constraint')
			if const :
				cmds.delete(const)
	
	
	
	@staticmethod
	def select_sub_objects() :
		u'''
		快速选择所选择物体的所有子对象
		'''
		selection = cmds.ls(sl = True)  # 获取选择的所有对象
		for obj in selection :
			cmds.select(cmds.listRelatives(obj , allDescendents = True , type = 'transform') , add = True)
	
	
	
	@staticmethod
	def make_undo(func) :
		u'''
		一键撤销的解释器
		'''
		
		
		
		@wraps(func)
		def wrap(*args , **kwargs) :
			cmds.undoInfo(openChunk = True)
			result = func(*args , **kwargs)
			cmds.undoInfo(closeChunk = True)
			return result
		
		
		
		return wrap
	
	
	
	@staticmethod
	def finger_Connect() :
		'''
		adv重新生成后手指的驱动可能会消失，于是可以依靠这个代码重新连接
		选择所有需要驱动的手指控制器加选Finger控制器创建连接
		'''
		
		
		
		# 选择所有需要驱动的手指控制器加选Finger控制器创建连接
		def myDrv(sdk , ctrl , str) :
			cmds.setAttr(ctrl + str , -2)
			cmds.setAttr(sdk + '.ry' , -18)
			cmds.setDrivenKeyframe(sdk + '.ry' , cd = ctrl + str , ott = 'linear')
			cmds.setAttr(ctrl + str , 10)
			cmds.setAttr(sdk + '.ry' , 90)
			cmds.setDrivenKeyframe(sdk + '.ry' , cd = ctrl + str , itt = 'linear')
			cmds.setAttr(ctrl + str , 0)
			cmds.setAttr(sdk + '.ry' , 0)
			cmds.setDrivenKeyframe(sdk + '.ry' , cd = ctrl + str)
		
		
		
		ctrl = cmds.ls(sl = True)
		myStr = ['.indexCurl' , '.middleCurl' , '.ringCurl' , '.pinkyCurl' , '.thumbCurl']
		for i in ctrl[0 :-1] :
			Extra = re.sub('FK' , 'FKExtra' , i)
			Grp = cmds.listRelatives(Extra , p = True)[0]
			SDK1 = cmds.group(em = True , p = Grp , n = 'SDK1' + i)
			cmds.parent(Extra , SDK1)
			if 'Index' in i :
				myDrv(SDK1 , ctrl[-1] , myStr[0])
			if 'Middle' in i :
				myDrv(SDK1 , ctrl[-1] , myStr[1])
			if 'Ring' in i :
				myDrv(SDK1 , ctrl[-1] , myStr[2])
			if 'Pinky' in i :
				myDrv(SDK1 , ctrl[-1] , myStr[3])
			if 'Thumb' in i :
				myDrv(SDK1 , ctrl[-1] , myStr[4])
			if 'Cup' in i :
				cmds.setAttr(ctrl[-1] + '.cup' , 0)
				cmds.setAttr(SDK1 + '.rx' , 0)
				cmds.setDrivenKeyframe(SDK1 + '.rx' , cd = ctrl[-1] + '.cup' , ott = 'linear')
				cmds.setAttr(ctrl[-1] + '.cup' , 10)
				cmds.setAttr(SDK1 + '.rx' , 65)
				cmds.setDrivenKeyframe(SDK1 + '.rx' , cd = ctrl[-1] + '.cup' , itt = 'linear')
		
		
		
		def myDrv(sdk , min , max , ctrl) :
			cmds.setAttr(ctrl + '.spread' , -5)
			cmds.setAttr(sdk + '.rz' , min)
			cmds.setDrivenKeyframe(sdk + '.rz' , cd = ctrl + '.spread' , ott = 'linear')
			cmds.setAttr(ctrl + '.spread' , 10)
			cmds.setAttr(sdk + '.rz' , max)
			cmds.setDrivenKeyframe(sdk + '.rz' , cd = ctrl + '.spread' , itt = 'linear')
			cmds.setAttr(ctrl + '.spread' , 0)
			cmds.setAttr(sdk + '.rz' , 0)
			cmds.setDrivenKeyframe(sdk + '.rz' , cd = ctrl + '.spread')
		
		
		
		for i in ctrl[0 :-1] :
			Grp = cmds.listRelatives('SDK1' + i , p = True)[0]
			SDK2 = cmds.group(em = True , p = Grp , n = 'SDK2' + i)
			
			cmds.parent('SDK1' + i , SDK2)
			if 'PinkyFinger1' in i :
				myDrv(SDK2 , 30 , -60 , ctrl[-1])
			if 'RingFinger1' in i :
				myDrv(SDK2 , 15 , -30 , ctrl[-1])
			if 'IndexFinger1' in i :
				myDrv(SDK2 , -20 , 40 , ctrl[-1])
	
	
	
	@staticmethod
	def create_node(node_type , node_name , match = False , match_node = None) :
		u'''
		根据给定的节点类型，在给定的位置生成新的节点。
		node_type；创建的新的节点类型
		node_name:创建的新的节点名称
		match:是否吸附对应的位置
		match_node:吸附对应的位置
		'''
		new_node = cmds.createNode(node_type , name = node_name)
		if match :
			cmds.matchTransform(new_node , match_node , position = True , rotation = True , scale = True)
		
		return new_node
	
	
	
	@staticmethod
	def get_maya_main_window() :
		u'''
		获取maya的主窗口
		:return:
		'''
		# c++的指针概念，获取maya的窗口对象
		pointer = omui.MQtUtil.mainWindow()
		return wrapInstance(int(pointer) , QtWidgets.QWidget)
	
	
	
	@staticmethod
	def save_file_as(current_selected_file) :
		u'''
		保存给定的文件的名称
		:param current_opend_file: 当前打开的文件
		:param current_selected_file: 选择保存的文件
		:return:
		'''
		# 根据所选择的文件获取源文件的名称，并打开重命名名称的窗口
		old_name = os.path.basename(current_selected_file)
		new_name = qtutils.input_dialog_text(u'重命名_{}'.format(old_name) , u'重命名为新的名称' , (500 , 200))
		new_name = '.'.join([new_name , 'ma'])
		if new_name is None :
			return
		
		if os.path.isfile(current_selected_file) :
			parent_path = os.path.dirname(current_selected_file)
		else :
			parent_path = current_selected_file
		
		new_path = QtUtils.path_joiner(parent_path , new_name)
		if os.path.exists(new_path) :
			print('{} already exists .Request ignored.'.format(new_path))
			return
		
		pm.saveAs(new_path)
	
	
	
	@staticmethod
	def get_current_scene_path() :
		u'''
		获取当前文件的绝对路径
		:return:
		'''
		return str(pm.sceneName().abspath()).replace('\\' , '/')
	
	
	
	@staticmethod
	def get_group_name(name_space) :
		u'''
		根据给定的name_space来设定组的名称
		:param name_space:
		:return:
		'''
		return 'REF_{}'.format(name_space)
	
	
	
	@staticmethod
	def create_reference(file_path , name_space = None) :
		u'''
		在maya里的当前文件创建引用
		:param file_path: 需要引用的文件路径
		:param name_space: 引用文件的名称空间
		:return:
		'''
		if name_space is None :
			name_space = os.path.basename(file_path).split('.')[0].upper()
		try :
			pm.Namespace(name_space).remove()
		except :
			pass
		# 设定引用的文件的组名，对应的引用文件放在这个组下
		grp_name = get_group_name(name_space)
		
		# 引用文件设置
		ref_node = pm.createReference(file_path ,
		                              namespace = name_space ,
		                              loadReferenceDepth = 'all' ,
		                              groupReference = True ,
		                              groupName = grp_name)
		
		return ref_node , pm.Namespace(name_space) , grp_name
	
	
	
	@staticmethod
	def create_native_script_job(event_name , callback) :
		#############################################################
		# 创建回调函数在新场景打开的时候执行回调函数
		#############################################################
		scene_open_callback_id = om.MEventMessage.addEventCallback(
				event_name , callback)
		# 创建回调函数被销毁的机制，防止重复调用
		return partial(om.MEventMessage.removeCallback , scene_open_callback_id)
	
	
	
	@staticmethod
	def fbxExport(des_path) :
		u"""
		所选择的物体导出成为fbx文件
		:type des_path: str
		:return:
		"""
		path_string = des_path.replace('\\' , '/')
		try :
			path(des_path).parent.makedirs_p()
			mel.eval(f'FBXExport -f "{path_string}" -s')
			print(f'Export succeeded. {pm.selected()} -> {path_string}')
		except Exception as e :
			print('Export failed. ' + path_string)
			print(e)
	
	
	
	@staticmethod
	def create_constraint(driver , driven , point_value = True , orient_value = True , scale_value = True , mo_value = True) :
		'''
		创建约束对象
		driver:约束者
		driven:被约束者
		'''
		if point_value :
			cmds.pointConstraint(driver , driven , mo = mo_value)
		if orient_value :
			cmds.orientConstraint(driver , driven , mo = mo_value)
		if scale_value :
			cmds.scaleConstraint(driver , driven , mo = mo_value)
	
	
	
	@staticmethod
	def move(obj , pos) :
		"""
		位移物体到指定的位置

		:param obj: str. maya的对象
		:param pos: list. 位置信息 x, y and z
		"""
		return cmds.move(pos[0] , pos[1] , pos[2] , obj , r = 1)
	
	
	
	@staticmethod
	def get_percentages(sample_count) :
		"""
		曲线的总长度为1，给定需要平分的点数量，返回每个点的位置信息
		例子：get_percentages(5) == [0.0, 0.25, 0.5, 0.75, 1.0]
		:param sample_count: int. 需要平分的点数量
		:return: list. 返回每个点的位置信息
		"""
		if sample_count <= 1 :
			return
		
		outputs = list()
		gap = 1.00 / (sample_count - 1)
		for index in range(sample_count) :
			outputs.append(index * gap)
		
		return outputs
	
	
	
	@staticmethod
	def get_point_on_curve(curve , sample_count) :
		"""
		获取具有均匀距离的nurbs曲线上的点信息
		https://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__cpp_ref_class_m_fn_nurbs_curve_html

		:param curve: str. nurbs曲线的名称
		:param sample_count: int. 采样点的数量
		:return: tuple. om.MPoint object and om.MVector object
		"""
		plists = Pipeline.get_percentages(sample_count)
		
		points = list()
		tangents = list()
		crv_fn = om.MFnNurbsCurve(transform.get_dag_path(curve))
		for percentage in plists :
			parameter = crv_fn.findParamFromLength(crv_fn.length() * percentage)
			point = om.MPoint()
			crv_fn.getPointAtParam(parameter , point)
			tangent = crv_fn.tangent(parameter)
			
			points.append(point)
			tangents.append(tangent)
		
		return points , tangents
	
	
	
	@staticmethod
	def create_joints_on_curve(curve , sample_count) :
		"""
		创建均匀分布在曲线上的关节点

		:param curve: str. 曲线的节点名称
		:param sample_count: int. 采样点的数量
		:return: list. 返回创建关节的列表
		"""
		
		jnt_list = list()
		#获取具有均匀距离的nurbs曲线上的点信息
		points , tangents = util.get_point_on_curve(curve , sample_count)
		for index in range(len(points)) :
			point = points[index]
			tangent = tangents[index]
			#在对应的点上创建关节，并且创建个transform组来做目标约束吸附旋转
			jnt = cmds.createNode('joint')
			jnt_list.append(jnt)
			temp_node = cmds.createNode('transform')
			
			cmds.xform(
					temp_node ,
					t = [point.x + tangent.x , point.y + tangent.y , point.z + tangent.z]
					)
			cmds.xform(jnt , t = [point.x , point.y , point.z])
			constraint = cmds.aimConstraint(temp_node , jnt)[0]
			cmds.delete([temp_node , constraint])
		
		return jnt_list