import maya.cmds as cmds



# curve
skin_curve = 'crv_l_lowerEyeLidSkin_001'
ctrl_curve = 'crv_l_lowerEyeLid_001'

# blink
blink_curve = 'crv_l_EyeEyeLidBlink_001'
upper_blink_curve = 'crv_l_upperEyeLidSkinBlink_001'
upper_skin_curve = 'crv_l_upperEyeLidSkin_001'

lower_blink_curve = 'crv_l_lowerEyeLidSkinBlink_001'
lower_skin_curve = 'crv_l_lowerEyeLidSkin_001'

aim_ctrl = 'ctrl_l_EyeAim_001'

# 控制器曲线对蒙皮曲线做wire变形，让控制器曲线控制蒙皮曲线,注意如果是两条曲线做wire变形器的话，被控制的曲线需要给个w参数
wire_node = cmds.wire(skin_curve , w = ctrl_curve , gw = False , en = 1.000000 , ce = 0.000000 ,
                      li = 0.000000)[0]
cmds.setAttr(wire_node + '.dropoffDistance[0]' , 200)

# 开始创建blink
# 将上眼皮的控制曲线与下眼皮的控制曲线对blink曲线做bs驱动,将两个目标体的影响值设置在0.5
bs_node = cmds.blendShape(upper_blink_curve , lower_blink_curve , blink_curve , w = [(0 , 0.5) , (1 , 0.5)])

# 属性blinkHeight连接给bs的权重值
# 查找连接的bs节点
cmds.connectAttr(aim_ctrl + '.blinkHeight' , bs_node[0] + '.{}'.format(lower_blink_curve))
reverse_node = cmds.createNode('reverse' , name = aim_ctrl.replace('ctrl' , 'reverse'))
cmds.connectAttr(aim_ctrl + '.blinkHeight' , self.reverse_node + '.inputX')
cmds.connectAttr(reverse_node + '.outputX' , bs_node[0] + '.{}'.format(upper_blink_curve))

# blink曲线对上眼皮的权重曲线的blink曲线制作线变形器，注意，需要先将blinkHeight调整到0
cmds.setAttr(aim_ctrl + '.blinkHeight' , 0)
upper_wire_node = cmds.wire(upper_blink_curve , w = blink_curve , gw = False , en = 1.000000 ,
                            ce = 0.000000 ,
                            li = 0.000000)[0]
# 调整上眼皮线变形器的参数
cmds.setAttr(upper_wire_node + '.dropoffDistance[0]' , 200)
cmds.setAttr(upper_wire_node + '.scale[0]' , 0)

# 上眼皮的权重曲线的blink曲线对上眼皮的权重曲线做bs
upper_bs_node = cmds.blendShape(upper_blink_curve , upper_skin_curve ,
                                w = [(0 , 1)])
cmds.connectAttr(aim_ctrl + '.blink' , upper_bs_node[0] + '.{}'.format(
		upper_blink_curve))

# blink曲线对下眼皮的权重曲线的blink曲线制作线变形器，注意，需要先将blinkHeight调整到1
cmds.setAttr(aim_ctrl + '.blinkHeight' , 1)
lower_wire_node = \
	cmds.wire(lower_blink_curve , w = blink_curve , gw = False , en = 1.000000 ,
	          ce = 0.000000 ,
	          li = 0.000000)[0]
# 调整下眼皮线变形器的参数
cmds.setAttr(lower_wire_node + '.dropoffDistance[0]' , 200)
cmds.setAttr(lower_wire_node + '.scale[0]' , 0)

# 下眼皮的权重曲线的blink曲线对上眼皮的权重曲线做bs
lower_bs_node = cmds.blendShape(lower_blink_curve , lower_skin_curve ,
                                             w = [(0 , 1)])
cmds.connectAttr(aim_ctrl + '.blink' , lower_bs_node[0] + '.{}'.format(
		lower_blink_curve))
# 恢复blinkHeight的数值
cmds.setAttr(aim_ctrl + '.blinkHeight' , 0.5)
