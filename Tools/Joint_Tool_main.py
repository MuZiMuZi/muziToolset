import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils
from importlib import reload

import maya.cmds as cmds


reload (jointUtils)
reload (pipelineUtils)


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
        #############################################################
        # 创建ui界面
        #############################################################
        self.main_window = pm.window (self.win_title , width = 300 , height = 500)

        pm.scrollLayout ()
        # 添加各个模块工具的ui
        self.init_joint_attr_ui ()
        self.init_add_joint_ui ()
        self.init_joint_tool_ui ()
        # self.main_window.show ()


    def init_joint_attr_ui (self) :
        ## 创建添加关节属性的ui界面
        pm.frameLayout (label = '关节属性' ,
                        collapsable = True ,
                        backgroundColor = [0 , 0 , 20])
        # pm.checkBox (label = '关节方向')
        cmds.iconTextCheckBox (style = 'iconAndTextHorizontal' , image1 = 'menuIconModify.png' , label = '关节方向')
        cmds.iconTextCheckBox (style = 'iconAndTextHorizontal' , image1 = 'kinJoint.png' , label = '关节定向')
        pm.setParent ('..')
        pm.setParent ('..')


    def init_add_joint_ui (self) :
        #############################################################
        # 创建添加关节工具的ui界面
        #############################################################
        pm.frameLayout (label = '添加关节' ,
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
        self.jnt_number = pm.intSliderGrp ('jnt_number' , label = '关节数量:' , f = True , min = 1 ,
                                           max = 100 , fmn = 1 ,
                                           fmx = 100 ,
                                           v = 1)
        pm.button (label = '执行' , command = lambda *a : None)
        pm.setParent ('..')
        pm.setParent ('..')


    def init_joint_tool_ui (self) :
        # 创建关节小工具的ui界面
        pm.frameLayout (label = '关节小工具' ,
                        collapsable = True ,
                        backgroundColor = [0 , 0 , 20])
        # 设置关节显示
        self.jnt_size = pm.floatSliderGrp ('jnt_Size' , label = '关节显示大小:' , f = True , min = 1 ,
                                           max = 10 , fmn = 1 ,
                                           fmx = 100 ,
                                           v = 1)
        pm.rowColumnLayout (numberOfColumns = 3)
        cmds.iconTextButton (style = 'iconAndTextHorizontal' , image1 = 'kinJoint.png' , label = '关节定向清零' ,
                             command = lambda *a : None)

        cmds.iconTextButton (style = 'iconAndTextHorizontal' , image1 = 'kinInsert.png' , label = '创建关节' ,
                             command = lambda *a : None)
        cmds.iconTextButton (style = 'iconAndTextHorizontal' , image1 = 'kinInsert.png' , label = '创建子关节' ,
                             command = lambda *a : None)
        cmds.iconTextButton (style = 'iconAndTextHorizontal' , image1 = 'kinInsert.png' , label = '组成关节链' ,
                             command = lambda *a : None)

        cmds.iconTextButton (style = 'iconAndTextHorizontal' , image1 = 'kinJoint.png' , label = '开启分段比例补偿' ,
                             command = lambda *a : None)
        cmds.iconTextButton (style = 'iconAndTextHorizontal' , image1 = 'kinJoint.png' , label = '关闭分段比例补偿' ,
                             command = lambda *a : None)
        pm.setParent ('..')
        pm.setParent ('..')


    def text_button (self) :
        jnts = cmds.ls (sl = True , type = 'joint')
        for jnt in jnts :
            jnt_obj = jointUtils.Joint_util (jnt)
            jnt_obj.get_AngleZ ()


def show () :
    try :
        cmds.deleteUI (joint_tool.win_title)
        cmds.delete (joint_tool)
    except :
        pass
    joint_tool = Joint_Tool ()
    joint_tool.main_window.show ()
