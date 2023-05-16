bpjnts = cmds.ls(sl = True)

for bpjnt in bpjnts :
	# 创建镜像位移的乘除节点
	trans_node = cmds.createNode('multiplyDivide' , name = bpjnt.replace('bpjnt' , 'trans'))
	cmds.setAttr(trans_node + '.input2X' , -1)
	
	cmds.connectAttr(bpjnt + '.translate' , trans_node + '.input1')
	cmds.connectAttr(trans_node + '.output' , bpjnt.replace('_l_' , '_r_') + '.translate')
	# 创建镜像旋转的乘除节点
	rotate_node = cmds.createNode('multiplyDivide' , name = bpjnt.replace('bpjnt' , 'rotate'))
	cmds.setAttr(rotate_node + '.input2Y' , -1)
	cmds.setAttr(rotate_node + '.input2Z' , -1)
	
	cmds.connectAttr(bpjnt + '.rotate' , rotate_node + '.input1')
	cmds.connectAttr(rotate_node + '.output' , bpjnt.replace('_l_' , '_r_') + '.rotate')