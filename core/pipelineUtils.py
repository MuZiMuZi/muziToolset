# coding=utf-8
u"""
这是一个用来编写流程工具的类

目前已有的功能：

clear_keys: 清除场景内所有的关键帧
add_face_tag : 将“isFace”标记添加到所选物体的属性上
remove_non_face_objs：移除没有带“isFace”标志的物体
copy_weight：复制蒙皮
rename_bs_sc：批量重命名对象的蒙皮和混合变形节点
distence_between：获取两个对象之间的距离.
add_extra_group：在对象上方添加一个额外的组.
reset_control：重置控制器上所有的数值.
list_operation：将两个列表的并集/差分/交集/对称_差分部分作为列表返回.
tag_joint：对选择的关节添加关节标签
batch_Constraints：选中多个物体，批量对物体进行约束
default_grp： 添加绑定的初始层级组，并隐藏连接对应的属性
create_constraints：快速创建约束
delete_constraints：删除所选择物体的所有约束节点
select_sub_objects：快速选择所选物体的所有子物体
"""
import math
from functools import wraps
import maya.cmds as cmds
import maya.mel as mel


import hierarchyUtils
import controlUtils
class Pipeline(object):
    def __init__(self):
        pass

    @staticmethod
    def clear_keys():
        u"""
        清除场景内所有的动画关键帧
        :return:
        """
        animCurves = cmds.ls(type = ['animCurveTA', 'animCurveTL', 'animCurveTU'])
        if animCurves:
            cmds.delete(animCurves)
            cmds.warning(u"已清除场景内所有的动画关键帧")
        else:
            cmds.warning(u"场景内没有动画关键帧")

    @staticmethod
    def add_face_tag():
        u"""将“isFace”标记添加到所选物体的属性上.

        """

        sel_to_tag_list = cmds.ls(sl = True)

        for sel in sel_to_tag_list:
            if not cmds.objExists('{}.isFace'.format(sel)):
                cmds.addAttr(sel, ln = 'isFace', at = 'bool', dv = 1)
                cmds.setAttr('{}.isFace'.format(sel), keyable = False, channelBox = False)

    @staticmethod
    def remove_non_face_objs():
        u"""“移除没有带face标志的物体.

        """

        assemblies = cmds.ls(assemblies = True)

        for assembly in assemblies:
            children = cmds.listRelatives(assembly, allDescendents = True, type = 'transform')
            if children:
                for child in children:
                    if not cmds.objExists('{}.isFace'.format(child)) or not cmds.getAttr('{}.isFace'.format(child)):
                        cmds.delete(child)

    @staticmethod
    def copy_weight():
        u'''

        Returns:复制蒙皮

        '''
        # 获取选择
        sel = cmds.ls(selection = True)

        source_mesh = sel[0]
        target_meshes = sel[1:]

        # 查询目标对象是否具有蒙皮信息
        for target_mesh in target_meshes:
            target_skin = mel.eval('findRelatedSkinCluster("' + target_mesh + '")')
            if target_skin:
                cmds.delete(target_skin)

        # 获取源对象的蒙皮信息
        source_skin = mel.eval('findRelatedSkinCluster("' + source_mesh + '")')

        # 获取源对象受影响的蒙皮信息
        source_joints = cmds.skinCluster(source_skin, query = True, influence = True)

        # 在每个目标对象中循环
        for target_mesh in target_meshes:
            # 用源关节绑定蒙皮
            target_skin = cmds.skinCluster(source_joints, target_mesh, toSelectedBones = True)[0]

            # 复制蒙皮权重
            cmds.copySkinWeights(sourceSkin = source_skin, destinationSkin = target_skin, noMirror = True,
                                 surfaceAssociation = 'closestPoint', influenceAssociation = ['label', 'oneToOne'])

            # 重命名对象蒙皮
            cmds.select(sel)
            Pipeline.rename_bs_sc()

    @staticmethod
    def rename_bs_sc():
        u'''
        批量重命名对象的蒙皮和混合变形节点
        '''
        geos = cmds.ls(sl = True)
        for geo in geos:
            geo_shape = cmds.listRelatives(geo, shapes = True)
            sc = cmds.listConnections(geo_shape, type = 'skinCluster')
            if sc:
                cmds.rename(sc, 'sc_{}'.format(geo))
            bs = cmds.listConnections(geo_shape, type = 'blendShape')
            if bs:
                cmds.rename(bs, 'bs_{}'.format(geo))

    @staticmethod
    def distence_between(node_a, node_b):
        u'''获取两个对象之间的距离.
        node_a(str): 对象a.
        node_b(str): 对象b.

        :return
        dist(float):两个对象之间的距离.
        '''
        point_a = cmds.xform(node_a, query = True, worldSpace = True, rotatePivot = True)
        point_b = cmds.xform(node_b, query = True, worldSpace = True, rotatePivot = True)
        dist = math.sqrt(sum([pow((b - a), 2) for b, a in zip(point_a, point_b)]))
        return dist

    @staticmethod
    def reset_control():
        u"""重置控制器上所有的数值.



         """
        ctrl_node = cmds.ls('ctrl_?_*_???')
        attrs = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
        scale_attrs = ['scaleX', 'scaleY', 'scaleZ']
        for ctrl in ctrl_node:
            for attr in attrs:
                lock_val = cmds.getAttr(ctrl + '.{}'.format(attr), lock = True)
                if lock_val == 0:
                    cmds.setAttr(ctrl + '.{}'.format(attr), 0)
                else:
                    pass
            for scale_attr in scale_attrs:
                lock_val = cmds.getAttr(ctrl + '.{}'.format(scale_attr), lock = True)
                if lock_val == 0:
                    cmds.setAttr(ctrl + '.{}'.format(scale_attr), 1)
                else:
                    pass
        ctrl_IKFKblend = cmds.ls('ctrl_?_*IKFKBend_???')
        for IKFKblend in ctrl_IKFKblend:
            cmds.setAttr(IKFKblend + '.IkFkBend', 1)

    @staticmethod
    def list_operation(list_a, list_b, operation = '|'):
        u"""将两个列表的并集/差分/交集/对称_差分部分作为列表返回.

        Args:
            list_a (list/None): 第一个列表.
            list_b (list/None): 第二个列表.
            operation (str): 运算符号为 '|', '&', '-', '^'.

        Returns:
            list: 作为列表的两个列表的并集/差分/交集/对称_差分部分.

        """

        # 如果无，则将无转换为[]空列表，仅用于操作
        if not list_a:
            list_a = []
        if not list_b:
            list_b = []

        set_a = set(list_a)
        set_b = set(list_b)

        if operation == '|':
            return list(set_a.union(set_b))
        elif operation == '&':
            return list(set_a.intersection(set_b))
        elif operation == '-':
            return list(set_a.difference(set_b))
        elif operation == '^':
            return list(set_a.symmetric_difference(set_b))

    @staticmethod
    def tag_joint():
        """
        tag joint base on its name

        Args:
            jnt (str): joint name
        """
        jnts = cmds.ls(type = 'joint')
        for jnt in jnts:
            name_parts = jnt.split('_')

            if name_parts[1] == 'l':
                side_index = 1
            elif name_parts[1] == 'r':
                side_index = 2
            else:
                side_index = 0

            cmds.setAttr(jnt + '.side', side_index)
            cmds.setAttr(jnt + '.type', 18)
            cmds.setAttr(jnt + '.otherType', name_parts[2] + name_parts[3], type = 'string')

    @staticmethod
    def batch_Constraints():
        u"""
        选择物体，批量制作约束
        """
        geos = cmds.ls(sl = True)
        for geo in geos:
            cmds.undoInfo(openChunk = True)  # 批量撤销的开头
            ctrl = controlUtils.Control(n = 'ctrl_' + geo, s = 'cube', r = 1)
            ctrl_transform = '{}'.format(ctrl.transform)
            sub_ctrl = controlUtils.Control(n = 'ctrlSub_' + geo, s = 'cube', r = 1 * 0.7)
            sub_ctrl.set_parent(ctrl.transform)
            sub_ctrl_transform = '{}'.format(sub_ctrl.transform)
            # 添加上层层级组
            offset_grp = hierarchyUtils.Hierarchy.add_extra_group(
                obj = ctrl_transform, grp_name = '{}'.format(ctrl_transform.replace('ctrl', 'offset')),
                world_orient = False)
            connect_grp = hierarchyUtils.Hierarchy.add_extra_group(
                obj = offset_grp, grp_name = offset_grp.replace('offset', 'connect'), world_orient = False)
            driven_grp = hierarchyUtils.Hierarchy.add_extra_group(
                obj = connect_grp, grp_name = connect_grp.replace('connect', 'driven'), world_orient = False)
            zero_grp = hierarchyUtils.Hierarchy.add_extra_group(
                obj = driven_grp, grp_name = driven_grp.replace('driven', 'zero'), world_orient = False)

            cmds.parentConstraint(sub_ctrl_transform, geo, mo = True)
            cmds.scaleConstraint(sub_ctrl_transform, geo, mo = True)
            cmds.addAttr(ctrl_transform,attributeType = 'bool', longName = 'subCtrlVis',niceName = U'次级控制器显示',keyable = True)
            cmds.connectAttr(ctrl_transform + '.subCtrlVis', sub_ctrl_transform + '.visibility')
            cmds.undoInfo(openChunk = False)  # 批量撤销的开头

    @staticmethod
    def default_grp():
        u'''
        添加绑定的初始层级组，并隐藏连接对应的属性
        '''
        # 创建顶层的Group组
        Group = cmds.createNode('transform', name = 'Group')

        # 创建Group层级下的子层级组，并做层级关系
        Geometry = cmds.createNode('transform', name = 'Geometry')
        Control = cmds.createNode('transform', name = 'Control')
        Custom = cmds.createNode('transform', name = 'Custom')
        cmds.parent(Geometry, Custom, Control, Group)

        # 创建RigNode层级下的子层级组并做层级关系
        RigNodes = cmds.createNode('transform', name = 'RigNodes')
        Joints = cmds.createNode('transform', name = 'Joints')
        RigNodes_Local = cmds.createNode('transform', name = 'RigNodesLocal')
        RigNodes_World = cmds.createNode('transform', name = 'RigNodesWorld')
        nCloth_geo_grp = cmds.createNode('transform', name = 'nCloth_geo_grp')
        cmds.parent(RigNodes_Local, RigNodes_World, RigNodes)
        cmds.parent(RigNodes, Joints, nCloth_geo_grp, Custom)

        # 创建Modle层级下的子层级组并且做层级关系
        Low_modle_grp = cmds.createNode('transform', name = 'grp_m_low_Modle_001')
        Mid_modle_grp = cmds.createNode('transform', name = 'grp_m_mid_Modle_001')
        High_modle_grp = cmds.createNode('transform', name = 'grp_m_high_Modle_001')
        cmds.parent(Low_modle_grp, Mid_modle_grp, High_modle_grp, Geometry)

        World_zero = [Group, Geometry, RigNodes_Local, RigNodes_World, RigNodes, Control, Joints, Custom]
        attrs_list = ['.translateX', '.translateY', '.translateZ', '.rotateX', '.rotateY', '.rotateZ', '.scaleX',
                      '.scaleY',
                      '.scaleZ', '.visibility', '.rotateOrder', '.subCtrlVis']
        rig_top_grp = 'Group'
        if not cmds.objExists(rig_top_grp):
            selections = cmds.ls(sl = True)
            if selections:
                rig_top_grp = selections[0]

        # 创建总控制器Character
        character_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_Character_001', shape = 'circle', radius = 10,
                                                              axis = 'X+',
                                                              pos = None,
                                                              parent = Control)

        # 创建世界控制器
        world_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_world_001', shape = 'local', radius = 8, axis = 'Z-',
                                                          pos = None,
                                                          parent = 'ctrl_m_Character_001')

        cog_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_cog_001', shape = 'circle', radius = 3, axis = 'X+',
                                                        pos = None,
                                                        parent = 'output_m_world_001')

        # 创建一个自定义的控制器，用来承载自定义的属性
        lock_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_m_custom_001', shape = 'cross', radius = 3, axis = 'X+',
                                                         pos = None,
                                                         parent = Custom)
        lock_ctrl = 'ctrl_m_custom_001'
        cmds.parentConstraint('ctrl_m_Character_001', lock_ctrl, mo = True)
        cmds.scaleConstraint('ctrl_m_Character_001', lock_ctrl, mo = True)

        # 创建自定义的控制器属性
        for attr in ['GeometryVis', 'ControlsVis', 'RigNodesVis', 'JointsVis']:
            if not cmds.objExists('{}.{}'.format(lock_ctrl, attr)):
                cmds.addAttr(lock_ctrl, ln = attr, at = 'bool', dv = 1, keyable = True)

        # 添加精度切换的属性
        if not cmds.objExists('{}.Resolution'.format(lock_ctrl)):
            cmds.addAttr(lock_ctrl, ln = 'Resolution', at = 'enum', en = 'low:mid:high', keyable = True)
            for idx, res in {0: 'low', 1: 'mid', 2: 'high'}.items():
                cnd_node = 'resolution_{}_conditionNode'.format(res)
                if not cmds.objExists(cnd_node):
                    cnd_node = cmds.createNode('condition', n = cnd_node)
                cmds.connectAttr('{}.Resolution'.format(lock_ctrl), '{}.firstTerm'.format(cnd_node), f = True)
                cmds.setAttr('{}.secondTerm'.format(cnd_node), idx)
                cmds.setAttr('{}.colorIfTrueR'.format(cnd_node), 1)
                cmds.setAttr('{}.colorIfFalseR'.format(cnd_node), 0)
                cmds.connectAttr('{}.outColorR'.format(cnd_node), 'grp_m_{}_Modle_001.visibility'.format(res), f = True)

        # 添加模型显示方式的属性
        if not cmds.objExists('{}.GeometryDisplayType'.format(lock_ctrl)):
            cmds.addAttr(lock_ctrl, ln = 'GeometryDisplayType', at = 'enum', en = 'Normal:Template:Reference',
                         keyable = True)

        # 连接 GeometryVis
        cmds.connectAttr('{}.GeometryVis'.format(lock_ctrl), '{}.visibility'.format(Geometry), f = True)

        # 连接 controlsVis
        cmds.connectAttr('{}.ControlsVis'.format(lock_ctrl), '{}.visibility'.format(Control), f = True)

        # 连接 RigNodesVis
        cmds.connectAttr('{}.RigNodesVis'.format(lock_ctrl), '{}.visibility'.format(RigNodes), f = True)

        # 连接 jointsVis
        cmds.connectAttr('{}.JointsVis'.format(lock_ctrl), '{}.visibility'.format(Joints), f = True)

        # 连接模型的可编辑属性
        cmds.setAttr(Geometry + '.overrideDisplayType', 2)
        cmds.connectAttr('{}.GeometryDisplayType'.format(lock_ctrl), Geometry + '.overrideEnabled', f = True)

        # 显示和隐藏属性
        for attr in attrs_list:
            cmds.setAttr(lock_ctrl + attr, l = True, k = False, cb = False)

        return {
            'Geometry': Geometry,
            'Control': Control,
            'RigNodes': RigNodes,
            'Joints': Joints,
            'RigNodes_Local': RigNodes_Local,
            'RigNodes_World': RigNodes_World,
            'nCloth_geo_grp': nCloth_geo_grp
        }

    @staticmethod
    def create_constraints():
        u"""
        快速创建约束.
        用法：先选择需要约束的物体，在选择被约束的物体
        """
        sel = cmds.ls(sl = True)
        driver_obj = sel[-1]
        driven_obj = sel[0:-1]
        cmds.pointConstraint(driver_obj, driven_obj, mo = True)
        cmds.orientConstraint(driver_obj, driven_obj, mo = True)
        cmds.scaleConstraint(driver_obj, driven_obj, mo = True)

    @staticmethod
    def delete_constraints():
        u'''
        快速删除选择物体的约束节点
        '''
        sel = cmds.ls(sl = True)
        for obj in sel:
            const = cmds.listConnections(obj, type = 'constraint')
            if const:
                cmds.delete(const)

    @staticmethod
    def select_sub_objects():
        u'''
        快速选择所选择物体的所有子对象
        '''
        selection = cmds.ls(sl = True)  # 获取选择的所有对象
        for obj in selection:
            cmds.select(cmds.listRelatives(obj, allDescendents = True, type = 'transform'), add = True)
    @staticmethod
    def make_undo(func):
        u'''
        一键撤销的解释器
        '''
        @wraps(func)
        def wrap(*args, **kwargs):
            cmds.undoInfo(openChunk = True)
            result = func(*args, **kwargs)
            cmds.undoInfo(closeChunk = True)
            return result

        return wrap