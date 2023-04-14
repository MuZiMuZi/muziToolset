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
from importlib import reload
from .import base_rig
from .import fk_rig
from .import ik_rig
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils


class IKFK_Rig(ik_rig.IK_Rig , fk_rig.FK_Rig) :


    def __init__(self , bp_joints = None , joint_parent = None , control_parent = None , space_list = None) :
        super(IKFK_Rig , self).__init__(bp_joints = bp_joints , joint_parent = joint_parent ,
                                        control_parent = control_parent , space_list = space_list)


    def create_ikfk_chain_rig(self) :
        u"""
        创建ikfk关节链混合的绑定
        """
        self.fk_chain = jointUtils.Joint.create_chain(self.bp_joints , suffix = 'FK' ,
                                                      joint_parent = self.jnt_grp)
        self.fk_chain_rig(self.fk_chain , self.control_parent)
        self.ik_chain = jointUtils.Joint.create_chain(self.bp_joints , suffix = 'IK' ,
                                                      joint_parent = self.jnt_grp)
        self.ik_chain_rig(self.ik_chain , self.control_parent , self.space_list , stretch = True)
        self.ikfk_chain = jointUtils.Joint.create_chain(self.bp_joints , suffix = 'Bind' ,
                                                        joint_parent = self.jnt_grp)
        self.ikfk_chain_rig(self.fk_chain , self.ik_chain , self.ikfk_chain , self.control_parent)


    def create_ribbon_Rig(self , ikfk_chain , control_parent , joint_parent , joint_number) :
        u"""
              创建ribbon关节的绑定
              """
        upper_part = nameUtils.Name(name = ikfk_chain[0])
        lower_part = nameUtils.Name(name = ikfk_chain[1])
        # 创建ribbon关节和twist关节
        self.ribbon_rig(upper_part.name , control_parent , joint_parent , joint_number = joint_number)
        self.ribbon_rig(lower_part.name , control_parent , joint_parent , joint_number = joint_number)

        # 吸附带控制器组的位置和旋转
        ribbon_upper_start_driven = 'driven_{}_{}Start_001'.format(upper_part.side , upper_part.description)
        ribbon_upper_End_driven = 'driven_{}_{}End_001'.format(upper_part.side , upper_part.description)

        ribbon_lower_start_driven = 'driven_{}_{}Start_001'.format(lower_part.side , lower_part.description)
        ribbon_lower_End_driven = 'driven_{}_{}End_001'.format(lower_part.side , lower_part.description)

        # 关节约束对应的控制器组

        cmds.parentConstraint(ikfk_chain[0] , ribbon_upper_start_driven , maintainOffset = False)
        cmds.parentConstraint(ikfk_chain[1] , ribbon_upper_End_driven , maintainOffset = False)

        cmds.parentConstraint(ikfk_chain[1] , ribbon_lower_End_driven , maintainOffset = False)
        cmds.parentConstraint(ikfk_chain[2] , ribbon_lower_start_driven , maintainOffset = False)


    def ikfk_chain_rig(self , fk_chain , ik_chain , ikfk_chain , control_parent) :
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
        make_bind_jnt_set = cmds.sets(name = make_bind_jnt_set , empty = True)
        if bind_jnt_set :
            bind_jnt_set = bind_jnt_set
        if not cmds.objExists(bind_jnt_set) or cmds.nodeType(bind_jnt_set) != 'objectSet' :
            bind_jnt_set = cmds.sets(name = bind_jnt_set , empty = True)
        for jnt in ikfk_chain :
            cmds.sets(make_bind_jnt_set , edit = True , forceElement = bind_jnt_set)
            cmds.sets(jnt , edit = True , forceElement = make_bind_jnt_set)

        # 获取创建控制器的关节的名称
        name_obj.type = 'ctrl'
        name_obj.description = name_obj.description + 'IKFKBend'
        # 创建ikfk切换的控制器
        IkFkBend_ctrl_obj = controlUtils.Control.create_ctrl(name_obj.name , shape = 'pPlatonic' , radius = 10 ,
                                                             axis = 'X+' ,
                                                             pos = ikfk_chain[0] , parent = None)
        IkFkBend_ctrl = name_obj.name
        IkFkBend_zero = IkFkBend_ctrl.replace('ctrl_' , 'zero_')
        cmds.move(0 , 15 , 15 , IkFkBend_zero , r = True , ls = True , wd = True)
        cmds.addAttr(IkFkBend_ctrl , longName = 'IkFkBend' , attributeType = 'double' , min = 0 , max = 1 ,
                     defaultValue = 1 ,
                     keyable = True)
        IkFkBend_grp = hierarchyUtils.Hierarchy.add_extra_group(obj = IkFkBend_zero ,
                                                                grp_name = IkFkBend_zero.replace('zero_' , 'grp_') ,
                                                                world_orient = False)
        # 锁定不需要的属性
        for channel in ['t' , 'r' , 's'] :

            for axis in ['x' , 'y' , 'z'] :
                cmds.setAttr(IkFkBend_ctrl + '.' + channel + axis , l = True , k = False , cb = False)
        cmds.setAttr(IkFkBend_ctrl + '.v' , l = True , k = False , cb = False)
        cmds.setAttr(IkFkBend_ctrl + '.ro' , l = True , k = False , cb = False)
        cmds.setAttr(IkFkBend_ctrl + '.subCtrlVis' , l = True , k = False , cb = False)

        # 用混合颜色节点来制作fk/ik开关
        # 连接切换
        for fk , ik , bind in zip(fk_chain , ik_chain , ikfk_chain) :
            for attr in ['translate' , 'rotate' , 'scale'] :
                blend_node = cmds.createNode('blendColors' , name = 'blend_{}_{}_001'.format(name_obj.side ,
                                                                                             name_obj.description))
                cmds.connectAttr(fk + '.{}'.format(attr) , blend_node + '.color1')
                cmds.connectAttr(ik + '.{}'.format(attr) , blend_node + '.color2')
                cmds.connectAttr(IkFkBend_ctrl + '.IkFkBend' , blend_node + '.blender')
                cmds.connectAttr(blend_node + '.output' , bind + '.{}'.format(attr))
        fk_ctrl_grp = fk_chain[0].replace('jnt_' , 'grp_')
        ik_ctrl_grp = ik_chain[0].replace('jnt_' , 'grp_')
        cmds.connectAttr(blend_node + '.blender' , fk_ctrl_grp + '.visibility')
        reverse_node = cmds.createNode('reverse' , name = blend_node.replace('blend_node_' , 'reverse_'))
        cmds.connectAttr(blend_node + '.blender' , reverse_node + '.inputX')
        cmds.connectAttr(reverse_node + '.outputX' , ik_ctrl_grp + '.visibility')

        hierarchyUtils.Hierarchy.parent(child_node = IkFkBend_grp , parent_node = control_parent)


    def ikfk_spine_rig(self) :
        u"""
        创建IK样条曲线（脊椎和脖子的绑定）和FK关节链的混合绑定
        """
        self.make(self.bp_joints)
        self.fk_chain = jointUtils.Joint.create_chain(self.bp_joints , suffix = 'FK' ,
                                                      joint_parent = self.jnt_grp)
        self.fk_chain_rig(self.fk_chain , self.control_grp)
        self.ik_chain = jointUtils.Joint.create_chain(self.bp_joints , suffix = 'IK' ,
                                                      joint_parent = self.jnt_grp)
        self.ik_spine_rig(self.ik_chain , self.control_grp , stretch = True)
        self.ikfk_chain = jointUtils.Joint.create_chain(self.bp_joints , suffix = 'Bind' ,
                                                        joint_parent = self.jnt_grp)
        self.ikfk_chain_rig(self.fk_chain , self.ik_chain , self.ikfk_chain , self.control_grp)


    def ribbon_rig(self , name , control_parent , joint_parent , joint_number = 5) :
        """
        创建ribbon控制器，给动画师更细致的动画效果
        思路：通过给定关节的名称来创建ribbon控制，通过曲线来生成曲面制作ribbon绑定，然后让生成的关节绑定在曲面上
        采用的变形器有twist，sine和wire变形器，通过这些变形器影响曲面，从而带动曲面上的关节

        Args:
            name(object):创建ribbon关节控制的名称
            control_parent:控制器组的父层级
            joint_parent:ribbon关节组的父层级
            joint_number (int): 需要创建的ribbon关节数量

        """
        # 从名称中获取ribbon控制器的边，描述，和编号
        ribbon = nameUtils.Name(name = name)

        # 从ribbon控制器中的边获取偏移值
        if ribbon.side != 'r' :
            offset_val = 1
        else :
            offset_val = -1

        # 创建ribbon控制器对应的层级组
        ribbon_ctrl_grp = cmds.createNode('transform' ,
                                          name = 'grp_{}_{}RibbonCtrls_{:03d}'.format(ribbon.side , ribbon.description ,
                                                                                      ribbon.index) ,
                                          parent = control_parent)
        ribbon_jnt_grp = cmds.createNode('transform' ,
                                         name = 'grp_{}_{}RibbonJnts_{:03d}'.format(ribbon.side , ribbon.description ,
                                                                                    ribbon.index) ,
                                         parent = joint_parent)
        nodes_local_grp = cmds.createNode('transform' ,
                                          name = 'grp_{}_{}RibbonNodesLocal_{:03d}'.format(ribbon.side ,
                                                                                           ribbon.description ,
                                                                                           ribbon.index) ,
                                          parent = self.rigNode_Local)
        nodes_world_grp = cmds.createNode('transform' ,
                                          name = 'grp_{}_{}RibbonNodesWorld_{:03d}'.format(ribbon.side ,
                                                                                           ribbon.description ,
                                                                                           ribbon.index) ,
                                          parent = self.rigNode_World)
        cmds.setAttr(ribbon_ctrl_grp + '.inheritsTransform' , 0)
        cmds.setAttr(nodes_world_grp + '.inheritsTransform' , 0)

        cmds.setAttr(nodes_local_grp + '.visibility' , 0)
        cmds.setAttr(nodes_world_grp + '.visibility' , 0)

        # 创建对应的曲线以生成nurbs曲面
        temp_curve = cmds.curve(point = [[5 * offset_val , 0 , 0] , [-5 * offset_val , 0 , 0]] , knot = [0 , 1] ,
                                degree = 1)
        # 根据关节数重建曲线
        cmds.rebuildCurve(temp_curve , degree = 3 , replaceOriginal = True , rebuildType = 0 , endKnots = 1 ,
                          keepRange = 0 ,
                          keepControlPoints = False , keepEndPoints = True , keepTangents = False ,
                          spans = joint_number + 1)
        # 复制这条曲线
        temp_curve_02 = cmds.duplicate(temp_curve)[0]
        # 移动两条曲线的位置来制作曲面
        cmds.setAttr(temp_curve + '.translateZ' , 1)
        cmds.setAttr(temp_curve_02 + '.translateZ' , -1)

        # 通过两条曲线来放样制作曲面
        surf = \
            cmds.loft(temp_curve_02 , temp_curve , constructionHistory = False , uniform = True , degree = 3 ,
                      sectionSpans = 1 ,
                      range = False , polygon = 0 ,
                      name = 'surf_{}_{}Ribbon_{:03d}'.format(ribbon.side , ribbon.description , ribbon.index))[0]
        cmds.parent(surf , nodes_local_grp)

        # 获得曲面的形状节点
        surf_shape = cmds.listRelatives(surf , shapes = True)[0]

        # 删除用来放样曲面的曲线
        cmds.delete(temp_curve , temp_curve_02)

        # 创建关节并附着到曲面
        fol_grp = cmds.createNode('transform' ,
                                  name = 'grp_{}_{}RibbonFollicles_{:03d}'.format(ribbon.side , ribbon.description ,
                                                                                  ribbon.index) ,
                                  parent = nodes_world_grp)

        # 创建ribbon关节的集合
        ribbon_jnt_set = 'set_ribbonJnt'
        make_ribbon_jnt_set = 'set_' + ribbon.side + '_' + ribbon.description + 'Jnt'
        make_ribbon_jnt_set = cmds.sets(name = make_ribbon_jnt_set , empty = True)
        if not cmds.objExists(ribbon_jnt_set) or cmds.nodeType(ribbon_jnt_set) != 'objectSet' :
            ribbon_jnt_set = cmds.sets(name = ribbon_jnt_set , empty = True)
            cmds.sets(make_ribbon_jnt_set , edit = True , forceElement = ribbon_jnt_set)
        else :
            cmds.sets(make_ribbon_jnt_set , edit = True , forceElement = ribbon_jnt_set)

        for i in range(joint_number) :
            # 创建毛囊
            fol_shape = cmds.createNode('follicle' , name = 'fol_{}_{}Ribbon{:03d}_{:03d}Shape'.format(ribbon.side ,
                                                                                                       ribbon.description ,
                                                                                                       i + 1 ,
                                                                                                       ribbon.index))
            # 重命名毛囊的tran节点名称
            fol = cmds.listRelatives(fol_shape , parent = True)[0]
            fol = cmds.rename(fol , fol_shape[:-5])
            # 把毛囊放入对应的层级组
            cmds.parent(fol , fol_grp)
            # 连接毛囊属性
            cmds.connectAttr(surf_shape + '.worldSpace[0]' , fol_shape + '.inputSurface')
            # 连接毛囊的形状节点以进行变换
            cmds.connectAttr(fol_shape + '.outTranslate' , fol + '.translate')
            cmds.connectAttr(fol_shape + '.outRotate' , fol + '.rotate')
            # 设置uv值
            cmds.setAttr(fol_shape + '.parameterU' , 0.5)
            cmds.setAttr(fol_shape + '.parameterV' , float(i) / (joint_number - 1))

            # 创建关节
            jnt = cmds.createNode('joint' ,
                                  name = 'jnt_{}_{}Ribbon{:03d}_{:03d}'.format(ribbon.side , ribbon.description ,
                                                                               i + 1 ,
                                                                               ribbon.index))
            parent_grp = ribbon_jnt_grp
            grp_nodes = []
            for node_type in ['zero' , 'offset'] :
                grp = cmds.createNode('transform' , name = jnt.replace('jnt' , node_type) , parent = parent_grp)
                grp_nodes.append(grp)
                parent_grp = grp

            cmds.parent(jnt , grp_nodes[-1])
            # 让对应的毛囊约束对应的关节点
            cmds.parentConstraint(fol , grp_nodes[0] , maintainOffset = False)
            # 将偏移组的旋转设置为零
            cmds.xform(grp_nodes[1] , rotation = [0 , 0 , 0] , worldSpace = True)

            # 将生成的ribbon关节放在对应的集里方便选择
            cmds.sets(jnt , edit = True , forceElement = make_ribbon_jnt_set)

        # 创建控制器
        ctrls = []
        for pos in ['start' , 'mid' , 'end'] :
            ctrl_name = 'ctrl_{}_{}{}_{:03d}'.format(ribbon.side , ribbon.description , pos.title() , ribbon.index)
            ctrl = controlUtils.Control.create_ctrl(ctrl_name , shape = 'hexagon' , radius = 5 ,
                                                    axis = 'Z+' ,
                                                    pos = None , parent = ribbon_ctrl_grp)

            ctrls.append(ctrl_name)
        # 放置控制器
        cmds.setAttr(ctrls[0].replace('ctrl' , 'zero') + '.translateX' , -5 * offset_val)
        cmds.setAttr(ctrls[2].replace('ctrl' , 'zero') + '.translateX' , 5 * offset_val)

        # 约束中间的控制器
        cmds.parentConstraint(ctrls[0] , ctrls[-1] , ctrls[1].replace('ctrl' , 'driven') , maintainOffset = False)

        # 添加twist的控制属性在第一个控制器和最后一个控制器上,'start'和 'end'
        cmds.addAttr(ctrls[0] , longName = 'twist' , niceName = u'扭曲' , attributeType = 'float' , keyable = True)
        cmds.addAttr(ctrls[-1] , longName = 'twist' , niceName = u'扭曲' , attributeType = 'float' , keyable = True)
        # 创建twist变形器
        twist_node , twist_hnd = cmds.nonLinear(surf , type = 'twist' , name = surf.replace('surf_' , 'twist_'))
        cmds.parent(twist_hnd , nodes_local_grp)
        cmds.setAttr(twist_hnd + '.rotate' , 0 , 0 , 90)
        scale_val = cmds.getAttr(twist_hnd + '.scaleX')
        cmds.setAttr(twist_hnd + '.scale' , scale_val * offset_val , scale_val * offset_val , scale_val * offset_val)
        # 连接twist变形器的属性到控制器上
        twist_hnd_shape = cmds.listRelatives(twist_hnd , shapes = True)[0]
        cmds.connectAttr(ctrls[0] + '.twist' , twist_node + '.endAngle')
        cmds.connectAttr(ctrls[-1] + '.twist' , twist_node + '.startAngle')

        # 添加sine的控制属性在中间的控制器上,'mid'
        cmds.addAttr(ctrls[1] , longName = 'sineDivider' , niceName = u'sine变形器属性设置 ----------' ,
                     attributeType = 'enum' ,
                     enumName = ' ' , keyable = False)
        cmds.setAttr(ctrls[1] + '.sineDivider' , channelBox = True , lock = True)
        cmds.addAttr(ctrls[1] , longName = 'amplitude' , niceName = u'振幅' , attributeType = 'float' , keyable = True ,
                     minValue = 0)
        cmds.addAttr(ctrls[1] , longName = 'wavelength' , niceName = u'波长' , attributeType = 'float' ,
                     keyable = True ,
                     minValue = 0.1 ,
                     defaultValue = 2)
        cmds.addAttr(ctrls[1] , longName = 'offset' , niceName = u'偏移' , attributeType = 'float' , keyable = True)
        cmds.addAttr(ctrls[1] , longName = 'sineRotation' , niceName = u'正弦旋转' , attributeType = 'float' ,
                     keyable = True)
        # 创建sine变形器
        sine_node , sine_hnd = cmds.nonLinear(surf , type = 'sine' , name = surf.replace('surf_' , 'sine_'))
        cmds.parent(sine_hnd , nodes_local_grp)
        cmds.setAttr(sine_hnd + '.rotate' , 0 , 0 , 90)
        scale_val = cmds.getAttr(sine_hnd + '.scaleX')
        cmds.setAttr(sine_hnd + '.scale' , scale_val * offset_val , scale_val * offset_val , scale_val * offset_val)
        cmds.setAttr(sine_node + '.dropoff' , 1)
        # 连接sine变形器的属性到控制器上
        sine_hnd_shape = cmds.listRelatives(sine_hnd , shapes = True)[0]
        cmds.connectAttr(ctrls[1] + '.amplitude' , sine_node + '.amplitude')
        cmds.connectAttr(ctrls[1] + '.wavelength' , sine_node + '.wavelength')
        cmds.connectAttr(ctrls[1] + '.offset' , sine_node + '.offset')
        cmds.connectAttr(ctrls[1] + '.sineRotation' , sine_hnd + '.rotateY')

        # 创建wire变形器
        # 创建wire变形器需要的曲线
        wire_curve = cmds.curve(point = [[-5 * offset_val , 0 , 0] , [0 , 0 , 0] , [5 * offset_val , 0 , 0]] ,
                                knot = [0 , 0 , 1 , 1] ,
                                degree = 2 ,
                                name = 'crv_{}_{}RibbonWire_{:03d}'.format(ribbon.side , ribbon.description ,
                                                                           ribbon.index))
        wire_curve_shape = cmds.listRelatives(wire_curve , shapes = True)[0]
        cmds.rename(wire_curve_shape , wire_curve + 'Shape')
        cmds.parent(wire_curve , nodes_world_grp)

        # 创建cluster 变形器，用控制器来约束cluster变形器的变化
        for ctrl , i in zip(ctrls , [0 , 1 , 2]) :
            cls_node , cls_hnd = cmds.cluster('{}.cv[{}]'.format(wire_curve , i) , name = ctrl.replace('ctrl' , 'cls'))
            cmds.parent(cls_hnd , nodes_world_grp)
            cmds.pointConstraint(ctrl , cls_hnd , maintainOffset = False)
        #
        # 创建wire变形器
        wire_node = surf.replace('surf' , 'wire')
        cmds.wire(surf , wire = wire_curve , name = wire_node)
        cmds.setAttr(wire_node + '.dropoffDistance[0]' , 200)
        cmds.parent(wire_curve + 'BaseWire' , nodes_local_grp)
