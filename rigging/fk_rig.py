# coding=utf-8

u"""
这是一个用来编写FK控制系统绑定的类，之后的绑定都会在这个类的基础上逐级继承下去

继承了base_rig

目前已有的功能：

fk_chain_rig：创建FK链的控制器绑定



"""
from importlib import reload
import maya.cmds as cmds
import muziToolset.core.controlUtils as controlUtils
import muziToolset.core.hierarchyUtils as hierarchyUtils
import muziToolset.core.jointUtils as jointUtils
import muziToolset.core.nameUtils as nameUtils
import muziToolset.core.pipelineUtils as pipelineUtils


reload(pipelineUtils)
reload(jointUtils)
import base_rig


class FK_Rig(base_rig.Base_Rig) :


    def __init__(self , bp_joints = None , joint_parent = None , control_parent = None) :
        super(FK_Rig , self).__init__()
        self.bp_joints = bp_joints
        self.joint_parent = joint_parent
        self.control_parent = control_parent


    def fk_chain_rig(self , fk_chain , control_parent) :
        u"""
        创建fk链的控制器绑定
        Args:
            control_parent(str): 控制器组的父层级

        Returns: fk_ctrl_grp ：fk控制器的最顶层

        """
        cmds.setAttr(fk_chain[0] + '.visibility' , 0)
        # 创建控制器
        parent = None
        for jnt in fk_chain :
            jnt_name = nameUtils.Name(name = jnt)
            ctrl_name = jnt.replace('jnt_' , 'ctrl_')
            ctrl = controlUtils.Control.create_ctrl(ctrl_name , shape = 'circle' , radius = 8 , axis = 'Y+' ,
                                                    pos = jnt ,
                                                    parent = None)
            zero = jnt.replace('jnt_' , 'zero_')
            output = jnt.replace('jnt_' , 'output_')
            cmds.parentConstraint(output , jnt , maintainOffset = True)
            cmds.scaleConstraint(output , jnt , maintainOffset = True)
            if parent :
                cmds.parent(zero , parent)
            parent = output
        fk_ctrl_grp = cmds.createNode('transform' , name = fk_chain[0].replace('jnt' , 'grp'))
        fk_chain_zero = fk_chain[0].replace('jnt' , 'zero')
        cmds.parent(fk_chain_zero , fk_ctrl_grp)
        if control_parent :
            hierarchyUtils.Hierarchy.parent(child_node = fk_ctrl_grp , parent_node = control_parent)
