import maya.cmds as cmds
import math

bbox = cmds.exactWorldBoundingBox( 'Surface')
radius = abs(bbox[0]-bbox[3])/2-1
pi = 3.141592654

surface_location = cmds.xform('Surface', q=True, t=True, ws=True)


for i in range(60):
    cube = cmds.polyCube()[0]
    arc = i*6*pi/180
    x,y,z=(
        radius*math.cos(arc)+surface_location[0],
        surface_location[1],
        radius*math.sin(arc)+surface_location[2]
        )
    cmds.move(x,y,z)
    if not i%5:
        cmds.setAttr(f'{cube}.scaleX', 2)
        cmds.setAttr(f'{cube}.scaleZ', 0.4)
    else:
        cmds.setAttr(f'{cube}.scaleY', 0.5)
        cmds.setAttr(f'{cube}.scaleZ', 0.2)
    cmds.setAttr(f'{cube}.rotateY', -6*i)

math_node = cmds.shadingNode('floatMath', asUtility=True)
cmds.setAttr(f'{math_node}.operation' ,3)
cmds.connectAttr('second.rotateY', f'{math_node}.floatA', force=True)
cmds.connectAttr(f'{math_node}.outFloat', 'minute.rotateY', force=True)
cmds.setAttr(f'{math_node}.floatB', 60)


math_node = cmds.shadingNode('floatMath', asUtility=True)
cmds.setAttr(f'{math_node}.operation' ,3)
cmds.connectAttr('minute.rotateY', f'{math_node}.floatA', force=True)
cmds.connectAttr(f'{math_node}.outFloat', 'hour.rotateY', force=True)
cmds.setAttr(f'{math_node}.floatB', 12)

time_units = {'seconds': 59, 'minutes': 59, 'hours': 11}
for key,value in time_units.items():
    if cmds.objExists(f'Surface.{key}'):
        pass
    else:
        cmds.addAttr('|Meshes|Surface', ln=key, at='double', min=0, max=value, dv=0, k=True)


math_nodes = [cmds.shadingNode('floatMath', asUtility=True) for i in range(5)]
for i,mode in enumerate([2, 0, 2, 0, 2]):
    cmds.setAttr(f'{math_nodes[i]}.operation' ,mode)

math_node_01 = math_nodes[0]
cmds.connectAttr('Surface.hours', f'{math_node_01}.floatA', force=True)
cmds.setAttr(f'{math_node_01}.floatB', 60)

math_node_02 = math_nodes[1]
cmds.connectAttr(f'{math_node_01}.outFloat', f'{math_node_02}.floatA', force=True)
cmds.connectAttr('Surface.minutes', f'{math_node_02}.floatB', force=True)

math_node_03 = math_nodes[2]
cmds.connectAttr(f'{math_node_02}.outFloat', f'{math_node_03}.floatA', force=True)
cmds.setAttr(f'{math_node_03}.floatB', 60)

math_node_04 = math_nodes[3]
cmds.connectAttr(f'{math_node_03}.outFloat', f'{math_node_04}.floatA', force=True)
cmds.connectAttr('Surface.seconds', f'{math_node_04}.floatB', force=True)

math_node_05 = math_nodes[4]
cmds.connectAttr(f'{math_node_04}.outFloat', f'{math_node_05}.floatA', force=True)
cmds.setAttr(f'{math_node_05}.floatB', -6)

cmds.connectAttr(f'{math_node_05}.outFloat', 'second.ry', force=True)
