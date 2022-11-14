# coding=utf-8

u"""
这是一个用来编写ikfk混合绑定的类，之后的绑定都会在这个类的基础上逐级继承下去
继承了ik_rig 和 fk_rig

目前已有的功能：

create_ikfk_chain_rig：创建ikfk关节链混合的绑定

ikfk_chain_rig：创建混合IKFk链的bind链控制器绑定

ikfk_spine_rig： 创建IK样条曲线（脊椎和脖子的绑定）和FK关节链的混合绑定

ribbon_Rig ： 创建ribbon关节的绑定


"""

import maya.cmds as cmds
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.pipelineUtils as pipelineUtils

import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.jointUtils as jointUtils

import base_rig
import ik_rig
import fk_rig



reload(controlUtils)
reload(base_rig)
reload(ik_rig)
reload(fk_rig)



class IKFK_Rig(ik_rig.IK_Rig, fk_rig.FK_Rig):
    def __init__(self, bp_joints = None, joint_parent = None, control_parent = None, mirror = True):
        super(IKFK_Rig, self).__init__(bp_joints = bp_joints, joint_parent=joint_parent,control_parent = control_parent)
        self.mirror = mirror

    def create_ikfk_chain_rig(self):
        u"""
        创建ikfk关节链混合的绑定
        """
        jnt_name = nameUtils.Name(name = self.bp_joints[0])
        if self.mirror and jnt_name.side == 'l':
            self.make(self.bp_joints)
            self.bp_joints_mirror = cmds.mirrorJoint(self.bp_joints[0], mirrorYZ = True, mirrorBehavior = True,
                                                     searchReplace = ['_l_', '_r_'])
            if self.joint_parent:
                self.joint_parent_mirror = self.joint_parent.replace('_l_', '_r_')
            else:
                self.joint_parent = self.jnt_grp
                self.joint_parent_mirror = self.jnt_grp.replace('_l_', '_r_')
            if self.control_parent:
                self.control_parent_mirror = self.control_parent.replace('_l_', '_r_')
            else:
                self.control_parent = self.control_grp
                self.control_parent_mirror = self.control_grp.replace('_l_', '_r_')
            # 创建_l_边的手臂的fk，ik，ikfk融合的绑定
            self.fk_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'FK',
                                                          joint_parent = self.jnt_grp)
            self.fk_chain_rig(self.fk_chain, self.control_parent)
            self.ik_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'IK',
                                                          joint_parent = self.jnt_grp)
            self.ik_chain_rig(self.ik_chain, self.control_parent)
            self.ikfk_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'Bind',
                                                            joint_parent = self.jnt_grp)
            self.ikfk_chain_rig(self.fk_chain, self.ik_chain, self.ikfk_chain, self.control_parent)
            # 创建_r_边的手臂的fk，ik，ikfk融合的绑定
            self.make(self.bp_joints_mirror)
            self.fk_chain_mirror = jointUtils.Joint.create_chain(self.bp_joints_mirror, suffix = 'FK',
                                                                 joint_parent = self.jnt_grp)
            self.fk_chain_rig(self.fk_chain_mirror, self.control_parent_mirror)
            self.ik_chain_mirror = jointUtils.Joint.create_chain(self.bp_joints_mirror, suffix = 'IK',
                                                                 joint_parent = self.jnt_grp)
            self.ik_chain_rig(self.ik_chain_mirror, self.control_parent_mirror)
            self.ikfk_chain_mirror = jointUtils.Joint.create_chain(self.bp_joints_mirror, suffix = 'Bind',
                                                                   joint_parent = self.joint_parent_mirror)

            self.ikfk_chain_rig(self.fk_chain_mirror, self.ik_chain_mirror, self.ikfk_chain_mirror,
                                self.control_parent_mirror)
        else:
            self.make(self.bp_joints)
            self.fk_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'FK',
                                                          joint_parent = self.jnt_grp)
            self.fk_chain_rig(self.fk_chain, self.control_parent)
            self.ik_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'IK',
                                                          joint_parent = self.jnt_grp)
            self.ik_chain_rig(self.ik_chain, self.control_parent)
            self.ikfk_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'Bind',
                                                            joint_parent = self.jnt_grp)
            self.ikfk_chain_rig(self.fk_chain, self.ik_chain, self.ikfk_chain, self.control_parent)

    def ikfk_chain_rig(self, fk_chain, ik_chain, ikfk_chain, control_parent):
        u"""
        创建混合IKFk链的bind链控制器绑定
        Args:
            control_parent(str): 控制器组的父层级

        Returns: ik_ctrl_grp ：ikfkBend控制器的最顶层

        """
        # 获取创建控制器的关节的名称
        name_obj = nameUtils.Name(name = ikfk_chain[0])

        # 创建bind_jnt 关节的集合
        bind_jnt_set = 'set_bindJnt'
        make_bind_jnt_set = 'set_' + name_obj.side + '_' + name_obj.description + 'Jnt'
        make_bind_jnt_set = cmds.sets(name = make_bind_jnt_set, empty = True)
        if bind_jnt_set:
            bind_jnt_set = bind_jnt_set
        if not cmds.objExists(bind_jnt_set) or cmds.nodeType(bind_jnt_set) != 'objectSet':
            bind_jnt_set = cmds.sets(name = bind_jnt_set, empty = True)
        for jnt in ikfk_chain:
            cmds.sets(make_bind_jnt_set, edit = True, forceElement = bind_jnt_set)
            cmds.sets(jnt, edit = True, forceElement = make_bind_jnt_set)

        # 获取创建控制器的关节的名称
        name_obj.type = 'ctrl'
        name_obj.description = name_obj.description + 'IKFKBend'
        # 创建ikfk切换的控制器
        IkFkBend_ctrl_obj = controlUtils.Control.create_ctrl(name_obj.name, shape = 'pPlatonic', radius = 10,
                                                             axis = 'X+',
                                                             pos = ikfk_chain[0], parent = None)
        IkFkBend_ctrl = name_obj.name
        IkFkBend_zero = IkFkBend_ctrl.replace('ctrl_', 'zero_')
        cmds.move(0, 15, 15, IkFkBend_zero, r = True, ls = True, wd = True)
        cmds.addAttr(IkFkBend_ctrl, longName = 'IkFkBend', attributeType = 'double', min = 0, max = 1, defaultValue = 1,
                     keyable = True)
        IkFkBend_grp = hierarchyUtils.Hierarchy.add_extra_group(obj = IkFkBend_zero,
                                                                grp_name = IkFkBend_zero.replace('zero_', 'grp_'),
                                                                world_orient = False)
        # 锁定不需要的属性
        for channel in ['t', 'r', 's']:

            for axis in ['x', 'y', 'z']:
                cmds.setAttr(IkFkBend_ctrl + '.' + channel + axis, l = True, k = False, cb = False)
        cmds.setAttr(IkFkBend_ctrl + '.v', l = True, k = False, cb = False)
        cmds.setAttr(IkFkBend_ctrl + '.ro', l = True, k = False, cb = False)
        cmds.setAttr(IkFkBend_ctrl + '.subCtrlVis', l = True, k = False, cb = False)

        # 用混合颜色节点来制作fk/ik开关
        # 连接切换
        for fk, ik, bind in zip(fk_chain, ik_chain, ikfk_chain):
            for attr in ['translate', 'rotate', 'scale']:
                blend_node = cmds.createNode('blendColors', name = 'blend_{}_{}_001'.format(name_obj.side,
                                                                                            name_obj.description))
                cmds.connectAttr(fk + '.{}'.format(attr), blend_node + '.color1')
                cmds.connectAttr(ik + '.{}'.format(attr), blend_node + '.color2')
                cmds.connectAttr(IkFkBend_ctrl + '.IkFkBend', blend_node + '.blender')
                cmds.connectAttr(blend_node + '.output', bind + '.{}'.format(attr))
        fk_ctrl_grp = fk_chain[0].replace('jnt_', 'grp_')
        ik_ctrl_grp = ik_chain[0].replace('jnt_', 'grp_')
        cmds.connectAttr(blend_node + '.blender', fk_ctrl_grp + '.visibility')
        reverse_node = cmds.createNode('reverse', name = blend_node.replace('blend_node_', 'reverse_'))
        cmds.connectAttr(blend_node + '.blender', reverse_node + '.inputX')
        cmds.connectAttr(reverse_node + '.outputX', ik_ctrl_grp + '.visibility')

        hierarchyUtils.Hierarchy.parent(child_node = IkFkBend_grp, parent_node = control_parent)

    def ikfk_spine_rig(self):
        u"""
        创建IK样条曲线（脊椎和脖子的绑定）和FK关节链的混合绑定
        """
        self.make(self.bp_joints)
        self.fk_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'FK',
                                                      joint_parent = self.jnt_grp)
        self.fk_chain_rig(self.fk_chain, self.control_grp)
        self.ik_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'IK',
                                                      joint_parent = self.jnt_grp)
        self.ik_spine_rig(self.ik_chain, self.control_grp)
        self.ikfk_chain = jointUtils.Joint.create_chain(self.bp_joints, suffix = 'Bind',
                                                        joint_parent = self.jnt_grp)
        self.ikfk_chain_rig(self.fk_chain, self.ik_chain, self.ikfk_chain, self.control_grp)

    def ribbon_Rig(self,ikfk_chain,control_parent,joint_number):
        u"""
              创建ribbon关节的绑定
              """
        upper_part = nameUtils.Name(name = ikfk_chain[0])
        lower_part = nameUtils.Name(name = ikfk_chain[1])
        # 创建ribbon关节和twist关节
        controlUtils.Control.create_ribbon(upper_part.name, control_parent,joint_number = joint_number)
        controlUtils.Control.create_ribbon(lower_part.name ,control_parent,joint_number = joint_number)

        # 吸附带控制器组的位置和旋转
        ribbon_upper_start_driven = 'driven_{}_{}Start_001'.format(upper_part.side, upper_part.description)
        ribbon_upper_Mid_driven = 'driven_{}_{}Mid_001'.format(upper_part.side, upper_part.description)
        ribbon_upper_End_driven = 'driven_{}_{}End_001'.format(upper_part.side, upper_part.description)

        ribbon_lower_start_driven = 'driven_{}_{}Start_001'.format(lower_part.side, lower_part.description)
        ribbon_lower_Mid_driven = 'driven_{}_{}Mid_001'.format(lower_part.side, lower_part.description)
        ribbon_lower_End_driven = 'driven_{}_{}End_001'.format(lower_part.side, lower_part.description)

        # 关节约束对应的控制器组

        cmds.parentConstraint(ikfk_chain[0], ribbon_upper_start_driven, maintainOffset = False)
        cmds.parentConstraint(ikfk_chain[1], ribbon_upper_End_driven, maintainOffset = False)

        cmds.parentConstraint(ikfk_chain[1], ribbon_lower_End_driven, maintainOffset = False)
        cmds.parentConstraint(ikfk_chain[2], ribbon_lower_start_driven, maintainOffset = False)