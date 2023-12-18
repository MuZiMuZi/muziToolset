# coding=utf-8
'''
眼睛的绑定系统创建
'''
import os
from importlib import reload

import maya.cmds as cmds

from . import eyeLid
from ...module.chain import chain
from ....core import controlUtils , jointUtils , nameUtils , pipelineUtils


reload (eyeLid)
reload(chain)
reload(jointUtils)

class Eye (chain.Chain) :
	

    def __init__ (self , side , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
                  control_parent = None) :
        super(Eye,self).__init__ (side , name , joint_number , length , joint_parent , control_parent)
        self.shape = 'circle'
        self.rtype = 'Eye'
        self.radius = 0.3

        # iris的缩放关节
        self.iris_bpjnt_list = list ()
        self.iris_jnt_list = list ()

        # 生成上部分的眼皮
        self.eye_lid_upper = eyeLid.EyeLid (side = self.side , name = 'upper' , joint_number = 7 , joint_parent = None ,
                                            control_parent = None)

        # 生成下部分的眼皮
        self.eye_lid_lower = eyeLid.EyeLid (side = self.side , name = 'lower' , joint_number = 7 , joint_parent = None ,
                                            control_parent = None)


    def create_namespace (self) :
        super ().create_namespace ()
        # 创建眼睛部位的命名规范
        self.aim_ctrl = ('ctrl_{}_{}{}Aim_001'.format (self.side , self.name , self.rtype))
        self.aim_loc = ('loc_{}_{}{}Aim_001'.format (self.side , self.name , self.rtype))
        self.jnt_loc = ('loc_{}_{}{}Jnt_001'.format (self.side , self.name , self.rtype))
        self.aim_crv = ('crv_{}_{}{}Aim_001'.format (self.side , self.name , self.rtype))
        for index in range (3) :
            self.iris_bpjnt_list.append (
                'bpjnt_{}_{}{}iris_{:03d}'.format (self.side , self.name , self.rtype , index + 1))
            self.iris_jnt_list.append (
                'jnt_{}_{}{}iris_{:03d}'.format (self.side , self.name , self.rtype , index + 1))
        # 创建眼睛闭合曲线的名称规范：blink
        self.blink_curve = 'crv_{}_{}{}EyeLidBlink_001'.format (self.side , self.name , self.rtype)

        # 创建连接blinkHeight上眼皮的reverse节点的名称规范
        self.reverse_node = self.eye_lid_upper.curve.replace ('crv' , 'reverse')

        # 创建上下眼皮的权重曲线的blink曲线的名称规范
        self.eye_lid_upper.blink_curve = self.eye_lid_upper.skin_curve.replace ('Skin' , 'SkinBlink')
        self.eye_lid_lower.blink_curve = self.eye_lid_lower.skin_curve.replace ('Skin' , 'SkinBlink')

        # 创建眼内侧和眼外侧的控制器的名称规范
        self.inn_ctrl = 'ctrl_{}_{}{}inn_001'.format (self.side , self.name , self.rtype)
        self.out_ctrl = 'ctrl_{}_{}{}out_001'.format (self.side , self.name , self.rtype)

        # 所有曲线的集合
        self.crv_list = [self.blink_curve , self.eye_lid_upper.blink_curve , self.eye_lid_lower.blink_curve]


    def create_bpjnt (self) :
        # 获得eye_bpjnt 的路径
        self.eye_bpjnt_path = os.path.abspath (__file__ + "/../../../bpjnt/eye_bpjnt.ma")
        # 导入关节
        cmds.file (self.eye_bpjnt_path , i = True , rnn = True)

        self.eye_lid_upper.create_bpjnt ()
        self.eye_lid_lower.create_bpjnt ()


    def create_joint (self) :
        # 创建眼球的关节
        for bpjnt , jnt in zip (self.bpjnt_list , self.jnt_list) :
            self.jnt = cmds.createNode ('joint' , name = jnt , parent = self.joint_parent)
            cons = cmds.parentConstraint (bpjnt , self.jnt , mo = False)
            cmds.delete (cons)
            # 指定关节的父层级为上一轮创建出来的关节
            self.joint_parent = self.jnt

        # 创建iris的关节
        for bpjnt , jnt in zip (self.iris_bpjnt_list , self.iris_jnt_list) :
            self.jnt = cmds.createNode ('joint' , name = jnt , parent = self.jnt_list [0])
            cons = cmds.parentConstraint (bpjnt , self.jnt , mo = False)
            cmds.delete(cons)

        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.jnt_list)
        jointUtils.Joint.joint_orientation (self.iris_jnt_list)

        self.eye_lid_upper.create_joint ()
        self.eye_lid_lower.create_joint ()


    def create_ctrl (self) :

        # 创建控制器总体的层级组
        self.ctrl_grp = cmds.createNode ('transform' , parent = self.control_parent , name = self.ctrl_grp)
        # 创建控制器
        self.ctrl = controlUtils.Control.create_ctrl (self.ctrl_list [0] , shape = 'circle' ,
                                                      radius = self.radius ,
                                                      axis = 'X+' , pos = self.jnt_list [0] ,
                                                      parent = self.ctrl_grp)
        # 移动控制器的位置
        cmds.setAttr (self.zero_list [0] + '.translateZ' ,
                      cmds.getAttr (self.zero_list [0] + '.translateZ') + 1)

        # 创建aim控制器用于做目标约束
        self.aim_ctrl = controlUtils.Control.create_ctrl (self.aim_ctrl , shape = 'shape_040' ,
                                                          radius = self.radius ,
                                                          axis = 'Z+' , pos = self.jnt_list [0] ,
                                                          parent = self.ctrl_grp)
        # 移动aim控制器的位置
        self.aim_zero = self.aim_ctrl.replace ('ctrl' , 'zero')
        # 移动控制器的位置
        cmds.setAttr (self.aim_zero + '.translateZ' ,
                      cmds.getAttr (self.aim_zero + '.translateZ') + 3)

        ## 创建曲线指示器
        # 创建aim控制器的loc来记录位置
        self.aim_loc = cmds.spaceLocator (name = self.aim_loc) [0]
        cmds.matchTransform (self.aim_loc , self.aim_ctrl , position = True , rotation =
        True ,
                             scale = True)
        cmds.parent (self.aim_loc , self.aim_ctrl)
        cmds.setAttr (self.aim_loc + '.visibility' , 0)
        # 创建jnt的loc来记录位置
        self.jnt_loc = cmds.spaceLocator (name = self.jnt_loc) [0]
        cmds.matchTransform (self.jnt_loc , self.jnt_list [0] , position = True , rotation = True , scale = True)
        cmds.parent (self.jnt_loc , self.jnt_list [0])
        cmds.setAttr (self.jnt_loc + '.visibility' , 0)

        # 连接loc和曲线来表示位置
        self.aim_crv = cmds.curve (degree = 1 , point = [(0.0 , 0.0 , 0.0) , (0.0 , 0.0 , 0.0)] ,
                                   name = self.aim_crv)
        aim_loc_shape = cmds.listRelatives (self.aim_loc , shapes = True) [0]
        jnt_loc_shape = cmds.listRelatives (self.jnt_loc , shapes = True) [0]
        aim_curve_shape = cmds.listRelatives (self.aim_crv , shapes = True) [0]

        # 连接曲线与loc
        cmds.connectAttr (aim_loc_shape + '.worldPosition[0]' , aim_curve_shape + '.controlPoints[0]')
        cmds.connectAttr (jnt_loc_shape + '.worldPosition[0]' , aim_curve_shape + '.controlPoints[1]')
        # 设置曲线的可见性
        cmds.setAttr (aim_curve_shape + '.overrideEnabled' , 1)
        cmds.setAttr (aim_curve_shape + '.overrideDisplayType' , 2)
        cmds.setAttr (self.aim_crv + '.inheritsTransform' , 0)
        cmds.parent (self.aim_crv , self.ctrl_grp)

        # 创建眼皮的控制器
        self.eye_lid_upper.create_ctrl ()
        self.eye_lid_lower.create_ctrl ()

        # 创建眼角的控制器
        self.inn_ctrl = controlUtils.Control.create_ctrl (self.inn_ctrl , shape = 'ball' , axis = 'X+' , radius = 0.1 ,
                                                          pos = self
                                                          .eye_lid_upper.zero_list [0] , parent = self.ctrl_grp)
        self.out_ctrl = controlUtils.Control.create_ctrl (self.out_ctrl , shape = 'ball' , axis = 'X+' , radius = 0.1 ,
                                                          pos = self
                                                          .eye_lid_upper.zero_list [-1] , parent = self.ctrl_grp)


    def add_constraint (self) :
        u"""
        创建约束
        """
        pipelineUtils.Pipeline.create_constraint (self.ctrl_list [0].replace ('ctrl' , 'output') , self.jnt_list [0] ,
                                                  point_value = False ,
                                                  orient_value = False , parent_value = True,scale_value =
                                                  True ,
                                                  mo_value = True)

        # 创建目标约束
        self.aim_output = self.aim_ctrl.replace ('ctrl' , 'output')
        cmds.aimConstraint (self.aim_output , self.driven_list [0] , offset = (0 , 0 , 0) , weight = 1 ,
                            aimVector = (1 , 0 , 0) , upVector = (

                0 , 1 , 0) , worldUpType = "vector" , worldUpVector = (0 , 1 , 0))

        self.eye_lid_upper.add_constraint()
        self.eye_lid_lower.add_constraint()

        # 添加闭合眼皮曲线的功能
        self.add_blink ()

        # 添加眼球移动的时候眼皮跟随运动的功能，眼球控制器对眼皮中间的控制器添加旋转约束，注意这次的旋转约束需要添加上眼皮控制器上层的组，这样可以控制旋转的幅度
        cmds.orientConstraint (self.output_list [0] , self.eye_lid_upper.zero_list [3] ,
                               self.eye_lid_upper.driven_list [3])
        cmds.orientConstraint (self.output_list [0] , self.eye_lid_lower.zero_list [3] ,
                               self.eye_lid_lower.driven_list [3])

        # 眼睛内侧控制器对上下眼皮的内侧控制器做约束
        cmds.parentConstraint (self.inn_ctrl.replace ('ctrl' , 'output') , self
                               .eye_lid_upper.driven_list [0])
        cmds.parentConstraint (self.inn_ctrl.replace ('ctrl' , 'output') , self
                               .eye_lid_lower.driven_list [0])
        # 隐藏上下眼皮的内侧控制器
        cmds.setAttr (self.eye_lid_upper.zero_list [0] + '.v' , 0)
        cmds.setAttr (self.eye_lid_lower.zero_list [0] + '.v' , 0)
        # 眼睛外侧控制器对上下眼皮的外侧控制器做约束
        cmds.parentConstraint (self.out_ctrl.replace ('ctrl' , 'output') , self
                               .eye_lid_upper.driven_list [-1])
        cmds.parentConstraint (self.out_ctrl.replace ('ctrl' , 'output') , self
                               .eye_lid_lower.driven_list [-1])
        # 隐藏上下眼皮的外侧控制器
        cmds.setAttr (self.eye_lid_upper.zero_list [-1] + '.v' , 0)
        cmds.setAttr (self.eye_lid_lower.zero_list [-1] + '.v' , 0)

        # 添加瞳孔缩放的功能
        self.create_iris ()
        # 整理整体的层级架构
        self.organization_hierarchy ()


    def add_blink (self) :
        u"""
        添加闭合眼皮曲线的功能
        """
        # 创建blink曲线
        self.blink_curve = cmds.duplicate (self.eye_lid_upper.curve , name = self.blink_curve) [0]

        # 将上眼皮的控制曲线与下眼皮的控制曲线对blink曲线做bs驱动,将两个目标体的影响值设置在0.5
        self.bs_node = cmds.blendShape (self.eye_lid_upper.curve , self.eye_lid_lower.curve , self.blink_curve ,
                                        w = [(0 , 0.5) , (1 , 0.5)])

        # 给眼球控制器添加blink的属性控制
        cmds.addAttr (self.aim_ctrl , longName = 'blink' , at = 'double' , defaultValue = 0 , minValue = 0 ,
                      maxValue = 1 ,
                      keyable = True)
        cmds.addAttr (self.aim_ctrl , longName = 'blinkHeight' , at = 'double' , defaultValue = 0.5 , minValue = 0 ,
                      maxValue = 1 ,
                      keyable = True)

        # 属性blinkHeight连接给bs的权重值
        # 查找连接的bs节点
        cmds.connectAttr (self.aim_ctrl + '.blinkHeight' , self.bs_node [0] + '.{}'.format (self.eye_lid_lower.curve))
        self.reverse_node = cmds.createNode ('reverse' , name = self.reverse_node)
        cmds.connectAttr (self.aim_ctrl + '.blinkHeight' , self.reverse_node + '.inputX')
        cmds.connectAttr (self.reverse_node + '.outputX' , self.bs_node [0] + '.{}'.format (self.eye_lid_upper.curve))

        # 创建上下眼皮的权重曲线的blink曲线
        self.eye_lid_upper.blink_curve = cmds.duplicate (self.eye_lid_upper.skin_curve , name = self.eye_lid_upper
                                                         .blink_curve) [0]
        self.eye_lid_lower.blink_curve = cmds.duplicate (self.eye_lid_lower.skin_curve , name = self.eye_lid_lower
                                                         .blink_curve) [0]

        # blink曲线对上眼皮的权重曲线的blink曲线制作线变形器，注意，需要先将blinkHeight调整到0
        cmds.setAttr (self.aim_ctrl + '.blinkHeight' , 0)
        self.eye_lid_upper.wire_node = \
            cmds.wire (self.eye_lid_upper.blink_curve , w = self.blink_curve , gw = False , en = 1.000000 ,
                       ce = 0.000000 ,
                       li = 0.000000) [0]
        # 调整上眼皮线变形器的参数
        cmds.setAttr (self.eye_lid_upper.wire_node + '.dropoffDistance[0]' , 200)
        cmds.setAttr (self.eye_lid_upper.wire_node + '.scale[0]' , 0)
        # 上眼皮的权重曲线的blink曲线对上眼皮的权重曲线做bs
        self.eye_lid_upper.bs_node = cmds.blendShape (self.eye_lid_upper.blink_curve , self.eye_lid_upper.skin_curve ,
                                                      w = [(0 , 1)])
        cmds.connectAttr (self.aim_ctrl + '.blink' , self.eye_lid_upper.bs_node [0] + '.{}'.format (
            self.eye_lid_upper.blink_curve))

        # blink曲线对下眼皮的权重曲线的blink曲线制作线变形器，注意，需要先将blinkHeight调整到1
        cmds.setAttr (self.aim_ctrl + '.blinkHeight' , 1)
        self.eye_lid_lower.wire_node = \
            cmds.wire (self.eye_lid_lower.blink_curve , w = self.blink_curve , gw = False , en = 1.000000 ,
                       ce = 0.000000 ,
                       li = 0.000000) [0]
        # 调整下眼皮线变形器的参数
        cmds.setAttr (self.eye_lid_lower.wire_node + '.dropoffDistance[0]' , 200)
        cmds.setAttr (self.eye_lid_lower.wire_node + '.scale[0]' , 0)

        # 下眼皮的权重曲线的blink曲线对上眼皮的权重曲线做bs
        self.eye_lid_lower.bs_node = cmds.blendShape (self.eye_lid_lower.blink_curve , self.eye_lid_lower.skin_curve ,
                                                      w = [(0 , 1)])
        cmds.connectAttr (self.aim_ctrl + '.blink' , self.eye_lid_lower.bs_node [0] + '.{}'.format (
            self.eye_lid_lower.blink_curve))
        # 恢复blinkHeight的数值
        cmds.setAttr (self.aim_ctrl + '.blinkHeight' , 0.5)


    def organization_hierarchy (self) :
        u"""
        整理整体的层级架构
        """
        cmds.parent (self.eye_lid_upper.eye_up_zero , self.top_node_grp)
        cmds.parent (self.eye_lid_upper.curve_nodes_grp , self.eye_lid_upper.skin_nodes_grp ,
                     self.eye_lid_lower.curve_nodes_grp , self.eye_lid_lower.skin_nodes_grp , self.top_node_grp)
        # 设置曲线的可见性
        for crv in self.crv_list :
            cmds.setAttr (crv + '.v' , 0)

        # 设置控制器组的层级结构
        cmds.parent (self.eye_lid_upper.ctrl_grp , self.eye_lid_lower.ctrl_grp , self.ctrl_grp)


    def create_iris (self) :
        """
        瞳孔缩放，运用勾股定理来制作瞳孔的缩放
        眼球半径的平方-关节TX的平方，再开更号即可得出缩放的值
        Returns:

        """
        # 给眼睛控制器添加控制瞳孔缩放的属性
        cmds.addAttr (self.ctrl_list [0] , longName = 'iris' , keyable = 1 , dv = 1 , minValue = -1 , maxValue = 2)
        # 获取眼球的半径值
        self.eye_radius = cmds.getAttr (self.jnt_list [-1] + '.translateX')
        # 给瞳孔缩放关节创建连接
        for jnt in self.iris_jnt_list :
            name_parts = nameUtils.Name (name = jnt)
            # 连接瞳孔缩放关节的位移
            offset_Tx_node = cmds.createNode ('multDoubleLinear' , name = jnt.replace ('jnt' , 'offsetTx'))
            cmds.connectAttr (self.ctrl_list [0] + '.iris' , offset_Tx_node + '.input1')
            cmds.setAttr (offset_Tx_node + '.input2' , cmds.getAttr (jnt + '.translateX'))
            cmds.connectAttr (offset_Tx_node + '.output' , jnt + '.translateX')

            # 创建一个乘方节点，用来计算眼球半径的平方和关节Tx的平方
            power_node = cmds.createNode ('multiplyDivide' , name = jnt.replace ('jnt' , 'power'))
            cmds.connectAttr (jnt + '.translateX' , power_node + '.input1X')
            cmds.setAttr (power_node + '.input1Y ' , self.eye_radius)
            # 设置平方
            cmds.setAttr (power_node + '.operation' , 3)
            cmds.setAttr (power_node + '.input2X ' , 2)
            cmds.setAttr (power_node + '.input2Y ' , 2)

            # 创建一个相减节点，用来计算半径的平方减去关节Tx平方的值
            minus_node = cmds.createNode ('plusMinusAverage' , name = jnt.replace ('jnt' , 'minus'))
            cmds.connectAttr (power_node + '.outputX' , minus_node + '.input1D[0]')
            cmds.connectAttr (power_node + '.outputY' , minus_node + '.input1D[1]')
            cmds.setAttr (power_node + '.operation ' , 2)

            # 创建一个开方节点，用于开方
            sqit_node = cmds.createNode ('multiplyDivide' , name = jnt.replace ('jnt' , 'sqit'))
            cmds.connectAttr (minus_node + '.output1D' , sqit_node + '.input1X')
            # 设置平方
            cmds.setAttr (sqit_node + '.operation' , 3)
            cmds.setAttr (sqit_node + '.input2X ' , 0.5)

            # 创建一个乘除节点，用于将缩放的值重新连接回关节的缩放
            div_node = cmds.createNode ('multiplyDivide' , name = jnt.replace ('jnt' , 'div'))
            cmds.connectAttr (sqit_node + '.outputX' , div_node + '.input1X')
            # 设置除法
            cmds.setAttr (div_node + '.operation ' , 2)

            # 将乘除节点最后得出的值连接回给关节的缩放Y,Z
            cmds.connectAttr (div_node + '.outputX' , jnt + '.scaleY')
            cmds.connectAttr (div_node + '.outputX' , jnt + '.scaleZ')


if __name__ == "__main__" :
    def build_setup () :
        eye_l = eye.Eye (side = 'l' , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
                         control_parent = None)
        eye_l.build_setup ()

        eye_r = eye.Eye (side = 'r' , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
                         control_parent = None)
        eye_r.build_setup ()


    def build_rig () :
        eye_l = eye.Eye (side = 'l' , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
                         control_parent = None)
        eye_l.build_rig ()

        eye_r = eye.Eye (side = 'r' , name = '' , joint_number = 2 , length = 10 , joint_parent = None ,
                         control_parent = None)
        eye_r.build_rig ()


    build_setup ()
    build_rig ()
