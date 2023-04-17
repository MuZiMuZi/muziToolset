# coding=utf-8
from importlib import reload

from . import matehuman_base_rig

import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.core.snapUtils as snapUtils
import muziToolset.core.matehumanUtils as matehumanUtils


reload(controlUtils)
reload(pipelineUtils)
reload(jointUtils)



class FK_Rig(matehuman_base_rig.Base_Rig) :
	u"""
	这是一个用来编写FK控制系统绑定的类，之后的绑定都会在这个类的基础上逐级继承下去

	继承了base_rig

	目前已有的功能：

	fk_chain_rig：创建FK链的控制器绑定



	"""
	
	
	def __init__(self , drv_jnts , joint_parent , control_parent, redius = 10) :
		super(FK_Rig , self).__init__()
		self.drv_jnts = drv_jnts
		self.joint_parent = joint_parent
		self.control_parent = control_parent
		self.redius = redius
	
	
	def create_fk_chain(self, constraint = False) :
		# 根据self.drv_jnts生成fk关节链
		self.fk_chain = jointUtils.Joint.create_mateHuman_chain(self.drv_jnts , 'fkjnt_' , self.joint_parent,constraint )
		
		return self.fk_chain
	
	def fk_chain_rig(self) :
		u"""
		创建fk链的控制器绑定
		Args:
			self.drv_jnts:mateHuman的self.drv_jnts用于放置模板的关节列表。
			self.control_parent(str): 控制器组的父层级
			self.redius: 控制器的大小

		Returns: fk_ctrl_grp ：fk控制器的最顶层

		"""
		# 创建控制器
		parent = None
		for jnt in self.drv_jnts :
			fk_ctrl = controlUtils.Control.create_mateHuman_ctrl(jnt , 'fkctrl' , shape = 'circle' , radius = self.redius ,
			                                                     axis = 'Y+' ,
			                                                     pos = jnt ,
			                                                     parent = None)
			zero = fk_ctrl.replace('ctrl' , 'zero')
			output = fk_ctrl.replace('ctrl' , 'output')
			cmds.parentConstraint(output , 'fkjnt_' + jnt , maintainOffset = True)
			cmds.scaleConstraint(output , 'fkjnt_' + jnt , maintainOffset = True)
			if parent :
				cmds.parent(zero , parent)
			parent = output
		# 创建fk控制器的总组，整理fk控制器的层级结构
		fk_ctrl_grp = cmds.createNode('transform' , name = 'fkgrp_' + self.drv_jnts[0])
		fk_chain_zero = 'fkzero_' + self.drv_jnts[0]
		cmds.parent(fk_chain_zero , fk_ctrl_grp)
		if self.control_parent :
			hierarchyUtils.Hierarchy.parent(child_node = fk_ctrl_grp , parent_node = self.control_parent)

	def _create_fk_chain_system(self, constraint = False):
		u'''
		创建fk链条绑定系统
		:return:
		'''
		self.fk_systeam_chain = self.create_fk_chain(constraint)
		self.fk_systeam_rig = self.fk_chain_rig()
		

