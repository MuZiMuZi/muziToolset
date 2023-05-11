import maya.cmds as cmds

from . import chain , chainFK , chainIK
from ..base import bone
from ...core import vectorUtils , controlUtils
from importlib import reload



reload(chainFK)
reload(chainIK)



class ChainIKFK(chain.Chain) :
	u'''
	创建ikfk的关节链条的绑定系统
	由三条关节链组成，ik关节链条，fk关节链条和ikfk关节链条组成
	'''
	
	
	
	def __init__(self , side , name , joint_nuber , direction , is_stretch = 1 , length = 10 , joint_parent = None ,
	             control_parent = None) :
		chain.Chain.__init__(self , side , name , joint_nuber , length , joint_parent , control_parent)
		
		# 初始化ik关节链条和fk关节链条
		self.ik_chain = chainIK.ChainIK(side , name , joint_nuber , direction , length , is_stretch)
		self.fk_chain = chainFK.ChainFK(side , name , joint_nuber , direction , length)
		
		self._rtype = 'chainIKFK'
		self.radius = 6
		# 获取初始的位置
		self.interval = length / (self.joint_nuber - 1)
		self.direction = list(vectorUtils.Vector(direction).mult_interval(self.interval))
		self.is_stretch = is_stretch
		self.axis = vectorUtils.Vector(direction).axis
	
	
	
	def create_bpjnt(self) :
		super().create_bpjnt()
		
		# 创建ik关节链条和fk关节链条的定位关节
		self.ik_chain.create_bpjnt()
		self.fk_chain.create_bpjnt()
	
	
	
	def create_namespace(self) :
		u"""
			创建名称进行规范整理
			"""
		super().create_namespace()
		# 初始化ik关节链条和fk关节链条的命名规范
		self.ik_chain.create_namespace()
		self.fk_chain.create_namespace()
	
	
	
	def create_joint(self) :
		'''
		根据定位的bp关节创建关节
		'''
		# 创建ik关节链条和fk关节链条的关节
		self.ik_chain.create_joint()
		self.fk_chain.create_joint()
		
		# 创建ikfk的关节
		cmds.select(clear = True)
		for joint_nuber , bpjnt in enumerate(self.bpjnt_list) :
			pos = cmds.xform(bpjnt , q = 1 , t = 1 , ws = 1)
			cmds.joint(p = pos , name = self.jnt_list[joint_nuber])
		
		cmds.delete(self.bpjnt_list[0])
		# 设置ik关节链条和fk关节链条的可见性
		cmds.setAttr(self.ik_chain.jnt_list[0] + '.v' , 0)
		cmds.setAttr(self.fk_chain.jnt_list[0] + '.v' , 0)
		
		cmds.parent(self.jnt_list[0] , self.joint_parent)
	
	
	
	def create_ctrl(self) :
		u'''
		创建控制器绑定
		'''
		self.ik_chain.create_ctrl()
		self.fk_chain.create_ctrl()
		
		# 创建用于ikfk切换的控制器
		self.ctrl = controlUtils.Control.create_ctrl(self.ctrl_list[0] , shape = 'cube' ,
		                                             radius = self.radius ,
		                                             axis = self.axis , pos = self.jnt_list[0] ,
		                                             parent = self.control_parent)
		
		# 添加IKFK切换的属性
		cmds.addAttr(self.ctrl , sn = 'Switch' , ln = 'ikfkSwitch' , at = 'double' , dv = 1 , min = 0 , max = 1 ,
		             k = 1)
		
		# 整理层级结构
		cmds.parent(self.ik_chain.zero_list[0] , self.output_list[0])
		cmds.parent(self.fk_chain.zero_list[0] , self.output_list[0])
	
	
	
	def add_constraint(self) :
		'''
		添加约束,ikfk关节链的约束比较特别，需要连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
		'''
		self.ik_chain.add_constraint()
		self.fk_chain.add_constraint()
		
		# IK关节链，FK关节链来约束IKFK关节链
		for joint_nuber in range(self.joint_nuber) :
			cons = cmds.parentConstraint(
					self.ik_chain.jnt_list[joint_nuber] ,
					self.fk_chain.jnt_list[joint_nuber] ,
					self.jnt_list[joint_nuber])[0]
			# 连接IKFK切换的属性做驱动关键帧来驱动不同的关节链条
			cmds.setDrivenKeyframe(
					'{}.w0'.format(cons) , cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 1)
			cmds.setDrivenKeyframe(
					'{}.w1'.format(cons) , cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 0)
			cmds.setDrivenKeyframe(
					'{}.w0'.format(cons) , cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 0)
			cmds.setDrivenKeyframe(
					'{}.w1'.format(cons) , cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 1)
			
			cmds.setDrivenKeyframe(self.ik_chain.ctrl_list[joint_nuber] + '.v' ,
			                       cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 1)
			cmds.setDrivenKeyframe(self.ik_chain.ctrl_list[joint_nuber] + '.v' ,
			                       cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 0)
			cmds.setDrivenKeyframe(self.fk_chain.ctrl_list[joint_nuber] + '.v' ,
			                       cd = self.ctrl_list[0] + '.Switch' , dv = 0 , v = 1)
			cmds.setDrivenKeyframe(self.fk_chain.ctrl_list[joint_nuber] + '.v' ,
			                       cd = self.ctrl_list[0] + '.Switch' , dv = 1 , v = 0)



if __name__ == '__main__' :
	def x() :
		custom = chainIKFK.ChainIKFK(side = 'l' , name = 'zz' , joint_nuber = 5 , direction = [1 , 0 , 0] ,
		                             joint_parent = None , control_parent = None)
		custom.build_setup()
	
	
	
	def y() :
		custom = chainIKFK.ChainIKFK(side = 'l' , name = 'zz' , joint_nuber = 5 , direction = [1 , 0 , 0] ,
		                             joint_parent = None , control_parent = None)
		custom.build_rig()



# x()
# y()