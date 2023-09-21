import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils
from importlib import reload
import maya.cmds as cmds


class Joint_Tool () :
    """
    一个关节工具的类
    """


    def __init__ (self , *args , **kwargs) :
        super ().__init__ (*args , **kwargs)
        self.win_name = 'Joint_Tool'
        self.win_title = 'Joint_Tool(关节工具)'
        self.init_ui ()


    def init_ui (self) :
        # 创建ui界面
        self.main_window = pm.window (self.win_title , width = 300 , height = 500)

        pm.scrollLayout ()
        # 创建装备fk的ui界面
        pm.frameLayout (label = 'create_FK(装配FK)' ,
                        collapsable = True)

        pm.rowColumnLayout (numberOfColumns = 2)

        pm.button (label = 'create_fk(创建fk)' , command = lambda *a : print ('create_fk(创建fk)'))
        pm.button (label = 'delete_fk(删除fk)' , command = lambda *a : print ('delete_fk(删除fk)'))
        pm.setParent ('..')
        pm.setParent ('..')

        # 创建装备ik的ui界面
        pm.frameLayout (label = 'create_IK(装配IK)' ,
                        collapsable = True)
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
        pm.button (label = 'create_IK(创建IK)' , command = lambda *a : None)
        pm.button (label = 'create_IK(删除IK)' , command = lambda *a : None)
        pm.setParent ('..')

        # 创建装备ik链条的ui界面
        pm.frameLayout (label = 'create_IK_Spine(装配IK链条绑定)' ,
                        collapsable = True)
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

        pm.button (label = 'create_IK(创建IK)' , command = lambda *a : None)
        pm.button (label = 'delete_IK(删除IK)' , command = lambda *a : None)
        pm.setParent ('..')

        # 创建关节小工具的ui界面
        pm.frameLayout (label = 'joint_tool(关节小工具)' ,
                        collapsable = True)
        # 设置关节显示
        self.jnt_size = pm.floatSliderGrp ('jnt_Size' , label = 'jnt_size(关节显示大小):' , f = True , min = 1 , max = 10 , fmn = 1 ,
                           fmx = 100 ,
                           v = 1)
        pm.rowColumnLayout (numberOfColumns = 3)
        pm.button (label = 'create_IK(创建IK)' , command = lambda *a : None)
        pm.button (label = 'create_IK(创建IK)' , command = lambda *a : None)
        pm.button (label = 'create_IK(创建IK)' , command = lambda *a : None)

        self.main_window.show ()


def show () :
    try :
        cmds.deleteUI (joint_tool.win_title)
        cmds.delete (joint_tool)
    except :
        pass
    joint_tool = Joint_Tool ()
