# coding=utf-8

u"""
这是一个用来编写关节工具的类

目前已有的功能：
 create_chain：通过放置的模板关节生成相应的IK、FK和Bindjoint

 create_joints_on_curve_rigging：基于曲线上的点创建关节(rigging版本)，还未添加是否为曲线的判断

 create_joints_on_curve：基于曲线上的点创建关节(通用版本)，还未添加是否为曲线的判断

"""

import maya.cmds as cmds
import muziToolset.core.nameUtils as nameUtils

import controlUtils

reload(controlUtils)


class Joint(object):
    def __init__(self):

        self.suffix = None
        self.joint_parent = None
        self.joints_chain = None
        self.driven_joint = None
        self.driver_joint = None
        self.avg_jnt = None
        self.bp_joints = None

    def avg_joint(self, driven_joint, weight = 0.5):
        """
        在选定的关节上创建新的avg关节用于旋转约束连接

        Args:
            driven_joint (list): 选定的关节，选定的关节的父层级关节将成为另一个驱动的关节
            weight (float): 两者之间的权重影响

        Returns:
            avg_jnt(str): avg关节的名称
        """
        name_obj = nameUtils.Name(name = driven_joint)
        self.driven_joint = driven_joint
        name_obj.description = name_obj.description + 'Avg'
        self.avg_jnt = cmds.createNode('joint', name = name_obj.name)
        # 选定的关节的父层级关节将成为另一个驱动的关节
        self.driver_joint = cmds.listRelatives(self.driven_joint, parent = True)

        cmds.matchTransform(self.avg_jnt, self.driven_joint, position = True)

        # 执行临时的方向约束以获得平均方向
        cons_node = cmds.orientConstraint(self.driver_joint, self.avg_jnt, maintainOffset = False)[0]
        cmds.setAttr(cons_node + '.interpType', 2)
        cmds.setAttr('{}.{}W0'.format(cons_node, self.driver_joint), weight)
        cmds.setAttr('{}.{}W1'.format(cons_node, self.driven_joint), 1 - weight)

        # 删除方向约束节点
        cmds.delete(cons_node)
        # 冻结变换
        cmds.makeIdentity(self.avg_jnt, apply = True, translate = True, rotate = True, scale = True)
        # avg关节作为选定关节的子物体
        cmds.parent(self.avg_jnt, self.driver_joint)

        # 执行方向约束以驱动avg关节
        cons_node = cmds.orientConstraint(self.driver_joint, self.driven_joint, maintainOffset = False)[0]
        cmds.setAttr(cons_node + '.interpType', 2)
        cmds.setAttr('{}.{}W0'.format(cons_node, self.driver_joint), weight)
        cmds.setAttr('{}.{}W1'.format(cons_node, self.driven_joint), 1 - weight)

    @staticmethod
    def create_joints_on_curve_rigging():
        u"""基于曲线上的点创建关节(rigging版本)

          """

        curve = cmds.ls(sl = True)[0]
        # 拆分名称
        obj = nameUtils.Name(name = curve)
        name_side = obj.side
        name_description = obj.description
        name_index = obj.index

        # 创建组
        grp_jnts = cmds.createNode('transform',
                                   name = 'grp_{}_{}Jnts_{:03d}'.format(name_side, name_description, name_index))

        # 获取节点的曲线形状
        curve_shape = cmds.listRelatives(curve, shapes = True)[0]

        # 获取曲线跨度和度数
        spans = cmds.getAttr(curve_shape + '.spans')
        degree = cmds.getAttr(curve_shape + '.degree')

        # 获取曲线的点数目
        cv_num = spans + degree

        # 创建关节并吸附到曲线
        for i in range(cv_num):
            jnt = cmds.createNode('joint', name = 'jnt_{}_{}_{:03d}'.format(name_side, name_description, i + 1))
            # 获取cv位置
            cv_pos = cmds.xform('{}.cv[{}]'.format(curve, i), query = True, translation = True, worldSpace = True)
            # 设置关节位置
            cmds.xform(jnt, translation = cv_pos, worldSpace = True)
            cmds.parent(jnt, grp_jnts)

    @staticmethod
    def create_joints_on_curve():
        u"""基于曲线上的点创建关节(通用版本)
            还未添加是否为曲线的判断
          """

        curve = cmds.ls(sl = True)[0]
        # 获取节点的曲线形状
        curve_shape = cmds.listRelatives(curve, shapes = True)[0]
        # 创建组
        grp_jnts = cmds.createNode('transform',
                                   name = 'grp_{}Jnts_001'.format(curve))

        # 获取节点的曲线形状
        curve_shape = cmds.listRelatives(curve, shapes = True)[0]

        # 获取曲线跨度和度数
        spans = cmds.getAttr(curve_shape + '.spans')
        degree = cmds.getAttr(curve_shape + '.degree')

        # 获取曲线的点数目
        cv_num = spans + degree

        # 创建关节并吸附到曲线
        for i in range(cv_num):
            jnt = cmds.createNode('joint', name = 'jnt_{}_{:03d}'.format(curve, i + 1))
            # 获取cv位置
            cv_pos = cmds.xform('{}.cv[{}]'.format(curve, i), query = True, translation = True, worldSpace = True)
            # 设置关节位置
            cmds.xform(jnt, translation = cv_pos, worldSpace = True)
            cmds.parent(jnt, grp_jnts)

    @staticmethod
    def create_chain(bp_joints,suffix, joint_parent = None):
        '''通过放置的模板关节生成相应的IK、FK和Bindjoint

        bp_joints(list): 用于放置模板的关节列表。
        suffix(str):要添加到关节的后缀.
        joint_parent(str):关节的父层级物体.

        :return(list):生成的关节列表.
        '''
        # 创建关节
        joints_chain = []
        for jnt in bp_joints:
            jnt_new = jnt
            jnt_new_name = nameUtils.Name(name = jnt_new)
            jnt_new_name.type = 'jnt'
            jnt_new_name.description = '{}{}'.format(jnt_new_name.description, suffix)
            jnt_new = cmds.createNode('joint', name = jnt_new_name.name)
            cmds.matchTransform(jnt_new, jnt, position = True, rotation = True)
            cmds.makeIdentity(jnt_new, apply = True, translate = True, rotate = True, scale = True)
            if joint_parent:
                cmds.parent(jnt_new, joint_parent)
            joint_parent = jnt_new
            joints_chain.append(jnt_new)
        cmds.setAttr(bp_joints[0] + '.visibility',0)
        return joints_chain

