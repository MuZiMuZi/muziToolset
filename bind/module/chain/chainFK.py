from importlib import reload

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
        u"""
        根据绑定关节来创建对应的控制器
        """
        # 判断场景里是否已经存在对应的控制器，重建的情况
        self.set_shape (self.shape)
        # 创建整体的控制器层级组
        # 判断场景里是否已经存在对应的控制器，重建的情况
        self._create_ctrl_grp ()

        # 对控制器组和关节组进行循环，创建对应关节的控制器以及吸附到对应的位置
        # 使用函数进行创建和吸附控制器
        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            self.ctrl = self._create_and_attach_controller (ctrl , jnt)


    def _create_and_attach_controller (self , ctrl , jnt) :
        """
        根据给定的控制器和关节创建控制器，吸附到对应位置，并根据边的情况进行调整
        """
        # 使用控制器工具类创建控制器
        parent = self.ctrl_grp
        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            self.ctrl = controlUtils.Control.create_ctrl (ctrl , shape = self.shape , radius = self.radius ,
                                                          axis = 'Z+' , pos = jnt , parent = parent)
            # 指定关节的父层级为上一轮创建出来的控制器层级组
            parent = ctrl.replace ('ctrl' , 'output')


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