class IK_Rig(matehuman_base_rig.Base_Rig) :
	
	
	def __init__(self , drv_jnts , joint_parent , control_parent , space_list , stretch = True) :
		super(IK_Rig , self).__init__()
		self.drv_jnts = drv_jnts
		self.joint_parent = joint_parent
		self.control_parent = control_parent
		self.space_list = space_list
		self.stretch = stretch
	
	
	def create_ik_chain(self,constraint = False) :
		# 根据self.drv_jnts生成ik关节链
		self.ik_chain = jointUtils.Joint.create_mateHuman_chain(self.drv_jnts , 'ikjnt_' , self.joint_parent ,
		                                                        constraint = False)
		
		return self.ik_chain
	
	
	def ik_chain_rig(self,Y_value = 1) :
		u"""
		创建IK链的控制器绑定
		Args:
			Y_value : 手臂的极向量控制器在后面为1，腿的极向量控制器在前面为-1
			self.drv_jnts(list): mateHuman的drv关节链
			self.control_parent(str): 控制器组的父层级
			space_list(list): 空间切换的空间
			stretch(bool):是否需要拉伸效果

		Returns:

		"""
		# 创建开始的IK控制器
		startIK_jnt = self.ik_chain[0]
		startIK_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.drv_jnts[0] , 'ikctrl' , shape = 'Cube' ,
		                                                          radius = 13 ,
		                                                          axis = 'Y+' ,
		                                                          pos = self.drv_jnts[0] , parent = None)
		
		startIK_ctrl_output = startIK_ctrl.replace('ctrl' , 'output')
		startIK_zero = startIK_ctrl.replace('ctrl' , 'zero')
		# cmds.pointConstraint(startIK_ctrl_output , startIK_jnt , maintainOffset = True)
		
		# 创建尾端的ik控制器
		endIK_jnt = self.ik_chain[2]
		endIK_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.drv_jnts[2] , 'ikctrl' , shape = 'Cube' ,
		                                                        radius = 13 ,
		                                                        axis = 'Y+' ,
		                                                        pos = self.drv_jnts[2] , parent = None)
		endIK_ctrl_output = endIK_ctrl.replace('ctrl' , 'output')
		endIK_zero = endIK_ctrl.replace('ctrl' , 'zero')
		
		endIK_local_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.drv_jnts[2] , 'ikctrlLocal' ,
		                                                              shape = 'local' ,
		                                                              radius = 10 ,
		                                                              axis = 'X-' ,
		                                                              pos = self.drv_jnts[2] , parent = None)
		endIK_local_zero = endIK_local_ctrl.replace('ctrl' , 'zero')
		cmds.parent(endIK_local_zero , endIK_ctrl_output)
		#
		# 创建ik的极向量控制器
		midIK_jnt = self.ik_chain[1]
		midIK_pv_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.drv_jnts[1] , 'ikctrlPv' , shape = 'Cube' ,
		                                                           radius = 8 ,
		                                                           axis = 'Y+' , pos = self.drv_jnts[1] , parent = None)
		midIK_pv_zero = midIK_pv_ctrl.replace('ctrl' , 'zero')
		cmds.matchTransform(midIK_pv_zero , midIK_jnt , position = True , rotation = True , scale = True)
		
		# 获取midIK_jnt的边
		midIK_jnt_mate = matehumanUtils.MateHuman(self.drv_jnts[1])
		if midIK_jnt_mate.side == 'r' :
			side_value = -1
		else :
			side_value = 1
		
		cmds.move(0 , 32 * side_value* Y_value , 0 , midIK_pv_zero , relative = True , objectSpace = True ,
		          worldSpaceDistance = True)
		
		# 创建ik极向量控制器的曲线指示器
		# 创建pv控制器的loc来记录位置
		midIK_pv_loc = cmds.spaceLocator(name = midIK_jnt.replace('jnt' , 'locPv'))[0]
		cmds.matchTransform(midIK_pv_loc , midIK_pv_zero , position = True , rotation = True , scale = True)
		cmds.parent(midIK_pv_loc , midIK_pv_ctrl)
		cmds.setAttr(midIK_pv_loc + '.visibility' , 0)
		# 创建pvjnt的loc来记录位置
		midIK_jnt_loc = cmds.spaceLocator(name = midIK_pv_loc.replace('locPv' , 'locJnt'))[0]
		cmds.matchTransform(midIK_jnt_loc , midIK_jnt , position = True , rotation = True , scale = True)
		cmds.parent(midIK_jnt_loc , midIK_jnt)
		cmds.setAttr(midIK_jnt_loc + '.visibility' , 0)
		
		# 连接loc和曲线来表示位置
		ikpv_curve = cmds.curve(degree = 1 , point = [(0.0 , 0.0 , 0.0) , (0.0 , 0.0 , 0.0)] ,
		                        name = midIK_pv_ctrl.replace('ctrl' , 'crv'))
		midIK_jnt_loc_shape = cmds.listRelatives(midIK_jnt_loc , shapes = True)[0]
		midIK_pv_loc_shape = cmds.listRelatives(midIK_pv_loc , shapes = True)[0]
		ikpv_curve_shape = cmds.listRelatives(ikpv_curve , shapes = True)[0]
		
		cmds.connectAttr(midIK_jnt_loc_shape + '.worldPosition[0]' , ikpv_curve_shape + '.controlPoints[0]')
		cmds.connectAttr(midIK_pv_loc_shape + '.worldPosition[0]' , ikpv_curve_shape + '.controlPoints[1]')
		
		cmds.setAttr(ikpv_curve_shape + '.overrideEnabled' , 1)
		cmds.setAttr(ikpv_curve_shape + '.overrideDisplayType' , 2)
		cmds.setAttr(ikpv_curve + '.inheritsTransform' , 0)
		
		#
		# 创建IKhandle控制
		rotate_ikhandle_name = startIK_jnt.replace('jnt' , 'ikhandle')
		rotate_ikhandle_node = cmds.ikHandle(name = rotate_ikhandle_name , startJoint = self.ik_chain[0] , endEffector = self.ik_chain[2] ,
		                                     sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True)[0]
		cmds.setAttr(rotate_ikhandle_node + '.visibility' , 0)
		endIK_local_output = endIK_local_zero.replace('zero' , 'output')
		cmds.parent(rotate_ikhandle_node , endIK_local_output)
		cmds.poleVectorConstraint(midIK_pv_ctrl , rotate_ikhandle_node)
		ik_ctrl_grp = cmds.createNode('transform' , name = self.ik_chain[0].replace('jnt' , 'grp'))
		cmds.parent(startIK_zero , midIK_pv_zero , endIK_zero , ikpv_curve , ik_ctrl_grp)
		if self.control_parent :
			hierarchyUtils.Hierarchy.parent(child_node = ik_ctrl_grp , parent_node = self.control_parent)

		# 添加空间切换
		if self.space_list :
			for ctrl in [midIK_pv_ctrl , endIK_ctrl] :
				self.add_spaceSwitch(ctrl , space_list)
		else :
			pass

		# 添加IK链的拉伸功能
		# 创建起始端关节控制器的定位loctor
		if self.stretch :
			startIK_pos_loc = cmds.spaceLocator(name = startIK_ctrl.replace('ctrl' , 'loc'))[0]
			startIK_pos_loc_shape = cmds.listRelatives(startIK_pos_loc , shapes = True)[0]
			cmds.matchTransform(startIK_pos_loc , startIK_ctrl)
			hierarchyUtils.Hierarchy.parent(child_node = startIK_pos_loc , parent_node = startIK_ctrl)

			# 创建末端关节控制器的定位loctor
			endIK_pos_loc = cmds.spaceLocator(name = endIK_ctrl.replace('ctrl' , 'loc'))[0]
			endIK_pos_loc_shape = cmds.listRelatives(endIK_pos_loc , shapes = True)[0]
			cmds.matchTransform(endIK_pos_loc , endIK_ctrl)
			hierarchyUtils.Hierarchy.parent(child_node = endIK_pos_loc , parent_node = endIK_ctrl)

			# 创建计算距离的distween节点，来计算首端关节到中端控制器的距离
			disBtw_node = cmds.createNode('distanceBetween' , name = endIK_pos_loc.replace('loc' , 'disBtw'))
			cmds.connectAttr(startIK_pos_loc_shape + '.worldPosition' , disBtw_node + '.point1')
			cmds.connectAttr(endIK_pos_loc_shape + '.worldPosition' , disBtw_node + '.point2')

			# 计算原本关节的距离值
			midIK_jnt_value = cmds.getAttr(midIK_jnt + '.translateX')
			endIK_jnt_value = cmds.getAttr(endIK_jnt + '.translateX')
			distance_value = midIK_jnt_value * side_value + endIK_jnt_value * side_value

			# 将现有的关节距离减去原本关节的距离得到拉伸的距离
			reduce_node = cmds.createNode('addDoubleLinear' , name = startIK_jnt.replace('jnt' , 'reduce'))
			cmds.connectAttr(disBtw_node + '.distance' , reduce_node + '.input1')
			cmds.setAttr(reduce_node + '.input2' , distance_value * -1*Y_value)

			# 将变化的数值除以二，均匀分配给对应的拉伸关节
			mult_node = cmds.createNode('multDoubleLinear' , name = startIK_jnt.replace('jnt' , 'mult'))
			cmds.connectAttr(reduce_node + '.output' , mult_node + '.input1')
			cmds.setAttr(mult_node + '.input2' , 0.5 * side_value)

			# 将变化的数值连接给对应的拉伸关节
			add_midIK_jnt_node = cmds.createNode('addDoubleLinear' , name = midIK_jnt.replace('jnt' , 'add'))
			add_endIK_jnt_node = cmds.createNode('addDoubleLinear' , name = endIK_jnt.replace('jnt' , 'add'))

			cmds.connectAttr(mult_node + '.output' , add_midIK_jnt_node + '.input1')
			cmds.setAttr(add_midIK_jnt_node + '.input2' , midIK_jnt_value)

			cmds.connectAttr(mult_node + '.output' , add_endIK_jnt_node + '.input1')
			cmds.setAttr(add_endIK_jnt_node + '.input2' , endIK_jnt_value)

			# 创建一个判断节点，当变化的数值大于0时才进行拉伸
			cond_node = cmds.createNode('condition' , name = startIK_jnt.replace('jnt' , 'cond'))
			cmds.setAttr(cond_node + '.operation' , 2)
			cmds.connectAttr(reduce_node + '.output' , cond_node + '.firstTerm')
			cmds.connectAttr(add_midIK_jnt_node + '.output' , cond_node + '.colorIfTrueR')
			cmds.connectAttr(add_endIK_jnt_node + '.output' , cond_node + '.colorIfTrueG')

			cmds.setAttr(cond_node + '.colorIfFalseR' , midIK_jnt_value)
			cmds.setAttr(cond_node + '.colorIfFalseG' , endIK_jnt_value)

			# 给控制器创建一个拉伸的属性，动画师根据需要可以选择是否拉伸
			cmds.addAttr(endIK_ctrl , longName = 'stretch' , attributeType = 'double' ,
			             niceName = u'拉伸' , minValue = 0 , maxValue = 1 , defaultValue = 1 , keyable = 1)

			# 创建blendcolor节点用来承载拉伸的设置
			stretch_blend_node = cmds.createNode('blendColors' , name = endIK_ctrl.replace('ctrl' , 'blend'))
			cmds.connectAttr(endIK_ctrl + '.stretch' , stretch_blend_node + '.blender')
			# 设置blendcolor节点混合值为0的时候，也就是没有拉伸的时候，color2R 和 color2G 的值是原关节的长度
			# 因为绑定有自定义的缩放比例，因此实际的距离值需要除以绑定缩放的比例才能得到真实的距离
			stretch_divBtw_node = cmds.createNode('multiplyDivide' ,
			                                      name = stretch_blend_node.replace('blend_' , 'div_'))

			cmds.setAttr(stretch_divBtw_node + '.operation' , 2)
			cmds.setAttr(stretch_divBtw_node + '.input1X' , midIK_jnt_value)
			cmds.setAttr(stretch_divBtw_node + '.input1Y' , endIK_jnt_value)

			cmds.connectAttr(self.character_ctrl + '.rigScale' , stretch_divBtw_node + '.input2X')
			cmds.connectAttr(self.character_ctrl + '.rigScale' , stretch_divBtw_node + '.input2Y')

			# 连接拉伸后的关节长度
			cmds.connectAttr(stretch_divBtw_node + '.outputX' , stretch_blend_node + '.color2R')
			cmds.connectAttr(stretch_divBtw_node + '.outputY' , stretch_blend_node + '.color2G')
			cmds.connectAttr(cond_node + '.outColorR' , stretch_blend_node + '.color1R')
			cmds.connectAttr(cond_node + '.outColorG' , stretch_blend_node + '.color1G')

			# 给控制器创建一个极向量锁定的属性，动画师根据需要可以选择是否进行极向量锁定
			cmds.addAttr(endIK_ctrl , longName = 'PvLock' , attributeType = 'double' ,
			             niceName = u'极向量锁定' , minValue = 0 , maxValue = 1 , defaultValue = 0 , keyable = 1)

			# 创建blendcolor节点用来承载极向量锁定的设置
			pvLock_blend_node = cmds.createNode('blendColors' , name = midIK_pv_ctrl.replace('ctrl' , 'blend'))
			cmds.connectAttr(endIK_ctrl + '.PvLock' , pvLock_blend_node + '.blender')

			# 获取起始控制器，极向量控制器，末端控制器层级下用来定位位置的loc.(startIK_pos_loc,midIK_pv_loc,endIK_pos_loc)
			# 创建对应的disteween节点来获取距离
			# 计算起始控制器到极向量控制器的距离
			upper_disBtw_node = cmds.createNode('distanceBetween' ,
			                                    name = startIK_pos_loc.replace('loc' , 'disBtw_upper'))
			cmds.connectAttr(startIK_pos_loc_shape + '.worldPosition' , upper_disBtw_node + '.point1')
			cmds.connectAttr(midIK_pv_loc_shape + '.worldPosition' , upper_disBtw_node + '.point2')

			# 创建一个相乘节点来连接
			mult_upper_disBtw_node = cmds.createNode('multDoubleLinear' ,
			                                         name = upper_disBtw_node.replace('disBtw_lower' , 'mult'))
			cmds.connectAttr(upper_disBtw_node + '.distance' , mult_upper_disBtw_node + '.input1')
			cmds.setAttr(mult_upper_disBtw_node + '.input2' , side_value)

			# 计算末端控制器到极向量控制器的距离
			lower_disBtw_node = cmds.createNode('distanceBetween' ,
			                                    name = startIK_pos_loc.replace('loc' , 'disBtw_lower'))
			cmds.connectAttr(midIK_pv_loc_shape + '.worldPosition' , lower_disBtw_node + '.point1')
			cmds.connectAttr(endIK_pos_loc_shape + '.worldPosition' , lower_disBtw_node + '.point2')
			# 创建一个相乘节点来连接
			mult_lower_disBtw_node = cmds.createNode('multDoubleLinear' ,
			                                         name = lower_disBtw_node.replace('disBtw_lower' , 'mult'))
			cmds.connectAttr(upper_disBtw_node + '.distance' , mult_lower_disBtw_node + '.input1')
			cmds.setAttr(mult_lower_disBtw_node + '.input2' , side_value)

			# 因为绑定有自定义的缩放比例，因此实际的距离值需要除以绑定缩放的比例才能得到真实的距离
			div_divBtw_node = cmds.createNode('multiplyDivide' , name = midIK_pv_loc.replace('loc' , 'div'))
			cmds.connectAttr(mult_upper_disBtw_node + '.output' , div_divBtw_node + '.input1X')
			cmds.connectAttr(mult_lower_disBtw_node + '.output' , div_divBtw_node + '.input1Y')
			cmds.connectAttr(self.character_ctrl + '.rigScale' , div_divBtw_node + '.input2X')
			cmds.connectAttr(self.character_ctrl + '.rigScale' , div_divBtw_node + '.input2Y')
			cmds.setAttr(div_divBtw_node + '.operation' , 2)

			# 将真实的距离连接给极向量锁定的blendcolor节点
			# 原理：当极向量锁定值为1打开的时候，启用的是color1的数值。当极向量锁定值为0关闭的时候，启用的是color2的数值

			cmds.connectAttr(div_divBtw_node + '.outputX' , pvLock_blend_node + '.color1R')
			cmds.connectAttr(div_divBtw_node + '.outputY' , pvLock_blend_node + '.color1G')

			# 将原先关节拉伸后的距离连接给极向量锁定的blendcolor节点的color2
			cmds.connectAttr(stretch_blend_node + '.outputR' , pvLock_blend_node + '.color2R')
			cmds.connectAttr(stretch_blend_node + '.outputG' , pvLock_blend_node + '.color2G')

			# 把混合后的关节长度连接给原关节
			cmds.connectAttr(pvLock_blend_node + '.outputR' , midIK_jnt + '.translateX')
			cmds.connectAttr(pvLock_blend_node + '.outputG' , endIK_jnt + '.translateX')
		else :
			pass
	
	
	def ik_spine_rig(self) :
		u"""
		创建IKspine链的控制器绑定
		Args:
			ik_chain(list):ik关节链
			self.control_parent(str): 控制器组的父层级
			stretch(bool):ikSpine链是否需要拉伸

		Returns: ik_ctrl_grp ：IK控制器的最顶层

		"""
		
		# 根据ik_chain的关节数量生成曲线
		ik_chain_crv = cmds.curve(degree = 3 , name = self.ik_chain[0].replace('ikjnt' , 'crv') ,
		                          p = [(0 , 0 , 0) , (0 , 0 , 0) , (0 , 0 , 0) , (0 , 0 , 0) , (0 , 0 , 0)])
		
		# 获取节点的曲线形状
		curve_shape = cmds.listRelatives(ik_chain_crv , shapes = True)[0]
		
		# 获取曲线跨度和度数
		spans = cmds.getAttr(curve_shape + '.spans')
		degree = cmds.getAttr(curve_shape + '.degree')
		
		# 获取曲线的点数目
		cv_num = spans + degree
		
		# 将曲线点吸附到关节上
		for i in range(cv_num) :
			jnt = self.ik_chain[i]
			# 获取jnt位置
			jnt_pos = cmds.xform(jnt , query = True , translation = True ,
			                     worldSpace = True)
			# 获取cv位置
			cv = '{}.cv[{}]'.format(ik_chain_crv , i)
			# 设置cv点的位置
			cmds.xform(cv , translation = jnt_pos , worldSpace = True)
		cmds.setAttr(ik_chain_crv + '.visibility' , 0)
		
		# 创建开始的IK控制器
		startIK_jnt = self.ik_chain[0]
		startIK_crv_jnt = pipelineUtils.Pipeline.create_node('joint' , startIK_jnt.replace('jnt' , 'crvjnt') ,
		                                                     match = True ,
		                                                     match_node = startIK_jnt)
		startIK_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.drv_jnts[0] , 'ikctrl' , shape = 'Cube' ,
		                                                          radius = 25 , axis = 'Y+' ,
		                                                          pos = startIK_jnt , parent = None)
		startIK_ctrl_output = startIK_ctrl.replace('ctrl' , 'output')
		startIK_zero = startIK_ctrl.replace('ctrl' , 'zero')
		cmds.parent(startIK_crv_jnt , startIK_ctrl_output)
		cmds.setAttr(startIK_crv_jnt + '.visibility' , 0)
		
		# 创建尾端的ik控制器
		endIK_jnt = self.ik_chain[-1]
		endIK_crv_jnt = pipelineUtils.Pipeline.create_node('joint' , endIK_jnt.replace('jnt' , 'crvjnt') ,
		                                                   match = True ,
		                                                   match_node = endIK_jnt)
		endIK_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.drv_jnts[-1] , 'ikctrl' , shape = 'Cube' ,
		                                                        radius = 25 ,
		                                                        axis = 'Y+' ,
		                                                        pos = endIK_jnt , parent = None)
		endIK_ctrl_output = endIK_ctrl.replace('ctrl' , 'output')
		endIK_zero = endIK_ctrl.replace('ctrl' , 'zero')
		cmds.parent(endIK_crv_jnt , endIK_ctrl_output)
		cmds.setAttr(endIK_crv_jnt + '.visibility' , 0)
		
		#
		# 创建中间的ik控制器
		midIK_jnt = self.ik_chain[2]
		midIK_crv_jnt = pipelineUtils.Pipeline.create_node('joint' , midIK_jnt.replace('jnt' , 'crvjnt') ,
		                                                   match = True ,
		                                                   match_node = midIK_jnt)
		
		midIK_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.drv_jnts[2] , 'ikctrl' ,
		                                                        shape = 'Cube' , radius = 20 , axis = 'Y+' ,
		                                                        pos = midIK_jnt , parent = None)
		midIK_ctrl_output = midIK_ctrl.replace('ctrl' , 'output')
		cmds.parent(midIK_crv_jnt , midIK_ctrl_output)
		cmds.setAttr(midIK_crv_jnt + '.visibility' , 0)
		midIK_zero = midIK_ctrl.replace('ctrl' , 'zero')
		
		# 曲线关节对ikspine曲线进行蒙皮
		cmds.skinCluster(startIK_crv_jnt , midIK_crv_jnt , endIK_crv_jnt , ik_chain_crv , tsb = True)
		
		# 曲线对ik关节做ik样条线手柄
		spine_ikhandle_node = \
			cmds.ikHandle(curve = ik_chain_crv , startJoint = self.ik_chain[0] , endEffector = self.ik_chain[4] ,
			              solver = 'ikSplineSolver' , createCurve = 0 ,
			              name = startIK_jnt.replace('jnt' , 'ikhandle'))[0]
		# 创建loc来制作ikhandle的横向旋转
		startIK_loc = cmds.spaceLocator(name = startIK_jnt.replace('jnt' , 'loc'))[0]
		endIK_loc = cmds.spaceLocator(name = endIK_jnt.replace('jnt' , 'loc'))[0]
		
		cmds.matchTransform(startIK_loc , startIK_jnt , position = True , rotation = True , scale = True)
		cmds.parent(startIK_loc , startIK_ctrl_output)
		cmds.matchTransform(endIK_loc , endIK_jnt , position = True , rotation = True , scale = True)
		cmds.parent(endIK_loc , endIK_ctrl_output)
		
		# 设置ikhandle的高级扭曲属性用来设置横向旋转
		cmds.setAttr(spine_ikhandle_node + '.dTwistControlEnable' , 1)
		cmds.setAttr(spine_ikhandle_node + '.dWorldUpType' , 4)
		cmds.connectAttr(startIK_loc + '.worldMatrix[0]' , spine_ikhandle_node + '.dWorldUpMatrix')
		cmds.connectAttr(endIK_loc + '.worldMatrix[0]' , spine_ikhandle_node + '.dWorldUpMatrixEnd')
		cmds.setAttr(spine_ikhandle_node + '.visibility' , 0)
		
		# 整理层级结构
		ik_ctrl_grp = cmds.createNode('transform' , name = self.ik_chain[0].replace('jnt' , 'grp'))
		cmds.parent(startIK_zero , midIK_zero , endIK_zero , ik_ctrl_grp)
		if self.control_parent :
			hierarchyUtils.Hierarchy.parent(child_node = ik_ctrl_grp , parent_node = self.control_parent)
		hierarchyUtils.Hierarchy.parent(child_node = spine_ikhandle_node , parent_node = self.rigNode_Local)
		hierarchyUtils.Hierarchy.parent(child_node = ik_chain_crv , parent_node = self.rigNode_World)
		
		# 添加拉伸效果
		# 获取ikspine曲线的形状节点
		if self.stretch :
			ik_chain_crv_shape = cmds.listRelatives(ik_chain_crv , shapes = True)[0]
			# 创建curveinfo节点来获取ikspine曲线的长度
			curveInfo_node = cmds.createNode('curveInfo' , name = ik_chain_crv.replace('crv' , 'crvInfo'))
			cmds.connectAttr(ik_chain_crv_shape + '.worldSpace' , curveInfo_node + '.inputCurve')
			ik_chain_crv_value = cmds.getAttr(curveInfo_node + '.arcLength')
			
			# 创建一个相加节点来获取ikspine曲线变换的数值
			add_curveInfo_node = cmds.createNode('addDoubleLinear' , name = ik_chain_crv.replace('crv' , 'add'))
			cmds.connectAttr(curveInfo_node + '.arcLength' , add_curveInfo_node + '.input1')
			cmds.setAttr(add_curveInfo_node + '.input2' , ik_chain_crv_value * -1)
			
			# 创建一个相乘节点，来将变换的数值平均分配给每个关节
			mult_curveInfo_node = cmds.createNode('multDoubleLinear' , name = ik_chain_crv.replace('crv' , 'mult'))
			cmds.connectAttr(add_curveInfo_node + '.output' , mult_curveInfo_node + '.input1')
			cmds.setAttr(mult_curveInfo_node + '.input2' , 0.25)
			
			# 给控制器创建一个拉伸的属性，动画师根据需要可以选择是否拉伸
			cmds.addAttr(endIK_ctrl , longName = 'stretch' , attributeType = 'double' ,
			             niceName = u'拉伸' , minValue = 0 , maxValue = 1 , defaultValue = 0 , keyable = 1)
			
			# 根据对应的关节创建对应的相加节点，将变换后的数值连接到对应的关节上
			for jnt in self.ik_chain[1 :-1] :
				add_node = cmds.createNode('addDoubleLinear' , name = jnt.replace('jnt' , 'add'))
			cmds.connectAttr(mult_curveInfo_node + '.output' , add_node + '.input1')
			cmds.setAttr(add_node + '.input2' , cmds.getAttr(jnt + '.translateX'))
			# 创建blendcolor节点用来承载拉伸的设置
			blend_node = cmds.createNode('blendColors' , name = jnt.replace('jnt' , 'blend'))
			cmds.connectAttr(endIK_ctrl + '.stretch' , blend_node + '.blender')
			# 设置blendcolor节点混合值为0的时候，也就是没有拉伸的时候，color2R 的值是原关节的长度
			cmds.setAttr(blend_node + '.color2R' , cmds.getAttr(jnt + '.translateX'))
			# 连接拉伸后的关节长度
			cmds.connectAttr(add_node + '.output' , blend_node + '.color1R')
			# 把混合后的关节长度连接给原关节
			cmds.connectAttr(blend_node + '.outputR' , jnt + '.translateX')


