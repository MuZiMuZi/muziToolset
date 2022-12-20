import maya.cmds as cmds

control_list = cmds.ls(sl = True)
attrs = ['.translateX','.translateY','.translateZ','.rotateX','.rotateY','.rotateZ']
for ctrl in control_list:
	parent_ctrl = cmds.listRelatives(ctrl,parent = True)[0]
	for attr in attrs:
		cmds.setAttr(parent_ctrl + attr,cmds.getAttr(ctrl + attr))
		cmds.setAttr(ctrl + attr,0)