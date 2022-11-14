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

import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.nameUtils as nameUtils

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
        super(Base_Rig, self).__init__()
        # self.side = None
        # if self.side == 'l':
        #     self.side_value = 1
        # elif self.side == 'r':
        #     self.side_value = -1

        # 定义世界的层级组架构
        self.character_ctrl = 'ctrl_m_character_001'
        self.world_ctrl = 'ctrl_m_world_001'
        self.cog_ctrl = 'ctrl_m_cog_001'
        self.custom_ctrl = 'ctrl_m_custom_001'

        self.group = 'group'
        self.geometry = 'geometry'
        self.control = 'control'
        self.custom = 'custom'

        self.rigNode = 'rigNode'
        self.joint = 'joint'
        self.rigNode_Local = 'rigNode_Local'
        self.rigNode_World = 'rigNode_World'
        self.nCloth = 'nCloth'
        self.modular_rig = 'modular_rig'

        self.low_modle_grp = 'grp_m_low_modle_001'
        self.mid_modle_grp = 'grp_m_mid_modle_001'
        self.high_modle_grp = 'grp_m_high_modle_001'

        self.rig_ctrl = [self.character_ctrl, self.cog_ctrl, self.custom_ctrl]
        self.rig_hierarchy_grp = [self.group, self.geometry, self.control, self.custom, self.rigNode, self.joint,
                                  self.rigNode_Local, self.rigNode_World, self.nCloth,
                                  self.modular_rig, self.low_modle_grp, self.mid_modle_grp, self.high_modle_grp]

        # 定义绑定模块

        self.arm_rig = 'arm_rig'
        self.hand_rig = 'hand_rig'
        self.leg_rig = 'leg_rig'
        self.foot_rig = 'foot_rig'
        self.neck_rig = 'neck_rig'
        self.spine_rig = 'spine_rig'
        self.modular_rig_list = [self.arm_rig, self.hand_rig, self.leg_rig, self.foot_rig, self.neck_rig,
                                 self.spine_rig]

        # # 定义绑定模块的bp定位关节
        # self.arm_bp_joints = self.get_modular_bp_joints(self.arm_rig)
        # self.leg_bp_joints = self.get_modular_bp_joints(self.leg_rig)
        # self.neck_bp_joints = self.get_modular_bp_joints(self.neck_rig)
        # self.spine_bp_joints = self.get_modular_bp_joints(self.spine_rig)
        # self.foot_bp_joints = self.get_modular_bp_joints(self.foot_rig)

        self.rig_top_grp = 'group'
        if not cmds.objExists(self.rig_top_grp):
            self.default_grp()

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
        # 根据self.rig_hierarchy_grp 来创建对应的层级组
        for transform in self.rig_hierarchy_grp:
            cmds.createNode('transform', name = transform)


        # 制作层级关系
        cmds.parent(self.geometry, self.custom, self.control, self.group)

        # 创建RigNode层级下的子层级组并做层级关系
        cmds.parent(self.rigNode_Local, self.rigNode_World, self.rigNode)
        cmds.parent(self.rigNode, self.joint, self.nCloth, self.modular_rig, self.custom)

        # 创建Modle层级下的子层级组并且做层级关系
        cmds.parent(self.low_modle_grp, self.mid_modle_grp, self.high_modle_grp, self.geometry)
        attrs_list = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.scaleX',
                      '.scaleY',
                      '.scaleZ', '.visibility', '.rotateOrder', '.subCtrlVis']
        # 创建总控制器Character
        controlUtils.Control.create_ctrl(self.character_ctrl, shape = 'circle', radius = 40,
                                                              axis = 'X+',
                                                              pos = None,
                                                              parent = self.control)
        cmds.addAttr(self.character_ctrl, longName = 'RigScale', niceName = u'绑定缩放', at = 'double', dv = 1,
                     keyable = True)
        for attr in ['.scaleX', '.scaleY', '.scaleZ']:
            cmds.connectAttr(self.character_ctrl + '.RigScale', self.character_ctrl + attr)
            cmds.setAttr(self.character_ctrl + attr, lock = True, keyable = False, channelBox = False)


        # 创建世界控制器
        controlUtils.Control.create_ctrl(self.world_ctrl, shape = 'local', radius = 35, axis = 'Z-',
                                                          pos = None,
                                                          parent = self.character_ctrl.replace('ctrl_','output_'))

        controlUtils.Control.create_ctrl(self.cog_ctrl, shape = 'circle', radius = 20, axis = 'X+',
                                                        pos = None,
                                                        parent = self.world_ctrl.replace('ctrl_','output_'))
        # 创建一个自定义的控制器，用来承载自定义的属性
        controlUtils.Control.create_ctrl(self.custom_ctrl, shape = 'cross', radius = 3, axis = 'X+',
                                                         pos = None,
                                                         parent = self.custom)
        cmds.parentConstraint(self.character_ctrl, self.custom_ctrl, mo = True)
        cmds.scaleConstraint(self.character_ctrl, self.custom_ctrl, mo = True)

        # 创建自定义的控制器属性
        for attr in ['GeometryVis', 'ControlsVis', 'RigNodesVis', 'JointsVis']:
            if not cmds.objExists('{}.{}'.format(self.custom_ctrl, attr)):
                cmds.addAttr(self.custom_ctrl, ln = attr, at = 'bool', dv = 1, keyable = True)

        # 添加精度切换的属性
        if not cmds.objExists('{}.Resolution'.format(self.custom_ctrl)):
            cmds.addAttr(self.custom_ctrl, ln = 'Resolution', at = 'enum', en = 'low:mid:high', keyable = True)
            for idx, res in {0: 'low', 1: 'mid', 2: 'high'}.items():
                cnd_node = 'resolution_{}_conditionNode'.format(res)
                if not cmds.objExists(cnd_node):
                    cnd_node = cmds.createNode('condition', n = cnd_node)
                cmds.connectAttr('{}.Resolution'.format(self.custom_ctrl), '{}.firstTerm'.format(cnd_node), f = True)
                cmds.setAttr('{}.secondTerm'.format(cnd_node), idx)
                cmds.setAttr('{}.colorIfTrueR'.format(cnd_node), 1)
                cmds.setAttr('{}.colorIfFalseR'.format(cnd_node), 0)
                cmds.connectAttr('{}.outColorR'.format(cnd_node), 'grp_m_{}_modle_001.visibility'.format(res), f = True)

        # 添加模型显示方式的属性
        if not cmds.objExists('{}.GeometryDisplayType'.format(self.character_ctrl)):
            cmds.addAttr(self.custom_ctrl, ln = 'GeometryDisplayType', at = 'enum', en = 'Normal:Template:Reference',
                         keyable = True)

        # 连接各个组的显示属性
        custom_ctrl_attrs = ['.GeometryVis','.ControlsVis','.RigNodesVis','.JointsVis']
        hierarchy_grp = [self.geometry,self.control,self.rigNode,self.joint]
        for attrs ,grp in zip(custom_ctrl_attrs,hierarchy_grp):
            cmds.connectAttr(self.custom_ctrl+ '{}'.format(attrs), '{}.visibility'.format(grp))
        # 连接模型的可编辑属性
        cmds.setAttr(self.geometry + '.overrideDisplayType', 2)
        cmds.connectAttr('{}.GeometryDisplayType'.format(self.custom_ctrl), self.geometry + '.overrideEnabled', f = True)

        # 显示和隐藏属性
        for attr in attrs_list:
            cmds.setAttr(self.custom_ctrl + attr, l = True, k = False, cb = False)

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
                                      parent = self.cog_ctrl.replace('ctrl_','output_'))
        self.jnt_grp = cmds.group(name = main_obj.name.replace('RigModule', 'Jnt'), em = True,
                                  parent = self.joint)
        # self.rigNodes_Local_grp = cmds.group(name = main_obj.name.replace('RigModule', 'RigNodesLocal'), em = True, parent = 'RigNodesLocal')
        # self.rigNodes_World_grp = cmds.group(name = main_obj.name.replace('RigModule', 'RigNodesWorld'), em = True, parent = 'RigNodesWorld')
