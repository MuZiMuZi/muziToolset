from importlib import reload

import maya.cmds as cmds

from . import foot
from bind.limb import limbIKFK



reload(foot)



class Leg(limbIKFK.LimbIKFK) :
	
	
	
	def __init__(self , side , name , joint_number = 3 , direction = [0 , -1 , 0] , is_stretch = 1 , length = 15 ,
	             limbtype = 'leg' ,
	             joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , direction , is_stretch , length , limbtype , joint_parent ,
		                 control_parent)
		self._rtype = 'Leg'
		self.axis = 'Z+'
		# 初始化脚掌的模块
		self.foot_limb = foot.Foot(side , name , joint_number = 3 , length = 6 , joint_parent = None ,
		                           control_parent = None)
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		self.foot_limb.create_namespace()
		self.ik_handle = ('handle_{}_{}{}_001'.format(self._side , self._name , 'LimbIK'))
	
	
	
	def create_bpjnt(self) :
		super().create_bpjnt()
		self.foot_limb.create_bpjnt()
	
	
	
	def create_joint(self) :
		super().create_joint()
		self.foot_limb.create_joint()
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		self.foot_limb.create_ctrl()
		# 将ikhandle放给脚腕的控制器
		cmds.parent(self.ik_handle , self.foot_limb.foot_ik.output_list[0])
	
	
	
	def add_constraint(self) :
		super().add_constraint()
		self.foot_limb.add_constraint()
		
		# 脚部关节对脚掌的控制器组做约束
		cmds.pointConstraint(self.jnt_list[-1] , self.foot_limb.ctrl_grp , mo = True)



if __name__ == '__main__' :
	def build_setup() :
		arm_l = arm.Arm(side = 'l' , name = 'zz' , joint_number = 3 , direction = [1 , 0 , 0] , length = 10 ,
		                is_stretch = 1 , joint_parent = None ,
		                control_parent = None)
		arm_l.build_setup()
	
	
	
	def build_rig() :
		arm_l = arm.Arm(side = 'l' , name = 'zz' , joint_number = 3 , direction = [1 , 0 , 0] , length = 10 ,
		                is_stretch = 1 , joint_parent = None ,
		                control_parent = None)
		arm_l.build_rig()
	
	
	
	#
	#
	build_setup()
	build_rig()
