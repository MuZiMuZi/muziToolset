# coding=utf-8

u"""
这是一个用来编写chest（胸部）绑定的类，之后的绑定都会在这个类的基础上逐级继承下去
继承了ikfk_rig

目前已有的功能：

create_arm_rig：创建手臂的控制器绑定



"""
from importlib import reload
from .import ikfk_rig
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils


reload(hierarchyUtils)
reload (controlUtils)

chest_bp_joints = ['bpjnt_l_shoulder_001' , 'bpjnt_l_elbow_001' , ' bpjnt_l_wrist_001']


class Chest_Rig(ikfk_rig.IKFK_Rig) :


    def __init__(self , bp_joints = None , joint_parent = None , control_parent = None , mirror = False ,
                 space_list = None) :
        super(Chest_Rig , self).__init__(bp_joints = bp_joints , joint_parent = joint_parent ,
                                         control_parent = control_parent , space_list = space_list)

        self.chest_jnt = 'jnt_m_chest_001'
        self.sternumPlvot_jnt = 'jnt_m_sternumPlvot_001'
        self.ribA_jnt = 'jnt_l_ribA_001'
        self.ribB_jnt = 'jnt_l_ribB_001'
        self.chest_ctrl = self.chest_jnt.replace('jnt_' , 'ctrl_')
        self.ribA_jnt_mirror = cmds.mirrorJoint(self.ribA_jnt , mirrorYZ = True , mirrorBehavior = True ,
                                                searchReplace = ['_l_' , '_r_'])[0]
        self.ribB_jnt_mirror = cmds.mirrorJoint(self.ribB_jnt , mirrorYZ = True , mirrorBehavior = True ,
                                                searchReplace = ['_l_' , '_r_'])[0]
        self.ribA_jnt_grp = hierarchyUtils.Hierarchy.get_child_object(self.ribA_jnt)
        self.ribB_jnt_grp = hierarchyUtils.Hierarchy.get_child_object(self.ribB_jnt)
        self.ribA_jnt_grp_mirror = hierarchyUtils.Hierarchy.get_child_object(self.ribA_jnt_mirror)
        self.ribB_jnt_grp_mirror = hierarchyUtils.Hierarchy.get_child_object(self.ribB_jnt_mirror)
        self.chest_jnt_grp = ['jnt_m_chest_001']
        self.make(self.chest_jnt_grp)


    def create_chest_rig(self) :
        # 创建胸腔的控制器
        chest_ctrl_obj = controlUtils.Control.create_ctrl(self.chest_ctrl , shape = 'ball' , radius = 13 , axis = 'Z+' ,
                                                          pos = self.chest_jnt ,
                                                          parent = self.control_grp)

        # 设置胸腔控制器的极限值为-2到2，-2和2是呼吸的极限值，默认的吸气呼气应该是1和-1
        cmds.transformLimits(self.chest_ctrl , translationX = (-2 , 2) , enableTranslationX = (True , True))

        # 创建一个相乘节点来连接胸腔的旋转
        sternum_mult_node = cmds.createNode('multDoubleLinear' , name = self.sternumPlvot_jnt.replace('jnt_' , 'mult_'))
        cmds.connectAttr(self.chest_ctrl + '.translateX' , sternum_mult_node + '.input1')
        cmds.setAttr(sternum_mult_node + '.input2' , 3)
        cmds.connectAttr(sternum_mult_node + '.output' , self.sternumPlvot_jnt + '.rotateZ')

        # 创建rotateIK的handle来实现胸腔起伏的效果
        ribA_ikhandle_node = \
            cmds.ikHandle(name = self.ribA_jnt.replace('jnt_' , 'ikhandle_') , startJoint = self.ribA_jnt_grp[0] ,
                          endEffector = self.ribA_jnt_grp[-1] ,
                          sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True)[0]
        ribB_ikhandle_node = \
            cmds.ikHandle(name = self.ribB_jnt.replace('jnt_' , 'ikhandle_') , startJoint = self.ribB_jnt_grp[0] ,
                          endEffector = self.ribB_jnt_grp[-1] ,
                          sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True)[0]

        ribA_ikhandle_node_mirror = cmds.ikHandle(name = self.ribA_jnt_mirror.replace('jnt_' , 'ikhandle_') ,
                                                  startJoint = self.ribA_jnt_grp_mirror[0] ,
                                                  endEffector = self.ribA_jnt_grp_mirror[-1] ,
                                                  sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True)[
            0]
        ribB_ikhandle_node_mirror = cmds.ikHandle(name = self.ribB_jnt_mirror.replace('jnt_' , 'ikhandle_') ,
                                                  startJoint = self.ribB_jnt_grp_mirror[0] ,
                                                  endEffector = self.ribB_jnt_grp_mirror[-1] ,
                                                  sticky = 'sticky' , solver = 'ikRPsolver' , setupForRPsolver = True)[
            0]

        # 整理ikhandle的层级
        cmds.parent(ribA_ikhandle_node , ribB_ikhandle_node , ribA_ikhandle_node_mirror , ribB_ikhandle_node_mirror ,
                    self.rigNode_World)

        # 创建对应的相乘节点来连接ikhandle的twist属性来控制胸腔的运动
        ribA_mult_node = cmds.createNode('multDoubleLinear' , name = self.ribA_jnt.replace('jnt_' , 'mult_'))
        ribB_mult_node = cmds.createNode('multDoubleLinear' , name = self.ribB_jnt.replace('jnt_' , 'mult_'))
        ribA_mult_node_mirror = cmds.createNode('multDoubleLinear' ,
                                                name = self.ribA_jnt_mirror.replace('jnt_' , 'mult_'))
        ribB_mult_node_mirror = cmds.createNode('multDoubleLinear' ,
                                                name = self.ribB_jnt_mirror.replace('jnt_' , 'mult_'))
        mult_nodes = [ribA_mult_node , ribB_mult_node , ribA_mult_node_mirror , ribB_mult_node_mirror]
        cmds.setAttr(ribA_mult_node + '.input2' , 2.5)
        cmds.setAttr(ribB_mult_node + '.input2' , -2.5)
        cmds.setAttr(ribA_mult_node_mirror + '.input2' , -3)
        cmds.setAttr(ribB_mult_node_mirror + '.input2' , 3)

        # 制作自动呼吸的预设设置
        # 我们需要的设置有：
        # amplitude（振幅）：用来控制自动呼吸的强度
        # frequency（频率）：用来控制自动呼吸的运动频率
        # offset（偏移）：用来偏移自动呼吸的sin曲线来修改曲线的偏移，达到动画中某一帧吸气或者呼气的效果
        # 自动呼吸的公式  Y = amplitude*sin（frequency * time + offset）

        # 在控制器上添加需要的属性设置
        cmds.addAttr(self.chest_ctrl , longName = 'autoBreathe' , attributeType = 'bool' ,
                     niceName = u'自动呼吸' , minValue = 0 , maxValue = 1 , defaultValue = 0 , keyable = 1)
        cmds.addAttr(self.chest_ctrl , longName = 'amplitude' , attributeType = 'double' ,
                     niceName = u'强度' , minValue = -2 , maxValue = 2 , defaultValue = 0.5 , keyable = 1)
        cmds.addAttr(self.chest_ctrl , longName = 'frequency' , attributeType = 'double' ,
                     niceName = u'频率' , defaultValue = 8 , keyable = 1)
        cmds.addAttr(self.chest_ctrl , longName = 'offset' , attributeType = 'double' ,
                     niceName = u'偏移' , defaultValue = 0 , keyable = 1)

        # 创建一个相乘节点来连接time和frequency的属性
        time_node = 'time1'
        frequency_mult_node = cmds.createNode('multDoubleLinear' , name = 'mult_m_autoBreatheFrequency_001')
        cmds.connectAttr(time_node + '.outTime' , frequency_mult_node + '.input1')
        cmds.connectAttr(self.chest_ctrl + '.amplitude' , frequency_mult_node + '.input2')

        # 创建一个相加节点来连接offset属性
        offset_add_node = cmds.createNode('addDoubleLinear' , name = 'add_m_autoBreatheOffset_001')
        cmds.connectAttr(frequency_mult_node + '.output' , offset_add_node + '.input1')
        cmds.connectAttr(self.chest_ctrl + '.offset' , offset_add_node + '.input2')

        # 创建一个eulerToQuat(欧拉角)节点用来输出正弦曲线
        sin_euler_node = cmds.createNode('eulerToQuat' , name = 'sin_m_autoBreathe_001')
        cmds.connectAttr(offset_add_node + '.output' , sin_euler_node + '.inputRotateX')

        # 创建一个相乘节点来连接输出后的正弦曲线和强度
        amplitude_mult_node = cmds.createNode('multDoubleLinear' , name = 'mult_m_autoBreatheAmplitude_001')
        cmds.connectAttr(sin_euler_node + '.outputQuatX' , amplitude_mult_node + '.input1')
        cmds.connectAttr(self.chest_ctrl + '.amplitude' , amplitude_mult_node + '.input2')

        # 创建一个相乘节点来连接0到1的自动呼吸的开关
        autoBreathe_mult_node = cmds.createNode('multDoubleLinear' , name = 'mult_m_autoBreathe_001')
        cmds.connectAttr(amplitude_mult_node + '.output' , autoBreathe_mult_node + '.input1')
        cmds.connectAttr(self.chest_ctrl + '.autoBreathe' , autoBreathe_mult_node + '.input2')

        # 所有自动呼吸的设置连接完成后最后连接给胸腔控制器上层的connect组
        chest_connect = self.chest_ctrl.replace('ctrl_' , 'connect_')
        cmds.connectAttr(autoBreathe_mult_node + '.output' , chest_connect + '.translateX')

        # 创建一个相加节点来承载最后所有的胸腔呼吸的数值
        autoBreathe_add_node = cmds.createNode('addDoubleLinear' , name = 'add_m_autoBreatheOutput_001')
        cmds.connectAttr(self.chest_ctrl + '.translateX' , autoBreathe_add_node + '.input1')
        cmds.connectAttr(autoBreathe_mult_node + '.output' , autoBreathe_add_node + '.input2')

        # 将这个所有的胸腔呼吸的数值重新连接回ikhandle的twist值
        for node in mult_nodes :
            cmds.connectAttr(autoBreathe_add_node + '.output' , node + '.input1')
            cmds.connectAttr(node + '.output' , node.replace('mult_' , 'ikhandle_') + '.twist')
