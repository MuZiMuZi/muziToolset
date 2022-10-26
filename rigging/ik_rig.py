# coding=utf-8

u"""
这是一个用来编写IK控制系统绑定的类，之后的绑定都会在这个类的基础上逐级继承下去
继承了base_rig
目前已有的功能：

ik_chain_rig：创建IK链的控制器绑定

ik_spine_rig：创建IKspine链的控制器绑定（脊椎，脖子）


"""

import maya.cmds as cmds

import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.pipelineUtils as pipelineUtils

import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.snapUtils as snapUtils

reload(pipelineUtils)
reload(jointUtils)
reload(snapUtils)

import base_rig

reload(base_rig)


class IK_Rig(base_rig.Base_Rig):
    def __init__(self, bp_joints = None, joint_parent = None, control_parent = None):
        super(IK_Rig, self).__init__()
        self.bp_joints = bp_joints
        self.joint_parent = joint_parent
        self.control_parent = control_parent

    def ik_chain_rig(self, ik_chain, control_parent):
        u"""
        创建IK链的控制器绑定
        Args:
            control_parent(str): 控制器组的父层级

        Returns: ik_ctrl_grp ：IK控制器的最顶层

        """
        cmds.setAttr(ik_chain[0] + '.visibility', 0)
        # 创建开始的IK控制器
        startIK_jnt = ik_chain[0]
        startIK_ctrl_name = startIK_jnt.replace('jnt_', 'ctrl_')
        startIK_ctrl_obj = controlUtils.Control.create_ctrl(startIK_ctrl_name, shape = 'Cube', radius = 13, axis = 'Y+',
                                                            pos = startIK_jnt, parent = None)
        startIK_ctrl = startIK_ctrl_name
        startIK_ctrl_output = startIK_ctrl.replace('ctrl_', 'output_')
        startIK_zero = startIK_ctrl.replace('ctrl_', 'zero_')
        cmds.pointConstraint(startIK_ctrl_output, startIK_jnt, maintainOffset = True)

        # 创建尾端的ik控制器
        endIK_jnt = ik_chain[2]
        endIK_ctrl_name = endIK_jnt.replace('jnt_', 'ctrl_')
        endIK_ctrl_obj = controlUtils.Control.create_ctrl(endIK_ctrl_name, shape = 'Cube', radius = 13, axis = 'Y+',
                                                          pos = endIK_jnt, parent = None)
        endIK_ctrl = endIK_ctrl_name
        endIK_ctrl_output = endIK_ctrl_name.replace('ctrl_', 'output_')
        endIK_zero = endIK_ctrl_name.replace('ctrl_', 'zero_')

        endIK_local_ctrl_name = nameUtils.Name(name = endIK_ctrl_name)
        endIK_local_ctrl_name.description = endIK_local_ctrl_name.description + 'local'
        endIK_local_ctrl_obj = controlUtils.Control.create_ctrl(endIK_local_ctrl_name.name, shape = 'local',
                                                                radius = 10,
                                                                axis = 'X-',
                                                                pos = endIK_jnt, parent = None)
        endIK_local_ctrl = endIK_local_ctrl_name.name
        endIK_local_zero = endIK_local_ctrl.replace('ctrl_', 'zero_')
        cmds.parent(endIK_local_zero, endIK_ctrl_output)
        #
        # 创建ik的极向量控制器
        midIK_jnt = ik_chain[1]
        midIK_pv_ctrl_obj = nameUtils.Name(name = midIK_jnt)
        midIK_pv_ctrl_obj.type = 'ctrl'
        midIK_pv_ctrl_obj.description = midIK_pv_ctrl_obj.description + 'Pv'
        midIK_pv_ctrl_obj2 = controlUtils.Control.create_ctrl(midIK_pv_ctrl_obj.name, shape = 'Cube',
                                                              radius = 8,
                                                              axis = 'Y+', pos = midIK_jnt, parent = None)
        midIK_pv_ctrl = midIK_pv_ctrl_obj.name
        midIK_pv_zero = midIK_pv_ctrl.replace('ctrl_', 'zero_')
        cmds.matchTransform(midIK_pv_zero, midIK_jnt, position = True, rotation = True, scale = True)

        cmds.parent(midIK_pv_zero, ik_chain[1])

        if midIK_pv_ctrl_obj.side == 'r':
            side_value = -1
        else:
            side_value = 1

        cmds.move(0, 32 * side_value, 0, midIK_pv_zero, relative = True, objectSpace = True, worldSpaceDistance = True)
        cmds.parent(midIK_pv_zero, world = True)

        # 创建ik极向量控制器的曲线指示器
        midIK_pv_loc = cmds.spaceLocator(name = midIK_pv_ctrl.replace('ctrl_', 'loc_'))[0]
        cmds.matchTransform(midIK_pv_loc, midIK_pv_ctrl)
        cmds.parent(midIK_pv_loc, midIK_pv_ctrl)
        cmds.setAttr(midIK_pv_loc + '.visibility', 0)
        midIK_jnt_loc = cmds.spaceLocator(name = midIK_jnt.replace('jnt_', 'loc_'))[0]
        cmds.matchTransform(midIK_jnt_loc, midIK_jnt)
        cmds.parent(midIK_jnt_loc, midIK_jnt)
        cmds.setAttr(midIK_jnt_loc + '.visibility', 0)

        # 连接loc和曲线来表示位置
        ikpv_curve = cmds.curve(degree = 1, point = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
                                name = midIK_pv_ctrl.replace('ctrl_', 'crv_'))
        midIK_jnt_loc_shape = cmds.listRelatives(midIK_jnt_loc, shapes = True)[0]
        midIK_pv_loc_shape = cmds.listRelatives(midIK_pv_loc, shapes = True)[0]
        ikpv_curve_shape = cmds.listRelatives(ikpv_curve, shapes = True)[0]

        cmds.connectAttr(midIK_jnt_loc_shape + '.worldPosition[0]', ikpv_curve_shape + '.controlPoints[0]')
        cmds.connectAttr(midIK_pv_loc_shape + '.worldPosition[0]', ikpv_curve_shape + '.controlPoints[1]')

        cmds.setAttr(ikpv_curve_shape + '.overrideEnabled', 1)
        cmds.setAttr(ikpv_curve_shape + '.overrideDisplayType', 2)

        #
        # 创建IKhandle控制
        ikhandle_name = startIK_jnt.replace('jnt_', 'ikhandle_')
        ikhandle_node = cmds.ikHandle(name = ikhandle_name, startJoint = ik_chain[0], endEffector = ik_chain[2],
                                      sticky = 'sticky', solver = 'ikRPsolver', setupForRPsolver = True)[0]
        cmds.setAttr(ikhandle_node + '.visibility', 0)
        endIK_local_output = endIK_local_zero.replace('zero_', 'output_')
        cmds.parent(ikhandle_node, endIK_local_output)
        cmds.poleVectorConstraint(midIK_pv_ctrl, ikhandle_node)
        ik_ctrl_grp = cmds.createNode('transform', name = ik_chain[0].replace('jnt', 'grp'))
        cmds.parent(startIK_zero, midIK_pv_zero, endIK_zero, ikpv_curve, ik_ctrl_grp)
        if control_parent:
            hierarchyUtils.Hierarchy.parent(child_node = ik_ctrl_grp, parent_node = control_parent)

    def ik_spine_rig(self, ik_chain, control_parent):
        u"""
        创建IKspine链的控制器绑定
        Args:
            control_parent(str): 控制器组的父层级

        Returns: ik_ctrl_grp ：IK控制器的最顶层

        """
        cmds.setAttr(ik_chain[0] + '.visibility', 0)

        ik_chain_crv = cmds.curve(degree = 3, name = self.bp_joints[0].replace('bpjnt_', 'crv_'),
                                  p = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)])

        # 获取节点的曲线形状
        curve_shape = cmds.listRelatives(ik_chain_crv, shapes = True)[0]

        # 获取曲线跨度和度数
        spans = cmds.getAttr(curve_shape + '.spans')
        degree = cmds.getAttr(curve_shape + '.degree')

        # 获取曲线的点数目
        cv_num = spans + degree

        # 将曲线点吸附到关节上
        for i in range(cv_num):
            jnt = ik_chain[i]
            # 获取jnt位置
            jnt_pos = cmds.xform(jnt, query = True, translation = True,
                                 worldSpace = True)
            # 获取cv位置
            cv = '{}.cv[{}]'.format(ik_chain_crv, i)
            # 设置cv点的位置
            cmds.xform(cv, translation = jnt_pos, worldSpace = True)

        # 创建开始的IK控制器
        startIK_jnt = ik_chain[0]
        startIK_crv_jnt = cmds.createNode('joint', name = startIK_jnt.replace('jnt_', 'crvjnt_'))
        cmds.matchTransform(startIK_crv_jnt, startIK_jnt, position = True, rotation = True, scale = True)
        startIK_ctrl = startIK_jnt.replace('jnt_', 'ctrl_')
        startIK_ctrl_obj = controlUtils.Control.create_ctrl(startIK_ctrl, shape = 'Cube', radius = 20, axis = 'Y+',
                                                            pos = startIK_jnt, parent = None)
        startIK_ctrl_output = startIK_ctrl.replace('ctrl_', 'output_')
        startIK_zero = startIK_ctrl.replace('ctrl_', 'zero_')
        cmds.parent(startIK_crv_jnt, startIK_ctrl_output)
        cmds.setAttr(startIK_crv_jnt + '.visibility', 0)

        # 创建尾端的ik控制器
        endIK_jnt = ik_chain[4]
        endIK_crv_jnt = cmds.createNode('joint', name = endIK_jnt.replace('jnt_', 'crvjnt_'))
        cmds.matchTransform(endIK_crv_jnt, endIK_jnt, position = True, rotation = True, scale = True)
        endIK_ctrl = endIK_jnt.replace('jnt_', 'ctrl_')
        endIK_ctrl_obj = controlUtils.Control.create_ctrl(endIK_ctrl, shape = 'Cube', radius = 20, axis = 'Y+',
                                                          pos = endIK_jnt, parent = None)
        endIK_ctrl_output = endIK_ctrl.replace('ctrl_', 'output_')
        endIK_zero = endIK_ctrl.replace('ctrl_', 'zero_')
        cmds.parent(endIK_crv_jnt, endIK_ctrl_output)
        cmds.setAttr(endIK_crv_jnt + '.visibility', 0)

        #
        # 创建中间的ik控制器
        midIK_jnt = ik_chain[2]
        midIK_crv_jnt = cmds.createNode('joint', name = midIK_jnt.replace('jnt_', 'crvjnt_'))
        cmds.matchTransform(midIK_crv_jnt, midIK_jnt, position = True, rotation = True, scale = True)
        midIK_ctrl = midIK_jnt.replace('jnt_', 'ctrl_')
        midIK_ctrl_obj = controlUtils.Control.create_ctrl(midIK_ctrl, shape = 'Cube', radius = 15, axis = 'Y+',
                                                          pos = midIK_jnt, parent = None)
        midIK_ctrl_output = midIK_ctrl.replace('ctrl_', 'output_')
        cmds.parent(midIK_crv_jnt, midIK_ctrl_output)
        cmds.setAttr(midIK_crv_jnt + '.visibility', 0)
        midIK_zero = midIK_ctrl.replace('ctrl_', 'zero_')

        # 曲线关节对ikspine曲线进行蒙皮
        cmds.skinCluster(startIK_crv_jnt, midIK_crv_jnt, endIK_crv_jnt, ik_chain_crv, tsb = True)

        # 曲线对ik关节做ik样条线手柄
        spine_ikhandle_node = cmds.ikHandle(curve = ik_chain_crv, startJoint = ik_chain[0], endEffector = ik_chain[4],
                                            solver = 'ikSplineSolver', createCurve = 0,
                                            name = startIK_jnt.replace('jnt_', 'ikhandle_'))[0]
        # 创建loc来制作ikhandle的横向旋转
        startIK_loc = cmds.spaceLocator(name = startIK_jnt.replace('jnt_', 'loc_'))[0]
        endIK_loc = cmds.spaceLocator(name = endIK_jnt.replace('jnt_', 'loc_'))[0]

        cmds.matchTransform(startIK_loc, startIK_jnt, position = True, rotation = True, scale = True)
        cmds.parent(startIK_loc, startIK_ctrl_output)
        cmds.matchTransform(endIK_loc, endIK_jnt, position = True, rotation = True, scale = True)
        cmds.parent(endIK_loc, endIK_ctrl_output)

        # 设置ikhandle的高级扭曲属性用来设置横向旋转
        cmds.setAttr(spine_ikhandle_node + '.dTwistControlEnable', 1)
        cmds.setAttr(spine_ikhandle_node + '.dWorldUpType', 4)
        cmds.connectAttr(startIK_loc + '.worldMatrix[0]', spine_ikhandle_node + '.dWorldUpMatrix')
        cmds.connectAttr(endIK_loc + '.worldMatrix[0]', spine_ikhandle_node + '.dWorldUpMatrixEnd')

        # 整理层级结构
        ik_ctrl_grp = cmds.createNode('transform', name = ik_chain[0].replace('jnt', 'grp'))
        cmds.parent(startIK_zero, midIK_zero, endIK_zero, ik_ctrl_grp)
        if control_parent:
            hierarchyUtils.Hierarchy.parent(child_node = ik_ctrl_grp, parent_node = control_parent)
        hierarchyUtils.Hierarchy.parent(child_node = spine_ikhandle_node, parent_node = self.RigNodes_Local)
        hierarchyUtils.Hierarchy.parent(child_node = ik_chain_crv, parent_node = self.RigNodes_World)

    def ik_chain_stretch(self):
        pass
