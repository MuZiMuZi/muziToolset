from importlib import reload

import maya.cmds as cmds
from . import foot
from ...module.base import base
from ...module.limb import limbIKFK




reload(foot)
reload(limbIKFK)



class Leg(base.Base) :
	
	
	
	def __init__(self , side , name , jnt_number = 3 , direction = [0 , -1 , 0] , is_stretch = 1 , length = 15 ,
	             limbtype = 'leg' ,
	             jnt_parent = None , control_parent = None) :
		super().__init__(side , name , jnt_number , direction , is_stretch , length , limbtype , jnt_parent ,
		                 control_parent)
		self._side = side
		self._name = name
		self._rtype = 'Leg'
		self.axis = 'Z+'
		# 初始化脚掌的模块
		self.foot_limb = foot.Foot(side , name , jnt_number = 3 , length = 6 , jnt_parent = None ,
		                           control_parent = None)
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		self.foot_limb.create_namespace()
	
	
	
	def create_bpjnt(self) :
		super().create_namespace()
		self.foot_limb.create_bpjnt()
	
	
	
	def create_joint(self) :
		super().create_namespace()
		self.foot_limb.create_joint()
	
	
	
	def create_ctrl(self) :
		super().create_namespace()
		self.foot_limb.create_ctrl()
	
	
	def add_constraint(self) :
		super().create_namespace()
		self.foot_limb.add_constraint()
		
		# 脚部关节对脚掌的控制器组做约束
		cmds.parentConstraint(self.leg_limb.jnt_list[-1] , self.foot_limb.ctrl_grp , mo = True)



if __name__ == '__main__' :
	def build_setup() :
		leg_l = leg.Leg(side = 'l' , name = 'zz' , jnt_number = 3 , direction = [0 , -1 , 0] , length = 10 ,
		                is_stretch = 1 , jnt_parent = None ,
		                control_parent = None)
		leg_l.build_setup()
	
	
	
	def build_rig() :
		leg_l = leg.Leg(side = 'l' , name = 'zz' , jnt_number = 3 , direction = [0 , -1 , 0] , length = 10 ,
		                is_stretch = 1 , jnt_parent = None ,
		                control_parent = None)
		leg_l.build_rig()
	
	
	
	#
	#
	build_setup()
	build_rig()
