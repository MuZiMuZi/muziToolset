# coding=utf-8
from importlib import reload
import maya.cmds as cmds
u"""
hierarchyUtils：这是一个用来对层级结构进行修改的类

目前已有的功能：

parent：查找子物体和父物体之间是否有父子层级关系
add_extra_group：在对象上方添加一个额外的组.
control_hierarchy:做控制器的层级结构
get_child_object:获取对象的所有子物体包括对象本身
"""

class Hierarchy(object):

    @staticmethod
    def parent(child_node, parent_node):
        u"""
        查找子物体和父物体之间是否有父子层级关系
        :param child_node:
        :param parent_node:
        :return:
        """
        if parent_node:
            parent_original = cmds.listRelatives(child_node, parent=True)
            if not parent_original or parent_original[0] != parent_node:
                cmds.parent(child_node, parent_node)
            else:
                cmds.warning(u'{} 已为 {}的子物体'.format(child_node, parent_node))
        else:
            cmds.warning(u'没有给定父物体节点')


    @staticmethod
    def add_extra_group(obj, grp_name, world_orient=False):
        u"""在对象上方添加一个额外的组.

        Args:
            obj (str):要添加额外组的Maya对象.
            grp_name (str): 额外的组名
            world_orient (bool): 设置新组的世界位置是否改变。

        Returns:
            str: 新添加的组.

        """

        obj_grp = cmds.group(name=grp_name, empty=True)
        t_pos = cmds.xform(obj, query=True, worldSpace=True, translation=True)
        r_pos = cmds.xform(obj, query=True, worldSpace=True, rotation=True)
        if world_orient:
            r_pos = [0, 0, 0]
        s_pos = cmds.xform(obj, q=True, worldSpace=True, s=True)
        cmds.xform(obj_grp, s=s_pos)
        cmds.xform(obj_grp, ws=True, t=t_pos)
        cmds.xform(obj_grp, ws=True, ro=r_pos)

        obj_parent = cmds.listRelatives(obj, parent=True)
        if obj_parent:
            cmds.parent(obj_grp, obj_parent[0], absolute=True)
            cmds.parent(obj, obj_grp, absolute=True)
        else:
            cmds.parent(obj, obj_grp, absolute=True)

        return obj_grp

    @staticmethod
    def control_hierarchy():
        """Add an upper level group to the controller.

            The naming convention is
            Type_Side_describe_index

            """
        CTRL_COLORS = {'m': 17,
                       'l': 6,
                       'r': 13}

        SUB_COLORS = {'m': 25,
                      'l': 15,
                      'r': 4}

        # get selected nurbs curve as controller
        ctrls = cmds.ls(selection=True)

        # loop in each ctrl and create hierarchy
        for ctrl in ctrls:
            # get name parts
            name_parts = ctrl.split('_')

            # create zero group
            zero = cmds.createNode('transform', name=ctrl.replace('ctrl_', 'zero_'))
            # create driven group
            driven = cmds.createNode('transform', name=ctrl.replace('ctrl_', 'driven_'), parent=zero)
            # create connect group
            connect = cmds.createNode('transform', name=ctrl.replace('ctrl_', 'connect_'), parent=driven)
            # create offset group
            offset = cmds.createNode('transform', name=ctrl.replace('ctrl_', 'offset_'), parent=connect)

            # snap to control position
            cmds.matchTransform(zero, ctrl, position=True, rotation=True)

            # parent control to offset group
            cmds.parent(ctrl, offset)

            # freeze transformation for controller
            cmds.makeIdentity(ctrl, apply=True, translate=True, rotate=True, scale=True)
            # delete history
            cmds.select(ctrl)
            cmds.DeleteHistory()

            # duplicate ctrl as sub control
            sub = cmds.duplicate(ctrl, name=ctrl.replace(name_parts[2], name_parts[2] + 'Sub'))[0]
            cmds.parent(sub, ctrl)
            cmds.setAttr(sub + '.scale', 0.5, 0.5, 0.5)
            cmds.makeIdentity(sub, apply=True, scale=True)

            # create output group
            output = cmds.createNode('transform', name=ctrl.replace('ctrl_', 'output_'), parent=ctrl)

            # connect attrs
            cmds.connectAttr(sub + '.translate', output + '.translate')
            cmds.connectAttr(sub + '.rotate', output + '.rotate')
            cmds.connectAttr(sub + '.scale', output + '.scale')
            cmds.connectAttr(sub + '.rotateOrder', output + '.rotateOrder')

            # show rotate order
            cmds.setAttr(ctrl + '.rotateOrder', channelBox=True)
            cmds.setAttr(sub + '.rotateOrder', channelBox=True)

            # add sub vis attr
            cmds.addAttr(ctrl, longName='subCtrlVis', attributeType='bool')
            cmds.setAttr(ctrl + '.subCtrlVis', channelBox=True)

            # connect sub vis
            cmds.connectAttr(ctrl + '.subCtrlVis', sub + '.visibility')
            # set color
            for ctrl_node, col_idx in zip([ctrl, sub], [CTRL_COLORS[name_parts[1]], SUB_COLORS[name_parts[1]]]):
                # get shape node
                shape_node = cmds.listRelatives(ctrl_node, shapes=True)[0]
                # set color
                # cmds.setAttr(shape_node + '.overrideEnabled', 1)
                # cmds.setAttr(shape_node + '.overrideColor', col_idx)

    @staticmethod
    def get_child_object(object):
        u'''
        获取对象的所有子物体包括对象本身
        :param object: 需要获取所有子物体的对象
        :return: 所有子物体的名称列表
        '''
        object_lsit = cmds.listRelatives(object, children = True, allDescendents = True)
        object_lsit.append(object)
        object_lsit.reverse()
        return object_lsit


    @staticmethod
    def create_rig_grp() :
        loc_grp = '_locator'
        ctrl_grp = '_control'
        jnt_grp = '_joint'
        mesh_grp = '_mesh'
        node_grp = '_node'
        for grp in [loc_grp , ctrl_grp , jnt_grp , mesh_grp, node_grp] :
            if not cmds.ls(grp) :
                cmds.group(em = 1 , name = grp)
                