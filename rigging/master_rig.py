# coding=utf-8

u"""
这是一个用来编写master最高层级组的基础类

目前已有的功能：

create_master_grp：创建绑定的初始层级组，并隐藏连接对应的属性


"""
from importlib import reload
from . import base_rig
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.nameUtils as nameUtils


class Master_Rig(base_rig.Base_Rig) :


    def __init__(self) :
        super(Master_Rig , self).__init__()
        self.rig_top_grp = 'group'
        if not cmds.objExists(self.rig_top_grp) :
            self.create_master_grp()


    def create_master_grp(self) :
        u'''
        创建绑定的初始层级组，并隐藏连接对应的属性
        '''
        # 根据self.rig_hierarchy_grp 来创建对应的层级组
        for transform in self.rig_hierarchy_grp :
            cmds.createNode('transform' , name = transform)

        # 制作层级关系
        cmds.parent(self.geometry , self.custom , self.control , self.group)

        # 创建RigNode层级下的子层级组并做层级关系
        cmds.parent(self.rigNode_Local , self.rigNode_World , self.rigNode)
        cmds.parent(self.rigNode , self.joint , self.nCloth , self.modular_rig , self.custom)

        # 创建Modle层级下的子层级组并且做层级关系
        cmds.parent(self.low_modle_grp , self.mid_modle_grp , self.high_modle_grp , self.geometry)
        attrs_list = ['.translateX' , '.translateY' , '.translateZ' , '.rotateX' , '.rotateY' , '.rotateZ' , '.scaleX' ,
                      '.scaleY' ,
                      '.scaleZ' , '.visibility' , '.rotateOrder' , '.subCtrlVis']
        # 创建总控制器Character
        controlUtils.Control.create_ctrl(self.character_ctrl , shape = 'circle' , radius = 40 ,
                                         axis = 'X+' ,
                                         pos = None ,
                                         parent = self.control)
        cmds.addAttr(self.character_ctrl , longName = 'rigScale' , niceName = u'绑定缩放' , attributeType = 'double' ,
                     defaultValue = 1 ,
                     keyable = True)
        for attr in ['.scaleX' , '.scaleY' , '.scaleZ'] :
            cmds.connectAttr(self.character_ctrl + '.rigScale' , self.character_ctrl + attr)
            cmds.setAttr(self.character_ctrl + attr , lock = True , keyable = False , channelBox = False)

        # 创建世界控制器
        controlUtils.Control.create_ctrl(self.world_ctrl , shape = 'local' , radius = 35 , axis = 'Z-' ,
                                         pos = None ,
                                         parent = self.character_ctrl.replace('ctrl_' , 'output_'))

        controlUtils.Control.create_ctrl(self.cog_ctrl , shape = 'circle' , radius = 20 , axis = 'X+' ,
                                         pos = None ,
                                         parent = self.world_ctrl.replace('ctrl_' , 'output_'))
        # 创建一个自定义的控制器，用来承载自定义的属性
        controlUtils.Control.create_ctrl(self.custom_ctrl , shape = 'cross' , radius = 3 , axis = 'X+' ,
                                         pos = None ,
                                         parent = self.custom)
        cmds.parentConstraint(self.character_ctrl , self.custom_ctrl , mo = True)
        cmds.scaleConstraint(self.character_ctrl , self.custom_ctrl , mo = True)

        # 创建自定义的控制器属性
        for attr in ['geometryVis' , 'controlsVis' , 'rigNodesVis' , 'jointsVis'] :
            if not cmds.objExists('{}.{}'.format(self.custom_ctrl , attr)) :
                cmds.addAttr(self.custom_ctrl , longName = attr , attributeType = 'bool' , defaultValue = 1 ,
                             keyable = True)

        # 添加精度切换的属性
        if not cmds.objExists('{}.resolution'.format(self.custom_ctrl)) :
            cmds.addAttr(self.custom_ctrl , longName = 'resolution' , attributeType = 'enum' ,
                         enumName = 'low:mid:high' ,
                         keyable = True)
            for idx , res in {0 : 'low' , 1 : 'mid' , 2 : 'high'}.items() :
                cnd_node = 'resolution_{}_conditionNode'.format(res)
                if not cmds.objExists(cnd_node) :
                    cnd_node = cmds.createNode('condition' , name = cnd_node)
                cmds.connectAttr('{}.resolution'.format(self.custom_ctrl) , '{}.firstTerm'.format(cnd_node) ,
                                 force = True)
                cmds.setAttr('{}.secondTerm'.format(cnd_node) , idx)
                cmds.setAttr('{}.colorIfTrueR'.format(cnd_node) , 1)
                cmds.setAttr('{}.colorIfFalseR'.format(cnd_node) , 0)
                cmds.connectAttr('{}.outColorR'.format(cnd_node) , 'grp_m_{}_modle_001.visibility'.format(res) ,
                                 force = True)

        # 添加模型显示方式的属性
        if not cmds.objExists('{}.geometryDisplayType'.format(self.character_ctrl)) :
            cmds.addAttr(self.custom_ctrl , longName = 'geometryDisplayType' , attributeType = 'enum' ,
                         enumName = 'Normal:Template:Reference' ,
                         keyable = True)

        # 连接各个组的显示属性
        custom_ctrl_attrs = ['.geometryVis' , '.controlsVis' , '.rigNodesVis' , '.jointsVis']
        hierarchy_grp = [self.geometry , self.control , self.rigNode , self.joint]
        for attrs , grp in zip(custom_ctrl_attrs , hierarchy_grp) :
            cmds.connectAttr(self.custom_ctrl + '{}'.format(attrs) , '{}.visibility'.format(grp))
        # 连接模型的可编辑属性
        cmds.setAttr(self.geometry + '.overrideDisplayType' , 2)
        cmds.connectAttr('{}.geometryDisplayType'.format(self.custom_ctrl) , self.geometry + '.overrideEnabled' ,
                         force = True)

        # 显示和隐藏属性
        for attr in attrs_list :
            cmds.setAttr(self.custom_ctrl + attr , lock = True , keyable = False , channelBox = False)

        # 创建用于空间切换的组
        for ctrl in self.rig_ctrl :
            ctrl_obj = nameUtils.Name(name = ctrl)
            space_grp = cmds.createNode('transform' , name = 'grp_m_{}Space_001'.format(ctrl_obj.description))
            cmds.parent(space_grp , ctrl)
            cmds.setAttr(space_grp + '.visibility' , 0)
