# coding=utf-8

u"""
这是一个用来编写spine（脊椎）绑定的类，之后的绑定都会在这个类的基础上逐级继承下去

目前已有的功能：

create_spine_rig：创建脊椎的控制器绑定



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


class Spine_Rig(matehuman_base_rig.Base_Rig) :
	
	
	def __init__(self ,  space_list , stretch = True) :
		super(Spine_Rig , self).__init__()
		self.drv_jnts = self.spine_jnts
		self.make(self.drv_jnts)
		self.space_list = space_list
		self.stretch = stretch
	
	
	def create_spine_rig(self) :
		# 创建脊椎的绑定
		spine_system = matehuman_ikfk_rig.IKFK_Rig(self.drv_jnts , self.joint_parent , self.control_parent ,
		                                           self.space_list , self.stretch, redius = 25)
		spine_system.create_ikfk_spine_rig()
		
		#创建胯部的绑定
		self.root_jnts_ikfk = pipelineUtils.Pipeline.create_node('joint' , 'ikfk_' + self.root_jnts , match = True ,
		                                                         match_node = self.root_jnts)
		
		self.pelvis_jnts_ikfk = pipelineUtils.Pipeline.create_node('joint' , 'ikfk_' + self.pelvis_jnts , match = True ,
		                                                           match_node = self.pelvis_jnts)
		cmds.parent(self.root_jnts_ikfk , self.pelvis_jnts_ikfk , self.joint)


# example
# m_spine = Spine_Rig(joint_parent , space_list , stretch = True)
#
# m_spine.create_ikfk_spine_rig()
