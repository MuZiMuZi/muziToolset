# coding=utf-8

u"""
这是一个用来编写hand(手指)绑定的类
继承了arm_rig

目前已有的功能：
create_hand_rig: 创建手指的FK绑定控制系统

fingerCurlRig : 设置手指关节旋转的姿势。


"""
from importlib import reload
from . import  matehuman_base_rig
from . import matehuman_arm_rig
from . import matehuman_ikfk_rig
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils



reload(pipelineUtils)
reload(jointUtils)
reload(hierarchyUtils)



class Hand_Rig(matehuman_base_rig.Base_Rig) :







    def __init__(self, joint_parent, control_parent,side) :
        super().__init__()
        self.joint_parent = joint_parent
        self.control_parent = control_parent
        self.side = side


    def create_hand_rig(self) :
        u"""
        创建手指的FK绑定控制系统
        """


        # 获取手指各模块的drv关节
        thumbHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('thumb_finger_{}'.format(side))
        indexHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('index_finger_{}'.format(side))
        middleHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('middle_finger_{}'.format(side))
        ringHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('ring_finger_{}'.format(side))
        pinkyHand_drv = matehumanUtils.MateHuman.get_mateHuman_drv_jnt('pinky_finger_{}'.format(side))

        # 创建手指各模块的FK关节链
        thumbHand_fk_system = matehuman_ikfk_rig.FK_Rig(thumbHand_drv, self.joint_parent,self.control_parent)
        thumbHand_fk_system.create_fk_chain()

        indexHand_fk_system = matehuman_ikfk_rig.FK_Rig(indexHand_drv , self.joint_parent , self.control_parent)
        indexHand_fk_system.create_fk_chain()
        
        middleHand_fk_system = matehuman_ikfk_rig.FK_Rig(middleHand_drv , self.joint_parent , self.control_parent)
        middleHand_fk_system.create_fk_chain()
        
        ringHand_fk_system = matehuman_ikfk_rig.FK_Rig(ringHand_drv , self.joint_parent , self.control_parent)
        ringHand_fk_system.create_fk_chain()
        
        pinkyHand_fk_system = matehuman_ikfk_rig.FK_Rig(pinkyHand_drv , self.joint_parent , self.control_parent)
        pinkyHand_fk_system.create_fk_chain()
        

        pose_ctrl_obj = controlUtils.Control.create_ctrl('ctrl_{}_handPose_001'.format('l') , shape = 'pPlatonic' ,
                                                         radius = 10 ,
                                                         axis = 'X+' ,
                                                         pos = thumbHand_fk_chain[0] , parent = hand_ctrl_grp)
        pose_ctrl_mirror_obj = controlUtils.Control.create_ctrl('ctrl_{}_handPose_001'.format('r') ,
                                                                shape = 'pPlatonic' ,
                                                                radius = 10 ,
                                                                axis = 'X+' ,
                                                                pos = thumbHand_fk_chain_mirror[0] ,
                                                                parent = hand_ctrl_grp_mirror)

        # self.fingerCurlRig()



    def fingerCurlRig(self) :
        u"""设置手指关节旋转的姿势。
             """
        # 获取手指名称
        finger_names = ['thumb' , 'index' , 'middle' , 'ring' , 'pinky']

        # 获取关节节数名称
        digit_names = {'thumb' : ['Metacarpal' , 'Base' , 'Tip']}

        # 获取curl的值
        curl_mult_values = {'thumb' : [-3 , -5 , -7] ,
                            'index' : [0 , -7.5 , -10.5 , -8] ,
                            'middle' : [0 , -7.5 , -10.5 , -8] ,
                            'ring' : [0 , -7.5 , -10.5 , -8] ,
                            'pinky' : [0 , -7.5 , -10.5 , -8]}

        # 循环到'lr'两边的每一侧
        for side in 'lr' :
            # 获取手姿势控制的控制器
            pose_ctrl = 'ctrl_{}_handPose_001'.format(side)
            # 循环到每个手指，并添加curl attr
            for finger in finger_names :
                cmds.addAttr(pose_ctrl , longName = finger + 'Curl' , attributeType = 'float' , keyable = True ,
                             minValue = 0 , maxValue = 10)
                curl_attr = '{}.{}Curl'.format(pose_ctrl , finger)

                # 获取卷曲值
                curl_values = curl_mult_values[finger]
                # 获取关节节数名称
                finger_digits = digit_names.get(finger , ['Metacarpal' , 'Base' , 'Mid' , 'Tip'])
                # 循环到每个手指并连接卷曲的值
                for digit , val in zip(finger_digits , curl_values) :
                    offset_name = 'offset_{}_{}{}Bind_001'.format(side , finger , digit.title())

                    if val :
                        # 创建乘法节点
                        mult_node = cmds.createNode('multDoubleLinear' ,
                                                    name = 'mult_{}_{}{}Curl_001'.format(side , finger , digit.title()))
                        # 连接驱动的节点的属性
                        cmds.connectAttr(curl_attr , mult_node + '.input1')
                        # 设置卷曲值
                        cmds.setAttr(mult_node + '.input2' , val)

                        # 将输出连接到偏移组的rotateZ
                        cmds.connectAttr(mult_node + '.output' , offset_name + '.rotateZ')
