# coding=utf-8

import math

import maya.cmds as cmds

# 查找圆盘的半径值
surface = 'surface'
bbox = cmds.exactWorldBoundingBox(surface)
# abs 是绝对值的意思，获取两者相减后的绝对值除二即可获得圆盘的半径
radius = abs(bbox[0] - bbox[3]) / 2

# 定义π的变量数值
pi = 3.1415926

# 获得圆盘的位置信息
surface_location = cmds.xform(surface,query = True,translation = True,worldSpace = True)
surface_location_x = surface_location[0]
surface_location_y = surface_location[1]
surface_location_z = surface_location[2]

# 循环按照度数生成需要的立方体
for index in range(60):
    cube = cmds.polyCube()[0]
    arc = index * 6 * pi / 180

    # 运用数学节点，计算cos和sin的值 ，pi/180用来转化成弧度
    x = radius * math.cos(arc) + surface_location_x
    y = surface_location_y
    z = radius * math.sin(arc) + surface_location_z

    # 移动方块盒子到对应的位置
    cmds.move(x, y, z)
    # 设置对应的旋转缩放，当数值取余5为0的时候，则为大的刻度，需要特殊处理
    if not index % 5:
        cmds.setAttr(cube + '.scaleX', 1.5)
        cmds.setAttr(cube + '.scaleZ', 0.5)
    else:
        cmds.setAttr(cube + '.scaleY', 0.5)
        cmds.setAttr(cube + '.scaleZ', 0.2)
    cmds.setAttr(cube + '.rotateY', index * -6)
