import maya.cmds as cmds

from . import hand
from ..chain import limbIKFK



class Arm(limbIKFK.LimbIKFK) :
	
	
	
	def __init__(self , side , name , joint_number = 3 , direction = [-1 , 0 , 0] , is_stretch = 1 , length = 15 ,
	             limbtype = 'arm' ,
	             joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , direction , is_stretch , length , limbtype , joint_parent ,
		                 control_parent)
		self._rtype = 'Arm'
		
		# 初始化手指的模块
		self.hand_limb = hand.Hand(side , name , joint_number , direction , length = 3 ,
		                           joint_parent = None ,
		                           control_parent = None)
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		self.hand_limb.create_namespace()
	
	
	
	def create_bpjnt(self) :
		super().create_bpjnt()
		self.hand_limb.create_bpjnt()
	
	
	
	def create_joint(self) :
		super().create_joint()
		self.hand_limb.create_joint()
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		self.hand_limb.create_ctrl()
	
	
	
	def add_constraint(self) :
		super().add_constraint()
		self.hand_limb.add_constraint()
		
		# 手部关节对手指的控制器组做约束
		cmds.pointConstraint(self.jnt_list[-1] , self.hand_limb.finger_grp , mo = True)



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
