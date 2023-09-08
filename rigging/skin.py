# coding=utf-8

import maya.cmds as cmds
import muziToolset.core.hierarchyUtils as hierarchyUtils
import pymel.core as pm
from importlib import reload

shapenodes = pm.selected()[0].getShape()
# 获取形状节点的历史节点类型为joint的节点
all_jnts = shapenodes.history(type = 'joint')

assert len(all_jnts) , u'请选择具有蒙皮的模型'
for jnt in all_jnts :
    skin_Matrix = cmds.listConnections(jnt + '.worldMatrix' , destination = True , skipConversionNodes = True ,
                                       plugs = True)
    # 添加上层层级组
    matrix_grp = cmds.group(name = 'matrix_{}'.format(jnt) , empty = True)
    t_pos = cmds.xform(jnt , query = True , worldSpace = True , translation = True)
    r_pos = cmds.xform(jnt , query = True , worldSpace = True , rotation = True)
    s_pos = cmds.xform(jnt , q = True , worldSpace = True , s = True)
    cmds.xform(matrix_grp , s = s_pos)
    cmds.xform(matrix_grp , ws = True , t = t_pos)
    cmds.xform(matrix_grp , ws = True , ro = r_pos)

    obj_parent = cmds.listRelatives(jnt , parent = True)
    if obj_parent :
        cmds.parent(matrix_grp , obj_parent[0] , absolute = True)
        cmds.parent(jnt , matrix_grp , absolute = True)
    else :
        cmds.parent(jnt , matrix_grp , absolute = True)

    # 创建multMatrix节点来连接
    matrix_node = cmds.createNode('multMatrix' , name = 'matrix_{}'.format(jnt))

    # 连接属性
    cmds.connectAttr(jnt + '.worldMatrix' , matrix_node + '.matrixIn[0]')
    cmds.connectAttr(matrix_grp + '.worldInverseMatrix' , matrix_node + '.matrixIn[1]')
    cmds.connectAttr(matrix_node + '.matrixSum' , skin_Matrix[0] , force = True)
