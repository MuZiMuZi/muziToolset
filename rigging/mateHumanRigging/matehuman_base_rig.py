# coding=utf-8

u"""
这是一个用来编写mateHuman自动绑定系统的基础类，之后的绑定都会在这个类的基础上逐级继承下去

目前已有的功能：

get_description_bp_joints：根据给定关节模块的名称来获取对应的模块组关节的名称

default_grp：创建绑定的初始层级组，并隐藏连接对应的属性

setup: 绑定生成的预设步骤，导入对应的模型和关节结构

make： 根据给定的bp_joints关节的名称来创建对应的模块组

"""

import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.matehumanUtils as matehumanUtils
import pymel.core as pm



class Base_Rig(object) :



    # # 规定一下命名规范
    # drv关节链: root_drv , spine_01_drv, thigh_r_drv

    # fk关节链:'fkjnt' + drv关节链
    # fk控制器：'fkctrl_边_模块_编号'
    #fk次级控制器：'fkctrlSub_边_模块_编号'

    # ik关节链：'ikjnt' + drv关节链
    # ik控制器：'ikctrl_边_模块_编号'
    # ik次级控制器：'ikctrlSub_边_模块_编号'



    def __init__(self) :
        super(Base_Rig , self).__init__()
        # # 定义mateHuman的关节层级
        # self.mateHuman_joint_set()
        self.side = None
        if self.side == 'l' :
            self.side_value = 1
        elif self.side == 'r' :
            self.side_value = -1

        # 定义世界的层级组架构
        self.character_ctrl = 'ctrl_m_character_001'
        self.world_ctrl = 'ctrl_m_world_001'
        self.cog_ctrl = 'ctrl_m_cog_001'
        self.custom_ctrl = 'ctrl_m_custom_001'

        self.group = 'group'
        self.geometry = 'geometry'
        self.control = 'control'
        self.custom = 'custom'

        self.rigNode = 'rigNode'
        self.joint = 'joint'
        self.rigNode_Local = 'rigNode_Local'
        self.rigNode_World = 'rigNode_World'
        self.nCloth = 'nCloth'
        self.description_rig = 'description_rig'

        self.low_modle_grp = 'grp_m_low_modle_001'
        self.mid_modle_grp = 'grp_m_mid_modle_001'
        self.high_modle_grp = 'grp_m_high_modle_001'

        self.rig_ctrl = [self.character_ctrl , self.world_ctrl , self.cog_ctrl , self.custom_ctrl]
        self.rig_hierarchy_grp = [self.group , self.geometry , self.control , self.custom , self.rigNode , self.joint ,
                                  self.rigNode_Local , self.rigNode_World , self.nCloth ,
                                  self.description_rig , self.low_modle_grp , self.mid_modle_grp , self.high_modle_grp]

        # 定义绑定模块

        self.arm_rig = 'arm_rig'
        self.hand_rig = 'hand_rig'
        self.leg_rig = 'leg_rig'
        self.foot_rig = 'foot_rig'
        self.neck_rig = 'neck_rig'
        self.spine_rig = 'spine_rig'
        self.chest_rig = 'chest_rig'
        self.description_rig_list = [self.arm_rig , self.hand_rig , self.leg_rig , self.foot_rig , self.neck_rig ,
                                     self.spine_rig , self.chest_rig]

        # # # 定义绑定模块的bp定位关节
        # self.arm_bp_joints = self.get_description_mateHuman_joints(self.arm_rig)
        # # self.leg_bp_joints = self.get_description_bp_joints(self.leg_rig)
        # # self.neck_bp_joints = self.get_description_bp_joints(self.neck_rig)
        # # self.spine_bp_joints = self.get_description_bp_joints(self.spine_rig)
        # # self.foot_bp_joints = self.get_description_bp_joints(self.foot_rig)

        # 设置matehuman导入maya的轴向
        cmds.setAttr('root_drv' + '.rotateX' , -90)
        cmds.setAttr('headRig_grp' + '.rotateX' , -90)





    def make(self , joint) :
        u"""
        根据给定的bp_joints关节的名称来创建对应的模块组
        mateHuman_description:给定的对应的模块名称
        """
        main_obj = self.mateHuman_decompose(joint)
        main_obj.name = 'RigModule_' + joint
        self.control_grp = cmds.group(name = main_obj.name.replace('RigModule_' , 'Ctrl_') , em = True ,
                                      parent = self.cog_ctrl.replace('ctrl_' , 'output_'))
        self.jnt_grp = cmds.group(name = main_obj.name.replace('RigModule_' , 'Jnt_') , em = True ,
                                  parent = self.joint)
        self.rigNodes_Local_grp = cmds.group(name = main_obj.name.replace('RigModule_' , 'RigNodesLocal_') , em = True ,
                                             parent = self.rigNode_Local)
        self.rigNodes_World_grp = cmds.group(name = main_obj.name.replace('RigModule_' , 'RigNodesWorld_') , em = True ,
                                             parent = self.rigNode_World)
        self.space_grp = cmds.group(name = main_obj.name.replace('RigModule_' , 'Space_') , em = True ,
                                    parent = self.control_grp)
        # 设置组的可见性
        cmds.setAttr(self.space_grp + '.visibility' , 0)



    @staticmethod
    def add_spaceSwitch(object , space_list) :
        u"""
        添加空间切换
        :param object: 需要添加空间切换的对象
        :param space_list(list): 添加空间切换的空间
        :return:
        """

        # 在对象上添加空间切换的属性控制
        cmds.addAttr(object , longName = 'spaceSwitch' , niceName = u'空间切换' , attributeType = 'enum' ,
                     en = ":".join(space_list) , keyable = True)

        for space_name in space_list :
            # 创建用于空间切换的定位器
            object_obj = nameUtils.Name(name = object)
            object_obj.type = 'loc'
            object_obj.description = object_obj.description + 'Space' + space_name
            loc_node = cmds.spaceLocator(name = object_obj.name)[0]
            # 创建定位器上层的组并吸附到添加空间切换的对象的位置
            loc_zero = cmds.createNode('transform' , name = loc_node.replace('loc_' , 'zero_'))
            cmds.parent(loc_node , loc_zero)
            cmds.matchTransform(loc_zero , object , position = True , rotation = True , scale = True)
            # 定位器对添加空间切换的对象上层的组做父子约束，并且整理层级
            cmds.parentConstraint(loc_node , object.replace('ctrl_' , 'space_') , mo = False)
            cmds.parent(loc_zero , 'grp_m_{}Space_001'.format(space_name))
            # 创建用于空间切换的判断节点
            space_cond_node = cmds.createNode('condition' , name = loc_node.replace('loc_' , 'cond_'))
            cmds.setAttr(space_cond_node + '.colorIfTrueR' , 1)
            cmds.setAttr(space_cond_node + '.colorIfFalseR' , 0)
            cmds.connectAttr(object + '.spaceSwitch' , space_cond_node + '.firstTerm')
            cmds.setAttr(space_cond_node + '.secondTerm' , space_list.index(space_name))
            # 连接约束节点
            constraint_node = object.replace('ctrl_' , 'space_') + '_parentConstraint1'
            cmds.connectAttr(space_cond_node + '.outColorR' ,
                             constraint_node + '.{}W{}'.format(loc_node , space_list.index(space_name)))
