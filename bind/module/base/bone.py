# coding=utf-8
import logging
from importlib import reload

import maya.cmds as cmds

from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils
from importlib import reload
import os


reload (hierarchyUtils)
reload (pipelineUtils)


class Bone (object) :
    """
    构架思路：创建定位的bp关节，然后生成对应的绑定
    创建绑定的步骤:
    build_setup(): 创建bp的定位关节,生成准备
        1.create_namespace(): 创建名称规范整理
        2.create_bpjnt() :根据名称规范，创建定位的bp关节
    build_rig(): 根据定位的bp关节创建绑定系统
        1.create_namespace(): 创建名称规范整理
        2.create_joint() :根据名称规范和定位的bp关节创建蒙皮关节
        3.create_ctrl() :根据名称规范和蒙皮关节创建控制器
        4.add_constraint() :控制器和蒙皮关节创建约束或者连接控制

    """


    def __init__ (self , side , name , joint_number , joint_parent = None , control_parent = None) :
        """
        根据给定的变量创建关节和控制器

        :param side: 关节的边
        :param name: 关节的模块名称
        :param joint_number: 关节的数量
        :param joint_parent: 生成的关节的父层级
        :param control_parent: 生成的控制器的父层级
        """
        # 创建层级结构
        main_group = 'grp_m_group_001'
        if cmds.objExists(main_group):
            pass
        else:
            hierarchyUtils.Hierarchy.create_rig_grp ()
        self._side = side
        self.joint_number = joint_number

        # 设置关节的父层级和控制器的父层级
        self.joint_parent = joint_parent
        self.control_parent = control_parent
        if not self.joint_parent :
            self.joint_parent = 'grp_m_jnt_001'
        if not self.control_parent :
            self.control_parent = 'grp_m_control_001'
        self.bpjnt_grp = 'grp_m_bpjnt_001'
        # 生成的绑定类型
        self._rtype = ''
        self._name = name
        self.shape = 'circle'
        self.radius = 5

        # 根据给定的边，名称和joint_number生成列表来存储创建的名称
        self.bpjnt_list = list ()
        self.jnt_list = list ()
        self.zero_list = list ()
        self.driven_list = list ()
        self.connect_list = list ()
        self.offset_list = list ()
        self.ctrl_list = list ()
        self.subctrl_list = list ()
        self.output_list = list ()

        # 判断边为'l'还是'r'
        if side == 'l' :
            self.side_value = 1
        elif side == 'r' :
            self.side_value = -1
        else :
            self.side_value = 0

        # 创建一个logger日志用来排查错误
        # 创建logger日志来排查错误
        self.logger_name = '{}_logger'.format (self.__class__.__name__)
        self.file_name = os.path.abspath (__file__ + "/../../../../log/bind.log")

        pipelineUtils.Pipeline.create_logging (logger_name = self.logger_name , file_name = self.file_name ,
                                               formatter = '%(asctime)s -%(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger (self.logger_name)
        self.logger.setLevel (logging.DEBUG)

        # 创建名称规范整理
        self.create_namespace ()


    @property
    def name (self) :
        return self._name


    @property
    def side (self) :
        return self._side


    @property
    def type (self) :
        return self._rtype


    @property
    def scale (self) :
        return self._scale


    def set_shape (self , shape) :
        u'''
        设置控制器形状
        '''
        self.shape = shape


    def create_namespace (self) :
        u"""
        创建名称规范整理
        """
        for i in range (self.joint_number) :
            self.bpjnt_list.append ('bpjnt_{}_{}{}_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
            self.jnt_list.append ('jnt_{}_{}{}_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
            self.zero_list.append ('zero_{}_{}{}_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
            self.driven_list.append ('driven_{}_{}{}_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
            self.connect_list.append ('connect_{}_{}{}_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
            self.offset_list.append ('offset_{}_{}{}_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
            self.ctrl_list.append ('ctrl_{}_{}{}_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
            self.subctrl_list.append ('ctrl_{}_{}{}Sub_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
            self.output_list.append ('output_{}_{}{}_{:03d}'.format (self._side , self._name , self._rtype , i + 1))
        self.ctrl_grp = ('grp_{}_{}{}_001'.format (self._side , self._name , self._rtype))


    def create_bpjnt (self) :
        """
        根据名称规范，创建定位的bp关节
        """
        for bpjnt in self.bpjnt_list :
            # 判断是否已经生成过定位关节，如果没有生成过定位关节的话则生成定位关节
            if cmds.objExists(bpjnt):
                cmds.delete(bpjnt)
            else:
                self.bpjnt = cmds.createNode ('joint' , name = bpjnt , parent = self.bpjnt_grp)
                # 给bp定位关节设置颜色方便识别
                cmds.setAttr (self.bpjnt + '.overrideEnabled' , 1)
                cmds.setAttr (self.bpjnt + '.overrideColor' , 13)
                # 将bp关节添加到选择集里方便进行选择
                pipelineUtils.Pipeline.create_set (self.bpjnt ,
                                                   set_name = '{}_{}{}_bpjnt_set'.format (self._side , self._name ,
                                                                                          self._rtype) ,
                                                   set_parent = 'bpjnt_set')
        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.bpjnt_list)


    def hide_bpjnt (self) :
        """
        定位完成后隐藏bpjnt关节
        """
        # 选择bp选择集
        cmds.select (clear = True)
        bpjnts_set = cmds.select ('bpjnt_set')
        # 选择bp选择集下所有子对象关节
        bpjnts_list = cmds.ls (sl = True , type = 'joint')
        # 对bpjnt关节列表做循环，设置他们的可见性
        for bpjnt in bpjnts_list :
            cmds.setAttr (bpjnt + '.visibility' , 0)


    def create_joint (self) :
        '''
        根据定位的bp关节创建关节
        '''
        # 隐藏bp的定位关节
        self.hide_bpjnt ()

        # 根据bp关节创建新的关节,需要做生成关节的准备，断掉bp关节上的所有属性链接
        for bpjnt in self.bpjnt_list :
            for attr in ['.translate' , '.rotate' , '.scale'] :
                # 判断bp关节上有没有连接的属性，如果有的话则断掉
                plug = cmds.listConnections (bpjnt + attr , s = True , d = False , p = True)
                if plug :
                    cmds.disconnectAttr (plug [0] , bpjnt + attr)
        # 判断场景里是否已经存在对应的关节，重建的情况
        for jnt in self.jnt_list:
            if cmds.objExists (jnt) :
                # 删除过去的关节后，并重新创建关节
                cmds.delete (jnt)
        else :
            pass
        for bpjnt , jnt in zip (self.bpjnt_list , self.jnt_list) :
            # 场景里没有存在对应的关节，第一次创建绑定的情况
            jnt = cmds.createNode ('joint' , name = jnt , parent = self.joint_parent)
            # 将蒙皮关节添加到选择集里方便进行选择
            pipelineUtils.Pipeline.create_set (jnt ,
                                               set_name = '{}_{}{}_jnt_set'.format (self._side , self._name ,
                                                                                    self._rtype) ,
                                               set_parent = 'jnt_set')
            cmds.matchTransform (jnt , bpjnt)


    def create_ctrl (self) :
        u"""
        创建控制器
        """
        self.set_shape (self.shape)
        # 创建整体的控制器层级组
        # 判断场景里是否已经存在对应的控制器，重建的情况
        if cmds.objExists (self.ctrl_grp) :
            # 删除过去的控制器层级组后，并重新创建控制器
            cmds.delete (self.ctrl_grp)
            self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.control_parent)
        else :
            self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.control_parent)

        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            self.ctrl = controlUtils.Control.create_ctrl (ctrl , shape = self.shape ,
                                                          radius = self.radius ,
                                                          axis = 'X+' , pos = jnt ,
                                                          parent = self.ctrl_grp)
            # 判断所创建的控制器的边，如果边为_r_的话，offset组需要修改镜像
            if self.side == 'r' :
                cmds.setAttr (ctrl.replace ('ctrl' , 'offset') + '.scaleX' , -1)


    def add_constraint (self) :
        '''
        添加约束
        '''
        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            pipelineUtils.Pipeline.create_constraint (ctrl.replace (' ctrl' , 'output') , jnt ,
                                                      point_value = True ,
                                                      orient_value = True , scale_value =
                                                      True ,
                                                      mo_value = True)


    def build_setup (self) :
        """
        创建bp的定位关节,生成准备
        """
        self.create_bpjnt ()


    def build_rig (self) :
        """
        创建绑定系统
        """
        self.create_joint ()
        self.create_ctrl ()
        self.add_constraint ()


    def delete_rig (self) :
        """
        删除已经创建好的绑定系统
        """
        # 删除已经创建好的关节
        for jnt in self.jnt_list :
            if cmds.objExists (jnt) :
                # 删除过去的关节后，并重新创建关节
                cmds.delete (jnt)
        else :
            pass

        if cmds.objExists (self.ctrl_grp) :
            cmds.delete (self.ctrl_grp)
        else :
            pass
