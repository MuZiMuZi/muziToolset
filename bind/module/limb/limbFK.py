from importlib import reload
from ....core import controlUtils , hierarchyUtils , pipelineUtils , jointUtils
from ..chain import chainFK
import maya.cmds as cmds
reload(chainFK)





class LimbFK(chainFK.ChainFK) :
	
	
	
	def __init__(self , side , name , joint_number = 3 , direction = [-1 , 0 , 0] , length = 10 , joint_parent = None ,
	             control_parent = None) :
		u"""
		创建手臂或者是腿部的四肢关节的FK绑定
		limbtype(str):给定的limbtype 是手臂还是腿部
		"""
		super().__init__(side , name , joint_number , direction , length , joint_parent , control_parent)
		self._rtype = 'LimbFK'
	
	
	

	
	
	
	def create_joint(self) :
		super().create_joint()
		# 隐藏bp的定位关节
		cmds.setAttr(self.bpjnt_list[0] + '.visibility' , 0)


if __name__ == '__main__' :
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
