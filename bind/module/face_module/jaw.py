# coding=utf-8
'''
下巴的绑定系统创建
'''
import os

import maya.cmds as cmds

from ....core import hierarchyUtils
from ...chain import chainFK



class Jaw(chainFK.ChainFK) :
	
	
	
	def __init__(self , side , name = '' , joint_number = 2 , direction = [-1 , 0 , 0] ,
	             length = 5 , joint_parent = None , control_parent = None) :
		super().__init__(side , name , joint_number , direction , length , joint_parent , control_parent)
		self.shape = 'circle'
		self._rtype = 'Jaw'
		self.radius = 0.4
		
		# 创建用于驱动下巴位移的偏移组
		self.offsetrot_list = list()
		# 创建用于驱动下巴位移的定位器loc
		self.offsetrot_zero = None
		self.offsetrot_loc = None
	
	
	
	def create_namespace(self) :
		super().create_namespace()
		# 创建用于驱动下巴位移的偏移组
		self.offsetrot_list.append(self.offset_list[0].replace('offset' , 'offsetRot'))
		self.offsetrot_list.append(self.ctrl_list[0].replace('ctrl' , 'ctrlRot'))
		self.offsetrot_list.append(self.subctrl_list[0].replace('ctrl' , 'ctrlRot'))
		
		# 创建用于驱动下巴位移的定位器loc
		self.offsetrot_zero = (self.ctrl_list[0].replace('ctrl' , 'zeroRot'))
		self.offsetrot_loc = (self.ctrl_list[0].replace('ctrl' , 'locRot'))
	
	
	
	def create_bpjnt(self) :
		# 获得jaw_bpjnt 的路径
		self.jaw_bpjnt_path = os.path.abspath(__file__ + "/../jaw_bpjnt.ma")
		# 导入关节
		cmds.file(self.jaw_bpjnt_path , i = True , rnn = True)
	
	
	
	def create_jaw_open(self) :
		u"""
		下巴控制器旋转的时候同时也可以驱动下巴的位移，这样子可以在旋转的过程中直接做出吃惊等一系列夸张的效果
		原理：获得控制器offset组，ctrl，和subctrl的旋转值，将其连接给乘除节点，最后连接回给控制器的connect组
		注意点：不能够直接通过约束loc的方式来获得数值连接，这样会产生cycle的循环，
		因此需要创建三个组来分别连接对应层级的旋转值和rotate order，最后用这个创建出来的子层级组再来进行约束
		"""
		# 创建用于驱动下巴位移的偏移组
		parent = self.ctrl_grp
		for offset in self.offsetrot_list :
			offset = cmds.createNode('transform' , name = offset , parent = parent)
			# 连接对应的旋转值和rotate order
			cmds.connectAttr(offset.replace('Rot_' , '_') + '.rotate' , offset + '.rotate')
			cmds.connectAttr(offset.replace('Rot_' , '_') + '.rotateOrder' , offset + '.rotateOrder')
			parent = offset
		
		# 创建用来约束定位的loc
		self.offsetrot_loc = cmds.spaceLocator(name = self.offsetrot_loc)[0]
		self.offsetrot_zero = hierarchyUtils.Hierarchy.add_extra_group(self.offsetrot_loc , self.offsetrot_zero ,
		                                                               world_orient = False)
		cmds.parent(self.offsetrot_zero , self.ctrl_grp)
		
		# 偏移组的子层级对loc进行旋转约束来记录数值
		cmds.orientConstraint(self.offsetrot_list[-1] , self.offsetrot_loc , mo = False)
		
		# 创建一个乘除节点来连接loc的旋转和下巴控制器的位移
		div_node = cmds.createNode('multiplyDivide' , name = self.ctrl_list[0].replace('ctrl' , 'div'))
		
		# 给下把控制器添加两个属性，offset_X,offset_Z,用于给动画师调整嘴巴张合的时候带动偏移的距离
		cmds.addAttr(self.ctrl_list[0] , ln = 'offset_X' , at = 'double' , dv = 0.01 , min = -0.05 , max = 0.05 ,
		             k = 1)
		cmds.addAttr(self.ctrl_list[0] , ln = 'offset_Z' , at = 'double' , dv = 0.01 , min = -0.05 , max = 0.05 ,
		             k = 1)
		
		# 连接loc的旋转和乘除节点
		cmds.connectAttr(self.offsetrot_loc + '.rotateY' , div_node + '.input1X')
		cmds.connectAttr(self.offsetrot_loc + '.rotateY' , div_node + '.input1Z')
		
		# 连接控制器的属性和乘除节点
		cmds.connectAttr(self.ctrl_list[0] + '.offset_X' , div_node + '.input2X')
		cmds.connectAttr(self.ctrl_list[0] + '.offset_Z' , div_node + '.input2Z')
		
		# 连接乘除节点和控制器上层的connect组的位移
		cmds.connectAttr(div_node + '.outputX' , self.connect_list[0] + '.translateX')
		cmds.connectAttr(div_node + '.outputZ' , self.connect_list[0] + '.translateZ')
	
	
	
	def create_ctrl(self) :
		super().create_ctrl()
		# 使控制器的旋转
		# 创建下巴控制器旋转时候的联动，下巴控制器旋转的时候同时也可以驱动下巴的位移，这样子可以在旋转的过程中直接做出吃惊等一系列夸张的效果
		self.create_jaw_open()



if __name__ == "__main__" :
	def build_setup() :
		jaw_m = jaw.Jaw(side = 'm' , joint_parent = None , control_parent = None)
		jaw_m.build_setup()
	
	
	
	def build_rig() :
		jaw_m = jaw.Jaw(side = 'm' , joint_parent = None , control_parent = None)
		jaw_m.build_rig()
	
	
	
	build_setup()
	build_rig()
