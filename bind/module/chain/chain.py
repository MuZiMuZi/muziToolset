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
import maya.cmds as cmds

from ....core import jointUtils , pipelineUtils , connectionUtils
from ..base import base
from importlib import reload


reload (connectionUtils)
reload (jointUtils)
reload (base)


class Chain (base.Base) :
    rigType = 'Chain'


    def __init__ (self , side , name , jnt_number , length = 10 , jnt_parent = None , ctrl_parent = None) :
        '''
        length：关节的总长度
        
        '''
        super ().__init__ (side , name , jnt_number , jnt_parent , ctrl_parent)
        self.length = length
        self.interval = None
        self.direction = None
        self.curve = None


    def create_bpjnt (self) :
        """
        创建定位的bp关节
        """
        # 设置bpjnt创建出来的位置放置在top_bpjnt_grp的层级下
        self.bpjnt_parent = self.top_bpjnt_grp

        # 根据命名规范创建用来定位的bp关节
        for bpjnt in self.bpjnt_list :
            self._create_single_bpjnt (bpjnt)
        # 进行关节定向
        jointUtils.Joint.joint_orientation (self.bpjnt_list)
        cmds.setAttr (self.bpjnt_list [0] + '.translateX' , 0)


    # 创建单个bp关节
    def _create_single_bpjnt (self , bpjnt , index) :
        """
           创建单个bp关节
           """
        # 判断是否已经生成过定位关节，如果没有生成过定位关节的话则生成定位关节
        if cmds.objExists (bpjnt) :
            cmds.delete (bpjnt)
        else :
            self.bpjnt = cmds.createNode ('joint' , name = bpjnt , parent = self.bpjnt_parent)
            # 给bp定位关节设置颜色方便识别
            cmds.setAttr (self.bpjnt + '.overrideEnabled' , 1)
            cmds.setAttr (self.bpjnt + '.overrideColor' , 13)

            # 调整距离,调整关节的朝向距离
            # 获取关节的位置信息，例如self.interval是关节的长度，self.direction是空间位置比如[0.0, 1, 0.0]
            # 他们相乘获得到distance，将关节为位移到对应的位置信息上
            distance = [element * self.interval for element in self.direction]
            pipelineUtils.Pipeline.move (bpjnt , distance)

            # 将bp关节添加到选择集里方便进行选择
            pipelineUtils.Pipeline.create_set (self.bpjnt ,
                                               set_name = '{}_{}{}_bpjnt_set'.format (self.side , self.name ,
                                                                                      self.rigType) ,
                                               set_parent = 'bpjnt_set')

            # 指定关节的父层级为上一轮创建出来的关节
            self.bpjnt_parent = self.bpjnt


    ## 根据bpjnt的位置，创建对应的关节吸附到对应位置，并且创建用来整理的集合
    def _create_and_attach_joint (self , bpjnt , jnt) :
        for bpjnt , jnt in zip (self.bpjnt_list , self.jnt_list) :
            # 场景里没有存在对应的关节，第一次创建绑定的情况
            self.jnt = cmds.createNode ('joint' , name = jnt , parent = self.jnt_parent)
            cmds.matchTransform (jnt , bpjnt)
            # 指定关节的父层级为上一轮创建出来的关节
            self.jnt_parent = self.jnt
            # 将蒙皮关节添加到选择集里方便进行选择
            pipelineUtils.Pipeline.create_set (jnt ,
                                               set_name = '{}_{}{}_jnt_set'.format (self.side , self.name ,
                                                                                    self.rigType) ,
                                               set_parent = 'jnt_set')
