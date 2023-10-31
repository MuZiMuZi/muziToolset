# coding=utf-8
u"""
这是一个用来编写adv插件的流程工具的类

目前已有的功能：
"""
from . import pipelineUtils , controlUtils , hierarchyUtils
from importlib import reload


reload (controlUtils)
import maya.cmds as cmds


class AdvUtils (object) :

    @staticmethod
    def add_lip_ctrl () :
        '''
        adv嘴唇中间添加新的次级控制器，应用于动画制作抿嘴的情况，注意需要吸附枢纽
        思路：
        adv的嘴唇绑定是通过面片上的关节来驱动的，因此只需要找到对应中间的关节添加上新的控制器，并且制作约束即可
        次级控制器约束关节，嘴唇大环控制器约束次级控制器
        注意约束不要添加缩放约束
        '''

        # 分成上下嘴唇两种情况制作次级控制器
        for type in ['upperLip' , 'lowerLip'] :
            lip_joint = type + 'RibbonJoint_M'
            lip_surface = type + 'CenterPlane'
            lip_main_ctrl = type + '_M'

            # 删除lip关节上自带的约束
            cmds.select (lip_joint , r = True)
            pipelineUtils.Pipeline.delete_constraints ()

            # 创建新的次级控制器并且吸附到lip关节上
            lip_ctrl = controlUtils.Control.create_ctrl (name = 'ctrl_m_{}Lip_001'.format (type) , shape = 'Cube' ,
                                                         radius = 0.3 , axis = 'Y+' , pos = lip_joint ,
                                                         parent = 'LipRegion_M')



            # 创建出来的次级控制器对lip关节进行约束
            pipelineUtils.Pipeline.create_constraint (lip_ctrl.replace ('ctrl' , 'output') , lip_joint ,
                                                      point_value = False , orient_value = False ,parent_value = True,
                                                      scale_value = False ,
                                                      mo_value = True)
            # lip总控制器对创建出来的次级控制器组做约束
            pipelineUtils.Pipeline.create_constraint (lip_main_ctrl ,
                                                      lip_ctrl.replace ('ctrl' , 'driven') ,
                                                      point_value = False , orient_value = False , parent_value = True ,
                                                      scale_value = False ,
                                                      mo_value = True)


    @staticmethod
    def add_lid_ctrl () :
        '''
        眼皮中间添加新的次级控制器，应用于动画制作的情况
        思路：
        对应中间的关节upperLidJoint_L 添加上新的控制器，并且制作约束即可
        次级控制器约束关节，嘴唇大环控制器约束次级控制器
        注意约束不要添加缩放约束
        '''

        # 分成上下嘴唇两种情况制作次级控制器
        for type in ['upperLid' , 'lowerLid' , 'lowerLidOuter' , 'upperLidOuter'] :
            for side in ['L' , 'R'] :
                lid_joint = type + 'Joint_{}'.format (side)
                lid_main_ctrl = type + '_{}'.format (side)

                # 删除lid关节上自带的约束
                cmds.select (lid_joint , r = True)
                pipelineUtils.Pipeline.delete_constraints ()

                # 创建新的次级控制器并且吸附到lid关节上
                lid_ctrl = controlUtils.Control.create_ctrl (name = 'ctrl_{}_{}_001'.format (side , type) ,
                                                             shape = 'Cube' ,
                                                             radius = 0.3 , axis = 'Y+' , pos = lid_joint ,
                                                             parent = lid_main_ctrl)
                # 控制器左右需要镜像一下，r边的情况下offset组的值需要乘-1
                if side == 'R' :
                    side_value = -1
                else :
                    side_value = 1
                for i in ['X' , 'Y' , 'Z'] :
                    cmds.setAttr (lid_ctrl.replace ('ctrl_' , 'offset_') + '.scale{}'.format (i) , side_value)
                # 创建出来的次级控制器对lid关节进行约束
                pipelineUtils.Pipeline.create_constraint (lid_ctrl.replace ('ctrl' , 'output') , lid_joint ,
                                                          point_value = False , orient_value = False ,
                                                          parent_value = True ,
                                                          scale_value = True ,
                                                          mo_value = True)


    @staticmethod
    def connect_CheekRaiser_ctrl():
        """
        adv脸部在生成的时候会自动连接CheekRaiser控制器的translateY轴，需要在控制器上层创建一个新的组来重新连接
        CheekRaiser_ctrl:CheekRaiser控制器
        bw_node:连接CheekRaiser控制器的translateY的节点
        """
        # 分成左右两边两种情况在控制器上层创建一个新的组来重新连接
        for side in ['L' , 'R'] :
            #获取CheekRaiser控制器和连接控制器的节点
            CheekRaiser_ctrl =  'CheekRaiser_{}'.format (side)
            bw_node = 'bwCheekRaiser_{}_translateY'.format(side)

            #在CheekRaiser控制器上层创建新的控制器层级组
            con_CheekRaiser_grp = cmds.group (CheekRaiser_ctrl, n = 'con_' + CheekRaiser_ctrl)

            #重新连接控制器的translateY
            cmds.connectAttr (bw_node + '.output' , con_CheekRaiser_grp + '.translateY')
            cmds.disconnectAttr(bw_node + '.output' , CheekRaiser_ctrl + '.translateY')


    @staticmethod
    def add_cheek_ctrl():
        """
        adv自带的脸颊控制器不够丰富，无法满足动画的需要，需要添加两个控制器，
        一个是眼皮下方用来控制鼻子外侧与颧骨这一带的控制器，
        第二个是颧骨到耳朵处用来模拟腮帮子咬合的效果
        """
        for type in ['cheekAdj' , 'cheekOcclus'] :
            for side in ['L' , 'R'] :
                type_joint = 'jnt_{}_{}_001'.format (side , type)

                type_joint = cmds.createNode('joint',name = type_joint,parent = 'FaceJoint_M')
                # 创建新的控制器并且吸附到对应的关节上
                type_ctrl = controlUtils.Control.create_ctrl (name = 'ctrl_{}_{}_001'.format (side , type) ,
                                                             shape = 'Cube' ,
                                                             radius = 0.3 , axis = 'Y+' , pos = type_joint ,
                                                             parent = None)
                # 控制器左右需要镜像一下，r边的情况下offset组的值需要乘-1
                if side == 'R' :
                    side_value = -1
                else :
                    side_value = 1
                cmds.setAttr (type_ctrl.replace ('ctrl_' , 'offset_') + '.scaleX', side_value)
            # 创建出来的控制器对关节进行约束
                pipelineUtils.Pipeline.create_constraint (type_ctrl.replace ('ctrl' , 'output') , type_joint ,
                                                          point_value = False , orient_value = False ,
                                                          parent_value = True ,
                                                          scale_value = True ,
                                                          mo_value = True)


    @staticmethod
    def add_jaw_ctrl () :
        """
        adv自带的下巴控制器不够丰富，无法满足动画的需要，需要添加两个控制器用来凹进去夸张表情，
        一个下嘴唇底部用来凹口轮扎肌的动态，jaw_adj ,这是两个关节组成的关节链条
        第二个是下巴底下用来突出下巴的动态
        """

        # 创建新的次级控制器并且吸附到lid关节上
        jaw_adj_ctrl = controlUtils.Control.create_ctrl (name = 'ctrl_{}_{}_001'.format (side , type) ,
                                                     shape = 'Cube' ,
                                                     radius = 0.3 , axis = 'Y+' , pos = lid_joint ,
                                                     parent = lid_main_ctrl)
        'TODO:'

        pass
