from importlib import reload

import maya.cmds as cmds

from ....core import controlUtils , jointUtils , pipelineUtils
from ..chain import chainIKFK
from ..limb import limbFK , limbIK



reload(limbFK)
reload(limbIK)
reload(chainIKFK)



class LimbIKFK(chainIKFK.ChainIKFK) :
	u'''
	创建手臂或者是腿部的四肢关节的绑定系统
	由三条关节链组成，ik关节链条，fk关节链条和ikfk关节链条组成
	'''
	
	
	
	def __init__(self , side , name , joint_number , direction , is_stretch = 1 , length = 10 , limbtype = None ,
	             joint_parent = None ,
	             control_parent = None) :
		super().__init__(side , name , joint_number , direction , is_stretch , length , joint_parent , control_parent)
		
		self._rtype = 'LimbIKFK'
		joint_number = 3
		# 判断给定的limbtype 是手臂还是腿部
		if limbtype == 'arm' :
			self.z_value = 1
		else :
			self.z_value = -1
		
		# 判断边为'l'还是'r'
		if side == 'l' :
			self.side_value = 1
		else :
			self.side_value = -1
		
		self.radius = 5
		
		# 初始化ik关节链条和fk关节链条
		self.ik_limb = limbIK.LimbIK(side , name , joint_number , direction , length , is_stretch , limbtype)
		self.fk_limb = limbFK.LimbFK(side , name , joint_number , direction , length)
	
	
	
	def create_namespace(self) :
		u"""
			创建名称进行规范整理
			"""
		super().create_namespace()
		# 初始化ik关节链条和fk关节链条的命名规范
		self.ik_limb.create_namespace()
		self.fk_limb.create_namespace()
	
	
	
	def create_bpjnt(self) :
		"""
		创建定位的bp关节
		"""
		for bpjnt in self.bpjnt_list :
			self.bpjnt = cmds.createNode('joint' , name = bpjnt , parent = self.joint_parent)
			# 指定关节的父层级为上一轮创建出来的关节
			self.joint_parent = self.bpjnt
			# 调整距离
			pipelineUtils.Pipeline.move(obj = self.bpjnt , pos = self.direction)
		
		# 创建ik关节链条和fk关节链条的定位关节
		self.ik_limb.create_bpjnt()
		self.fk_limb.create_bpjnt()
		
		# 设置ik关节链条和fk关节链条的定位关节的显示
		cmds.setAttr(self.ik_limb.bpjnt_list[0] + '.v' , 0)
		cmds.setAttr(self.fk_limb.bpjnt_list[0] + '.v' , 0)
		
		# 设置连接让定位关节驱动ik和fk的关节链条
		for bpjnt , ik_bpjnt , fk_bpjnt in zip(self.bpjnt_list , self.ik_limb.bpjnt_list , self.fk_limb.bpjnt_list) :
			cmds.parentConstraint(bpjnt , ik_bpjnt , mo = False)
			cmds.parentConstraint(bpjnt , fk_bpjnt , mo = False)
		# 创建logging用来记录日志
		self.logger.debug(u'{}_{}  :  BP joint creation completed for positioning'.format(self.name , self.side))
	
	
	
	def create_joint(self) :
		'''
		根据定位的bp关节创建关节
		'''
		# 创建ik关节链条和fk关节链条的关节
		self.ik_limb.create_joint()
		self.fk_limb.create_joint()
		
		# 创建ikfk的关节
		cmds.select(clear = True)
		for joint_number , bpjnt in enumerate(self.bpjnt_list) :
			pos = cmds.xform(bpjnt , q = 1 , t = 1 , ws = 1)
			cmds.joint(p = pos , name = self.jnt_list[joint_number])
		# 进行关节定向
		jointUtils.Joint.joint_orientation(self.jnt_list)
		# 隐藏bp的定位关节
		cmds.setAttr(self.bpjnt_list[0] + '.visibility' , 0)
		# 设置ik关节链条和fk关节链条的可见性
		cmds.setAttr(self.ik_limb.jnt_list[0] + '.v' , 0)
		cmds.setAttr(self.fk_limb.jnt_list[0] + '.v' , 0)
		
		cmds.parent(self.jnt_list[0] , self.joint_parent)
		# 创建logging用来记录日志
		self.logger.debug(u'{}_{}  :  Skin joint creation completed'.format(self.name , self.side))
	
	
	
	def create_ctrl(self) :
		u'''
		创建控制器绑定
		'''
		self.ik_limb.create_ctrl()
		self.fk_limb.create_ctrl()
		
		# 创建整体的控制器层级组
		self.ctrl_grp = cmds.createNode('transform' , name = self.ctrl_grp , parent = self.control_parent)
		# 创建用于ikfk切换的控制器
		self.ctrl = controlUtils.Control.create_ctrl(self.ctrl_list[0] , shape = 'pPlatonic' ,
		                                             radius = self.radius ,
		                                             axis = self.axis , pos = self.jnt_list[0] ,
		                                             parent = self.ctrl_grp)
		cmds.setAttr(self.zero_list[0] + '.translateZ' , -5)
		# 添加IKFK切换的属性
		cmds.addAttr(self.ctrl , sn = 'Switch' , ln = 'ikfkSwitch' , at = 'double' , dv = 1 , min = 0 , max = 1 ,
		             k = 1)
		
		# 整理层级结构
		cmds.parent(self.ik_limb.ctrl_grp , self.output_list[0])
		cmds.parent(self.fk_limb.ctrl_grp , self.output_list[0])
		# 创建logging用来记录日志
		self.logger.debug(u'{}_{}  :  Controller creation completed'.format(self.name , self.side))
	
	
	
	def add_constraint(self) :
		'''
		添加约束,ikfk关节链的约束比较特别，需要连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
		'''
		self.ik_limb.add_constraint()
		self.fk_limb.add_constraint()
		
		# IK关节链，FK关节链来约束IKFK关节链
		for joint_number in range(self.joint_number) :
			cons = cmds.parentConstraint(
					self.ik_limb.jnt_list[joint_number] ,
					self.fk_limb.jnt_list[joint_number] ,
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
			
			# 设置ik关节链条和ik控制器的可见性
			cmds.setDrivenKeyframe(self.ik_limb.ctrl_grp + '.v' ,
			                       cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 1)
			cmds.setDrivenKeyframe(self.ik_limb.ctrl_grp + '.v' ,
			                       cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 0)
			
			# 设置fk关节链条和fk控制器的可见性
			cmds.setDrivenKeyframe(self.fk_limb.ctrl_grp + '.v' ,
			                       cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 1)
			cmds.setDrivenKeyframe(self.fk_limb.ctrl_grp + '.v' ,
			                       cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 0)
		# 创建logging用来记录日志
		self.logger.debug(u'{}_{}  :  Constraint creation completed'.format(self.name , self.side))
	
	
	
	def build_setup(self) :
		super().build_setup()
		# 创建logging用来记录日志
		self.logger.debug('done')
		self.logger.info(
			'{}_{}  :  Create positioning joints for BP and prepare for generation'.format(self.name , self.side))
		self.logger.info('\n')
	
	
	
	def build_rig(self) :
		super().build_rig()
		# 创建logging用来记录日志
		self.logger.debug('done')
		self.logger.info(u'{}_{}  :  Create binding system'.format(self.name , self.side))
		self.logger.info('\n')



if __name__ == '__main__' :
	def build_setup() :
		custom = limbIKFK.LimbIKFK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] ,
		                           length = 10 ,
		                           is_stretch = 1 ,
		                           limbtype = 'arm' ,
		                           joint_parent = None ,
		                           control_parent = None)
		custom.build_setup()
	
	
	
	def build_rig() :
		custom = limbIKFK.LimbIKFK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] ,
		                           length = 10 ,
		                           limbtype = 'arm' ,
		                           joint_parent = None ,
		                           control_parent = None)
		custom.build_rig()
	
	
	
	build_setup()
	build_rig()
