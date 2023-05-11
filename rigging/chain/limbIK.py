from . import chain , chainIK , chainFK
import maya.cmds as cmds
from ...core import pipelineUtils , vectorUtils,controlUtils



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
		self._rtype = 'IK'
		
		# 判断给定的limbtype 是手臂还是腿部
		if limbtype == 'arm' :
			self.z_value = 1
		else :
			self.z_value = -1
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		self.pv_ctrl = ('ctrl_{}_{}{}PV_001'.format(self._side , self._name , self._rtype))
		self.pv_loc = ('loc_{}_{}{}PV_001'.format(self._side , self._name , self._rtype))
		self.jnt_loc = ('jnt_{}_{}{}PV_001'.format(self._side , self._name , self._rtype))
		self.pv_curve = ('crv_{}_{}{}PV_001'.format(self._side , self._name , self._rtype))
	
	
	
	def build_ikHandle(self) :
		u'''
				创建ikHandle
				'''
		
		print(self.jnt_list[0])
		# 创建ikSolverHandle
		
		self.ik_handle = cmds.ikHandle(name = self.ik_handle , startJoint = self.jnt_list[0] ,
		                               endEffector = self.jnt_list[-1] ,
		                               sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True)[0]
		
		cmds.setAttr(self.ik_handle + '.v' , 0)
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		# 创建极向量控制器
		self.pv_ctrl = controlUtils.Control.create_ctrl(self.pv_ctrl , shape = 'cube' ,
		                                                radius = self.radius ,
		                                                axis = 'X+' , pos = self.jnt_list[1] ,
		                                                parent = self.control_parent)
		# 移动极向量控制器组的位置
		cmds.setAttr(self.pv_ctrl.replace('ctrl' , 'zero') + '.translateZ' , 10 * self.z_value)

		cmds.parent(self.ik_handle , self.output_list[-1])
		
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
	
	
	
	def add_constraint(self) :
		# 极向量控制器约束ikHandle
		cmds.poleVectorConstraint(self.pv_ctrl.replace('ctrl' , 'output') , self.ik_handle)
	
	
	
	def build_rig(self) :
		self.create_namespace()
		self.joint_orientation()
		self.create_joint()
		self.build_ikHandle()
		self.create_ctrl()
		# self.add_constraint()
