import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils
from importlib import reload

import maya.cmds as cmds


class Rig_Tool () :
    """
    一个绑定工具的类
    """


    def __init__ (self , *args , **kwargs) :
        super ().__init__ (*args , **kwargs)
        self.win_name = 'Rig_Tool'
        self.win_title = 'Rig_Tool(绑定工具)'
        self.init_ui ()


    def init_ui (self) :
        #############################################################
        # 创建ui界面
        #############################################################
        self.main_window = pm.window (self.win_title , width = 300 , height = 500)

        pm.scrollLayout ()
        # 添加各个模块工具的ui
        self.init_fk_ui ()
        self.init_ik_ui ()
        self.init_ikspine_ui ()


    def init_fk_ui (self) :
        #############################################################
        # 创建装备fk的ui界面
        #############################################################
        pm.frameLayout (label = '装配FK' ,
                        collapsable = True ,
                        backgroundColor = [0 , 0 , 20])

        pm.rowColumnLayout (numberOfColumns = 2)

        pm.button (label = '创建fk链条' , command = lambda *a : None)
        pm.button (label = '删除fk链条' , command = lambda *a : print ('delete_fk(1)'))
        pm.setParent ('..')
        pm.setParent ('..')


    def init_ik_ui (self) :
        #############################################################
        # 创建装备ik的ui界面
        #############################################################
        pm.frameLayout (label = '装配IK' ,
                        collapsable = True ,
                        backgroundColor = [0 , 0 , 20])
        pm.textFieldButtonGrp (label = '起始关节' ,
                               columnWidth3 = [50 , 140 , 5] ,
                               adjustableColumn = 2 ,
                               editable = False ,
                               buttonLabel = '拾取' ,
                               placeholderText = '请选择起始关节' ,
                               buttonCommand = lambda *a : None)

        pm.textFieldButtonGrp (label = '结束关节' ,
                               columnWidth3 = [50 , 140 , 5] ,
                               adjustableColumn = 2 ,
                               editable = False ,
                               buttonLabel = '拾取' ,
                               placeholderText = '请选择结束关节' ,
                               buttonCommand = lambda *a : None)
        pm.rowColumnLayout (numberOfColumns = 2)
        pm.button (label = '创建IK' , command = lambda *a : None)
        pm.button (label = '删除IK' , command = lambda *a : None)
        pm.setParent ('..')
        pm.setParent ('..')


    def init_ikspine_ui (self) :
        #############################################################
        # 创建装备ik链条的ui界面
        #############################################################
        pm.frameLayout (label = '装配IK链条绑定' ,
                        collapsable = True ,
                        backgroundColor = [0 , 0 , 20])
        pm.textFieldButtonGrp (label = '起始关节' ,
                               columnWidth3 = [50 , 140 , 5] ,
                               adjustableColumn = 2 ,
                               editable = False ,
                               buttonLabel = '拾取' ,
                               placeholderText = '请选择起始关节' ,
                               buttonCommand = lambda *a : None)

        pm.textFieldButtonGrp (label = '结束关节' ,
                               columnWidth3 = [50 , 140 , 5] ,
                               adjustableColumn = 2 ,
                               editable = False ,
                               buttonLabel = '拾取' ,
                               placeholderText = '请选择结束关节' ,
                               buttonCommand = lambda *a : None)
        pm.textFieldButtonGrp (label = '曲线' ,
                               columnWidth3 = [50 , 140 , 5] ,
                               adjustableColumn = 2 ,
                               editable = False ,
                               buttonLabel = '拾取' ,
                               placeholderText = '请选择spine曲线' ,
                               buttonCommand = lambda *a : None)

        pm.rowColumnLayout (numberOfColumns = 2)

        pm.button (label = '创建IK链条' , command = lambda *a : None)
        pm.button (label = '删除IK链条' , command = lambda *a : None)
        pm.setParent ('..')
        pm.setParent ('..')
