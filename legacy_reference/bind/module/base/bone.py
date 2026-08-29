# coding=utf-8
from __future__ import unicode_literals , print_function

import logging
import os
from importlib import reload


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

import maya.cmds as cmds
from ....core import controlUtils , hierarchyUtils , jointUtils , pipelineUtils , connectionUtils


reload (connectionUtils)


class Bone (object) :
    """
   骨骼绑定的类，用于在Maya中创建骨骼绑定系统。
    帮助文档请参考：
    https://www.yuque.com/yuqueyonghur5eqgu/qev20s/nsdlrea8e8q88qai?singleDoc#《bone.py》
   主要分为两个阶段：build_setup() 和 build_rig()。
   build_setup() 阶段用于创建骨骼绑定的准备工作，包括创建定位的bp关节和整理命名空间。
   build_rig() 阶段用于根据定位的bp关节创建实际的绑定系统，包括创建绑定关节、控制器和约束。

   Attributes:
       TOP_GROUP_NAMES (list): 最高层级组的名称列表。
       rig_type (str): 生成的绑定类型。
       shape (str): 控制器的形状。
       radius (int): 控制器的半径。

   Args:
       side (str): 侧面，通常是 'l' 或 'r'。
       name (str): 模块的名称。
       jnt_number (int): 关节的数量。
       jnt_parent (str, optional): 生成的关节的父层级，默认为 None。
       ctrl_parent (str, optional): 生成的控制器的父层级，默认为 None。
   """

    TOP_GROUP_NAMES = [
        'grp_m_group_001' ,
        'grp_m_bpjnt_001' ,
        'grp_m_control_001' ,
        'grp_m_jnt_001' ,
        'grp_m_mesh_001' ,
        'grp_m_node_001'
    ]
    rig_type = 'bone'
    shape = 'circle'
    radius = 10


    def __init__ (self , side , name , jnt_number , jnt_parent = None , ctrl_parent = None) :
        """
        根据给定的变量创建关节和控制器

        :param side(str): 关节的边
        :param name(str): 关节的模块名称
        :param jnt_number(int): 关节的数量
        :param jnt_parent(str): 生成的关节的父层级
        :param ctrl_parent(str): 生成的控制器的父层级
        """
        # 初始化最高层级组结构
        self._setup_top_groups ()

        # 初始化组件的边和关节数量
        self.side = side
        self.name = name
        self.jnt_number = jnt_number

        # 设置关节的父层级和控制器的父层级
        self.jnt_parent = jnt_parent
        self.ctrl_parent = ctrl_parent
        # 初始化组件的输入的参数
        self._init_parameter ()

        # 根据给定的边，名称和jnt_number生成列表来存储创建的名称
        self._setup_list ()

        # 创建一个logger日志用来排查错误
        # 创建logger日志来排查错误
        self._setup_logger ()


    # 根据给定的side，name等属性，创建名称进行规范整理
    def create_namespace (self) :
        """
        根据给定的side，name等属性，创建名称进行规范整理。

        根据给定的side，name等属性，生成名称规范整理列表，包括基础的和额外的名称规范列表。
        最终，创建基础的名称规范整理列表，所有组件都需要用到的名称规范列表。
        同时，创建额外的名称规范列表，特殊组件需要创建的名称规范列表，例如脚掌的额外关节定位，脸部多余关节与控制器等等。

        Returns:
            None
        """
        # 初始化额外的绑定模块
        self._init_extra ()

        # 创建基础的名称规范整理列表，所有组件都需要用到的名称规范列表
        self._create_base_namespace ()

        # 创造额外的名称规范列表，特殊组件需要创建的名称规范列表，例如脚掌的额外关节定位，脸部多余关节与控制器等等
        self._create_extra_namespace ()

        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}_{}   :  1.create_namespace,done!'.format (self.side , self.name , self.rig_type))


    def create_bpjnt (self) :
        """
        根据名称规范，创建定位的bp关节。

        根据名称规范，创建基础的定位的bp关节，所有组件都需要用到的定位关节。
        然后，根据名称规范，创建额外的定位的bp关节，例如脚掌的额外关节定位，脸部多余关节与控制器等等。
        最后，显示定位关节组。

        Returns:
            None
        """
        # 根据名称规范，创建基础的定位的bp关节，所有组件都需要用到的定位关节
        self._create_base_bpjnt ()

        # 根据名称规范，创建额外的定位的bp关节，例如脚掌的额外关节定位，脸部多余关节与控制器等等
        self._create_extra_bpjnt ()

        # 显示定位关节组
        self._set_bpjnt_vis (vis_bool = True)

        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}_{}   :  2.create_bpjnt,done!'.format (self.side , self.name , self.rig_type))


    def create_joint (self) :
        """
        根据定位的bp关节创建绑定关节。

        隐藏bp的定位关节，根据bp关节创建新的关节并断开所有属性链接，检查场景是否存在关节并删除，根据基础的bp关节创建基础蒙皮关节，
        然后根据额外的bp关节创建额外蒙皮关节，例如脚掌的额外关节定位，脸部多余关节与控制器等等。

        Raises:
            RuntimeError: 如果在创建关节的过程中出现运行时错误，则抛出异常。
        """

        # 隐藏bp的定位关节
        self._set_bpjnt_vis (vis_bool = 0)

        # 检查已经创建的定位关节是否符合要求
        self._cheek_jnt_list ()

        # 根据基础的定位的bp关节，所有组件都需要用到的定位关节，创建基础的蒙皮关节
        self._create_base_joint ()

        # 根据额外的定位的bp关节，创建额外的蒙皮关节，例如脚掌的额外关节定位，脸部多余关节与控制器等等
        self._create_extra_joint ()

        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}_{}   :  3.create_joint,done!'.format (self.side , self.name , self.rig_type))


    # 根据绑定关节来创建对应的控制器
    def create_ctrl (self) :
        """
        根据绑定关节来创建对应的控制器。

        使用给定的形状创建整体的控制器层级组，并根据基础蒙皮关节创建基础控制器，然后根据额外蒙皮关节创建额外控制器。

        Raises:
            RuntimeError: 如果在创建控制器过程中出现运行时错误，则抛出异常。
        """

        # 设置控制器形状
        self._set_shape (self.shape)

        # 创建整体的控制器层级组
        # 判断场景里是否已经存在对应的控制器，重建的情况
        self._create_ctrl_grp ()

        # 根据基础的蒙皮关节，创建对应的基础控制器
        self._create_base_ctrl ()

        # 根据额外的蒙皮关节，创建额外的控制器
        self._create_extra_ctrl ()

        # 创建整理层级控制器组的层级结构
        self._create_ctrl_hierarchy ()

        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}_{}   :  4.create_ctrl,done!'.format (self.side , self.name , self.rig_type))


    # 对应的控制器与绑定关节之间创建连接
    def create_constraint (self) :
        """
        对应的控制器与绑定关节之间创建连接。

        使用基础控制器与蒙皮关节之间的索引信息，以及额外控制器与额外关节之间的信息，分别创建连接约束。

        Raises:
            RuntimeError: 如果创建连接约束过程中出现运行时错误，则抛出异常。
        """

        # 在基础的控制器与蒙皮关节之间创建连接
        self._create_base_constraint ()

        # 在额外的控制器与额外的关节之间创建连接
        self._create_extra_constraint ()

        # 创建logging用来记录日志
        self.logger.debug (u'{}_{}_{}   :  5.create_constraint,done!'.format (self.side , self.name , self.rig_type))


    # 创建bp的定位关节,生成准备
    def build_setup (self) :
        """
        创建bp的定位关节,生成准备。

        调用 create_namespace 和 create_bpjnt 函数，根据给定的 side，name 等属性创建名称进行规范整理，
        并创建bp的定位关节，用于生成准备。

        Returns:
            None
        """
        # 根据给定的 side，name 等属性，创建名称进行规范整理
        self.create_namespace ()
        self.create_bpjnt ()

        # 创建logging用来记录日志
        self.logger.info (u'{}_{}_{}    :  ---build_setup---,done!'.format (self.side , self.name , self.rig_type))
        self.logger.debug ('\n')


    # 根据生成的bp定位关节，创建绑定系统
    def build_rig (self) :
        """
        根据生成的bp定位关节，创建绑定系统。

        调用 create_joint、create_ctrl 和 create_constraint 函数，
        根据生成的 bp 定位关节，创建绑定系统。

        Returns:
            None
        """
        # 创建绑定系统的关节、控制器和约束
        self.create_joint ()
        self.create_ctrl ()
        self.create_constraint ()

        # 创建logging用来记录日志
        self.logger.info (u'{}_{}_{}    :  ---build_rig---,done!'.format (self.side , self.name , self.rig_type))
        self.logger.debug ('\n')


    # 删除已经创建好的绑定系统
    def delete_rig (self) :
        """
        删除已经创建好的绑定系统。

        删除已经创建好的定位关节、关节和控制器组。删除之后重新创建关节。

        Returns:
            None
        """
        # 重新显示出已经创建好的定位关节
        self._set_bpjnt_vis(vis_bool = True)
        # 删除已经创建好的关节
        for jnt in self.jnt_list :
            if cmds.objExists (jnt) :
                # 删除过去的关节后，再重新创建关节
                cmds.delete (jnt)

        # 删除控制器组
        if cmds.objExists (self.ctrl_grp) :
            cmds.delete (self.ctrl_grp)

        # 创建logging用来记录日志
        self.logger.info (u'{}_{}_{}    :   ---delete_rig---,done!'.format (self.side , self.name , self.rig_type))
        self.logger.debug ('\n')


    # 初始化最高层级组结构
    def _setup_top_groups (self) :
        """
        初始化最高层级组结构。

        如果最高层级组结构已存在，则直接使用已存在的组名称。
        否则，通过调用 Hierarchy 模块的 create_rig_grp 函数来创建最高层级的组结构。

        Returns:
            None
        """
        if cmds.objExists (self.TOP_GROUP_NAMES [0]) :
            # 如果已存在最高层级组结构，则直接使用已存在的组名称
            self.top_main_group = 'grp_m_group_001'
            self.top_bpjnt_grp = 'grp_m_bpjnt_001'
            self.top_ctrl_grp = 'grp_m_control_001'
            self.top_jnt_grp = 'grp_m_jnt_001'
            self.top_mesh_grp = 'grp_m_mesh_001'
            self.top_node_grp = 'grp_m_node_001'
        else :
            # 如果不存在最高层级组结构，则创建新的组结构
            hierarchy_names = hierarchyUtils.Hierarchy.create_rig_grp ()
            self.top_bpjnt_grp , self.top_ctrl_grp , self.top_jnt_grp , self.top_mesh_grp , self.top_node_grp , self.top_main_group = hierarchy_names


    # # 根据给定的边，名称和jnt_number生成列表来存储创建的名称
    def _setup_list (self) :
        """
        根据给定的边，名称和jnt_number生成列表来存储创建的名称。

        根据给定的边，名称和关节数量(jnt_number)，初始化多个列表用于存储不同类型的名称。
        这些列表包括 bpjnt_list, jnt_list, zero_list, driven_list, connect_list, offset_list, ctrl_list, subctrl_list,
        output_list，以及 ctrl_grp。

        Returns:
            None
        """
        # 根据给定的边，名称和关节数量(jnt_number)生成列表来存储创建的名称
        self.bpjnt_list = list ()
        self.jnt_list = list ()
        self.zero_list = list ()
        self.driven_list = list ()
        self.connect_list = list ()
        self.offset_list = list ()
        self.ctrl_list = list ()
        self.subctrl_list = list ()
        self.output_list = list ()

        # 额外的关节列表
        self.extra_bpjnt_list = list ()
        self.extra_jnt_list = list ()


    def _init_parameter (self) :
        """
        初始化组件的输入的参数
        """
        # 判断当没有输入关节的父层级或者关节的父层级不存在于场景里的时候，则将关节父层级自动设置成为世界的关节总组
        if not self.jnt_parent or not cmds.objExists (self.jnt_parent) :
            self.jnt_parent = self.top_jnt_grp

        # 判断当没有输入控制器的父层级或者控制器的父层级不存在于场景里的时候，则将控制器父层级自动设置成为世界的控制器总组
        if not self.ctrl_parent or not cmds.objExists (self.ctrl_parent) :
            self.ctrl_parent = self.top_ctrl_grp

        # 根据给定的边，初始化side_value的值，用于镜像控制器以及位移
        self._setup_side_value ()


    # 根据给定的边，初始化side_value的值，用于镜像控制器以及位移
    def _setup_side_value (self) :
        '''
        根据给定的边，初始化side_value的值，用于镜像控制器以及位移。

        根据给定的边，设置side_value的值，用于在镜像控制器和位移时确定方向。

        Returns:
            int: side_value的值，1表示左侧，-1表示右侧，0表示无效值。
        '''
        # 判断边为'l'还是'r'
        if self.side == 'l' :
            self.side_value = 1
        elif self.side == 'r' :
            self.side_value = -1
        else :
            self.side_value = 0


    # 创建一个logger日志用来排查错误
    # 创建logger日志来排查错误
    def _setup_logger (self) :
        """
        创建一个logger日志用来排查错误。

        创建一个logger日志来排查错误，设置日志文件名、格式和日志级别。

        Returns:
            logging.Logger: 创建的logger实例
        """
        self.logger_name = f'{self.__class__.__name__}_logger'

        # 获取 log/bind.log 文件的绝对路径
        self.file_name = os.path.abspath (__file__ + "/../../../../log/bind.log")

        # 使用 Pipeline 模块中的函数创建日志记录
        pipelineUtils.Pipeline.create_logging (logger_name = self.logger_name , file_name = self.file_name ,
                                               formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 获取 logger 实例
        self.logger = logging.getLogger (self.logger_name)
        self.logger.setLevel (logging.DEBUG)


    # 设置bp关节的可见性，用于切换状态，当绑定系统创建完成的时候设置bp关节为隐藏状态，当绑定系统删除的时候则设置bp关节为显示状态
    def _set_bpjnt_vis (self , vis_bool = False) :
        """
        设置bp关节的可见性，用于切换状态，当绑定系统创建完成的时候设置bp关节为隐藏状态，当绑定系统删除的时候则设置bp关节为显示状态
        vis_bool(bool):bp关节的可见性,0为不可见，1为可见
        """
        # 设置bp关节组的可见性
        cmds.setAttr (self.top_bpjnt_grp + '.visibility' , vis_bool)


    # 设置控制器形状
    def _set_shape (self , shape) :
        u'''
        设置控制器形状
        '''
        self.shape = shape


    # 初始化额外的绑定模块
    def _init_extra (self) :
        '''
        初始化额外的绑定模块
        '''
        pass


    # 创建基础的名称规范整理列表,所有组件都需要用到的名称规范列表
    def _create_base_namespace (self) :
        '''
        创建基础的名称规范整理列表,所有组件都需要用到的名称规范列表
        self.bpjnt_list = list ()
        self.jnt_list = list ()
        self.zero_list = list ()
        self.driven_list = list ()
        self.connect_list = list ()
        self.offset_list = list ()
        self.ctrl_list = list ()
        self.subctrl_list = list ()
        self.output_list = list ()

        Parameters:
            index (int): 索引值，用于生成规范名称的数字部分。

        Returns:
            None
        '''

        # 对关节的数量做循环，来创建需要创建的名称规范列表
        for index in range (self.jnt_number) :
            self.bpjnt_list.append ('bpjnt_{}_{}{}_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))
            self.jnt_list.append ('jnt_{}_{}{}_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))
            self.zero_list.append ('zero_{}_{}{}_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))
            self.driven_list.append ('driven_{}_{}{}_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))
            self.connect_list.append (
                'connect_{}_{}{}_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))
            self.offset_list.append ('offset_{}_{}{}_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))
            self.ctrl_list.append ('ctrl_{}_{}{}_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))
            self.subctrl_list.append (
                'ctrl_{}_{}{}Sub_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))
            self.output_list.append ('output_{}_{}{}_{:03d}'.format (self.side , self.name , self.rig_type , index + 1))

        # 控制器组的名称
        self.ctrl_grp = 'grp_{}_{}{}Ctrl_001'.format (self.side , self.name , self.rig_type)


    # 创造额外的名称规范列表，特殊组件需要创建的名称规范列表，例如脚掌的额外关节定位，脸部多余关节与控制器等等
    def _create_extra_namespace (self) :
        '''
        创造额外的名称规范列表，特殊组件需要创建的名称规范列表，例如脚掌的额外关节定位，脸部多余关节与控制器等等
        '''
        pass


    # 根据名称规范，创建基础的定位的bp关节,所有组件都需要用到的定位关节
    def _create_base_bpjnt (self) :
        '''
        根据名称规范，创建基础的定位的bp关节，所有组件都需要用到的定位关节

        Returns:
            None
        '''
        for index , bpjnt in enumerate (self.bpjnt_list) :
            # 创建单个bp关节
            self._create_single_bpjnt (bpjnt , index , parent = self.top_bpjnt_grp)

        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.bpjnt_list)


    # 根据名称规范，创建额外的定位的bp关节,例如脚掌的额外关节定位，脸部多余关节与控制器等等
    def _create_extra_bpjnt (self) :
        '''
        根据名称规范，创建额外的定位的bp关节,例如脚掌的额外关节定位，脸部多余关节与控制器等等
        '''
        pass


    # 创建单个bp关节
    def _create_single_bpjnt (self , bpjnt , index , parent) :
        """
        创建单个bp关节。

        Parameters:
            bpjnt (str): 定位的bp关节的名称。
            index (int): 关节的索引，用于生成唯一的名称。
            parent (str): 父层级的名称。

        Returns:
            None
        """
        # 判断是否已经生成过定位关节，如果没有生成过定位关节的话则生成定位关节
        if cmds.objExists (bpjnt) :
            cmds.delete (bpjnt)
        else :
            # 创建bp关节
            self.bpjnt = cmds.createNode ('joint' , name = bpjnt , parent = parent)

            # 设置bp关节的位置，防止多个关节聚集在一起不好选择
            cmds.setAttr (self.bpjnt + '.translateX' , index * 5)

            # 给bp定位关节设置颜色方便识别
            cmds.setAttr (self.bpjnt + '.overrideEnabled' , 1)
            cmds.setAttr (self.bpjnt + '.overrideColor' , 13)

            # 将bp关节添加到选择集里方便进行选择
            pipelineUtils.Pipeline.create_set (
                self.bpjnt ,
                set_name = 'set_{}_{}{}Bpjnt_001'.format (self.side , self.name , self.rig_type) ,
                set_parent = 'bpjnt_set'
            )
        return self.bpjnt

        # 判断场景里是否已经存在对应的关节，重建的情况,当之前的关节存在于场景中的时候进行删除


    def _cheek_jnt_objExists (self , jnt_list) :
        """
            检查关节是否已存在，如果存在则删除。

            遍历关节列表，检查每个关节是否已存在于场景中，如果存在则删除。

            Raises:
                RuntimeError: 如果在删除关节过程中出现运行时错误，则抛出异常。
            """
        # 判断，当jnt_list列表里面有值的时候则进行下一步操作，删除已经存在的蒙皮关节
        if jnt_list :
            # 删除已存在的关节
            try :
                for jnt in jnt_list :
                    if cmds.objExists (jnt) :
                        cmds.delete (jnt)
            except RuntimeError as e :
                raise RuntimeError (f"删除关节过程中出现运行时错误. Error: {str (e)}")
        # 判断，当jnt_list列表里面没有值的时候则跳过
        else :
            pass


    # 检查关节列表的连接，如果有多余的属性连接的话则断掉
    def _cheek_bpjnt_connect (self , jnt_list) :
        """
        检查定位关节列表的连接，如果有多余的属性连接的话则断掉
        """
        # 判断，当jnt_list列表里面有值的时候则检查关节列表的连接
        if jnt_list :
            try :
                # 遍历bp关节列表，对每个bp关节的平移、旋转和缩放属性进行检查，如果存在连接，则断开连接
                for jnt in jnt_list :
                    con = connectionUtils.Connection ()
                    con.disconnect_attributes (node = jnt , attribute_list = ['.translate' , '.rotate' , '.scale'])
            except RuntimeError as e :
                raise RuntimeError (f"断开连接时发生错误。错误信息: {str (e)}")
        # 判断，当jnt_list列表里面没有值的时候则跳过
        else :
            pass


    def _cheek_jnt_list (self) :
        """
        检查已经创建的定位关节是否符合要求
        """

        # 检查基础的蒙皮关节是否已经存在于场景中
        self._cheek_jnt_objExists (self.jnt_list)
        # 检查基础的定位关节是否有节点连接
        self._cheek_bpjnt_connect (self.bpjnt_list)

        # 检查额外的蒙皮关节是否已经存在于场景中
        self._cheek_jnt_objExists (self.extra_jnt_list)
        # 检查额外的定位关节是否有节点连接
        self._cheek_bpjnt_connect (self.extra_bpjnt_list)


    # 根据给定的bp关节位置创建绑定关节，吸附到对应位置，并创建用于整理的集合
    def _create_and_attach_joint (self , bpjnt , jnt) :
        """
        根据给定的bp关节位置创建绑定关节，吸附到对应位置，并创建用于整理的集合
        """
        # 场景里没有存在对应的关节，第一次创建绑定的情况
        jnt = cmds.createNode ('joint' , name = jnt , parent = self.jnt_parent)

        # 将蒙皮关节添加到选择集以便于选择
        pipelineUtils.Pipeline.create_set (
            jnt ,
            set_name = '{}_{}{}_jnt_set'.format (self.side , self.name , self.rigType) ,
            set_parent = 'jnt_set'
        )

        # 吸附绑定关节与定位关节的位置
        cmds.matchTransform (jnt , bpjnt)


    # 根据基础的定位的bp关节,所有组件都需要用到的定位关节,创建基础的蒙皮关节
    def _create_base_joint (self) :
        """
        根据bpjnt的位置，创建对应的基础关节并吸附到对应位置，并创建用来整理的集合。

        使用给定的bpjnt位置列表，为每个bpjnt创建对应的基础关节，并将其吸附到对应的位置。同时，创建一个用于整理的集合。

        Raises:
            RuntimeError: 如果在创建基础关节或集合过程中出现运行时错误，则抛出异常。
        """

        # 根据bpjnt的位置，创建对应的基础关节并吸附到对应位置
        # 同时，创建一个用于整理的集合
        try :
            for bpjnt , jnt in zip (self.bpjnt_list , self.jnt_list) :
                self._create_and_attach_joint (bpjnt , jnt)
        except RuntimeError as e :
            raise RuntimeError (f"Failed to create and attach base joints or collection. Error: {str (e)}")


    # 根据额外的定位的bp关节,创建额外的蒙皮关节，例如脚掌的额外关节定位，脸部多余关节与控制器等等，
    def _create_extra_joint (self) :
        '''
        根据额外的定位的bp关节,创建额外的蒙皮关节，例如脚掌的额外关节定位，脸部多余关节与控制器等等，
        '''
        pass


    ## 创建整体的控制器层级组
    # 判断场景里是否已经存在对应的控制器，重建的情况
    def _create_ctrl_grp (self) :
        """
        创建整体的控制器层级组。

        判断场景里是否已经存在对应的控制器层级组，若存在则删除过去的并重新创建，否则直接创建新的控制器层级组。

        Raises:
            RuntimeError: 如果在创建或删除控制器层级组过程中出现运行时错误，则抛出异常。
        """

        # 创建整体的控制器层级组
        # 判断场景里是否已经存在对应的控制器，重建的情况

        if cmds.objExists (self.ctrl_grp) :
            try :
                # 删除过去的控制器层级组并重新创建
                cmds.delete (self.ctrl_grp)
                self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.ctrl_parent)
            except RuntimeError as e :
                raise RuntimeError (f"Failed to delete or recreate control group. Error: {str (e)}")
        else :
            # 直接创建新的控制器层级组
            self.ctrl_grp = cmds.createNode ('transform' , name = self.ctrl_grp , parent = self.ctrl_parent)


    # 根据给定的控制器和关节创建控制器，吸附到对应位置，并根据边的情况进行调整
    def _create_and_attach_controller (self , ctrl , jnt , parent , axis = 'X+') :
        """
        根据给定的控制器和关节创建控制器，吸附到对应位置，并根据边的情况进行调整

        Parameters:
            ctrl (str): 控制器的名称。
            jnt (str): 关节的名称。
            axis(str): 关节的轴向
            parent (str): 控制器的父层级。

        Returns:
            str: 创建的控制器的名称。
        """
        # 使用控制器工具类创建控制器
        created_ctrl = controlUtils.Control.create_ctrl (
            ctrl , shape = self.shape , radius = self.radius , axis = axis , pos = jnt , parent = parent
        )

        return created_ctrl


    # 根据基础的蒙皮关节,创建对应的基础控制器
    def _create_base_ctrl (self) :
        """
        根据基础的蒙皮关节，创建对应的基础控制器。

        对控制器组和关节组进行循环，为每个基础蒙皮关节创建对应的控制器，并将其吸附到关节的位置。

        Raises:
            ValueError: 如果创建控制器过程中出现参数错误，则抛出异常。
        """

        # 对控制器组和关节组进行循环，创建对应关节的控制器以及吸附到对应的位置
        # 使用函数进行创建和吸附控制器
        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            # 调用函数创建并吸附控制器
            self.ctrl = self._create_and_attach_controller (ctrl , jnt , parent = self.ctrl_grp)


    # 根据额外的蒙皮关节，创建额外的控制器
    def _create_extra_ctrl (self) :
        '''
        根据额外的蒙皮关节，创建额外的控制器
        '''
        pass


    def _create_ctrl_hierarchy (self) :
        '''
        # 创建整理层级控制器组的层级结构
        '''
        pass


    # 根据给定的控制器和关节创建约束关系
    def _create_controller_constraint (self , ctrl , jnt) :
        """
        根据给定的控制器和关节创建约束关系。

        使用管道工具类 Pipeline.create_constraint 函数创建约束关系，连接控制器的输出到关节。

        :param ctrl(str): 控制器的名称。
        :param jnt(str): 关节的名称。
        """
        # 使用管道工具类创建约束
        pipelineUtils.Pipeline.create_constraint (
            ctrl.replace (' ctrl' , 'output') , jnt ,
            point_value = False , orient_value = False , parent_value = True , scale_value = True , mo_value = True
        )


    # 在基础的控制器与蒙皮关节之间创建连接
    def _create_base_constraint (self) :
        """
        根据给定的控制器和关节创建基础的约束关系。

        对每个控制器和关节的组合调用 _create_controller_constraint 函数，创建约束关系。

        Returns:
            None
        """
        # 根据给定的控制器和关节创建约束关系
        for ctrl , jnt in zip (self.ctrl_list , self.jnt_list) :
            self._create_controller_constraint (ctrl , jnt)


    # 在额外的控制器与额外的关节之间创建连接
    def _create_extra_constraint (self) :
        '''
        在额外的控制器与额外的关节之间创建连接
        '''
        pass
