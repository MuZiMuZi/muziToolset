from importlib import reload

import maya.cmds as cmds

from . import chain
from ....core import controlUtils , vectorUtils


reload (vectorUtils)
reload (chain)


class ChainFK (chain.Chain) :
    rigType = 'ChainFK'
    def __init__ (self , side , name , jnt_number , direction = None , length = 10 , jnt_parent = None ,
                  ctrl_parent = None) :
        u"""
        用来创建fk关节链条的绑定
        length(int)：关节的总长度
        direction（list）:从根节点到顶部节点的方向例如[1,0,0]或者[0,1,0]
        """
        super ().__init__ (side , name , jnt_number , length , jnt_parent , ctrl_parent)
        self.interval = length / (self.jnt_number - 1)
        self.direction = list (vectorUtils.Vector (direction).mult_interval (self.interval))

        self.shape = 'square'
        self.axis = vectorUtils.Vector (direction).axis
        self.radius = 2


    def create_ctrl (self) :
        # 判断场景里是否已经存在对应的控制器，重建的情况
        if cmds.objExists (self.ctrl_grp) :
            # 删除过去的控制器层级组后，并重新创建控制器
            cmds.delete (self.ctrl_grp)
            self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.ctrl_parent)
        else :
            self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.ctrl_parent)

        self.set_shape (self.shape)

        parent = self.ctrl_grp
        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            self.ctrl = controlUtils.Control.create_ctrl (ctrl , shape = self.shape , radius = self.radius ,
                                                          axis = 'Z-' , pos = jnt , parent = parent)
            # 指定关节的父层级为上一轮创建出来的控制器层级组
            parent = ctrl.replace ('ctrl' , 'output')


    def add_constraint (self) :
        for jnt_number , jnt in enumerate (self.jnt_list) :
            cmds.parentConstraint (self.ctrl_list [jnt_number] , jnt)
            cmds.scaleConstraint (self.ctrl_list [jnt_number] , jnt)


# 示例
# import muziToolset.bind.module.chain.chainFK as chainFK
# from importlib import reload
#
#
# reload (chainFK)
#
# ch = chainFK.ChainFK (side = 'r' , name = '' , jnt_number = 4 , direction = [-1 , 0 , 0] , length = 10 ,
#                       jnt_parent = None ,
#                       ctrl_parent = None)
#
# ch.build_setup ()
