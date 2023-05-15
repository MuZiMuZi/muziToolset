import maya.cmds as cmds
from ..base import base , bone
from ..chain import chain , chainFK , chainIK
from ...core import controlUtils , jointUtils , hierarchyUtils , vectorUtils



class Foot(chain.Chain) :
	
	
	
	def __init__(self , side , name , joint_number = 3 , length = 6 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		self.length = length
		# 整理命名规范的列表
		self.parts = ['Ankle' , 'Ball' , 'Toe']
		self.rvs_jnt_parts = ['Heel' , 'Tiptoe' , 'Inn' , 'Out']
		self.rvs_bpjnt_list = list()
		self.rvs_jnt_list = list()
		self.rvs_ctrl_list = list()
		self.rvs_output_list = list()
		
		self.joint_number = joint_number
		self.value = length / joint_number
		self.radius = 3
		# 初始化foot的ik和fk系统
		self.foot_fk = chainFK.ChainFK(self.side , self.name , self.joint_number ,
		                               direction = [0 , 0 , -1] ,
		                               length = self.length ,
		                               joint_parent = self.joint_parent , control_parent = self.control_parent)
		self.foot_ik = chainIK.ChainIK(self.side , self.name , self.joint_number , direction = [0 , 0 , -1] ,
		                               length = self.length ,
		                               joint_parent = self.joint_parent , control_parent = self.control_parent)
		# 设置foot_fk的基础属性,控制器大小，前缀和控制器朝向
		self.foot_fk._rtype = 'footFK'
		self.foot_fk.axis = 'X+'
		self.foot_fk.radius = 2
		# 设置foot_ik的基础属性,控制器形状，前缀
		self.foot_ik._rtype = 'footIK'
		self.foot_ik.set_shape('cube')
		self.foot_ik.radius = 2
	
	
	
	def create_namespace(self) :
		u"""
		创建名称规范整理
		"""
		# 创建脚部ik和fk的命名规范
		self.foot_fk.create_namespace()
		self.foot_ik.create_namespace()
		for part in self.parts :
			self.bpjnt_list.append('bpjnt_{}_{}{}_001'.format(self._side , self._name , part))
			self.jnt_list.append('jnt_{}_{}{}_001'.format(self._side , self._name , part))
			self.zero_list.append('zero_{}_{}{}_001'.format(self._side , self._name , part))
			self.driven_list.append('driven_{}_{}{}_001'.format(self._side , self._name , part))
			self.ctrl_list.append('ctrl_{}_{}{}_001'.format(self._side , self._name , part))
			self.output_list.append('output_{}_{}{}_001'.format(self._side , self._name , part))
		self.ctrl_grp = ('grp_{}_{}{}_001'.format(self._side , self._name , self._rtype))
		# 创建用来定位旋转轴心点的关节
		for part in self.rvs_jnt_parts :
			self.rvs_bpjnt_list.append('bpjnt_{}_{}{}_001'.format(self._side , self._name , part))
			self.rvs_jnt_list.append('jnt_{}_{}{}_001'.format(self._side , self._name , part))
			self.rvs_ctrl_list.append('ctrl_{}_{}{}_001'.format(self._side , self._name , part))
			self.rvs_output_list.append('output_{}_{}{}_001'.format(self._side , self._name , part))
		
		self.heel_bpjnt = ('bpjnt_{}_{}Heel_001'.format(self._side , self._name))
		self.tiptoe_bpjnt = ('bpjnt_{}_{}Tiptoe_001'.format(self._side , self._name))
		self.inn_bpjnt = ('bpjnt_{}_{}Inn_001'.format(self._side , self._name))
		self.out_bpjnt = ('bpjnt_{}_{}Out_001'.format(self._side , self._name))
		
		# 创建 IKhandle 的名称规范
		self.ball_ikhandle = self.jnt_list[1].replace('jnt' , 'ikhandle')
		self.toe_ikhandle = self.jnt_list[-1].replace('jnt' , 'ikhandle')
		#创建整体的控制器层级组
		self.ctrl_grp = ('grp_{}_{}{}_001'.format(self._side , self._name , self._rtype))
	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		# 创建脚部的fk，ik关节
		self.foot_fk.create_bpjnt()
		self.foot_ik.create_bpjnt()
		# 设置脚部的fk，ik关节的可见性
		cmds.setAttr(self.foot_fk.bpjnt_list[0] + '.v' , 0)
		cmds.setAttr(self.foot_ik.bpjnt_list[0] + '.v' , 0)
		# 创建用来混合的关节
		for index , bpjnt in enumerate(self.bpjnt_list) :
			self.bpjnt = cmds.createNode('joint' , name = bpjnt , parent = self.joint_parent)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.bpjnt
			# 调整距离
			cmds.setAttr(self.bpjnt + '.translate' , 0 , 0 , self.value)
			# 约束ik定位的关节链
			cmds.parentConstraint(self.bpjnt , self.foot_ik.bpjnt_list[index] , mo = False)
			
			# 约束fk定位的关节链
			cmds.parentConstraint(self.bpjnt , self.foot_fk.bpjnt_list[index] , mo = False)
		
		cmds.setAttr(self.bpjnt_list[0] + '.translate' , self.value * self.side_value , self.value , 0)
		# 创建用来定位ik旋转轴心点的关节
		for rvs_jnt in self.rvs_bpjnt_list :
			self.rvs_jnt = cmds.createNode('joint' , name = rvs_jnt)
		# 进行关节定向
		jointUtils.Joint.joint_orientation(self.rvs_bpjnt_list)
		
		# 设置定位旋转轴心点的关节的位置
		cmds.setAttr(self.tiptoe_bpjnt + '.translate' , self.value * self.side_value , 0 , self.value * 2)
		cmds.setAttr(self.heel_bpjnt + '.translate' , self.value * self.side_value , 0 , 0)
		cmds.setAttr(self.inn_bpjnt + '.translate' , 0 , 0 , self.value)
		cmds.setAttr(self.out_bpjnt + '.translate' , self.value * 2 * self.side_value , 0 , self.value)
	
	
	
	def create_joint(self) :
		super().create_joint()
		
		# 创建脚部的fk，ik关节
		self.foot_fk.create_joint()
		self.foot_ik.create_joint()
		# 设置脚部的fk，ik关节的可见性
		cmds.setAttr(self.foot_fk.jnt_list[0] + '.v' , 0)
		cmds.setAttr(self.foot_ik.jnt_list[0] + '.v' , 0)
		for fk_jnt , ik_jnt , jnt in zip(self.foot_fk.jnt_list , self.foot_ik.jnt_list , self.jnt_list) :
			# 吸附对应的关节位置
			cmds.delete(cmds.parentConstraint(jnt , fk_jnt , mo = False))
			cmds.delete(cmds.parentConstraint(jnt , ik_jnt , mo = False))
			# fk和ik关节约束jnt关节
			cmds.parentConstraint(fk_jnt , ik_jnt , jnt)
		
		# 创建用来定位ik旋转轴心点的关节
		parent = self.foot_ik.jnt_list[-1]
		for rvs_bpjnt in self.rvs_bpjnt_list :
			self.jnt = cmds.createNode('joint' , name = rvs_bpjnt.replace('bpjnt' , 'jnt') , parent =
			parent)
			cmds.matchTransform(self.jnt , rvs_bpjnt)
			cmds.delete(rvs_bpjnt)
			parent = self.jnt
	
	
	
	def build_ikSingle(self) :
		u'''
		创建ikSingle的绑定系统
		'''
		self.ball_ikhandle = cmds.ikHandle(name = 'ball_ikhandle' , startJoint = self.foot_ik.jnt_list[0] ,
		                                   endEffector = self.foot_ik.jnt_list[1] ,
		                                   sticky = 'sticky' , solver = 'ikSCsolver' , setupForRPsolver = True)[0]
		
		self.toe_ikhandle = cmds.ikHandle(name = 'ball_ikhandle' , startJoint = self.foot_ik.jnt_list[1] ,
		                                  endEffector = self.foot_ik.jnt_list[2] ,
		                                  sticky = 'sticky' , solver = 'ikSCsolver' , setupForRPsolver = True)[0]
	
	
	
	def add_footik_ctrl(self) :
		"""
		添加footik的控制
		heelSide:脚跟滑动
		heelRoll:脚跟翻转
		ballRoll:脚掌翻转
		toeSide:脚尖滑动
		toeRoll:脚尖翻转
		toeTap:抬脚尖
		heelTap:抬脚跟
		toeLeft:
		toeStraight:
		"""
		ankle_ik_ctrl = self.foot_ik.ctrl_list[0]
		# 需要添加到ik控制器上的属性控制
		footik_attrs_list = ['toeTap' , 'heelTap' , 'toeRoll' , 'heelRoll' , 'toeSide' , 'heelSide' ,
		                     'toeLeft' ,
		                     'toeStraight']
		cmds.addAttr(ankle_ik_ctrl , ln = 'footIKCtrl' , nn = 'footIKCtrl--------' , at = 'bool' , k = 1)
		for attr in footik_attrs_list :
			cmds.addAttr(ankle_ik_ctrl , sn = attr , at = 'double' , dv = 0 , min = -100 , max = 100 ,
			             k = 1)
		
		# 连接属性控制
		# 在ankleIK控制器上连接对应的脚部控制开关
		cmds.connectAttr(ankle_ik_ctrl + '.toeTap' , self.tiptoe_bpjnt.replace('bpjnt' , 'connect') + '.rotateX')
		cmds.connectAttr(ankle_ik_ctrl + '.heelTap' , self.heel_bpjnt.replace('bpjnt' , 'connect') + '.rotateX')
		
		cmds.connectAttr(ankle_ik_ctrl + '.toeRoll' , self.tiptoe_bpjnt.replace('bpjnt' , 'connect') + '.rotateZ')
		cmds.connectAttr(ankle_ik_ctrl + '.heelRoll' , self.heel_bpjnt.replace('bpjnt' , 'connect') + '.rotateZ')
		
		cmds.connectAttr(ankle_ik_ctrl + '.toeSide' , self.tiptoe_bpjnt.replace('bpjnt' , 'connect') + '.rotateY')
		cmds.connectAttr(ankle_ik_ctrl + '.heelSide' , self.heel_bpjnt.replace('bpjnt' , 'connect') + '.rotateY')
	
	
	
	def create_ctrl(self) :
		# 创建整体的控制器层级组
		self.ctrl_grp = cmds.createNode('transform' , name = self.ctrl_grp , parent = self.control_parent)
		
		# 创建脚部的fk，ik控制器
		self.foot_fk.create_ctrl()
		self.foot_ik.create_ctrl()
		# 创建用来定位ik旋转轴心点的控制器
		parent = self.foot_ik.output_list[0]
		for rvs_bpjnt in self.rvs_bpjnt_list :
			rvs_ctrl = controlUtils.Control.create_ctrl(rvs_bpjnt.replace('bpjnt' , 'ctrl') , shape = 'ball' ,
			                                            radius = self.radius * 0.5 ,
			                                            axis = 'X+' , pos = rvs_bpjnt.replace('bpjnt' , 'jnt') ,
			                                            parent = parent)
			parent = rvs_ctrl.replace('ctrl' , 'output')
			
		# 添加ik控制器的footik控制
		self.add_footik_ctrl()
		
		# 整理IK控制器的层级结构
		cmds.parent(self.foot_ik.zero_list[1] , self.foot_ik.zero_list[-1] ,
		            self.rvs_bpjnt_list[-1].replace('bpjnt' , 'output'))
		cmds.parent(self.foot_ik.zero_list[0], self.ctrl_grp)
		

		
		# 整理FK控制器的层级结构
		cmds.parent(self.foot_fk.zero_list[0] , self.ctrl_grp)
		
		# 创建用于ikfk切换的控制器
		self.ctrl = controlUtils.Control.create_ctrl(self.ctrl_list[0] , shape = 'pPlatonic' ,
		                                             radius = self.radius * 1.2 ,
		                                             axis = 'X+', pos = self.jnt_list[0] ,
		                                             parent = self.ctrl_grp)
		cmds.setAttr(self.zero_list[0] + '.translateX' , 5 * self.side_value)
		# 添加IKFK切换的属性
		cmds.addAttr(self.ctrl , sn = 'Switch' , ln = 'ikfkSwitch' , at = 'double' , dv = 1 , min = 0 , max = 1 ,
		             k = 1)
		
	
	
	def add_constraint(self) :
		u"""
		添加控制器的约束
		"""
		# fk的关节控制器添加约束
		self.foot_fk.add_constraint()
		
		# ik的关节控制器添加约束
		# 创建ikhandle
		self.build_ikSingle()
		cmds.parent(self.ball_ikhandle , self.foot_ik.output_list[1])
		cmds.parent(self.toe_ikhandle , self.foot_ik.output_list[-1])
		
		# 用来定位ik旋转轴心点的控制器约束对应的关节
		for index , jnt in enumerate(self.rvs_jnt_list) :
			cmds.parentConstraint(self.rvs_output_list[index] , jnt)
			
			# IK关节链，FK关节链来约束IKFK关节链
			for joint_number in range(self.joint_number) :
				cons = cmds.parentConstraint(
						self.foot_ik.jnt_list[joint_number] ,
						self.foot_fk.jnt_list[joint_number] ,
						self.jnt_list[joint_number])[0]
				# 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
				cmds.setDrivenKeyframe(
						'{}.w0'.format(cons) , cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 1)
				cmds.setDrivenKeyframe(
						'{}.w1'.format(cons) , cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 0)
				cmds.setDrivenKeyframe(
						'{}.w0'.format(cons) , cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 0)
				cmds.setDrivenKeyframe(
						'{}.w1'.format(cons) , cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 1)
				
				cmds.setDrivenKeyframe(self.foot_ik.ctrl_list[joint_number] + '.v' ,
				                       cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 1)
				cmds.setDrivenKeyframe(self.foot_ik.ctrl_list[joint_number] + '.v' ,
				                       cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 0)
				cmds.setDrivenKeyframe(self.foot_fk.ctrl_list[joint_number] + '.v' ,
				                       cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 1)
				cmds.setDrivenKeyframe(self.foot_fk.ctrl_list[joint_number] + '.v' ,
				                       cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 0)
	
	
	
	def build_rig(self) :
		super().build_rig()
