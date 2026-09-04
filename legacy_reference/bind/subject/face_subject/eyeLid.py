# coding=utf,8
'''
眼皮的绑定系统创建
'''

from importlib import reload

import maya.cmds as cmds

from ...module.base import base
from ....core import controlUtils , jointUtils , pipelineUtils


reload (pipelineUtils)
reload (base)


class EyeLid (base.Base) :
    example_curve = ['crv_l_upperEyeLidSkin_001' , 'crv_l_lowerEyeLidSkin_001']


    def __init__ (self , side , name , jnt_number = 7 , jnt_parent = None , ctrl_parent = None) :
        super ().__init__ (side , name , jnt_number , jnt_parent , ctrl_parent)
        # 定位用的曲线
        self.skin_curve = 'crv_{}_{}{}Skin_001'.format (self.side , self.name , self.rigType)
        self.name = name
        self.shape = 'cube'
        self.rigType = 'EyeLid'
        self.radius = 1
        self.jnt_number = jnt_number
        self.curve_jnt_list = []
        # 创建眼袋的名称列表
        self.pouch_ctrl_list = []
        self.pouch_jnt_list = []
        self.pouch_zero_list = []
        self.pouch_bpjnt_list = []
        self.pouch_output_list = []

        # 判断为上部分还是下部分，用来移动y轴的位置
        if self.name == 'upper' :
            self.y_value = 1
        else :
            self.y_value = -1

        #
        self.create_namespace ()


    def create_namespace (self) :
        u"""
        创建名称规范整理
        """
        super ().create_namespace ()
        # 整理与控制器有关的曲线的名称规范层级结构
        self.curve = 'crv_{}_{}{}_001'.format (self.side , self.name , self.rigType)
        for index in range (self.jnt_number) :
            self.curve_jnt_list.append ('jnt_{}_{}{}_{:03d}'.format (self.side , self.name , self.rigType , index + 1))
        self.curve_jnt_grp = 'grp_{}_{}{}Jnts_001'.format (self.side , self.name , self.rigType)
        self.curve_nodes_grp = 'grp_{}_{}{}RigNodes_001'.format (self.side , self.name , self.rigType)

        # 整理与蒙皮关节有关的曲线名称规范层级结构
        self.skin_curve = 'crv_{}_{}{}Skin_001'.format (self.side , self.name , self.rigType)
        self.skin_jnt_grp = 'grp_{}_{}{}SkinJnts_001'.format (self.side , self.name , self.rigType)
        self.skin_nodes_grp = 'grp_{}_{}{}SkinRigNodes_001'.format (self.side , self.name , self.rigType)
        # 整理眼睛的关节和向上方向的参考向量的名称规范层级结构
        self.eye_jnt = 'jnt_{}_Eye_001'.format (self.side)
        self.eye_up_loc = 'loc_{}_EyeUp_001'.format (self.side)
        self.eye_up_zero = 'zero_{}_EyeUp_001'.format (self.side)
        # 添加眼袋的名称规范
        for i in range (3) :
            self.pouch_ctrl_list.append (
                'ctrl_{}_{}{}Pouch_{:03d}'.format (self.side , self.name , self.rigType , i + 1))
            self.pouch_jnt_list.append (
                'jnt_{}_{}{}Pouch_{:03d}'.format (self.side , self.name , self.rigType , i + 1))
            self.pouch_zero_list.append (
                'zero_{}_{}{}Pouch_{:03d}'.format (self.side , self.name , self.rigType , i + 1))
            self.pouch_bpjnt_list.append ('bpjnt_{}_{}{}Pouch_{:03d}'.format (self.side , self.name , self.rigType ,
                                                                              i + 1))
            self.pouch_output_list.append ('output_{}_{}{}Pouch_{:03d}'.format (self.side , self.name , self.rigType ,
                                                                                i + 1))
        self.pouch_master_ctrl = 'ctrl_{}_{}{}PouchMaster_001'.format (self.side , self.name , self.rigType)
        # 整理节点的层级结构
        self.node_grp = 'grp_{}_{}{}Nodes_001'.format (self.side , self.name , self.rigType)
        self.pouch_jnt_grp = 'grp_{}_{}{}PouchJnts_001'.format (self.side , self.name , self.rigType)


    def create_bpjnt (self) :
        """
        创建定位的bp关节
        """
        # 创建曲线
        self.build_curve ()
        # 创建眼袋的bp定位关节
        for index , bpjnt in enumerate (self.pouch_bpjnt_list) :
            bpjnt = cmds.createNode ('joint' , name = bpjnt)
            cmds.matchTransform (bpjnt , self.jnt_list [-1])
            # 移动位置
            cmds.setAttr (bpjnt + '.translateX' , cmds.getAttr (self.jnt_list [-1] + '.translateX') + index * 0.25)
            cmds.setAttr (bpjnt + '.translateY' ,
                          cmds.getAttr (self.jnt_list [-1] + '.translateY') + 0.25 * self.y_value)
            cmds.setAttr (bpjnt + '.translateZ' , cmds.getAttr (self.jnt_list [-1] + '.translateZ') + 0.25)


    def build_curve (self) :
        u"""
        根据选择的模型点创建用于定位的曲线
        """

        # 根据skin_curve来制作curve，用于制作控制器的控制
        self.curve = cmds.duplicate (self.skin_curve , name = self.curve) [0]
        cmds.setAttr (self.skin_curve + '.visibility' , 0)
        # 重建self.curve用来控制曲线
        self.curve = \
            cmds.rebuildCurve (self.curve , ch = 1 , rpo = 1 , rt = 0 , end = 1 , kr = 0 , kcp = 0 , kep = 1 , kt = 0 ,
                               s = 4 , d = 3 , tol = 0.01) [0]

        # 在曲线上创建关节用来蒙皮曲线创建控制器的约束
        cmds.select (self.curve)
        self.curve_jnt_dict = jointUtils.Joint.create_joints_on_curve (is_parent = False)
        jnt_list = self.curve_jnt_dict ['jnt_list']
        # 重命名蒙皮关节和层级结构的名称
        for index , jnt in enumerate (jnt_list) :
            cmds.rename (jnt , self.curve_jnt_list [index])
        self.curve_jnt_grp = cmds.rename (self.curve_jnt_dict ['jnt_grp'] , self.curve_jnt_grp)
        self.curve_nodes_grp = cmds.rename (self.curve_jnt_dict ['node_grp'] , self.curve_nodes_grp)
        # 蒙皮曲线
        cmds.skinCluster (self.curve_jnt_list , self.curve)


    def create_joint (self) :
        u'''
        创建眼皮的权重关节在曲线上
        '''

        # 控制器曲线对蒙皮曲线做wire变形，让控制器曲线控制蒙皮曲线,注意如果是两条曲线做wire变形器的话，被控制的曲线需要给个w参数
        wire_node = cmds.wire (self.skin_curve , w = self.curve , gw = False , en = 1.000000 , ce = 0.000000 ,
                               li = 0.000000) [0]
        cmds.setAttr (wire_node + '.dropoffDistance[0]' , 200)

        # 将控制器的关节进行隐藏
        cmds.setAttr (self.curve_jnt_grp + '.visibility' , 0)
        # 判断向上的目标物体是否存在，如果不存在的话则创建
        if cmds.objExists (self.eye_up_loc) :
            pass
        else :
            self.eye_up_zero = cmds.createNode ('transform' , name = self.eye_up_zero)
            self.eye_up_loc = cmds.spaceLocator (name = self.eye_up_loc) [0]
            cmds.parent (self.eye_up_loc , self.eye_up_zero)
            cmds.matchTransform (self.eye_up_zero , self.eye_jnt)
            cmds.setAttr (self.eye_up_loc + '.translateY' , 5)
        # 创建眼皮的权重关节在曲线上
        pipelineUtils.Pipeline.create_eyelid_joints_on_curve (self.skin_curve , self.eye_jnt , self.eye_up_loc)

        # 整理节点的层级结构
        self.node_grp = cmds.createNode ('transform' , name = self.node_grp , parent = self.top_node_grp)
        cmds.parent (self.curve_nodes_grp , self.skin_nodes_grp , self.node_grp)
        cmds.parent (self.skin_jnt_grp , self.top_jnt_grp)
        # 整理关节层级结构
        self.pouch_jnt_grp = cmds.createNode ('transform' , name = self.pouch_jnt_grp)
        cmds.parent (self.pouch_jnt_grp , self.top_jnt_grp)

        # 根据眼袋的bp关节的位置创建眼袋关节
        for bpjnt , jnt in zip (self.pouch_bpjnt_list , self.pouch_jnt_list) :
            jnt = cmds.createNode ('joint' , name = jnt)
            cmds.matchTransform (jnt , bpjnt)
            cmds.parent (jnt , self.pouch_jnt_grp)


    def create_ctrl (self) :
        super ().create_ctrl ()
        # 创建眼袋总组控制器
        self.pouch_master_ctrl = controlUtils.Control.create_ctrl (self.pouch_master_ctrl , shape = 'circle' ,
                                                                   radius = self.radius * 2 ,
                                                                   axis = 'Z+' , pos = self.pouch_jnt_list [1] ,
                                                                   parent = self.ctrl_grp)

        # 创建眼袋关节的控制器
        for ctrl , jnt in zip (self.pouch_ctrl_list , self.pouch_jnt_list) :
            self.pouch_ctrl = controlUtils.Control.create_ctrl (ctrl , shape = 'cube' ,
                                                                radius = self.radius ,
                                                                axis = 'X+' , pos = jnt ,
                                                                parent = self.pouch_master_ctrl.replace ('ctrl' ,
                                                                                                         'output'))
            # 右边控制器的offset组都要设置缩放X为-1，才可以进行对称运动
            # 判断当边为'_r_'的时候设置缩放X
            if self.side == 'r' :
                cmds.setAttr (self.pouch_ctrl.replace ('ctrl_' , 'offset_') + '.scaleX' , -1)


    def add_constraint (self) :
        super ().add_constraint ()

        # 控制器之间需要添加约束
        # ctrl_list =
        # [0,3,6]
        # [0,2,3]
        # [0,1,2]
        # [3,4,6]
        # [4,5,6]


        # # 约束中间的控制器[0,2,3]，两侧的控制器约束中间的控制器
        # cmds.parentConstraint (self.output_list [0] , self.output_list [3] , self.driven_list [2] , mo = True)
        #
        # # 约束中间的控制器[0,1,2]，两侧的控制器约束中间的控制器
        # cmds.parentConstraint (self.output_list [0] , self.output_list [2] , self.driven_list [1] , mo = True)
        #
        # # 约束中间的控制器[3,4,6]，两侧的控制器约束中间的控制器
        # cmds.parentConstraint (self.output_list [3] , self.output_list [6] , self.driven_list [4] , mo = True)
        #
        # # 约束中间的控制器[4,5,6]，两侧的控制器约束中间的控制器
        # cmds.parentConstraint (self.output_list [4] , self.output_list [6] , self.driven_list [5] , mo = True)

        # 第二个控制器和第六个控制器是为了调整小的形态，默认是隐藏的,连接他们的可见性到中间的控制器上
        cmds.addAttr (self.ctrl_list [3] , attributeType = 'bool' , longName = 'LidSubCtrlVis' , keyable = 1 ,
                      defaultValue = 0)

        # # 连接可见性
        # cmds.connectAttr (self.ctrl_list [3] + '.LidSubCtrlVis' , self.ctrl_list [1] + '.visibility')
        # cmds.connectAttr (self.ctrl_list [3] + '.LidSubCtrlVis' , self.ctrl_list [5] + '.visibility')

        # 设置曲线的可见性
        cmds.setAttr (self.curve + '.v' , 0)
        cmds.setAttr (self.skin_curve + '.v' , 0)

        # 眼袋控制器与眼袋关节之间进行约束
        for output , jnt in zip (self.pouch_output_list , self.pouch_jnt_list) :
            pipelineUtils.Pipeline.create_constraint (output , jnt , point_value = False , orient_value = False ,
                                                      parent_value = True ,
                                                      scale_value = False ,
                                                      mo_value = True)

        # 曲线控制器与曲线关节之间进行约束
        for output , jnt in zip (self.output_list , self.curve_jnt_list) :
            pipelineUtils.Pipeline.create_constraint (output , jnt , point_value = False , orient_value = False ,
                                                      parent_value = True ,
                                                      scale_value = False ,
                                                      mo_value = True)
