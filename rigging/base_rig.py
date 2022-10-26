# coding=utf-8

u"""
这是一个用来编写自动绑定系统的基础类，之后的绑定都会在这个类的基础上逐级继承下去

目前已有的功能：

get_modular_bp_joints：根据给定关节模块的名称来获取对应的模块组关节的名称

default_grp：创建绑定的初始层级组，并隐藏连接对应的属性

setup: 绑定生成的预设步骤，导入对应的模型和关节结构

make： 根据给定的bp_joints关节的名称来创建对应的模块组

"""

import maya.cmds as cmds

import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.pipelineUtils as pipelineUtils

import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.jointUtils as jointUtils

reload(pipelineUtils)
reload(jointUtils)

skeletonPath = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton'

troll_model = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/model/troll_model.ma'
biped_skeleton = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/biped_skeleton.ma'

arm_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/arm_rig.ma'
hand_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/hand_rig.ma'
leg_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/leg_rig.ma'
foot_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/foot_rig.ma'
neck_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/neck_rig.ma'
spine_rig = 'C:/Users/lixin/Documents/maya/scripts/muziToolset/rigging/skeleton/spine_rig.ma'

modular_rig = [arm_rig, hand_rig, leg_rig, foot_rig, neck_rig, spine_rig]


class Base_Rig(object):

    def __init__(self):
        self.rig_top_grp = 'Group'
        if not cmds.objExists(self.rig_top_grp):
            self.default_grp()

        # self.side = None
        # if self.side == 'l':
        #     self.side_value = 1
        # elif self.side == 'r':
        #     self.side_value = -1

        # 定义世界的层级组架构
        self.Group = 'Group'
        self.Geometry = 'Geometry'
        self.Control = 'Control'
        self.Custom = 'Custom'

        self.RigNodes = 'RigNodes'
        self.Joints = 'Joints'
        self.RigNodes_Local = 'RigNodesLocal'
        self.RigNodes_World = 'RigNodesWorld'
        self.nCloth_geo_grp = 'nCloth_geo_grp'
        self.modular_rig = 'modular_rig'

        self.Low_modle_grp = 'grp_m_low_Modle_001'
        self.Mid_modle_grp = 'grp_m_mid_Modle_001'
        self.High_modle_grp = 'grp_m_high_Modle_001'

        self.cog_ctrl = 'ctrl_m_cog_001'

        self.lock_ctrl = 'ctrl_m_custom_001'

        # 定义绑定模块

        self.arm_rig = 'arm_rig'
        self.hand_rig = 'hand_rig'
        self.leg_rig = 'leg_rig'
        self.foot_rig = 'foot_rig'
        self.neck_rig = 'neck_rig'
        self.spine_rig = 'spine_rig'
        self.modular_rig_list = [self.arm_rig, self.hand_rig, self.leg_rig, self.foot_rig, self.neck_rig,
                                 self.spine_rig]

        # 定义绑定模块的bp定位关节
        self.arm_bp_joints = self.get_modular_bp_joints(self.arm_rig)
        self.leg_bp_joints = self.get_modular_bp_joints(self.leg_rig)
        self.neck_bp_joints = self.get_modular_bp_joints(self.neck_rig)
        self.spine_bp_joints = self.get_modular_bp_joints(self.spine_rig)
        self.foot_bp_joints = self.get_modular_bp_joints(self.foot_rig)

    def get_modular_bp_joints(self, modular):
        u"""
        根据给定关节模块的名称来获取对应的模块组关节的名称
        """
        modular_bp_joints = cmds.listRelatives(modular, ad = True, c = True)
        modular_bp_joints.reverse()
        return modular_bp_joints

    def default_grp(self):
        u'''
        创建绑定的初始层级组，并隐藏连接对应的属性
        '''
        # 创建顶层的Group组
        self.Group = cmds.createNode('transform', name = 'Group')

        # 创建Group层级下的子层级组，并做层级关系
        self.Geometry = cmds.createNode('transform', name = 'Geometry')
        self.Control = cmds.createNode('transform', name = 'Control')
        self.Custom = cmds.createNode('transform', name = 'Custom')
        cmds.parent(self.Geometry, self.Custom, self.Control, self.Group)

        # 创建RigNode层级下的子层级组并做层级关系
        self.RigNodes = cmds.createNode('transform', name = 'RigNodes')
        self.Joints = cmds.createNode('transform', name = 'Joints')
        self.RigNodes_Local = cmds.createNode('transform', name = 'RigNodesLocal')
        self.RigNodes_World = cmds.createNode('transform', name = 'RigNodesWorld')
        self.nCloth_geo_grp = cmds.createNode('transform', name = 'nCloth_geo_grp')
        self.modular_rig = cmds.createNode('transform', name = 'modular_rig')
        cmds.parent(self.RigNodes_Local, self.RigNodes_World, self.RigNodes)
        cmds.parent(self.RigNodes, self.Joints, self.nCloth_geo_grp, self.modular_rig, self.Custom)

        # 创建Modle层级下的子层级组并且做层级关系
        self.Low_modle_grp = cmds.createNode('transform', name = 'grp_m_low_Modle_001')
        self.Mid_modle_grp = cmds.createNode('transform', name = 'grp_m_mid_Modle_001')
        self.High_modle_grp = cmds.createNode('transform', name = 'grp_m_high_Modle_001')
        cmds.parent(self.Low_modle_grp, self.Mid_modle_grp, self.High_modle_grp, self.Geometry)

        World_zero = [self.Group, self.Geometry, self.RigNodes_Local, self.RigNodes_World, self.RigNodes, self.Control,
                      self.Joints, self.Custom]
        attrs_list = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.scaleX',
                      '.scaleY',
                      '.scaleZ', '.visibility', '.rotateOrder', '.subCtrlVis']
        # 创建总控制器Character
        character_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_Character_001', shape = 'circle', radius = 40,
                                                              axis = 'X+',
                                                              pos = None,
                                                              parent = self.Control)

        # 创建世界控制器
        world_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_world_001', shape = 'local', radius = 35, axis = 'Z-',
                                                          pos = None,
                                                          parent = 'ctrl_m_Character_001')

        cog_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_cog_001', shape = 'circle', radius = 20, axis = 'X+',
                                                        pos = None,
                                                        parent = 'output_m_world_001')
        self.cog_ctrl = 'ctrl_m_cog_001'
        # 创建一个自定义的控制器，用来承载自定义的属性
        lock_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_custom_001', shape = 'cross', radius = 3, axis = 'X+',
                                                         pos = None,
                                                         parent = self.Custom)
        self.lock_ctrl = 'ctrl_m_custom_001'
        cmds.parentConstraint('ctrl_m_Character_001', self.lock_ctrl, mo = True)
        cmds.scaleConstraint('ctrl_m_Character_001', self.lock_ctrl, mo = True)

        # 创建自定义的控制器属性
        for attr in ['GeometryVis', 'ControlsVis', 'RigNodesVis', 'JointsVis']:
            if not cmds.objExists('{}.{}'.format(self.lock_ctrl, attr)):
                cmds.addAttr(self.lock_ctrl, ln = attr, at = 'bool', dv = 1, keyable = True)

        # 添加精度切换的属性
        if not cmds.objExists('{}.Resolution'.format(self.lock_ctrl)):
            cmds.addAttr(self.lock_ctrl, ln = 'Resolution', at = 'enum', en = 'low:mid:high', keyable = True)
            for idx, res in {0: 'low', 1: 'mid', 2: 'high'}.items():
                cnd_node = 'resolution_{}_conditionNode'.format(res)
                if not cmds.objExists(cnd_node):
                    cnd_node = cmds.createNode('condition', n = cnd_node)
                cmds.connectAttr('{}.Resolution'.format(self.lock_ctrl), '{}.firstTerm'.format(cnd_node), f = True)
                cmds.setAttr('{}.secondTerm'.format(cnd_node), idx)
                cmds.setAttr('{}.colorIfTrueR'.format(cnd_node), 1)
                cmds.setAttr('{}.colorIfFalseR'.format(cnd_node), 0)
                cmds.connectAttr('{}.outColorR'.format(cnd_node), 'grp_m_{}_Modle_001.visibility'.format(res), f = True)

        # 添加模型显示方式的属性
        if not cmds.objExists('{}.GeometryDisplayType'.format(self.lock_ctrl)):
            cmds.addAttr(self.lock_ctrl, ln = 'GeometryDisplayType', at = 'enum', en = 'Normal:Template:Reference',
                         keyable = True)

        # 连接 GeometryVis
        cmds.connectAttr('{}.GeometryVis'.format(self.lock_ctrl), '{}.visibility'.format(self.Geometry), f = True)

        # 连接 controlsVis
        cmds.connectAttr('{}.ControlsVis'.format(self.lock_ctrl), '{}.visibility'.format(self.Control), f = True)

        # 连接 RigNodesVis
        cmds.connectAttr('{}.RigNodesVis'.format(self.lock_ctrl), '{}.visibility'.format(self.RigNodes), f = True)

        # 连接 jointsVis
        cmds.connectAttr('{}.JointsVis'.format(self.lock_ctrl), '{}.visibility'.format(self.Joints), f = True)

        # 连接模型的可编辑属性
        cmds.setAttr(self.Geometry + '.overrideDisplayType', 2)
        cmds.connectAttr('{}.GeometryDisplayType'.format(self.lock_ctrl), self.Geometry + '.overrideEnabled', f = True)

        # 显示和隐藏属性
        for attr in attrs_list:
            cmds.setAttr(self.lock_ctrl + attr, l = True, k = False, cb = False)

    def setup(self):
        u'''
        绑定生成的预设步骤，导入对应的模型和关节结构
        '''
        # 导入模型
        # cmds.file(troll_model, i = True)

        # 导入关节结构
        for modular in modular_rig:
            cmds.file(modular, i = True)

        # 整理导入进来的关节结构和模型层级
        # rootJnt = 'root1_jnt'
        # cmds.parent(rootJnt, self.Joints)

    def make(self, bp_joints):
        u"""
        根据给定的bp_joints关节的名称来创建对应的模块组
        """
        main_obj = nameUtils.Name(name = bp_joints[0])
        main_obj.description = main_obj.description + 'RigModule'
        main_obj.type = 'grp'
        self.control_grp = cmds.group(name = main_obj.name.replace('RigModule', 'Ctrl'), em = True,
                                      parent = 'output_m_cog_001')
        self.jnt_grp = cmds.group(name = main_obj.name.replace('RigModule', 'Jnt'), em = True,
                                  parent = 'Joints')
        # self.rigNodes_Local_grp = cmds.group(name = main_obj.name.replace('RigModule', 'RigNodesLocal'), em = True, parent = 'RigNodesLocal')
        # self.rigNodes_World_grp = cmds.group(name = main_obj.name.replace('RigModule', 'RigNodesWorld'), em = True, parent = 'RigNodesWorld')

    # class test:
    #     def __init__(self, ikfk):
    #         self.ikfk = ikfk
    #
    #     def A(self):
    #         print(self.ikfk, "fkSYS")
    #
    #     def B(self):
    #         print(self.ikfk, "ikSYS")
    #
    # snap = "ik"
    #
    # if snap == 'ik':
    #     ddd = test(snap)
    #     ddd.A()
    # elif snap == 'fk':
    #     ddd = test(snap)
    #     ddd.A()
