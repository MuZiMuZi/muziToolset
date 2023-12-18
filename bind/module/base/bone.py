# coding=utf-8
# 导入所有需要的模块

from __future__ import unicode_literals , print_function


try :
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance

except ImportError :
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtWidgets import *
    from PySide import __version__
    from shiboken import wrapInstance
import logging
import os

import maya.cmds as cmds

from ... import config
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils


class RigItem (QListWidgetItem) :
    """
    定义了一个名为 RigItem 的类，它是 QtWidgets.QListWidgetItem 的子类，用于表示一个骨骼组件
    """


    # 表示一个骨骼组件的列表项，初始化了列表项的一些属性，包括名称、图标
    def __init__ (self , name) :
        """
        表示一个骨骼组件的列表项，初始化了列表项的一些属性，包括名称、图标

        :param name(str):根据给定的模块名称初始化属性，包括名称、图标
        """
        super (RigItem , self).__init__ ()

        # 初始化ui的文件
        self.base_ui = None
        self.extra_ui = None

        # 根据给定的名称初始化图标的名称
        self.icon = '{}.png'.format (name)
        # 获取config配置文件里的ui路径来设置图标
        icon = QIcon ()
        path = os.path.join (config.icon_dir , self.icon)
        icon.addFile (path)
        self.setIcon (icon)

        # 绑定属性的小部件
        self.base_widget = None
        self.extra_widget = None

        # 绑定的组件对象
        self._obj = None


    # 初始化作为QWidget对象的base_widget属性，用于设置绑定组件的基础属性，比如（边，名称，关节数量，关节的父物体，控制器的父物体）等属性
    # （side,name,jnt_number,jnt_parent,control_parent）
    def create_base_widget (self) :
        """
        初始化作为QWidget对象的base_widget属性，用于设置绑定组件的边，名称，关节数量，关节的父物体，控制器的父物体等属性
        side,name,jnt_number,jnt_parent,control_parent
        """
        pass


    # 初始化作为QWidget对象的extra_widget属性,用于设置绑定组件的特殊属性，比如(长度，朝向，拉伸，IK启用，FK启用,twist启用)等属性
    # （Length, orientation, stretch, IK enabled, FK enabled, twist enabled）

    def create_extra_widget (self) :
        """
        #初始化作为QWidget对象的extra_widget属性,用于设置绑定组件的特殊属性，比如(长度，朝向，拉伸，IK启用，FK启用,twist启用)等属性
        #（Length, orientation, stretch, IK enabled, FK enabled, twist enabled）
        """
        pass


    # 分析base_widget中的输入并将其作为参数返回
    def parse_base_widget (self) :
        """
        分析base_widget中的输入并将其作为参数返回
        """
        pass


    # 分析extra_widget中的输入并将其作为参数返回
    def parse_extra_widget (self) :
        """
        #分析extra_widget中的输入并将其作为参数返回
        """
        pass


    # 根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备
    def build_setup (self , *args , **kwargs) :
        """
        根据base_widget和extra_widget返回的参数创建bp的定位关节,生成准备
        """
        pass


    # 根据base_widget和extra_widget返回的参数，创建绑定系统
    def build_rig (self , *args , **kwargs) :
        """
        根据base_widget和extra_widget返回的参数，创建绑定系统
        """


    # 根据base_widget和extra_widget返回的参数，删除绑定系统
    def delete_rig (self) :
        """
        根据base_widget和extra_widget返回的参数，删除绑定系统
        """
        pass


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

        :param side(str): 关节的边
        :param name(str): 关节的模块名称
        :param joint_number(int): 关节的数量
        :param joint_parent(str): 生成的关节的父层级
        :param control_parent(str): 生成的控制器的父层级
        """
        # 创建层级结构，当场景里不存在最高级层级组的时候，自动创建最高级层级组
        main_group = 'grp_m_group_001'
        if cmds.objExists (main_group) :
            self.top_main_group = 'grp_m_group_001'
            self.top_bpjnt_grp = 'grp_m_bpjnt_001'
            self.top_ctrl_grp = 'grp_m_control_001'
            self.top_jnt_grp = 'grp_m_jnt_001'
            self.top_mesh_grp = 'grp_m_mesh_001'
            self.top_node_grp = 'grp_m_node_001'
        else :
            self.top_bpjnt_grp , self.top_ctrl_grp , self.top_jnt_grp , self.top_mesh_grp , self.top_node_grp , self.top_main_group = hierarchyUtils.Hierarchy.create_rig_grp ()
        # 初始化组件的边和关节数量
        self.side = side
        self.name = name
        self.joint_number = joint_number

        # 设置关节的父层级和控制器的父层级
        self.joint_parent = joint_parent
        self.control_parent = control_parent
        if not self.joint_parent :
            self.joint_parent = self.top_jnt_grp
        if not self.control_parent :
            self.control_parent = self.top_ctrl_grp
        self.top_bpjnt_grp = 'grp_m_bpjnt_001'

        cmds.setAttr (self.top_bpjnt_grp + '.visibility' , 0)
        # 生成的绑定类型
        self.rtype = 'bone'
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




    # 设置控制器形状
    def set_shape (self , shape) :
        u'''
        设置控制器形状
        '''
        self.shape = shape


    # 根据给定的side，name等属性，创建名称进行规范整理
    def create_namespace (self) :
        u"""
        创建名称进行规范整理
        """
        for i in range (self.joint_number) :
            self.bpjnt_list.append ('bpjnt_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.jnt_list.append ('jnt_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.zero_list.append ('zero_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.driven_list.append ('driven_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.connect_list.append ('connect_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.offset_list.append ('offset_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.ctrl_list.append ('ctrl_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.subctrl_list.append ('ctrl_{}_{}{}Sub_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
            self.output_list.append ('output_{}_{}{}_{:03d}'.format (self.side , self.name , self.rtype , i + 1))
        self.ctrl_grp = ('grp_{}_{}{}_001'.format (self.side , self.name , self.rtype))


    # 根据给定的名称规范，创建定位的bp关节
    def create_bpjnt (self) :
        """
        根据名称规范，创建定位的bp关节
        """
        for bpjnt in self.bpjnt_list :
            # 判断是否已经生成过定位关节，如果没有生成过定位关节的话则生成定位关节
            if cmds.objExists (bpjnt) :
                cmds.delete (bpjnt)
            else :
                self.bpjnt = cmds.createNode ('joint' , name = bpjnt , parent = self.bpjnt_grp)
                # 给bp定位关节设置颜色方便识别
                cmds.setAttr (self.bpjnt + '.overrideEnabled' , 1)
                cmds.setAttr (self.bpjnt + '.overrideColor' , 13)
                # 将bp关节添加到选择集里方便进行选择
                pipelineUtils.Pipeline.create_set (self.bpjnt ,
                                                   set_name = '{}_{}{}_bpjnt_set'.format (self.side , self.name ,
                                                                                          self.rtype) ,
                                                   set_parent = 'bpjnt_set')
        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.bpjnt_list)


    # 设置bp关节的可见性，用于切换状态，当绑定系统创建完成的时候设置bp关节为隐藏状态，当绑定系统删除的时候则设置bp关节为显示状态
    def set_bpjnt_vis (self , vis_bool) :
        """
        设置bp关节的可见性，用于切换状态，当绑定系统创建完成的时候设置bp关节为隐藏状态，当绑定系统删除的时候则设置bp关节为显示状态
        vis_bool(bool):bp关节的可见性,0为不可见，1为可见
        """
        # 选择bp选择集
        cmds.select (clear = True)
        if cmds.objExists ('bpjnt_set') :
            bpjnts_set = cmds.select ('bpjnt_set')
            # 选择bp选择集下所有子对象关节
            bpjnts_list = cmds.ls (sl = True , type = 'joint')
            # 对bpjnt关节列表做循环，设置他们的可见性
            for bpjnt in bpjnts_list :
                cmds.setAttr (bpjnt + '.visibility' , vis_bool)


    # 根据定位的bp关节创建绑定关节
    def create_joint (self) :
        '''
        根据定位的bp关节创建绑定关节
        '''
        # 隐藏bp的定位关节
        self.set_bpjnt_vis (vis_bool = 0)

        # 根据bp关节创建新的关节,需要做生成关节的准备，断掉bp关节上的所有属性链接
        for bpjnt in self.bpjnt_list :
            for attr in ['.translate' , '.rotate' , '.scale'] :
                # 判断bp关节上有没有连接的属性，如果有的话则断掉
                plug = cmds.listConnections (bpjnt + attr , s = True , d = False , p = True)
                if plug :
                    cmds.disconnectAttr (plug [0] , bpjnt + attr)
        # 判断场景里是否已经存在对应的关节，重建的情况
        for jnt in self.jnt_list :
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
                                               set_name = '{}_{}{}_jnt_set'.format (self.side , self.name ,
                                                                                    self.rtype) ,
                                               set_parent = 'jnt_set')
            # 吸附绑定关节与定位关节的位置
            cmds.matchTransform (jnt , bpjnt)
        # 将bp关节放到bp关节组里隐藏
        for bpjnt in self.bpjnt_list :
            hierarchyUtils.Hierarchy.parent (bpjnt , self.top_bpjnt_grp)


    # 根据绑定关节来创建对应的控制器
    def create_ctrl (self) :
        u"""
        根据绑定关节来创建对应的控制器
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

        # 对控制器组和关节组进行循环，创建对应关节的控制器以及吸附到对应的位置
        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            self.ctrl = controlUtils.Control.create_ctrl (ctrl , shape = self.shape ,
                                                          radius = self.radius ,
                                                          axis = 'X+' , pos = jnt ,
                                                          parent = self.ctrl_grp)
            # 判断所创建的控制器的边，如果边为_r_的话，offset组需要修改镜像
            if self.side == 'r' :
                cmds.setAttr (ctrl.replace ('ctrl' , 'offset') + '.scaleX' , -1)


    # 对应的控制器与绑定关节之间创建连接
    def add_constraint (self) :
        '''
        对应的控制器与绑定关节之间创建连接
        '''
        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            pipelineUtils.Pipeline.create_constraint (ctrl.replace (' ctrl' , 'output') , jnt ,
                                                      point_value = False ,
                                                      orient_value = False , parent_value = True , scale_value =
                                                      True ,
                                                      mo_value = True)


    # 创建bp的定位关节,生成准备
    def build_setup (self) :
        """
        创建bp的定位关节,生成准备
        """
        # 根据给定的side，name等属性，创建名称进行规范整理
        self.create_namespace ()
        self.create_bpjnt ()


    # 根据生成的bp定位关节，创建绑定系统
    def build_rig (self) :
        """
        根据生成的bp定位关节，创建绑定系统
        """

        self.create_joint ()
        self.create_ctrl ()
        self.add_constraint ()


    # 删除已经创建好的绑定系统
    def delete_rig (self) :
        """
        删除已经创建好的绑定系统
        """
        # 删除已经创建好的关节
        for jnt in self.jnt_list :
            if cmds.objExists (jnt) :
                # 删除过去的关节后，再重新创建关节
                cmds.delete (jnt)
        else :
            pass
        # 如果对应的控制器组存在则删除控制器组
        if cmds.objExists (self.ctrl_grp) :
            cmds.delete (self.ctrl_grp)
        else :
            pass
