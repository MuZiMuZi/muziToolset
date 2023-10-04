import os
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import pymel.core as pm
from .config import ui_dir , icon_dir
from ..core import pipelineUtils , nameUtils , jointUtils , qtUtils
from importlib import reload

import maya.cmds as cmds


reload (qtUtils)


class Rig_Tool (QtWidgets.QWidget) :
    """
    一个绑定工具的类
    """


    def __init__ (self , parent = None) :
        super (Rig_Tool , self).__init__ (parent)
        self.win_name = 'Rig_Tool'
        self.win_title = 'Rig_Tool(绑定工具)'
        self.create_widgets ()
        self.create_layouts ()


    def create_widgets (self) :
        self.fk_label = QtWidgets.QLabel ('创建FK----------------' , self)
        self.create_fk_button = QtWidgets.QPushButton ('创建fk链条')
        self.delete_fk_button = QtWidgets.QPushButton ('删除fk链条')


        self.ik_start_button = QtWidgets.QPushButton ('拾取ik起始关节')
        self.ik_start_line = QtWidgets.QLineEdit()
        self.ik_end_button = QtWidgets.QPushButton ('拾取ik结束关节')
        self.ik_end_line = QtWidgets.QLineEdit ()
    def create_layouts (self) :
        #创建fk系统的layout
        self.fk_layout = QtWidgets.QFormLayout (self)
        self.fk_layout.addRow (self.fk_label)
        self.fk_layout.addRow (self.create_fk_button , self.delete_fk_button)

        #创建ik系统的layout
        self.ik_layout = QtWidgets.QFormLayout (self)
        self.ik_layout.addRow('起始关节',self.ik_start_line,self.ik_start_button)






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


def main () :
    return Rig_Tool ()


if __name__ == "__main__" :
    app = QApplication (sys.argv)
    mainwindow = Rig_Tool ()
    mainwindow.show ()
    sys.exit (app.exec_ ())
