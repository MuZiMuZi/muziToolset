
# coding=utf-8

'''
将cmds库慢慢转化到pymel的示例
'''


import math

import maya.cmds as cmds
import pymel.core as pm
# 初始化对象作为变量
clock_face = pm.SCENE.surface
second_pointer = pm.SCENE.second
minute_pointer = pm.SCENE.minute
hour_pointer = pm.SCENE.hour


# 获取圆盘的半径值
bbox = clock_face.getBoundingBox()
radius = bbox.w/2-1
pi = 3.141592654

# 获取圆盘在世界层级下的位置
surface_location = clock_face.getTranslation(space = 'world')

# 按照角度生成多边形放在对应位置上，并且设置旋转，当为5的倍数的时候需要设置更大的缩放
for i in range(60):
    cube = cmds.polyCube()[0]
    arc = i * 6 * pi / 180
    x, y, z = (
        radius * math.cos(arc) + surface_location[0],
        surface_location[1],
        radius * math.sin(arc) + surface_location[2]
    )
    cube = pm.PyNode(cube)
    cube.translate.set([x,y,z])
    if not i % 5:
        cube.scale.set([2,1,0.4])
    else:
        cube.scale.set([1,0.5,0.2])
    cube.rotateY.set(-6*i)

#创建second_math_node 节点并设置属性
second_math_node = pm.createNode('floatMath',name = 'math_m_second_001')
second_math_node.operation.set(3)
#连接属性
second_pointer.rotateY >> second_math_node.floatA
second_math_node.outFloat >>minute_pointer.rotateY
second_math_node.floatB.set(60)

#创建minute_math_node 节点并设置属性
minute_math_node = pm.createNode('floatMath',name = 'math_m_minute_001')
minute_math_node.operation.set(3)
#连接属性
minute_pointer.rotateY >> minute_math_node.floatA
minute_math_node.outFloat >>hour_pointer.rotateY
minute_math_node.floatB.set(12)


time_units = {'seconds': 59, 'minutes': 59, 'hours': 11}
for key, value in time_units.items():
    if clock_face.hasAttr(key):
        pass
    else:
        clock_face.addAttr(ln = key, at = 'double', min = 0, max = value, dv = 0, k = True)

math_nodes = [pm.createNode('floatMath') for i in range(5)]
for i,mode in enumerate([2, 0, 2, 0, 2]):
    math_nodes[i].operation.set(mode)

math_node_01 = math_nodes[0]
clock_face.hours >> math_node_01.floatA
math_node_01.floatB.set(60)

math_node_02 = math_nodes[1]
math_node_01.outFloat >> math_node_02.floatA
clock_face.minutes >> math_node_02.floatB

math_node_03 = math_nodes[2]
math_node_02.outFloat >> math_node_03.floatA
math_node_03.floatB.set(60)

math_node_04 = math_nodes[3]
math_node_03.outFloat >> math_node_04.floatA
clock_face.seconds >> math_node_04.floatB

math_node_05 = math_nodes[4]
math_node_04.outFloat >> math_node_05.floatA
math_node_05.floatB.set(-6)

math_node_05.outFloat >> second_pointer.ry
