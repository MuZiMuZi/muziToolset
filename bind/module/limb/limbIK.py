import maya.cmds as cmds

from ....core import controlUtils , hierarchyUtils
from ..chain import chainIK



class LimbIK(chainIK.ChainIK) :
	u"""
	创建手臂或者是腿部的四肢关节的IK绑定,IK绑定需要创建极向量控制器和ikHandle
	"""
	
	
	
	def __init__(self , side , name , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 , is_stretch = 1 ,
	             limbtype = None ,
	             joint_parent = None ,
	             control_parent = None) :
		u"""
		创建手臂或者是腿部的四肢关节的IK绑定
		limbtype(str):给定的limbtype 是手臂还是腿部
		"""
		super().__init__(side , name , joint_number , direction , length , is_stretch , joint_parent , control_parent)
		self._rtype = 'LimbIK'
		self.joint_number = joint_number
		# 判断给定的limbtype 是手臂还是腿部
		if limbtype == 'arm' :
			self.z_value = 1
		else :
			self.z_value = -1
		
		self.radius = 5
		
		self.shape = 'cube'
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		self.pv_ctrl = ('ctrl_{}_{}{}PV_001'.format(self._side , self._name , self._rtype))
		self.pv_loc = ('loc_{}_{}{}PV_001'.format(self._side , self._name , self._rtype))
		self.jnt_loc = ('jnt_{}_{}{}PV_001'.format(self._side , self._name , self._rtype))
		self.pv_curve = ('crv_{}_{}{}PV_001'.format(self._side , self._name , self._rtype))
		self.local_ctrl = ('ctrl_{}_{}{}Local_001'.format(self._side , self._name , self._rtype))
		self.startIK_pos_loc = self.jnt_list[0].replace('jnt' , 'loc')
		self.endIK_pos_loc = self.jnt_list[-1].replace('jnt' , 'loc')
		
		# 添加一个末端的iK关节用来制作singleIKhandle，
		self.endIK_handle = ('handle_{}_{}{}End_001'.format(self._side , self._name , self._rtype))
		self.endIK_jnt = 'jnt_{}_{}{}_{:03d}'.format(self._side , self._name , self._rtype , self.joint_number + 1)
	
	
	
	def create_joint(self) :
		super().create_joint()
		self.endIK_jnt = cmds.createNode('joint' , name = self.endIK_jnt , parent = self.jnt_list[-1])
		con = cmds.parentConstraint(self.jnt_list[-1] , self.endIK_jnt , mo = False)
		cmds.delete(con)
		cmds.setAttr(self.endIK_jnt + '.translateX' , 5 * side_value)
	
	
	
	def build_ikHandle(self) :
		u'''
				创建ikHandle
				'''
		
		# 创建ikSolverHandle
		
		self.ik_handle = cmds.ikHandle(name = self.ik_handle , startJoint = self.jnt_list[0] ,
		                               endEffector = self.jnt_list[2] ,
		                               sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True)[0]
		
		# 创建末端的ikspineHandle
		self.endIK_handle = cmds.ikHandle(name = self.endIK_handle , startJoint = self.jnt_list[2] ,
		                                  endEffector = self.endIK_jnt ,
		                                  sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True)[0]
		
		cmds.setAttr(self.ik_handle + '.v' , 0)
		cmds.setAttr(self.endIK_handle + '.v' , 0)
	
	
	
	def create_ctrl(self) :
		u'''
		创建控制器结构
		'''
		super().create_ctrl()
		# 创建ikhandle系统
		self.build_ikHandle()
		cmds.setAttr(self.zero_list[1] + '.v' , 0)
		# 创建极向量控制器
		self.pv_ctrl = controlUtils.Control.create_ctrl(self.pv_ctrl , shape = 'ball' ,
		                                                radius = self.radius * 0.6 ,
		                                                axis = 'X+' , pos = self.jnt_list[1] ,
		                                                parent = self.ctrl_grp)
		# 移动极向量控制器组的位置
		cmds.setAttr(self.pv_ctrl.replace('ctrl' , 'zero') + '.translateZ' , -10 * self.z_value * self.side_value)
		
		cmds.parent(self.ik_handle , self.endIK_handle , self.output_list[-1])
		
		## 创建ik极向量控制器的曲线指示器
		# 创建pv控制器的loc来记录位置
		midIK_pv_loc = cmds.spaceLocator(name = self.pv_loc)[0]
		cmds.matchTransform(midIK_pv_loc , self.pv_ctrl.replace('ctrl' , 'output') , position = True , rotation =
		True ,
		                    scale = True)
		cmds.parent(midIK_pv_loc , self.pv_ctrl)
		cmds.setAttr(midIK_pv_loc + '.visibility' , 0)
		# 创建pvjnt的loc来记录位置
		midIK_jnt_loc = cmds.spaceLocator(name = self.jnt_loc)[0]
		cmds.matchTransform(midIK_jnt_loc , self.jnt_list[1] , position = True , rotation = True , scale = True)
		cmds.parent(midIK_jnt_loc , self.jnt_list[1])
		cmds.setAttr(midIK_jnt_loc + '.visibility' , 0)
		
		# 连接loc和曲线来表示位置
		ikpv_curve = cmds.curve(degree = 1 , point = [(0.0 , 0.0 , 0.0) , (0.0 , 0.0 , 0.0)] ,
		                        name = self.pv_curve)
		midIK_jnt_loc_shape = cmds.listRelatives(midIK_jnt_loc , shapes = True)[0]
		midIK_pv_loc_shape = cmds.listRelatives(midIK_pv_loc , shapes = True)[0]
		ikpv_curve_shape = cmds.listRelatives(ikpv_curve , shapes = True)[0]
		
		# 连接曲线与loc
		cmds.connectAttr(midIK_jnt_loc_shape + '.worldPosition[0]' , ikpv_curve_shape + '.controlPoints[0]')
		cmds.connectAttr(midIK_pv_loc_shape + '.worldPosition[0]' , ikpv_curve_shape + '.controlPoints[1]')
		# 设置曲线的可见性
		cmds.setAttr(ikpv_curve_shape + '.overrideEnabled' , 1)
		cmds.setAttr(ikpv_curve_shape + '.overrideDisplayType' , 2)
		cmds.setAttr(ikpv_curve + '.inheritsTransform' , 0)
		cmds.parent(ikpv_curve , self.ctrl_grp)
		
		# 创建local控制器给手腕
		self.local_ctrl = controlUtils.Control.create_ctrl(self.local_ctrl , shape = 'cross' ,
		                                                   radius = self.radius * 0.75 ,
		                                                   axis = 'X+' , pos = self.jnt_list[-1] ,
		                                                   parent = self.ctrl_list[-1])
		
		# 判断是否需要添加拉伸功能
		if not self.is_stretch :
			return
		else :
			self.add_stretch()
	
	
	
	def add_constraint(self) :
		# 极向量控制器约束ikHandle
		cmds.poleVectorConstraint(self.pv_ctrl.replace('ctrl' , 'output') , self.ik_handle)
		
		# ikHandle放到local控制器层级下
		cmds.parent(self.ik_handle , self.local_ctrl.replace('ctrl' , 'output'))
		
		# 首段ik控制器点约束首段ik关节
		cmds.pointConstraint(self.output_list[0] , self.jnt_list[0] , mo = True)
	
	
	
	def add_stretch(self) :
		u"""
		添加ik链条的拉伸功能
		"""
		self.startIK_pos_loc = cmds.spaceLocator(name = self.startIK_pos_loc)[0]
		startIK_pos_loc_shape = cmds.listRelatives(self.startIK_pos_loc , shapes = True)[0]
		cmds.matchTransform(self.startIK_pos_loc , self.ctrl_list[0])
		cmds.setAttr(self.startIK_pos_loc + '.v' , 0)
		hierarchyUtils.Hierarchy.parent(child_node = self.startIK_pos_loc , parent_node = self.output_list[0])
		
		# 创建末端关节控制器的定位loctor
		self.endIK_pos_loc = cmds.spaceLocator(name = self.endIK_pos_loc)[0]
		endIK_pos_loc_shape = cmds.listRelatives(self.endIK_pos_loc , shapes = True)[0]
		cmds.setAttr(self.endIK_pos_loc + '.v' , 0)
		cmds.matchTransform(self.endIK_pos_loc , self.ctrl_list[-1])
		hierarchyUtils.Hierarchy.parent(child_node = self.endIK_pos_loc , parent_node = self.output_list[-1])
		
		# 创建计算距离的distween节点，来计算首端关节到中端控制器的距离
		disBtw_node = cmds.createNode('distanceBetween' , name = self.endIK_pos_loc.replace('loc' , 'disBtw'))
		cmds.connectAttr(startIK_pos_loc_shape + '.worldPosition' , disBtw_node + '.point1')
		cmds.connectAttr(endIK_pos_loc_shape + '.worldPosition' , disBtw_node + '.point2')
		
		# 计算原本关节的距离值
		midIK_jnt_value = cmds.getAttr(self.jnt_list[1] + '.translateX')
		endIK_jnt_value = cmds.getAttr(self.jnt_list[-1] + '.translateX')
		distance_value = midIK_jnt_value * self.side_value + endIK_jnt_value * self.side_value
		
		# 将现有的关节距离减去原本关节的距离得到拉伸的距离
		reduce_node = cmds.createNode('addDoubleLinear' , name = self.jnt_list[0].replace('jnt' , 'reduce'))
		cmds.connectAttr(disBtw_node + '.distance' , reduce_node + '.input1')
		cmds.setAttr(reduce_node + '.input2' , distance_value * -1 * self.z_value)
		
		# 将变化的数值除以二，均匀分配给对应的拉伸关节
		mult_node = cmds.createNode('multDoubleLinear' , name = self.jnt_list[0].replace('jnt' , 'mult'))
		cmds.connectAttr(reduce_node + '.output' , mult_node + '.input1')
		cmds.setAttr(mult_node + '.input2' , 0.5 * self.side_value * self.z_value)
		
		# 将变化的数值连接给对应的拉伸关节
		add_midIK_jnt_node = cmds.createNode('addDoubleLinear' , name = self.jnt_list[1].replace('jnt' , 'add'))
		add_endIK_jnt_node = cmds.createNode('addDoubleLinear' , name = self.jnt_list[-1].replace('jnt' , 'add'))
		
		cmds.connectAttr(mult_node + '.output' , add_midIK_jnt_node + '.input1')
		cmds.setAttr(add_midIK_jnt_node + '.input2' , midIK_jnt_value)
		
		cmds.connectAttr(mult_node + '.output' , add_endIK_jnt_node + '.input1')
		cmds.setAttr(add_endIK_jnt_node + '.input2' , endIK_jnt_value)
		
		# 创建一个判断节点，当变化的数值大于0时才进行拉伸
		cond_node = cmds.createNode('condition' , name = self.jnt_list[0].replace('jnt' , 'cond'))
		cmds.setAttr(cond_node + '.operation' , 2)
		cmds.connectAttr(reduce_node + '.output' , cond_node + '.firstTerm')
		cmds.connectAttr(add_midIK_jnt_node + '.output' , cond_node + '.colorIfTrueR')
		cmds.connectAttr(add_endIK_jnt_node + '.output' , cond_node + '.colorIfTrueG')
		
		cmds.setAttr(cond_node + '.colorIfFalseR' , midIK_jnt_value)
		cmds.setAttr(cond_node + '.colorIfFalseG' , endIK_jnt_value)
		
		# 给控制器创建一个拉伸的属性，动画师根据需要可以选择是否拉伸
		cmds.addAttr(self.ctrl_list[-1] , longName = 'stretch' , attributeType = 'double' ,
		             niceName = u'拉伸' , minValue = 0 , maxValue = 1 , defaultValue = 1 , keyable = 1)
		
		# 创建blendcolor节点用来承载拉伸的设置
		stretch_blend_node = cmds.createNode('blendColors' , name = self.ctrl_list[-1].replace('ctrl' , 'blend'))
		cmds.connectAttr(self.ctrl_list[-1] + '.stretch' , stretch_blend_node + '.blender')
		# 设置blendcolor节点混合值为0的时候，也就是没有拉伸的时候，color2R 和 color2G 的值是原关节的长度
		# 连接拉伸后的关节长度
		stretch_divBtw_node = cmds.createNode('multiplyDivide' ,
		                                      name = stretch_blend_node.replace('blend' , 'div'))
		
		cmds.setAttr(stretch_divBtw_node + '.operation' , 2)
		cmds.setAttr(stretch_divBtw_node + '.input1X' , midIK_jnt_value)
		cmds.setAttr(stretch_divBtw_node + '.input1Y' , endIK_jnt_value)
		cmds.connectAttr(stretch_divBtw_node + '.outputX' , stretch_blend_node + '.color2R')
		cmds.connectAttr(stretch_divBtw_node + '.outputY' , stretch_blend_node + '.color2G')
		cmds.connectAttr(cond_node + '.outColorR' , stretch_blend_node + '.color1R')
		cmds.connectAttr(cond_node + '.outColorG' , stretch_blend_node + '.color1G')
		
		# 给控制器创建一个极向量锁定的属性，动画师根据需要可以选择是否进行极向量锁定
		cmds.addAttr(self.ctrl_list[-1] , longName = 'PvLock' , attributeType = 'double' ,
		             niceName = u'极向量锁定' , minValue = 0 , maxValue = 1 , defaultValue = 0 , keyable = 1)
		pv_loc_shape = cmds.listRelatives(self.pv_loc , shapes = True)[0]
		
		# 创建blendcolor节点用来承载极向量锁定的设置
		pvLock_blend_node = cmds.createNode('blendColors' , name = self.pv_ctrl.replace('ctrl' , 'blend'))
		cmds.connectAttr(self.ctrl_list[-1] + '.PvLock' , pvLock_blend_node + '.blender')
		
		# 获取起始控制器，极向量控制器，末端控制器层级下用来定位位置的loc.(startIK_pos_loc,midIK_pv_loc,endIK_pos_loc)
		# 创建对应的disteween节点来获取距离
		# 计算起始控制器到极向量控制器的距离
		upper_disBtw_node = cmds.createNode('distanceBetween' ,
		                                    name = self.startIK_pos_loc.replace('loc' , 'disBtw_upper'))
		cmds.connectAttr(startIK_pos_loc_shape + '.worldPosition' , upper_disBtw_node + '.point1')
		cmds.connectAttr(pv_loc_shape + '.worldPosition' , upper_disBtw_node + '.point2')
		
		# 创建一个相乘节点来连接
		mult_upper_disBtw_node = cmds.createNode('multDoubleLinear' ,
		                                         name = upper_disBtw_node.replace('disBtw_lower' , 'mult'))
		cmds.connectAttr(upper_disBtw_node + '.distance' , mult_upper_disBtw_node + '.input1')
		cmds.setAttr(mult_upper_disBtw_node + '.input2' , self.side_value * self.z_value)
		
		# 计算末端控制器到极向量控制器的距离
		lower_disBtw_node = cmds.createNode('distanceBetween' ,
		                                    name = self.startIK_pos_loc.replace('loc' , 'disBtw_lower'))
		cmds.connectAttr(pv_loc_shape + '.worldPosition' , lower_disBtw_node + '.point1')
		cmds.connectAttr(endIK_pos_loc_shape + '.worldPosition' , lower_disBtw_node + '.point2')
		# 创建一个相乘节点来连接
		mult_lower_disBtw_node = cmds.createNode('multDoubleLinear' ,
		                                         name = lower_disBtw_node.replace('disBtw_lower' , 'mult'))
		cmds.connectAttr(lower_disBtw_node + '.distance' , mult_lower_disBtw_node + '.input1')
		cmds.setAttr(mult_lower_disBtw_node + '.input2' , self.side_value * self.z_value)
		
		# 将真实的距离连接给极向量锁定的blendcolor节点
		# 原理：当极向量锁定值为1打开的时候，启用的是color1的数值。当极向量锁定值为0关闭的时候，启用的是color2的数值
		
		cmds.connectAttr(mult_upper_disBtw_node + '.output' , pvLock_blend_node + '.color1R')
		cmds.connectAttr(mult_lower_disBtw_node + '.output' , pvLock_blend_node + '.color1G')
		
		# 将原先关节拉伸后的距离连接给极向量锁定的blendcolor节点的color2
		cmds.connectAttr(stretch_blend_node + '.outputR' , pvLock_blend_node + '.color2R')
		cmds.connectAttr(stretch_blend_node + '.outputG' , pvLock_blend_node + '.color2G')
		
		# 把混合后的关节长度连接给原关节
		cmds.connectAttr(pvLock_blend_node + '.outputR' , self.jnt_list[1] + '.translateX')
		cmds.connectAttr(pvLock_blend_node + '.outputG' , self.jnt_list[-1] + '.translateX')



if __name__ == '__main__' :
	def build_setup() :
		custom = limbIK.LimbIK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
		                       is_stretch = 1 ,
		                       limbtype = 'arm' ,
		                       joint_parent = None ,
		                       control_parent = None)
		custom.build_setup()
	
	
	
	def build_rig() :
		custom = limbIK.LimbIK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
		                       limbtype = 'arm' ,
		                       joint_parent = None ,
		                       control_parent = None)
		custom.build_rig()
	
	
	
	build_setup()
	build_rig()
