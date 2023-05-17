bp_list = cmds.ls(sl = True)

for bp in bp_list :
	# 创建镜像位移的乘除节点
	trans_bp_node = cmds.createNode('multiplyDivide' , name = bp.replace('bp' , 'trans'))
	cmds.setAttr(trans_bp_node + '.input2X' , -1)
	
	cmds.connectAttr(bp + '.translate' , trans_bp_node + '.input1')
	cmds.connectAttr(trans_bp_node + '.output' , bp.replace('_l_' , '_r_') + '.translate')
	# 创建镜像旋转的乘除节点
	rotate_bpctrl_node = cmds.createNode('multiplyDivide' , name = bp.replace('bp' , 'rotate'))
	cmds.setAttr(rotate_bpctrl_node + '.input2Y' , -1)
	cmds.setAttr(rotate_bpctrl_node + '.input2Z' , -1)
	
	cmds.connectAttr(bp + '.rotate' , rotate_bpctrl_node + '.input1')
	cmds.connectAttr(rotate_bpctrl_node + '.output' , bp.replace('_l_' , '_r_') + '.rotate')