class IKFK_Rig(matehuman_base_rig.Base_Rig) :
	u"""
	这是一个用来编写ikfk混合绑定的类，之后的绑定都会在这个类的基础上逐级继承下去
	继承了ik_rig 和 fk_rig

	目前已有的功能：

	create_ikfk_chain_rig：创建ikfk关节链混合的绑定

	ikfk_chain_rig：创建混合IKFk链的bind链控制器绑定

	ikfk_spine_rig： 创建IK样条曲线（脊椎和脖子的绑定）和FK关节链的混合绑定

	ribbon_Rig ： 创建ribbon关节的绑定


	"""
	
	
	def __init__(self , drv_jnts , joint_parent , control_parent , space_list , stretch) :
		super(IKFK_Rig , self).__init__()
		self.drv_jnts = drv_jnts
		self.joint_parent = joint_parent
		self.control_parent = control_parent
		self.space_list = space_list
		self.stretch = stretch
	
	
	def create_ikfk_chain(self) :
		# 根据self.drv_jnts生成ik关节链
		self.ikfk_chain = jointUtils.Joint.create_mateHuman_chain(self.drv_jnts , 'ikfkjnt_' , self.joint_parent,
		                                                          constraint = True)
		
		return self.ikfk_chain
	
	
	def ikfk_spine_rig(self) :
		u"""
		创建IK样条曲线（脊椎和脖子的绑定）和FK关节链的混合绑定
		"""
		self.fk_systeam_chain = self.create_fk_chain()
		self.fk_systeam_rig = self.fk_chain_rig()
		
		self.ik_systeam_chain = self.create_ik_chain()
		self.ik_systeam_rig = self.ik_spine_rig()
		self.ikfk_chain_rig(self.fk_systeam_chain , self.ik_systeam_chain)
	
	
	def ikfk_chain_rig(self , fk_chain , ik_chain) :
		u"""
		创建混合IKFk链的bind链控制器绑定
		Args:
			fk_chain:fk关节链
			ik_chain:ik关节链
			drv_jnts:mateHuman的drv关节链
			control_parent(str): 控制器组的父层级

		Returns: ik_ctrl_grp ：ikfkBend控制器的最顶层

		"""
		# 获取创建控制器的关节的名称
		ctrl_jnt = matehumanUtils.MateHuman(self.drv_jnts[0])
		
		# 创建bind_jnt 关节的集合
		bind_jnt_set = 'set_bindJnt'
		make_bind_jnt_set = 'set_' + ctrl_jnt.side + '_' + ctrl_jnt.description + 'Jnt'
		make_bind_jnt_set = cmds.sets(name = make_bind_jnt_set , empty = True)
		if bind_jnt_set :
			bind_jnt_set = bind_jnt_set
		if not cmds.objExists(bind_jnt_set) or cmds.nodeType(bind_jnt_set) != 'objectSet' :
			bind_jnt_set = cmds.sets(name = bind_jnt_set , empty = True)
		for jnt in self.drv_jnts :
			cmds.sets(make_bind_jnt_set , edit = True , forceElement = bind_jnt_set)
			cmds.sets(jnt , edit = True , forceElement = make_bind_jnt_set)
		
		# 创建ikfk切换的控制器
		ikfkBend_ctrl = controlUtils.Control.create_mateHuman_ctrl(self.drv_jnts[0] , 'ikfkctrl' ,
		                                                           shape = 'pPlatonic' , radius = 10 ,
		                                                           axis = 'X+' ,
		                                                           pos = self.drv_jnts[0] , parent = None)
		ikfkBend_zero = ikfkBend_ctrl.replace('ctrl' , 'zero')
		cmds.move(0 , 15 , 15 , ikfkBend_zero , r = True , ls = True , wd = True)
		cmds.addAttr(ikfkBend_ctrl , longName = 'IkFkBend' , attributeType = 'double' , min = 0 , max = 1 ,
		             defaultValue = 1 ,
		             keyable = True)
		ikfkBend_grp = hierarchyUtils.Hierarchy.add_extra_group(obj = ikfkBend_zero ,
		                                                        grp_name = ikfkBend_zero.replace('zero' , 'grp') ,
		                                                        world_orient = False)
		
		# 锁定不需要的属性
		for channel in ['t' , 'r' , 's'] :
			
			for axis in ['x' , 'y' , 'z'] :
				cmds.setAttr(ikfkBend_ctrl + '.' + channel + axis , l = True , k = False , cb = False)
		cmds.setAttr(ikfkBend_ctrl + '.v' , l = True , k = False , cb = False)
		cmds.setAttr(ikfkBend_ctrl + '.ro' , l = True , k = False , cb = False)
		cmds.setAttr(ikfkBend_ctrl + '.subCtrlVis' , l = True , k = False , cb = False)
		
		# 用混合颜色节点来制作fk/ik开关
		# 连接切换
		for fk , ik , bind in zip(fk_chain , ik_chain , self.ikfk_chain) :
			for attr in ['translate' , 'rotate' , 'scale'] :
				blend_node = cmds.createNode('blendColors' , name = 'blend_{}_{}_001'.format(ctrl_jnt.side ,
				                                                                             ctrl_jnt.description))
				cmds.connectAttr(fk + '.{}'.format(attr) , blend_node + '.color1')
				cmds.connectAttr(ik + '.{}'.format(attr) , blend_node + '.color2')
				cmds.connectAttr(ikfkBend_ctrl + '.IkFkBend' , blend_node + '.blender')
				cmds.connectAttr(blend_node + '.output' , bind + '.{}'.format(attr))
		
		fk_ctrl_grp = fk_chain[0].replace('jnt' , 'grp')
		ik_ctrl_grp = ik_chain[0].replace('jnt' , 'grp')
		# 用混合颜色节点来连接fk/ik的控制器的显示开关
		cmds.connectAttr(ikfkBend_ctrl + '.IkFkBend' , fk_ctrl_grp + '.visibility')
		reverse_node = cmds.createNode('reverse' , name = blend_node.replace('blend_node_' , 'reverse_'))
		cmds.connectAttr(ikfkBend_ctrl + '.IkFkBend' , reverse_node + '.inputX')
		cmds.connectAttr(reverse_node + '.outputX' , ik_ctrl_grp + '.visibility')
		
		# 用ikfk关节链来约束mateHuman的驱动关节
		for ikfk , drv in zip(self.ikfk_chain , self.drv_jnts) :
			cmds.parentConstraint(ikfk , drv , mo = True)
			cmds.scaleConstraint(ikfk , drv , mo = True)
		
		# 整理层级结构
		hierarchyUtils.Hierarchy.parent(child_node = ikfkBend_grp , parent_node = self.control_parent)
	
	
	def create_ribbon_Rig(self , ikfk_chain , control_parent , joint_parent , joint_number) :
		u"""
			  创建ribbon关节的绑定
			  """
		upper_part = nameUtils.Name(name = ikfk_chain[0])
		lower_part = nameUtils.Name(name = ikfk_chain[1])
		# 创建ribbon关节和twist关节
		self.ribbon_rig(upper_part.name , self.control_parent , self.joint_parent , joint_number = joint_number)
		self.ribbon_rig(lower_part.name , self.control_parent , self.joint_parent , joint_number = joint_number)
		
		# 吸附带控制器组的位置和旋转
		ribbon_upper_start_driven = 'driven_{}_{}Start_001'.format(upper_part.side , upper_part.description)
		ribbon_upper_End_driven = 'driven_{}_{}End_001'.format(upper_part.side , upper_part.description)
		
		ribbon_lower_start_driven = 'driven_{}_{}Start_001'.format(lower_part.side , lower_part.description)
		ribbon_lower_End_driven = 'driven_{}_{}End_001'.format(lower_part.side , lower_part.description)
		
		# 关节约束对应的控制器组
		
		cmds.parentConstraint(ikfk_chain[0] , ribbon_upper_start_driven , maintainOffset = False)
		cmds.parentConstraint(ikfk_chain[1] , ribbon_upper_End_driven , maintainOffset = False)
		
		cmds.parentConstraint(ikfk_chain[1] , ribbon_lower_End_driven , maintainOffset = False)
		cmds.parentConstraint(ikfk_chain[2] , ribbon_lower_start_driven , maintainOffset = False)
	
	
	def create_fk_chain_system(self) :
		u'''
		创建fk链条绑定系统
		:return:
		'''
		self.fk_systeam = FK_Rig(self.drv_jnts , self.joint_parent , self.control_parent,redius = 10)
		self.fk_systeam_chain = self.fk_systeam.create_fk_chain()
		self.fk_systeam_rig = self.fk_systeam.fk_chain_rig()
	
	
	def create_ik_chain_system(self, Y_value) :
		u'''
		创建ik链条绑定系统
		:return:
		'''
		self.ik_systeam = IK_Rig(self.drv_jnts , self.joint_parent , self.control_parent , self.space_list ,
		                         self.stretch)
		self.ik_systeam_chain = self.ik_systeam.create_ik_chain()
		self.ik_systeam_rig = self.ik_systeam.ik_chain_rig(Y_value)
	
	
	def create_ik_spine_system(self, Y_value) :
		u'''
		创建ikSpine绑定系统
		:return:
		'''
		self.ik_systeam = IK_Rig(self.drv_jnts , self.joint_parent , self.control_parent , self.space_list ,
		                         self.stretch)
		self.ik_systeam_chain = self.ik_systeam.create_ik_chain()
		self.ik_systeam_rig = self.ik_systeam.ik_chain_rig(Y_value)
	
	
	def create_ikfk_chain_rig(self, Y_value) :
		u"""
		创建ikfk关节链混合的绑定,手臂，腿部关节
		"""
		
		# 创建fk控制系统
		self.create_fk_chain_system()
		
		# 创建ik控制系统
		self.create_ik_chain_system(Y_value)
		
		# 创建ikfk融合系统
		self.ikfk_systeam_chain = self.create_ikfk_chain()
		self.ikfk_chain_rig(self.fk_systeam_chain , self.ik_systeam_chain)
	
	
	def create_ikfk_spine_rig(self) :
		u"""
		创建IK样条曲线（脊椎和脖子的绑定）和FK关节链的混合绑定
		"""
		
		# 创建fk控制系统
		self.create_fk_chain_system()
		
		# 创建ik控制系统
		self.create_ik_spine_system(Y_value)
		
		# 创建ikfk融合系统
		self.ikfk_systeam_chain = self.create_ikfk_chain()
		self.ikfk_spine_rig(self.fk_systeam_chain , self.ik_systeam_chain)
	
	
	def ribbon_rig(self , name , control_parent , joint_parent , joint_number = 5) :
		u"""
		创建ribbon控制器，给动画师更细致的动画效果
		思路：通过给定关节的名称来创建ribbon控制，通过曲线来生成曲面制作ribbon绑定，然后让生成的关节绑定在曲面上
		采用的变形器有twist，sine和wire变形器，通过这些变形器影响曲面，从而带动曲面上的关节

		Args:
			name(object):创建ribbon关节控制的名称
			self.control_parent:控制器组的父层级
			self.joint_parent:ribbon关节组的父层级
			joint_number (int): 需要创建的ribbon关节数量

		"""
		# 从名称中获取ribbon控制器的边，描述，和编号
		ribbon = nameUtils.Name(name = name)
		
		# 从ribbon控制器中的边获取偏移值
		if ribbon.side != 'r' :
			offset_val = 1
		else :
			offset_val = -1
		
		# 创建ribbon控制器对应的层级组
		ribbon_ctrl_grp = cmds.createNode('transform' ,
		                                  name = 'grp_{}_{}RibbonCtrls_{:03d}'.format(ribbon.side , ribbon.description ,
		                                                                              ribbon.index) ,
		                                  parent = self.control_parent)
		ribbon_jnt_grp = cmds.createNode('transform' ,
		                                 name = 'grp_{}_{}RibbonJnts_{:03d}'.format(ribbon.side , ribbon.description ,
		                                                                            ribbon.index) ,
		                                 parent = self.joint_parent)
		nodes_local_grp = cmds.createNode('transform' ,
		                                  name = 'grp_{}_{}RibbonNodesLocal_{:03d}'.format(ribbon.side ,
		                                                                                   ribbon.description ,
		                                                                                   ribbon.index) ,
		                                  parent = self.rigNode_Local)
		nodes_world_grp = cmds.createNode('transform' ,
		                                  name = 'grp_{}_{}RibbonNodesWorld_{:03d}'.format(ribbon.side ,
		                                                                                   ribbon.description ,
		                                                                                   ribbon.index) ,
		                                  parent = self.rigNode_World)
		cmds.setAttr(ribbon_ctrl_grp + '.inheritsTransform' , 0)
		cmds.setAttr(nodes_world_grp + '.inheritsTransform' , 0)
		
		cmds.setAttr(nodes_local_grp + '.visibility' , 0)
		cmds.setAttr(nodes_world_grp + '.visibility' , 0)
		
		# 创建对应的曲线以生成nurbs曲面
		temp_curve = cmds.curve(point = [[5 * offset_val , 0 , 0] , [-5 * offset_val , 0 , 0]] , knot = [0 , 1] ,
		                        degree = 1)
		# 根据关节数重建曲线
		cmds.rebuildCurve(temp_curve , degree = 3 , replaceOriginal = True , rebuildType = 0 , endKnots = 1 ,
		                  keepRange = 0 ,
		                  keepControlPoints = False , keepEndPoints = True , keepTangents = False ,
		                  spans = joint_number + 1)
		# 复制这条曲线
		temp_curve_02 = cmds.duplicate(temp_curve)[0]
		# 移动两条曲线的位置来制作曲面
		cmds.setAttr(temp_curve + '.translateZ' , 1)
		cmds.setAttr(temp_curve_02 + '.translateZ' , -1)
		
		# 通过两条曲线来放样制作曲面
		surf = \
			cmds.loft(temp_curve_02 , temp_curve , constructionHistory = False , uniform = True , degree = 3 ,
			          sectionSpans = 1 ,
			          range = False , polygon = 0 ,
			          name = 'surf_{}_{}Ribbon_{:03d}'.format(ribbon.side , ribbon.description , ribbon.index))[0]
		cmds.parent(surf , nodes_local_grp)
		
		# 获得曲面的形状节点
		surf_shape = cmds.listRelatives(surf , shapes = True)[0]
		
		# 删除用来放样曲面的曲线
		cmds.delete(temp_curve , temp_curve_02)
		
		# 创建关节并附着到曲面
		fol_grp = cmds.createNode('transform' ,
		                          name = 'grp_{}_{}RibbonFollicles_{:03d}'.format(ribbon.side , ribbon.description ,
		                                                                          ribbon.index) ,
		                          parent = nodes_world_grp)
		
		# 创建ribbon关节的集合
		ribbon_jnt_set = 'set_ribbonJnt'
		make_ribbon_jnt_set = 'set_' + ribbon.side + '_' + ribbon.description + 'Jnt'
		make_ribbon_jnt_set = cmds.sets(name = make_ribbon_jnt_set , empty = True)
		if not cmds.objExists(ribbon_jnt_set) or cmds.nodeType(ribbon_jnt_set) != 'objectSet' :
			ribbon_jnt_set = cmds.sets(name = ribbon_jnt_set , empty = True)
			cmds.sets(make_ribbon_jnt_set , edit = True , forceElement = ribbon_jnt_set)
		else :
			cmds.sets(make_ribbon_jnt_set , edit = True , forceElement = ribbon_jnt_set)
		
		for i in range(joint_number) :
			# 创建毛囊
			fol_shape = cmds.createNode('follicle' , name = 'fol_{}_{}Ribbon{:03d}_{:03d}Shape'.format(ribbon.side ,
			                                                                                           ribbon.description ,
			                                                                                           i + 1 ,
			                                                                                           ribbon.index))
			# 重命名毛囊的tran节点名称
			fol = cmds.listRelatives(fol_shape , parent = True)[0]
			fol = cmds.rename(fol , fol_shape[:-5])
			# 把毛囊放入对应的层级组
			cmds.parent(fol , fol_grp)
			# 连接毛囊属性
			cmds.connectAttr(surf_shape + '.worldSpace[0]' , fol_shape + '.inputSurface')
			# 连接毛囊的形状节点以进行变换
			cmds.connectAttr(fol_shape + '.outTranslate' , fol + '.translate')
			cmds.connectAttr(fol_shape + '.outRotate' , fol + '.rotate')
			# 设置uv值
			cmds.setAttr(fol_shape + '.parameterU' , 0.5)
			cmds.setAttr(fol_shape + '.parameterV' , float(i) / (joint_number - 1))
			
			# 创建关节
			jnt = cmds.createNode('joint' ,
			                      name = 'jnt_{}_{}Ribbon{:03d}_{:03d}'.format(ribbon.side , ribbon.description ,
			                                                                   i + 1 ,
			                                                                   ribbon.index))
			parent_grp = ribbon_jnt_grp
			grp_nodes = []
			for node_type in ['zero' , 'offset'] :
				grp = cmds.createNode('transform' , name = jnt.replace('jnt' , node_type) , parent = parent_grp)
				grp_nodes.append(grp)
				parent_grp = grp
			
			cmds.parent(jnt , grp_nodes[-1])
			# 让对应的毛囊约束对应的关节点
			cmds.parentConstraint(fol , grp_nodes[0] , maintainOffset = False)
			# 将偏移组的旋转设置为零
			cmds.xform(grp_nodes[1] , rotation = [0 , 0 , 0] , worldSpace = True)
			
			# 将生成的ribbon关节放在对应的集里方便选择
			cmds.sets(jnt , edit = True , forceElement = make_ribbon_jnt_set)
		
		# 创建控制器
		ctrls = []
		for pos in ['start' , 'mid' , 'end'] :
			ctrl_name = 'ctrl_{}_{}{}_{:03d}'.format(ribbon.side , ribbon.description , pos.title() , ribbon.index)
			ctrl = controlUtils.Control.create_ctrl(ctrl_name , shape = 'hexagon' , radius = 5 ,
			                                        axis = 'Z+' ,
			                                        pos = None , parent = ribbon_ctrl_grp)
			
			ctrls.append(ctrl_name)
		# 放置控制器
		cmds.setAttr(ctrls[0].replace('ctrl' , 'zero') + '.translateX' , -5 * offset_val)
		cmds.setAttr(ctrls[2].replace('ctrl' , 'zero') + '.translateX' , 5 * offset_val)
		
		# 约束中间的控制器
		cmds.parentConstraint(ctrls[0] , ctrls[-1] , ctrls[1].replace('ctrl' , 'driven') , maintainOffset = False)
		
		# 添加twist的控制属性在第一个控制器和最后一个控制器上,'start'和 'end'
		cmds.addAttr(ctrls[0] , longName = 'twist' , niceName = u'扭曲' , attributeType = 'float' , keyable = True)
		cmds.addAttr(ctrls[-1] , longName = 'twist' , niceName = u'扭曲' , attributeType = 'float' , keyable = True)
		# 创建twist变形器
		twist_node , twist_hnd = cmds.nonLinear(surf , type = 'twist' , name = surf.replace('surf_' , 'twist_'))
		cmds.parent(twist_hnd , nodes_local_grp)
		cmds.setAttr(twist_hnd + '.rotate' , 0 , 0 , 90)
		scale_val = cmds.getAttr(twist_hnd + '.scaleX')
		cmds.setAttr(twist_hnd + '.scale' , scale_val * offset_val , scale_val * offset_val , scale_val * offset_val)
		# 连接twist变形器的属性到控制器上
		twist_hnd_shape = cmds.listRelatives(twist_hnd , shapes = True)[0]
		cmds.connectAttr(ctrls[0] + '.twist' , twist_node + '.endAngle')
		cmds.connectAttr(ctrls[-1] + '.twist' , twist_node + '.startAngle')
		
		# 添加sine的控制属性在中间的控制器上,'mid'
		cmds.addAttr(ctrls[1] , longName = 'sineDivider' , niceName = u'sine变形器属性设置 ----------' ,
		             attributeType = 'enum' ,
		             enumName = ' ' , keyable = False)
		cmds.setAttr(ctrls[1] + '.sineDivider' , channelBox = True , lock = True)
		cmds.addAttr(ctrls[1] , longName = 'amplitude' , niceName = u'振幅' , attributeType = 'float' , keyable = True ,
		             minValue = 0)
		cmds.addAttr(ctrls[1] , longName = 'wavelength' , niceName = u'波长' , attributeType = 'float' ,
		             keyable = True ,
		             minValue = 0.1 ,
		             defaultValue = 2)
		cmds.addAttr(ctrls[1] , longName = 'offset' , niceName = u'偏移' , attributeType = 'float' , keyable = True)
		cmds.addAttr(ctrls[1] , longName = 'sineRotation' , niceName = u'正弦旋转' , attributeType = 'float' ,
		             keyable = True)
		# 创建sine变形器
		sine_node , sine_hnd = cmds.nonLinear(surf , type = 'sine' , name = surf.replace('surf_' , 'sine_'))
		cmds.parent(sine_hnd , nodes_local_grp)
		cmds.setAttr(sine_hnd + '.rotate' , 0 , 0 , 90)
		scale_val = cmds.getAttr(sine_hnd + '.scaleX')
		cmds.setAttr(sine_hnd + '.scale' , scale_val * offset_val , scale_val * offset_val , scale_val * offset_val)
		cmds.setAttr(sine_node + '.dropoff' , 1)
		# 连接sine变形器的属性到控制器上
		sine_hnd_shape = cmds.listRelatives(sine_hnd , shapes = True)[0]
		cmds.connectAttr(ctrls[1] + '.amplitude' , sine_node + '.amplitude')
		cmds.connectAttr(ctrls[1] + '.wavelength' , sine_node + '.wavelength')
		cmds.connectAttr(ctrls[1] + '.offset' , sine_node + '.offset')
		cmds.connectAttr(ctrls[1] + '.sineRotation' , sine_hnd + '.rotateY')
		
		# 创建wire变形器
		# 创建wire变形器需要的曲线
		wire_curve = cmds.curve(point = [[-5 * offset_val , 0 , 0] , [0 , 0 , 0] , [5 * offset_val , 0 , 0]] ,
		                        knot = [0 , 0 , 1 , 1] ,
		                        degree = 2 ,
		                        name = 'crv_{}_{}RibbonWire_{:03d}'.format(ribbon.side , ribbon.description ,
		                                                                   ribbon.index))
		wire_curve_shape = cmds.listRelatives(wire_curve , shapes = True)[0]
		cmds.rename(wire_curve_shape , wire_curve + 'Shape')
		cmds.parent(wire_curve , nodes_world_grp)
		
		# 创建cluster 变形器，用控制器来约束cluster变形器的变化
		for ctrl , i in zip(ctrls , [0 , 1 , 2]) :
			cls_node , cls_hnd = cmds.cluster('{}.cv[{}]'.format(wire_curve , i) , name = ctrl.replace('ctrl' , 'cls'))
			cmds.parent(cls_hnd , nodes_world_grp)
			cmds.pointConstraint(ctrl , cls_hnd , maintainOffset = False)
		#
		# 创建wire变形器
		wire_node = surf.replace('surf' , 'wire')
		cmds.wire(surf , wire = wire_curve , name = wire_node)
		cmds.setAttr(wire_node + '.dropoffDistance[0]' , 200)
		cmds.parent(wire_curve + 'BaseWire' , nodes_local_grp)

