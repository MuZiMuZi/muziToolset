# coding=utf-8
'''
眉毛的绑定系统创建
'''
import os
from importlib import reload



import maya.cmds as cmds

from ....core import controlUtils , pipelineUtils
from ...base import base



reload(pipelineUtils)
reload(base)


class Brow(base.Base) :
	
	
	
	def __init__(self , side = '' , name = '' , joint_number = 1 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , joint_parent , control_parent)
		self.radius = 0.25
		self.shape = 'ball'
		self._rtype = 'Brow'
		
		# 创建两边的眉毛系统
		self.brow_l = base.Base(side = 'l' , name = '' , joint_number = 4 , joint_parent = None , control_parent =
		None)
		self.brow_l._rtype = 'Brow'
		self.brow_l.shape = 'cube'
		self.brow_l.radius = 0.1
		
		self.brow_r = base.Base(side = 'r' , name = '' , joint_number = 4 , joint_parent = None , control_parent =
		None)
		self.brow_r._rtype = 'Brow'
		self.brow_r.shape = 'cube'
		self.brow_r.radius = 0.1
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		# 创建两边的眉毛名称规范
		self.brow_l.create_namespace()
		self.brow_r.create_namespace()
		# 创建左边的眉毛曲线和曲面名称
		self.brow_l.drive_crv = self.brow_l.bpjnt_list[0].replace('bpjnt' , 'crv')
		self.brow_l.drive_suf = self.brow_l.bpjnt_list[0].replace('bpjnt' , 'suf')
		# 创建左边的眉毛的整体控制器
		self.brow_l.master_ctrl = ('ctrl_{}_{}{}Master_001'.format('l' , self._name , self._rtype))
		
		# 创建右边的眉毛曲线和曲面名称
		self.brow_r.drive_crv = self.brow_r.bpjnt_list[0].replace('bpjnt' , 'crv')
		self.brow_r.drive_suf = self.brow_r.bpjnt_list[0].replace('bpjnt' , 'suf')
		self.brow_r.master_ctrl = ('ctrl_{}_{}{}Master_001'.format('r' , self._name , self._rtype))
	
	
	
	def create_bpjnt(self) :
		# 获得brow_bpjnt 的路径
		self.brow_bpjnt_path = os.path.abspath(__file__ + "/../../../bpjnt/brow_bpjnt.ma")
		# 导入关节
		cmds.file(self.brow_bpjnt_path , i = True , rnn = True)
	
	
	
	def create_suf(self) :
		u"""
		创建用于眉毛部位的曲面
		"""
		
		# 创建左边的bp定位眉毛曲线
		self.brow_l.drive_crv = pipelineUtils.Pipeline.create_curve_on_joints(self.brow_l.bpjnt_list ,
		                                                                      self.brow_l.drive_crv , degree = 3
		                                                                      )
		# 放样曲线出曲面
		# 通过两条曲线来放样制作左边眉毛的曲面
		self.brow_l.drive_suf = pipelineUtils.Pipeline.create_surface_on_curve(self.brow_l.drive_crv ,
		                                                                       self.brow_l.drive_suf , spans = 6 ,
		                                                                       offset = 0.1)
		
		# 创建右边的bp定位眉毛曲线
		self.brow_r.drive_crv = pipelineUtils.Pipeline.create_curve_on_joints(self.brow_r.bpjnt_list ,
		                                                                      self.brow_r.drive_crv , degree = 3
		                                                                      )
		# 放样曲线出曲面
		# 通过两条曲线来放样制作右边眉毛的曲面
		self.brow_r.drive_suf = pipelineUtils.Pipeline.create_surface_on_curve(self.brow_r.drive_crv ,
		                                                                       self.brow_r.drive_suf , spans = 6 ,
		                                                                       offset = 0.1)
	
	
	
	def create_joint(self) :
		super().create_joint()
		
		# 创建眉毛右边的关节
		self.brow_r.create_joint()
		# 右边的关节对曲面进行蒙皮
		cmds.skinCluster(self.brow_r.jnt_list , self.brow_r.drive_suf , tsb = True)
		
		# 创建眉毛左边的关节
		self.brow_l.create_joint()
		
		# 左边的关节对曲面进行蒙皮
		cmds.skinCluster(self.brow_l.jnt_list , self.brow_l.drive_suf , tsb = True)
		
		# 设置关节的可见性
		for jnt in self.brow_l.jnt_list + self.brow_r.jnt_list :
			cmds.setAttr(jnt + '.v' , 0)
	
	
	
	def create_folice(self) :
		u"""
		对曲面创建毛囊，并且创建权重的关节
		"""
		# 创建左边的曲面上的毛囊和权重关节
		self.brow_l.follicle_dict = pipelineUtils.Pipeline.create_joint_follicle_on_surface(self.brow_l.drive_suf ,
		                                                                                    self.brow_l.side ,
		                                                                                    self.brow_l._rtype ,
		                                                                                    joint_number = 6)
		
		# 创建右边的曲面上的毛囊和权重关节
		self.brow_r.follicle_dict = pipelineUtils.Pipeline.create_joint_follicle_on_surface(self.brow_r.drive_suf ,
		                                                                                    self.brow_r.side ,
		                                                                                    self.brow_r._rtype ,
		                                                                                    joint_number = 6)
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		# 创建眉毛右边的控制器
		# 创建眉毛右边的整体控制器
		self.brow_l.master_ctrl = controlUtils.Control.create_ctrl(self.brow_l.master_ctrl , shape = 'square' ,
		                                                           radius = 0.25 ,
		                                                           axis = 'X+' , pos = self.brow_l.jnt_list[1] ,
		                                                           parent = self.control_parent)
		self.brow_l.create_ctrl()
		# 整理眉毛左边的控制器层级结构
		cmds.parent(self.brow_l.drive_suf , self.brow_l.ctrl_grp)
		cmds.parent(self.brow_l.master_ctrl.replace('ctrl' , 'zero') , self.brow_l.ctrl_grp)
		cmds.parent(self.brow_l.follicle_dict['deform_grp'] , self.brow_l.ctrl_grp)
		
		# 创建眉毛左边的控制器
		# 创建眉毛右边的整体控制器
		self.brow_r.master_ctrl = controlUtils.Control.create_ctrl(self.brow_r.master_ctrl , shape = 'square' ,
		                                                           radius = 0.25 ,
		                                                           axis = 'X+' , pos = self.brow_r.jnt_list[1] ,
		                                                           parent = self.control_parent)
		self.brow_r.create_ctrl()
		# 整理眉毛右边的控制器层级结构
		cmds.parent(self.brow_r.drive_suf , self.brow_r.ctrl_grp)
		cmds.parent(self.brow_r.master_ctrl.replace('ctrl' , 'zero') , self.brow_r.ctrl_grp)
		cmds.parent(self.brow_r.follicle_dict['deform_grp'] , self.brow_r.ctrl_grp)
		
		# 整体控制器添加属性
		for ctrl in [self.brow_l.master_ctrl , self.brow_r.master_ctrl] :
			cmds.addAttr(ctrl , ln = 'BrowCtrlsVis' , dv = 0 , at = 'bool' , k = 1)
			cmds.addAttr(ctrl , ln = 'FollowValue' , nn = 'FollowValue---------' , dv = 0 , at = 'bool' ,
			             hidden = False , k = 0)
			for index in range(4) :
				cmds.addAttr(ctrl , ln = 'Follow{:02d}'.format(index) , dv = 1 - 0.25 * index , at = 'float' ,
				             min = 0 ,
				             max = 1 , k = 1)
	
	
	
	def add_constraint(self) :
		super().add_constraint()
		self.brow_l.add_constraint()
		self.brow_r.add_constraint()
		
		# 左右两边的眉毛控制器约束中间眉心的控制器
		brow_l_output = self.brow_l.output_list[0]
		brow_r_output = self.brow_r.output_list[0]
		
		cmds.parentConstraint(brow_l_output , brow_r_output , self.driven_list[0] , mo = True)
		
		# 左边眉毛的整体控制器连接子级控制器
		self.create_connect(self.brow_l.master_ctrl , self.brow_l.connect_list)
		# 左边眉毛的整体控制器连接子级控制器的显示
		cmds.connectAttr(self.brow_l.master_ctrl + '.BrowCtrlsVis' ,
		                 self.brow_l.follicle_dict['ctrl_grp'] + '.visibility')
		
		# 右边眉毛的整体控制器连接子级控制器
		self.create_connect(self.brow_r.master_ctrl , self.brow_r.connect_list)
		# 右边眉毛的整体控制器连接子级控制器的显示
		cmds.connectAttr(self.brow_r.master_ctrl + '.BrowCtrlsVis' ,
		                 self.brow_r.follicle_dict['ctrl_grp'] + '.visibility')
	
	
	
	def create_connect(self , driver , driven) :
		u"""
		创建眉毛整体控制器与子级控制器的连接,连接控制器显示和跟随的值
		driver：驱动者
		driven：被驱动者
		"""
		for index in range(4) :
			# 创建位移的乘除节点
			trans_node = cmds.createNode('multiplyDivide' ,
			                             name = driven[index].replace('connect' , 'trans'))
			cmds.connectAttr(driver + '.translate' , trans_node + '.input1')
			for axis in ['X' , 'Y' , 'Z'] :
				cmds.connectAttr(driver + '.Follow{:02d}'.format(index) , trans_node + '.input2{}'.format(axis))
			cmds.connectAttr(trans_node + '.output' , driven[index] + '.translate')
			# 创建旋转的乘除节点
			rotate_node = cmds.createNode('multiplyDivide' ,
			                              name = driven[index].replace('connect' , 'rotate'))
			cmds.connectAttr(driver + '.rotate' , rotate_node + '.input1')
			for axis in ['X' , 'Y' , 'Z'] :
				cmds.connectAttr(driver + '.Follow{:02d}'.format(index) , rotate_node + '.input2{}'.format(axis))
			cmds.connectAttr(rotate_node + '.output' , driven[index] + '.rotate')
	
	
	
	def build_rig(self) :
		"""
		创建绑定系统
		"""
		self.create_namespace()
		self.create_suf()
		self.create_joint()
		self.create_folice()
		self.create_ctrl()
		self.add_constraint()



if __name__ == "__main__" :
	def build_setup() :
		brow_m = brow.Brow(side = 'm' , joint_parent = None , control_parent = None)
		brow_m.build_setup()
	
	
	
	def build_rig() :
		brow_m = brow.Brow(side = 'm' , joint_parent = None , control_parent = None)
		brow_m.build_rig()
	
	
	
	build_setup()
	build_rig()
