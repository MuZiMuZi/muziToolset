# coding=utf-8

u"""
这是一个用来编写footIK（脚掌）绑定的类
继承了leg_rig
目前已有的功能：

create_footIK_rig：创建脚掌Ik的控制器绑定



"""
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils


reload(pipelineUtils)
reload(jointUtils)

import leg_rig
import ikfk_rig


# leg_bp_joints = ['bpjnt_l_hip_001', 'bpjnt_l_knee_001',' bpjnt_l_ankle_001','bpjnt_l_ball_001','bpjnt_l_toe_001']

class Foot_Rig(leg_rig.Leg_Rig) :


    def __init__(self , bp_joints = None , joint_parent = None , control_parent = None , mirror = True ,
                 space_list = None) :
        super(Foot_Rig , self).__init__(bp_joints = bp_joints , joint_parent = joint_parent ,
                                        control_parent = control_parent , space_list = space_list)
        self.mirror = mirror
        self.foot_bp_joints = self.get_modular_bp_joints(self.foot_rig)
        self.bp_joints = self.foot_bp_joints
        footHeelPivot_jnt = 'jnt_l_footHeelPivot_001'
        cmds.mirrorJoint(footHeelPivot_jnt , mirrorYZ = True , mirrorBehavior = True ,
                         searchReplace = ['_l_' , '_r_'])
        # self.create_footIK_rig('l')
        # self.create_footIK_rig('r')


    def create_footIK_rig(self , side) :
        if side == 'l' :
            side_value = 1
        else :
            side_value = -1
        # 定义各部位关节的名称
        ankle_ctrl = 'ctrl_{}_ankleIK_001'.format(side)
        footHeelPivot_jnt = 'jnt_{}_footHeelPivot_001'.format(side)
        footToePivot_jnt = 'jnt_{}_footToePivot_001'.format(side)
        footInnPivot_jnt = 'jnt_{}_footInnPivot_001'.format(side)
        footOutPivot_jnt = 'jnt_{}_footOutPivot_001'.format(side)

        hip_IK_ikhandle = 'ikhandle_{}_hipIK_001'.format(side)
        ankle_IK_jnt = 'jnt_{}_ankleIK_001'.format(side)
        ball_IK_jnt = 'jnt_{}_ballIK_001'.format(side)
        toe_IK_jnt = 'jnt_{}_toeIK_001'.format(side)

        # 创建脚掌定位的控制器
        footHeelPivot_ctrl = footHeelPivot_jnt.replace('jnt_' , 'ctrl_')
        footHeelPivot_ctrl_obj = controlUtils.Control.create_ctrl(footHeelPivot_ctrl , shape = 'ball' , radius = 3 ,
                                                                  axis = 'X+' ,
                                                                  pos = footHeelPivot_jnt ,
                                                                  parent = ankle_ctrl.replace('ctrl_' , 'output_'))
        footToePivot_ctrl = footToePivot_jnt.replace('jnt_' , 'ctrl_')
        footToePivot_ctrl_obj = controlUtils.Control.create_ctrl(footToePivot_ctrl , shape = 'ball' , radius = 3 ,
                                                                 axis = 'X+' ,
                                                                 pos = footToePivot_jnt ,
                                                                 parent = footHeelPivot_ctrl.replace('ctrl_' ,
                                                                                                     'output_'))
        footInnPivot_ctrl = footInnPivot_jnt.replace('jnt_' , 'ctrl_')
        footInnPivot_ctrl_obj = controlUtils.Control.create_ctrl(footInnPivot_ctrl , shape = 'ball' , radius = 3 ,
                                                                 axis = 'X+' ,
                                                                 pos = footInnPivot_jnt ,
                                                                 parent = footToePivot_ctrl.replace('ctrl_' ,
                                                                                                    'output_'))
        footOutPivot_ctrl = footOutPivot_jnt.replace('jnt_' , 'ctrl_')
        footOutPivot_ctrl_obj = controlUtils.Control.create_ctrl(footOutPivot_ctrl , shape = 'ball' , radius = 3 ,
                                                                 axis = 'X+' ,
                                                                 pos = footOutPivot_jnt ,
                                                                 parent = footInnPivot_ctrl.replace('ctrl_' ,
                                                                                                    'output_'))

        ball_IK_handle = cmds.ikHandle(name = ball_IK_jnt.replace('jnt_' , 'ikhandle_') , startJoint = ankle_IK_jnt ,
                                       endEffector = ball_IK_jnt ,
                                       sticky = 'sticky' , solver = 'ikSCsolver' , setupForRPsolver = True)[0]

        toe_IK_handle = cmds.ikHandle(name = toe_IK_jnt.replace('jnt_' , 'ikhandle_') , startJoint = ball_IK_jnt ,
                                      endEffector = toe_IK_jnt ,
                                      sticky = 'sticky' , solver = 'ikSCsolver' , setupForRPsolver = True)[0]

        # 创建ball关节，toe关节的spineIK设置
        ball_IK_ctrl = 'ctrl_{}_ballIk_001'.format(side)
        ball_IK_ctrl_obj = controlUtils.Control.create_ctrl(ball_IK_ctrl , shape = 'cube' , radius = 11 ,
                                                            axis = 'X+' ,
                                                            pos = ball_IK_jnt ,
                                                            parent = footOutPivot_ctrl.replace('ctrl_' , 'output_'))

        toe_IK_ctrl = 'ctrl_{}_toeIk_001'.format(side)
        toe_IK_ctrl_obj = controlUtils.Control.create_ctrl(toe_IK_ctrl , shape = 'cube' , radius = 6 ,
                                                           axis = 'X+' ,
                                                           pos = toe_IK_jnt ,
                                                           parent = footOutPivot_ctrl.replace('ctrl_' , 'output_'))
        cmds.parent(hip_IK_ikhandle , ball_IK_ctrl)
        cmds.parent(ball_IK_handle , ball_IK_ctrl)
        cmds.parent(toe_IK_handle , toe_IK_ctrl)

        # 在ankleIK控制器上添加对应的脚部控制开关
        cmds.addAttr(ankle_ctrl , attributeType = 'bool' , longName = 'footCtrl' , niceName = ' footCtrl------ ' ,
                     keyable = False)
        cmds.setAttr(ankle_ctrl + '.footCtrl' , channelBox = True , lock = True)

        cmds.addAttr(ankle_ctrl , attributeType = 'double' , longName = 'toeTap' , niceName = u' 抬脚尖 ' ,
                     keyable = True)
        cmds.addAttr(ankle_ctrl , attributeType = 'double' , longName = 'heelTap' , niceName = u' 抬脚跟 ' ,
                     keyable = True)

        cmds.addAttr(ankle_ctrl , attributeType = 'double' , longName = 'toeRoll' , niceName = u' 沿着脚尖旋转 ' ,
                     keyable = True)
        cmds.addAttr(ankle_ctrl , attributeType = 'double' , longName = 'heelRoll' , niceName = u' 沿着脚跟旋转 ' ,
                     keyable = True)

        cmds.addAttr(ankle_ctrl , attributeType = 'double' , longName = 'toeSide' , niceName = u' 沿着脚尖滑动 ' ,
                     keyable = True)
        cmds.addAttr(ankle_ctrl , attributeType = 'double' , longName = 'heelSide' , niceName = u' 沿着脚跟滑动 ' ,
                     keyable = True)

        # cmds.addAttr(ankle_ctrl, attributeType = 'double', longName = 'bank', niceName = u' 脚左右抬起 ', keyable = True)

        # 在ankleIK控制器上连接对应的脚部控制开关
        cmds.connectAttr(ankle_ctrl + '.toeTap' , footToePivot_ctrl.replace('ctrl_' , 'connect_') + '.rotateZ')
        cmds.connectAttr(ankle_ctrl + '.heelTap' , footHeelPivot_ctrl.replace('ctrl_' , 'connect_') + '.rotateZ')

        cmds.connectAttr(ankle_ctrl + '.toeRoll' , footToePivot_ctrl.replace('ctrl_' , 'connect_') + '.rotateX')
        cmds.connectAttr(ankle_ctrl + '.heelRoll' , footHeelPivot_ctrl.replace('ctrl_' , 'connect_') + '.rotateX')

        cmds.connectAttr(ankle_ctrl + '.toeSide' , footToePivot_ctrl.replace('ctrl_' , 'connect_') + '.rotateY')
        cmds.connectAttr(ankle_ctrl + '.heelSide' , footHeelPivot_ctrl.replace('ctrl_' , 'connect_') + '.rotateY')

        # # 连接脚左右抬起的控制
        # footInnPivot_connect =  footInnPivot_ctrl.replace('ctrl_', 'connect_')
        # footOutPivot_connect = footOutPivot_ctrl.replace('ctrl_', 'connect_')
        # cmds.connectAttr(ankle_ctrl + '.bank', footInnPivot_connect + '.rotateZ')
        # cmds.setAttr(footInnPivot_ctrl.replace('ctrl_', 'connect_') + '.rotateZ')
        # mult_bank_node = cmds.createNode('multDoubleLinear',name = footInnPivot_ctrl.replace('ctrl_','mult_'))
        # cmds.setAttr(mult_bank_node + '.input2',-1 * side_value)
        # cmds.connectAttr(ankle_ctrl + '.bank ',mult_bank_node + '.input1')
        # cmds.connectAttr(mult_bank_node + '.output',footOutPivot_connect + '.rotateZ')
        #
        # # 设置脚左右抬起的极限值控制
        # cmds.transformLimits( footInnPivot_connect,rz = (0, 45),erz = (True, False))
        # cmds.transformLimits(footOutPivot_connect, rz = (0, 45), erz = (True, False))
