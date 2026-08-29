# coding=utf-8
u"""
这是一个用来编写adv插件的流程工具的类

目前已有的功能：
"""
import maya.cmds as cmds

from . import pipelineUtils , controlUtils , attrUtils


class AdvUtils (object) :

    # adv嘴唇中间添加新的次级控制器，应用于动画制作抿嘴的情况，注意需要吸附枢纽
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
                                                      point_value = False , orient_value = False , parent_value = True ,
                                                      scale_value = False ,
                                                      mo_value = True)
            # lip总控制器对创建出来的次级控制器组做约束
            pipelineUtils.Pipeline.create_constraint (lip_main_ctrl ,
                                                      lip_ctrl.replace ('ctrl' , 'driven') ,
                                                      point_value = False , orient_value = False , parent_value = True ,
                                                      scale_value = False ,
                                                      mo_value = True)


    # 眼皮中间添加新的次级控制器，应用于动画制作的情况
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


    # adv脸部在生成的时候会自动连接CheekRaiser控制器的translateY轴，需要在控制器上层创建一个新的组来重新连接
    @staticmethod
    def connect_CheekRaiser_ctrl () :
        """
        adv脸部在生成的时候会自动连接CheekRaiser控制器的translateY轴，需要在控制器上层创建一个新的组来重新连接
        CheekRaiser_ctrl:CheekRaiser控制器
        bw_node:连接CheekRaiser控制器的translateY的节点
        """
        # 分成左右两边两种情况在控制器上层创建一个新的组来重新连接
        for side in ['L' , 'R'] :
            # 获取CheekRaiser控制器和连接控制器的节点
            CheekRaiser_ctrl = 'CheekRaiser_{}'.format (side)
            bw_node = 'bwCheekRaiser_{}_translateY'.format (side)

            # 在CheekRaiser控制器上层创建新的控制器层级组
            con_CheekRaiser_grp = cmds.group (CheekRaiser_ctrl , n = 'con_' + CheekRaiser_ctrl)

            # 重新连接控制器的translateY
            cmds.connectAttr (bw_node + '.output' , con_CheekRaiser_grp + '.translateY')
            cmds.disconnectAttr (bw_node + '.output' , CheekRaiser_ctrl + '.translateY')


    # adv自带的脸颊控制器不够丰富，无法满足动画的需要，需要添加两个控制器，
    @staticmethod
    def add_cheek_ctrl () :
        """
        adv自带的脸颊控制器不够丰富，无法满足动画的需要，需要添加两个控制器，
        一个是眼皮下方用来控制鼻子外侧与颧骨这一带的控制器，
        第二个是颧骨到耳朵处用来模拟腮帮子咬合的效果
        """
        for type in ['cheekAdj' , 'cheekOcclus'] :
            for side in ['L' , 'R'] :
                type_joint = 'jnt_{}_{}_001'.format (side , type)

                type_joint = cmds.createNode ('joint' , name = type_joint , parent = 'FaceJoint_M')
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
                cmds.setAttr (type_ctrl.replace ('ctrl_' , 'offset_') + '.scaleX' , side_value)
                # 创建出来的控制器对关节进行约束
                pipelineUtils.Pipeline.create_constraint (type_ctrl.replace ('ctrl' , 'output') , type_joint ,
                                                          point_value = False , orient_value = False ,
                                                          parent_value = True ,
                                                          scale_value = True ,
                                                          mo_value = True)


    # adv自带的下巴控制器不够丰富，无法满足动画的需要，需要添加两个控制器用来凹进去夸张表情，
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


    # adv重新生成后手指的驱动可能会消失，于是可以依靠这个代码重新连接,选择所有需要驱动的手指控制器加选Finger控制器创建连接
    @staticmethod
    def finger_Connect () :
        '''
        adv重新生成后手指的驱动可能会消失，于是可以依靠这个代码重新连接
        选择所有需要驱动的手指控制器加选Finger控制器创建连接
        '''


        # 选择所有需要驱动的手指控制器加选Finger控制器创建连接
        def myDrv (sdk , ctrl , str) :
            cmds.setAttr (ctrl + str , -2)
            cmds.setAttr (sdk + '.ry' , -18)
            cmds.setDrivenKeyframe (sdk + '.ry' , cd = ctrl + str , ott = 'linear')
            cmds.setAttr (ctrl + str , 10)
            cmds.setAttr (sdk + '.ry' , 90)
            cmds.setDrivenKeyframe (sdk + '.ry' , cd = ctrl + str , itt = 'linear')
            cmds.setAttr (ctrl + str , 0)
            cmds.setAttr (sdk + '.ry' , 0)
            cmds.setDrivenKeyframe (sdk + '.ry' , cd = ctrl + str)


        ctrl = cmds.ls (sl = True)
        myStr = ['.indexCurl' , '.middleCurl' , '.ringCurl' , '.pinkyCurl' , '.thumbCurl']
        for i in ctrl [0 :-1] :
            Extra = re.sub ('FK' , 'FKExtra' , i)
            Grp = cmds.listRelatives (Extra , p = True) [0]
            SDK1 = cmds.group (em = True , p = Grp , n = 'SDK1' + i)
            cmds.parent (Extra , SDK1)
            if 'Index' in i :
                myDrv (SDK1 , ctrl [-1] , myStr [0])
            if 'Middle' in i :
                myDrv (SDK1 , ctrl [-1] , myStr [1])
            if 'Ring' in i :
                myDrv (SDK1 , ctrl [-1] , myStr [2])
            if 'Pinky' in i :
                myDrv (SDK1 , ctrl [-1] , myStr [3])
            if 'Thumb' in i :
                myDrv (SDK1 , ctrl [-1] , myStr [4])
            if 'Cup' in i :
                cmds.setAttr (ctrl [-1] + '.cup' , 0)
                cmds.setAttr (SDK1 + '.rx' , 0)
                cmds.setDrivenKeyframe (SDK1 + '.rx' , cd = ctrl [-1] + '.cup' , ott = 'linear')
                cmds.setAttr (ctrl [-1] + '.cup' , 10)
                cmds.setAttr (SDK1 + '.rx' , 65)
                cmds.setDrivenKeyframe (SDK1 + '.rx' , cd = ctrl [-1] + '.cup' , itt = 'linear')


        def myDrv (sdk , min , max , ctrl) :
            cmds.setAttr (ctrl + '.spread' , -5)
            cmds.setAttr (sdk + '.rz' , min)
            cmds.setDrivenKeyframe (sdk + '.rz' , cd = ctrl + '.spread' , ott = 'linear')
            cmds.setAttr (ctrl + '.spread' , 10)
            cmds.setAttr (sdk + '.rz' , max)
            cmds.setDrivenKeyframe (sdk + '.rz' , cd = ctrl + '.spread' , itt = 'linear')
            cmds.setAttr (ctrl + '.spread' , 0)
            cmds.setAttr (sdk + '.rz' , 0)
            cmds.setDrivenKeyframe (sdk + '.rz' , cd = ctrl + '.spread')


        for i in ctrl [0 :-1] :
            Grp = cmds.listRelatives ('SDK1' + i , p = True) [0]
            SDK2 = cmds.group (em = True , p = Grp , n = 'SDK2' + i)

            cmds.parent ('SDK1' + i , SDK2)
            if 'PinkyFinger1' in i :
                myDrv (SDK2 , 30 , -60 , ctrl [-1])
            if 'RingFinger1' in i :
                myDrv (SDK2 , 15 , -30 , ctrl [-1])
            if 'IndexFinger1' in i :
                myDrv (SDK2 , -20 , 40 , ctrl [-1])


    # 添加adv修型关节的控制器控制
    @staticmethod
    def add_Slider_ctrl () :
        """
        添加adv修型关节的控制器控制
        """
        #获取adv上所具有的修型关节
        slider_joints = cmds.ls ('*Slider*' , type = 'joint')
        #创建总的关节控制器层级总组
        slider_ctrl_grp = cmds.createNode ('transform' , name = 'slider_ctrl_grp')
        for slider_joint in slider_joints :
            # 获取关节上的slide数值
            # 列出关节上的所有属性
            joint_all_attrs = cmds.listAttr (slider_joint , connectable = True , inUse = True)
            # 判断是否具有slide这个属性
            if 'slide' in joint_all_attrs :
                # 创建对应的修型控制器
                slider_ctrl = controlUtils.Control.create_ctrl (name = 'ctrl_{}_001'.format (slider_joint) ,
                                                                shape = 'Cube' ,
                                                                radius = 1 , axis = 'Y+' , pos = slider_joint ,
                                                                parent = slider_ctrl_grp)
                # 锁定不需要的属性
                attrs_list = ['translateX' , 'translateY' , 'translateZ' , 'rotateX' , 'rotateY' , 'rotateZ' ,
                              'scaleX' , 'scaleY' , 'scaleZ' , 'rotateOrder' , 'visibility' , 'subCtrlVis']
                attrUtils.Attr.lock_and_hide_attrs (slider_ctrl , attrs_list , lock = True , hide = True)
                # 修型控制器上添加对应的slide属性用于连接关节的slide属性
                cmds.addAttr (slider_ctrl , longName = 'slide_ctrl' , attributeType = 'float' , keyable = True)
                # 获取关节上slide的值设置在修型控制器上
                cmds.setAttr (slider_ctrl + '.slide_ctrl' , cmds.getAttr (slider_joint + '.slide'))
                # 连接修型控制器和关节的属性
                cmds.connectAttr (slider_ctrl + '.slide_ctrl' , slider_joint + '.slide')

                # 获取关节的父关节，对控制器上层组做父子约束
                pipelineUtils.Pipeline.create_constraint (slider_joint , slider_ctrl.replace ('ctrl' , 'driven') ,
                                                          parent_value = True ,
                                                          scale_value = True ,
                                                          mo_value = True)

            else :
                return
