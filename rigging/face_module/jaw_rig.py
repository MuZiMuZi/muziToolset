# coding=utf-8
'''
下巴的绑定系统创建
'''
import maya.cmds as cmds

class Jaw_Rig(object):
	
	def __init__(self, joint_parent = None , control_parent = None):
		self.jaw_bpjnt = ['bpjnt_m_Jaw_001','bpjnt_m_Jaw_002']
		
	def create_jaw_rig(self):
		u'''
		生成下巴的绑定
		'''
		self.jaw_ctrl = controlUtils.Control.create_ctrl(self.jaw_bpjnt[0].replace('bpjnt','ctrl') , shape = 'jawCtrl' , radius = 8 , axis = 'Y+' ,
		                                                 pos = self.jaw_bpjnt[0] ,
		                                                 parent = None)
		
		