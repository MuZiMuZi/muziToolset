from ..base import base , bone
from ..chain import chainFK , chain
from . import finger
import maya.cmds as cmds



class Hand(finger.Finger) :
	
	
	
	def __init__(self , side , name , joint_number = 4 , direction = [-1 , 0 , 0] , length = 3 , joint_parent = None ,
	             control_parent = None) :
		super().__init__(side , name , joint_number , direction , length , joint_parent , control_parent)
		self._rtype = ''
		# 初始化手指的模块
		self.thumb_finger = finger.Finger(self.side , 'thumb' , joint_number = 3 , direction = self.direction ,
		                                  length = self.length , joint_parent = self.joint_parent ,
		                                  control_parent = self.control_parent)
		
		self.index_finger = finger.Finger(self.side , 'index' , joint_number = 4 , direction = self.direction ,
		                                  length = self.length , joint_parent = self.joint_parent ,
		                                  control_parent = self.control_parent)
		
		self.middle_finger = finger.Finger(self.side , 'middle' , joint_number = 4 , direction = self.direction ,
		                                   length = self.length , joint_parent = self.joint_parent ,
		                                   control_parent = self.control_parent)
		
		self.ring_finger = finger.Finger(self.side , 'ring' , joint_number = 4 , direction = self.direction ,
		                                 length = self.length , joint_parent = self.joint_parent ,
		                                 control_parent = self.control_parent)
		
		self.pinky_finger = finger.Finger(self.side , 'pinky' , joint_number = 4 , direction = self.direction ,
		                                  length = self.length , joint_parent = self.joint_parent ,
		                                  control_parent = self.control_parent)
		self.finger_list = [self.thumb_finger , self.index_finger , self.middle_finger , self.ring_finger ,
		                    self.pinky_finger]
	
	
	
	def create_namespace(self) :
		# 创建手指各模块的定位关节
		for finger in self.finger_list :
			finger.create_namespace()
	
	
	
	def create_bpjnt(self) :
		# 创建手指各模块的定位关节
		for index , finger in enumerate(self.finger_list) :
			finger.create_bpjnt()
			# 移动初始关节的位置
			cmds.setAttr(finger.bpjnt_list[0] + '.translateZ' , int(index * 2))
			cmds.setAttr(finger.bpjnt_list[0] + '.translateX' , int(-20 * self.side_value))
	
	
	
	def create_joint(self) :
		# 创建手指各模块的蒙皮关节
		for index , finger in enumerate(self.finger_list) :
			finger.create_joint()
	
	
	
	def create_ctrl(self) :
		# 创建手指各模块的绑定
		for finger in self.finger_list :
			finger.create_ctrl()
	
	
	
	def add_constraint(self) :
		for finger in self.finger_list :
			finger.add_constraint()



if __name__ == '__main__' :
	def build_setup() :
		finger_l = hand.Hand(side = 'l' , name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
		                     joint_parent = None ,
		                     control_parent = None)
		finger_l.build_setup()
	
	
	
	def build_rig() :
		finger_l = hand.Hand(side = 'l' , name = 'zz' , joint_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
		                     joint_parent = None ,
		                     control_parent = None)
		finger_l.build_rig()
	
	
	
	build_setup()
	build_rig()
