from importlib import reload

import maya.cmds as cmds

from . import chain
from ..base import base
from ....core import controlUtils , pipelineUtils


reload (base)
reload (chain)
reload (pipelineUtils)


class ChainEP (chain.Chain) :
    rtype = 'ChainEP'


    def __init__ (self , side , name , jnt_number , ctrl_number , curve , jnt_parent = None ,
                  ctrl_parent = None) :

        u'''
        给定一根曲线，根据曲线的长度来创建关节和控制器
        用来创建类似绳子物体的绑定
        需要注意的点有，生成的关节数量需要大于生成的控制器数量
        jnt_number：生成的关节数量
        ctrl_number：生成的控制器数量
        crv_node：需要创建控制器与关节的曲线
        '''
        self.ctrl_number = ctrl_number
        super ().__init__ (side , name , jnt_number , jnt_parent , ctrl_parent)

        self.curve = curve
        self.radius = 3
        self.set_shape ('ball')

        # 根据给定的控制器数量，获取控制对应的百分比信息
        if self.ctrl_number < 2 :
            raise ValueError (u"请有足够的控制控制器数量")
        if self.ctrl_number > self.jnt_number :
            raise ValueError (u"控制器的数量请小于关节的数量")

        self.guide_curve = None
        self.cvs = list ()

        # # 曲线的总长度为1，给定需要平分的点数量，返回每个点的位置信息
        percents = pipelineUtils.Pipeline.get_percentages (self.ctrl_number)
        for p in percents :
            integer = int (round (p * (self.jnt_number - 1)))
            self.cvs.append (integer)


    def create_namespace (self) :
        #  根据给定的边，名称和jnt_number生成列表来存储创建的名称
        self._setup_list ()

        # 根据给定的边，名称和jnt_number生成列表来存储关节组创建的名称
        for i in range (self.jnt_number) :
            self.bpjnt_list.append ('bpjnt_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.jnt_list.append ('jnt_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.zero_list.append ('zero_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.driven_list.append ('driven_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.connect_list.append ('connect_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.offset_list.append ('offset_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.ctrl_list.append ('ctrl_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.subctrl_list.append ('ctrl_{}_{}{}Sub_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.output_list.append ('output_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))


    def create_bpjnt (self) :
        """
        创建定位的bp关节
        """
        # 设置bpjnt创建出来的位置放置在top_bpjnt_grp的层级下
        self.bpjnt_parent = self.top_bpjnt_grp
        bpjnt_list = pipelineUtils.Pipeline.create_joints_on_curve (self.curve , self.jnt_number)
        for jnt_number , bpjnt in enumerate (bpjnt_list) :
            bpjnt = cmds.rename (bpjnt , self.bpjnt_list [jnt_number])
            cmds.parent (bpjnt , self.bpjnt_parent)
            # 指定关节的父层级为上一轮创建出来的关节
            self.bpjnt_parent = bpjnt


    def create_joint (self) :
        # 根据bp关节创建新的关节
        for bpjnt , jnt in zip (self.bpjnt_list , self.jnt_list) :
            jnt = cmds.createNode ('joint' , name = jnt , parent = self.jnt_parent)
            cmds.matchTransform (jnt , bpjnt)
            # 指定关节的父层级为上一轮创建出来的关节
            self.jnt_parent = jnt
        # 隐藏bp的定位关节
        cmds.setAttr (self.bpjnt_list [0] + '.visibility' , 0)


    def create_ctrl (self) :
        self.set_shape (self.shape)
        # 创建整体的控制器层级组
        self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.ctrl_parent)

        # 使用列表存储控制器
        self.ctrl_instances = []

        for index in self.cvs :
            ctrl_instance = controlUtils.Control.create_ctrl (
                self.ctrl_list [index] , shape = self.shape , radius = self.radius ,
                axis = 'X+' , pos = self.jnt_list [index] , parent = self.ctrl_parent
            )
            # 将控制器实例添加到列表中
            self.ctrl_instances.append (ctrl_instance)


    def add_constraint (self) :
        '''
        在关节和控制器之间添加平滑衰减约束
        '''
        for cv_index in self.cvs :
            # 开头的关节进行约束
            if cv_index == 0 :
                cmds.pointConstraint (self.ctrl_list [cv_index] , self.jnt_list [cv_index] , mo = 1)
                cmds.orientConstraint (self.ctrl_list [cv_index] , self.jnt_list [cv_index] , mo = 1)

            # 结尾的关节进行约束
            elif cv_index == self.cvs [-1] :
                cmds.pointConstraint (self.ctrl_list [cv_index] , self.jnt_list [-1] , mo = 1)
                cmds.orientConstraint (self.ctrl_list [cv_index] , self.jnt_list [-1])

            # 中间的关节进行约束
            else :
                for jnt_index in range (self.cvs.index (cv_index) , self.cvs.index (cv_index) + 1) :
                    head = cv_index
                    tail = self.cvs [self.cvs.index (cv_index) + 1]
                    for jnt in range (head , tail + 1) :
                        gap = 1.00 / (tail - head)

                        # 设置前后两端的控制器影响关节的权重值
                        cmds.pointConstraint (self.ctrl_list [head] , self.jnt_list [jnt] ,
                                              w = 1 - ((jnt - head) * gap) , mo = 1)
                        cmds.pointConstraint (self.ctrl_list [tail] , self.jnt_list [jnt] ,
                                              w = (jnt - head) * gap , mo = 1)
                        cmds.orientConstraint (self.ctrl_list [head] , self.jnt_list [jnt] ,
                                               w = 1 - ((jnt - head) * gap) , mo = 1)
                        cmds.orientConstraint (self.ctrl_list [tail] , self.jnt_list [jnt] ,
                                               w = (jnt - head) * gap , mo = 1)


if __name__ == '__main__' :
    def x () :
        custom = chainEP.ChainEP (side = 'l' , name = 'zz' , jnt_number = 20 , ctrl_number = 20 , curve = 'curve1' ,
                                  jnt_parent = None , ctrl_parent = None)
        custom.build_setup ()


    def y () :
        custom = chainEP.ChainEP (side = 'l' , name = 'zz' , jnt_number = 20 , ctrl_number = 20 , curve = 'curve1' ,
                                  jnt_parent = None , ctrl_parent = None)
        custom.build_rig ()
