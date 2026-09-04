# coding=utf-8
'''
眉毛的绑定系统创建
'''
import os
from importlib import reload

import maya.cmds as cmds

from ...module.base import base
from ....core import controlUtils , pipelineUtils


reload (pipelineUtils)
reload (base)


class Brow (base.Base) :


    def __init__ (self , side = '' , name = '' , jnt_number = 1 , jnt_parent = None , ctrl_parent = None) :
        super ().__init__ (side , name , jnt_number , jnt_parent , ctrl_parent)
        self.radius = 0.25
        self.shape = 'ball'
        self.rigType = 'Brow'

        # 创建两边的眉毛系统
        self.brow_l = base.Base (side = 'l' , name = '' , jnt_number = 7 , jnt_parent = None , ctrl_parent =
        None)
        self.brow_l.rigType = 'Brow'
        self.brow_l.shape = 'cube'
        self.brow_l.radius = 0.2

        self.brow_r = base.Base (side = 'r' , name = '' , jnt_number = 7 , jnt_parent = None , ctrl_parent =
        None)
        self.brow_r.rigType = 'Brow'
        self.brow_r.shape = 'cube'
        self.brow_r.radius = 0.2


    def create_namespace (self) :
        super ().create_namespace ()
        # 创建两边的眉毛名称规范
        self.brow_l.create_namespace ()
        self.brow_r.create_namespace ()
        # 创建两边眉毛用来定位的控制器关节和控制器的名称规范
        self.brow_l.bpjnt_follow_list = []
        self.brow_l.ctrl_follow_list = []
        self.brow_l.connect_follow_list = []
        self.brow_l.output_follow_list = []
        self.brow_l.offset_follow_list = []

        self.brow_r.bpjnt_follow_list = []
        self.brow_r.ctrl_follow_list = []
        self.brow_r.connect_follow_list = []
        self.brow_r.output_follow_list = []
        self.brow_r.offset_follow_list = []

        for i in range (4) :
            self.brow_l.bpjnt_follow_list.append (
                'bpjnt_{}_{}{}Follow_{:03d}'.format ('l' , self.name , self.rigType , i + 1))
            self.brow_l.ctrl_follow_list.append (
                'ctrl_{}_{}{}Follow_{:03d}'.format ('l' , self.name , self.rigType , i + 1))
            self.brow_l.connect_follow_list.append (
                'connect_{}_{}{}Follow_{:03d}'.format ('l' , self.name , self.rigType , i + 1))
            self.brow_l.output_follow_list.append (
                'output_{}_{}{}Follow_{:03d}'.format ('l' , self.name , self.rigType , i + 1))
            self.brow_l.offset_follow_list.append (
                'offset_{}_{}{}Follow_{:03d}'.format ('l' , self.name , self.rigType , i + 1))

            self.brow_r.bpjnt_follow_list.append (
                'bpjnt_{}_{}{}Follow_{:03d}'.format ('r' , self.name , self.rigType , i + 1))
            self.brow_r.ctrl_follow_list.append (
                'ctrl_{}_{}{}Follow_{:03d}'.format ('r' , self.name , self.rigType , i + 1))
            self.brow_r.connect_follow_list.append (
                'connect_{}_{}{}Follow_{:03d}'.format ('r' , self.name , self.rigType , i + 1))
            self.brow_r.output_follow_list.append (
                'output_{}_{}{}Follow_{:03d}'.format ('r' , self.name , self.rigType , i + 1))
            self.brow_r.offset_follow_list.append (
                'offset_{}_{}{}Follow_{:03d}'.format ('r' , self.name , self.rigType , i + 1))

        # 创建左边的眉毛曲线和曲面名称
        self.brow_l.bpjnt_crv = self.brow_l.bpjnt_list [0].replace ('bpjnt' , 'bpcrv')
        self.brow_l.drive_crv = self.brow_l.bpjnt_list [0].replace ('bpjnt' , 'crv')
        self.brow_l.drive_suf = self.brow_l.bpjnt_list [0].replace ('bpjnt' , 'suf')
        # 创建左边的眉毛的整体控制器
        self.brow_l.master_ctrl = ('ctrl_{}_{}{}Master_001'.format ('l' , self.name , self.rigType))

        # 创建右边的眉毛曲线和曲面名称
        self.brow_r.bpjnt_crv = self.brow_r.bpjnt_list [0].replace ('bpjnt' , 'bpcrv')
        self.brow_r.drive_crv = self.brow_r.bpjnt_list [0].replace ('bpjnt' , 'crv')
        self.brow_r.drive_suf = self.brow_r.bpjnt_list [0].replace ('bpjnt' , 'suf')
        # 创建右边的眉毛的整体控制器
        self.brow_r.master_ctrl = ('ctrl_{}_{}{}Master_001'.format ('r' , self.name , self.rigType))


    def create_bpjnt (self) :
        # 获得brow_bpjnt 的路径
        self.brow_bpjnt_path = os.path.abspath (__file__ + "/../../../bpjnt/brow_bpjnt.ma")
        # 导入关节
        cmds.file (self.brow_bpjnt_path , i = True , rnn = True)


    def create_suf (self) :
        u"""
        创建用于眉毛部位的曲面
        """

        # 创建左边的bp定位眉毛曲线
        self.brow_l.drive_crv = cmds.duplicate (self.brow_l.bpjnt_crv , name = self.brow_l.drive_crv) [0]

        # 放样曲线出曲面
        # 通过两条曲线来放样制作左边眉毛的曲面
        self.brow_l.drive_suf = pipelineUtils.Pipeline.create_surface_on_curve (self.brow_l.drive_crv ,
                                                                                self.brow_l.drive_suf , spans = 6 ,
                                                                                offset = 0.2)

        # 创建右边的bp定位眉毛曲线
        self.brow_r.drive_crv = cmds.duplicate (self.brow_r.bpjnt_crv , name = self.brow_r.drive_crv) [0]

        # 放样曲线出曲面
        # 通过两条曲线来放样制作右边眉毛的曲面
        self.brow_r.drive_suf = pipelineUtils.Pipeline.create_surface_on_curve (self.brow_r.drive_crv ,
                                                                                self.brow_r.drive_suf , spans = 6 ,
                                                                                offset = 0.2)


    def create_joint (self) :
        super ().create_joint ()

        # 创建眉毛右边的关节
        self.brow_r.create_joint ()
        # 右边的关节对曲面进行蒙皮
        cmds.skinCluster (self.brow_r.jnt_list , self.brow_r.drive_suf , tsb = True)

        # 创建眉毛左边的关节
        self.brow_l.create_joint ()

        # 左边的关节对曲面进行蒙皮
        cmds.skinCluster (self.brow_l.jnt_list , self.brow_l.drive_suf , tsb = True)

        # 设置关节的可见性
        for jnt in self.brow_l.jnt_list + self.brow_r.jnt_list :
            cmds.setAttr (jnt + '.v' , 0)


    def create_folice (self) :
        u"""
        对曲面创建毛囊，并且创建权重的关节
        """
        # 创建左边的曲面上的毛囊和权重关节
        self.brow_l.follicle_dict = pipelineUtils.Pipeline.create_joint_follicle_on_surface (self.brow_l.drive_suf ,
                                                                                             self.brow_l.side ,
                                                                                             self.brow_l.rigType ,
                                                                                             jnt_number = 7)

        # 创建右边的曲面上的毛囊和权重关节
        self.brow_r.follicle_dict = pipelineUtils.Pipeline.create_joint_follicle_on_surface (self.brow_r.drive_suf ,
                                                                                             self.brow_r.side ,
                                                                                             self.brow_r.rigType ,
                                                                                             jnt_number = 7)


    def create_ctrl (self) :
        super ().create_ctrl ()
        ##左边
        # 创建眉毛左边的控制器 分为三层控制器： Master——Follow——ctrl
        # 创建眉毛左边的Master控制器
        self.brow_l.master_ctrl = controlUtils.Control.create_ctrl (self.brow_l.master_ctrl , shape = 'square' ,
                                                                    radius = 2 ,
                                                                    axis = 'X+' , pos = self.brow_l.jnt_list [1] ,
                                                                    parent = self.ctrl_parent)
        # 创建眉毛左边的Follow控制器
        for follow_ctrl , follow_jnt in zip (self.brow_l.ctrl_follow_list , self.brow_l.bpjnt_follow_list) :
            self.brow_l.follow_ctrl = controlUtils.Control.create_ctrl (follow_ctrl , shape = 'square' ,
                                                                        radius = 1 ,
                                                                        axis = 'X+' , pos = follow_jnt ,
                                                                        parent = self.brow_l.master_ctrl.replace (
                                                                            'ctrl' , 'output'))
        # 创建眉毛左边的蒙皮控制器
        self.brow_l.create_ctrl ()

        # 整理眉毛左边的控制器层级结构
        cmds.parent (self.brow_l.drive_suf , self.brow_l.ctrl_grp)
        cmds.parent (self.brow_l.master_ctrl.replace ('ctrl' , 'zero') , self.brow_l.ctrl_grp)
        cmds.parent (self.brow_l.follicle_dict ['deform_grp'] , self.brow_l.ctrl_grp)

        ##右边
        # 创建眉毛右边的控制器 分为三层控制器： Master——Follow——ctrl
        # 创建眉毛右边的Master控制器
        # 右边控制器的offset组都要设置缩放X为-1，才可以进行对称运动
        self.brow_r.master_ctrl = controlUtils.Control.create_ctrl (self.brow_r.master_ctrl , shape = 'square' ,
                                                                    radius = 2 ,
                                                                    axis = 'X+' , pos = self.brow_r.jnt_list [1] ,
                                                                    parent = self.ctrl_parent)
        cmds.setAttr (self.brow_r.master_ctrl.replace ('ctrl' , 'offset') + '.scaleX' , -1)

        # 创建眉毛右边的Follow控制器
        for follow_ctrl , follow_jnt in zip (self.brow_r.ctrl_follow_list , self.brow_r.bpjnt_follow_list) :
            self.brow_r.follow_ctrl = controlUtils.Control.create_ctrl (follow_ctrl , shape = 'square' ,
                                                                        radius = 1 ,
                                                                        axis = 'X+' , pos = follow_jnt ,
                                                                        parent = self.brow_r.master_ctrl.replace (
                                                                            'ctrl' , 'output'))
        # 右边控制器的offset组都要设置缩放X为-1，才可以进行对称运动
        for follow_offset in self.brow_r.offset_follow_list :
            cmds.setAttr (follow_offset + '.scaleX' , -1)

        # 创建眉毛右边的蒙皮控制器
        self.brow_r.create_ctrl ()
        # for ctrl_offset in self.brow_r.offset_list :
        #     cmds.setAttr (ctrl_offset + '.scaleX' , -1)


        # 整理眉毛右边的控制器层级结构
        cmds.parent (self.brow_r.drive_suf , self.brow_r.ctrl_grp)
        cmds.parent (self.brow_r.master_ctrl.replace ('ctrl' , 'zero') , self.brow_r.ctrl_grp)
        cmds.parent (self.brow_r.follicle_dict ['deform_grp'] , self.brow_r.ctrl_grp)

        # 整体控制器添加属性
        for ctrl in [self.brow_l.master_ctrl , self.brow_r.master_ctrl] :
            cmds.addAttr (ctrl , ln = 'BrowCtrlsVis' , dv = 0 , at = 'bool' , k = 1)
            cmds.addAttr (ctrl , ln = 'FollowValue' , nn = 'FollowValue---------' , dv = 0 , at = 'bool' ,
                          hidden = False , k = 0)
            for index in range (4) :
                cmds.addAttr (ctrl , ln = 'Follow{:02d}'.format (index + 1) , dv = 1 - 0.25 * index , at = 'float' ,
                              min = 0 ,
                              max = 1 , k = 1)


    def add_constraint (self) :
        super ().add_constraint ()
        self.brow_l.add_constraint ()
        self.brow_r.add_constraint ()
        # 左边
        # 左右两边的眉毛控制器约束中间眉心的控制器
        brow_l_output = self.brow_l.output_list [0]
        brow_r_output = self.brow_r.output_list [0]

        cmds.parentConstraint (brow_l_output , brow_r_output , self.driven_list [0] , mo = True)

        # 左边眉毛的整体控制器连接follow控制器
        self.create_connect (self.brow_r.master_ctrl , self.brow_r.connect_follow_list , side_value = -1)

        # 左边眉毛的整体控制器连接子级控制器的显示
        for zero in self.brow_r.zero_list :
            cmds.connectAttr (self.brow_r.master_ctrl + '.BrowCtrlsVis' ,
                              zero + '.visibility')

        # 左边眉毛的follow控制器组连接蒙皮控制器
        # follow_001控制器约束ctrl_001
        cmds.parentConstraint (self.brow_r.output_follow_list [0] , self.brow_r.driven_list [0] ,
                               mo = True)
        # follow_001控制器和follow_002控制器约束ctrl_002
        cmds.parentConstraint (self.brow_r.output_follow_list [0] , self.brow_r.output_follow_list [1] ,
                               self.brow_r.driven_list [1] ,
                               mo = True)
        # follow_002控制器约束ctrl_003
        cmds.parentConstraint (self.brow_r.output_follow_list [1] , self.brow_r.driven_list [2] ,
                               mo = True)
        # follow_002控制器和follow_003控制器约束ctrl_004
        cmds.parentConstraint (self.brow_r.output_follow_list [1] , self.brow_r.output_follow_list [2] ,
                               self.brow_r.driven_list [3] ,
                               mo = True)
        # follow_003控制器约束ctrl_005
        cmds.parentConstraint (self.brow_r.output_follow_list [2] , self.brow_r.driven_list [4] ,
                               mo = True)
        # follow_003控制器和follow_004控制器约束ctrl_006
        cmds.parentConstraint (self.brow_r.output_follow_list [2] , self.brow_r.output_follow_list [3] ,
                               self.brow_r.driven_list [5] ,
                               mo = True)

        # follow_004控制器约束ctrl_007
        cmds.parentConstraint (self.brow_r.output_follow_list [3] , self.brow_r.driven_list [6] ,
                               mo = True)

        ###右边
        # 右边眉毛的整体控制器连接follow控制器
        self.create_connect (self.brow_l.master_ctrl , self.brow_l.connect_follow_list)
        # 右边眉毛的整体控制器连接子级控制器的显示
        for zero in self.brow_l.zero_list :
            cmds.connectAttr (self.brow_l.master_ctrl + '.BrowCtrlsVis' ,
                              zero + '.visibility')
        # 右边眉毛的follow控制器组连接蒙皮控制器
        # follow_001控制器约束ctrl_001
        cmds.parentConstraint (self.brow_l.output_follow_list [0] , self.brow_l.driven_list [0] ,
                               mo = True)
        # follow_001控制器和follow_002控制器约束ctrl_002
        cmds.parentConstraint (self.brow_l.output_follow_list [0] , self.brow_l.output_follow_list [1] ,
                               self.brow_l.driven_list [1] ,
                               mo = True)
        # follow_002控制器约束ctrl_003
        cmds.parentConstraint (self.brow_l.output_follow_list [1] , self.brow_l.driven_list [2] ,
                               mo = True)
        # follow_002控制器和follow_003控制器约束ctrl_004
        cmds.parentConstraint (self.brow_l.output_follow_list [1] , self.brow_l.output_follow_list [2] ,
                               self.brow_l.driven_list [3] ,
                               mo = True)
        # follow_003控制器约束ctrl_005
        cmds.parentConstraint (self.brow_l.output_follow_list [2] , self.brow_l.driven_list [4] ,
                               mo = True)
        # follow_003控制器和follow_004控制器约束ctrl_006
        cmds.parentConstraint (self.brow_l.output_follow_list [2] , self.brow_l.output_follow_list [3] ,
                               self.brow_l.driven_list [5] ,
                               mo = True)

        # follow_004控制器约束ctrl_007
        cmds.parentConstraint (self.brow_l.output_follow_list [3] , self.brow_l.driven_list [6] ,
                               mo = True)


    def create_connect (self , driver , driven , side_value = 1) :
        u"""
        创建眉毛整体控制器与子级控制器的连接,连接控制器显示和跟随的值
        driver：驱动者
        driven：被驱动者
        side_value:左右两边因为需要镜像的缘故，控制器位移的数值是相反的，因此需要乘上side_value,L边为1，R边为-1
        """
        """
           创建眉毛整体控制器与子级控制器的连接，连接控制器显示和跟随的值
           driver：驱动者
           driven：被驱动者列表
           side_value: 左右两边因为需要镜像的缘故，控制器位移的数值是相反的，因此需要乘上side_value，L边为1，R边为-1
           """

        # 对于每个轴（X、Y、Z）进行处理
        for index in range (4) :
            # 创建位移的乘除节点
            trans_side_node = cmds.createNode ('multDoubleLinear' ,
                                               name = driven [index].replace ('connect' , 'transMult'))

            trans_node = cmds.createNode ('multiplyDivide' ,
                                          name = driven [index].replace ('connect' , 'trans'))
            # 创建位移的乘除节点的连接
            cmds.connectAttr (driver + '.translate' , trans_node + '.input1')

            cmds.connectAttr (driver + '.Follow{:02d}'.format (index + 1) , trans_side_node + '.input1')
            cmds.setAttr (trans_side_node + '.input2' , side_value)
            for axis in ['Y' , 'Z'] :
                cmds.connectAttr (driver + '.Follow{:02d}'.format (index + 1) , trans_node + '.input2{}'.format (axis))
            cmds.connectAttr (trans_side_node + '.output' , trans_node + '.input2X')

            # 将位移的乘除节点连接给对应的控制器
            cmds.connectAttr (trans_node + '.output' , driven [index] + '.translate')

            # 创建旋转的乘除节点

            rotate_side_node = cmds.createNode ('multDoubleLinear' ,
                                                name = driven [index].replace ('connect' , 'rotateMult'))
            rotate_node = cmds.createNode ('multiplyDivide' ,
                                           name = driven [index].replace ('connect' , 'rotate'))
            # 设置旋转的乘除节点的连接
            cmds.connectAttr (driver + '.rotate' , rotate_node + '.input1')
            cmds.connectAttr (driver + '.Follow{:02d}'.format (index + 1) , rotate_side_node + '.input1')
            cmds.setAttr (rotate_side_node + '.input2' , side_value)

            for axis in ['Y' , 'Z'] :
                cmds.connectAttr (driver + '.Follow{:02d}'.format (index + 1) , rotate_node + '.input2{}'.format (axis))
            cmds.connectAttr (rotate_side_node + '.output' , rotate_node + '.input2X')
            cmds.connectAttr (rotate_node + '.output' , driven [index] + '.rotate')


    def build_rig (self) :
        """
        创建绑定系统
        """
        self.create_namespace ()
        self.create_suf ()
        self.create_joint ()
        self.create_folice ()
        self.create_ctrl ()
        self.add_constraint ()


if __name__ == "__main__" :
    def build_setup () :
        brow_m = brow.Brow (side = 'm' , jnt_parent = None , ctrl_parent = None)
        brow_m.build_setup ()


    def build_rig () :
        brow_m = brow.Brow (side = 'm' , jnt_parent = None , ctrl_parent = None)
        brow_m.build_rig ()


    build_setup ()
    build_rig ()
