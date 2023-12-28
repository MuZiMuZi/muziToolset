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
import os
import maya.cmds as cmds

from ....core import jointUtils , pipelineUtils , connectionUtils
from ..base import base
from importlib import reload


reload (connectionUtils)
reload (jointUtils)
reload (base)


class ChainItem (base.BaseItem) :

    def __init__ (self , name = 'chain') :
        """Override"""
        super (ChainItem , self).__init__ (name)
        self.extra_ui = 'chain.ui'
        self.init_extra ()


    # 初始化作为QWidget对象的extra_widget属性,用于设置绑定组件的特殊属性，比如(长度，朝向，拉伸，IK启用，FK启用,twist启用)等属性
    # （Length, orientation, stretch, IK enabled, FK enabled, twist enabled）

    def create_extra_widget (self) :
        """
        #初始化作为QWidget对象的extra_widget属性,用于设置绑定组件的特殊属性，比如(长度，朝向，拉伸，IK启用，FK启用,twist启用)等属性
        #（Length, orientation, stretch, IK enabled, FK enabled, twist enabled）
        """
        self.extra_widget = QWidget ()
        uic.loadUi (os.path.join (UI_DIR , self.extra_ui) , self.extra_widget)

        for direction in Direction :
            self.extra_widget.length_sbox.addItem (str (direction.value))


    def parse_extra (self) :
        """Override"""
        seg = self.extra_widget.ui_seg_sbox.value ()
        length = self.extra_widget.ui_len_sbox.value ()
        direction = ast.literal_eval (self.extra_widget.ui_dir_cbox.currentText ())

        return [seg , length , direction]


class Chain (base.Base) :


    def __init__ (self , side , name , jnt_number , length = 10 , jnt_parent = None , ctrl_parent = None) :
        '''
        length：关节的总长度
        
        '''
        base.Base.__init__ (self , side , name , jnt_number , jnt_parent , ctrl_parent)

        self.rtype = 'Chain'

        self.length = length
        self.interval = None
        self.direction = None
        self.curve = None


    def create_bpjnt (self) :
        """
        创建定位的bp关节
        """
        # 设置bpjnt创建出来的位置放置在top_bpjnt_grp的层级下
        self.jnt_parent = self.top_bpjnt_grp
        for bpjnt in self.bpjnt_list :
            # 判断是否已经生成过定位关节，如果没有生成过定位关节的话则生成定位关节
            if cmds.objExists (bpjnt) :
                cmds.delete (bpjnt)
            else :
                self.bpjnt = cmds.createNode ('joint' , name = bpjnt , parent = self.jnt_parent)
                # 给bp定位关节设置颜色方便识别
                cmds.setAttr (self.bpjnt + '.overrideEnabled' , 1)
                cmds.setAttr (self.bpjnt + '.overrideColor' , 13)
                # 指定关节的父层级为上一轮创建出来的关节
                self.jnt_parent = self.bpjnt
                # 调整距离,调整关节的朝向距离
                #获取关节的位置信息，例如self.interval是关节的长度，self。direction是空间位置比如[0.0, 1, 0.0]
                #他们相乘获得到distance，将关节为位移到对应的位置信息上
                distance = [element * self.interval for element in self.direction]
                pipelineUtils.Pipeline.move (bpjnt, distance)
                # 将bp关节添加到选择集里方便进行选择
                pipelineUtils.Pipeline.create_set (self.bpjnt ,
                                                   set_name = '{}_{}{}_bpjnt_set'.format (self.side , self.name ,
                                                                                          self.rtype) ,
                                                   set_parent = 'bpjnt_set')
        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.bpjnt_list)
        cmds.setAttr (self.bpjnt_list [0] + '.translateX' , 0)


    def create_joint (self) :
        '''
        根据定位的bp关节创建关节
        '''
        # 根据bp关节创建新的关节
        for bpjnt in self.bpjnt_list :
            # 断掉上面的属性链接
            connectionUtils.Connection.disconnect_attributes (bpjnt , ['.translate' , '.rotate' , '.scale'])

        # 判断场景里是否已经存在对应的关节，重建的情况
        if cmds.objExists (self.jnt_list [0]) :
            # 删除过去的关节后，并重新创建关节
            cmds.delete (self.jnt_list [0])
        else :
            pass
        for bpjnt , jnt in zip (self.bpjnt_list , self.jnt_list) :
            # 场景里没有存在对应的关节，第一次创建绑定的情况
            self.jnt = cmds.createNode ('joint' , name = jnt , parent = self.jnt_parent)
            cmds.matchTransform (jnt , bpjnt)
            # 指定关节的父层级为上一轮创建出来的关节
            self.jnt_parent = self.jnt
            # 将蒙皮关节添加到选择集里方便进行选择
            pipelineUtils.Pipeline.create_set (jnt ,
                                               set_name = '{}_{}{}_jnt_set'.format (self.side , self.name ,
                                                                                    self.rtype) ,
                                               set_parent = 'jnt_set')

        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.jnt_list)
