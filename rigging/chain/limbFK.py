from . import chain , chainIK , chainFK
import maya.cmds as cmds
from ...core import pipelineUtils , vectorUtils



class LimbFK(chainFK.ChainFK) :
	u"""
	创建手臂或者是腿部的四肢关节的FK绑定
	"""
	
	
	
	def __init__(self , side , name , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 , joint_parent = None ,
	             control_parent = None) :
		super().__init__(side , name , joint_number , direction , length , joint_parent , control_parent)
		self._rtype =''
	
	

if __name__ == '__main__':
	def build_setup() :
		custom = limbFK.LimbFK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
		                       joint_parent = None ,
		                       control_parent = None)
		custom.build_setup()
	
	
	
	def build_rig() :
		custom = limbFK.LimbFK(side = 'l' , name = 'zz' , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 ,
		                       joint_parent = None ,
		                       control_parent = None)
		custom.build_rig()
	
	
	
	build_setup()
	build_rig()
