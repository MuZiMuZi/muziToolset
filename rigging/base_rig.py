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

        # # 定义绑定模块的bp定位关节
        # self.arm_bp_joints = self.get_modular_bp_joints(self.arm_rig)
        # self.leg_bp_joints = self.get_modular_bp_joints(self.leg_rig)
        # self.neck_bp_joints = self.get_modular_bp_joints(self.neck_rig)
        # self.spine_bp_joints = self.get_modular_bp_joints(self.spine_rig)
        # self.foot_bp_joints = self.get_modular_bp_joints(self.foot_rig)

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

    def create_ribbon(self,bp_joints,joint_number = 5):
        """
        创建ribbon绑定系统

        Args:
            bp_joints： 摆放关节的名称
            side (str): ribbon's side
            description (str): ribbon's description
            index (int): ribbon's index
            joint_number (int): how many joints need to be attached to the ribbon, default is 9
        """
        bp_joints_obj = nameUtils.Name(name  = bp_joints[0])

        # 根据关节的边来获取偏移值
        if bp_joints_obj.side != 'r':
            offset_val = 1
        else:
            offset_val = -1

        # create groups
        ribbon_grp = cmds.createNode('transform', name = 'grp_{}_{}Ribbon_{:03d}'.format(bp_joints_obj.side, bp_joints.description, bp_joints.index))
        ribbon_ctrl_grp = cmds.createNode('transform',
                                          name = 'grp_{}_{}RibbonCtrls_{:03d}'.format(bp_joints_obj.side, bp_joints.description, bp_joints.index),
                                          parent = ribbon_grp)
        ribbon_jnt_grp = cmds.createNode('transform',
                                         name = 'grp_{}_{}RibbonJnts_{:03d}'.format(bp_joints_obj.side, bp_joints.description, bp_joints.index),
                                         parent = ribbon_grp)
        nodes_local_grp = cmds.createNode('transform',
                                          name = 'grp_{}_{}RibbonNodesLocal_{:03d}'.format(bp_joints_obj.side, bp_joints.description, bp_joints.index),
                                          parent = ribbon_grp)
        nodes_world_grp = cmds.createNode('transform',
                                          name = 'grp_{}_{}RibbonNodesWorld_{:03d}'.format(bp_joints_obj.side, bp_joints.description, bp_joints.index),
                                          parent = ribbon_grp)
        cmds.setAttr(nodes_world_grp + '.inheritsTransform', 0)

        cmds.setAttr(nodes_local_grp + '.visibility', 0)
        cmds.setAttr(nodes_world_grp + '.visibility', 0)

        # create temp curve to generate nurbs surface
        temp_curve = cmds.curve(point = [[-5 * offset_val, 0, 0], [5 * offset_val, 0, 0]], knot = [0, 1], degree = 1)
        # rebuild curve base on joints number
        cmds.rebuildCurve(temp_curve, degree = 3, replaceOriginal = True, rebuildType = 0, endKnots = 1, keepRange = 0,
                          keepControlPoints = False, keepEndPoints = True, keepTangents = False,
                          spans = joint_number + 1)
        # duplicate the curve
        temp_curve_02 = cmds.duplicate(temp_curve)[0]
        # offset curves so we can loft later
        cmds.setAttr(temp_curve + '.translateZ', 1)
        cmds.setAttr(temp_curve_02 + '.translateZ', -1)

        # loft surface
        surf = \
        cmds.loft(temp_curve_02, temp_curve, constructionHistory = False, uniform = True, degree = 3, sectionSpans = 1,
                  range = False, polygon = 0, name = 'surf_{}_{}Ribbon_{:03d}'.format(bp_joints_obj.side, bp_joints.description, bp_joints.index))[0]
        cmds.parent(surf, nodes_local_grp)

        # get surface shapes node
        surf_shape = cmds.listRelatives(surf, shapes = True)[0]

        # delete temps curves
        cmds.delete(temp_curve, temp_curve_02)

        # create joints and attach to surface
        fol_grp = cmds.createNode('transform',
                                  name = 'grp_{}_{}RibbonFollicles_{:03d}'.format(bp_joints_obj.side, bp_joints.description, bp_joints.index),
                                  parent = nodes_world_grp)

        for i in range(joint_number):
            # create follicle
            fol_shape = cmds.createNode('follicle',
                                        name = 'fol_{}_{}Ribbon{:03d}_{:03d}Shape'.format(bp_joints_obj.side, bp_joints.description, i + 1,
                                                                                          bp_joints.index))
            # rename transform node
            fol = cmds.listRelatives(fol_shape, parent = True)[0]
            fol = cmds.rename(fol, fol_shape[:-5])
            # parent to follicle group
            cmds.parent(fol, fol_grp)
            # connect follicle
            cmds.connectAttr(surf_shape + '.worldSpace[0]', fol_shape + '.inputSurface')
            # connect follicle shape to transform
            cmds.connectAttr(fol_shape + '.outTranslate', fol + '.translate')
            cmds.connectAttr(fol_shape + '.outRotate', fol + '.rotate')
            # set uv value
            cmds.setAttr(fol_shape + '.parameterU', 0.5)
            cmds.setAttr(fol_shape + '.parameterV', float(i) / (joint_number - 1))

            # create joint
            jnt = cmds.createNode('joint',
                                  name = 'jnt_{}_{}Ribbon{:03d}_{:03d}'.format(bp_joints_obj.side, bp_joints.description, i + 1,
                                                                                          bp_joints.index))
            parent_grp = ribbon_jnt_grp
            grp_nodes = []
            for node_type in ['zero', 'offset']:
                grp = cmds.createNode('transform', name = jnt.replace('jnt', node_type), parent = parent_grp)
                grp_nodes.append(grp)
                parent_grp = grp

            cmds.parent(jnt, grp_nodes[-1])
            # constraint joint with follicle
            cmds.parentConstraint(fol, grp_nodes[0], maintainOffset = False)
            # set offset group orientation back to zero
            cmds.xform(grp_nodes[1], rotation = [0, 0, 0], worldSpace = True)

        # create controller
        ctrls = []
        for pos in ['start', 'end', 'mid']:
            ctrl = create_ctrl(description + pos.title(),
                               side,
                               index,
                               shape = 'Square',
                               shape_scale = 1.5,
                               cvs_pos = None,
                               axis = 'Z+',
                               pos = jnt,
                               lock_attrs = [],
                               parent = None,
                               animation_set = 'body_Ctrls_Set')
            ctrls.append(ctrl)
            ctrl_zero = nameUtils.Name(name = ctrl)
            ctrl_zero.type = 'zero'
            cmds.parent(ctrl_zero.name, ribbon_ctrl_grp)
        # place controllers
        cmds.setAttr(ctrls[0].replace('ctrl', 'zero') + '.translateX', -5 * offset_val)
        cmds.setAttr(ctrls[1].replace('ctrl', 'zero') + '.translateX', 5 * offset_val)
        cmds.setAttr(ctrls[0].replace('ctrl', 'zero') + '.visibility', 0)
        cmds.setAttr(ctrls[1].replace('ctrl', 'zero') + '.visibility', 0)

        # constraint mid control
        cmds.pointConstraint(ctrls[0], ctrls[1], ctrls[-1].replace('ctrl', 'driven'), maintainOffset = False)

        # add twist
        cmds.addAttr(ctrls[0], longName = 'twist', attributeType = 'float', keyable = True)
        cmds.addAttr(ctrls[1], longName = 'twist', attributeType = 'float', keyable = True)
        # twist deformer
        twist_node, twist_hnd = cmds.nonLinear(surf, type = 'twist', name = surf.replace('surf', 'twist'))
        cmds.parent(twist_hnd, nodes_local_grp)
        cmds.setAttr(twist_hnd + '.rotate', 0, 0, 90)
        scale_val = cmds.getAttr(twist_hnd + '.scaleX')
        cmds.setAttr(twist_hnd + '.scale', scale_val * offset_val, scale_val * offset_val, scale_val * offset_val)
        # connect twist attr
        twist_hnd_shape = cmds.listRelatives(twist_hnd, shapes = True)[0]
        cmds.connectAttr(ctrls[0] + '.twist', twist_node + '.endAngle')
        cmds.connectAttr(ctrls[1] + '.twist', twist_node + '.startAngle')

        # add sine
        cmds.addAttr(ctrls[-1], longName = 'sineDivider', niceName = 'SINE ----------', attributeType = 'enum',
                     enumName = ' ', keyable = False)
        cmds.setAttr(ctrls[-1] + '.sineDivider', channelBox = True, lock = True)
        cmds.addAttr(ctrls[-1], longName = 'amplitude', attributeType = 'float', keyable = True, minValue = 0)
        cmds.addAttr(ctrls[-1], longName = 'wavelength', attributeType = 'float', keyable = True, minValue = 0.1,
                     defaultValue = 2)
        cmds.addAttr(ctrls[-1], longName = 'offset', attributeType = 'float', keyable = True)
        cmds.addAttr(ctrls[-1], longName = 'sineRotation', attributeType = 'float', keyable = True)
        # sine deformer
        sine_node, sine_hnd = cmds.nonLinear(surf, type = 'sine', name = surf.replace('surf', 'sine'))
        cmds.parent(sine_hnd, nodes_local_grp)
        cmds.setAttr(sine_hnd + '.rotate', 0, 0, 90)
        scale_val = cmds.getAttr(sine_hnd + '.scaleX')
        cmds.setAttr(sine_hnd + '.scale', scale_val * offset_val, scale_val * offset_val, scale_val * offset_val)
        cmds.setAttr(sine_node + '.dropoff', 1)
        # connect sine attr
        sine_hnd_shape = cmds.listRelatives(sine_hnd, shapes = True)[0]
        cmds.connectAttr(ctrls[-1] + '.amplitude', sine_node + '.amplitude')
        cmds.connectAttr(ctrls[-1] + '.wavelength', sine_node + '.wavelength')
        cmds.connectAttr(ctrls[-1] + '.offset', sine_node + '.offset')
        cmds.connectAttr(ctrls[-1] + '.sineRotation', sine_hnd + '.rotateY')

        # wire deformer
        # create curve
        wire_curve = cmds.curve(point = [[-5 * offset_val, 0, 0], [0, 0, 0], [5 * offset_val, 0, 0]],
                                knot = [0, 0, 1, 1],
                                degree = 2, name = 'crv_{}_{}RibbonWire_{:03d}'.format(side, description, index))
        wire_curve_shape = cmds.listRelatives(wire_curve, shapes = True)[0]
        cmds.rename(wire_curve_shape, wire_curve + 'Shape')
        cmds.parent(wire_curve, nodes_world_grp)

        # create clusters
        for ctrl, i in zip(ctrls, [0, 2, 1]):
            cls_node, cls_hnd = cmds.cluster('{}.cv[{}]'.format(wire_curve, i), name = ctrl.replace('ctrl', 'cls'))
            cmds.parent(cls_hnd, nodes_world_grp)
            cmds.pointConstraint(ctrl, cls_hnd, maintainOffset = False)

        # create wire deformer
        wire_node = surf.replace('surf', 'wire')
        cmds.wire(surf, wire = wire_curve, name = wire_node)
        cmds.setAttr(wire_node + '.dropoffDistance[0]', 200)
        cmds.parent(wire_curve + 'BaseWire', nodes_local_grp)

        Controls = 'Controls'
        Joints = 'Joints'
        RigNodes_Local = 'RigNodesLocal'
        RigNodes_World = 'RigNodesWorld'
        cmds.parent(ribbon_ctrl_grp, Controls)
        cmds.parent(ribbon_jnt_grp, Joints)
        cmds.parent(nodes_local_grp, RigNodes_Local)
        cmds.parent(nodes_world_grp, RigNodes_World)
        cmds.delete(ribbon_grp)

        return ribbon_grp, ribbon_ctrl_grp, ribbon_jnt_grp, nodes_local_grp, nodes_world_grp
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
