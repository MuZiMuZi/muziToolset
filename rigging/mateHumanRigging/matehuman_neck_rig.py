# coding=utf-8

u"""
这是一个用来编写neck（脖子）绑定的类，之后的绑定都会在这个类的基础上逐级继承下去

目前已有的功能：

create_neck_rig：创建脖子的控制器绑定



"""
import maya.cmds as cmds
from . import matehuman_ikfk_rig
from . import matehuman_base_rig
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils
import muziToolset.core.matehumanUtils as matehumanUtils
from importlib import reload


reload(pipelineUtils)
reload(jointUtils)
reload(matehuman_ikfk_rig)


class Neck_Rig(matehuman_base_rig.Base_Rig) :
	
	
	def __init__(self ,  space_list) :
		super(Neck_Rig , self).__init__()
		self.drv_jnts = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('neck')
		self.make(self.drv_jnts)
		self.space_list = space_list
	
	
	def create_neck_rig(self) :
		# 创建脖子的fk绑定系统
		neck_system = matehuman_ikfk_rig.FK_Rig(self.drv_jnts , self.joint_parent , self.control_parent)
		neck_system._create_fk_chain_system(constraint = True)


# example
# m_neck = Neck_Rig(joint_parent , space_list )
#
# m_neck.create_neck_rig()
