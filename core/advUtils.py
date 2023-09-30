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
                                                         radius = 0.5 , axis = 'Y+' , pos = lip_joint ,
                                                         parent = 'LipRegion_M')



            # 创建出来的次级控制器对lip关节进行约束
            pipelineUtils.Pipeline.create_constraint (lip_ctrl.replace ('ctrl' , 'output') , lip_joint ,
                                                      point_value = True , orient_value = True ,
                                                      scale_value = False ,
                                                      mo_value = True)
            # lip总控制器对创建出来的次级控制器组做约束
            pipelineUtils.Pipeline.create_constraint (lip_main_ctrl ,
                                                      lip_ctrl.replace ('ctrl' , 'driven') ,
                                                      point_value = True , orient_value = True ,
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
                                                             radius = 0.5 , axis = 'Y+' , pos = lid_joint ,
                                                             parent = lid_main_ctrl)
                # 控制器左右需要镜像一下，r边的情况下offset组的值需要乘-1
                if side == 'R' :
                    side_value = -1
                else :
                    side_value = 1
                for i in ['x' , 'y' , 'z'] :
                    cmds.setAttr (lid_ctrl.replace ('ctrl_' , 'offset_') + 'translate{}'.format (i) , side_value)
                # 创建出来的次级控制器对lid关节进行约束
                pipelineUtils.Pipeline.create_constraint (lid_ctrl.replace ('ctrl' , 'output') , lid_joint ,
                                                          point_value = True , orient_value = True ,
                                                          scale_value = True ,
                                                          mo_value = True)
